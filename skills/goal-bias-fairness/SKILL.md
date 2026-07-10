---
name: goal-bias-fairness
description: "Find the code that ranks, scores, or filters people, list the exact fields it consumes, and check whether any eval ever sliced results by group — suspicions labeled. Audit brief 116 · AI-Ethics — runs a four-phase audit of the current repo and writes FAIRNESS.md at the repo root."
---

# Goal: Bias & Fairness Audit

You are working inside this repo. Mission: find the code that decides about people — every function that ranks, scores, filters, approves, or targets users — and audit what the repo can prove: the fields each decision consumes, the thresholds it hardcodes, and whether any evaluation ever checked its results per group.

Read-only pass. Your only write is the report file.

## Phase 1 — Find the deciding code
- Locate every path that ranks, scores, filters, approves, or targets: sort keys, score functions, model calls whose output gates what a user gets, moderation queues, recommendation joins.
- For each, list the exact inputs at the call site — the columns selected, the features built, the prompt variables interpolated. Verbatim, not paraphrased.
- Collect the evaluation surface: test files, eval configs, metrics code — anything that measures these decisions at all.

## Phase 2 — Audit through 6 lenses
Every finding is **measured** (cited from code or eval output) or **suspected** (a risk the repo can't confirm) — label it, and give every suspected finding the measurement that would settle it.
1. **Proxy inputs, read from the field list** — postcode, name, age, gender-coded fields, device or locale signals feeding a score; cite the line where each enters
2. **Hardcoded thresholds** — one global cutoff (score > 0.7, minimum account age) applied to everyone; the cutoff is measured, whom it disadvantages is usually suspected — say both
3. **Unsliced evals** — an eval exists and never groups results by anything; the aggregate metric is measured, per-group harm is unmeasured, and that gap is the finding
4. **Self-feeding loops** — decisions whose outputs re-enter their own training or ranking data; trace the data path in code
5. **Prompt-borne assumptions** — instructions or few-shot examples that encode who the "normal" user is; quote them
6. **Recourse in the code** — after an adverse decision: an appeal path, an explanation string, an override flag — or a code path that simply ends at "denied"

## Phase 3 — Curate
- Rank by decision stakes × people affected: approval and moderation outrank ordering.
- The unmeasured list is a first-class artifact: every subgroup question this repo cannot answer today, each with the eval that would answer it.
- Never launder a suspicion into a finding; the labels are the audit's integrity.

## Phase 4 — Report
Create `FAIRNESS.md` at repo root:
1. **Decision ledger** — decision · code location · exact inputs (verbatim) · threshold · evaluated per group? yes / aggregate-only / not at all
2. **Findings** — each: measured/suspected · lens · evidence (file:line or quoted prompt) · mitigation
3. **The unmeasured list** — the fairness questions the repo cannot answer, each with the eval to build
4. **Priority** — the first three moves: typically a proxy to drop, an eval to slice, a threshold to justify

Start the report with today's date. If `FAIRNESS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- What a decision consumes is a fact in the code — cite the field list verbatim
- Measured and suspected never share a rank; overclaiming bias is its own harm
- No code that ranks, scores, or filters people in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fairness gaps to address first
