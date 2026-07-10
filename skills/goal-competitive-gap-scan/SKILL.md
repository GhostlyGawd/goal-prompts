---
name: goal-competitive-gap-scan
description: "Research real rivals on the web, then split the gaps: table stakes you must match vs differentiation bets only you can make. Audit brief 10 · Growth — runs a four-phase audit of the current repo and writes COMPETITIVE.md at the repo root."
---

# Goal: Competitive Gap Scan

You are working inside this repo. Mission: place this product against its real competitors — research them on the web — and split the findings into table stakes to match and differentiation bets to make.

Read the repo, search the web. Your only write is the report file.

## Phase 1 — Define the arena
- From the code and copy: what category is this product in, and for whom, specifically?
- Search the web and pick 3–5 real competitors a prospective user would actually compare.
- For each: skim their site, pricing, onboarding flow, changelog, and user reviews.

## Phase 2 — Compare through 6 lenses
1. **Table stakes we lack** — features every rival has that users assume exist
2. **Their patterns worth learning** — onboarding, empty states, pricing pages that clearly work
3. **Pricing & packaging norms** — how the market slices tiers; where this product sits
4. **Underleveraged strengths** — things this repo already does that rivals don't; are they even surfaced?
5. **Positioning gaps** — the words rivals own vs the words this product could own
6. **Their users' complaints** — review-mining: recurring rival pain points are openings

## Phase 3 — Curate
- Stakes vs bets: match the market minimum, differentiate everywhere else
- Every gap names the competitor and the evidence (page, review, doc)
- Flag what NOT to copy — features that fit their strategy, not this one

## Phase 4 — Report
Create `COMPETITIVE.md` at repo root:
1. **Arena summary** — category, audience, the 3–5 rivals and one line on each
2. **Comparison table** — capability · us · each rival
3. **Table stakes list** — ranked by user expectation, with effort
4. **Differentiation bets** — 3 moves that exploit rival weaknesses using existing strengths
5. **Do-not-copy list** — with reasons

Start the report with today's date. If `COMPETITIVE.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Evidence from the web, cited; no imagined competitor features
- Differentiation must trace to something real in this repo
- No identifiable product to compare in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which moves to make
