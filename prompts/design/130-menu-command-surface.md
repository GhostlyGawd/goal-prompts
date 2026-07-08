---
id: "130"
title: Menu & Command Surface Audit
family: Design
question: is it beautiful?
output: MENUS.md
tagline: Menus, dropdowns, context menus, and command palettes — do they reveal what is inside, work by keyboard and thumb, and still find things as the list grows?
---
# Goal: Menu & Command Surface Audit

You are working inside this repo. Mission: audit every place actions and destinations hide behind a click — menus, dropdowns, context menus, overflow "⋯" buttons, and any command palette — and find the ones that hide too much, cost too much to reach, or fall apart at scale.

Read-only pass. Trigger the menus in the running app or trace their components and handlers; your only write is the report file.

## Phase 1 — Inventory the surfaces
- List every menu species: primary/secondary nav menus, select dropdowns, context (right-click) menus, overflow and kebab menus, command palette, action bars.
- For each, record how it opens, what it contains, and how it is built (native `<select>`, custom, library).
- Note keyboard access, focus handling, and whether items are labeled or icon-only.

## Phase 2 — Audit through 8 lenses
Cite the component and trigger for every finding.
1. **Discoverability** — can a user tell what is inside before opening; the critical action buried in an unlabeled kebab
2. **Reachability** — click and keystroke cost to the common items; the everyday action three menus deep
3. **Keyboard & focus** — open, arrow, type-ahead, Escape, and focus return on close; the menu you cannot leave without a mouse
4. **Touch & pointer** — hover-only menus with no tap path; targets too small or too close for a thumb
5. **Labeling** — verb-first, plain-language items; icon-only entries with no accessible name or tooltip
6. **Grouping & order** — related items grouped, destructive items separated, most-used near the top — not source-code order
7. **Scale** — the menu at 5 items versus 50: search, sections, or a wall to scroll; the flat list that should be grouped
8. **State & feedback** — disabled items that explain why, selected/checked state, loading, and closing on select or outside click

## Phase 3 — Curate
- Rank by traffic × cost: a hidden or unreachable everyday action outranks a cosmetic ordering nit.
- Separate "hidden" (cannot find it), "unreachable" (cannot operate it), and "unruly" (does not scale).
- For each, name the surface and the fix — promote, label, group, or make a palette.

## Phase 4 — Report
Create `MENUS.md` at repo root:
1. **Menu inventory** — species · trigger · contents · how built · keyboard/touch verdict
2. **Findings** — each: lens · component · what the user cannot do · the fix
3. **Promote list** — actions that should leave a menu for a visible control
4. **The one rule** — the menu convention this codebase should standardize on

## Rules
- Every finding names the menu component and how it is triggered
- An action nobody can find is an action that does not exist
- Report only — end by asking which menu fixes to make
