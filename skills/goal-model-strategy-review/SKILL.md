---
name: goal-model-strategy-review
description: "Model-to-task fit across every call site — where cheaper and faster would do, where quality is starved, and what happens when a provider blinks. Goal Prompt 36 · Agent — inspects the current repo and writes MODELS.md at the repo root."
---

# Goal: Model Strategy Review

You are working inside this repo. Mission: review every model call site for fit — the right model, settings, and fallback for each job — and find where the product overpays, underserves, or has no plan B.

Read-only pass. Your only write is the report file.

## Phase 1 — Inventory the call sites
- Every place a model is invoked: model name, parameters, purpose, estimated volume, latency tolerance.
- How are models referenced — pinned versions, floating "latest", env config?
- What happens today if the primary provider errors or stalls? Trace it.

## Phase 2 — Audit through 7 lenses
1. **Fit** — frontier models doing classification and extraction a small model handles; small models visibly failing reasoning-heavy jobs (check traces and complaints)
2. **Pinning risk** — floating aliases that drift under you vs pinned versions aging toward deprecation; is there a policy at all
3. **Fallback absence** — provider outage or rate-limit equals product outage; no second model, no queue, no graceful message
4. **Parameter hygiene** — temperatures nobody chose, max_tokens silently truncating outputs, defaults everywhere
5. **Structured output** — parsing prose with regex where JSON mode or tool calling exists
6. **Caching leverage** — provider prompt caching and response memoization unused on repeated prefixes and idempotent calls
7. **Upgrade process** — how a new model version gets evaluated before swap; ad hoc vibes or an eval run (see 34)

## Phase 3 — Curate
- Every swap candidate carries expected deltas: quality risk, latency, cost per call × volume
- Resilience gaps ranked by user-facing blast radius

## Phase 4 — Report
Create `MODELS.md` at repo root:
1. **Call-site table** — site · model · params · volume · latency need · verdict
2. **Swap candidates** — each: current → proposed · expected deltas · eval to run first
3. **Resilience plan** — fallback chain, timeout, and user-facing behavior per failure mode
4. **Pinning policy** — one paragraph the team can adopt
5. **Quick wins** — parameter and caching fixes shippable today

Start the report with today's date. If `MODELS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- No model swap without an eval gate; cost savings that ship regressions are debts
- Match the model to the step, not the brand to the product
- No model calls in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which changes to make
