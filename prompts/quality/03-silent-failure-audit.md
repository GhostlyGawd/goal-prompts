---
id: "03"
title: Silent Failure Audit
family: Quality
question: does it work?
output: OBSERVABILITY.md
tagline: Find swallowed errors, missing logs, and monitoring blind spots — everywhere the system can break without anyone knowing.
---
# Goal: Silent Failure Audit

You are working inside this repo. Mission: find every place this system can fail without anyone knowing — swallowed errors, invisible background failures, monitoring blind spots — and produce an instrumentation plan.

Read-only pass. Your only write is the report file.

## Phase 1 — Map how errors are supposed to flow
- Where do errors go today: a logger, a monitoring service, the console, nowhere?
- Which operations are fire-and-forget: background jobs, webhooks, emails, cache writes?
- If the database, a third-party API, or a queue failed right now — what would you see, and how soon?

## Phase 2 — Audit through 8 lenses
Cite file and line for every finding.
1. **Swallowed errors** — empty catch blocks, catch-log-continue, errors mapped to defaults silently
2. **Logs to nowhere** — errors logged where nobody looks; no aggregation or alerting path
3. **Context-free failures** — logs without IDs, user context, or correlation; undebuggable when they fire
4. **User-visible, system-invisible** — the user sees an error state the system never records
5. **Retries that mask** — retry loops hiding a dying dependency until it fully fails
6. **Silent background death** — jobs, crons, webhooks, emails failing with no surfaced signal
7. **Lying health checks** — endpoints returning healthy while core functions are broken
8. **Alert gaps** — failures that are recorded but would never page or notify anyone

## Phase 3 — Curate
- Rank by blast radius × silence: how bad is it, times how long until a human notices
- Keep only findings with a concrete failure scenario attached

## Phase 4 — Report
Create `OBSERVABILITY.md` at repo root:
1. **Blind-spot map** — table: failure scenario · visibility today · time-to-detection · gap
2. **Top 5 "you'd never know" scenarios** — narrated in two sentences each
3. **Instrumentation plan** — each: what to instrument · where (path) · signal type (log/metric/alert) · effort
4. **Quick wins** — swallowed catches to fix this week

Start the report with today's date. If `OBSERVABILITY.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- "It logs to console" is not observability
- Prefer a few high-signal alerts over noisy logging everywhere
- No runtime error paths in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which gaps to close first
