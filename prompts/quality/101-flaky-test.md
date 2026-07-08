---
id: "101"
title: Flaky-Test Audit
family: Quality
question: does it work?
output: FLAKY.md
tagline: The tests that fail intermittently — the ones eroding trust in the suite until a red build stops meaning anything.
---
# Goal: Flaky-Test Audit

You are working inside this repo. Mission: find the tests that pass and fail without the code changing — and the nondeterminism behind each — because a suite people re-run until it's green is a suite they no longer trust.

Read-only pass. Read the tests, their setup, and any run history; change nothing but the report file.

## Phase 1 — Hunt the nondeterminism
- Look for the usual sources: time, order, network, randomness, shared resources.
- Check run history or retry config for tests already known to be re-run.
- Note tests that pass alone but might fail in a parallel or shuffled suite.

## Phase 2 — Audit through 7 lenses
Name the nondeterminism source for every finding.
1. **Timing & waits** — sleeps, fixed timeouts, and races between test and code under test
2. **Order dependence** — passes alone, fails in a suite because of shared state
3. **Clock & date** — reliance on real time, timezones, or "now" without freezing it
4. **Network & external** — real HTTP, third-party services, unmocked I/O in unit tests
5. **Randomness** — unseeded random data; hash or set ordering assumed stable
6. **Resource leakage** — unclosed connections, ports, or temp files bleeding across tests
7. **Environment sensitivity** — passes locally, fails in CI on parallelism, locale, or filesystem

## Phase 3 — Curate
- Rank by how often each blocks a build and how central the test is.
- For each, give the fix — freeze the clock, seed the data, mock the boundary, isolate the resource.
- Decide fix-now versus quarantine: keep a flaky critical test's intent, but stop it blocking others.

## Phase 4 — Report
Create `FLAKY.md` at repo root:
1. **Suspected flakes** — each: test · nondeterminism source · how to reproduce · confidence
2. **Fixes** — the deterministic replacement for each source
3. **Quarantine list** — the flakes to isolate now versus fix now, and why
4. **Prevention** — the patterns (fixed clock, seeded random, sanctioned mocks) to adopt

## Rules
- Name the source of nondeterminism; "sometimes fails" is not a diagnosis
- Quarantine to unblock, but quarantine is a debt, not a fix
- Report only — end by asking which flaky tests to fix first
