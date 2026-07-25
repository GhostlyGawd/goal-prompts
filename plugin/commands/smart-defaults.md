---
description: "What the product decides so the user doesn't have to — prefilled forms, remembered choices, resume where you left off — and every question it had no right to ask."
---

# Goal: Smart Defaults & Anticipation Audit

You are working inside this repo. Mission: find every decision the product pushes onto the user that it could have made itself. The products that feel effortless are the ones doing quiet work up front — inferring, remembering, prefilling — so the user's first move is the real one. Every unnecessary question is a small resignation.

Read-only pass. Read the forms, settings, onboarding, and state persistence in code, and run the first-run and return paths; your only write is the report file.

## Phase 1 — Inventory the questions
- Collect everything the product asks: onboarding steps, form fields, settings, pickers, empty dropdowns, confirmation choices.
- For each, note what the product already knows at that moment (locale, prior behavior, context, sensible convention) that could answer it.
- Trace what persists per user between sessions — and what resets to factory every visit.

## Phase 2 — Audit through 7 lenses
Cite the field, setting, or flow and its file for every finding.
1. **Works before configured** — the first run produces value with zero setup; every gate between install and first output that a default could remove
2. **Never ask what you know** — fields requesting what the system already has (email on file, detected timezone, last-used project); the form that starts blank in a product full of context
3. **Choices remembered** — the option picked three times becomes the default; sort orders, view modes, and last-used values persisted per user, not reset per session
4. **Resume, don't restart** — reopening lands where the user left off: the open document, the half-done task, the scroll depth — not the home screen
5. **The likely next step** — after each core action, the probable next action is pre-staged one step away, not re-navigated from scratch
6. **Settings as indecision** — options that exist because the team wouldn't choose; every toggle is a question exported to the user, so which could a strong default retire
7. **Cheap to overrule** — every inference visible and reversible in one step; a wrong guess costs a click, never a hunt — anticipation, not a trap

## Phase 3 — Curate
- Rank by frequency × friction: a needless question in the daily loop outranks one at setup.
- Separate "remove the question" (default it), "answer it from context" (prefill), and "remember the answer" (persist).
- For each, name the default you'd ship and the override path.

## Phase 4 — Report
Create `DEFAULTS.md` at repo root:
1. **Question findings** — each: lens · flow · file · what's asked · the default that retires it
2. **The memory map** — what persists per user today versus what should
3. **First-run delta** — steps between install and first value now, and after these defaults
4. **Retired settings** — the options a confident default would remove

Start the report with today's date. If `DEFAULTS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every proposed default names its evidence — the signal that makes it the right guess
- A default that guesses wrong expensively (destructive, billed, sent) is worse than asking; flag those as correctly asked
- No user-facing configuration or input surface in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which question the product should stop asking first
