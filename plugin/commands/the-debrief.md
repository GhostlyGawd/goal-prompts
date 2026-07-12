---
description: "The milestone-boundary review — what was agreed, what landed, and a verdict on every piece: keep, finish, formalize, or revert — logged so decided stays decided."
---

# Goal: The Debrief

You are working inside this repo. Mission: review one increment of work — a branch, a milestone, everything since the last debrief — against what was agreed before it started, and rule on every change that landed. The review humans skip when tired is where drift compounds; this brief is that review, on rails.

Read-only pass. Your only write is the report file.

## Phase 1 — Fix the mandate and the window
- The mandate: what was agreed before this work began — the charter's Now list, a spec's acceptance criteria, an issue list, or the operator's written ask. Quote it verbatim. If nothing was written down, that is the first finding, not a license to invent one.
- The window: a git range — since the last `DEBRIEF.md` entry, a branch, a tag pair, or dates the operator names.
- What landed: every commit in the window, grouped into changes by surface; note which arrived with tests.

## Phase 2 — Audit through 6 lenses
1. **Mandate fit** — changes that trace to the agreed scope, each matched to its mandate line
2. **Stowaways** — landed but never asked for: drive-by features, gold-plating, while-I-was-in-there work
3. **Shortfall** — asked for but missing, or landed without its acceptance met; name which done claim fails
4. **Silent re-scopes** — the mandate itself edited inside the window: moved goalposts, softened criteria, reworded asks
5. **Debt taken** — shortcuts that borrowed from later: skipped tests, new TODOs, dependencies added without a recorded decision
6. **Verification honesty** — for each done claim, was it proven by a command or asserted by prose? Spot-run the checks for the three biggest.

## Phase 3 — Rule
- One verdict per change: **keep** (fit and verified), **finish** (back on Now, with its gap named), **formalize** (a good stowaway — amend the charter or spec first), or **revert** (hand to 47).
- No averaging: an increment with stowaways and shortfall is not mostly done — it is two lists, ruled separately.

## Phase 4 — Report
Create `DEBRIEF.md` at repo root:
1. **The mandate** — quoted, with its source
2. **The ledger** — change · asked for? · verified? · verdict; one bold-titled finding per non-keep
3. **Verdicts to execute** — the revert and finish lists, findings-shaped so 47 can take them to commits
4. **Debrief history** — one dated row per run, appended; never edit old rows

Start the report with today's date. If `DEBRIEF.md` already exists from a previous run, read it first, append to its history, and lead with whether the last debrief's verdicts were actually executed — a ruling nobody enforced is this run's first finding.

## Rules
- Judge against the mandate as it stood when the window opened — later edits to it are lens-4 evidence, not the bar
- An empty window — no commits since the last debrief? Say so in a one-paragraph null report and stop; there is nothing to review.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which verdicts to execute, and whether to fold the formalize list into the charter (149)
