---
name: goal-abuse-overload
description: "Whether the system defends itself against traffic that is not a well-behaved user — bots, scrapers, floods, and expensive requests that can exhaust it. Audit brief 124 · Reliability — runs a four-phase audit of the current repo and writes ABUSE.md at the repo root."
---

# Goal: Abuse & Overload Protection

You are working inside this repo. Mission: judge how the system holds up against hostile or careless load — the automated abuse, the floods, and the disproportionately expensive requests that can exhaust resources or run up a bill. This is defense against overload, distinct from designing fair API limits.

Read-only pass. Read the exposed endpoints, their cost, and any protections; change nothing but the report file.

## Phase 1 — Find the expensive and exposed
- List the operations that cost far more than a normal request: heavy queries, exports, AI calls, fan-outs.
- Note which of those are reachable without authentication or payment.
- See what protects the system when load spikes.

## Phase 2 — Audit through 7 lenses
1. **Expensive endpoints** — requests that cost far more than they charge or check
2. **Unauthenticated exposure** — costly operations reachable with no login and no cost
3. **Bot & scrape resistance** — defenses against automated abuse, enumeration, and harvesting
4. **Overload behavior** — load shedding and prioritization under flood, or everything falling together
5. **Amplification** — one request that triggers many: fan-out, recursion, unbounded work
6. **Resource exhaustion** — memory, connections, and disk an attacker or bug can consume
7. **Abuse detection** — would sustained abuse be noticed and throttled, or run until it bills or breaks

## Phase 3 — Curate
- Rank by ease of exploitation × cost of the damage: an unauthenticated expensive endpoint tops the list.
- For each, name the defense — auth, a cost ceiling, load shedding, bot mitigation, detection.
- Separate "runs up a bill" from "takes the system down"; both are outages of a kind.

## Phase 4 — Report
Create `ABUSE.md` at repo root:
1. **Exposed & expensive** — the surfaces most attractive to abuse, with their cost
2. **Findings** — each: risk · surface · ease and cost · the defense
3. **Overload behavior** — what happens under flood today, and the shedding to add
4. **Priority** — the defenses to add first, by ease of exploitation and blast radius

Start the report with today's date. If `ABUSE.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- An unauthenticated expensive endpoint is a denial-of-wallet waiting to happen
- Under overload, shed load deliberately; do not let everything fail together
- No public-facing endpoints in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which abuse defenses to add first
