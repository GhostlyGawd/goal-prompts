# Bug Hunt — 2026-07-13

No prior `BUGS.md` in this repo — this is the first pass, so there is no delta to report.

## Summary

- **Scope audited**: `calc.py` (15 lines, one function `subtotal_cents`) and its test suite (`tests/test_calc.py`, 4 tests, all passing).
- **Findings**: 0 confirmed defects. 1 low-severity validation nitpick, `worth-verifying`, that does not currently manifest anywhere in the repo (no caller code exists to trigger it).
- **Scariest finding**: none. The module is exactly what the README claims — "a tiny, deliberately boring calculator" with integer-cent math, no floats, no shared mutable state that's written to, and explicit validation on every input path (empty order, unknown SKU, non-positive/non-int quantity).

This is a genuine null result for the "defect" bar. Below is the lens-by-lens evidence so the audit is checkable, plus the one item that didn't rise to a finding but is worth knowing about.

## Findings

### (Not filed as a defect) `bool` quantities silently accepted as 1 or 0
- **Severity/Confidence**: S3 (annoyance) / worth-verifying — no evidence anywhere in this repo that a caller ever passes a `bool` as `qty`, so there's no demonstrated trigger, only a latent gap.
- **Location**: `calc.py:11` — `if not isinstance(qty, int) or qty <= 0:`
- **Trigger**: `subtotal_cents({"apple": True})`. Because `bool` is a subclass of `int` in Python, `isinstance(True, int)` is `True` and `True > 0`, so this silently succeeds and is billed as `qty=1` (40 cents). `{"apple": False}` correctly falls through to the `qty <= 0` rejection since `False == 0`.
- **Expected vs actual**: README claims "validated inputs"; a `bool` is not an integer quantity a shopper would ever legitimately submit, so the validation is slightly looser than the stated intent.
- **Root cause**: `isinstance(qty, int)` doesn't exclude `bool`, a well-known Python gotcha.
- **Fix sketch**: `if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:`
- **Effort**: S (one-line change, one new test case).
- **Why not filed as a real bug**: nothing in this repo constructs order dicts from untrusted/serialized input (no web handler, no CLI, no JSON parsing) that could hand a `bool` to this function, so there's no current path from "attacker/user input" to this branch. Flagging it so it's on record if a caller is added later.

## Lens-by-lens audit trail

1. **Unhandled failures** — every invalid path (`empty`, `unknown sku`, `bad qty`) raises a specific, typed exception; the happy path returns a plain `int`. No bare `except`, no swallowed errors, nothing to unhandle.
2. **Null/empty paths** — `{}` and `None` are both falsy and correctly hit the `if not items` guard (`calc.py:5`) before any iteration.
3. **Race conditions** — `PRICES_CENTS` is read-only inside the function; nothing in the repo writes to it after import, and there's no concurrency (threads/async) anywhere in this codebase. No race is possible with the code as it exists today.
4. **Boundary values** — `qty <= 0` rejects `0` and negatives; Python ints are arbitrary-precision so there's no overflow at large `qty`. Confirmed `qty=-1` and `qty=0` both raise via existing tests plus manual check.
5. **Time & math** — money is tracked in integer cents throughout (`PRICES_CENTS`, `total`), so there's no floating-point rounding error, the classic money-math bug class. No date/time logic exists to have off-by-one or timezone bugs.
6. **State drift** — `PRICES_CENTS` is a module-level dict but nothing in the repo mutates it; `subtotal_cents` never writes to it. No drift is observable in the current code.
7. **Validation gaps** — every field is checked (SKU membership, qty type, qty sign) except the `bool`-as-`int` gap noted above.
8. **Resource leaks** — no file handles, sockets, or other resources are opened.

Also compared against `README.md`'s claims ("Integer-cent money math, validated inputs, no shared state") — all three claims hold in the current code; the `bool` gap above is the only (minor) place validation is looser than the wording implies.

## Verification plan

- `python3 -m unittest discover -s tests` — all 4 existing tests pass (confirmed this run).
- If the `bool` item is ever addressed: add `subtotal_cents({"apple": True})` → expect `ValueError`, and `subtotal_cents({"apple": False})` → expect `ValueError` (already passes today) as regression tests.

## Top fixes first

None required. If the team wants belt-and-suspenders validation, the `bool` exclusion (effort S) is the only outstanding item, and it's optional given no current caller can reach it.
