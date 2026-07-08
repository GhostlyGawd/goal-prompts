---
id: "92"
title: Feature-Flag & Rollback Readiness
family: Ops
question: does it run?
output: ROLLBACK.md
tagline: Whether a bad change can be undone fast — whether the system ships behind flags, rolls back cleanly, and has kill switches for its riskiest paths.
---
# Goal: Feature-Flag & Rollback Readiness

You are working inside this repo. Mission: judge how quickly a bad change can be reversed — whether risky work ships dark and toggleable, whether a deploy can be rolled back cleanly, and whether the dangerous paths have an off switch.

Read-only pass. Read the deploy pipeline, migration history, and flag usage; change nothing. Your only write is the report file.

## Phase 1 — Trace how change ships
- Follow a change from merge to production: how it deploys, and how it would be reverted.
- Find the flag system, if any, and how features are turned on and off.
- Note the riskiest paths: migrations, payments, external calls, anything expensive or irreversible.

## Phase 2 — Audit through 7 lenses
1. **Rollback path** — can the last deploy be reverted quickly, or is deploy effectively one-way
2. **Migration reversibility** — schema changes that cannot roll back without data loss; expand/contract discipline
3. **Feature flags** — risky features shipped dark and toggleable, or all-or-nothing at deploy time
4. **Kill switches** — the expensive, external, or experimental paths that can be disabled without a deploy
5. **Flag hygiene** — stale flags never removed, flags with no owner, flag logic gone load-bearing
6. **Progressive delivery** — canary or percentage rollout, or every change straight to 100%
7. **Deploy vs release** — whether code can ship without immediately going live

## Phase 3 — Curate
- Rank by the cost of a bad change on that path: an irreversible migration outranks a toggle nobody uses.
- For each gap, name what to add: a flag, a kill switch, a reversible migration pattern, a canary.
- List stale flags to remove; dead flags are their own risk.

## Phase 4 — Report
Create `ROLLBACK.md` at repo root:
1. **Rollback posture** — how a bad deploy is undone today, and where that breaks down
2. **One-way doors** — the irreversible paths, ranked by risk, each with the fix
3. **Flag hygiene** — stale flags to remove and orphaned flags to assign
4. **Add first** — the flags and kill switches worth introducing now

## Rules
- A migration that cannot roll back turns a bad deploy into an incident
- Every flag is debt; the ones without owners are the expensive kind
- Report only — end by asking which rollback gaps to close first
