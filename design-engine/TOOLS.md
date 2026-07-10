# TOOLS — the engine's executable index

Every tool, its invocation, exit contract, and gate status. New tools
register here (PROTOCOL.md §3). All Python tools take `--brand PATH` to
override the manifest (default: `design-engine/brand.json`; env
`BRAND_JSON` also works).

| tool | runs on | does | gate status |
|---|---|---|---|
| `tools/brand_lint.py` | stdlib py | validates brand.json against brand.schema.json + semantic invariants (theme role parity, alias resolution, font files exist, contrast config names real roles). Exit 1 with one line per problem. | **gate-grade** — scripts/check step 2 |
| `tools/contrast.py` | stdlib py | the WCAG 2.1 matrix: text roles × surfaces, accent roles × surfaces, categorical hues (raw on default theme, color-mix'd on others) — all against thresholds brand.json itself declares. `--report [file]` writes the full matrix to out/contrast-report.txt. Exit 1 per violation. | **gate-grade** — scripts/check step 2 |
| `tools/tokens_build.py` | stdlib py | compiles brand.json → the host's tokens.css (fonts, themes, radii, space, elevation, motion, categorical rules, reduced-motion collapse). Importable (`compile_css()`) or CLI; `--check` diffs against disk and exits 1 on drift. | gate-grade transitively (the host build consumes it; engine tests pin parity) |
| `tools/mark_render.py` | stdlib py (+Pillow for PNG) | the mark's one implementation: `svg()` inline SVG, `favicon_data_uri()`, `png(size)` app icons. CLI prints SVG + URI; `--png SIZE OUT` rasterizes. | gate-grade transitively (build consumes svg/favicon; icons are generate-time) |
| `tools/specimen.py` | stdlib py | renders brand.json as out/specimen.html — palette with live ratios, categorical spectrum per theme, type ramp, space/radii, motion demos, mark at sizes, voice. The artifact every design gate reviews. | generate-time |
| `tools/css_hex_lint.py` | stdlib py | flags raw hex/rgb()/hsl() inside `<style>` blocks and style="" attributes of the files in brand.json host.hex_lint.files (allowlist = regexes, each a documented exception). `--list` reports without failing. | gate-grade **once the host's surfaces are var-clean** (rebrand Phase 4); until then run by hand |
| `tools/font_subset.py` | fontTools + brotli | license-checks (OFL/Apache/UFL name-table markers — gate, `--allow-unverified` needs an ADR) then latin-subsets a TTF/OTF to woff2 in the host's fonts dir. | generate-time |
| `tools/shots.cjs` | node + playwright-core + Chromium | boots a static server over the host, visits host.pages_to_shoot × themes_to_shoot. Default: screenshots → out/shots/. `--assert`: health floor (page loads, zero console/page errors, var(--ink) resolves, fonts loaded), exit 1 on failure. | `--assert` is gate-grade where node+Chromium are guaranteed; pixels never gated |
| `tools/image_lab.py` | Pillow | the image workhorse: `sample` (k-means palette from any image), `map` (re-ink onto a palette; posterize/boost), `duotone`, `halftone`, `grain`, `outline`, `crop`, `resize`. Turns board/reference/generated imagery into brand assets (see library/techniques/image-treatment.md). | generate-time |
| `tools/scene.py` | stdlib py | procedural illustration with craft density: wobble paths, hatching, grain/rough filters, misregistration, board-motif generators (arch bands, doc shelves, checker floors, bubble lamps). Deterministic by seed. Importable library, no CLI. | generate-time (importable) |
| `tools/present.py` | stdlib py | gate presentations from a JSON spec, structurally enforcing library/techniques/presentation-protocol.md (options as finished things, labels, one recommendation, appendix evidence, self-contained). | generate-time |
| `tools/motion_preview.cjs` | node + playwright-core | motion/video artifacts: records a WEBM of an HTML prototype + a frame strip of PNGs (`--seconds`, `--frames`, `--click`). For judging motion at gates; never pixel-gated. | generate-time |
| `tools/imagegen.py` | stdlib urllib + provider API key | NEW raster imagery: pluggable providers (openai gpt-image-1 / replicate FLUX via IMAGEGEN_PROVIDER + key env), `--style <board>` composes the board's technique+palette language into the prompt, `--reink` pipes output through image_lab onto the brand inks. Exits loudly with setup instructions when no key is configured. | generate-time (requires key) |
| `tools/qa_sheet.py` | Pillow | tiles every screenshot in out/shots/ into ONE labeled contact sheet (out/qa-sheet.jpg) — the QA loop's review artifact; "look at everything" becomes one image. | generate-time |
| `tools/enginelib.py` | stdlib py | shared library, not a CLI: manifest loading, WCAG math, color-mix arithmetic, theme/alias resolution. | n/a |
| `tests/` (test_engine.py) | stdlib py | pins tool logic + the manifest↔tokens.css parity guard. `python3 -m unittest discover -s design-engine/tests` | **gate-grade** — scripts/check step 3 |
