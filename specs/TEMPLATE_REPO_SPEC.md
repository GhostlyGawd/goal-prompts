# TEMPLATE_REPO_SPEC — the golden-path template

2026-07-09 · Status: **built this session** — Phase 4 selected the template
repo (with its hook layer and spec linter) as the keystone, so per the
mission's deliverable rule the spec lives with the artifact:

**→ The authoritative spec is [`template/README.md`](../template/README.md),
which ships inside every instantiated product repo so the rules travel with
the code.**

This stub records what the spec covers and how the template was verified,
so specs/ stays a complete index.

## What template/README.md specifies

- The enforcement hierarchy as the design rule (exit codes > scripts > prose).
- The two layers: harness (operator-owned, hook-blocked: `scripts/`,
  `.githooks/`, `.github/`, `.claude/`, `tests/harness/`) vs product
  (`src/`, product `tests/`, `evals/cases/`, SPEC.md, DECISIONS.md).
- The gate: `scripts/check` = spec lint → unittest → evals;
  `--prove-red` plants a canary and asserts the gate can fail.
- The four deterministic enforcement moments: PostToolUse (every edit),
  pre-commit (every commit), CI (every push), brief 144 (ship gate) — plus
  the PreToolUse block on harness edits.
- The mechanically-enforced contract: AC grammar, built-needs-test,
  dependency-needs-ADR, zero deps by default.
- Instantiation steps (what brief 141 runs) and the operator-only duties
  (GitHub repo, required status check, CODEOWNERS handle).
- The deviation rule: different stack = rewrite the harness layer keeping
  the same enforcement moments + an ADR (DECISIONS.md ADR-4).

## Verification performed this session (hermetic, in a scratch copy)

| Claim | Proof |
|---|---|
| Pristine scaffold is green | `sh scripts/check` → ALL CHECKS PASSED (13 harness tests + smoke test + eval case) |
| The gate can fail | `sh scripts/check --prove-red` → PROVE-RED OK |
| Red commits cannot land | broke `src/product.py`, `git commit` → pre-commit hook rejected it |
| Post-edit hook blocks on red | `scripts/hook-check` exit 0 green, exit 2 red (measured) |
| Harness edits are blocked | `scripts/hook-protect` exit 2 for all five harness paths, exit 0 for product paths (tested via subprocess in tests/harness/) |
| The spec linter is honest | 7 lint tests: good spec passes; missing section, malformed AC, built-without-test, dependency-without-ADR all fail |
