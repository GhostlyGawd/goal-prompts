---
name: goal-release-pipeline-audit
description: "Map merged-PR to production; every manual step is a finding. Includes the rollback-readiness verdict. Audit brief 23 · Ops — runs a four-phase audit of the current repo and writes RELEASE.md at the repo root."
---

# Goal: Release Pipeline Audit

You are working inside this repo. Mission: map the full path from merged PR to production, treat every manual step as a finding, and deliver a verdict on rollback readiness.

Read-only pass: inspect CI configs, deploy scripts, docs. Your only write is the report file.

## Phase 1 — Map the pipeline
- Trace the actual path: merge → build → test → deploy → verify. From configs and scripts, not from memory or docs.
- Time each stage where measurable; note which steps are automated vs human-driven.
- Who can deploy, from where, and what does a deploy require?

## Phase 2 — Audit through 7 lenses
1. **CI health** — duration, flaky steps, and the checks NOT run (types, lint, security scans, size budgets)
2. **Manual steps** — every human action between merge and production: each is latency, error surface, and a bus-factor risk
3. **Rollback path** — does one exist; has it ever been exercised; are data migrations reversible or one-way doors?
4. **Environment parity** — differences between local/staging/prod that produce works-on-my-machine failures
5. **Migration safety** — how schema changes deploy relative to code; the window where they can disagree
6. **Flag hygiene** — feature flags: kill switches for risky changes, and stale flags rotting in the code
7. **Release visibility** — can anyone tell what shipped, when, and what changed? Changelog, tags, deploy log

## Phase 3 — Curate
- Rank by deploy-confidence gained per unit effort
- Every finding cites the config, script, or absence thereof

## Phase 4 — Report
Create `RELEASE.md` at repo root:
1. **Pipeline map** — stage · time · automated? · risk noted
2. **Rollback verdict** — ready / partial / one-way, with evidence
3. **Findings** — each: issue · risk · fix · effort
4. **The one automation** — the single step to automate first and its payoff
5. **Deploy checklist** — interim, until automation lands

Start the report with today's date. If `RELEASE.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Judge the pipeline that exists, not the one described in docs
- Boring, frequent, reversible deploys are the goal
- No release pipeline in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fixes to make
