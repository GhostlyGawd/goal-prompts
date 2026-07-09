# CLAUDE.md — working in this product repo

This repo was instantiated from the goal-prompts golden-path template. The
harness layer is operator-owned; you build the product inside it. README.md
carries the full contract — this file is the working summary.

## The one command

```sh
sh scripts/check
```

Spec lint → tests → evals. Run it before every commit; the pre-commit hook,
the PostToolUse hook, and CI all run the same thing, so passing here means
passing everywhere.

## The rules that are enforced (don't fight them)

- **SPEC.md is the only source of work.** Implement acceptance criteria
  (`AC-n`); nothing else gets built. An AC you can't test as written is a
  spec question, not a license to improvise.
- **Test first.** Every AC lands as a failing test named `test_ac_<n>_...`,
  then the least code that passes, then one commit: `feat(AC-n): <criterion>`.
  Mark the AC `status: built` in the same commit — the lint checks the test
  exists.
- **Never edit the harness layer:** `scripts/`, `.githooks/`, `.github/`,
  `.claude/`, `tests/harness/`. A PreToolUse hook blocks these edits. If the
  gate seems wrong, stop and tell the operator; do not route around it.
- **Never weaken a test to get green.** Deleting or loosening a failing test
  is the one failure mode the hooks cannot catch — it is also the one the
  ship gate (brief 144) sabotage-checks for. Fix the code or revert.
- **Red blocks.** After any edit the gate runs; on red, fix or revert before
  anything else. Never commit on red.
- **Dependencies need an ADR.** stdlib only unless DECISIONS.md names the
  package — the lint greps for it.
- **DECISIONS.md is append-only.** New choice, new ADR; never rewrite one.

## Layout

- `src/` — product code (yours)
- `tests/` — product tests (yours); `tests/harness/` is not yours
- `evals/cases/*.json` — golden cases run by `evals/run.py`
- `SPEC.md` — the contract (written by brief 142, revised only through it)
- `DECISIONS.md` — the ADR log
