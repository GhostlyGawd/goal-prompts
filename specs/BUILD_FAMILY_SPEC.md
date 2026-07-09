# BUILD_FAMILY_SPEC — the construction briefs

2026-07-09 · Status: **implemented this session** (prompts/build/, all gates
green). This spec records the design so future changes are judged against
intent, not memory. Design rationale: DECISIONS.md ADR-3.

## Family

- Name: **Build** · question: **will it ship?** · color `#8CD94C` · icon `i-build`
- Position in FAMILY_ORDER: after Act — the catalog reads audit → act → build.
- The family conductor `raw/family-build.md` is auto-generated in id order,
  which is execution order — it IS the build pipeline (no extra artifact).

## The brief list

| id | title | output | writes code? | gate placement |
|---|---|---|---|---|
| 141 | Scaffold the Rails | SCAFFOLD.md | yes — installs the harness into this repo (greenfield or graft) | end of Phase 2 (Fixer pattern) |
| 142 | Spec the Product | SPEC.md | no — its report *is* the spec | classic (end, in Rules) |
| 143 | Implement to Spec | BUILDLOG.md | yes — the AC loop | end of Phase 2 (Fixer pattern) |
| 144 | Ship Gate | SHIP-GATE.md | no — read-only, sabotage reverted | classic (end, in Rules) |

Execution order is id order: scaffold → spec → implement → gate. Scaffold
precedes spec so SPEC.md is written *inside* the rails, where
`scripts/spec_lint.py` gates it the moment it exists (ADR-3).

## Phase structure (shared skeleton, per house rules)

All four keep the linted 4-phase skeleton. The family's re-interpretation:
Phase 1 = load the contract (verdict / spec / log), Phase 2 = the lenses +
(for write-briefs) the scope gate, Phase 3 = the loop (instantiate / harden /
build / rule), Phase 4 = the report.

## Hard gates the briefs lean on (enforced outside the prose)

1. **Instantiation proof** — 141 must run `scripts/check` (green) *and*
   `scripts/check --prove-red` (gate can fail) and paste both tails. A
   scaffold whose gate cannot go red is rejected by instruction, and 144
   re-checks it by execution.
2. **Spec format** — 142 cannot end until `spec_lint.py` passes: required
   sections, the AC grammar (`- **AC-n** — <criterion> | check:
   `command` | status: next|built|dropped`), unique ids, ≥1 live AC.
3. **Built means test-pinned** — `status: built` without an `ac_<n>` test in
   `tests/` is a lint failure, so 143's claims are checkable.
4. **Dependency = ADR** — a requirements.txt line with no DECISIONS.md entry
   naming the package fails the gate.
5. **Harness immutability** — 143's loop runs with the PreToolUse hook
   blocking `scripts/`, `.githooks/`, `.github/`, `.claude/`,
   `tests/harness/`; the brief's "never edit the harness" rule is narration
   of a block, not a request.
6. **Every-edit / every-commit / every-push** — PostToolUse hook, pre-commit
   hook, CI: 143 cannot leave red states behind even if it wanted to.

## The SPEC.md convention

- Lives at the product repo root, written only through 142 (first write or
  revision), ratified by the operator at 142's ask-first gate.
- AC ids are permanent: never renumbered, retired with `status: dropped` —
  because 143's commits (`feat(AC-n): …`) and test names (`test_ac_<n>_…`)
  cite them.
- Briefs *reference* SPEC.md rather than embed specs, which is what keeps
  all four bodies under the 4,000-char gate (current: 3.0–3.7k with front
  matter).
- Sections (mirrored by the template skeleton and required by the lint):
  Job · Non-goals · Acceptance criteria · Interfaces · Evals · Dependencies
  · Kill criteria.

## Null-report behavior (the family's own routing)

Each brief's null report doubles as sequencing enforcement: 142/143 stop
with a null report when there is no scaffold/spec ("run 141 first"), 144
when there is nothing to judge, 141 when there is no verdict and no
operator ask to put the repo on rails. Running a Build brief out of order
degrades to a pointer at the right one.

## Non-goals for this family

- No CI/deploy briefs (Ops family owns that: 23, 137).
- No refactor/cleanup briefs (Act and Subtract own that: 47, 26, 27).
- No growth work on the shipped product (Growth family, after shipping).
- Never run against goal-prompts itself (no spec_lint here → null report).
