---
name: brand-strategy
description: Define or redefine what a brand IS before any pixel work — positioning, naming, voice, mark concepts, and visual direction, delivered as a reviewable strategy artifact ending at an operator decision gate. Use when starting a rebrand, naming a product, or when design work has no written strategy to serve.
---

# Brand Strategy

## MANDATORY first step
Read `design-engine/library/INDEX.md` and the active board
(`library/boards/*/board.json`) before producing anything visual; apply the
library craft checklist and present options per
`library/techniques/presentation-protocol.md` (or via `tools/present.py`).
Flat-primitive-only art and non-self-contained artifacts are defects.

You are running the strategy phase of the design engine. The output is a
decision artifact, not design: it exists so the operator can choose a
direction cheaply, before identity work makes change expensive.

## Ground rules
- Read `design-engine/brand.json` first — `identity` is the current verbal
  brand, `meta.brand_version` its generation. Read the host's positioning
  docs (README, landing copy) before proposing anything.
- Strategy work changes NO repo surface. The only writes are artifacts in
  `design-engine/out/`.
- End at a gate: present the artifact, ask the operator to pick. Never
  carry a "winner" forward on your own judgment.

## Method
1. **Anchor** — one paragraph on what the product does, for whom, and the
   feeling the brand must produce (from real evidence: the repo, its copy,
   its users). If the operator gave reference imagery, name what it encodes
   (era, palette temperature, geometry, mood) in concrete visual terms.
2. **Name candidates** (if naming is in scope) — 4–6, always including
   "keep the current name" with its equity honestly stated. For each: the
   idea it carries, how it sounds in a sentence ("check X", "X says the
   build is red"), collision risk (search npm, GitHub, domains via
   available tools), and how deep a rename would cut (display layer vs
   URLs/packages/namespaces).
3. **Mark concepts** — 3 distinct geometric directions, each expressible in
   brand.json `mark` primitives (the mark must survive: browser tab 16px,
   nav 24px, app icon 512px, OG card). Render real SVG via
   `tools/mark_render.py` geometry — no hand-waved descriptions.
4. **Palette direction** — 2–3 studies (surfaces + one accent each), each
   sanity-checked with `tools/contrast.py` math before showing. A study
   that can't reach the manifest's contrast floors is shown crossed out,
   with the failing ratio — honesty beats seduction.
5. **Voice** — tone in one sentence, 4–6 principles, banned words. Voice
   must be *testable*: a stranger should be able to say "this sentence is
   on/off brand".
6. **Type direction** — shortlist faces by role (display/sans/mono) with
   license class stated. Free/OFL unless the operator has said otherwise.

## Deliverable
One HTML artifact in `design-engine/out/` (build it like
`tools/specimen.py` builds its page — self-contained, real fonts where
possible) presenting all of the above side by side. Then STOP and ask:
which name, which mark, which palette direction, which type direction?
Record the picks in the artifact or a strategy note for the identity phase.
