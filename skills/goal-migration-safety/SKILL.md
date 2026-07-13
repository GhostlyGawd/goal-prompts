---
name: goal-migration-safety
description: "Schema and data migrations under real traffic — table locks, reversibility, timed-out backfills, and the deploy ordering that turns a change into an outage. Goal Prompt 71 · Data — inspects the current repo and writes MIGRATIONS.md at the repo root."
---

# Goal: Migration Safety

You are working inside this repo. Mission: find the migrations that will bite under real traffic — the ones that lock a hot table, cannot be undone, backfill millions of rows in one transaction, or assume code and schema deploy at the same instant.

Read-only pass. Read the migration history and the code that depends on it. Your only write is the report file.

## Phase 1 — Map the migration path
- What runs migrations (framework, tool, hand-rolled), and when — before deploy, at boot, manually?
- Are migrations reversible by design (down steps), and has a rollback ever been exercised?
- How large are the tables the recent migrations touch, and how much traffic hits them?

## Phase 2 — Audit through 8 lenses
Cite the migration file for every finding.
1. **Locking** — `ALTER TABLE`, index builds, or column changes that take an exclusive lock on a large hot table; is the concurrent/online form used
2. **Reversibility** — irreversible steps (dropped columns, destructive transforms) with no down path or backup gate
3. **Expand/contract** — schema and code shipped as one risky step instead of add-new → migrate → switch → drop-old
4. **Backfills** — data changes in a single unbatched transaction that will time out or bloat the log; no resume-from-progress
5. **Long transactions** — DDL and DML mixed, or a migration holding a transaction open long enough to starve connections
6. **Ordering & compatibility** — old code against new schema (or the reverse) during rollout; NOT NULL added before the app stops writing null
7. **Data safety** — transforms with no dry-run, no row-count check, no before/after validation; silent truncation or precision loss
8. **Partial failure** — a migration that dies halfway: does it resume cleanly or leave the schema wedged

## Phase 3 — Curate
- Separate outage-class hazards (locks a hot table) from cleanliness (a missing down step on a tiny table).
- For each hazard: the failure it produces, the size threshold where it bites, and the safe rewrite.
- Rank by blast radius under production load.

## Phase 4 — Report
Create `MIGRATIONS.md` at repo root:
1. **Verdict** — can you deploy the pending migrations at peak without fear? the scariest one named
2. **Findings** — each: Migration · Lens · Hazard · Trigger (size/traffic) · Safe rewrite · Effort
3. **Rollback reality** — which recent migrations can actually be undone, and how
4. **Pattern to adopt** — the expand/contract or batched-backfill template worth standardizing

Start the report with today's date. If `MIGRATIONS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Judge each migration against the table size and traffic it will really meet
- A hazard names the failure it causes, not just "this looks risky"
- No schema migrations in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which migrations to rewrite first
