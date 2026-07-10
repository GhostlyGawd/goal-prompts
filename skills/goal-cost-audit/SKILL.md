---
name: goal-cost-audit
description: "Expensive queries, chatty API loops, unbounded storage, oversized resources — savings ranked by effort. Audit brief 24 · Ops — runs a four-phase audit of the current repo and writes COSTS.md at the repo root."
---

# Goal: Cost Audit

You are working inside this repo. Mission: find where this system spends money it doesn't need to — compute, storage, third-party calls, egress — and rank the savings by effort.

Read-only pass. Your only write is the report file.

## Phase 1 — Identify the cost drivers
- From code and config: what does this system pay for? Compute/hosting, database, storage, third-party APIs, email/SMS, telemetry.
- Which of those scale with usage, and which are flat?
- Where are the metered calls: every paid API and the code that hits it.

## Phase 2 — Audit through 7 lenses
1. **Expensive frequent work** — heavy queries or jobs on hot paths or tight schedules; recomputing what could be stored
2. **Chatty loops** — per-item API calls that batch endpoints could collapse; N calls where 1 would do
3. **Missing caches** — repeated identical fetches of slow-changing data from paid sources
4. **Unbounded growth** — logs, blobs, soft-deleted rows, old versions accumulating forever with no lifecycle policy
5. **Oversize by config** — instance sizes, provisioned capacity, always-on resources for spiky workloads
6. **Telemetry volume** — logging/tracing at a verbosity that costs real money to ingest and store
7. **Redundant schedules** — crons doing overlapping work, or work whose output nobody reads

## Phase 3 — Curate
- Estimate monthly impact per finding — order of magnitude is fine; show the arithmetic
- Rank by savings ÷ effort; flag anything that trades reliability for pennies

## Phase 4 — Report
Create `COSTS.md` at repo root:
1. **Cost driver map** — what's paid for and what it scales with
2. **Findings** — each: issue · location · monthly impact estimate · fix · effort · risk
3. **Savings ladder** — ranked, cumulative estimate
4. **Lifecycle policies to add** — retention/archival rules for the unbounded growth
5. **Verification plan** — how to confirm each saving after the change

Start the report with today's date. If `COSTS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Show the arithmetic behind every estimate
- Never save money by making failures more likely — flag those tradeoffs
- No traceable infrastructure or service spend in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which savings to take
