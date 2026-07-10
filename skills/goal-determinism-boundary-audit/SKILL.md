---
name: goal-determinism-boundary-audit
description: "LLM calls that should be plain code, rigid code that should be judgment — redraw the line between deterministic and model-driven. Audit brief 40 · Automation — runs a four-phase audit of the current repo and writes BOUNDARIES.md at the repo root."
---

# Goal: Determinism Boundary Audit

You are working inside this repo. Mission: audit where the line sits between deterministic code and model judgment — and redraw it where the wrong side is doing the work.

Read-only pass. Your only write is the report file.

## Phase 1 — Inventory both sides
- Every model call: input variability, correctness requirement, volume, cost, latency.
- Every complex rule system: regex forests, keyword lists, giant if-trees, scoring heuristics — and the edge-case patches accreted around them (check git log for their churn).

## Phase 2 — Audit through 6 lenses
1. **LLM-that-should-be-code** — fixed transforms, structured-data parsing, arithmetic, template filling, date math: paying tokens and accepting nondeterminism where a function is free and exact
2. **Code-that-should-judge** — brittle rules drowning in exceptions; keyword matching approximating meaning; the if-tree that grows a branch per support ticket
3. **Hybrid seams** — the strong pattern: model extracts, code validates; code narrows candidates, model decides; neither side alone
4. **Missing validation** — model output consumed directly where a deterministic check exists (schema, range, referential integrity, checksum)
5. **Consistency contracts** — places the same input must yield the same output — then why is sampling nondeterministic there?
6. **The escalation ladder** — rules → small model → big model → human: does a ladder exist, or does everything ride the most expensive rung?

## Phase 3 — Curate
- Each migration carries expected deltas: reliability, cost, latency, maintenance
- List what stays model-driven on purpose — genuine judgment, genuine variability — so nobody "optimizes" it later

## Phase 4 — Report
Create `BOUNDARIES.md` at repo root:
1. **Inventory** — call/rule · side today · verdict: keep / demote-to-code / promote-to-model / hybrid
2. **Migrations** — each: change · expected deltas · eval or test to run first
3. **The ladder** — the escalation design for this product
4. **Keep list** — judgment that has earned its tokens
5. **The boundary principle** — one paragraph stating this codebase's rule

Start the report with today's date. If `BOUNDARIES.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Determinism is a feature: never spend variance where exactness is required
- Judgment is a feature too: never fake it with a thousand rules
- No automation mixing deterministic and model-driven steps in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which migrations to make
