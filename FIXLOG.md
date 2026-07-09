# FIXLOG.md
*Produced by brief 47 · The Fixer, run against this repo (goal-prompts). Part of the sample-report gallery — this is the acting half of the catalog dogfooding itself: the reports at this root became the commits below. Newest session first.*

## Session — open-items backlog, round 2 (2026-07-09)
- Branch: `claude/open-items-backlog-rm6wzx`, restarted off `main` (`f03bc06`, the round-1 squash-merge)
- Focus: ship the round-1 "deferred" findings that are genuinely buildable, and kill the last concrete staleness (og.png).

### Fixed
| # | Finding | Source | Commit | Verified by |
|---|---|---|---|---|
| 1 | og.png regenerated to 135/21 + embedded PNG-metadata drift guard | SHOWCASE F7 | `53b9ce8` | build fails if og.png's tEXt count ≠ catalog (proven); render reads "135 briefs / 21 families" |
| 2 | Studio GitHub-repo input error state (red border + `aria-invalid`, clears on edit) | STATES S4 | `5eb61e1` | Chromium: border `rgb(232,76,61)` + `aria-invalid` on a bad ref |
| 3 | Guided next-step hint on copy, naming the brief's output file | ACTIVATION A1 | `5eb61e1` | Chromium: toast reads "…writes `<OUTPUT>` at the root", dismissable |
| 4 | Gloss "brief" on first use in the hero | COMPREHENSION F3 | `5eb61e1` | hero sub reads "a ready-made, copy-paste prompt" |
| 5 | Schematic report mock: real text alternative + visible caption | SHOWCASE F4 | `5eb61e1` | `role=img` + `aria-label`; `.mockcap` caption present |
| 6 | Zero-result empty state raised off `--faint` to `--dim` | HIERARCHY F7 | `5eb61e1` | computed color `rgb(183,184,190)` |
| 7 | Hero offer line leads with free / no-signup / local | CRO F1 | `5eb61e1` | `.micro` contains "no signup · nothing leaves your machine" |
| 8 | Nav "Get started" CTA unified onto `#catalog` | CRO F6 | (ledger commit) | both start affordances now lead to the catalog |

### Still deferred (need a human decision or an external asset — recorded in each report)
- Hero headline rewrite (COMPREHENSION F1); default-way-in and copyable-brief-near-hero (CRO F2/F7); partner contact CTA (CRO F5 — needs a real contact route); a "start here" default brief (ACTIVATION A2 — needs the maintainer's pick); retention features with local-first tradeoffs (RETENTION R1–R5); the hero A/B (ACTIVATION A3).
- Subjective visual-hierarchy + color-meaning changes (HIERARCHY F3–F6, COLOR C2–C8) and the type/spacing-scale systematization (TYPO T3–T5, LAYOUT L1–L6) — these are dedicated design-refactor passes, not fold-ins; doing them blind would risk the regressions the reports themselves warn about.

### Blocked (external, unchanged)
- SHOWCASE F1–F3 (product-in-action GIF, Studio screenshot, finding→commit before/after) — need real screen captures.
- IMPROVEMENTS 11 (npm publish + MCP-registry listing) — needs npm credentials.

## Session — open-items backlog (2026-07-09)
- Branch: `claude/open-items-backlog-rm6wzx` · off `main` (`b7d0988`)
- Reports consumed: the Design family (HIERARCHY, TYPOGRAPHY, COLOR, LAYOUT,
  STATES, BRAND) and the experience suite (COMPREHENSION, SHOWCASE, PROOF,
  RETENTION, ACTIVATION, CRO), plus DX — every finding given a disposition
  (FIXED / already-done / deferred / blocked) in its own report.
- Protocol: one finding per commit, `scripts/check` green after each;
  visual/interaction fixes verified in headless Chromium.
- Theme: the biggest debt was **staleness** — the public counts and much of the
  design backlog were already out of date, so this pass shipped the genuine
  remainder and reconciled every ledger.

### Fixed
| # | Finding | Source | Commit | Verified by |
|---|---|---|---|---|
| 1 | Inject live counts into static meta/OG/hero/chart | COMPREHENSION F2 · CRO F3 | `c8e6840` | index.html shows 135/35/21; no `__N_*__` left; browser hero reads 135/35 |
| 2 | README count + full 21-family taxonomy, build-guarded | COMPREHENSION F2 | `fb7ec0a` | build fails on a wrong count or missing family (proven) |
| 3 | CHANGELOG records the 6 Design briefs + 3 playbooks | staleness | `f9043df` | 135 briefs / 35 playbooks entry added |
| 4 | Keyboard focus rings restored on all text inputs | STATES S1–S3 | `7bbad5b` | Chromium: `.search input` shows a 2px ring on focus |
| 5 | `--faint` lifted to AA in both themes | COLOR C1 | `c749c75` | computed ≥4.5:1 on ink/panel/panel-2; #8B8D95 / #6A6C73 |
| 6 | Mono @700 faux-bold retargeted to shipped 600 | TYPO T1 | `63f35c1` | detail badge computed font-weight = 600 |
| 7 | Dead `--panel-3` token removed | COLOR C9 | `3eb8044` | 0 occurrences in tokens.css |
| 8 | Shared disabled/press states + link hover across landing+tools | STATES S5–S7 | `1d2498b` | Chromium: button:disabled opacity 0.5 |
| 9 | Canonical URL + SoftwareApplication JSON-LD | CRO F4 | `a6d29ab` | JSON-LD parses with live count; canonical present |
| 10 | Gloss MCP/conductor, label partner mock, surface checksum | COMPREHENSION F4/F5 · CRO F8 · PROOF F1/F6 | `56655aa` | Chromium: "example" label + "SHA-256 verified" present |
| 11 | Studio/Vitals brand mark aligned 22→24 | BRAND B5 | (ledger) | matches nav/detail canonical mark |
| 12 | Mobile horizontal overflow in the catalog finder | found in verify | `523f7b4` | Chromium: no page overflow at 390/360px |

### Already resolved by the earlier redesign (reconciled, not re-fixed)
- **TYPO T2** — unused `plexmono-500` was dropped in the font redesign (400/600 only).
- **BRAND B1–B4** — favicon is now the bar mark; `--radius` is one shared token;
  `og.py` renders in Schibsted/Plex; a `--r-sm/--r-md/--r-pill` scale exists.
- **HIERARCHY F1/F2** — the nav CTA is a ghost and cards promote the title (mobile pass).
- **COLOR C1 (dark)** — the palette redesign lifted dark faint most of the way; this
  pass finished it (light mode + `--panel-2`).

### Deferred (disposition recorded in each report)
- Subjective visual-hierarchy / color-meaning changes (HIERARCHY F3–F7, COLOR
  C2–C8) and type/spacing-scale systematization (TYPO T3–T5, LAYOUT L1–L6) —
  large, citation-shifting, design-judgment work best done as dedicated passes.
- Hero/CTA copy rewrites (COMPREHENSION F1/F3, CRO F1/F2/F6/F7) — wording is the
  maintainer's call.
- Product features with local-first tradeoffs (RETENTION R1–R5, ACTIVATION
  A1–A5), STATES S4 input-error state, `j/k` nav (DX) — buildable follow-ups.
- New minor issue found: `.drop-big` / Studio checkbox request `--sans` @700 where
  Plex Sans ships only 400/600 (a fresh faux-bold).

### Blocked (need assets/credentials this environment lacks)
- **SHOWCASE F1–F3** — product-in-action GIF, Studio screenshot, finding→commit
  before/after: need real screen captures.
- **IMPROVEMENTS 11** — npm publish + MCP-registry listing: needs npm credentials
  (unchanged from prior sessions).

### Follow-ups the fixes revealed
- With counts build-injected and README-guarded, `og.png` (a hand-made raster) is
  the last surface that can still misstate the catalog size — a build-time
  regeneration (Pillow) would close it.
- A fresh Color and Typography audit against the *current* dark+light palette
  would replace the pre-redesign COLOR/TYPO findings that now measure code that no
  longer ships.

## Session — 0.8 cycle (2026-07-07)
- Branch: `claude/product-improvement-discovery-7yhdyg` · off 0.7.0 (`97ad4fe`)
- Reports consumed: IMPROVEMENTS.md (the v0.7 re-run), plus carried-forward BUGS.md and SECURITY.md findings
- Protocol: one finding per commit, `scripts/check` green after each. Selection = the whole 16-item opportunity map.

### Fixed
| # | Finding | Source | Commit | Verified by |
|---|---|---|---|---|
| 1 | Share cards for briefs 46–67 + generator & build gate | IMPROVEMENTS 1 | `cba0db3` | `scripts/og.py` renders 22 cards; build fails on a missing `og/<id>.png` |
| 2 | Deep-link scroll clears the sticky toolbar | BUGS 3 | `f8ffa35` | `openFromHash` sets scroll-margin from measured toolbar height |
| 3 | Zero-result search → closest briefs + `search_zero` event | IMPROVEMENTS 3 | `c6d7083` | ported stem/rarity scoring; "looping" → 32 first, verified in node |
| 4 | Run tracker timestamps, staleness nudge, copy→run link | IMPROVEMENTS 4 | `7364947` | marks store `Date.now()`; "run · Nd ago"; stale-vitals nudge |
| 5 | Families injected by the build (kill 3-way sync) | IMPROVEMENTS 5 | `f3d313c` | `__FAMILIES_JSON__` derived from front matter; build fails on missing token |
| 6 | Self-host Archivo + IBM Plex Mono | SECURITY 4 | `224243d` | no `fonts.googleapis`/`gstatic` in built HTML; OFL license vendored |
| 7 | Studio loads reports from a GitHub repo | IMPROVEMENTS 7 (big bet) | `a4af75c` | repo-ref parser + report filter unit-tested; API + raw fallback |
| 8 | Report grammar defined; parsers lean on it | IMPROVEMENTS 9 (big bet) | `48fdcb0` | new lint rule + test; Studio surfaces impact chip |
| 9 | Venture dogfood (sourced Gut Check) | IMPROVEMENTS 8 (big bet) | `f5f9fc3` | 3 reports under `examples/venture/`; example chips on 62/63/67 |
| 10 | MCP version from package.json; 3-digit hash router | IMPROVEMENTS 12 · BUGS 4 | `683dff5` | smoke green; `^\d{2,3}$` |
| 11 | Conductor copy on playbook chips | IMPROVEMENTS 13 | `ab85d16` | ⧉ button fires `copy_conductor` from the chip |
| 12 | sitemap.xml + robots.txt from the build | IMPROVEMENTS 14 | `7af662e` | 71-URL sitemap; robots points at it; both follow `GOAL_PROMPTS_BASE` |
| 13 | Vitals Viewer (`/vitals`) for HEALTH.md history | IMPROVEMENTS 10 (big bet) | `82c6194` | table parser unit-tested; in the JS-syntax gate |
| 14 | Offline PWA via a generated service worker | IMPROVEMENTS 15 | `979b9f2` | content-hash cache version, deterministic; `node --check sw.js` |
| 15 | MCP package publish-ready (`files` allowlist, keywords) | IMPROVEMENTS 11 | `e2b1ebe` | `npm pack --dry-run` → lean ~150KB tarball |

### Skipped / partial
- **npm publish itself** (IMPROVEMENTS 11, big bet) — the package is now publish-ready but the actual `npm publish` and MCP-registry listing are blocked on npm credentials this environment doesn't have. Prep shipped; the publish is the one remaining manual step.
- **Community brief index** (prior IMPROVEMENTS big bet) — still a project, not a one-commit fix; not in this run's scope.

### Follow-ups the fixes revealed
- `scripts/og.py` needs Pillow — a heavier dep than the stdlib-only site build. It's a dev/generate-time tool (the build only *checks* cards exist), but worth a note in CONTRIBUTING if brief-adding contributors hit it.
- The Studio's GitHub loader and the report grammar (items 7–8) now make a report *schema validator* tractable — a natural next audit of the report format itself.
- Family colors still live in two places (`template.html` CSS + `scripts/og.py`); only order/questions got unified. A future pass could inject colors too.

## Session — 0.5 cycle (2026-07-07)
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
