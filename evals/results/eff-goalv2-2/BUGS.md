# Bug Hunt — 2026-07-13

No previous `BUGS.md` found — this is the first report.

## Summary

8 findings: **2 × S1 certain** (money/inventory can be manipulated by a client-supplied
quantity or discount with no bounds checking), **1 × S1 worth-verifying** (unguarded
read-modify-write on the JSON "database" — a classic lost-update race, latent until a
concurrent entry point exists), **3 × S2** (a documented pagination contract that's
inverted, an unhandled crash on empty-cart checkout, and the test suite silently
mutating the live database on every run), **2 × S3** (an edge-case KeyError and a
UTC-timestamp promise the code doesn't keep).

**Scariest finding:** `Cart.add()` / `store.reserve()` place no floor on `qty`. A
negative quantity passes the `stock >= qty` check trivially, *increases* inventory
instead of reserving it, and simultaneously drives the order total down (or negative)
via `pricing.total`. One bad or malicious input silently corrupts stock and revenue
in the same request.

## Findings

### 1. Negative/zero quantity corrupts stock and money — S1, certain
**Location:** `app.py:8-9` (`Cart.add`), `store.py:22-28` (`reserve`), `pricing.py:5-9` (`subtotal`)
**Trigger:** `c = Cart(); c.add("plum", -5); c.checkout()`
**Expected:** quantities must be positive; invalid quantities are rejected before touching stock or price.
**Actual:** `reserve()` checks `inventory.get(sku, 0) >= qty`, which is trivially true for any negative `qty`, then does `inventory[sku] -= qty` — subtracting a negative number *adds* stock. Meanwhile `pricing.subtotal` computes `PRICES[sku] * qty`, so the same negative `qty` also drags the order total down (or negative, i.e. the "store" owes the customer). Nothing in `Cart.add`, `reserve`, or `pricing` rejects `qty <= 0`.
**Root cause:** no input validation at the only boundary that accepts a caller-supplied quantity.
**Fix sketch:** reject non-positive `qty` in `Cart.add` (or `reserve`) with a `ValueError`; add a unit test asserting negative/zero quantities are rejected and stock is unchanged.
**Effort:** S

### 2. Discount is unbounded — can make the total negative — S1, certain
**Location:** `app.py:11,18` (`Cart.checkout`), `pricing.py:12-14` (`total`)
**Trigger:** `Cart().add("apple", 1)` then `checkout(discount=2.0)`
**Expected:** discount is a fraction in `[0, 1)`; out-of-range values are rejected.
**Actual:** `pricing.total` computes `pre = subtotal * (1 - discount)` with no clamp. `discount=2.0` yields a negative pre-tax (and post-tax) total; `discount<0` silently *increases* the charge instead of erroring. Neither `Cart.checkout` nor `pricing.total` validates the range.
**Root cause:** same class of gap as #1 — a caller-controlled numeric parameter feeds directly into a money calculation with no bounds check.
**Fix sketch:** validate `0 <= discount < 1` in `pricing.total` (or at the `checkout` boundary) and raise on violation.
**Effort:** S

### 3. Running the test suite mutates the live `db.json` — S2, certain (directly observed)
**Location:** `tests/test_shop.py:12-16` (`test_checkout_reserves_and_totals`), `store.py:3` (`DB` path)
**Trigger:** `python3 -m unittest discover -s tests`
**Expected:** tests run against an isolated/temporary store; the repo's `db.json` is untouched by `python3 -m unittest`.
**Actual:** verified live during this audit — `db.json`'s `apple` stock dropped from `8` to `7` and gained a new order record after a single test run, because `store.DB` always resolves to the real `db.json` next to `store.py` and the test never overrides it. Every CI/dev run permanently consumes one unit of `apple` stock and appends an order. After 8 runs, `apple` stock hits 0 and `test_checkout_reserves_and_totals` starts failing with `RuntimeError: out of stock: apple` — a test that fails only because earlier test runs, not code changes, exhausted shared state.
**Root cause:** `store.py` hardcodes its data file path with no injection point for tests to point elsewhere.
**Fix sketch:** let `store` take a configurable DB path (env var or module-level override), and have tests use `tempfile`/`tearDown` to point at a scratch file.
**Effort:** S

### 4. Pagination is off by one page vs. the documented contract — S2, certain
**Location:** `pagination.py:1-3`
**Trigger:** `page_of(products, page=1, size=2)` on any product list, per the README's own example.
**Expected (README):** "Pagination is 1-based: `page=1` returns the first `size` products."
**Actual:** `start = page * size`, so `page=1` returns `products[size:size*2]` — the *second* page. The true first page is only reachable via the undocumented, out-of-spec `page=0`. Every caller that follows the documented API skips the first `size` items entirely and eventually walks off the end one page early.
**Root cause:** missing `-1` — should be `start = (page - 1) * size`.
**Fix sketch:** change to `start = (page - 1) * size`; add a boundary test for `page=1` and `page=0`/negative rejection.
**Effort:** S

### 5. Checkout on an empty cart crashes with an unhandled `ValueError` — S2, certain
**Location:** `app.py:12` (`Cart.checkout`, `biggest = max(self.items.values())`)
**Trigger:** `Cart().checkout()` before any `add()` call.
**Expected:** a clear, handled error (or a no-op) for an empty cart.
**Actual:** `max()` on the empty `self.items.values()` raises `ValueError: max() arg is an empty sequence`, uncaught, before the stock-reservation loop even runs. Any UI/API path that lets a user reach checkout with zero items (double-click, back-button, race with a "remove item" action) surfaces a raw stack trace instead of a friendly message.
**Root cause:** boundary case (empty collection) not handled before `max()`.
**Fix sketch:** guard at the top of `checkout`: `if not self.items: raise ValueError("cart is empty")`, and let the caller present that as a normal error.
**Effort:** S

### 6. Read-modify-write on `db.json` is not atomic — lost updates under concurrency — S1, worth-verifying
**Location:** `store.py:6-15` (`_load`/`_save`), `store.py:22-36` (`reserve`, `record_order`)
**Trigger:** two `reserve()` (or `reserve()` + `record_order()`) calls interleaved — e.g. two concurrent checkout requests for the same SKU when stock is low.
**Expected:** stock reservation is atomic; concurrent requests can't both succeed against the same last unit, and no order is silently dropped.
**Actual:** `reserve()` does `data = _load()` → check → mutate → `_save(data)` with no lock, and `record_order()` does a separate `_load()`/`_save()` round trip. If two calls interleave between `_load()` and `_save()`, both can read the same stock value, both pass the `>=` check, and the second `_save()` overwrites the first's changes — either overselling stock (both charge a customer for the last unit) or silently losing one caller's order record. There is no whole-file lock or file-based transaction.
**Root cause:** the JSON file is used as if it were a transactional store, with no locking primitive around the read-modify-write cycle.
**Why "worth-verifying" not "certain":** today `app.py` exposes no concurrent entry point (no web server/threading in this repo) — the race requires two calls to `reserve`/`record_order` truly overlapping in-process or across processes, which needs a driver (e.g. a future Flask layer) to actually trigger. Given the README calls this "a tiny order service," a concurrent front end is the obvious next step, at which point this becomes a certain, high-severity bug.
**Fix sketch:** wrap `_load`→mutate→`_save` in a file lock (e.g. `fcntl.flock`) or move to a store with real transactions (`sqlite3`) before adding any concurrent entry point.
**Effort:** M

### 7. Unguarded `PRICES[sku]` lookup can raise `KeyError` past the stock check — S3, worth-verifying
**Location:** `pricing.py:8` (`subtotal`), contrast with `store.py:24` (`inventory.get(sku, 0)`)
**Trigger:** `Cart().add("unknown_sku", 0); Cart().checkout()` (or any inventory SKU added to `db.json` without a matching `PRICES` entry).
**Expected:** an unknown/misconfigured SKU produces a clear, handled error at any quantity.
**Actual:** `reserve()` is lenient — `inventory.get(sku, 0) >= qty` is `True` for `qty <= 0` even on a nonexistent SKU, so reservation "succeeds" as a no-op. Execution then reaches `pricing.subtotal`, which does `PRICES[sku]` with no `.get()`/default, raising an unhandled `KeyError`. (For `qty > 0` the mismatch instead surfaces as a misleading `RuntimeError: out of stock: <sku>` for an item that was never stocked at all, from `app.py:15`.)
**Root cause:** `store` and `pricing` disagree on how to treat an unknown SKU (lenient default vs. hard lookup), and neither path produces a caller-friendly error.
**Fix sketch:** validate `sku in PRICES` once, at `Cart.add` or the top of `checkout`, and raise a single clear `ValueError("unknown sku: ...")` instead of relying on the two subsystems to fail consistently.
**Effort:** S

### 8. Order timestamps are recorded in local time, not UTC as documented — S3, certain
**Location:** `store.py:33` (`order["at"] = datetime.datetime.now().isoformat()`), vs. README: "Order timestamps are recorded in **UTC**."
**Trigger:** run on any host whose system timezone isn't UTC; record an order.
**Expected:** timestamp is UTC, per the documented contract (`db.json` already shows naive timestamps with no offset, implying callers will treat them as UTC).
**Actual:** `datetime.datetime.now()` returns naive local time, not UTC — on a non-UTC host the recorded `at` field is simply wrong, with no timezone offset to even detect the discrepancy. Any future reconciliation, audit, or time-boxed logic (e.g. a refund window, per the README's "work in progress" note) built on this field would be silently off by the host's UTC offset.
**Root cause:** `datetime.now()` used where `datetime.now(datetime.timezone.utc)` (or `datetime.utcnow()`) was intended.
**Fix sketch:** `datetime.datetime.now(datetime.timezone.utc).isoformat()`.
**Effort:** S

## Verification plan
- #1, #2: add unit tests in `tests/test_shop.py` asserting `Cart.add`/`checkout` raise on negative/zero qty and out-of-range discount; confirm stock/total unchanged after the raise.
- #3: point `store.DB` at a temp file in test `setUp`/`tearDown`; re-run suite N>8 times and confirm `db.json` (the real one) is byte-identical before/after.
- #4: add `test_pagination.py` asserting `page_of(products, 1, size=2) == products[:2]`.
- #5: add a test asserting `Cart().checkout()` raises a clear, documented exception (not `ValueError` from `max`).
- #6: requires a concurrency harness (two threads/processes hammering `reserve` on a SKU with stock=1) — flag as a follow-up once/if a concurrent entry point is added; not practically testable via the current single-threaded `Cart` API alone.
- #7: add a test adding an inventory-only or wholly-unknown SKU at qty 0 and asserting a clean `ValueError`, not `KeyError`.
- #8: add a test freezing/mocking `datetime.now` vs `now(utc)` and asserting the recorded `at` uses the UTC-aware path.

## Top fixes first
1. #1 negative/zero quantity validation (S1, effort S) — closes an active money/inventory exploit.
2. #2 discount bounds validation (S1, effort S) — closes the negative-total exploit.
3. #4 pagination off-by-one (S2, effort S) — trivial fix, directly contradicts documented API, affects every listing consumer.
4. #5 empty-cart guard (S2, effort S) — trivial, removes an unhandled crash.
5. #3 test isolation from `db.json` (S2, effort S) — stops CI from eating its own fixture data.
6. #7 unify unknown-SKU handling (S3, effort S).
7. #8 UTC timestamp fix (S3, effort S).
8. #6 file-locking / transactional store (S1-if-triggered, effort M) — do this before any concurrent entry point ships, not urgent today.
