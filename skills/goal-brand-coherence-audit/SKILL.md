---
name: goal-brand-coherence-audit
description: "Does this look like one thing made on purpose — logo usage, icon language, imagery, radius and shadow DNA — audited against what the brand claims to be. Audit brief 59 · Design — runs a four-phase audit of the current repo and writes BRAND.md at the repo root."
---

# Goal: Brand Coherence Audit

You are working inside this repo. Mission: judge whether this product's visual identity reads as one deliberate thing — across logo, icons, illustration, imagery, and graphic assets — and find where it drifts into a collage.

Read-only pass. Your only write is the report file.

## Phase 1 — Collect the identity
- Gather what the brand claims: name, tagline, stated personality — from README, marketing pages, design docs, brand files if any exist.
- Inventory the assets: logo variants, favicon, OG images, icon sets and their sources, illustrations, photography, empty-state art, email and social templates in the repo.
- Note the graphic DNA in code: border radii, shadow styles, gradients — the recurring shapes that make a look.

## Phase 2 — Audit through 8 lenses
1. **One icon language** — stroke widths, corner styles, fill versus outline, grid sizes: one set, or three libraries cohabiting
2. **Logo hygiene** — variants, clear space, minimum sizes, the backgrounds it appears on; the stretched and recolored sins
3. **Radius and shadow DNA** — corner radii and elevation as a consistent signature, or per-component whims; count the distinct radii
4. **Imagery voice** — photos and illustrations sharing a treatment (grade, style, subject) or stock-photo roulette
5. **Personality match** — does the visual tone (playful, serious, technical, warm) match the copy's tone and the product's claim; cite the mismatches
6. **Cross-surface consistency** — app, marketing site, emails, OG cards, favicon: recognizably the same product?
7. **Asset hygiene** — SVGs optimized and consistent (viewBoxes, currentColor), raster where vector belongs, duplicate logo files quietly drifting apart
8. **Distinctiveness** — swap the logo for a competitor's: does anything else still identify this product; name the ownable graphic elements, or their absence

## Phase 3 — Curate
- Name the identity in one sentence, from evidence — what the visuals actually say today.
- Rank drifts by user-facing surface area; separate unify fixes (pick one of the three styles) from define gaps (no style was ever chosen).

## Phase 4 — Report
Create `BRAND.md` at repo root:
1. **The identity, as shipped** — one honest paragraph
2. **Asset census** — logos, icons, imagery: counts, sources, drift
3. **Findings** — ranked by visibility
4. **The coherence kit** — the 5–10 decisions (radius, icon set, image treatment…) that would make it one thing

Start the report with today's date. If `BRAND.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Judge what ships, not what the brand deck intended — cite files and surfaces
- Consistency beats beauty; one okay style everywhere outranks three good ones
- No brand surface in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fixes to make
