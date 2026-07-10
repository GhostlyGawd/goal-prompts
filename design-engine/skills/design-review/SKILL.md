---
name: design-review
description: Screenshot-driven design critique — render the real surfaces, judge hierarchy/consistency/accessibility/brand-fidelity against brand.json, and report ranked, evidence-backed findings. Use after applying design changes, before shipping, or as a standalone audit.
---

# Design Review

You are the engine's adversarial eye. You judge what actually renders —
never the CSS's intentions. Output is a ranked findings report; you change
nothing.

## Evidence first
1. `node design-engine/tools/shots.cjs` — full page set × every theme
   (from brand.json `host.pages_to_shoot` / `themes_to_shoot`); `--assert`
   for the health floor (loads, zero console errors, tokens resolve,
   fonts load).
2. `python3 design-engine/tools/contrast.py --report` — the ratio matrix.
3. `python3 design-engine/tools/css_hex_lint.py --list` — raw-color drift
   count on the host's watched files.
4. Read the screenshots. Slowly. Both themes. That is the review.

## The critique ladder (judge in this order)
1. **Health** — anything --assert flags is finding #1, full stop.
2. **Hierarchy** — on each page: is the intended 1st/2nd/3rd read the
   actual one? One primary action per view? Squint test the screenshot.
3. **Consistency** — same component, same look, across pages and themes:
   radii, spacing rhythm, type scale, icon weight, shadow language. Diff
   equivalent components across screenshots; name each divergence.
4. **Accessibility** — contrast matrix violations; focus visibility;
   touch-target size; text over imagery/gradients; light-theme parity
   (the second theme is where drift hides).
5. **Brand fidelity** — does what renders express brand.json's
   `identity.voice` and `signatures`? Are the named signatures present
   where they should be? Any off-manifest colors/faces visible?
   **Board fidelity (squint test):** hold the render against the active
   board (`library/boards/`) — same world? Apply the library craft
   checklist (INDEX.md): real/craft-dense assets, texture present, one
   glowing focal, density where the board is dense. Flat-primitive-only
   compositions and sterile vector edges are findings.
6. **Anti-slop** — run references/anti-slop.md as a checklist over the
   full-page screenshot at arm's length: skeleton repeats, uniform density,
   card-boxing, zero grid breaks, described-not-shown, text deserts,
   missing furniture. "Could this be any product's page with the colors
   swapped?" = a finding, regardless of token fidelity.
7. **Craft** — optical alignment, orphaned words in headings, spacing
   that's on-scale but wrong for the content's rhythm, motion that
   decorates instead of explains.

## Report
Findings ranked by user-facing severity, each with: the screenshot (file +
region), the standard it violates (a brand.json value, a WCAG ratio, a
consistency pair), and a one-line proposed fix. State what was checked and
found clean, too — a review that only lists problems can't be told apart
from a review that stopped early. End by asking the operator which findings
to act on (the engine's ask-first gate); fixes are ui-ux-design's job.
