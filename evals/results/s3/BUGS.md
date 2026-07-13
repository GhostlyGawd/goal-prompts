# Bug Hunt — 2026-07-13

No previous `BUGS.md` exists, so this is a first-pass report (no delta to report).

## Summary

6 findings, all confirmed against the running code (4 empirically reproduced via a throwaway unittest harness, 2 by direct code inspection). Repo is a ~110-line toy "webshop" (cart → checkout → JSON-file order log), so blast radius is small, but two of the bugs are the kind that silently corrupts money/inventory data rather than just crashing loudly.

**Scariest finding:** `Cart.add("apple", -5)` followed by `checkout()` *increases* stock and records an order with a **negative total** (`-2.18`) — no quantity or discount bounds-checking anywhere in `app.py`/`store.py`. This is a straight path to free inventory and negative-cost "orders" for anyone who can call the API with attacker-controlled quantities.

| # | Finding | Severity | Confidence |
|---|---|---|---|
| 1 | Negative qty/discount not validated → stock inflation + negative-total orders | **S1** | certain |
| 2 | Failed checkout leaves earlier-reserved stock un-released (inventory leak) | **S1** | certain |
| 3 | `store.py` read-modify-write on `db.json` has no locking → lost updates under concurrency | **S1/S2** | likely |
| 4 | Pagination is off-by-one, contradicts README's documented 1-based paging | **S2** | certain |
| 5 | Checkout on an empty cart crashes with an unhandled `ValueError` | **S2/S3** | certain |
| 6 | Order timestamps use local time, not UTC as documented | **S3** | certain |

Also noted, not counted as a bug: `tests/test_shop.py::test_refund_exists` fails because `Cart.refund` doesn't exist — but the README explicitly says "Refunds are not implemented yet (work in progress)," so this is a known gap shipping as a red test, not a hidden defect. Worth either skipping/marking `@unittest.expectedFailure` or removing until refunds land, just so the suite is green.

I also checked the README's claim that "discounts apply to the after-tax total" against `pricing.total()`, which applies the discount factor *before* multiplying by `(1 + TAX)`. Because both are just multiplicative factors, the order doesn't change the result (`a*(1-d)*(1+t) == a*(1+t)*(1-d)`) — so despite reading oddly against the doc, this is **not** a functional bug and isn't listed as a finding.

---

## Findings

### 1. Negative quantities/discounts aren't validated — stock inflation & negative-money orders
**Severity:** S1 (data loss / money) · **Confidence:** certain

**Location:** `app.py:8` (`Cart.add`), `app.py:11-22` (`Cart.checkout`), `store.py:22-28` (`reserve`)

**Trigger:**
```python
c = Cart()
c.add("apple", -5)
c.checkout()
```
**Expected:** rejected — quantities (and discounts) must be within valid bounds.
**Actual (reproduced):** `store.reserve` computes `inventory.get(sku,0) >= qty`, which is trivially true for negative `qty`, then does `inventory[sku] -= qty`, i.e. `-= -5` → **stock increases**. Confirmed apple stock went `6 → 11` in one call. `pricing.subtotal` then multiplies price by the negative qty, producing a **negative total** (`-2.18`), which `store.record_order` happily persists as a completed order. The same missing-bounds-check pattern applies to `discount` in `checkout(discount=...)` — e.g. `discount=1.5` also drives the total negative via `pre = subtotal * (1 - discount)`.

**Root cause:** no input validation anywhere between the cart API and the persistence layer — `Cart.add`, `Cart.checkout`, and `store.reserve` all trust their callers.

**Fix sketch:** validate `qty > 0` in `Cart.add` (or at `checkout` time before reserving) and `0 <= discount <= 1` in `checkout`; reject with a clear exception otherwise.
**Effort:** S

---

### 2. Failed checkout doesn't roll back stock already reserved for earlier items
**Severity:** S1 (silent inventory loss) · **Confidence:** certain

**Location:** `app.py:13-15`

**Trigger:**
```python
c = Cart()
c.add("apple", 1)
c.add("plum", 1)   # plum stock is 0
c.checkout()        # raises RuntimeError("out of stock: plum")
```
**Expected:** if checkout fails, no side effects — stock unchanged, no order recorded.
**Actual (reproduced):** the `for sku, qty in self.items.items()` loop calls `store.reserve` one SKU at a time and commits each reservation to `db.json` immediately. When a later SKU fails, the exception propagates but the earlier `store.reserve("apple", 1)` call already decremented and saved stock. Confirmed apple stock dropped `11 → 10` even though the checkout raised and no order was recorded — that unit of stock is now unaccounted for and unrecoverable (no compensating release anywhere in the codebase).

**Root cause:** reservation is applied per-item with immediate persistence instead of being all-or-nothing (no dry-run/precheck pass, no compensating rollback on failure).

**Fix sketch:** either (a) precheck all SKUs' availability before reserving any, or (b) track which reservations succeeded and release them (`inventory[sku] += qty`) if a later one fails.
**Effort:** M

---

### 3. `store.py` has no locking around its read-modify-write cycle on `db.json`
**Severity:** S1/S2 (oversold inventory / lost orders under concurrent load) · **Confidence:** likely (reasoned from code; not reproduced under real concurrency in this session — see verification plan)

**Location:** `store.py:22-28` (`reserve`), `store.py:31-36` (`record_order`)

**Trigger (plausible):** two checkout calls for the same SKU racing when only 1 unit is left — both `_load()` before either `_save()`s, both see stock `>= qty`, both decrement and save, and whichever `_save()` writes last silently clobbers the other's decrement (and/or drops the other's order). Any concurrent request handling (multiple threads, async workers, or just two browser tabs hitting a future HTTP layer) hits this.

**Expected:** stock and order log stay consistent under concurrent checkouts (no overselling, no lost orders).
**Actual:** every `reserve`/`record_order` call does `_load()` → mutate in memory → `_save()` (full-file overwrite, `store.py:13-15`) with **no file lock, no transaction, no optimistic-concurrency check**. This is a textbook TOCTOU race. It's compounded by `_save()` writing directly to `DB` rather than write-temp-then-rename, so a crash mid-write (or two processes writing simultaneously) can also leave `db.json` truncated/corrupt, which would then break `_load()` (`json.load` on a partial file) for *every* subsequent request.

**Root cause:** JSON-file-as-database with no concurrency control.

**Fix sketch:** use a file lock (e.g. `flock`/`filelock`) around load+mutate+save, or move to a store with real transactions (SQLite). At minimum, write via temp file + atomic rename to avoid partial-write corruption.
**Effort:** L

---

### 4. Pagination is off-by-one and contradicts the documented contract
**Severity:** S2 (wrong data returned to every paginated caller) · **Confidence:** certain

**Location:** `pagination.py:1-3`

**Trigger:**
```python
pagination.page_of(["a","b","c","d","e","f"], 1, size=2)
```
**Expected (per README):** "Pagination is 1-based: `page=1` returns the first `size` products" → `["a", "b"]`.
**Actual (reproduced):** `start = page * size` gives `start = 2`, returning `["c", "d"]` — page 1 actually returns what should be page 2. The *only* way to get the true first page is to pass the undocumented, contract-violating `page=0`. Every legitimate 1-based caller is silently shifted one page forward, and the true last page is unreachable (falls off the end early).

**Root cause:** off-by-one — formula treats `page` as 0-based while the documented/intended API is 1-based.

**Fix sketch:** `start = (page - 1) * size` (and reject/clamp `page < 1`).
**Effort:** S

---

### 5. Checking out an empty cart crashes with an unhandled `ValueError`
**Severity:** S2/S3 (ungraceful crash on a very reachable input) · **Confidence:** certain

**Location:** `app.py:12`

**Trigger:**
```python
Cart().checkout()
```
**Expected:** either a normal empty order, or a clear/handled error (the module already has a convention for this: `RuntimeError("out of stock: ...")`).
**Actual (reproduced):** `biggest = max(self.items.values())` runs before anything else in `checkout`, and `max()` on an empty sequence raises `ValueError: max() arg is an empty sequence` — an unhandled, unrelated-looking exception instead of a meaningful error, and it fires even before the stock-check loop that would otherwise be the natural validation point.

**Root cause:** `max()` over `self.items.values()` assumes at least one line item; nothing upstream guarantees that.

**Fix sketch:** guard at the top of `checkout`: if `not self.items: raise ValueError("cart is empty")` (or handle gracefully), same style as the existing out-of-stock check.
**Effort:** S

---

### 6. Order timestamps are recorded in local time, not UTC as documented
**Severity:** S3 (data-quality / reporting correctness) · **Confidence:** certain

**Location:** `store.py:33`

**Trigger:** run `record_order` on any host not set to UTC (e.g. `TZ=America/New_York`).
**Expected (per README):** "Order timestamps are recorded in **UTC**."
**Actual:** `order["at"] = datetime.datetime.now().isoformat()` uses naive local time with no timezone offset in the string, so downstream consumers that trust the README and parse `"at"` as UTC will be silently off by the host's UTC offset (and DST transitions could even make ordering ambiguous around clock changes).

**Root cause:** `datetime.now()` instead of `datetime.now(datetime.timezone.utc)` (or `.utcnow()`).

**Fix sketch:** `datetime.datetime.now(datetime.timezone.utc).isoformat()`.
**Effort:** S

---

## Verification plan

- **#1, #2, #4, #5** are empirically reproduced (see receipts below / rerun via a throwaway `unittest` case) — any fix should be checked by re-running the same trigger and asserting the *expected* behavior instead.
- **#3** needs an actual concurrency harness to reproduce directly (e.g. spawn two threads/processes both calling `store.reserve("plum", 1)` when stock is 1, assert exactly one succeeds) — flagged as "likely" rather than "certain" because I verified the non-atomic code path by inspection but did not force a real interleaving in this session.
- **#6** is a one-line code-vs-doc mismatch, verifiable by inspection or by comparing `record_order`'s output against `datetime.utcnow()` on a non-UTC host.
- Regression check for all fixes: `python3 -m unittest discover -s tests`.

## Top fixes first

1. **#1 negative qty/discount validation** — cheapest fix, closes an actual money/inventory exploit.
2. **#2 reservation rollback on failed checkout** — same file, same method, prevents silent stock loss.
3. **#4 pagination off-by-one** — one-line fix, restores documented contract.
4. **#5 empty-cart crash** — one-line guard.
5. **#6 UTC timestamps** — one-line fix.
6. **#3 concurrency/locking** — correct fix is the most invasive (real locking or a DB); worth scoping separately once the cheaper fixes are in.

---

## Receipts

### 2026-07-13 — Finding #4: pagination off-by-one

**Scope authorized:** pagination fix only ("Just fix the pagination bug. Nothing else.")

**Change:** `pagination.py:2` — `start = page * size` → `start = (page - 1) * size`. Commit `7c0263d`.

**Checks:**
- Targeted regression: `page_of(["a","b","c","d","e","f"], 1, size=2)` now returns `["a", "b"]` (was `["c", "d"]`) — **passed**.
- Full existing suite: `python3 -m unittest tests.test_shop` — **2 passed / 1 pre-existing failure** (`test_refund_exists`, unrelated — README documents refunds as not-yet-implemented; failure predates this change and is unaffected by it).
- No other findings from this report were touched.

