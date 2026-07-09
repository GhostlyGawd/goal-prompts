# DX.md
*Produced by brief 14 · New-Dev Onboarding Audit, run against this repo (goal-prompts, v0.4). Part of the sample-report gallery.*

## Time-to-first-PR estimate
**20–30 minutes** for a brief contribution; the floor is genuinely low because the toolchain is `git`, `python3`, and a text editor.

## Stumble log
- **Clone → build**: `python3 build.py` works first try, zero dependencies — the table output doubles as a tour of the catalog. No stumble.
- **View**: opening `index.html` directly works (site is self-contained). No stumble.
- **Edit a brief**: front-matter format is documented in README; the linter catches skeleton violations with named errors. Confirmed by introducing a deliberate violation — the failure message names the file and rule. No stumble.
- **Stumble 1 — no single check command.** A contributor must know the full ritual: `python3 build.py`, then Node syntax-check of the extracted site script, then the MCP smoke test if `mcp/` changed. Nothing documents or bundles this; CI example covers only build + drift.
- **Stumble 2 — build.py has no tests of its own.** The linter is load-bearing and just demonstrated why: its first version miscounted lenses by reading Phase 4 report items (caught during 0.4 development, fixed by scoping to Phase 2). A regression here silently lowers the catalog's quality bar. Evidence: `lint()` in `build.py`, no `tests/`.
- **Stumble 3 — generated vs source dirs are learnable only by reading build.py.** `raw/`, `b/`, `index.html`, `catalog.json`, `checksums.txt`, and the archives are all regenerated; README doesn't say "never hand-edit these." A well-meaning PR editing `raw/30.md` would be silently clobbered.
- **Node requirement is optional but undeclared** — only `mcp/` work needs it; README implies nothing either way.

## Fixes
1. `scripts/check` running build + linter tests + JS check + MCP smoke; referenced in CONTRIBUTING and the CI example. SHIPPED in 0.5.
2. `tests/test_build.py` — SHIPPED in 0.5 with 12 cases, including the Phase-2 lens-scoping regression this audit named.
3. README "project layout" block marking generated paths — effort S (shipped in 0.4's README update).
4. One line in CONTRIBUTING: Node needed only for `mcp/` and site-script checks. SHIPPED in 0.5.

## The one-hour fix
Fix 1 shipped in 0.5: a single `scripts/check` command collapses the entire contribution ritual into one step and is now the CI body — every future contributor saves the discovery cost this audit paid. Remaining open: `j/k` keyboard navigation (self-hosting fonts shipped in 0.8).

**Backlog reconciliation (2026-07-09):** `j/k` keyboard navigation remains **DEFERRED** — it's purely additive and nothing in the catalog depends on it. Every other DX fix is shipped.

*Report only — which fixes should be made?*
