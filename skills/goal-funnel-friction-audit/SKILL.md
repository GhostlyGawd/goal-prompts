---
name: goal-funnel-friction-audit
description: "Reconstruct the signup → activation → habit funnel from code, count the steps, and rank every drop-off point. Goal Prompt 09 · Growth — inspects the current repo and writes FUNNEL.md at the repo root."
---

# Goal: Funnel Friction Audit

You are working inside this repo. Mission: reconstruct this product's funnel from the code — entry → signup → first value → habit — count every step a user takes, and rank the friction at each stage.

This audits the funnel's structure — steps, stalls, drop-offs. For persuasion on the public surfaces, run 75; for the first session after signup, run 80.

Read-only pass. Your only write is the report file.

## Phase 1 — Reconstruct the funnel
- Trace the actual path a new user walks: which routes, screens, forms, and confirmations, in what order?
- Count at each stage: screens, fields, clicks, waits, decisions.
- Where is the "aha" — the first moment of real value — and how far from the front door is it?

## Phase 2 — Audit each stage
1. **Entry** — is the value proposition clear above the fold; page weight; does the CTA match what happens next
2. **Signup** — field count, verification walls, OAuth options, password rules, what happens on error
3. **Activation** — required setup before value; empty states that guide vs dead-end; sample data; time-to-first-value in steps
4. **Habit** — reasons to return: saved state, history, notifications or digests, streak/progress mechanics
5. **Silent stalls** — states where a user is stuck with no visible next action
6. **Instrumentation** — is each stage measured; would you even see the drop-off today?

## Phase 3 — Curate
- Rank friction by position × severity: early-funnel losses compound
- Every finding cites the screen/component and the exact moment a user churns
- Kill fixes that add steps to remove steps

## Phase 4 — Report
Create `FUNNEL.md` at repo root:
1. **Funnel map** — stage-by-stage table: steps today · friction found · proposed fix · expected effect · effort
2. **The biggest leak** — one stage, argued in a paragraph
3. **Step-count budget** — steps to first value today vs the achievable minimum
4. **Instrumentation gaps** — events needed to measure this funnel for real

Start the report with today's date. If `FUNNEL.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Count from the user's fingers: taps, fields, waits — not abstractions
- Removing a step beats improving a step
- No user funnel in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fixes to build
