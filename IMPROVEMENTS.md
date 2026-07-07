# IMPROVEMENTS.md
*Produced by brief 00 · Product Improvement Discovery, run against this repo (goal-prompts, v0.4). Part of the sample-report gallery.*

## Product snapshot
Goal-prompts is a catalog of 46 audit briefs for coding agents, built as a static site from markdown sources by a zero-dependency Python build. Users are developers who copy a brief (site), install briefs as slash commands (installer), or let agents fetch them directly (raw URLs, conductors, MCP server). The journey: land on catalog → filter/search → copy or install → run in a repo → read the report → compose reports with brief 28. Underused assets: the reports the briefs produce (nothing consumes them besides brief 28) and the catalog's own git history.

## Top 5 quick wins
1. **Stemmed matching in suggest_briefs** — FIX · SHIPPED in 0.5 · `mcp/server.cjs` now stems query words (ing/ed/s) before substring matching and weights rare words above ubiquitous ones; "looping" ranks 32 first, verified by `scripts/mcp-smoke.cjs`.
2. **"Sample report" chips on audited cards** — NEW · SHIPPED in 0.5 · briefs carry an optional `example` field in front matter; the build plumbs it into `catalog.json` and the card renders a "sample report" chip. Live on 00/01/06/14/47.
3. **Self-host the two fonts** — IMPROVE · `template.html` loads Archivo and IBM Plex Mono from Google Fonts; offline and privacy-sensitive users get fallbacks. Vendor the woff2 files. Effort S.
4. **j/k keyboard navigation** — NEW · the site has `/` and ctrl-K for search but no way to move between cards without a pointer. Effort S.
5. **`scripts/check` one-command gate** — IMPROVE · SHIPPED in 0.5 · build + linter tests + JS syntax + MCP smoke in one script, now the body of the CI example.

## Top 3 big bets
1. **Publish the MCP server to npm and MCP directories** — today's `npx github:` install works but is undiscoverable; a registry listing is the distribution unlock. Blocked on npm credentials.
2. **Report-diff viewer** — brief 29 produces dated HEALTH.md scorecards; a page that accepts two runs and renders trend arrows would make the weekly loop visual. Evidence: HEALTH history-table format already stable by design.
3. **Community brief index** — surface briefs from forks (GitHub topic search) in an opt-in directory; the linter already defines the quality bar contributions must clear.

## Full list (remaining items)
- **IMPROVE · UX** — playbook conductor button only appears inside an active playbook view; also surface it on the playbook chips. Evidence: `render()` playbook branch in template.
- **NEW · Reach** — per-family conductor prompts ("run all Trust briefs"). SHIPPED in 0.5 · `build.py` emits `raw/family-<slug>.md` for every family and the card famhead has a "run all N" button; the MCP server adds `make_conductor` for arbitrary id lists.
- **IMPROVE · Trust** — `suggest_briefs` states its scoring method in results. SHIPPED in 0.5.
- **NEW · Engagement** — "surprise me": one-tap random brief, weighted toward families the run-tracker shows untouched.

## Sequence
Ship 1–2 (they harden what 0.4 just launched), then 5, then fonts; big bets start with npm publish the day credentials exist.

*Report only — which items should be built?*
