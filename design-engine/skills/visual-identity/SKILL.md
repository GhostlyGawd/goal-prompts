---
name: visual-identity
description: Derive a complete, validated visual identity system — palette, type, spacing, radii, elevation, motion, mark — as a new brand.json version, proven by the contrast gate and presented as a specimen page. Use after a strategy direction is chosen, or to evolve an existing system.
---

# Visual Identity

You turn a chosen direction into a complete system in
`design-engine/brand.json`. The manifest is the deliverable; the specimen
page is its proof. Nothing is applied to product surfaces in this phase.

## Ground rules
- Every change lands in brand.json, then immediately:
  `python3 design-engine/tools/brand_lint.py && python3 design-engine/tools/contrast.py`.
  The validator decides legibility, not taste. Iterate color candidates
  against the gate until the whole matrix passes — never lower a threshold
  to make a palette fit (raising one is always welcome).
- Bump `meta.brand_version` once per generation, note what changed.
- Regenerate the proof after every meaningful step:
  `python3 design-engine/tools/specimen.py` → `out/specimen.html`.

## Method, in dependency order
1. **Surfaces first** — the ink/panel ladder sets the world's light. Pick
   the default theme's 4 surfaces + 3 line steps; check text roles against
   all of them before touching accents.
2. **Text ramp** — text/body/dim/faint as a deliberate emphasis ladder
   (target: text ≥ 7:1, body/dim ≥ 4.5:1, faint ≥ 3:1 minimum on every
   surface).
3. **Accents + semantics** — brand accent(s), success/warning/danger, and
   the aliases that give them job names (`@success` refs). Keep the
   browse-primary vs act-primary distinction if the host has one.
4. **Categorical set** (if the host needs one) — derive N distinguishable
   hues *inside* the new world: sweep hue spacing programmatically, gate
   each with contrast.py, and set `categorical_mix_light` so every hue
   survives every theme. Squint test: the set should feel like one family.
5. **Companion themes** — a light theme is its own composition (same role
   names, re-derived values), not an inversion. Same gates apply.
6. **Type** — source chosen faces with `tools/font_subset.py` (license
   check is a gate; subset to latin; files land in the host's fonts dir);
   declare faces + stacks + preload in brand.json. brand_lint verifies the
   files exist.
7. **Motion** — durations (fast/base/slow + one signature long) and easing
   curves that express the brand's physics; `reduced_motion` policy stays
   `collapse-to-instant` unless the operator overrides.
8. **Elevation** — shadow/glow recipes as named tokens. If the brand's
   light has a direction (e.g. glow-from-within), it lives here.
9. **Mark** — final geometry in `mark` (bars/primitives, favicon
   composition). Verify at 16/24/64/512 via `tools/mark_render.py` and on
   the specimen.

## Deliverable + gate
`brand.json` vN passing brand_lint + contrast, `out/specimen.html`, and a
contrast report (`contrast.py --report`). Present the specimen and STOP:
the operator approves the system BEFORE any application work. Iterating
here is cheap; after application it is not.
