---
id: "13"
title: Tech Debt Map
family: Team
question: can others build on it?
output: DEBT.md
tagline: Duplication, tangles, and dead patterns — mapped as interest paid vs principal owed, with a refactor sequence that pays for itself.
---
# Goal: Tech Debt Map

You are working inside this repo. Mission: map the technical debt as an economist would — what interest is being paid today, what the principal costs to retire — and produce a refactor sequence where every step pays for itself.

Read-only pass. Your only write is the report file.

## Phase 1 — Find where debt concentrates
- Cross churn with complexity: which files are both large and frequently edited? (use git log)
- Census the TODO/FIXME/HACK comments: count, age, clusters.
- Where do new features take longest to add? Trace one recent feature's diff to see what it had to touch.

## Phase 2 — Audit through 8 lenses
1. **Duplication clusters** — the same logic living in 3 places, drifting apart
2. **God files & modules** — everything-magnets that every change touches
3. **Tangles** — import cycles, layers reaching around each other
4. **Pattern inconsistency** — three ways to fetch, two ways to handle errors; every choice a new dev must relearn
5. **Dead weight** — code kept "just in case", vestigial abstractions
6. **Outdated idioms** — patterns the ecosystem has moved past, blocking upgrades
7. **Test-hostile design** — code that can't be tested without mocking the world
8. **Historic hotspots** — files that keep appearing in bug-fix commits

## Phase 3 — Curate
- Every item states its **interest**: how it hurts today (slower features, recurring bugs, onboarding cost)
- And its **principal**: realistic cost to fix
- Explicitly list debt to ACCEPT — real debt not worth paying down; write down why

## Phase 4 — Report
Create `DEBT.md` at repo root:
1. **Debt inventory** — each: item · interest paid · principal · evidence (paths, churn numbers)
2. **Refactor sequence** — ordered steps, each safe, independently shippable, and justified by what it unlocks next
3. **Accepted debt register** — with reasons; revisit dates optional
4. **The first refactor** — scoped fully, with a safety plan (tests to add first)

Start the report with today's date. If `DEBT.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- No refactor without a payoff story: what gets faster, safer, or simpler after
- Sequence so each step de-risks the next
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which refactor to start
