---
id: "32"
title: Loop & Termination Audit
family: Agent
question: does the agent deliver?
output: LOOPS.md
tagline: How runs end — iteration caps, stop conditions, stuck-state detection, and the true cost of one pathological run.
---
# Goal: Loop & Termination Audit

You are working inside this repo. Mission: audit how every agent loop ends — on success, on failure, and on the bad days in between — and price what a pathological run costs today.

Read-only pass. Your only write is the report file.

## Phase 1 — Map the loops
- Find every agentic loop: entry point, the per-step cycle, and every path out.
- Record the caps: max iterations, max tokens, max wall-clock, max cost — which exist, what values, and whether anything enforces them.
- What state persists across steps, and what happens to it when a run dies?

## Phase 2 — Audit through 7 lenses
1. **Unbounded loops** — no cap, or a cap so high it's decorative; what stops a runaway besides luck
2. **Stop-condition quality** — the model declaring "done" vs the system verifying done; who checks the work
3. **Stuck-state detection** — same tool called with same args repeatedly, zero-progress steps, oscillation between two states: detected or invisible?
4. **Context exhaustion** — the window fills mid-run: truncate, summarize, crash, or silently degrade? Trace the actual code path
5. **Retry interaction** — retries inside loops inside retries: multiply out the worst case
6. **Zombie runs** — started, abandoned by the user, still burning tokens; who reaps them
7. **Goal drift** — in long runs, is the objective re-anchored, or does step 40 only see step 39?

## Phase 3 — Curate
- Compute the pathological run: max steps × avg tokens per step × price, plus wall-clock
- Rank findings by expected cost × likelihood, not theoretical elegance

## Phase 4 — Report
Create `LOOPS.md` at repo root:
1. **Loop inventory** — loop · caps today · exit paths · state on death
2. **The pathological run** — the arithmetic, written out
3. **Termination matrix** — scenario (success, stuck, exhausted, abandoned, error) → behavior today → gap → fix
4. **Fixes** — ranked; caps and stuck-detection usually first

Start the report with today's date. If `LOOPS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every loop needs a reason it must end — "the model will stop" is not one
- Verified completion beats self-reported completion
- No agent loops in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fixes to make
