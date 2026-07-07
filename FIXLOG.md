# FIXLOG.md
*Produced by brief 47 · The Fixer, run against this repo (goal-prompts) during the 0.5 cycle. Part of the sample-report gallery — this is the acting half of the catalog dogfooding itself: the reports at this root became the commits below.*

## Session
- Date: 2026-07-07 · branch: `v0.5-round` · off 0.4.0 (`d041b3f`)
- Reports consumed: IMPROVEMENTS.md, SECURITY.md, DX.md
- Protocol: one finding per commit, the repo's own `scripts/check` run green after each

## Fixed
| Finding | Source | Commit | Verified by |
|---|---|---|---|
| Stemmed + rarity-weighted `suggest_briefs` | IMPROVEMENTS quick win 1 | `c5fd25c` | `scripts/mcp-smoke.cjs` — "looping" ranks 32 first |
| Sample-report chips on audited cards | IMPROVEMENTS quick win 2 | `3bd1a9f` | build emits `example` into catalog.json; chip renders on 00/01/06/14/47 |
| Per-family conductors ("run all Trust") | IMPROVEMENTS full-list | `3a9f517` | 15 `raw/family-*.md` written; "run all N" button on each family |
| `suggest_briefs` states its scoring method | IMPROVEMENTS full-list | `c5fd25c` | method line present in tool output (asserted in smoke) |
| Linter tests, incl. Phase-2 lens scoping | DX fix 2 | `6a56976` | `python3 -m unittest discover -s tests` — 12 pass |
| `scripts/check` one-command gate + smoke | DX fix 1 · IMPROVEMENTS 5 | `49ef1d8` | `scripts/check` runs build + tests + JS syntax + MCP smoke |
| Baseline security headers | SECURITY finding 3 | `8e8d57d` | nosniff · Referrer-Policy · frame-ancestors in vercel.json |
| Node-requirement note in CONTRIBUTING | DX fix 4 | `8d1c81b` | CONTRIBUTING names `scripts/check`; Node only for mcp/ + site scripts |

These eight fixes were selected from the reports; the same cycle also shipped
features that were not fix-findings (the Act family and briefs 48–53, the
Report Studio, `make_conductor`, and `GOAL_PROMPTS_BASE` fork support), committed
separately.

## Skipped (findings deliberately not taken this cycle)
- **Self-host the two fonts** — SECURITY finding 4 / IMPROVEMENTS quick win 3 / DX. Effort M and a genuine tradeoff (offline + privacy vs. a build-time font pipeline); left open for its own change.
- **j/k keyboard navigation** — IMPROVEMENTS quick win 4. Additive, no report depends on it.
- **Deep-link scroll-margin under the sticky toolbar** — BUGS finding 3 (BUGS was not in this run's consumed set; belongs to a Fixer pass over BUGS.md).
- **Three-digit hash router** — BUGS finding 4, forward-compat only (ids reach 53; the cap bites at 100).
- **npm publish, report-diff viewer, community index, "surprise me"** — IMPROVEMENTS big bets / engagement; scoped as projects, not one-commit fixes.

## Follow-ups the fixes revealed
- The rarity weighting is deliberately clamped (df floor 5) so a single vivid tagline can't dominate; worth revisiting if the catalog grows past ~100 briefs, where true IDF would behave differently.
- `scripts/check` now defines the contribution contract end to end — a natural home for a future link-checker over the `example` and `raw` URLs.
- With the Studio consuming reports and 47 consuming reports, the report format itself is now load-bearing; a light report schema could make both parsers stricter.

*Report only — which of the skipped findings should the next Fixer run take?*
