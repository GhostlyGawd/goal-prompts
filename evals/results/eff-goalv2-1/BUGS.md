# Bug Hunt — 2026-07-13

No previous `BUGS.md` existed, so this is the initial report (no delta).

## Summary

6 findings. **3 rated S1** (inventory/money integrity), **2 rated S2**, **1 rated S3**.

Scariest finding: **negative-quantity checkout** (`app.py`/`store.py`) lets a caller
inflate inventory and produce a negative-total order with zero validation — a direct
money/data-integrity hole, not an edge case someone has to squint to find.
Close behind: a failed multi-item checkout **permanently loses inventory** for the
items that *did* reserve before the failure, because there's no rollback.

Housekeeping note: running the test suite (`python3 -m unittest discover -s tests`)
mutates the committed `tests`-adjacent fixture `db.json` in place (see Finding 7) —
doing so during this audit left `db.json` with `apple: 7` and an extra order instead
of the committed `apple: 8`. I was not able to revert it (git checkout was declined),
so `db.json` in the working tree currently differs from `HEAD` by that one test run.

## Findings

### 1. Negative/zero quantities are never validated — inventory inflation & negative-total orders
- **Severity/Confidence:** S1 · certain
- **Location:** `store.py:22-28` (`reserve`), `app.py:8-22` (`Cart.add`/`checkout`), `pricing.py:5-9` (`subtotal`)
- **Trigger:** `cart.add("apple", -1000); cart.checkout()`. `reserve()` checks
  `data["inventory"].get(sku, 0) >= qty`; with `qty = -1000` any stock level satisfies
  `stock >= -1000`, then `data["inventory"][sku] -= qty` **adds** 1000 units back.
  `pricing.subtotal` then computes `PRICES[sku] * -1000`, a negative line total that
  flows straight into `total()` and gets persisted via `record_order`.
- **Expected vs actual:** Expected — quantities are positive integers; a bad quantity
  is rejected. Actual — any integer (including negative or zero) is accepted,
  silently inflating inventory and/or producing negative-total orders.
- **Root cause:** No input validation anywhere on the `qty` path between `Cart.add`
  and `store.reserve`/`pricing.subtotal`.
- **Fix sketch:** Validate `qty > 0` (and probably `isinstance(qty, int)`) in
  `Cart.add`, raising a `ValueError` immediately; optionally also guard in
  `store.reserve` as defense-in-depth since it's the layer that actually mutates
  shared state.
- **Effort:** S

### 2. Failed multi-item checkout leaves earlier reservations permanently decremented (no rollback)
- **Severity/Confidence:** S1 · certain
- **Location:** `app.py:12-15` (`Cart.checkout`)
- **Trigger:** Cart with two SKUs, e.g. `apple` (in stock) and `plum` (stock is `0`
  in the shipped `db.json`). `checkout()` iterates `self.items.items()`; the first
  `store.reserve("apple", n)` call succeeds and is saved to disk *immediately*
  (`store.reserve` does its own load/save per call). The second call for `plum`
  fails, and `checkout()` raises `RuntimeError` before `record_order` ever runs.
  The `apple` stock decrement is never undone.
- **Expected vs actual:** Expected — a failed checkout is atomic: either the whole
  order reserves and is recorded, or nothing changes. Actual — partial stock
  decrements survive a failed checkout with no corresponding order, so inventory
  silently shrinks ("phantom shrinkage") every time a multi-item cart hits an
  out-of-stock item after an in-stock one.
- **Root cause:** Each `store.reserve()` call is its own independent
  load/mutate/save transaction; `Cart.checkout` has no compensating action
  (no rollback / no pre-flight stock check across all items before committing any).
- **Fix sketch:** Either (a) check availability for *all* items before reserving
  any of them (two-pass: validate then commit), or (b) track which reservations
  succeeded and release them back to inventory if a later one fails.
- **Effort:** S–M

### 3. `reserve`/`_load`/`_save` have no locking — concurrent checkouts can oversell
- **Severity/Confidence:** S1 (defect) · likely to manifest under concurrent access
- **Location:** `store.py:6-28` (`_load`, `_save`, `reserve`)
- **Trigger:** Two concurrent calls to `store.reserve("plum", 3)` when `plum` has
  4 in stock. Both read (`_load`) the same `inventory["plum"] = 4` before either
  writes back. Both see `4 >= 3` and both proceed to `_save` with
  `inventory["plum"] = 1`, having actually sold 6 units of a 4-unit stock — a
  classic time-of-check-to-time-of-use race, since there is no file lock, no
  atomic write, and no in-memory mutex around the read-modify-write.
- **Expected vs actual:** Expected — stock can never go negative / be oversold.
  Actual — under concurrent requests it can, because the "check stock, then
  write stock" sequence isn't atomic.
- **Root cause:** `_load`/`_save` are plain unsynchronized file I/O; nothing
  serializes access to `db.json` across concurrent callers.
- **Fix sketch:** Add a file lock (e.g. `fcntl.flock` / `filelock`) around the
  load-check-decrement-save sequence in `reserve`, or move to a datastore with
  real transactions.
- **Effort:** M

### 4. Pagination is off by one page — `page=1` skips the first page
- **Severity/Confidence:** S2 · certain
- **Location:** `pagination.py:1-3` (`page_of`)
- **Trigger:** `page_of(products, page=1, size=2)`. README states "Pagination is
  1-based: `page=1` returns the first `size` products." Code computes
  `start = page * size`, so `page=1` gives `start=2`, returning
  `products[2:4]` — the *second* page, not the first. Verified directly:
  `page_of(['p0','p1','p2','p3','p4','p5'], 1, size=2) == ['p2','p3']`, not
  `['p0','p1']`. The only way to get the true first page is `page=0`, which
  contradicts "1-based."
- **Expected vs actual:** Expected — `page=1` → `products[0:size]`. Actual —
  `page=1` → `products[size:2*size]`; every caller following the documented
  contract silently sees the wrong page (and the true first page of products
  is unreachable through the documented API).
- **Root cause:** Missing `page - 1` conversion from 1-based page number to
  0-based slice offset.
- **Fix sketch:** `start = (page - 1) * size` (and arguably validate `page >= 1`).
- **Effort:** S

### 5. Empty-cart checkout crashes with a raw `ValueError` instead of a clear error
- **Severity/Confidence:** S2 · certain
- **Location:** `app.py:12` (`Cart.checkout`, `biggest = max(self.items.values())`)
- **Trigger:** `Cart().checkout()` with no items ever added (or all removed —
  though there's no remove method today). `self.items.values()` is empty, and
  Python's `max()` on an empty sequence raises
  `ValueError: max() iterable argument is empty sequence` — an unrelated,
  confusing error instead of a meaningful "cart is empty" message. This is a
  very plausible trigger: any UI/API that allows a checkout call before an add,
  or after a double-submit, hits it.
- **Expected vs actual:** Expected — checking out an empty cart gives a clear,
  handleable error (or a defined no-op). Actual — an opaque `ValueError` from deep
  inside `max()`, with no indication of the actual problem.
- **Root cause:** No guard for the empty-cart case before computing `biggest`.
- **Fix sketch:** Guard at the top of `checkout()`: `if not self.items: raise
  ValueError("cart is empty")` (or similar explicit, documented exception).
- **Effort:** S

### 6. Order timestamps use local server time, not UTC as documented
- **Severity/Confidence:** S3 · worth-verifying (depends on deployment timezone)
- **Location:** `store.py:33` (`record_order`, `datetime.datetime.now().isoformat()`)
- **Trigger:** README states "Order timestamps are recorded in **UTC**."
  `datetime.datetime.now()` returns local system time with no timezone info
  attached, so on any host whose local timezone isn't UTC, the recorded
  `"at"` field is silently wrong — and because `isoformat()` on a naive datetime
  carries no offset, downstream consumers have no way to tell it's not UTC. In
  this sandbox the system clock happens to be set to UTC, so the bug is masked
  here but not fixed.
- **Expected vs actual:** Expected — `"at"` is always UTC (ideally with an
  explicit `Z`/offset). Actual — `"at"` is naive local time, correct only by
  coincidence of host timezone configuration.
- **Root cause:** `datetime.datetime.now()` instead of a UTC-aware call.
- **Fix sketch:** `datetime.datetime.now(datetime.timezone.utc).isoformat()`.
- **Effort:** S

## Also noted (not ranked as a shipped-code bug)

- **`tests/test_shop.py::test_refund_exists`** currently fails
  (`hasattr(Cart, "refund")` is `False`) — but the README explicitly discloses
  "Refunds are not implemented yet (work in progress)," so this reads as an
  intentional, tracked gap rather than a latent defect. Flagging only because a
  failing test in the suite could mask a *real* regression later if nobody
  distinguishes "expected WIP failure" from "new failure."
- **Test suite mutates the shared fixture `db.json` in place** (`store.reserve`/
  `record_order` write to the real `db.json` on disk, and tests don't reset it).
  Repeated test runs permanently consume `apple` stock and pile up `orders`;
  since `plum` is already at 0 stock in the fixture, this is already partway
  toward making `test_checkout_reserves_and_totals` fail purely from prior test
  runs, independent of any code bug. Worth adding test isolation (e.g. a temp
  `DB` path) if this suite is meant to be run repeatedly/in CI.

## Verification plan

- Findings 1, 4, 5: reproduced directly by static trace of the arithmetic/control
  flow (pagination off-by-one and empty-cart `max()` confirmed by direct
  execution; negative-qty math confirmed by hand-tracing `reserve`/`subtotal`,
  not executed against the shared `db.json` fixture to avoid further mutating it).
  A unit test per finding (bad qty, page=1 contents, empty-cart checkout) would
  pin these down and prevent regression.
- Finding 2: reproducible with a two-SKU cart where the second SKU is
  out-of-stock (e.g. `apple` + `plum` against the shipped `db.json`, since
  `plum` stock is `0`); assert `apple` stock is unchanged after the expected
  `RuntimeError`.
- Finding 3: requires a concurrency test — two threads/processes calling
  `store.reserve` on the same SKU simultaneously with a race-prone stock level;
  assert final stock never goes negative and total reserved never exceeds
  starting stock.
- Finding 6: requires either mocking `datetime.datetime.now` under a non-UTC
  `TZ`, or asserting the stored timestamp carries explicit UTC offset info.

## Top fixes first

1. Finding 1 (negative qty validation) — cheapest fix, closes an outright
   money/inventory exploit.
2. Finding 2 (checkout rollback) — closes the inventory-shrinkage leak.
3. Finding 4 (pagination off-by-one) — trivial fix, but affects every paginated
   listing today.
4. Finding 5 (empty-cart guard) — trivial, improves error clarity.
5. Finding 3 (locking) — real fix is more involved (needs a locking strategy
   or a datastore change); worth scoping separately.
6. Finding 6 (UTC timestamps) — trivial fix, lowest user-facing pain.
