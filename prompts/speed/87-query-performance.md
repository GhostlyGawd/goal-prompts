---
id: "87"
title: Query Performance & N+1 Audit
family: Speed
question: does it scale?
output: QUERIES.md
tagline: The database access patterns that fall over as data and traffic grow — N+1s, missing indexes, unbounded reads, and lock contention.
---
# Goal: Query Performance & N+1 Audit

You are working inside this repo. Mission: find the data-access patterns that are fine on a laptop and fatal in production — the queries whose cost grows with rows, traffic, or both.

Read-only pass. Read the data-access code and schema; run read-only `EXPLAIN`/query logs if available; change nothing. Your only write is the report file.

## Phase 1 — Find the hot paths
- Identify the highest-traffic and most expensive endpoints and jobs.
- Trace how each reads data: raw queries, ORM calls, what is loaded eagerly vs lazily.
- Note the tables that grow without bound; queries against them age worst.

## Phase 2 — Audit through 7 lenses
Give the query and its call site for every finding.
1. **N+1 queries** — a query per row; ORM lazy-loads inside a loop, serializer, or render
2. **Missing indexes** — filters, joins, and sorts on unindexed columns; full-table scans
3. **Unbounded results** — queries with no limit or pagination that grow with the table
4. **Over-fetching** — `SELECT *`, loading columns and relations never used, chatty round-trips
5. **Hot-path cost** — the queries on the busiest routes and the ones issued per request
6. **Transactions & locking** — long transactions, lock contention, N+1 writes
7. **Caching gaps** — identical reads repeated every request that never memoize or cache

## Phase 3 — Curate
- Rank by cost × frequency: a cheap query on the hottest path can outweigh a slow rare one.
- For each, name the fix: an index, an eager-load, a batch, a bound, or a cache.
- Distinguish a code fix from a schema change; size each.

## Phase 4 — Report
Create `QUERIES.md` at repo root:
1. **Worst offenders** — ranked by cost × frequency, with the query and call site
2. **Findings** — each: pattern · location · why it scales badly · the fix · effort
3. **Index plan** — the indexes to add, and the queries each serves
4. **How to confirm** — the measurement that proves each fix worked

Start the report with today's date. If `QUERIES.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Rank by cost × frequency, not raw query time
- An index is not free; justify each by the queries it serves
- No database queries in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which queries to optimize first
