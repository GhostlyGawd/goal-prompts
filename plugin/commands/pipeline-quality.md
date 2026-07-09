---
description: "Run every job twice on paper and yesterday once more — duplicates, half-written partitions, now() in a backfill — and a ledger of who notices stale data."
---

# Goal: Data Pipeline Quality

You are working inside this repo. Mission: audit the pipelines that move and transform data — with two paper experiments per job: run it twice (what duplicates?), and run it for last Tuesday (can it even target the past?) — then write the freshness ledger: for every dataset, who or what notices when it goes stale.

Read-only pass. Read the jobs, schedules, and SQL; run nothing that writes. Your only write is the report file.

## Phase 1 — Map the pipelines
- Inventory every job: trigger/schedule → sources → transforms → destinations. Include the cron nobody remembers and the notebook that became production.
- For each destination dataset, note who consumes it downstream — dashboards, models, exports, other jobs.
- Find the existing safety net: data tests, row-count checks, freshness alerts, or nothing.

## Phase 2 — Audit through 7 lenses
Every finding cites the job and line — the INSERT, the now(), the missing check.
1. **The twice-run test** — run each job twice on paper: blind INSERTs that duplicate, or MERGE/upsert/partition-overwrite that converges; cite the write statement
2. **The backfill test** — can the job target an arbitrary past window, or is `now()`/`today` baked into its logic so history is unreachable; cite the timestamp source
3. **Half-written visibility** — a job dies mid-write: do consumers see a partial partition, or is the write staged-then-swapped atomically
4. **Freshness contracts** — per dataset: the expected update cadence, the check that enforces it, and who is told; "a customer notices" is a finding
5. **Tests on data, not just code** — assertions on row counts, nulls, uniqueness, and referential integrity at pipeline boundaries — or unit tests only, while the data goes unchecked
6. **Schema drift at the gates** — an upstream adds, renames, or retypes a column: does ingestion fail loudly, adapt, or silently write garbage
7. **Lineage & blast radius** — when a table is wrong, can you name every downstream consumer from code, or does the incident do the naming

## Phase 3 — Curate
- Rank by silent-damage potential: wrong-but-plausible data feeding a dashboard outranks a loud crash.
- For each, name the mechanism: an idempotent write pattern, a parameterized run date, a staged swap, a freshness check with an owner.
- Distinguish jobs to harden from jobs to rewrite; a notebook-turned-pipeline usually knows which it is.

## Phase 4 — Report
Create `PIPELINES.md` at repo root:
1. **Pipeline map** — job · schedule · sources → destinations · downstream consumers
2. **The two tests** — per job: twice-run verdict · backfill verdict, each with the cited line
3. **Freshness ledger** — dataset · expected cadence · enforcing check or "none" · who finds out
4. **Findings** — each: lens · job (file:line) · silent or loud failure · the mechanism to fix it
5. **First hardening** — the one change that prevents the most silent damage

Start the report with today's date. If `PIPELINES.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- A pipeline that cannot re-run yesterday is one incident away from data loss
- Loud failure is a feature; silent plausible data is the enemy
- No data pipelines or scheduled transforms in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which pipelines to harden first
