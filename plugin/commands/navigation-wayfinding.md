---
description: "The three questions every screen owes a user — where am I, where can I go, how do I get back — plus the nav that hides, the dead ends, and the jargon labels."
---

# Goal: Navigation & Wayfinding Audit

You are working inside this repo. Mission: judge whether a user can always answer three questions — where am I, where can I go, and how do I get back — and find the screens where the navigation goes silent.

Read-only pass. Walk the app or trace the routes, nav components, and menus; your only write is the report file.

## Phase 1 — Map the structure
- Enumerate the routes/screens and the global navigation: primary nav, secondary nav, footer, tabs, breadcrumbs.
- Draw the tree: what is top-level, what is nested, what is reachable only by deep link.
- For each key screen note the current-location cue and the way back. Pick 5–8 core journeys to walk.

## Phase 2 — Audit through 8 lenses
Cite the route, component, or label for every finding.
1. **Where am I** — active-state and title cues on every screen; the page that leaves you guessing which section you are in
2. **Where can I go** — are the next steps visible, or does the path forward depend on knowing a URL
3. **How do I get back** — back, breadcrumbs, and escape from modals and flows; the dead end whose only exit is the browser button
4. **Depth & reach** — clicks to each key destination; the important page buried four levels down
5. **Label clarity** — do nav labels match the user's words, or the org chart and internal jargon
6. **Structure fit** — does the IA group things the way users look for them, or the way the code is organized
7. **Consistency** — nav in the same place, order, and behavior across screens; the section that reinvents it
8. **State & scale** — active/hover/focus on nav items, and whether the menu still holds at 50 items, not just the demo's 5

## Phase 3 — Curate
- Rank by how many core journeys each break touches — a broken back on the main flow outranks a mislabeled footer link.
- Separate "lost" (no location cue), "stuck" (no way forward or back), and "buried" (too deep); fix lost and stuck first.
- For each, name the screen and the fix.

## Phase 4 — Report
Create `NAVIGATION.md` at repo root:
1. **The map** — the nav tree as it actually is, with depth and dead ends marked
2. **Journey walks** — each core journey: where a user gets lost, stuck, or turned around
3. **Findings** — each: lens · route/component · what the user cannot answer · the fix
4. **The one rule** — the wayfinding convention this codebase should adopt

Start the report with today's date. If `NAVIGATION.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every finding names a route, component, or label — not a vibe
- A dead end on a core journey is a bug, not a nicety
- No navigation surface in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which wayfinding fixes to make
