---
id: "108"
title: Account Lifecycle Audit
family: Product
question: what could this be?
output: LIFECYCLE.md
tagline: The whole arc of an account beyond signup — settings, export, plan changes, and deletion — and whether the product treats users with dignity, even leaving.
---
# Goal: Account Lifecycle Audit

You are working inside this repo. Mission: judge the account arc after signup — managing it, changing plans, exporting data, and leaving — and whether the product respects the user at every stage, including the exit. How a product handles leaving is how it earns being recommended.

Read-only pass. Trace the account, billing, and deletion flows; change nothing but the report file.

## Phase 1 — Walk the arc
- Map the stages: settings, plan changes, data export, deletion, dormancy, and return.
- For each, find the path a user takes and whether it is self-serve.
- Note where a step requires contacting support that shouldn't.

## Phase 2 — Audit through 7 lenses
Cite the flow or screen for every finding.
1. **Settings & control** — can users find and change what governs their account; sane defaults
2. **Data export** — can a user get their data out, in a usable form, without support
3. **Plan & billing changes** — upgrade, downgrade, cancel: clear, self-serve, no traps
4. **Account deletion** — a real delete path, what it removes, and honest handling of retained data
5. **Offboarding dignity** — cancellation without hostage-taking; a graceful, respectful exit
6. **Reactivation** — coming back: is data preserved and return easy
7. **Lifecycle edges** — dormant accounts, seat changes, ownership transfer, team departure

## Phase 3 — Curate
- Rank by trust impact and legal exposure: no real deletion path outranks a clunky settings page.
- Flag dark patterns — the deliberate friction on cancel or delete — for removal.
- Separate "missing feature" from "hostile design"; name the hostile ones plainly.

## Phase 4 — Report
Create `LIFECYCLE.md` at repo root:
1. **The arc, mapped** — each stage, its path, and whether it is self-serve
2. **Findings** — each: stage · location · what the user hits · the fix
3. **Dark patterns** — the deliberate friction to remove, called out
4. **Priority fixes** — ranked by trust and exposure, deletion and export first

## Rules
- A product with no self-serve delete or export is holding users hostage
- Make leaving as easy as joining; that is what gets you recommended
- Report only — end by asking which lifecycle fixes to make first
