---
description: "What waiting on an agent feels like — progress honesty, interruptibility, showing the work, and salvaging partial results."
---

# Goal: Agent Experience Audit

You are working inside this repo. Mission: walk the experience of using an agent-powered feature — kickoff, the wait, the result, the follow-up — and find where the interface hides, stalls, or strands the human.

Read-only pass. Your only write is the report file.

## Phase 1 — Walk the journey
- Trace the primary agent feature from the user's seat: how a run starts, what the screen shows while it works, how results arrive, what happens next.
- Inventory every UI state in code: idle, queued, running, streaming, partial, failed, done. Which exist? Which are the same spinner?
- Measure or estimate the real wait times per state.

## Phase 2 — Audit through 7 lenses
1. **Progress honesty** — a three-minute spinner vs visible steps; progress bars animating on a timer rather than reality
2. **Interruptibility** — a cancel control exists, is findable, and actually stops the work and the spend — trace what cancel truly does
3. **Latency shaping** — streaming, early partials, or a skeleton of what's coming vs all-or-nothing delivery
4. **Show the work** — can the user see what the agent did — steps taken, sources used — or is it a verdict from a black box?
5. **Failure UX** — the run fails: is the message actionable, are partial results salvaged, is retry one tap or start-over?
6. **Input affordances** — does the interface teach what the agent can and can't do, or is it an empty box and a prayer?
7. **Review before commit** — agent-made changes previewable and reversible, or applied the instant the model speaks (see 43)

## Phase 3 — Curate
- Rank by felt time and felt risk on the most-used flow
- Every fix names its state and component; no vibes-level "improve loading"

## Phase 4 — Report
Create `AGENT-UX.md` at repo root:
1. **Journey walkthrough** — state by state, with real timings
2. **The worst wait** — narrated as the user lives it
3. **Findings** — each: state · lens · fix · effort
4. **The first change** — usually visibility or streaming; spelled out

Start the report with today's date. If `AGENT-UX.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Perceived speed is a design material; honesty about progress builds more trust than speed itself
- Cancel must mean cancel — work, side effects, and billing
- No AI features with a user surface in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fixes to make
