---
description: "A fast weekly vitals pass — tests, build, deps, TODOs — diffed against the last run so drift shows up as trend arrows."
---

# Goal: Recurring Health Check

You are working inside this repo. Mission: run a fast vitals pass — minutes, not an afternoon — and diff it against the last run so drift shows up as trend arrows, not surprises. Designed to re-run weekly.

Read-only checks. Your only write is the report file.

## Phase 1 — Load the baseline
- Look for an existing HEALTH.md at the repo root and in `reports/`. If present, parse the previous scorecard and history table for diffing.
- If absent, this run establishes the baseline; say so.

## Phase 2 — Take the vitals
Collect quickly, mostly via commands; skip gracefully what doesn't apply:
1. **Tests** — pass/fail · count · runtime
2. **Build** — succeeds? · time · bundle/artifact size
3. **Dependencies** — vulnerability count (audit) · outdated count
4. **Static health** — lint errors · type errors
5. **Code load** — TODO/FIXME count · total LOC · file count
6. **Momentum** — commits since last check · most-churned files this period

## Phase 3 — Diff and judge
- Trend arrow per vital: better / same / worse vs last run.
- Flag regressions loudly — a vital that got worse is the headline.
- One-line interpretation per flagged item: what likely caused it (check recent commits).

## Phase 4 — Report
Overwrite `HEALTH.md` at repo root (append to history, replace the rest):
1. **Scorecard** — vital · value · trend arrow · note
2. **Regressions** — what got worse, the likely cause, the suggested response
3. **Three actions** — the most valuable things to do before next check
4. **History table** — one dated row per run, appended; never edit old rows

Start the report with today's date. If `HEALTH.md` already exists, the baseline parsed in Phase 1 is the diff target — lead with what changed since.

## Rules
- Speed is a feature: minutes, or it won't get re-run
- Numbers over prose; the format must stay stable so diffs stay meaningful
- Same vitals every run — consistency is what makes trends real
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking whether to act on the regressions
