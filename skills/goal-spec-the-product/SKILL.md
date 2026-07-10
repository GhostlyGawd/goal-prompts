---
name: goal-spec-the-product
description: "Turns venture research and operator intent into SPEC.md — a contract where every acceptance criterion carries a command a machine can run. Audit brief 142 · Build — runs a four-phase audit of the current repo and writes SPEC.md at the repo root."
---

# Goal: Spec the Product

You are working inside this repo — a product repo scaffolded from the goal-prompts template. Mission: turn the venture research and the operator's intent into `SPEC.md`, a contract in which every acceptance criterion can be checked by a machine.

This is the load-bearing document of the build: 143 implements nothing that is not in it, and 144 ships nothing that fails it. Your only write is the spec file.

## Phase 1 — Collect what is known
- Read the research if it exists: VERDICT.md, POSITIONING.md, DEMAND.md, NICHE.md (root or `reports/`) — the wedge, the buyer, and the pain define the job.
- Read the `SPEC.md` skeleton the scaffold left, and `scripts/spec_lint.py` — the format the gate enforces. The spec must pass it.
- List the questions only the operator can answer (price, name, niche details) and ask them now, rather than inventing answers.

## Phase 2 — Draft through 7 lenses
1. **Job** — the one job the product does, in a sentence a buyer would recognize
2. **Buyer and the first dollar** — who pays, and the shortest wired path from stranger to revenue
3. **Acceptance criteria** — every behavior as `**AC-n** — <criterion> | check: <command>`; if no command can check it, rewrite it until one can, or demote it to a non-goal
4. **Non-goals** — what v1 refuses to do; scope creep dies here, in writing
5. **Interfaces** — inputs, outputs, schemas, error shapes; exact enough to test against
6. **Evals** — for judgment-shaped output, golden cases in `evals/cases/` and a numeric floor
7. **Kill criteria** — the measurable tripwires that mean stop building

## Phase 3 — Harden
- Run `python3 scripts/spec_lint.py` against the draft until it passes; the lint is the format, not a suggestion.
- Strike every AC that restates another; a good v1 spec has 5–12.
- Mark the ACs the first build session should take with `status: next`.

## Phase 4 — Report
Write `SPEC.md` at repo root in the skeleton's sections: Job, Non-goals, Acceptance criteria, Interfaces, Evals, Dependencies, Kill criteria.

Date the header. If `SPEC.md` already exists from a previous run with ratified content, this is a spec revision — read it first, lead with what changed, and never renumber existing ACs; retire them with `status: dropped` instead, because 143's commits cite their ids.

## Rules
- Every AC carries a runnable `check:` — mechanical verifiability is the product-selection constraint, and this is where it is enforced
- The spec must pass `scripts/spec_lint.py` before this brief ends
- Answers you don't have come from the operator, never from imagination
- Not inside a scaffolded repo — no `scripts/spec_lint.py` here? Say so in a one-paragraph null report and stop: run 141 first.
- If a `reports/` directory exists at the repo root, the null report goes there — but `SPEC.md` itself always lives at the root, where the gate reads it.
- Report only — end by asking the operator to ratify the spec before 143 builds against it
