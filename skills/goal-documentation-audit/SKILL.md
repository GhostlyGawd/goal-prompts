---
name: goal-documentation-audit
description: "Follow the docs literally to find where they lie, then rank the gaps by who gets blocked — and which wrong docs to delete. Goal Prompt 16 · Clarity — inspects the current repo and writes DOCS.md at the repo root."
---

# Goal: Documentation Audit

You are working inside this repo. Mission: test the documentation against reality — follow it literally, find where it lies, find what's missing — and rank the gaps by who gets blocked.

Read-only pass. Your only write is the report file.

## Phase 1 — Inventory and audiences
- List everything that documents this project: README, docs folders, wikis referenced, inline comments, API docs, changelog.
- Name the audiences: new developer, end user, operator/deployer. Each doc serves one — or fails all.

## Phase 2 — Audit through 7 lenses
1. **README truth-test** — follow it step by step; record the first point of failure and every divergence
2. **Config coverage** — diff the env vars and flags the code reads against what any doc mentions
3. **API drift** — documented endpoints/params vs what routes actually accept and return
4. **Lying comments** — inline comments contradicting the code beside them (worse than no comment)
5. **The missing map** — could a new dev draw the architecture from docs alone? What's the biggest unexplained area?
6. **Dead ends** — broken links, references to removed files, stale screenshots
7. **Change history** — is there any way to learn what shipped recently and why?

## Phase 3 — Curate
- Rank by who's blocked and how hard: setup-blocking beats nice-to-know
- Mark docs to DELETE: wrong documentation is worse than none
- Every finding cites the doc location and the code that contradicts it

## Phase 4 — Report
Create `DOCS.md` at repo root:
1. **Truth-test log** — the README walk with divergences inline
2. **Fix-now list** — actively wrong docs: correct or delete, with effort
3. **Gap list** — missing docs ranked by blocked audience
4. **Proposed doc map** — what should exist, one line each, nothing aspirational
5. **The first doc to write** — outlined in 5 bullets

Start the report with today's date. If `DOCS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Test docs by following them, not by reading them
- Fewer, accurate docs beat many stale ones
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which docs to fix first
