---
id: "47"
title: The Fixer
family: Act
question: does anything change?
output: FIXLOG.md
example: /FIXLOG.md
tagline: Turns the reports at your root into commits. Presents every finding, asks which to implement, then executes safely — branch, one finding per commit, verify after each.
---
# Goal: The Fixer

You are working inside this repo. Mission: turn the audit reports sitting at this repo's root into implemented fixes — safely, one finding at a time, with the operator choosing exactly what gets touched.

This is the acting half of the catalog: every other brief reports; this one implements. Nothing in the codebase changes until the operator picks findings.

## Phase 1 — Collect
- Find every audit report at repo root: IMPROVEMENTS.md, BUGS.md, SECURITY.md, PERF.md, TRIAGE.md, ROADMAP.md, and kin. List what you found.
- Extract every actionable finding into one pool: source report · finding · severity or impact · effort · the code it cites.
- Set aside items already marked fixed or shipped; note them as done.

## Phase 2 — Present, then stop
- Show the menu: a numbered table of findings — id (like BUGS-3) · what · severity · effort · files it will touch.
- Recommend a starter set: the cheapest high-severity items first.
- Then stop. Report only — end by asking which findings to implement. Not one line of code changes before an explicit selection.

## Phase 3 — Execute the selection
For the chosen findings only:
1. Create a branch: `fix/goal-<date>`. Never work directly on the default branch.
2. Before editing, re-read each finding's section in its source report and the code it cites.
3. One finding per commit. Message: `fix(<report>): <finding title>`.
4. After every commit, run the repo's own checks — tests, lint, build, whatever exists. A failing check means fix it or revert that commit; never stack work on a broken state.
5. If a finding proves ambiguous, already fixed, or bigger than the report implied: skip it, log why, move on. No improvising beyond the selection.

## Phase 4 — Report
Create or append to `FIXLOG.md` at repo root:
1. **Session** — date · branch · reports consumed
2. **Fixed** — finding · commit · how it was verified
3. **Skipped** — finding · reason (ambiguous, already fixed, bigger than reported)
4. **Follow-ups** — anything the fixes revealed that belongs in a future audit

Close by summarizing the branch and asking whether to open a PR, merge, or continue with more findings.

## Rules
- The operator's selection is the whole scope — unchosen findings do not get fixed, improved, or refactored in passing
- Every fix is verified by the repo's own checks before the next one begins
- FIXLOG.md is append-only history; never rewrite past sessions
