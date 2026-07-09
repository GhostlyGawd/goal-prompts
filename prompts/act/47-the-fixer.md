---
id: "47"
title: The Fixer
family: Act
question: does anything change?
output: FIXLOG.md
example: /FIXLOG.md
related: 46 28
tagline: Turns your root reports into commits. Asks the scope — all, high-priority, or its pick — then builds them in dependency order, one verified commit each.
---
# Goal: The Fixer

You are working inside this repo. Mission: turn the audit reports sitting at this repo's root into implemented fixes — safely, in dependency order, one finding at a time, with the operator choosing how much to take on.

This is the acting half of the catalog: every other brief reports; this one implements. Nothing in the codebase changes until the operator picks a scope.

## Phase 1 — Collect
- Find every audit report at the repo root and in `reports/`: IMPROVEMENTS.md, BUGS.md, SECURITY-AUDIT.md, PERF.md, TRIAGE.md, ROADMAP.md, and kin. List what you found.
- Extract every actionable finding into one pool: source report · finding · severity or impact · effort · the code it cites.
- Set aside items already marked fixed or shipped; note them as done.

## Phase 2 — Present, then ask the scope
- Show the menu: a numbered table of findings — id (like BUGS-3) · what · severity · effort · files it will touch.
- Map dependencies: which findings must land before others — a schema before the code that uses it, a rename before its callers, a shared util before its consumers.
- Then stop and ask how much to take on. Report only — end by asking which scope to run:
  - **Everything** — every finding, sequenced into a dependency-ordered plan and built in that order
  - **High-priority only** — the high-severity or high-leverage findings; the rest deferred to a later pass
  - **The Fixer's pick** — you propose a sensible starter set (cheapest high-severity first) and say why
  - **A set I name** — the operator hand-picks findings by id
- Recommend one, but change nothing until the operator answers.

## Phase 3 — Plan, then execute
1. Write the build order for the chosen scope: merge duplicates, sequence by dependency (foundations before dependents), then by severity within each tier. Show this plan before touching code.
2. Create a branch: `fix/goal-<date>`. Never work directly on the default branch.
3. Before editing each finding, re-read its section in the source report and the code it cites.
4. One finding per commit, in plan order. Message: `fix(<report>): <finding title>`.
5. After every commit, run the repo's own checks — tests, lint, build, whatever exists. A failing check means fix it or revert that commit; never stack work on a broken state.
6. If a finding proves ambiguous, already fixed, or bigger than the report implied: skip it, log why, keep going. No improvising beyond the agreed scope.

## Phase 4 — Report
Create or append to `FIXLOG.md` at repo root:
1. **Session** — date · branch · reports consumed · scope chosen
2. **Build plan** — the dependency-ordered sequence that was executed
3. **Fixed** — finding · commit · how it was verified
4. **Skipped** — finding · reason (ambiguous, already fixed, bigger than reported)
5. **Follow-ups** — anything the fixes revealed that belongs in a future audit

Close by summarizing the branch and asking whether to open a PR, merge, or run the deferred findings next.

## Rules
- The agreed scope is the whole job — findings outside it don't get fixed, improved, or refactored in passing
- Build in dependency order: nothing lands before the finding it depends on
- Every fix is verified by the repo's own checks before the next one begins
- FIXLOG.md is append-only history; never rewrite past sessions
- If a `reports/` directory exists at the repo root, `FIXLOG.md` lives there instead of the root.
