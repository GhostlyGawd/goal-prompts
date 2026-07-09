---
id: "138"
title: Event & Message Contracts
family: Data
question: is it sound?
output: EVENTS.md
tagline: Diff what producers write against what consumers assume — schema drift, ordering bets, missing idempotency keys — and find the message that breaks when a deploy staggers.
---
# Goal: Event & Message Contracts

You are working inside this repo. Mission: audit the contracts between everything that publishes a message and everything that consumes one. The real schema is not in a doc — it is the diff between what producer code writes and what consumer code assumes. Find where that diff bites.

Read-only pass. Your only write is the report file.

## Phase 1 — Build the contract matrix
- Inventory every event and message: queues, topics, webhooks, pub/sub, outbox tables. For each, find every producer and every consumer in the code.
- Extract each event's real shape from the producer's serialization code, and each consumer's real expectations from its parsing code — file:line both sides.
- Note where a schema is declared (registry, shared types, protos) versus implied by code agreement alone.

## Phase 2 — Audit through 7 lenses
Every finding cites producer and consumer code.
1. **Shape drift** — fields written that no consumer reads; fields consumers require that producers only sometimes write; optionality disagreements
2. **Evolution discipline** — how a field gets added or renamed today: versioned, additive-only, or edit-and-pray; do consumers tolerate unknown fields
3. **The staggered deploy** — old consumer meets new event and new consumer meets old event, mid-rollout: trace both directions per event
4. **Ordering bets** — consumers that assume arrival order or exactly-once where the transport promises neither; cite the assuming line
5. **Idempotency keys** — re-delivery of each event: deduplicated by a key, tolerated by design, or a double side effect
6. **Poison & dead letters** — the message that always fails: retried forever, dropped silently, or parked where a human actually looks
7. **Replay safety** — yesterday's events replayed today (backfill, recovery): idempotent catch-up or a duplication disaster

## Phase 3 — Curate
- Rank by side-effect severity × how ordinary the trigger is: a staggered deploy happens every release; rank what it breaks first.
- For each contract gap, name the mechanism: a version field, a tolerant reader, a dedup key, a DLQ with an owner.
- Flag the contracts that exist only as code agreement — each one is drift waiting for a refactor.

## Phase 4 — Report
Create `EVENTS.md` at repo root:
1. **Contract matrix** — event · producers · consumers · declared schema or code-implied · drift found
2. **The staggered-deploy trace** — per risky event: old↔new in both directions, what breaks
3. **Findings** — each: lens · event · producer/consumer (file:line) · failure it causes · the mechanism to fix it
4. **Replay verdict** — could yesterday's stream re-run safely today; the events that say no

Start the report with today's date. If `EVENTS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- The producer's serializer and the consumer's parser are the contract; docs are commentary
- Assume every message arrives twice, late, and out of order — the transport's fine print says it may
- No queues, topics, webhooks, or event streams in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which contract gaps to close first
