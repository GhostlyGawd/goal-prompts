# Design Engine

A portable branding & design engine. One folder holds the entire brand as
data (`brand.json`), the tools that compile, validate, and render it, and
the design skills that know how to use them. **Copy this folder into another
repo, write a new brand.json, wire the gate — ported.**

It is also a Claude Code plugin (`.claude-plugin/plugin.json`): installed,
it contributes `/design-engine:de-*` commands and six design skills.

## The idea

Design systems drift because the brand lives in N places — a CSS file, a
logo SVG, an icon script, a social-card generator, someone's memory. Here
it lives once:

```
brand.json  ──tokens_build──▶  tokens.css            (every page links it)
            ──mark_render───▶  inline SVG, favicon,  (header, tab,
                               PNG app icons          home-screen, OG)
            ──specimen──────▶  out/specimen.html     (the review artifact)
            ──brand_lint────▶  exit code             (structure + invariants)
            ──contrast──────▶  exit code             (the WCAG matrix)
```

Validators exit non-zero — the gate is an exit code, not a style guide
nobody reads (the host's ADR-1 principle).

## Layout

```
brand.json           THE single source of brand truth (see brand.schema.json)
tools/               executables — see TOOLS.md for the full index
skills/              six design skills: brand-strategy, visual-identity,
                     ui-ux-design, motion-design, graphic-design, design-review
commands/            /design-engine:de-* thin wrappers over the tools/skills
PROTOCOL.md          how to find or build a new tool (rules of extension)
TOOLS.md             every tool: invocation, exit contract, gate status
out/                 gitignored: specimen.html, shots/, contrast-report.txt
```

## Quickstart (10 minutes, any repo)

1. Copy `design-engine/` to the repo root.
2. Write `brand.json`: encode the palette (role names of your choice, but
   keep one theme as `default_theme`), type faces (files must exist on
   disk), space/radii, motion, mark geometry, and the `host` block —
   where tokens.css goes, where fonts live, which pages to screenshot.
3. `python3 design-engine/tools/brand_lint.py` until clean.
4. `python3 design-engine/tools/contrast.py` until clean — set the
   thresholds in brand.json `contrast` to floors your palette actually
   clears, then only ever raise them.
5. Compile: `python3 design-engine/tools/tokens_build.py` writes
   `host.tokens_out`; link it from your pages. (Python-build hosts can
   instead `import tokens_build` and consume `compile_css()` directly —
   set `host.integration` accordingly; this repo's build.py is the
   reference.)
6. Wire the gate: add brand_lint + contrast + the engine's tests
   (`python3 -m unittest discover -s design-engine/tests`) to your check
   script/CI.
7. Look at it: `python3 design-engine/tools/specimen.py` →
   `out/specimen.html`.

## The portability contract

**The host provides:** a `host` block in brand.json; something that links
the compiled tokens file; (optionally) a check gate to wire the validators
into; (optionally) node + playwright-core + Chromium for screenshots and
Pillow/fontTools for raster/font work.

**The engine guarantees:** core tools are stdlib-Python/zero-dep-Node and
run anywhere; every validator exits non-zero on violation; generate-time
tools (png/font/screenshot) degrade to a loud SKIP when their deps are
absent; engine code never hardcodes host facts — everything host-specific
is data in brand.json. The host may import the engine; the engine never
imports the host.

## Working on a brand

The skills are the method — each ends at an operator decision gate:

| phase | skill | command |
|---|---|---|
| what the brand IS | brand-strategy | `/design-engine:de-strategy` |
| the validated system | visual-identity | `/design-engine:de-identity` |
| applying to surfaces | ui-ux-design | — (part of normal editing) |
| motion language | motion-design | — |
| assets & marks | graphic-design | — |
| critique | design-review | `/design-engine:de-review` |

Utility commands: `de-tokens` (compile/--check), `de-contrast` (the
matrix), `de-shots` (screenshots / --assert health).

Need a capability the engine lacks? PROTOCOL.md defines how to find or
build it without weakening anything.
