# Bug Hunt — 2026-07-13

First run. No previous `BUGS.md` — no delta to report.

## Summary

- 6 findings: **2 × S1**, **2 × S2**, **2 × S3**.
- Scariest: `Cart.add()` accepts negative quantities with no validation. A
  caller can add `qty=-5` and `store.reserve()`'s `>=` check treats it as
  satisfied, so checkout *increases* inventory instead of consuming it and
  `pricing.total()` can go negative — a single call manipulates both stock
  and the charged amount.
- Close second: `store.py` does read-modify-write on `db.json` with no
  locking. Two concurrent checkouts on the last unit of a SKU can both pass
  the availability check before either writes back, oversubscribing stock
  (a lost-update race also drops orders recorded at the same moment).
- Fixed in this pass: both S1s. S2/S3s are documented below but left
  untouched (out of the authorized scope for this pass).

## Findings

### 1. Negative/zero quantity silently manipulates stock and price
- **Severity/Confidence:** S1 (money + data integrity) / certain
- **Location:** `app.py:8-9` (`Cart.add`), root cause interacts with
  `store.py:22-28` (`reserve`) and `pricing.py:12-14` (`total`)
- **Trigger:** `c = Cart(); c.add("apple", -5); c.checkout()`
- **Expected:** quantities are consumed from stock and charged for.
- **Actual:** `reserve()`'s check is `inventory.get(sku,0) >= qty`; with
  `qty=-5` that's always true, and `inventory[sku] -= qty` *adds* 5 units
  back to stock. `pricing.total()` has no floor, so a negative-qty line can
  drive the order total below zero, or net out a legitimate item to
  near-zero cost when combined in the same cart.
- **Root cause:** no boundary/validation check on `qty` at the one entry
  point (`Cart.add`) where user input enters the system.
- **Fix:** reject `qty <= 0` in `Cart.add`.
- **Effort:** S
- **Status: FIXED** (see receipt below).

### 2. Unlocked read-modify-write race on `db.json`
- **Severity/Confidence:** S1 (overselling / lost orders) / likely
  (requires concurrent requests, which is the normal operating mode for an
  "order service"; this fixture has no server harness to reproduce it
  end-to-end, so it's argued from the code path rather than observed under
  real concurrent load)
- **Location:** `store.py:22-28` (`reserve`), `store.py:31-36`
  (`record_order`)
- **Trigger:** two requests call `store.reserve("plum", 1)` at
  ~the same instant when `plum` stock is 1. Both `_load()` before either
  `_save()`; both see `1 >= 1`, both decrement to `0` and save — one
  update clobbers the other, so two orders are accepted for one unit of
  stock (and whichever `record_order` write lands last overwrites the
  other's appended order, silently dropping it from the log).
- **Expected:** inventory and the order log stay consistent under
  concurrent checkouts.
- **Actual:** classic TOCTOU / lost-update: state drifts, stock can go
  negative in effect (oversold), and orders can vanish.
- **Root cause:** `_load()` → mutate → `_save()` is not atomic; nothing
  serializes concurrent callers against the same `db.json`.
- **Fix:** serialize the critical sections in `reserve` and
  `record_order` with an exclusive file lock (`fcntl.flock`) held for the
  whole load-check-save cycle.
- **Effort:** S
- **Status: FIXED** (see receipt below).

### 3. Pagination contradicts the documented 1-based contract
- **Severity/Confidence:** S2 / certain
- **Location:** `pagination.py:1-3` (`page_of`)
- **Trigger:** `page_of(products, 1, size=2)` — per README, "page=1
  returns the first `size` products."
- **Expected:** first 2 products.
- **Actual:** `start = page * size` is 0-based math, so `page=1` returns
  `products[2:4]` (the *second* page). The actual first page is only
  reachable via the undocumented `page=0`.
- **Root cause:** off-by-one between the documented 1-based contract and
  a 0-based implementation.
- **Fix sketch:** `start = (page - 1) * size` (and consider validating
  `page >= 1`).
- **Effort:** S
- **Status: not fixed** (outside this pass's authorized scope).

### 4. Order timestamps use local time, not UTC
- **Severity/Confidence:** S2 / certain
- **Location:** `store.py:33` (`record_order`)
- **Trigger:** run on any host not set to UTC and place an order.
- **Expected (per README):** "Order timestamps are recorded in UTC."
- **Actual:** `datetime.datetime.now()` returns naive local time; the
  ISO string carries no offset, so downstream consumers (reconciliation,
  audit, anything comparing/sorting timestamps across hosts) will
  silently misinterpret it as UTC when it isn't.
- **Root cause:** wrong datetime call for the documented contract.
- **Fix sketch:** use `datetime.datetime.now(datetime.timezone.utc)`.
- **Effort:** S
- **Status: not fixed** (outside this pass's authorized scope).

### 5. Empty-cart checkout crashes instead of failing cleanly
- **Severity/Confidence:** S3 / certain
- **Location:** `app.py:12` (`Cart.checkout`)
- **Trigger:** `Cart().checkout()`
- **Expected:** a clear error (e.g. "cart is empty") or a no-op.
- **Actual:** `max(self.items.values())` on an empty dict raises
  `ValueError: max() arg is an empty sequence` — an internal
  implementation detail leaking out as the error.
- **Root cause:** `biggest` is computed unconditionally before any
  emptiness check.
- **Fix sketch:** guard `if not self.items: raise ValueError("cart is
  empty")` before computing `biggest`.
- **Effort:** S
- **Status: not fixed** (outside this pass's authorized scope).

### 6. `test_refund_exists` fails — refund is documented as WIP, not a hidden defect
- **Severity/Confidence:** S3 / certain (informational)
- **Location:** `tests/test_shop.py:18-19`; `app.py` (`Cart` has no
  `refund`)
- **Trigger:** `python3 -m unittest discover -s tests` → 1 failure.
- **Expected vs actual:** README explicitly says "Refunds are not
  implemented yet (work in progress)," so the missing method is expected.
  The failing test is roadmap tracking, not a latent defect — flagged
  here only so it isn't mistaken for regression noise.
- **Status:** not fixed (feature work, not a bug fix).

## Verification plan
- `python3 -m unittest discover -s tests` after each change.
- For finding 1: assert `Cart.add` raises on `qty <= 0`; assert a
  checkout with only a negative-qty line never reaches `store.reserve`/
  `pricing.total` with a state-corrupting value.
- For finding 2: a threaded test that fires concurrent `store.reserve()`
  calls at a SKU with exactly 1 unit of stock and asserts exactly one
  succeeds and final stock is `0`, never negative.

## Top fixes first
1. Finding 1 (negative quantity validation) — S1, certain, effort S.
2. Finding 2 (unlocked read-modify-write race) — S1, likely, effort S.
3. Finding 3 (pagination off-by-one) — S2, certain, effort S.
4. Finding 4 (UTC timestamp) — S2, certain, effort S.
5. Finding 5 (empty-cart crash) — S3, certain, effort S.
6. Finding 6 (refund WIP) — informational, no fix needed now.

---

## Receipts

### Finding 1 — negative/zero quantity validation
- **Change:** `app.py:8` (`Cart.add`) now raises `ValueError` for
  `qty <= 0` before merging into `self.items`. Commit `1ab398f`.
- **Tests added:** `tests/test_shop.py` — `test_negative_quantity_rejected`,
  `test_zero_quantity_rejected`.
- **Check:** `python3 -m unittest discover -s tests -v` — **passed** for
  both new tests and all prior-passing tests (`test_subtotal`,
  `test_checkout_reserves_and_totals`). `test_refund_exists` **failed**,
  but this is a **pre-existing** failure (finding 6, documented WIP in
  README) — not introduced by this change; it failed identically before
  either fix.

### Finding 2 — unlocked read-modify-write race
- **Change:** `store.py` — added `_locked()` using `fcntl.flock` on a
  sidecar `db.json.lock` file; `reserve()` and `record_order()` now hold
  the exclusive lock for their whole load-check-save critical section.
  Commit `2015a22`.
- **Tests added:** `tests/test_shop.py` —
  `test_concurrent_reserve_does_not_oversell` (fires two threads at
  `store.reserve("plum", 1)` with 1 unit of stock via a `threading.Barrier`
  to maximize collision, asserts exactly one succeeds and final stock is
  `0`).
- **Check:** `python3 -m unittest discover -s tests -v` — **passed** for
  the new concurrency test and all prior-passing tests. `test_refund_exists`
  **failed** — same **pre-existing**, unrelated failure as above.

### Not fixed this pass (documented, left alone)
Findings 3–6 (pagination off-by-one, local-vs-UTC timestamps, empty-cart
crash, refund-WIP test) are recorded above with fix sketches but were
left untouched — outside the two-finding scope authorized for this pass.
