---
id: "146"
title: Modal, Dialog & Overlay Audit
family: Design
question: is it beautiful?
output: OVERLAYS.md
tagline: Every floating layer — modals, drawers, popovers, sheets — does each earn its interruption, trap focus, dismiss cleanly, and never stack into a maze?
related: 58 130 133 86
---
# Goal: Modal, Dialog & Overlay Audit

You are working inside this repo. Mission: audit every surface that floats above the page — modals, dialogs, drawers, popovers, tooltips, sheets — and find the ones that interrupt without earning it, trap the user, or break focus and dismissal.

Read-only pass. Trigger the overlays in the running app or trace their components and open/close handlers; your only write is the report file.

## Phase 1 — Inventory the overlays
- List every floating species: modal dialog, confirm/alert, side drawer, bottom sheet, popover, dropdown panel, tooltip, coachmark.
- For each, record what triggers it, what it contains, whether it blocks the page (modal) or not, and how it is built (native `<dialog>`, library, custom).
- Note the open, close, and stacking behavior, and the keyboard and focus handling.

## Phase 2 — Audit through 8 lenses
Cite the component and trigger for every finding.
1. **Earns the interruption** — does this need to be a modal, or would inline, a page, or a non-blocking panel serve; the dialog that stops everything to show one line
2. **Focus management** — focus moves in on open, stays trapped inside, and returns to the trigger on close; the modal you can tab out of behind
3. **Dismissal** — Escape, backdrop click, and an always-visible close; the overlay with no exit, or one that closes on a stray click mid-edit
4. **Stacking** — modals opening modals; z-index wars, scroll bleed to the page behind, two backdrops fighting
5. **Scroll & size** — long content scrolls within the overlay, not the body; behavior when it is taller than the viewport, especially on a phone
6. **Confirmation honesty** — destructive confirms that name the consequence and default to safe; the "Are you sure?" that guards nothing and trains people to click through
7. **Accessibility** — role, aria-modal, a labelled title, and the rest of the page inert to screen readers while open
8. **Motion & responsiveness** — enter and exit that orient not distract; the desktop modal that should be a full sheet on a phone

## Phase 3 — Curate
- Rank by how badly each traps or blocks a user on a core flow — a leaking focus trap or an exit-less modal outranks a slow fade.
- Separate "should not be an overlay", "broken focus/dismissal", and "stacking/scroll"; fix trapping and exits first.
- For each, name the overlay and the fix.

## Phase 4 — Report
Create `OVERLAYS.md` at repo root:
1. **Overlay inventory** — species · trigger · blocking? · how built · focus/dismiss verdict
2. **Findings** — each: lens · component · what the user hits · the fix
3. **Demote list** — the overlays that should become inline, a page, or a non-blocking panel
4. **The one rule** — the overlay and focus convention this codebase should adopt

Start the report with today's date. If `OVERLAYS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every finding names the overlay component and how it opens and closes
- An overlay a keyboard user cannot escape is a broken overlay
- Prefer the least interruptive surface that does the job
- No modals or overlays in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which overlay fixes to make
