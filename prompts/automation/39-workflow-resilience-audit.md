---
id: "39"
title: Workflow Resilience Audit
family: Automation
question: does the process hold?
output: WORKFLOWS.md
tagline: Crash the automation at step 3 of 7 on paper — resumability, idempotency, duplicate side effects, poison inputs, dead letters.
---
# Goal: Workflow Resilience Audit

You are working inside this repo. Mission: crash every automated workflow on paper — mid-step, mid-run, mid-burst — and find where reality diverges from the happy path the code assumes.

Read-only pass. Your only write is the report file.

## Phase 1 — Map the workflows
- List each automated workflow: trigger → steps → outputs → side effects. Mark which steps are model calls, which are code, which touch external systems.
- Where does workflow state live between steps, and what claims to own it?
- Which side effects are visible to users or third parties the moment they happen?

## Phase 2 — Break it through 7 lenses
For each, name the concrete workflow and step.
1. **Crash mid-run** — the process dies at step 3 of 7: does the run resume, orphan, or restart from zero re-doing side effects?
2. **Idempotency** — re-running a step or a whole run: emails sent twice, records duplicated, charges repeated?
3. **Poison inputs** — one malformed item that fails every retry: does it wedge the queue or get quarantined?
4. **Partial outputs** — half-written artifacts and half-applied changes visible to users during or after failure
5. **Timeout coverage** — every external call and model call: bounded, or able to hang a worker forever
6. **Backpressure** — a burst of triggers: queued, dropped, or a thundering herd into your rate limits
7. **Dead letters** — permanently failing items: routed somewhere a human actually sees, or silently retried into eternity (see 03)

## Phase 3 — Curate
- Rank by side-effect severity × likelihood: double-charging beats double-logging
- Every fix names its mechanism: idempotency key, checkpoint, quarantine, timeout value

## Phase 4 — Report
Create `WORKFLOWS.md` at repo root:
1. **Workflow table** — workflow · steps · state store · external side effects
2. **Crash matrix** — workflow × failure scenario → behavior today → gap → fix
3. **Idempotency plan** — the keys and checks, step by step
4. **Dead-letter design** — where failures land and who sees them
5. **The nightmare replay** — the worst plausible failure, narrated in five sentences

## Rules
- Assume every step can die twice: once mid-write, once mid-retry
- Side effects are forever; design for at-least-once delivery or prove exactly-once
- Report only — end by asking which fixes to build
