---
id: "43"
title: Human-in-the-Loop Placement
family: AI-UX
question: does the human trust it?
output: HITL.md
tagline: Approval gates audited for rubber-stamp fatigue and silent damage — who reviews what, when, with enough context to actually judge.
---
# Goal: Human-in-the-Loop Placement

You are working inside this repo. Mission: audit where humans sit in the agent's loop — which actions are gated, which run silent — and redesign the placement so review happens where it matters and nowhere else.

Read-only pass. Your only write is the report file.

## Phase 1 — Map gates and gaps
- Inventory every approval or review gate: what's gated, who reviews, what they're shown, and the volume.
- If traces exist, pull the rejection rate per gate — approval rates near 100% are a finding, not a comfort.
- Inventory the inverse: irreversible or external-facing actions with **no** gate at all.

## Phase 2 — Audit through 7 lenses
1. **Rubber-stamp fatigue** — high-volume, low-rejection gates training humans to click yes; worse than no gate because it manufactures false safety
2. **Missing gates** — silent sends, deletes, publishes, payments; rank by blast radius (see 35)
3. **Review context** — the approver sees enough to actually judge — the evidence, the diff, the recipient — or just a button labeled Approve
4. **Placement logic** — gates before cheap reversible steps, nothing before the expensive irreversible one
5. **Interrupt vs digest** — ten pings a day vs one reviewable batch; which does each gate deserve
6. **Escalation criteria** — uncertainty, stakes, or novelty routing to humans dynamically, or the same fixed rule for everything
7. **Rejection capture** — a human says no: is the reason recorded and fed back (see 45), or discarded with the click

## Phase 3 — Curate
- Sort every action class into gate / sample-review / log-only, and defend each placement
- The scarce resource is human attention; spend it where judgment changes outcomes

## Phase 4 — Report
Create `HITL.md` at repo root:
1. **Gate inventory** — gate · volume · rejection rate · context shown · verdict
2. **Fatigue findings** — where approval has become theater
3. **Missing-gate list** — by blast radius
4. **The placement map** — every action class: gate / sample / log, with reasons
5. **Review UX fixes** — what each approver needs on screen

Start the report with today's date. If `HITL.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- A gate humans always approve protects no one and costs everyone
- Gate by consequence, not by convenience of implementation
- No automated decisions needing human oversight in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which placements to change
