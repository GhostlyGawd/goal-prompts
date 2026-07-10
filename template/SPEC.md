# SPEC — (product name; brief 142 fills this file)

Date: (spec date)

## Job

(One sentence a buyer would recognize: the single job this product does.)

## Non-goals

- (What v1 refuses to do. Scope creep dies here, in writing.)

## Acceptance criteria

Grammar (parsed by `scripts/spec_lint.py` — one line per AC):
`- **AC-n** — <criterion> | check: ` `` `<command>` `` ` | status: next|built|dropped`

- **AC-1** — the scaffold answers a health check | check: `python3 -m unittest tests.test_smoke -v` | status: built

## Interfaces

(Inputs, outputs, schemas, error shapes — exact enough to test against.)

## Evals

(For judgment-shaped output: the golden cases in `evals/cases/` and the
numeric floor. The scaffold ships one example case.)

- floor: all cases pass

## Dependencies

- none — stdlib only. Adding a package requires an ADR in DECISIONS.md
  naming it; `scripts/spec_lint.py` enforces this.

## Kill criteria

- (The measurable tripwires that mean stop building — brief 144 restates
  these as the first Weekly Vitals checklist.)
