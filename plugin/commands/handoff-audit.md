---
description: "Every agent-to-human and agent-to-agent baton pass — context dropped, work duplicated, escalations landing where nobody looks."
---

# Goal: Handoff Audit

You are working inside this repo. Mission: trace every baton pass in the system — agent to human, human to agent, agent to agent — and find where context drops, work duplicates, or the baton lands where nobody is standing.

Read-only pass. Your only write is the report file.

## Phase 1 — Map the handoffs
- Enumerate them: escalations, approvals, notifications, task submissions, corrections, sub-agent calls, pipeline stages.
- For each: what payload transfers, in what format, through what channel, with what deadline.
- Which handoffs are load-bearing — the product stalls if they stall?

## Phase 2 — Audit through 7 lenses
1. **Context drops** — the receiver missing what the sender knew: a human shown a conclusion without the evidence; agent B without agent A's constraints and failed attempts
2. **Dead ends** — escalations posted to channels nobody watches; agents waiting on human input with no timeout, reminder, or fallback
3. **Duplication** — receiver redoing sender's work because the handoff didn't carry it, or trust in it
4. **Acknowledgment** — does the sender know the baton was caught? Fire-and-forget passes that fail silently (see 03)
5. **Correction flow** — a human fixes agent output: does the fix flow back into prompts, memory, or evals — or evaporate (see 45)?
6. **Queue visibility** — pending handoffs: countable, aged, alarmed? Or discovered when a user complains
7. **Format mismatch** — agent emits JSON where the human needs prose; human writes prose where the agent needs fields; translation done badly or not at all

## Phase 3 — Curate
- Rank by stall cost: load-bearing handoffs first
- Every fix names the mechanism: payload spec, timeout + fallback, ack, digest

## Phase 4 — Report
Create `HANDOFFS.md` at repo root:
1. **Handoff map** — from → to · payload · channel · deadline · load-bearing?
2. **Findings** — each: handoff · lens · what's lost · fix
3. **Payload specs** — for the worst 3, the exact fields the receiver needs
4. **Timeout and fallback table** — every human-wait, bounded
5. **The one handoff to fix first**

Start the report with today's date. If `HANDOFFS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- A handoff is a contract: payload, deadline, and acknowledgment, or it's a hope
- Escalation paths must terminate at a human who will actually see it
- No handoffs between humans, agents, or systems in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which handoffs to fix
