---
name: ui-ux-design
description: Apply the brand system to product surfaces — layout, hierarchy, components, states — consuming tokens only, verified by screenshots. Use when styling or restyling pages, building components, or applying a new brand.json to an existing UI.
---

# UI / UX Design

## MANDATORY first step
Read `design-engine/library/INDEX.md` and the active board
(`library/boards/*/board.json`) before producing anything visual; apply the
library craft checklist and present options per
`library/techniques/presentation-protocol.md` (or via `tools/present.py`).
Flat-primitive-only art and non-self-contained artifacts are defects.

You apply `design-engine/brand.json` to real surfaces. The system is
already decided (visual-identity's job); your job is composition,
hierarchy, and fidelity — and keeping the token layer the only source of
color, space, and motion.

## Ground rules
- **Consume, never restate.** Every color is `var(--role)`, every duration
  `var(--dur-*)`, every gap on the spacing scale. A raw hex in component
  CSS is a defect — `tools/css_hex_lint.py` exists to make that an exit
  code; run it on the files you touch and drive its count down, never up.
- Layout literals that tokens can't carry (breakpoints in `@media`) stay
  literal but must mirror token values.
- Respect the host's structure: find where component CSS lives (inline
  blocks, a build string, files) and edit there. Never fork a second copy
  of a component's styles.

## Method
1. **Read the hierarchy before styling.** For each page: what must a
   visitor see 1st, 2nd, 3rd? One primary action per view; emphasis spends
   a budget — if everything is bold, nothing is.
2. **Type does the layout.** Scale + weight + width (measure ~60–75ch)
   carry structure; boxes and lines are the fallback, not the default.
3. **States are the design.** Hover, focus-visible, active, disabled,
   empty, loading, error — a component isn't done until all its states
   consume tokens and read clearly in every theme. Focus rings are
   non-negotiable.
4. **Motion is meaning.** Transitions use `var(--dur-*)` +
   `var(--ease-*)`; motion signals causality (what appeared, what
   changed), never decoration for its own sake. Reduced-motion must
   degrade gracefully (the token collapse handles duration; verify nothing
   depends on an animation to be usable).
5. **Verify by looking.** After changes:
   `node design-engine/tools/shots.cjs` for every affected page × theme,
   then read the screenshots — check hierarchy, spacing rhythm, contrast
   in situ, both themes. `--assert` mode must stay green (no console
   errors, tokens resolve, fonts load).

## Deliverable + gate
Changed surfaces + before/after screenshots from `out/shots/`. For a
restyle program, end at an operator gate with the screenshot grid; for
incremental work, the gate is the host's check script staying green.
