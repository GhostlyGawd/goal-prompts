---
id: "52"
title: Agent Readiness Audit
family: Team
question: can others build on it?
output: AGENT-READINESS.md
tagline: Can a coding agent work here? Entry files, one-command checks, discoverable conventions, and a mechanical definition of done — audited by attempting the work.
---
# Goal: Agent Readiness Audit

You are working inside this repo. Mission: judge how well this repo supports coding agents as contributors — can an agent orient, make a change, and verify it, without a human whispering tribal knowledge.

Read-only pass. Your only write is the report file. You are the test subject: log your own stumbles as evidence.

## Phase 1 — Cold start
- Spend the first minutes exactly as an arriving agent would: read CLAUDE.md / AGENTS.md / .cursorrules, then CONTRIBUTING, then README. What do they promise?
- Try the promised commands read-only — build, test, lint, typecheck. Record which work as documented, which lie, and which don't exist.

## Phase 2 — Audit through 8 lenses
1. **Entry file** — CLAUDE.md or equivalent: exists, current, and states the commands, the layout, and the don'ts — or every agent starts by guessing
2. **One-command truth** — build, test, and lint each behind one documented command with honest exit codes; the gap between "run the tests" and knowing how
3. **Convention discoverability** — could an agent infer naming, structure, and patterns from three examples, or do the rules live in heads
4. **Feedback speed** — minutes from edit to verdict; slow checks mean agents ship unverified work
5. **Blast-radius guards** — migrations, deploys, destructive scripts: clearly marked and gated, or one innocent command away
6. **Context economics** — what an agent must read to be useful: giant files, generated code not marked as generated, docs that sprawl past their usefulness
7. **Task shape** — are issues scoped and greppable; does a small change touch two files or twelve
8. **Definition of done** — can success be verified mechanically by tests and checks, or only by asking a human

## Phase 3 — Curate
- Walk one small, real task end to end, planning only — orient, locate, plan the change, plan the verification. Log every stumble and what it cost.
- Rank fixes by stumbles removed per unit of effort.

## Phase 4 — Report
Create `AGENT-READINESS.md` at repo root:
1. **Readiness verdict** — the cold-start experience in five lines
2. **Stumble log** — where an agent loses time or confidence, with evidence
3. **Fixes** — ranked; the entry file and one-command checks usually first
4. **The one-hour fix** — the single change that removes the most stumbles

## Rules
- Your own confusion during this audit is admissible evidence — cite it
- Judge what the repo communicates, not what its authors intended
- Report only — end by asking which fixes to make
