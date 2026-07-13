---
name: goal-monetization-map
description: "Find the premium-worthy features, the natural upgrade moments, and the billing friction between users and paying you. Goal Prompt 11 · Growth — inspects the current repo and writes REVENUE.md at the repo root."
---

# Goal: Monetization Map

You are working inside this repo. Mission: map how this product makes money — or could — by finding premium-worthy value, natural upgrade moments, and the friction between a willing user and a completed payment.

Read-only pass. Your only write is the report file.

## Phase 1 — Understand the current model
- What exists today: free, paid, tiers, trials? Where does billing code live, if anywhere?
- What is expensive to serve (compute, storage, third-party costs) — and is that cost gated?
- What do power users do here that casual users don't? (infer from features and data model)

## Phase 2 — Audit through 6 lenses
1. **Premium-worthy value** — features that are high-value, costly to serve, collaborative, or power-user-only: natural paid-tier material
2. **Upgrade moments** — where a user hits a limit or a success high point; is there a well-placed, honest prompt there?
3. **Packaging** — free-tier generosity (too much? too little to feel value?); tier logic clarity; what each tier is FOR
4. **Payment friction** — pricing-page clarity, checkout steps, trust signals, what happens on failed payment
5. **Expansion paths** — seats, usage, add-ons: revenue that grows as the customer succeeds
6. **Plumbing gaps** — can users actually upgrade/downgrade/cancel in-product; are limits even enforced in code?

## Phase 3 — Curate
- Every proposal names the willingness-to-pay signal behind it (usage pattern, cost, alternative price)
- Flag churn risks: aggressive gating that would poison goodwill
- Prefer honest value gates over dark patterns — always

## Phase 4 — Report
Create `REVENUE.md` at repo root:
1. **Current model snapshot** — what exists, what's enforced, what leaks
2. **Packaging proposal** — tiers with the one-line job of each
3. **Upgrade moment placements** — where in the UI/code, with trigger conditions
4. **Friction fixes** — pricing page and checkout, ranked
5. **Quick wins vs structural changes**

Start the report with today's date. If `REVENUE.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Monetize value delivered, not hostage features
- Every gate needs a "still generous" free story
- No monetizable product surface in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which changes to make
