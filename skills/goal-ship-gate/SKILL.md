---
name: goal-ship-gate
description: "The adversarial go/no-go. Re-runs every check fresh, sabotages code to prove the tests bite, walks the revenue path end to end, and rules ship or hold. Goal Prompt 144 · Build — inspects the current repo and writes SHIP-GATE.md at the repo root."
---

# Goal: Ship Gate

You are working inside this repo — a product repo built against `SPEC.md`. Mission: the adversarial go/no-go before real users or money — verify by running, never by reading, and rule ship or hold.

Read-only pass: every experiment below is reverted before this brief ends. Your only lasting write is the report file.

## Phase 1 — Load the contract
- Read `SPEC.md` (the bars), `BUILDLOG.md` (the claims), `DECISIONS.md` (the promises).
- Note every AC claiming `status: built` — those claims are on trial.

## Phase 2 — Verify through 6 lenses
1. **The gate itself** — run `scripts/check` fresh, then `scripts/check --prove-red`; a gate that cannot go red proves nothing
2. **AC truth** — run every built AC's `check:` command verbatim; produce a pass/fail table, no paraphrase
3. **Test honesty** — pick 3 built ACs, deliberately break each behavior (revert after), and confirm its test goes red; a test that survives sabotage asserts nothing
4. **Harness integrity** — diff the harness layer (`scripts/`, `.githooks/`, `.github/`, `.claude/`, `tests/harness/`) against the goal-prompts template; any drift is a finding, whoever made it
5. **Eval floor** — run `python3 evals/run.py`; scores against the spec's numeric floor
6. **The first dollar** — walk the spec's revenue path end to end: can a stranger actually pay today, and does the money arrive somewhere the operator controls?

## Phase 3 — Rule
- The bars come from `SPEC.md` and were written before this run; never adjust them to fit the results.
- Any hard fail — a red AC, a sabotage-proof test, harness drift, a broken payment path — is a hold, named after its blocker. No averaging.

## Phase 4 — Report
Create `SHIP-GATE.md` at repo root:
1. **Scorecard** — lens · result · evidence, as command-output tails
2. **The ruling** — ship or hold, in one plain paragraph
3. **Blockers** — if hold: finding · which brief fixes it (143 for unmet ACs, 142 for spec gaps, 47 for report findings)
4. **Watch after ship** — the kill criteria from `SPEC.md`, restated as the first Weekly Vitals (29) checklist

Start the report with today's date. If `SHIP-GATE.md` already exists from a previous run, read it first and lead with what changed — especially blockers that were open and are now closed.

## Rules
- Verify by executing; a gate that trusts reports is not a gate
- Sabotage is always reverted: `git status` must be clean when this brief ends
- No `SPEC.md`, or no implementation to judge at this root? Say so in a one-paragraph null report and stop.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking whether to ship, or which blocker to send back first
