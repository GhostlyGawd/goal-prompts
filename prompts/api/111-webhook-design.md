---
id: "111"
title: Webhook Design Audit
family: API
question: will developers adopt it?
output: WEBHOOKS.md
tagline: The webhooks this product sends and receives — delivery guarantees, retries, signing, and whether a consumer can actually build on them reliably.
---
# Goal: Webhook Design Audit

You are working inside this repo. Mission: judge the webhooks this product emits (and any it consumes) as a contract other systems depend on — whether they deliver reliably, prove their origin, and give a developer what they need to build without guessing.

Read-only pass. Read the event-emitting code, delivery mechanism, and any receiving handlers; change nothing but the report file.

## Phase 1 — Map the webhook surface
- List the events the product emits, their payloads, and how delivery happens.
- Find any webhooks the product receives and how it verifies and processes them.
- Note what a consumer is promised about delivery, ordering, and retries.

## Phase 2 — Audit through 7 lenses
1. **Delivery guarantees** — at-least-once versus best-effort; what happens when the consumer is down
2. **Retries & backoff** — a retry policy with backoff and a dead-letter path, or silent give-up
3. **Idempotency & ordering** — a stable event id so consumers can dedupe; any ordering promise
4. **Signing & verification** — signed payloads, a documented scheme, replay protection
5. **Payload design** — a stable, versioned schema with enough context, not a thin id-only ping
6. **Consumer ergonomics** — a way to test, replay, and inspect deliveries; visible failures
7. **Receiving side** — if the product consumes webhooks: signature checks, timeouts, safe processing

## Phase 3 — Curate
- Rank by how badly each gap breaks a consumer: silent drops and unverifiable payloads top the list.
- For each, name the fix — a retry queue, a signature, an event id, a richer payload.
- Separate "unreliable delivery" from "hard to build against"; both lose developers.

## Phase 4 — Report
Create `WEBHOOKS.md` at repo root:
1. **The surface** — events, payloads, and how delivery works today
2. **Findings** — each: severity · lens · what a consumer hits · the fix
3. **Reliability plan** — the retry, dead-letter, and idempotency changes to make delivery trustworthy
4. **Security plan** — the signing and verification a consumer can rely on

Start the report with today's date. If `WEBHOOKS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- A webhook with no retry and no signature is a best-effort rumor
- Design for the consumer whose endpoint was down for five minutes
- No webhooks in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which webhook fixes to make first
