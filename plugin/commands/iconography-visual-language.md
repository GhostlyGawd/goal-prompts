---
description: "The icon set as it actually ships — one visual language or a ransom note, every glyph readable and labeled, meanings consistent, and weight kept in check."
---

# Goal: Iconography & Visual Language Audit

You are working inside this repo. Mission: audit the icons and small visual marks this product ships — and find where they speak in different accents, carry meanings no one can guess, or ship without the label a screen reader needs.

Read-only pass. Read the icon assets, components, and their usages; render them if a dev server exists. Your only write is the report file.

## Phase 1 — Collect the set
- Find every icon source: SVG files, icon fonts, component library, inline paths, emoji used as icons.
- Count unique icons and how many libraries or styles are in play; note stroke widths, sizes, and grid.
- Map each icon to its meaning(s) and where it is used — the same glyph for two ideas, two glyphs for one idea.

## Phase 2 — Audit through 7 lenses
Cite the icon and its usage for every finding.
1. **One visual language** — consistent style, weight, corner, and grid, or a ransom note of mismatched sets
2. **Meaning is legible** — does the glyph read as its meaning without a caption; the abstract mark only the designer understands
3. **Consistent mapping** — one icon per concept and one concept per icon; the pencil that means both edit and compose
4. **Labeled for all** — icon-only controls with an accessible name or tooltip; decorative icons hidden from screen readers
5. **Icon plus label** — do critical or ambiguous actions pair the icon with text, rather than betting on recognition
6. **Size & optical balance** — legible at rendered sizes, aligned to text, optically centered in their buttons
7. **Weight & delivery** — one delivery method not four; a whole icon font shipped to use six glyphs; unoptimized SVG

## Phase 3 — Curate
- Rank by confusion × traffic: an ambiguous icon on a common control outranks a stylistic nit on a rare one.
- Separate "inconsistent style", "ambiguous meaning", and "unlabeled"; fix unlabeled first — it is accessibility.
- For each, name the icon, the problem, and the fix — relabel, replace, add text, or consolidate the set.

## Phase 4 — Report
Create `ICONOGRAPHY.md` at repo root:
1. **Icon census** — sources, libraries, counts, and the styles in play
2. **Meaning map** — icon · intended meaning · where used · collisions
3. **Findings** — each: lens · icon/usage · what the user misreads · the fix
4. **The system** — the one icon set, size scale, and labeling rule this codebase should adopt

Start the report with today's date. If `ICONOGRAPHY.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every finding names the icon and where it is used
- An icon-only control with no accessible name is a broken control
- Prefer one consistent set and icon-plus-label over clever marks
- No icons in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which icon fixes to make
