---
description: "The flagship. Understand the whole product, then surface prioritized opportunities across UI, UX, retention, engagement, community, and beauty."
---

# Goal: Product Improvement Discovery

You are working inside this repo. Mission: deeply understand this product, then surface a grounded, prioritized set of opportunities — new features, fixes, synergies, updates, iterations, improvements — across every surface: UI, UX, friendliness, helpfulness, community, retention, engagement, performance, beauty.

Discovery only, not implementation. Read anything, run read-only checks (tests, dev server, linters), but don't modify code. Your only write is the report file.

## Phase 1 — Understand the product
Explore until you can answer from evidence, not guesses:
- What is this product, who is it for, what core job does it do?
- Current journey: entry → first value → habit → sharing/return?
- What existing infrastructure, data, or half-built features are underused?

Check: README/docs, package manifest, routes/screens, key components, API endpoints, schema, feature flags, analytics events, error handling, TODO/FIXME comments, recent git log. Getting the product wrong makes everything downstream wrong.

## Phase 2 — Audit through 12 lenses
Find concrete evidence in code for each — never hypotheticals.
1. **UI & beauty** — hierarchy; spacing/type/color consistency; hover/focus states; motion; dark mode; polish
2. **UX & flows** — steps to core value; dead ends; confusing nav; missing undo/confirmations
3. **Onboarding** — empty states, sample data, guided first action, time-to-first-value
4. **Friendliness** — microcopy clarity, jargon, error messages that say what to do next, accessibility
5. **Helpfulness** — smart defaults, suggestions, autofill, anticipating needs
6. **Feedback & state** — loading/skeletons, optimistic updates, success confirmation, graceful failure
7. **Retention** — reasons to return: saved progress, history, streaks, digests, resurfacing past value
8. **Engagement** — core-loop depth, personalization, progression, delight
9. **Community** — sharing, collaboration, invites, comments, profiles, viral loops
10. **Synergies** — existing features/data that combine into more than their parts; often the cheapest big wins
11. **Fixes & felt debt** — likely bugs, TODOs, dead code, perf drags, anything eroding trust
12. **Reach** — mobile responsiveness, offline, i18n, shareable links/SEO, PWA

## Phase 3 — Generate wide, curate hard
- 20–30 raw ideas → cut to the strongest 10–15
- Kill anything generic enough to fit any app
- Every survivor cites repo evidence (paths, components, patterns)
- Tag each: **FIX** (broken today) / **IMPROVE** (works, could be better) / **NEW** (doesn't exist)

## Phase 4 — Report
Create `IMPROVEMENTS.md` at repo root:
1. **Product snapshot** — what, who, journey (5–8 sentences)
2. **Opportunity map** — impact × effort table
3. **Top 5 quick wins** (~a day each) + **Top 3 big bets**
4. **Full list** — each: Name · Tag+lens · Evidence · Proposal · Why it matters · Effort S/M/L · Impact L/M/H · Risks
5. **Sequence** — if only 3 ship first, which and why

Start the report with today's date. If `IMPROVEMENTS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- No evidence, no idea
- Prefer removing friction over adding features; synergies over net-new complexity
- Think PM + designer + engineer at once: desirable, usable, feasible
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking me which items to build
