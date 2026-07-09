---
description: "The edit to build to test to see-it-work cycle, timed — and the daily friction that taxes every change the team makes."
---

# Goal: Inner-Loop Speed Audit

You are working inside this repo. Mission: measure the developer inner loop — the edit → build → test → see-the-result cycle — and find the friction that taxes every single change, because a slow loop is a tax paid a hundred times a day.

Read-only pass. Run the setup, build, and tests; time the loop; read the tooling config. Change nothing but the report file.

## Phase 1 — Time the loop
- Go from clone to a running app; record every step and how long it takes.
- Make a trivial change and measure the time to see it reflected.
- Run one test, then the whole suite; note both times and whether you can run just the relevant test.

## Phase 2 — Audit through 7 lenses
1. **Cold start** — steps and time from clone to running; undocumented manual setup
2. **Edit-to-feedback** — hot reload versus full restart; how long to see a change
3. **Test loop** — time for one test versus the suite; can you target just the affected tests
4. **Build times** — incremental versus full; caching; what forces a full rebuild
5. **Local realism** — how faithfully local mirrors prod; flaky services, missing seed data
6. **Daily friction** — the manual steps, env fiddling, and rituals repeated every day
7. **Toolchain feedback** — lint/typecheck/format speed and whether they run in-editor or only in CI

## Phase 3 — Curate
- Rank by frequency × delay: a 30-second reload hit all day dwarfs a slow but rare full build.
- Separate one-time setup pain from per-change pain; the second compounds.
- For each, name the concrete fix — a cache, a watch mode, a seed script, a doc.

## Phase 4 — Report
Create `INNERLOOP.md` at repo root:
1. **The loop, timed** — each step from edit to feedback, with its duration
2. **Friction ranked** — by daily cost, each with what a developer endures
3. **Fixes** — each: friction · fix · time saved per day · effort
4. **Target loop** — what the cycle should feel like, and the two changes that get closest

Start the report with today's date. If `INNERLOOP.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Rank by daily cost, not one-time pain
- A fast loop is a feature; measure it in seconds, not vibes
- No build or test loop in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which friction to remove first
