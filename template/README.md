# The golden-path template

This directory is a complete, self-verifying product repository. Brief
`141 · Scaffold the Rails` copies it to a new path, runs `git init`, wires the
hooks, and proves the gate bites — that is a product repo, ready for
`142 · Spec the Product`. This README is the template's spec; it ships with
every instantiation so the rules travel with the code.

**Design rule (the enforcement hierarchy):** deterministic enforcement
(hooks, CI, exit codes) beats executable artifacts (scripts, templates),
which beat written instructions. A capable-but-fallible agent can rationalize
past prose; it cannot rationalize past a failing exit code. Everything
load-bearing here is therefore a command that exits non-zero.

## Two layers

**The harness layer — operator-owned, agent-read-only:**

| Path | What it is |
|---|---|
| `scripts/check` | the one gate: spec lint → tests → evals. `--prove-red` plants a failing canary and asserts the gate goes red |
| `scripts/spec_lint.py` | deterministic spec linter: required sections, the AC grammar, built-ACs-have-tests, dependencies-have-ADRs |
| `scripts/hook-protect` | Claude Code PreToolUse hook — blocks any edit to the harness layer (exit 2) |
| `scripts/hook-check` | Claude Code PostToolUse hook — runs the gate after every file edit, blocks on red (exit 2) |
| `.claude/settings.json` | wires both hooks |
| `.githooks/pre-commit` | runs the gate before every commit (`git config core.hooksPath .githooks`) |
| `.github/workflows/check.yml` | CI runs the same gate on every push and PR |
| `.github/CODEOWNERS` | routes harness-layer changes to the operator |
| `tests/harness/` | tests of the harness itself: hooks wired, files present, spec lint honest |

**The product layer — the agent builds here:**
`src/` (code), `tests/` (product tests, outside `tests/harness/`), `evals/cases/`
(golden cases), `SPEC.md` (the contract), `DECISIONS.md` (append-only ADRs).

## The contract, mechanically enforced

- `SPEC.md` is the only source of work. Every acceptance criterion is one line
  in a grammar `spec_lint.py` parses:
  `- **AC-1** — <criterion> | check: ` `` `<command>` `` ` | status: next`
  (status: `next`, `built`, or `dropped`). An AC without a runnable check
  cannot be written — that is the product-selection constraint (only build
  what a machine can verify) turned into a parse error.
- Every `status: built` AC must have `ac_<n>` in a test name under `tests/` —
  claiming built without a pinning test is a lint failure, not a style issue.
- Zero dependencies by default. If `requirements.txt` gains a package, the
  lint fails unless `DECISIONS.md` names that package in an ADR.
- The gate runs at four moments, all deterministic: after every file edit
  (PostToolUse), before every commit (pre-commit), on every push (CI), and
  fresh at the ship gate (brief 144). Red blocks; nothing asks the agent's
  opinion.
- Edits to the harness layer are blocked at tool-call time (PreToolUse,
  exit 2). If the gate itself is wrong, the agent's move is to stop and
  report — the fix belongs to the operator.

## Instantiating (what 141 does)

```sh
cp -r template/ <product-path> && cd <product-path>
git init
git config core.hooksPath .githooks
sh scripts/check              # must be green on the pristine scaffold
sh scripts/check --prove-red  # must report PROVE-RED OK
git add -A && git commit -m "scaffold: <product> from goal-prompts template"
```

**Operator duties the agent cannot do:** create the GitHub repo and push;
make the `check` workflow a required status check (branch protection);
replace `@OPERATOR` in `.github/CODEOWNERS` with a real handle.

## The loop after scaffold

`142` writes `SPEC.md` (spec-lint-clean before it ends) → `143` implements,
one AC per verified commit, test first → `144` re-runs everything
adversarially and rules ship or hold → `29 · Weekly Vitals` and
`46/47 · Triage & Fixer` operate what shipped.

## Deviating

The stack default is Python 3 stdlib + `unittest` — chosen because zero
dependencies is the cheapest reliability money can't buy, and because the
parent repo proves the stack. A product may deviate (different language,
a framework) only by rewriting the harness layer to keep the same four
enforcement moments and recording the deviation as an ADR in `DECISIONS.md`.
The invariant is the contract above, not the language.
