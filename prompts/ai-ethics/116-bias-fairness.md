---
id: "116"
title: Bias & Fairness Audit
family: AI-Ethics
question: is the AI responsible?
output: FAIRNESS.md
tagline: Whether the product's AI or algorithmic decisions treat different groups fairly — or whether the data, features, or evaluation bake in bias that harms some users.
---
# Goal: Bias & Fairness Audit

You are working inside this repo. Mission: examine where the product makes automated decisions about people — with a model or an algorithm — and judge whether it treats different groups fairly, or quietly disadvantages some through its data, features, or thresholds.

Read-only pass. Read the model usage, the features it consumes, and any evaluation; change nothing but the report file.

## Phase 1 — Find the decisions that affect people
- Identify where the product ranks, scores, filters, approves, or targets users.
- For each, note the inputs it uses and the outcome it drives.
- Find what fairness measurement, if any, exists today.

## Phase 2 — Audit through 7 lenses
1. **Disparate outcomes** — where outputs or decisions differ across groups with no legitimate reason
2. **Proxy features** — inputs that stand in for protected attributes (zip for race, name for gender)
3. **Data skew** — training or reference data that under- or misrepresents some users
4. **Evaluation gaps** — no measurement across subgroups; only aggregate metrics
5. **Feedback loops** — decisions that reinforce themselves (who is shown, who is approved)
6. **Threshold & calibration** — one cutoff that is fair on average but unfair per group
7. **Human recourse** — can an affected user understand and contest a decision

## Phase 3 — Curate
- Rank by potential harm × number affected: a biased approval decision outranks a cosmetic ranking skew.
- For each, distinguish measured bias from plausible-but-unmeasured risk, and say which.
- Name the mitigation — a proxy to drop, a subgroup metric to track, a threshold to recalibrate.

## Phase 4 — Report
Create `FAIRNESS.md` at repo root:
1. **Decision map** — where the product decides about people, and on what inputs
2. **Findings** — each: potential harm · lens · evidence or hypothesis · the mitigation
3. **What is unmeasured** — the fairness the product does not currently check
4. **Priority** — the subgroup evaluations and mitigations to add first

Start the report with today's date. If `FAIRNESS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Aggregate accuracy can hide per-group harm; measure across subgroups
- Say plainly what is measured versus suspected; do not overclaim either way
- No model-driven decisions in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fairness issues to address first
