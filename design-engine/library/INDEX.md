# LIBRARY — the engine's mind

The callable knowledge layer. **Every design skill is REQUIRED to load the
relevant entries before producing pixels** (the skills say so explicitly).
Quality lives here, not in per-session effort.

## Boards — `boards/<name>/`
Operator reference imagery as first-class assets: the images + `board.json`
(machine-sampled palettes via image_lab, decoded motifs, system rules, don'ts).
Current: **midcentury-editorial** (5 images, hero-grade: arch-hall).
Drop new images into a board folder and run `image_lab.py sample` — they are
usable hero art the same day via `image_lab.py map`.

## References — `references/`
- `mid-century-editorial.md` — the aesthetic dossier: what makes the style
  read true, composition rules, type rules, motion character, named exemplars.
- `anti-slop.md` — the ten named defects of generic AI UI (section-skeleton
  repeat, uniform density, card-boxing, no grid violation, described-not-shown,
  text deserts, furniture-free, symmetry-default, hedge-copy, decorative
  motion). Review-enforced; token-swapping a slop skeleton is still slop.

## Techniques — `techniques/` (each is an executable recipe)
- `image-treatment.md` — reference/generated image → brand asset (the re-ink
  pipeline). THE default way to make hero art.
- `svg-gouache.md` — procedural art with craft density (scene.py): wobble,
  hatching, roughened edges, grain, misregistration. The fallback when no
  reference exists.
- `hero-composition.md` — how the board composes a hero; checklist.
- `presentation-protocol.md` — the selection science for gates/artifacts.
- `qa-loop.md` — the ship gate for visual work: matrix asserts (viewports ×
  themes, overflow check), the contact sheet review, interaction states,
  findings in writing. The gate checks logic; this checks design.
- `editorial-layout.md` — the composition system: magazine furniture, scale
  violence, asymmetry & grid breaks, content-as-artifact, inhabited pages,
  the motif used structurally. The antidote to every anti-slop defect.

## The craft checklist (design-review enforces this)
1. Real assets or craft-dense procedural — flat-primitive-only art is a defect.
2. Texture present (grain/paper) and edges alive (rough/wobble), not sterile.
3. One glowing focal per composition; supporting detail is dense, not empty.
4. Limited palette, posterized shapes, ink discipline — from the board/brand,
   never ad-hoc colors.
5. Squint test against the board: same world?
6. All text/color pairings pre-gated with the engine's contrast math.
