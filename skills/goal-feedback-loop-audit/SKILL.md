---
name: goal-feedback-loop-audit
description: "How user signal re-enters the product — corrections captured or evaporating, thumbs nobody reads, and the complaint-to-fix path. Audit brief 45 · Product — runs a four-phase audit of the current repo and writes FEEDBACK.md at the repo root."
---

# Goal: Feedback Loop Audit

You are working inside this repo. Mission: trace how user signal enters this product and whether it ever changes anything — or whether feedback is collected into a void.

Read-only pass. Your only write is the report file.

## Phase 1 — Map the signal channels
- Every way users tell you something: thumbs and ratings, edits and corrections of outputs, retries, abandonments, support tickets, cancellations.
- For each: where does the signal land — a table, a tool, a Slack channel, nowhere?
- Find the readers: search the code and docs for anything that *consumes* each signal.

## Phase 2 — Audit through 7 lenses
1. **Capture gaps** — the richest signals uncollected: a user editing the agent's output is a labeled correction, vanishing on save; a retry is a thumbs-down nobody logged
2. **Dead-end signals** — thumbs stored in a table with zero readers; the census of write-only feedback
3. **Loop latency** — complaint → fix: is there a path at all, and how long is it in practice
4. **Signal-to-artifact wiring** — bad runs becoming eval cases (34), corrections becoming few-shots or prompt fixes (30), feature pain becoming roadmap items
5. **Closing with users** — "you reported this, it's fixed" — the cheapest retention message that almost nobody sends
6. **Raw-session review** — does any human regularly read real transcripts, or only dashboards of averages
7. **Ask fatigue** — rating prompts so frequent that response rates collapse; measure what's actually answered

## Phase 3 — Curate
- Rank channels by signal quality × current waste: high-quality ignored signals first
- Every wiring proposal names source, destination artifact, and owner

## Phase 4 — Report
Create `FEEDBACK.md` at repo root:
1. **Signal inventory** — channel · volume · destination · readers found
2. **Dead-ends ranked** — the write-only list
3. **The wiring plan** — signal → artifact (eval, prompt, roadmap) → mechanism
4. **The loop to close this week** — one signal, end to end, spelled out
5. **Ask hygiene** — what to stop asking

Start the report with today's date. If `FEEDBACK.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Feedback that changes nothing is a survey, not a loop
- Corrections are gold: captured labels users paid you with their patience to create
- No user feedback channels in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which loop to close first
