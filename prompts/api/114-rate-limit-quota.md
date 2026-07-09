---
id: "114"
title: Rate-Limit & Quota Design
family: API
question: will developers adopt it?
output: QUOTAS.md
tagline: The API's rate limits and quotas as a product surface — whether they protect the system while staying fair, predictable, and workable for real consumers.
---
# Goal: Rate-Limit & Quota Design

You are working inside this repo. Mission: judge the API's rate limits and quotas from the consumer's side — whether they protect the platform without punishing well-behaved developers, and whether a client can see and adapt to them instead of hitting a wall.

Read-only pass. Read the limiting logic, its responses, and its documentation; change nothing but the report file.

## Phase 1 — Map the limits
- Find where limits and quotas are enforced and where they are absent.
- Note how a client learns its limit and its remaining budget.
- See what happens when a limit is hit: the status, the message, the guidance.

## Phase 2 — Audit through 7 lenses
1. **Limits exist** — the endpoints and actions with no limit that should have one
2. **Fairness & granularity** — per-key or per-tenant limits versus one global bucket; noisy neighbors
3. **Communicated limits** — standard headers (limit, remaining, reset) so clients can self-regulate
4. **Predictable behavior** — clear 429s with `Retry-After`; no silent throttling or opaque failure
5. **Burst vs sustained** — absorbing legitimate bursts without punishing them; token bucket vs fixed window
6. **Tiering & quotas** — limits matched to plan tiers; documented quotas; defined overage behavior
7. **Documentation** — limits published and discoverable, not learned by hitting them

## Phase 3 — Curate
- Rank by impact on legitimate consumers and on system safety; an unlimited expensive endpoint is both a fairness and a reliability gap.
- For each, name the fix — a header, a `Retry-After`, per-key buckets, a documented quota.
- Separate "protect the system" from "be fair and clear"; good limits do both.

## Phase 4 — Report
Create `QUOTAS.md` at repo root:
1. **Limit posture** — per surface: limited? fair? communicated?
2. **Findings** — each: lens · surface · the gap · the fix
3. **Consumer experience** — the headers and `Retry-After` behavior to make limits self-regulating
4. **Tiering** — the quota-per-tier and overage design to adopt

Start the report with today's date. If `QUOTAS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- A limit the client cannot see is a trap; publish it in headers
- Rate limiting is a product feature, not just a defense
- No rate-limited API surface in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which limit changes to make first
