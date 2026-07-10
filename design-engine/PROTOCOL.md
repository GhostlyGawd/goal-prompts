# PROTOCOL — finding or building engine tools

The engine must be able to grow new capabilities without growing entropy.
This is the extension contract; it exists so the tenth tool is as
trustworthy as the first.

## 1 · FIND before you build

In order:
1. **TOOLS.md** — does a listed tool already do this, or take a flag that
   would? Read the tool's docstring, not just its name.
2. **The host's scripts/** — hosts often already have generators
   (screenshots, social cards, icons). Prefer extending the host's tool at
   its home over duplicating it in the engine — but if it encodes brand
   facts, move those facts to brand.json and make the tool read them.
3. **An existing tool + a small flag** beats a new tool. A new tool beats
   a bloated one. Judgment, then taste.

## 2 · BUILD, in this order of preference

1. **stdlib Python** — the default. Runs everywhere the engine goes.
2. **zero-dependency Node** — when the capability is browser/JS-shaped.
3. **Blessed generate-time deps** — Pillow (raster), fontTools + brotli
   (fonts), playwright-core + a system Chromium (rendering). Tools using
   these must detect absence and SKIP loudly with install hints, never
   crash cryptically — the core engine keeps working without them.
4. **Anything else** — stop. A new dependency class needs a decision
   record in the host's DECISIONS.md (or equivalent) *first*, naming what
   it buys and what it costs.

## 3 · Every new tool ships with

- **An exit contract.** Validators exit non-zero on violation with one
  line per finding (the gate is an exit code, not prose). Generators
  print what they wrote.
- **A test** in `design-engine/tests/` pinning the logic worth trusting.
- **One line in TOOLS.md** — name, invocation, contract, gate status.
- **A gate classification:** *gate-grade* (deterministic, dependency-free,
  wired into the host's check) or *generate-time* (needs deps or a
  browser; run on change; outputs committed; NEVER pixel-gated — browser
  and library versions drift, determinism doesn't survive them).
- **No host facts in code.** Paths, page lists, palette values, theme
  names — all read from brand.json. If a tool needs a new kind of host
  fact, extend the `host` block (and brand.schema.json).

## 4 · Never weaken

- Never lower a contrast threshold to make a palette fit; raise palettes
  to meet thresholds. (Narrowing recorded in brand.json with a dated note
  is the only exception, and it must monotonically tighten over time.)
- Never remove or soften a host gate step to get green; fix the red.
- Never fork a second source of truth for anything brand.json already
  holds — extend the manifest instead.

## 5 · Asset strategy (the anti-stick-figure rule)

Visual work draws from `design-engine/library/` in this order: (1) re-inked
reference imagery (`image_lab` over `library/boards/` or operator-supplied
images), (2) craft-dense procedural art (`scene.py` per the svg-gouache
technique), (3) bare primitives — marks and UI glyphs only. Every asset must
be regenerable (source + command + palette recorded). Gate artifacts are
self-contained (fonts and images as data URIs) and follow
library/techniques/presentation-protocol.md. If the host has an
image-generation API key, a generator backend may be added behind the same
image_lab pipeline (new dep class → host ADR first, §2.4).

## 6 · Naming & shape conventions

- Python tools: `snake_case.py`, module docstring states purpose +
  invocation + gate status, `main(argv) -> int`, `--brand` flag for a
  manifest override, shared helpers in `enginelib.py`.
- Node tools: `kebab-or-plain.cjs`, header comment likewise, no deps
  beyond the blessed list.
- Everything writes artifacts to `design-engine/out/` (gitignored),
  never to the repo root.
