---
id: "123"
title: Capacity & Scalability Audit
family: Reliability
question: will it stay up?
output: CAPACITY.md
tagline: Every ceiling the config actually sets — pools, workers, queue bounds — read into a headroom ledger naming what saturates first, and at what multiple of today.
---
# Goal: Capacity & Scalability Audit

You are working inside this repo. Mission: read the ceilings this system has actually configured — every pool size, worker count, memory limit, and queue bound — and compute the headroom ledger: how much growth each absorbs before it saturates, and which gives out first.

This is the measured pass: today's ceilings, from config. For the on-paper 10x thought experiment across the whole product — cost, ops, third parties — run 05.

Read-only pass. Your only write is the report file.

## Phase 1 — Read the ceilings out of the config
- Grep the limits that exist: DB pool size, worker and thread counts, memory limits, queue depths, rate limits, autoscale min/max, file handles. Cite each value and its file.
- Find the ceilings nobody set: an unconfigured pool has a number too — name the library default you're inheriting.
- Identify the shared, finite resources several components contend for.

## Phase 2 — Audit through 7 lenses
Every ceiling in a finding is a number with a file, or a named library default.
1. **The arithmetic** — requests per second × queries per request against pool size; workers × job time against arrival rate: which inequality fails first as load grows
2. **Statefulness** — what pins the app to one node: local files, in-memory sessions, sticky state; could a second instance run today, provably
3. **Inherited defaults** — the load-bearing ceilings nobody chose: the default pool of 10, the unbounded default queue, the default heap
4. **Data growth** — queries whose cost grows with table size: missing LIMITs, unindexed scans — cite the query; today's fast is tomorrow's timeout
5. **Queue math** — arrival rate vs drain rate; where work can arrive faster than it drains, what bounds the backlog — memory is not a bound
6. **Saturation behavior** — at each ceiling: queue, shed, or collapse? Find the code that decides, or note that nothing does
7. **Elasticity** — what scales automatically vs what needs a human and a deploy, with the config that proves it

## Phase 3 — Curate
- Build the saturation ladder: order the ceilings by which is hit first at steady growth, arithmetic shown.
- For each rung, name the fix — raise the number, add an index, add a bound, evict the state — and whether it is a config change or an architecture change.
- Flag every ceiling that turns out to be an accident.

## Phase 4 — Report
Create `CAPACITY.md` at repo root:
1. **Headroom ledger** — resource · configured ceiling (file:line, or named default) · estimated consumption today · multiple of today's load until saturation
2. **The saturation ladder** — the order things give out, with the arithmetic
3. **Findings** — each: ceiling · what hits it · behavior at saturation · fix · config vs architecture
4. **The cheapest headroom** — the one config change that buys the most runway

Start the report with today's date. If `CAPACITY.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- A ceiling is a number with a file, never a vibe; unconfigured means the library default, which you name
- The first bottleneck is the audit; average utilization is trivia
- No long-running service in this repo — nothing with pools, workers, or queues to saturate? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which ceilings to raise first
