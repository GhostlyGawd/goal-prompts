---
id: "54"
title: Visual Hierarchy Audit
family: Design
question: is it beautiful?
output: HIERARCHY.md
example: /reports/HIERARCHY.md
tagline: Where the eye actually goes versus where it should — focal points, size and weight and contrast doing real work, and the screens where everything shouts at once.
---
# Goal: Visual Hierarchy Audit

You are working inside this repo. Mission: audit whether each key screen directs attention where the product needs it — and find the screens where everything competes and nothing wins.

Read-only pass. Your only write is the report file. If a dev server exists, run it read-only and judge rendered screens; otherwise trace the stylesheets and components.

## Phase 1 — Map the screens
- List the 5–8 screens or states that matter most: entry, core value, conversion, empty, error.
- For each, name the one thing a user must see or do there. That is the intended focal point — write it down before auditing, so the audit can disagree with it.
- Locate the styling sources: global CSS, design tokens, component styles, utility classes.

## Phase 2 — Audit through 8 lenses
1. **The squint test** — rank each screen's elements by visual weight from the actual styles: does the intended focal point win, or does a sidebar, banner, or logo outshout it
2. **One primary action** — count elements styled as primary per screen; two primaries is zero primaries
3. **Size and weight math** — is importance encoded in the type scale and weights, or is everything 14–16px medium
4. **Contrast allocation** — is the highest contrast reserved for what matters most, or are decorative elements borrowing attention they never earned
5. **Position and flow** — does reading order match task order; key actions below the fold or stranded in corners
6. **Grouping and proximity** — related things near, unrelated things apart; borders and boxes doing work whitespace should do
7. **Signal-to-chrome ratio** — pixels spent on content versus navigation, borders, shadows, and decoration, per screen
8. **Consistency of emphasis** — the same importance styled the same way everywhere, or hierarchy reinvented per page

## Phase 3 — Curate
- For each key screen: intended focal point versus actual winner, citing the CSS that decides it.
- Rank fixes by attention reclaimed per line of CSS changed.

## Phase 4 — Report
Create `HIERARCHY.md` at repo root:
1. **Screen table** — screen · should win · actually wins · the deciding styles
2. **Findings** — ranked, each citing selectors, tokens, or values
3. **Fixes** — usually demotions; the fastest hierarchy fix is quieting what shouts
4. **The one rule** — the emphasis convention this codebase should adopt

Start the report with today's date. If `HIERARCHY.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every claim cites a selector, token, or measured value — no vibes without the pixels that cause them
- Prefer demoting noise over promoting signal; hierarchy is subtraction first
- No user interface in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fixes to make
