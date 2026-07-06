---
id: "14"
title: New-Dev Onboarding Audit
family: Team
question: can others build on it?
output: DX.md
tagline: Walk clone → install → run → change → PR like a brand-new developer and log every stumble on the way to a first contribution.
---
# Goal: New-Dev Onboarding Audit

You are working inside this repo. Mission: experience this repo as a brand-new developer would — clone, install, run, make a change, open a PR — and log every stumble between them and a first contribution.

Read-only toward the codebase; you may exercise setup steps in a sandbox. Your only write is the report file.

## Phase 1 — Walk the path literally
Follow the README exactly as written, noting where reality diverges:
- Clone → install: missing prerequisites, undocumented versions, failing steps
- Configure: env vars and secrets — where does a new dev get them; is there an example file?
- Run: does the app start; is there seed data or an empty shell?
- Verify: do the tests pass out of the box?

## Phase 2 — Audit through 7 lenses
1. **Docs vs reality** — every README step that fails, lies, or assumes tribal knowledge
2. **Secrets bootstrap** — the path from zero to working config; blockers requiring another human
3. **Seed data** — can a new dev see the product working, or a blank screen?
4. **Loop speed** — edit → see result: how many seconds; test cycle time
5. **Error quality** — when setup is wrong, do errors say what to do next?
6. **Contribution path** — branch conventions, CI feedback time, review expectations: written anywhere?
7. **Tribal knowledge** — decisions and gotchas that live only in someone's head; list what you had to infer

## Phase 3 — Curate
- Rank friction by where it lands: earlier stumbles cost every future hire
- Every finding: exact step, what happened, what should happen

## Phase 4 — Report
Create `DX.md` at repo root:
1. **Time-to-first-PR estimate** — today, honestly, with the breakdown
2. **Stumble log** — the walk, step by step, with findings inline
3. **Fixes** — each: what · file to change · effort; ordered by stage
4. **The one-hour fix** — the single improvement that saves the most time for every future developer

## Rules
- Report what actually happened when steps were followed, not what docs claim
- A setup script beats a setup document
- Report only — end by asking which fixes to make
