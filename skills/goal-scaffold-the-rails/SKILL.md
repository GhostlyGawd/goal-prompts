---
name: goal-scaffold-the-rails
description: "Installs the golden-path harness into this repo — greenfield or grafted onto existing code — and proves the gate bites, red fails, green passes, before more code lands. Audit brief 141 · Build — runs a four-phase audit of the current repo and writes SCAFFOLD.md at the repo root."
---

# Goal: Scaffold the Rails

You are working inside this repo — the repo the product actually lives in, whether it is empty or already full of code. Mission: install the goal-prompts golden-path harness here and prove it bites — red fails, green passes — before any further product code lands.

This is a Build brief: it writes files, but only after the operator approves the plan at the Phase 2 gate.

## Phase 1 — Locate the mandate and the template
- Find the mandate: a `VERDICT.md` go ruling (at this root or in `reports/`), or the operator's explicit ask to put this repo on rails. Quote it.
- Locate the template: the `template/` directory of the goal-prompts repo — a local checkout, or `git clone --depth 1 https://github.com/GhostlyGawd/goal-prompts`.
- Read `template/README.md` end to end; it is the contract for what you are about to install.

## Phase 2 — Audit readiness, then ask
Score the installation through these lenses; cite evidence:
1. **Mandate** — a documented go, or an explicit operator ask? A hunch is not a mandate.
2. **Mechanical verifiability** — can this product's quality be checked by commands: tests, schema validation, golden files, rubric-scored evals with a numeric floor? If quality is pure taste, say so — this harness is the wrong tool.
3. **Mode** — greenfield (empty repo: copy the whole template) or graft (existing code: install the harness layer plus the SPEC.md and DECISIONS.md skeletons, clobbering nothing)?
4. **Existing checks** — what test, lint, and build commands already run here? Propose the one-line wiring of each into `scripts/check`; the operator ratifies those exact lines at this gate, because the harness is operator-owned.
5. **Stack fit** — the template default is Python 3 stdlib + unittest, zero dependencies. Any deviation needs a DECISIONS.md entry; name it now.
6. **Operator duties** — what only a human can do: push to GitHub, make the `check` workflow a required status check, point CODEOWNERS at themselves.

Then stop. Report only — end by asking whether to install as planned, adjust, or abort. Nothing is written until the operator answers.

## Phase 3 — Install and prove
1. Copy the agreed files into this repo; `git config core.hooksPath .githooks`. Never overwrite an existing file unless the plan listed it.
2. Run `scripts/check` — must pass green before any new product code.
3. Run `scripts/check --prove-red` — plants a failing canary and asserts the gate goes red; a gate that cannot fail is not a gate. Capture both outputs.
4. Fill ADR-0001 in DECISIONS.md (product, date, mode, wiring, deviations) and commit as `scaffold: harness from goal-prompts template`.

## Phase 4 — Report
Create `SCAFFOLD.md` at repo root:
1. **What was installed** — files added; in graft mode, the existing commands now wired into the gate
2. **Harness proof** — the green run and the prove-red run, verbatim tails
3. **Operator TODOs** — the Phase 2 duties still open, as checkboxes
4. **Next** — run 142 · Spec the Product to write SPEC.md before building

Start the report with today's date. If `SCAFFOLD.md` already exists from a previous run, this repo is already on rails — verify the harness still bites and lead with what changed since.

## Rules
- Nothing is written before the Phase 2 gate; the operator's answer is the scope
- Graft mode clobbers nothing: existing files are never overwritten, and existing tests keep running — now inside the gate
- The installed harness layer (`scripts/`, `.githooks/`, `.github/`, `.claude/`, `tests/harness/`) is operator-owned from the moment it lands
- No go verdict and no operator ask to put this repo on rails? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking at the Phase 2 gate before creating anything
