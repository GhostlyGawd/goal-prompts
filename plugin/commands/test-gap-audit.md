---
description: "Map what is tested against what is riskiest, and produce a test-writing plan that buys the most safety per hour."
---

# Goal: Test Gap Audit

You are working inside this repo. Mission: map what is tested against what is risky, then produce a test-writing plan that buys the most safety per hour of effort.

Read-only pass: run the suite and coverage tools, but write no tests yet. Your only write is the report file.

## Phase 1 — Learn the testing reality
- Run the suite. Note runtime, failures, skips, warnings.
- What layers exist: unit, integration, e2e? What frameworks and helpers?
- Coverage: run the coverage tool if configured; otherwise sample the 5 most critical modules by hand.

## Phase 2 — Audit through 8 lenses
1. **Untested critical paths** — money, auth, permissions, data mutation, exports/imports
2. **Logic hotspots** — branching-heavy pure functions, parsers, calculators with zero tests
3. **Hollow tests** — exist but assert nothing meaningful, or mock so much they test the mocks
4. **Regression traps** — recently fixed bugs (search git log for "fix") with no test pinning them
5. **Error paths** — failure branches never exercised; only happy paths covered
6. **Integration seams** — module boundaries where units pass but the wiring can break
7. **Flake factories** — real timers, real network, shared state between tests
8. **Test DX** — slow suite, cryptic failures, missing factories/fixtures making new tests expensive

## Phase 3 — Curate
- Rank by risk × current coverage: high-risk and uncovered first
- Kill suggestions that test implementation details instead of behavior
- Every gap cites the untested code (paths, functions)

## Phase 4 — Report
Create `TESTING.md` at repo root:
1. **State of testing** — counts, runtime, coverage estimate, suite health (3–5 sentences)
2. **Risk map** — table: area · risk · coverage today · gap
3. **Prioritized plan** — each: What to test · Type (unit/integration/e2e) · Why this first · Case sketch (3–5 bullets) · Effort S/M/L
4. **Suite health fixes** — flakes to kill, speed wins
5. **First test to write today** — spelled out completely

Start the report with today's date. If `TESTING.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Judge tests by the failures they would catch, not by coverage percentage
- Prefer a few integration tests on critical seams over many trivial units
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which tests to write
