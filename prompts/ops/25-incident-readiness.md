---
id: "25"
title: Incident Readiness Review
family: Ops
question: does it run?
output: RELIABILITY.md
tagline: The 3am table — for each failure scenario: how you'd detect it, how you'd respond, and the gap in between.
---
# Goal: Incident Readiness Review

You are working inside this repo. Mission: for every plausible failure, answer three questions — how would you know, what would you do, how bad does it get — and close the gap between today's answers and good ones.

Read-only pass. Your only write is the report file.

## Phase 1 — Enumerate what can fail
- List external dependencies (database, third-party APIs, queues, storage, email) and critical internal services.
- For each: what does the code do today when it's down, slow, or returning garbage? Trace the actual handling.
- Find the backups: do they exist, and has a restore ever been tested?

## Phase 2 — Audit through 7 lenses
1. **Failure handling** — timeouts set? retries with backoff? or infinite hangs and instant cascades
2. **Degradation** — when a dependency dies, does one feature die or does the whole app?
3. **Detection** — for each scenario: would an alert fire, or would a user report it first? Estimate time-to-know
4. **Runbooks** — for the top 5 likely incidents: does written guidance exist, or does response depend on one person's memory?
5. **Restore reality** — backups untested are hopes; trace the restore path and its expected duration
6. **Human single points** — operations only one person can perform; access only one person holds
7. **Blast radius** — can one bad deploy, one poisoned job, or one heavy tenant take everything down?

## Phase 3 — Curate
- Rank scenarios by likelihood × impact × current unreadiness
- Every gap names its cheapest meaningful mitigation

## Phase 4 — Report
Create `RELIABILITY.md` at repo root:
1. **The 3am table** — scenario · detection today · response today · gap · fix
2. **Backup/restore verdict** — with the untested-assumption list
3. **Top 5 runbooks to write** — with a skeleton outline for each
4. **Cheapest resilience wins** — timeouts, alerts, and kill switches shippable this week
5. **The nightmare scenario** — the worst plausible day, narrated, and what changes it

## Rules
- An untested backup is a hypothesis; label it as one
- Detection before prevention: knowing fast beats never failing
- Report only — end by asking which gaps to close
