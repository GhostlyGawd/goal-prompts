# DESIGN_DIRECTION — the ledger

The pinned art direction for every Goal Prompts surface (landing, `b/`/`p/`
detail pages, Studio, Vitals, OG cards, icons). This file exists because of a
failure mode we measured, not a preference: **an agent asked to "redesign the
landing page" with no pinned direction samples the maximum-likelihood landing
page** — soft neutrals, rounded cards, a kicker, two buttons, a features grid.
Every regeneration re-converges there. Ten redesign passes produced ten
near-identical pages (see git log up to 0.13). A direction only survives
across sessions if it is written down as *decisions*, not adjectives.

Read this before restyling anything. If you want to overturn it, append a
superseding ADR to DECISIONS.md first (ADR discipline applies to design).

## The concept (one sentence)

**The landing page is typeset like the artifact the product sells — an audit
report:** paper and ink, ruled sections, numbered findings, mono metadata,
and one vermilion accent used the way an auditor uses a red pen.

Everything follows from that sentence. When in doubt, ask "what would a
beautifully typeset audit report do?" — not "what do landing pages do?"

## Hard rules (the tripwires)

1. **One accent.** Vermilion (`--fc`: `#FF6B47` dark / `#B93A16` light) is
   the only voice color. The 17 family hues are *metadata* — a dot, a filing
   tab, a swatch — never decoration, never a second accent, never a badge
   background. If a change makes two hues compete at section scale, it's off
   direction.
2. **Ink and paper, warm.** Backgrounds are warm ink (`#15120D`) / warm paper
   (`#F2EFE6`), never neutral gray, never pure black/white, never gradients.
3. **Rules do the structure.** Sections open with a numbered mono kicker on a
   hairline (`01 · THE PROBLEM ————`). Lists are ruled rows, not floating
   rounded panels. Radius is 2–3px; if a new component wants ≥8px rounding,
   it's drifting back to the slop basin.
4. **Mono is the metadata voice.** File names, counts, severities, nav,
   labels: IBM Plex Mono. Display: Schibsted Grotesk, heavy (700–780) and
   tight. Body: Plex Sans. No new fonts.
5. **Show the artifact, not a schematic.** Hero-level proof slots show *real*
   content from this repo's own reports (BUGS.md findings, real commits).
   Never replace them with lorem-shaped mockups.
6. **The mark is 4 bars, tallest flagged vermilion** ("every audit surfaces
   the finding that matters"). It lives in `build.BRAND_MARK` + `FAVICON`,
   `scripts/icons.py`, `scripts/og.py`, and inline in `template.html`,
   `studio.html`, `vitals.html` — change all seven together or none.
7. **Tokens are the only theme.** Palette changes go in `TOKENS_CSS`
   (build.py) exclusively; component CSS may reference tokens only. That is
   how one edit re-keys every surface at once.

## Process rules (why redesigns used to be invisible)

- **Render before you commit.** Run `node scripts/design-shot.cjs` and *look
  at the PNGs* (light, dark, mobile) before and after. CSS edited on
  plausibility alone is how sub-perceptual "redesigns" happen.
- **A visual change must be visible.** If a before/after screenshot diff
  wouldn't be noticed by a stranger at arm's length, don't call it a
  redesign; call it maintenance.
- **Consistency audits (BRAND.md et al.) are maintenance, not design.** They
  keep this direction tight; they cannot originate one. Don't run another
  coherence audit and expect the identity to improve.
