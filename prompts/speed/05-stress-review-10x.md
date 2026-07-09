---
id: "05"
title: 10x Stress Review
family: Speed
question: does it scale?
output: SCALE.md
related: 123
tagline: Simulate 10x users, data, and traffic on paper — find what breaks first, at what threshold, and the cheapest mitigation.
---
# Goal: 10x Stress Review

You are working inside this repo. Mission: put tomorrow's load on today's architecture — 10x the users, 10x the data, 10x the traffic — and find what breaks first, in what order, and what each fix costs.

This is a thought experiment on tomorrow's load, the whole product included — cost, ops, third parties. For today's configured ceilings, measured from config, run 123.

Read-only pass, thinking on paper. Your only write is the report file.

## Phase 1 — Establish today's scale
- Infer current scale from code and config: pool sizes, rate limits, page sizes, batch sizes, timeouts.
- Which growth axis matters most for this product: users, data volume, traffic spikes, or tenant count?
- Which tables, queues, and stores grow without bound?

## Phase 2 — Stress through 7 lenses
For each, name the breaking mechanism and estimate the threshold.
1. **10x data** — unpaginated queries, full scans, unbounded UI lists, tables with no archival story
2. **10x users** — connection pools, session storage, rate limits, lock contention, auth bottlenecks
3. **Single points of failure** — one-instance assumptions, local file state, in-memory queues/caches that don't survive restarts or replicas
4. **Jobs & queues** — backlog behavior under load, retry storms, poison messages, no dead-letter path
5. **Third-party ceilings** — API quotas and rate limits you'll hit at 10x
6. **Cost curve** — what scales linearly vs what explodes (per-request third-party calls, storage egress)
7. **Operational load** — manual steps that become 10x painful (deploys, support lookups, data fixes)

## Phase 3 — Curate
- Order findings by which breaks first as load grows
- For each: cheap patch vs real fix — name both
- Explicitly list what NOT to fix yet (premature scaling is also a bug)

## Phase 4 — Report
Create `SCALE.md` at repo root:
1. **Today's scale snapshot** — the numbers and assumptions
2. **First-to-break ranking** — each: bottleneck · breaking mechanism · estimated threshold · symptom users would see
3. **Mitigations** — cheap patch and real fix per bottleneck, with effort
4. **Do-not-fix-yet list** — premature optimizations to consciously skip
5. **The one change** — biggest headroom per unit of effort

Start the report with today's date. If `SCALE.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every bottleneck needs a mechanism — "might be slow" doesn't count
- Respect today's simplicity: recommend the least architecture that survives 10x
- No load-bearing system in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which mitigations to build
