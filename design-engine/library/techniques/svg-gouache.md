# Technique — svg gouache (procedural craft density)

For surfaces that need art with no photo reference: draw with `tools/scene.py`
so vectors read as printed illustration, never as "clean minimal vector".
Flat-primitive-only compositions are a review defect (INDEX checklist #1).

## The five moves (all in scene.py, deterministic by seed)
1. **Wobble** — `wobble_path(points, seed, amp≈0.7–1.2)`: every drawn line
   gets hand jitter. Straight SVG lines are the tell of lazy vector art.
2. **Rough edges** — `rough_filter(scale≈1.6–2.4)` on big filled shapes:
   displacement turns geometry into brushwork.
3. **Grain** — `grain_filter()` over the whole scene at 3–6% multiply.
4. **Hatching** — `hatch(...)` for shadow and texture, not opacity fades.
5. **Misregistration** — `misregister(body, dx≈1.4)`: the offset second color
   pass that says "printed by humans".

## Density budget
A hero-grade scene wants 150+ honest elements (documents with rule lines,
tiles, shelf silhouettes, a figure). scene.py generators (`doc_shelf`,
`checker_floor`, `arch_band`, `bubble_lamp`) exist so density is cheap.
If a composition has under ~30 elements, it is a spot illustration, not a hero.

## Composition (see references/mid-century-editorial.md)
Depth by repetition; one glow (`bubble_lamp` with glow=True — the ONLY glow);
ink figure for scale; frame with rules. Palette from brand.json/board.json
only.

## Honest limits
Procedural art approaches the board but the re-ink pipeline
(image-treatment.md) beats it whenever a reference exists — the Gate-E proof
showed exactly this. Reach for scene.py for secondary surfaces, diagrams,
OG backgrounds, motion props; reach for image_lab for heroes.
