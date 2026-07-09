---
id: "58"
title: Interaction States & Motion Audit
family: Design
question: is it beautiful?
output: STATES.md
tagline: The state matrix every element owes you — hover, focus, active, disabled, loading, error — plus motion that means something versus transitions that just jiggle.
---
# Goal: Interaction States & Motion Audit

You are working inside this repo. Mission: audit every interactive element's full state matrix and every animation's purpose — find the missing states, the invisible focus, and the motion that communicates nothing.

Read-only pass. Your only write is the report file.

## Phase 1 — Inventory the interactive surface
- List the interactive species: button variants, links, inputs, selects, toggles, cards that click, rows that click, custom controls.
- For each species, locate its styles and record which states are defined: default, hover, focus-visible, active, disabled, loading, error, success.
- Inventory the motion: transitions, keyframes, animation libraries; the durations and easings in use; prefers-reduced-motion handling.

## Phase 2 — Audit through 8 lenses
1. **The state matrix** — species × states: the empty cells are the findings; the button with no focus style, the input with no error style
2. **Focus visibility** — tab through the core flow, or trace the focus rules: always visible, sufficient contrast, and never outline removed without a replacement
3. **Feedback latency** — does every click acknowledge within ~100ms (pressed state, spinner, optimistic update) or leave dead air
4. **Loading honesty** — skeletons that match the final layout versus content that shifts; the spinner flash on fast responses
5. **Disabled clarity** — disabled elements that explain themselves via hint or tooltip, versus mysteries; when disabled should have been hidden
6. **Motion with meaning** — each animation's job: orient, connect, or confirm — versus decoration; UI durations in the 100–300ms band
7. **One motion vocabulary** — shared duration and easing tokens, or every component improvising its own physics
8. **Reduced motion** — prefers-reduced-motion honored; parallax and autoplay behavior for the vestibular-sensitive

## Phase 3 — Curate
- Build the actual matrix table from the code.
- Rank the empty cells by traffic × severity — focus gaps first; they are accessibility, not polish.

## Phase 4 — Report
Create `STATES.md` at repo root:
1. **The matrix** — species × states: filled, empty, broken
2. **Focus and feedback findings** — ranked
3. **Motion inventory** — animation · purpose · duration and easing · verdict (keep, tune, cut)
4. **The motion tokens** — the durations and easings this codebase should standardize on

Start the report with today's date. If `STATES.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Trace real selectors and rendered behavior — a state that exists only in the design file does not exist
- Focus visibility outranks all polish
- No interactive UI in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fixes to make
