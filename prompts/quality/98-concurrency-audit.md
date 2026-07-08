---
id: "98"
title: Concurrency & Race-Condition Audit
family: Quality
question: does it work?
output: CONCURRENCY.md
tagline: The bugs that only appear under load — races, shared mutable state, and ordering assumptions that hold on a quiet laptop and break in production.
---
# Goal: Concurrency & Race-Condition Audit

You are working inside this repo. Mission: find the defects that hide until two things happen at once — races, unguarded shared state, and ordering assumptions that pass every test on a quiet machine and corrupt data under real traffic.

Read-only pass. Read concurrent paths, shared state, and transaction boundaries; change nothing but the report file.

## Phase 1 — Find the concurrent surfaces
- Identify what runs concurrently: request handlers, background jobs, workers, async tasks, webhooks.
- Locate shared mutable state each touches: globals, singletons, caches, the same database rows.
- Note the operations that must be atomic but span several steps.

## Phase 2 — Audit through 7 lenses
Give the interleaving that triggers each finding.
1. **Shared mutable state** — globals, singletons, and caches mutated from concurrent requests or threads
2. **Check-then-act races** — read, decide, write sequences with no atomicity (TOCTOU)
3. **Idempotency** — retries, double-submits, and webhook redelivery that duplicate effects
4. **Locking discipline** — missing locks, over-broad locks, lock ordering that can deadlock
5. **Async ordering** — assumptions that async work completes in order; unawaited work
6. **Transaction boundaries** — multi-statement logic with no transaction; wrong isolation level
7. **External concurrency** — concurrent writes to one row; a job runner processing a task twice

## Phase 3 — Curate
- Rank by blast radius × likelihood: data corruption on a hot path outranks a rare double-log.
- For each, describe the interleaving that triggers it and the fix — atomic op, lock, idempotency key, transaction.
- Flag the ones that are silent: races that corrupt without ever throwing.

## Phase 4 — Report
Create `CONCURRENCY.md` at repo root:
1. **Findings** — each: severity S1–S3 · location · the interleaving that triggers it · the fix
2. **Silent corruptors** — the races that leave no error behind, called out
3. **Systemic fixes** — the idempotency keys, locks, or transaction patterns that close whole classes
4. **How to reproduce** — the concurrency the tests should now exercise

## Rules
- Describe the interleaving; a race with no scenario is a guess
- The dangerous races are the silent ones that corrupt without throwing
- Report only — end by asking which races to fix first
