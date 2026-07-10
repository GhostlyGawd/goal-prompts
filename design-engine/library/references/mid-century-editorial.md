# Mid-Century Editorial — aesthetic dossier

The operator's brand world (see `boards/midcentury-editorial/`). This file is
what "expert" means: the rules that make the style read true.

## The world in one line
A beautifully art-directed 1958 catalog/magazine: warm cream paper, cobalt
blue as the color of *things*, one glowing orange lamp, ink linework, dense
printed detail, optimistic daylight.

## Color rules
- Paper is the ground. Cream (#F7F2E3-family), never white-white, never black.
- Cobalt is structure and objects (walls, furniture, arches, bottles) — a
  ladder of 3–5 blues from navy-ink to cornflower gives depth.
- Orange = THE accent, embodied as a lit object (lamp). Exactly one glow per
  composition. Orange never sets body text on paper (fails contrast; use the
  gated dark orange for text).
- Supporting: mustard, coral red, warm greys/tans. Ink (#1D1F28-family) draws
  every line.
- Saturation is print-ink, not screen-neon (cap ~78% HSL saturation).

## Technique rules (what makes gouache read as gouache)
- Limited palette, hard posterized shapes (no smooth gradients as atmosphere).
- Paper shows through: grain overlay everywhere (3–6% multiply).
- Edges alive: displacement/roughening on big shapes, wobble on drawn lines.
- Print misregistration: a color pass offset 1–2px reads as screen print.
- Density: real compositions carry hundreds of small honest details
  (documents with rule-lines, objects on shelves) — emptiness reads cheap.

## Composition rules (from the board)
- Depth by repetition: arches receding, shelves marching, tiles gridding.
- One focal glow (the lamp), placed off-center, cord visible.
- A human figure for scale and warmth, drawn as ink silhouette.
- Frame with ink rules like a printed page; captions in typewriter mono.

## Typography of the era (our system)
- Display: Fraunces (warm wonky display serif — the ad-world voice), tight
  leading (~1.0), italic for the emphatic word, cobalt or ink only.
- Body: Source Serif 4 — real print serif, 15–17px, 60–70ch measure.
- The typewriter: Space Mono for kickers, filenames, folios, captions —
  uppercase, letterspaced .1–.18em, small.
- Double-rule masthead lines (3px + 1px) are the page's signature frame.

## Motion character (apply via the motion tokens)
Curtains and lamplight, not springs and pops: slower-than-tech eases
(--ease-standard glide), one long drift per page (--dur-drift, e.g. the lamp's
glow breathing), reveals like a page turning — opacity+2-4px rise, staggered
30–60ms. Reduced-motion collapses to instant, nothing depends on animation.

## Named exemplars (for calibration, not copying)
Charles Schridde's Motorola "House of the Future" ads; Case Study House
program photography (Julius Shulman) reframed as illustration; 1950s Esquire /
Fortune editorial illustration; Alexander Girard's textile geometry; George
Nelson's Bubble Lamps (the literal lamp).
