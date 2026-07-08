---
id: "100"
title: Test-Quality Audit
family: Quality
question: does it work?
output: TESTQUALITY.md
tagline: Whether the tests actually protect the code — asserting meaningful behavior, or merely executing lines and passing no matter what.
---
# Goal: Test-Quality Audit

You are working inside this repo. Mission: judge whether the test suite would actually catch a regression — whether tests assert real behavior or just run code and pass. High coverage that asserts nothing is a false sense of safety.

Read-only pass. Read the tests and what they cover; change nothing but the report file.

## Phase 1 — Read the tests, not the coverage number
- Sample tests across the critical paths and read what they assert.
- Note where coverage is high but assertions are thin or absent.
- Identify the risky, high-value logic and check how seriously it is tested.

## Phase 2 — Audit through 7 lenses
1. **Assertion strength** — tests that exercise code but assert little; snapshot-only "coverage"
2. **Behavior vs implementation** — tests bound to internals that break on refactor and miss real regressions
3. **Coverage honesty** — high line coverage hiding untested branches, error paths, and edges
4. **Meaningful failure** — would each test actually fail if the behavior broke
5. **Data realism** — fixtures that dodge the hard cases: empty, huge, malformed, boundary
6. **Isolation** — tests that pass only in order, share state, or depend on the clock or network
7. **Critical-path priority** — is the risky, valuable logic tested, or only the easy getters

## Phase 3 — Curate
- Rank by risk left uncovered: weak tests on money or auth outrank a thin test on a label.
- For each weak test, say what it should assert instead.
- Name the untested-in-practice paths — covered by a line but not by a real check.

## Phase 4 — Report
Create `TESTQUALITY.md` at repo root:
1. **Weakest tests** — ranked by the risk they pretend to cover, each with what it should assert
2. **Untested in practice** — paths with coverage but no meaningful assertion
3. **Critical gaps** — high-value logic that needs real tests, prioritized
4. **What good looks like** — an example rewrite turning a hollow test into a real one

## Rules
- Coverage measures lines run, not behavior verified; judge the assertions
- A test that cannot fail is documentation, not protection
- Report only — end by asking which tests to strengthen first
