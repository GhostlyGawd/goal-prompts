---
name: graphic-design
description: Produce brand graphics — heroes, marks, icons, OG cards, illustration — from real reference assets and craft-dense procedural art, never bare primitives. Use for any visual asset work.
---

# Graphic Design

**MANDATORY, before any pixels:** read `design-engine/library/INDEX.md`, the
active board's `board.json` + images (`library/boards/`), and the relevant
technique files. The library is the expertise; working from memory instead of
the library is the defect that produces stick-figure art.

## The asset ladder (in order of preference)
1. **Re-inked reference imagery** — any image in `library/boards/` (or newly
   supplied by the operator) processed through `tools/image_lab.py` per
   `techniques/image-treatment.md`. This is THE way to make hero art: it
   inherits the reference's density and craft for free. New operator images
   drop into boards/ and are production-usable the same day.
2. **Craft-dense procedural art** — `tools/scene.py` per
   `techniques/svg-gouache.md`: wobble, roughened edges, hatching, grain,
   misregistration, 150+ element density for hero-grade scenes. For
   secondary surfaces, diagrams, OG backgrounds, motion props.
3. **Bare geometric primitives** — ONLY for the mark itself (which must
   survive 16px) and UI glyphs. A composition made only of clean primitives
   is a review defect (library checklist #1).

## Non-negotiables (from the library checklist)
- Grain/texture present; edges alive on anything hero-grade.
- One glowing focal per composition (the board's law).
- Palette from brand.json/board.json only; print-ink saturation.
- Marks run the gauntlet before showing: app icon → favicon → nav → real
  16px tab → one-color.
- Every asset regenerable: source, command, and palette recorded (sidecar
  note or generator script). Hand-tuned unreproducible files are forbidden.
- Artifacts self-contained (fonts + images as data URIs).

## Tools
`image_lab.py` (sample/map/duotone/halftone/grain/outline), `scene.py`,
`mark_render.py` (the mark's one implementation — extend it, never redraw),
`motion_preview.cjs` (motion/video artifacts), host generators (og.py,
icons.py). Missing capability? PROTOCOL.md §1–2: find, then build, then
register in TOOLS.md.

## Gate
Present via `techniques/presentation-protocol.md` (or `tools/present.py`):
options as finished things, labeled, one recommendation, evidence in
appendix. For style-fidelity work, ALWAYS show the source reference beside
the output — the operator judges likeness directly.
