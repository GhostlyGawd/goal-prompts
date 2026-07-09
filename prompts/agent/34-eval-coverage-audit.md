---
id: "34"
title: Eval Coverage Audit
family: Agent
question: does the agent deliver?
output: EVALS.md
tagline: The test-gap audit for nondeterminism — golden sets, regression evals, judge quality, and the drift between eval and production.
---
# Goal: Eval Coverage Audit

You are working inside this repo. Mission: map what agent behavior is actually evaluated against what the product actually does, and produce the eval plan that catches regressions before users do.

Read-only pass. Your only write is the report file.

## Phase 1 — Learn the eval reality
- What exists: golden datasets, assertion suites, LLM judges, human review, dashboards? Where do they live, when do they run — CI, ad hoc, never?
- List the product's real task types (from code and traces), with rough volume per type.
- What raw material exists for building evals — traces, logs, user corrections?

## Phase 2 — Audit through 8 lenses
1. **Coverage vs reality** — task types × eval existence: the matrix, with the uncovered high-volume cells circled
2. **Golden-set health** — size, age, whether cases came from real traffic or imagination
3. **Judge quality** — LLM judges never validated against human labels; position, length, and self-preference bias unchecked
4. **Regression protection** — prompt and model changes in git log that shipped with no eval run attached
5. **Eval–prod drift** — sanitized eval inputs vs the messy inputs production actually receives
6. **Metric honesty** — pass rates hiding severity; no cost or latency tracked alongside quality
7. **Nondeterminism handling** — single-sample pass/fail on stochastic outputs; no repeat runs, no variance reported
8. **Failure feedback** — production failures becoming new eval cases, or evaporating

## Phase 3 — Curate
- Rank gaps by volume × blast radius of an unnoticed regression
- Prefer small, real-traffic golden sets over large synthetic ones

## Phase 4 — Report
Create `EVALS.md` at repo root:
1. **Coverage matrix** — task type · volume · eval today · gap
2. **Health verdicts** — golden sets, judges, CI wiring
3. **Eval plan** — each: capability · dataset source (mine the traces) · grader (assertion/judge/human) · size · run trigger
4. **The first eval** — spelled out completely, buildable today

Start the report with today's date. If `EVALS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- An eval that never blocks a ship is a dashboard, not a gate
- Judge the judges: no LLM grader without a human-agreement check
- No LLM behavior to evaluate in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which evals to build
