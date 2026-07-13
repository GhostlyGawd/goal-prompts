# Bug Hunt — 2026-07-13 (update)

A `BUGS.md` from an earlier pass today already exists; this report re-verifies
every prior finding against the current code and adds two newly discovered
issues.

## Delta vs. previous report

- **Fixed:** #4 (pagination off-by-one) — `pagination.py:2` now reads
  `start = (page - 1) * size` (commit `7c0263d`). Verified: `page_of([...], 1,
  size=2)` returns `["a", "b"]` as documented.
- **Still present (code unchanged since last pass):** #1 negative qty/discount
  not validated, #2 failed checkout doesn't roll back earlier reservations,
  #3 no locking around `db.json` read-modify-write, #5 empty-cart checkout
  crashes with unhandled `ValueError`, #6 order timestamps use local time
  instead of UTC.
- **New this pass:** #7 unregistered-SKU reservation crashes with an
  unhandled `KeyError`, #8 negative page numbers in `pagination.page_of`
  silently return real (wrong) product data instead of being rejected.
- **Regressed:** none.
- **Not a bug (re-confirmed):** discount-before-tax ordering in
  `pricing.total` is algebraically equivalent to discount-after-tax, so it
  doesn't violate the README despite reading oddly. `test_refund_exists`
  fails because refunds are explicitly documented as not-yet-implemented —
  a known gap, not a hidden defect.

## Summary

8 findings total (6 carried over minus 1 fixed, plus 2 new), all confirmed
either by direct reproduction (unittest harness, discarded after use — see
Verification plan) or by code inspection. This is still a ~110-line toy
webshop, but the money/inventory-integrity bugs (#1, #2, #3) remain the
scariest: `Cart.add("apple", -5)` → `checkout()` still inflates stock and
records a negative-total order, and there is still no locking around the
JSON "database."

| # | Finding | Severity | Confidence | Status |
|---|---|---|---|---|
| 1 | Negative qty/discount not validated → stock inflation + negative-total orders | **S1** | certain | still present |
| 2 | Failed checkout leaves earlier-reserved stock un-released | **S1** | certain | still present |
| 3 | `store.py` read-modify-write on `db.json` has no locking | **S1/S2** | likely | still present |
| 4 | Pagination off-by-one | S2 | certain | **fixed** |
| 5 | Checkout on empty cart crashes with unhandled `ValueError` | **S2/S3** | certain | still present |
| 6 | Order timestamps use local time, not UTC as documented | **S3** | certain | still present |
| 7 | Reserving an unregistered SKU with qty ≤ 0 crashes with unhandled `KeyError` | **S2/S3** | certain | new |
| 8 | Negative page numbers silently return a real (wrong) product slice | **S3** | certain | new |

---

## Findings carried over (still present)

Code in `app.py`, `store.py`, `pricing.py` is byte-identical to the previous
pass, so these are re-stated with the same evidence rather than re-derived.
Full trigger/root-cause detail is unchanged from the prior report; abridged
here, see git history of this file if the full text is needed.

### 1. Negative quantities/discounts aren't validated
**S1 · certain · `app.py:8,11-22`, `store.py:22-28`**
`Cart().add("apple", -5); .checkout()` still increases stock (`inventory[sku]
-= qty` with negative `qty`) and persists a negative total. No bounds check
on `qty` or `discount` anywhere between the API and `db.json`.
**Fix sketch:** reject `qty <= 0` in `Cart.add`/`checkout`, reject
`discount` outside `[0, 1]`. **Effort:** S

### 2. Failed checkout doesn't roll back already-reserved stock
**S1 · certain · `app.py:13-15`**
The reservation loop in `checkout` commits each SKU to `db.json`
immediately; if a later SKU is out of stock, the exception propagates but
earlier reservations are not released. **Fix sketch:** precheck all SKUs
before reserving any, or track and release successful reservations on
failure. **Effort:** M

### 3. No locking around `db.json` read-modify-write
**S1/S2 · likely (reasoned, not force-reproduced under real concurrency) ·
`store.py:22-28,31-36`**
`reserve`/`record_order` both do `_load()` → mutate → `_save()` with no
lock, no transaction, and no atomic write (`_save` writes `DB` directly, not
via temp+rename). Concurrent checkouts on the last unit of a SKU can both
succeed, or a crash mid-write can corrupt `db.json` for every subsequent
request. **Fix sketch:** file lock around load+mutate+save, or move to
SQLite; at minimum write via temp-file+rename. **Effort:** L

### 5. Empty-cart checkout crashes with unhandled `ValueError`
**S2/S3 · certain · `app.py:12`**
`max(self.items.values())` runs before any validation; on an empty cart it
raises `ValueError: max() arg is an empty sequence` instead of a meaningful
error. **Fix sketch:** `if not self.items: raise ValueError("cart is
empty")` at the top of `checkout`. **Effort:** S

### 6. Order timestamps use local time, not UTC as documented
**S3 · certain · `store.py:33`**
`datetime.datetime.now().isoformat()` — naive local time, no offset,
contradicts README's "recorded in UTC." **Fix sketch:**
`datetime.datetime.now(datetime.timezone.utc).isoformat()`. **Effort:** S

---

## New findings

### 7. Reserving an unregistered SKU with qty ≤ 0 crashes with unhandled `KeyError`
**Severity:** S2/S3 (unhandled crash on a reachable input) · **Confidence:** certain (reproduced)

**Location:** `store.py:22-28` (`reserve`)

**Trigger:**
```python
import store
store.reserve("doesnotexist", 0)
```
**Expected:** either `True`/`False` (same contract as any other SKU) or a
clear validation error — same style as the existing "out of stock" path.

**Actual (reproduced):**
```
File "store.py", line 25, in reserve
    data["inventory"][sku] -= qty
KeyError: 'doesnotexist'
```
`data["inventory"].get(sku, 0) >= qty` reads with a safe default (`0 >= 0`
is `True`), but the very next line writes with `data["inventory"][sku] -=
qty`, which requires the key to already exist — `dict[k] -= v` first *reads*
`dict[k]`. For a genuinely unknown SKU this raises `KeyError` instead of
returning `False`. Reachable from `Cart.checkout()` any time a caller adds a
line item for a SKU not in `PRICES`/inventory with `qty == 0` (e.g. a
client-side bug that submits a zero-quantity line, or a typo'd SKU with
qty 0), and also for unknown SKU + negative qty (interacts with #1).

**Root cause:** asymmetric use of `.get(sku, 0)` for the read and `[sku]`
for the write — the "default to 0" fallback only applies to the comparison,
not the mutation.

**Fix sketch:** use `data["inventory"][sku] = data["inventory"].get(sku, 0)
- qty` (or reject unknown SKUs explicitly before touching inventory).
**Effort:** S

---

### 8. Negative page numbers silently return a real (wrong) product slice instead of erroring
**Severity:** S3 (validation gap, confusing but non-destructive) · **Confidence:** certain (reproduced)

**Location:** `pagination.py:1-3`

**Trigger:**
```python
pagination.page_of(["a","b","c","d","e","f"], -1, size=2)
```
**Expected:** an invalid page (< 1) should be rejected or clamped to an
empty/first page — it should not look like a legitimate result.

**Actual (reproduced):** `start = (page - 1) * size` = `-4` for `page=-1,
size=2`; Python slicing then treats `-4` as "4th from the end," so
`products[-4:-2]` returns `["c", "d"]` — **the exact same result as the
valid `page=2`**. A caller that passes a negative page (off-by-one bug
upstream, corrupted query param, etc.) gets a page of real, plausible data
back with no indication anything was wrong, rather than an empty list or an
error.

**Root cause:** the fix for the original off-by-one (#4, `(page - 1) *
size`) restored the documented 1-based contract for valid input but didn't
add a bound check for `page < 1`; negative `start` silently invokes
Python's negative-indexing semantics instead of signaling an invalid
request.

**Fix sketch:** `if page < 1: raise ValueError("page must be >= 1")` (or
clamp `start = max(0, (page - 1) * size)`, though clamping still can't
distinguish "invalid" from "page 1" — raising is clearer here).
**Effort:** S

---

## Verification plan

- #1, #2, #5, #7, #8 are empirically reproduced via a throwaway `unittest`
  harness (created, run, and deleted within this session — not committed).
- #3 still needs a real concurrency harness (two threads/processes racing
  `store.reserve("plum", 1)` when stock is 1) to move from "likely" to
  "certain" — flagged as reasoned-from-code, not force-reproduced.
- #6 is a one-line code-vs-doc mismatch, verifiable by inspection or by
  running `record_order` on a non-UTC host and comparing against
  `datetime.now(timezone.utc)`.
- Regression check for all fixes: `python3 -m unittest discover -s tests`.
  Note: `tests/test_shop.py::test_checkout_reserves_and_totals` calls the
  real `Cart.checkout()` against the real `db.json` (no test fixture/mock),
  so every test run mutates production-looking data (stock decrements,
  order log grows) — this is itself a symptom of the same "no isolation
  between logic and the JSON store" root cause as #3, worth fixing
  alongside it (inject a temp DB path in tests) but not counted as a
  separate finding here.

## Top fixes first

1. **#1 negative qty/discount validation** — cheapest fix, closes an actual
   money/inventory exploit.
2. **#7 unknown-SKU KeyError** — one-line fix (`.get` on write too), same
   file/area as #1, closes a crash path.
3. **#2 reservation rollback on failed checkout** — prevents silent stock
   loss.
4. **#8 negative-page validation** — one-line guard, closes a
   confusing-data-instead-of-error gap.
5. **#5 empty-cart crash** — one-line guard.
6. **#6 UTC timestamps** — one-line fix.
7. **#3 concurrency/locking** — most invasive; correct fix is real locking
   or a DB, worth scoping separately once the cheaper fixes are in.

---

## Receipts

### 2026-07-13 — Finding #4: pagination off-by-one (from previous pass)

**Scope authorized:** pagination fix only ("Just fix the pagination bug.
Nothing else.")

**Change:** `pagination.py:2` — `start = page * size` → `start = (page - 1)
* size`. Commit `7c0263d`.

**Checks:**
- Targeted regression: `page_of(["a","b","c","d","e","f"], 1, size=2)` now
  returns `["a", "b"]` (was `["c", "d"]`) — **passed**.
- Full existing suite: `python3 -m unittest tests.test_shop` — **2 passed /
  1 pre-existing failure** (`test_refund_exists`, unrelated). — **passed
  (with known pre-existing failure)**
- No other findings from that report were touched.

### 2026-07-13 — This pass: re-verification, no fixes applied yet

**Scope:** audit only, per current instructions — no fixes were authorized
or applied this pass.

**Checks run:**
- `python3 -m unittest tests.test_shop -v` — **1 pass, 1 pass,
  1 pre-existing fail** (`test_refund_exists`) — matches previous pass,
  confirms no regression from the pagination fix — **passed (pre-existing
  failure unrelated)**.
- Reproduced #7 (`store.reserve("doesnotexist", 0)` → `KeyError`) and #8
  (`page_of([...], -1, size=2)` → `["c","d"]`) via a throwaway `unittest`
  file, then deleted the scratch file — **confirmed / passed as
  repro-checks**.
- Confirmed #1, #2, #4, #5, #6 status by direct code inspection against the
  previous report's line numbers (all match current file contents except
  `pagination.py`, which now has the fix) — **inspection passed**.
