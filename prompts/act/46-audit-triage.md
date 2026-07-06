---
id: "46"
title: Audit Triage
family: Act
question: what needs attention?
output: TRIAGE.md
tagline: Fifteen-minute recon that reads the repo and tells you which briefs to run, in what order, and why — the router for the whole catalog.
---
# Goal: Audit Triage

You are working inside this repo. Mission: a fast reconnaissance pass that ends with a ranked, justified list of which audit briefs this specific repo most needs — so the operator spends effort where it pays, not on a blanket sweep.

Read-only pass, fifteen minutes of wall-clock thinking. Your only write is the report file.

## Phase 1 — Read the repo's shape
- Identify what this is: app, service, library, agent product? What stack, what stage, roughly how mature?
- Skim the signals fast: README, package manifest, directory layout, test presence, CI config, recent git log, TODO/FIXME density.
- Detect the character: does this system take payments, hold personal data, call LLMs, run background jobs, serve a UI, ship on a schedule? Each trait pulls in different briefs.

## Phase 2 — Score the catalog against this repo
Weigh each dimension by evidence found, not habit.
1. **Risk exposure** — money, auth, personal data, irreversible actions present → pulls Trust (06–08), Data (21), Guardrails (35)
2. **Agent surface** — LLM calls, tools, loops, prompts in the repo → pulls Agent family (30–38, 48–50)
3. **Change pain** — high churn, big files, sparse tests, felt debt → pulls Quality (01–03), Team (13), Data (22)
4. **Scale pressure** — growth signals, heavy queries, unbounded tables → pulls Speed (04–05, 51), Ops (24)
5. **Maturity gaps** — thin docs, rough onboarding, no release story → pulls Clarity (16–18), Team (14, 52), Ops (23, 53)
6. **Product stage** — early and seeking direction vs live and optimizing → pulls Product (00, 45), Growth (09–12)

## Phase 3 — Curate the route
- Rank the recommended briefs by expected value on THIS repo; cut briefs that don't fit the evidence.
- Group into a sequence: what to run first (highest signal, unblocks others), what can wait.
- Note which briefs would compose well here, and flag brief 28 as the capstone once several reports exist.

## Phase 4 — Report
Create `TRIAGE.md` at repo root:
1. **Repo profile** — what this is, stack, stage, and the traits detected (3–5 sentences)
2. **Recommended briefs** — table: brief · why it fits (cite the evidence) · priority H/M/L · expected finding
3. **Suggested run order** — the sequence, with the reason each comes when it does
4. **Skip list** — briefs that don't fit here, so the operator doesn't waste a run
5. **The first brief to run** — one pick, and what it will likely surface

## Rules
- Every recommendation cites something real in the repo — no generic "you should test more"
- Recommend the fewest briefs that cover the real risk, not the whole catalog
- Report only — end by asking which briefs to run first
