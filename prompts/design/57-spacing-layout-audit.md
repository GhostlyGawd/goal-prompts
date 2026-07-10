---
id: "57"
title: Spacing & Layout Audit
family: Design
question: is it beautiful?
output: LAYOUT.md
example: /reports/LAYOUT.md
tagline: The spacing scale nobody wrote down — margins and paddings inventoried, grid discipline checked, alignment breaks found, and density judged screen by screen.
---
# Goal: Spacing & Layout Audit

You are working inside this repo. Mission: reverse-engineer the spacing system this product actually uses, find where layout discipline breaks — misalignment, arbitrary gaps, container chaos — and judge density against each screen's job.

Read-only pass. Your only write is the report file.

## Phase 1 — Extract the system
- Grep margins, paddings, and gaps; count distinct values. Is there a scale — 4/8-based, tokens — and what fraction of usage honors it?
- Map the layout machinery: grids, flex patterns, container max-widths, breakpoints. How many container widths exist, and why?
- Collect the debt markers: magic negative margins, absolute-position patches, !important in layout rules, transform nudges.

## Phase 2 — Audit through 8 lenses
1. **Scale adherence** — values on versus off the scale; the 13px gap between two 16px siblings
2. **Alignment integrity** — edges that should share a line and don't; optical versus box alignment on icons and buttons
3. **Container discipline** — consistent max-widths and gutters, or every page choosing its own; content touching viewport edges on mobile
4. **Density fit** — dense screens (tables, dashboards) versus breathing screens (landing, onboarding): is the density chosen or accidental
5. **Proximity semantics** — spacing encoding relationships: within-group gaps smaller than between-group gaps, consistently
6. **Responsive re-flow** — the layout at 320, 768, and 1280: what wraps awkwardly, overflows, or leaves canyon whitespace
7. **Spacing ownership** — components carrying their own outer margins (chaos) versus parents composing gaps (discipline)
8. **The patch layer** — every negative margin and nudge marks a place the system failed; inventory them as evidence

## Phase 3 — Curate
- Propose the scale; map today's values onto it.
- Rank fixes by screens straightened per token adopted; the patch-layer deletions come free.

## Phase 4 — Report
Create `LAYOUT.md` at repo root:
1. **The spacing census** — values, counts, on or off scale
2. **Alignment and container findings** — with selectors and coordinates
3. **Density verdicts** — per key screen, with reasoning
4. **Fixes** — the scale, the container rule, and the patches to delete

Start the report with today's date. If `LAYOUT.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Cite values and selectors — a cramped feeling needs the pixels behind it
- Fix systems, not instances; one token beats forty edits
- No UI layout in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fixes to make
