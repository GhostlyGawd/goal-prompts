---
name: goal-compounding-value
description: "What grows the more it's used — history, saved work, personalization — and whether it's surfaced back as value or sits inert in a table nobody reads. Goal Prompt 155 · Craft — inspects the current repo and writes COMPOUNDING.md at the repo root."
---

# Goal: Compounding Value Audit

You are working inside this repo. Mission: find what makes the hundredth session worth more than the first. Sticky products compound — every use deposits something (history, refinements, artifacts, learned preferences) that makes the next use better, until leaving would mean abandoning something real. 78 audits the return trip's messaging and churn cliffs; this brief audits the *asset* that makes returning worth it.

Read-only pass. Read the data model, persistence, and personalization code; your only write is the report file.

## Phase 1 — Inventory the deposits
- List everything that accrues per user with use: history, saved work, templates, tags, settings refinements, connected integrations, learned behavior.
- For each, find where it's stored — and every surface where it's shown back or used on the user's behalf.
- Note what the product *could* accumulate from natural use but currently discards: searches, corrections, repeated patterns, drafts.

## Phase 2 — Audit through 7 lenses
Cite the store and surface for every finding.
1. **Deposits exist** — natural use leaves residue automatically; the product that forgets each session and makes every visit a first visit
2. **Value surfaced back** — accrued data working for the user: searchable history, suggestions from past behavior, "pick up where you left off" — versus rotting unread in a table
3. **Early investment invited** — the first sessions offer small acts of ownership (name it, pin it, save the view) that visibly improve the next session; investment asked before any value is delivered is the anti-pattern
4. **Time-to-irreplaceable** — how many sessions until this account is meaningfully better than a fresh one; what the tenth visit has that a new signup doesn't
5. **Compounding, not hoarding** — the asset stays valuable as it grows: old items resurface when relevant, scale is organized, not a landfill of stale entries
6. **Earned, not walled** — export and portability intact; stickiness from value the user would miss, never from data held hostage — lock-in found here is a defect, not a strategy
7. **The asset made visible** — the user can see what they've built ("124 notes, 8 templates, a year of history") stated as inventory, not wielded as guilt

## Phase 3 — Curate
- Rank by leverage: data already collected but never surfaced is the cheapest win; new accrual mechanics cost more.
- Separate "discarded" (start keeping), "inert" (surface it), and "invisible" (show the asset).
- For each, name the store, the surface it should reach, and what the user gains.

## Phase 4 — Report
Create `COMPOUNDING.md` at repo root:
1. **Asset inventory** — what accrues today: store · surfaced where · verdict (working / inert / discarded)
2. **Compounding findings** — each: lens · data · file · the mechanism to build
3. **Time-to-irreplaceable** — the session count today, and the changes that shorten it
4. **Portability check** — what's exportable, what isn't, and what that says

Start the report with today's date. If `COMPOUNDING.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every finding points at a real store or its absence — no speculative features unmoored from the data model
- Recommend accrual only from natural use; anything requiring extra user labor must pay back visibly in the same session
- No per-user persistence and no account model in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Before asking, present the top findings as a ranked list in plain words
- Report only — end by asking which buried asset to surface first
