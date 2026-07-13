---
name: goal-analytics-coverage
description: "Which user behaviors are invisible today — and the tracking plan that makes the five questions that matter answerable. Goal Prompt 20 · Data — inspects the current repo and writes ANALYTICS.md at the repo root."
---

# Goal: Analytics Coverage Audit

You are working inside this repo. Mission: determine which user behaviors are invisible today, and produce the tracking plan that makes the five questions that matter answerable.

Read-only pass. Your only write is the report file.

## Phase 1 — Establish questions and current state
- Infer the 5 questions this team most needs answered (from the product's stage and model): e.g. where does activation fail, which features retain, what precedes churn/upgrade.
- Inventory current tracking: which events exist, where they fire, what tool receives them.
- Trace one key user flow and list every meaningful action along it.

## Phase 2 — Audit through 7 lenses
1. **Invisible behaviors** — key actions (core loop, aha moment, sharing) emitting no event
2. **Funnel blindness** — stages of signup → activation with no instrumentation between them
3. **Naming chaos** — inconsistent event names (tense, casing, verb-noun order) making analysis painful
4. **Context poverty** — events missing the properties needed to segment (plan, source, count, state)
5. **Failure blindness** — errors and abandonments untracked; only successes recorded
6. **Zombie events** — events that fire but nothing consumes, or duplicates measuring the same act differently
7. **Privacy leaks** — personal data flowing into analytics payloads that shouldn't

## Phase 3 — Curate
- Judge every gap against the 5 questions: track what answers them, cut what doesn't
- Fewer well-propertied events beat many shallow ones

## Phase 4 — Report
Create `ANALYTICS.md` at repo root:
1. **The 5 questions** — and an honest can/can't-answer-today verdict for each
2. **Tracking plan** — table: event name · trigger (file/component) · properties · question it serves
3. **Naming convention** — the rule, plus renames for existing events
4. **Privacy fixes** — payloads to scrub
5. **Implementation order** — sequenced by question priority

Start the report with today's date. If `ANALYTICS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every event must serve a named question — no tracking for tracking's sake
- Properties are where the insight lives; name them explicitly
- No product events to instrument in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which events to implement
