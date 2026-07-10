---
name: goal-token-economics-audit
description: "Cost per completed task, not per call — retry waste, context bloat priced out, cache leverage, and the margin math. Audit brief 38 · Agent — runs a four-phase audit of the current repo and writes TOKENS.md at the repo root."
---

# Goal: Token Economics Audit

You are working inside this repo. Mission: compute what a completed task actually costs — including the retries, failures, and bloat — and rank the savings that don't damage quality.

Read-only pass. Your only write is the report file.

## Phase 1 — Establish the unit
- The unit is cost per **completed task**, not per API call. Define the task types.
- Gather the inputs: model prices, average calls per run, tokens per call (from traces or estimation), retry rates, and failure rates — failed runs still bill.
- Note which numbers are measured vs estimated; mark estimates.

## Phase 2 — Audit through 7 lenses
1. **Failure and retry waste** — tokens spent on runs that produced nothing a user kept; the invisible tax on every success
2. **Context bloat priced** — the stale payloads and token hogs (see 33), converted to money at volume
3. **Cache leverage** — provider prompt caching on stable prefixes; memoization of idempotent calls; both usually unused
4. **Model overkill priced** — frontier pricing on small-model jobs (see 36): the monthly delta, in numbers
5. **Output discipline** — unbounded generations where a cap or terser format loses nothing
6. **Dead spend** — results computed and never read; speculative calls whose outputs get discarded
7. **The scaling curve** — cost at 10x usage: which term grows linearly, which explodes, and where the margin dies if priced

## Phase 3 — Curate
- Show the arithmetic on every estimate — order of magnitude is fine, hand-waving is not
- Flag any saving that trades quality or reliability; those go through an eval (34) first

## Phase 4 — Report
Create `TOKENS.md` at repo root:
1. **Unit economics table** — task type · calls · tokens · retries · cost per success · (margin, if priced)
2. **Waste ranked** — with arithmetic shown
3. **Savings ladder** — cumulative, each step marked safe or needs-eval
4. **The scaling curve** — the 10x projection and the knob that matters most
5. **First change** — best money per unit of effort

Start the report with today's date. If `TOKENS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Per-success is the only honest denominator
- Never save tokens by shipping worse answers unmeasured
- No token spend in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which savings to take
