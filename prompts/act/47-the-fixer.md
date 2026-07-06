---
id: "47"
title: The Fixer
family: Act
kind: action
question: shall we fix it?
output: FIXLOG.md
tagline: The one brief that changes code. Reads any audit report, asks which findings to implement, then fixes them safely — one commit each, re-checked.
---
# Goal: The Fixer

You are working inside this repo. Mission: turn an audit report into merged fixes — safely, one finding at a time, with the operator approving scope before anything changes.

This brief modifies code. Unlike every audit brief, it acts — but it never acts without explicit approval first, and it works in small reversible steps.

## Phase 1 — Load and understand the findings
- Ask which report to work from, or detect audit reports at repo root (BUGS.md, SECURITY.md, PERF.md, and the rest).
- Parse the findings: name, severity, location, proposed fix, effort. Restate them back compactly so the operator sees what you see.
- Confirm a clean working tree and note the current branch; if the tree is dirty, stop and say so.

## Phase 2 — Agree the scope (gate — do not skip)
- Present the findings as a numbered list with severity and effort.
- Ask the operator which to implement: all, a subset, or just the top N. **Wait for an answer. Change nothing until they choose.**
- For anything destructive, ambiguous, or architectural, flag that it needs a human decision and surface the options rather than guessing.

## Phase 3 — Implement, one finding per commit
Work on a dedicated branch (e.g. `fixer/<report>-<date>`). For each approved finding, in severity order:
1. Make the smallest change that resolves it; touch only what the finding names.
2. Run the relevant tests or checks; if the repo has a check script, run it.
3. Commit alone, message referencing the finding. One finding, one commit — so any single fix can be reverted cleanly.
4. If a fix balloons beyond its estimate or breaks something, stop, revert that change, and report — don't push through.

## Phase 4 — Log
Create `FIXLOG.md` at repo root:
1. **Session summary** — report worked from, branch name, findings approved vs deferred
2. **Changes** — per finding: what changed · files · commit · check result
3. **Deferred & blocked** — what wasn't done and why (needs decision, out of scope, risky)
4. **Verification** — how to confirm the fixes; what the operator should review before merge
5. **Suggested next** — re-run the source audit to confirm findings cleared

## Rules
- Never change code before the operator approves scope in Phase 2 — ask before acting
- One finding per commit; smallest viable change; stay inside what the finding names
- If a fix isn't clearly safe, defer it with options rather than guessing
- Leave the branch and FIXLOG for review — end by asking whether to open a PR or re-run the audit
