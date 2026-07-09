---
description: "The type scale, or the lack of one — sizes, weights, line lengths and heights, font loading, and every place text is asked to do a job at the wrong size."
---

# Goal: Typography Audit

You are working inside this repo. Mission: inventory every way this product sets type and judge it as a system — scale, rhythm, readability, loading — then find where text works hardest and reads worst.

Read-only pass. Your only write is the report file.

## Phase 1 — Inventory the type
- Extract every font-size, weight, line-height, letter-spacing, and family in use: grep the CSS, tokens, and framework config; check computed styles on a running dev server if one exists.
- Count distinct values. A healthy system has one scale; record how many this one has grown.
- Map the fonts: families loaded, weights shipped versus weights used, subsets, and the loading strategy (swap, block, fallback stacks).

## Phase 2 — Audit through 8 lenses
1. **Scale coherence** — do the sizes form a deliberate scale with a ratio and steps, or an accretion of 13, 14, 15, 16, and 17px decisions
2. **Measure** — line lengths on real content: roughly 45–75 characters, or viewport-wide paragraphs on desktop
3. **Rhythm** — line-height fit for size and role (tight headings, roomy body); vertical spacing derived from type or improvised per component
4. **Weight discipline** — how many weights carry the hierarchy; bolding as the only emphasis tool; faux bold or italic where the weight was never loaded
5. **Hierarchy through type** — can the structure be read from type alone; heading levels that render identically
6. **Responsive type** — fixed pixels at every viewport, or fluid and stepped; readability at 320px and at 4k
7. **Loading and fallbacks** — flash behavior, fallback stacks matched to metrics, weights shipped but never used
8. **The neglected text** — form labels, captions, tables, code, empty states: styled deliberately or inheriting whatever was nearby

## Phase 3 — Curate
- Propose the minimal scale this product needs; map every current value onto it and count the deletions.
- Rank findings by pages of reading improved per change.

## Phase 4 — Report
Create `TYPOGRAPHY.md` at repo root:
1. **The inventory** — current values, clustered, with usage counts and sources
2. **The proposed scale** — sizes, weights, line-heights, and the mapping from today
3. **Findings** — ranked, with the file and selector behind each
4. **Font economics** — what is loaded versus used, and the bytes to reclaim

Start the report with today's date. If `TYPOGRAPHY.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Measured values only — cite the file and selector for every number
- The best deliverable is a smaller system, not more rules
- No UI typography in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fixes to make
