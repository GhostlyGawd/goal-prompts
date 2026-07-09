---
description: "Whether the data can be trusted — the constraints and checks that prevent the corrupt, orphaned, and contradictory rows that quietly accumulate."
---

# Goal: Data Integrity Audit

You are working inside this repo. Mission: judge whether the schema and the code that writes to it prevent bad data — or merely hope for good data — and find the invariants that are assumed but never enforced.

Read-only pass. Read the schema, models, and write paths; run read-only queries to find existing bad rows; change nothing else. Your only write is the report file.

## Phase 1 — Learn the data model
- Map the core entities, their relationships, and the invariants the domain requires.
- Find every path that writes each entity: endpoints, jobs, migrations, seed scripts, admin tools.
- Note where the same data is written from more than one place.

## Phase 2 — Audit through 7 lenses
Cite the table, column, or write path for every finding.
1. **Constraints** — missing `NOT NULL`, unique, foreign-key, and check constraints the domain needs
2. **Referential integrity** — orphaned rows, dangling references, cascades that delete too much or too little
3. **Duplication** — the same entity stored twice; no natural key to dedupe on
4. **Validation placement** — an invariant enforced in one write path but not the others
5. **Enumerations & state** — free text where an enum belongs; impossible state combinations allowed
6. **Temporal & numeric soundness** — timezone-naive timestamps, float money, nullable-vs-zero confusion
7. **Migration residue** — half-migrated columns, defaults masking missing data

## Phase 3 — Curate
- Rank by blast radius: an invariant that guards money or identity outranks a cosmetic one.
- For each, give the constraint or check to add and a query to find rows already violating it.
- Separate "prevent new bad data" from "clean up existing"; both are needed.

## Phase 4 — Report
Create `INTEGRITY.md` at repo root:
1. **Integrity risks** — ranked by blast radius, with the invariant at stake
2. **Findings** — each: table/column · the missing guard · a query to find bad rows · the fix
3. **Constraint plan** — the constraints and checks to add, ordered by safety
4. **Cleanup** — the existing bad data to reconcile before enforcing

Start the report with today's date. If `INTEGRITY.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- An invariant enforced in code but not the schema will be violated eventually
- Every finding names a query that surfaces the rows already breaking it
- No stored data to keep consistent in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which constraints to enforce first
