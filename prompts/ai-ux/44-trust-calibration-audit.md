---
id: "44"
title: Trust Calibration Audit
family: AI-UX
question: does the human trust it?
output: TRUST.md
tagline: Confidence theater vs honest hedging — uncertainty channels, citation integrity, and what the product does after being wrong.
---
# Goal: Trust Calibration Audit

You are working inside this repo. Mission: audit whether this product's expressed confidence matches its actual reliability — and fix the places where certainty is theater.

Read-only pass. Your only write is the report file.

## Phase 1 — Collect the confidence surfaces
- Everywhere the product signals capability or certainty: output tone, disclaimers, onboarding promises, empty states, error copy, marketing strings in the UI.
- What does the system actually know about its own reliability — eval scores (34), failure rates (37) — and does any surface reflect it?

## Phase 2 — Audit through 7 lenses
1. **Confidence theater** — uniformly authoritative tone regardless of task difficulty; prompts or post-processing that strip the model's own hedges
2. **Uncertainty channels** — any mechanism to express "not sure" — phrasing, scores, abstention — and whether it correlates with actual error or is cosmetic
3. **Citation integrity** — sources displayed: do they exist, and do they support the sentence they decorate? Spot-check the mechanism, not just the rendering
4. **Abstention design** — can the agent decline, ask, or escalate instead of guessing — and does the UX punish declining so hard the model never does
5. **Failure honesty** — after a wrong answer: correction visible, silent edit, or never acknowledged at all
6. **Capability framing** — what onboarding and empty states promise vs what evals show it delivers; the gap is churn in incubation
7. **Trust repair** — the flow after a user catches an error: apology-and-fix path, or nothing (see 45)

## Phase 3 — Curate
- Rank by damage: overconfidence on high-stakes outputs first
- Every fix is concrete copy, a rendering change, or a mechanism — not "be more honest"

## Phase 4 — Report
Create `TRUST.md` at repo root:
1. **Surface inventory** — surface · current signal · reality it should reflect
2. **Theater findings** — with verbatim examples
3. **Calibration fixes** — where uncertainty enters, how it renders, what triggers abstention
4. **Citation fix plan** — from decoration to verification
5. **Copy rewrites** — worst 5, before/after

Start the report with today's date. If `TRUST.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Calibrated trust beats maximal trust: users who know when to check stay longer
- Never let styling erase the model's honest doubt
- No AI output shown to users in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fixes to make
