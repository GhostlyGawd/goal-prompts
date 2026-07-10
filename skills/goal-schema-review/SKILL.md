---
name: goal-schema-review
description: "Missing indexes, absent constraints, JSON blobs hiding structure — with a migration plan sequenced safest-first. Audit brief 19 · Data — runs a four-phase audit of the current repo and writes SCHEMA.md at the repo root."
---

# Goal: Schema Review

You are working inside this repo. Mission: review the data model against how the code actually queries it — find the missing indexes, absent constraints, and structural smells — and produce a migration plan sequenced safest-first.

Read-only pass. Your only write is the report file.

## Phase 1 — Extract schema and query patterns
- Reconstruct the schema from migrations, models, or the ORM definitions.
- Map the top query patterns from the code: which lookups, joins, and filters actually run, and how often (hot paths).
- Note table growth: which tables grow with users, with events, without bound?

## Phase 2 — Audit through 8 lenses
1. **Missing indexes** — real query patterns scanning unindexed columns; foreign keys without indexes
2. **Absent constraints** — uniqueness, FKs, and NOT NULL enforced only in app code; the database allowing states the app considers impossible
3. **Accidental nullability** — columns nullable by default that the code always assumes present
4. **Blob smell** — JSON columns hiding fields the code filters or joins on
5. **Naming drift** — inconsistent casing, singular/plural, ambiguous names
6. **Half-applied patterns** — soft-delete on some tables, cascades on some FKs; the inconsistency is the bug
7. **Orphan risk** — deletes that strand child rows; cleanup that depends on app code running
8. **Migration hazards** — pending changes that would lock large tables; irreversible migrations

## Phase 3 — Curate
- Every finding names the symptom it will cause: slow query, corrupt state, painful migration later
- Sequence fixes by risk: additive (indexes, constraints on clean data) → backfills → destructive

## Phase 4 — Report
Create `SCHEMA.md` at repo root:
1. **Schema snapshot** — tables, sizes/growth, relationships in brief
2. **Findings** — each: issue · symptom it causes · evidence (query in code + schema gap) · fix migration sketch · risk
3. **Index plan** — tied to the actual hot queries, not speculative
4. **Migration sequence** — ordered, each step safe and reversible where possible; backfill notes
5. **First migration** — written out

Start the report with today's date. If `SCHEMA.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Index for queries that exist, not queries you imagine
- The database should enforce what the app assumes
- No database schema in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which migrations to write
