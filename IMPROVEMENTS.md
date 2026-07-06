# IMPROVEMENTS.md
*Produced by brief 00 · Product Improvement Discovery, run against this repo (goal-prompts, v0.4). Part of the sample-report gallery.*

## Product snapshot
Goal-prompts is a catalog of 46 audit briefs for coding agents, built as a static site from markdown sources by a zero-dependency Python build. Users are developers who copy a brief (site), install briefs as slash commands (installer), or let agents fetch them directly (raw URLs, conductors, MCP server). The journey: land on catalog → filter/search → copy or install → run in a repo → read the report → compose reports with brief 28. Underused assets: the reports the briefs produce (nothing consumes them besides brief 28) and the catalog's own git history.

## Top 5 quick wins
1. **Stemmed matching in suggest_briefs** — FIX · evidence: `mcp/server.cjs score()` uses raw substring `indexOf`; the smoke test query "looping" failed to match bodies containing "loop", ranking 41 above 32. Strip common suffixes (ing/ed/s) before matching. Effort S.
2. **"Sample report" chips on audited cards** — NEW · briefs 00/01/06/14 now have real output at repo root; the cards don't link to it. Add an `example` field to `catalog.json` and a chip in `template.html`. Effort S.
3. **Self-host the two fonts** — IMPROVE · `template.html` loads Archivo and IBM Plex Mono from Google Fonts; offline and privacy-sensitive users get fallbacks. Vendor the woff2 files. Effort S.
4. **j/k keyboard navigation** — NEW · the site has `/` and ctrl-K for search but no way to move between cards without a pointer. Effort S.
5. **`scripts/check` one-command gate** — IMPROVE · see DX.md; build + JS syntax + MCP smoke in one script, reused by CI. Effort S.

## Top 3 big bets
1. **Publish the MCP server to npm and MCP directories** — today's `npx github:` install works but is undiscoverable; a registry listing is the distribution unlock. Blocked on npm credentials.
2. **Report-diff viewer** — brief 29 produces dated HEALTH.md scorecards; a page that accepts two runs and renders trend arrows would make the weekly loop visual. Evidence: HEALTH history-table format already stable by design.
3. **Community brief index** — surface briefs from forks (GitHub topic search) in an opt-in directory; the linter already defines the quality bar contributions must clear.

## Full list (remaining items)
- **IMPROVE · UX** — playbook conductor button only appears inside an active playbook view; also surface it on the playbook chips. Evidence: `render()` playbook branch in template.
- **NEW · Reach** — per-family conductor prompts ("run all Trust briefs"); generation is 5 lines in `build.py` since `conductor()` already takes any id list.
- **IMPROVE · Trust** — `suggest_briefs` should state its scoring method in results (it does in the tool description; repeat in output).
- **NEW · Engagement** — "surprise me": one-tap random brief, weighted toward families the run-tracker shows untouched.

## Sequence
Ship 1–2 (they harden what 0.4 just launched), then 5, then fonts; big bets start with npm publish the day credentials exist.

*Report only — which items should be built?*
