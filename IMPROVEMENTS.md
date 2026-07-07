# IMPROVEMENTS.md
*Produced by brief 00 · Product Improvement Discovery, run against this repo (goal-prompts, v0.7). Supersedes the v0.4 sample run; part of the sample-report gallery.*

## Product snapshot
Goal-prompts is a catalog of 68 audit briefs for coding agents — each a <4k-char prompt that runs a 4-phase audit (Explore → Audit → Curate → Report) and leaves one evidence-backed report at the target repo's root. It is built as a static site by a stdlib-only Python build (`build.py`) from markdown sources, with five ways in: the catalog UI (`index.html`), slash-command installer (`install`), stable raw URLs + conductors (`raw/`), a zero-dependency MCP server (`mcp/server.cjs`), and the machine index (`catalog.json`). Users are developers running Claude Code (or any agent) on their own repos. The journey: land on catalog → filter/search → copy a brief (optionally aimed via the operator-context box) → run it in a repo → drop the reports into Report Studio (`/studio`) → tick findings → the generated 47 · Fixer prompt turns them into commits, logged in FIXLOG.md. Retention machinery exists but is thin: a localStorage run tracker with a nudge toward brief 28 after five runs, and the Weekly Vitals playbook (brief 29) that implies a weekly habit nothing in the product actually supports. The most underused assets: the search/suggest scoring that exists only server-side in `mcp/server.cjs`, the run tracker's data (booleans, no dates), and the newest flagship family (Venture, 60–67) which ships with zero sample output.

## Opportunity map

| # | Item | Tag | Impact | Effort |
|---|---|---|---|---|
| 1 | OG images for briefs 46–67 (+ generator in build) | FIX | H | S–M |
| 2 | Deep-link scroll hides under sticky toolbar | FIX | M | S |
| 3 | Zero-result search: suggest + log the miss | IMPROVE | H | S |
| 4 | Run tracker: timestamps, staleness, copy→run link | IMPROVE | H | S |
| 5 | Inject FAMILIES from build (kill 3-way sync) | IMPROVE | M | S |
| 6 | Self-host the two fonts | IMPROVE | M | M |
| 7 | Studio: load reports straight from a GitHub repo | NEW | H | M |
| 8 | Venture sample reports in the gallery | NEW | H | M |
| 9 | Report schema shared by briefs / Studio / Fixer | IMPROVE | H | M–L |
| 10 | HEALTH.md report-diff viewer (Weekly Vitals loop) | NEW | M | L |
| 11 | npm publish + MCP registry listing | NEW | H | S (blocked) |
| 12 | MCP server version read from package.json | FIX | L | S |
| 13 | Conductor copy on playbook chips | IMPROVE | M | S |
| 14 | sitemap.xml + robots.txt from the build | NEW | M | S |
| 15 | Offline PWA (service worker; studio manifest link) | IMPROVE | M | M |
| 16 | Hash router caps at two-digit ids | FIX | L | S |

## Top 5 quick wins
1. **OG images for the 22 newest briefs** — FIX · UI/Reach. `og/` holds `00.png`–`45.png` (46 files) but briefs run to 67; every `b/<id>.html` for the Act, Design, Venture families and briefs 48–53 references a 404 image (`b/46.html` → `/og/46.png`). Share pages are the viral surface — right now the newest, most differentiated families unfurl broken. Root cause is felt debt: OG generation isn't in `build.py`, so new briefs ship without cards. Generate the 22, and add a check (or generator) to the build so it can't regress.
2. **Zero-result search that helps and learns** — IMPROVE · Helpfulness/Data. `matches()` in `template.html` is AND-substring; the empty state says only "try another word." Meanwhile `mcp/server.cjs` already has stemmed, rarity-weighted scoring (`stem()`, `rarity()`, `score()`). Port it into the page as a "closest matches" fallback, and fire a `search_zero` analytics event with the query — missed searches are the purest demand signal for which brief to write next (analytics events exist for every copy action but nothing instruments search).
3. **Deep-link scroll fix** — FIX · UX. BUGS.md finding 3, open since v0.4: `.card{scroll-margin-top:120px}` (template.html:153) vs a sticky toolbar that wraps to ~180px on narrow screens, so `/#30` from a share link opens with the card top hidden. One CSS value (or set it from measured toolbar height). Share links are the entry point the `b/` pages exist to serve.
4. **Run tracker grows a memory** — IMPROVE · Retention. `runs[id]` is a boolean (template.html:400–403); "mark run" is fully manual and disconnected from Copy. Store a timestamp instead (truthy, so backward compatible), render "run 12d ago" on marked cards, nudge when Weekly Vitals (29) is stale by more than a week, and after a Copy flip the button to "ran it? mark it". This turns the only per-user data the product has into the habit loop brief 29 promises.
5. **Families defined once** — IMPROVE · Felt debt. Family order + questions live in `build.py` (FAMILY_ORDER), again in `template.html` (FAMILIES array), and colors a third time in CSS — CLAUDE.md itself warns "keep them in sync." The build already injects `__PROMPTS_JSON__`/`__PLAYBOOKS_JSON__`; add `__FAMILIES_JSON__` and delete the duplicate. Adding family #18 becomes a one-file change.

## Top 3 big bets
1. **Report Studio loads reports straight from GitHub** — NEW · Synergy/UX. Today the Studio requires downloading `.md` files and dropping them in (studio.html drop/paste wiring, lines 475–509), but the reports the briefs produce live at repo roots on GitHub. A "load from repo" input fetching `raw.githubusercontent.com/<owner>/<repo>/<branch>/{IMPROVEMENTS,BUGS,SECURITY,…}.md` (CORS-open, still zero backend) removes the last manual step in the product's core loop: audit → reports → Studio → Fixer. The demo button already proves the fetch-and-parse path works for same-origin files.
2. **A light report schema, then lean on it** — IMPROVE · Synergy. FIXLOG.md's own follow-up: with the Studio parser (`parseReport`, studio.html:243–274) and brief 47 both consuming reports, the report format is load-bearing but only conventionally defined — the parser guesses severity from regex over free text. Specify the finding shape (bold title · severity · effort · tag) in each brief's Phase 4, teach the linter to enforce it on the briefs' own report templates, and the Studio parser gets stricter, the Fixer gets safer, and item 10 (diff viewer) becomes tractable. This compounds every other surface.
3. **Publish the MCP server + dogfood the Venture family** — NEW · Reach/Trust. Distribution: `npx github:` works but is undiscoverable; npm + MCP-registry listings are the unlock (carryover, blocked on credentials — smallest real step: publish once, automate later). Trust: Venture (60–67) now *opens* the catalog yet has no sample output — the gallery (`examples/index.html`) covers only the Day-1 run, and `example:` front matter exists on just 00/01/06/14/47. Run the Gut Check playbook (62·63·67) on one real niche and add the three reports; the family's "every claim carries a source and date" rule is exactly what a skeptical first-time visitor needs to see demonstrated.

## Full list (remaining items)
- **6 · Self-host Archivo + IBM Plex Mono** — IMPROVE · Trust/Reach. Open across three reports (SECURITY-4, old IMPROVEMENTS QW3, DX); `template.html:18–20` and `studio.html:17–19` still hit Google Fonts — the site's only runtime third-party dependency, and the blocker for real offline. Effort M · Impact M · Risk: font-file licensing hygiene (both are OFL).
- **10 · HEALTH.md diff viewer** — NEW · Retention. Brief 29 emits dated scorecards designed for trend arrows; nothing renders two runs side by side. A `/vitals` page (same client-side pattern as Studio) that accepts two HEALTH.md files and shows deltas makes the weekly loop visible. Effort L · Impact M · Risk: depends on item 9 for stable parsing.
- **12 · MCP version duplication** — FIX · Felt debt. `mcp/server.cjs:272` hardcodes `"0.7.0"`, duplicating `package.json:3`; they will drift. `require("../package.json").version`. Effort S · Impact L.
- **13 · Conductor on playbook chips** — IMPROVE · UX. Carryover: the copy-conductor button renders only inside the active playbook view (`render()` playbook branch, template.html:673–679); the chips themselves (`buildPbs`) offer no one-tap copy. Effort S · Impact M.
- **14 · sitemap.xml + robots.txt** — NEW · Reach. 68 share pages, `/studio`, `/examples/` — and nothing tells crawlers. `build.py` already knows every URL; emit both files in the same pass. Effort S · Impact M · Risk: none.
- **15 · Offline PWA** — IMPROVE · Reach. `manifest.json` declares standalone display and icons, but there's no service worker, and `studio.html` doesn't even link the manifest. The site is fully self-contained once fonts are local (item 6) — a ~30-line cache-first worker makes the whole catalog work on a plane. Effort M · Impact M · Risk: cache invalidation on deploys; version the cache with the build.
- **16 · Three-digit hash router** — FIX · Felt debt. BUGS-4 carryover: `openFromHash()` regex `^\d\d$` (template.html:718) breaks at id 100; the catalog grew 30→68 in one week. `^\d{2,3}$` now, while it's one character. Effort S · Impact L.

## Sequence — if only 3 ship first
1. **OG images 46–67 (item 1)** — the only thing broken today on a sharing surface; every Venture/Design share link currently unfurls with a dead image, and those are the families you'd share.
2. **Zero-result suggest + `search_zero` event (item 3)** — reuses code the repo already has, fixes the one dead end in the catalog UX, and starts collecting the demand data that should drive which briefs get written next.
3. **Studio GitHub loader (item 7)** — the biggest friction cut in the core loop; after it, "run a playbook, open Studio, point it at the repo, copy the Fixer" is end-to-end without leaving the browser.

*Report only — which items should be built?*
