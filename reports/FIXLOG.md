# FIXLOG.md
*Produced by brief 47 · The Fixer, run against this repo (goal-prompts). Part of the sample-report gallery — this is the acting half of the catalog dogfooding itself: the reports at this root became the commits below. Newest session first.*

## Session — every finding, worked through (2026-07-26)
- Branch: `claude/product-engagement-stickiness-1cril7`
- Focus: the operator's "work through every finding" — all 8 findings from the
  same-day POLISH run (shipped earlier on this branch), all 32 findings from the
  fresh All-Craft run (DEFAULTS, PERCEIVED-SPEED, COMPOUNDING, SIGNATURE), and a
  full re-verification of the 18 defect-shaped legacy reports (~300 findings
  triaged against current code by 11 parallel read-only passes; the venture and
  strategy reports are analysis artifacts and were left out of fixing scope).
  Triage verdict on the legacy backlog: the overwhelming majority had already
  shipped in rounds R01–R66 — 26 items were still live, and all are closed below
  or declined with reasons. Every behavioral fix was verified in a real browser.

### Fixed (this round)
| Finding | Source | What shipped |
|---|---|---|
| Studio's GitHub loader blind to `reports/`, the product's own default output dir | DEFAULTS Q1 (S1) | loader lists `/contents/reports` beside the root; probe tries `reports/<name>` first |
| Repo ref asked twice, remembered never | DEFAULTS Q2 | `gp-repo` saved on success; prefills Studio, the landing analyzer, and Vitals |
| One-shot roadmap milestone permanently masked the stale-Vitals nudge | DEFAULTS Q3 + SIGNATURE M6/R2 | staleness outranks the milestone on landing + detail pages; both nudges dismissible (per-stale-period / forever) |
| Detail pages hid run state the device stores | DEFAULTS Q4 | "✓ run · 3d ago" chips beside CTAs and sequence steps |
| Browse gate re-asked a proven regular | DEFAULTS Q5 | any run mark boots into the catalog |
| Conductor copies dropped Operator context | DEFAULTS Q6 | ctx block rides `makeConductor()` and the playbook-page CTA |
| Fallback probe guessed 11 names while the catalog knows 157 | DEFAULTS Q7 | run-marked briefs' outputs probed first via catalog.json |
| `product` field blank after a call that carries it | DEFAULTS Q8 | repo description prefills it — only when empty, announced, editable |
| Coarse pointer lost the real next step | DEFAULTS Q9 | toast shows paste guidance AND the raw-URL bridge |
| Vitals had no fetch path | DEFAULTS Q10 | one-tap "refresh HEALTH.md from ⟨repo⟩" (reports/ first) |
| Hero copy frozen for the bodies.json download | SPEED W1 (S2) | synchronous "copying…" + aria-busy; feedback/fail restore |
| Warm cache bought returning visitors nothing (lie-fi worst case) | SPEED W2 (S2) | SW races network vs 2.5s timeout → cache; content-hash cache self-invalidates on deploy |
| GH load: flat "loading…" over 22 requests; 403 reported as "no reports" | SPEED W3 (S2) | phase narration on the button; rate limit named honestly |
| Step copy double-fetched and lost the copy on WebKit | SPEED W4 | disabled during fetch; gesture-synchronous ClipboardItem |
| Step copies polluted the /raw/ usage metric | SPEED W5 | steps source bodies.json; /raw/ stays the agents' endpoint |
| Quickstart hidden until full parse (6.2s at 40KB/s) | SPEED W6 + CRO NF1 + FUNNEL entry | server-rendered visible link at button weight beside the CTAs; JS upgrades in place |
| The ~15 min wait started unstated on the majority path | SPEED W7 | both toast forms name it |
| Quick view popped in two motions | SPEED W8 | min-height reserved while loading |
| Demo fetched 4 samples serially | SPEED W9 | parallel fetch, ordered add |
| The charter fed back only through conductors | COMPOUNDING C1 (S1) | charter line on every copy: both `withContext` twins |
| Weekly re-run wiped Studio triage | COMPOUNDING C2 (S2) | checks re-attach by normalized title across re-adds |
| Sequence builder: one unnamed slot, "destroy it" at the cap | COMPOUNDING C3 (S2) | named saves under `gp-seqs`; "your conductors" row under the storefront |
| Nothing stated what the user built | COMPOUNDING C4 (S2) | inventory line beside the export controls |
| Run history overwritten to one timestamp | COMPOUNDING C5 | capped `gp-runhist` array; "✓ run ×3" labels |
| Searches evaporated | COMPOUNDING C6 | recent-searches row, cap 5, saved only when a query found something |
| Nothing read FIXLOG.md back | COMPOUNDING C7 | briefs 29 + 46 credit fixed findings to their logged commits in the diff |
| The loop's proof moment was silent | SIGNATURE M1 | "N findings closed since the last load" receipt; fixed rows sink, dimmed, deduped |
| Vitals painted wins red | SIGNATURE M2 | lower-is-better map; unknown metrics honestly neutral |
| Vitals shipped half-open ([hidden] unpinned) | SIGNATURE M3 | Studio's one-line pin copied over |
| Single briefs ended as a file path, not a felt win | SIGNATURE M4 | "ranked list in plain words" bullet in all 157 briefs + linter rule + CONTRIBUTING grammar |
| First-copy toast was a four-path menu that never decayed | SIGNATURE M5/R1/R3 | first form: paste + what-next; decays to one line after the first run; Day-1 tee waits for proven intent |
| Debrief shape unpinned, could drift silently | SIGNATURE §2 | three-beat shape (ranked list · ask · handoff) pinned in the conductor test |
| Overclaim: "Every Goal Prompt is tested on this repo" | PROOF NF1 | rescoped to the playbook families whose reports are public |
| Studio events lacked the cohort ids | RETENTION §4 | same 8-line track() helper the other pages carry |
| Double-filled primaries on every generated page | HIERARCHY F1/F3 | nav CTA ghosted site-wide; Studio's drop/demo own the fill |
| Four inherited faux-bolds | TYPO T1 | real faces/weights (display 740, mono 600) |
| 29 half-pixel sizes + line-height sprawl regressed since round 3 | TYPO T3/T5 | re-folded to the round-3 map (visually indistinguishable) |
| Detail pages lacked disabled/press/link-affordance states | STATES S5/S6/S7 | three SITE_CSS rules; checkbox hover added |
| Tool navs bypassed width tokens, dropped links at 640px, off-scale pads | LAYOUT L1/L3/L4 | `--w-read`/`--gutter` navs; scroll-not-vanish links; 4pt-scale pads |
| Conductor gloss was tooltip-only; raw report .md indexable | COMPREHENSION F4 · SEO-8 | visible seqbar gloss; `/reports/(.*)` noindexed |
| Post-run failure was invisible | FUNNEL stall 4 | "no report? →" recovery line in #how, linked from every copy toast |
| Device-bound state, export buried | FUNNEL habit (c) | "export setup →" rides the welcome-back banner |

### Declined by design, with reasons
- **COLOR C7 (merge/retire family hues):** 24 families now share the hue wheel,
  but color stopped being the sole family signal when C8 shipped famchips
  (icon + name). Recoloring families is an identity decision ADR-12/13 reserve
  for the operator — flagged, not executed.
- **LAYOUT L5 (collapse 11 breakpoints to 3):** rewriting @media literals
  changes real behavior at in-between widths for near-zero user-visible payoff —
  fails the round-3 "no perceptible change" bar for value remaps.
- **LAYOUT L6 tail (map 14/18/26/34px onto the 4pt grid):** those maps ARE
  perceptible 2px shifts at dozens of call sites; the on-scale values are
  tokenized, the off-scale tail is documented instead of silently moved.
- **TYPO T3's aggressive half (a 5-step type scale in brand.json):** folding
  14/15/16 into one step shifts running text — same decline as round 3; the
  half-pixel defect itself is re-fixed.

### Ops-only remainder (no code path)
- Raw-fetch counting (FUNNEL §4.3/§4.4, RETENTION): enable the Vercel
  Observability filter on `pathname:/raw/` (+ commands archives) and date it in
  docs/usage-metrics.md — dashboard access only the operator has.
- SIGNATURE §2's gallery transcript: wants the debrief of a *real* external
  run, not a mockup — becomes available the first time one is captured.

## Session — open-items backlog, round 3 (2026-07-09)
- Branch: `claude/open-items-backlog-rm6wzx`
- Focus: build the "irreducible remainder" round 2 left behind — the spacing/type
  *value* remap and the "product seen working" visual — anything buildable without
  fabricating a credential or a fake media asset. Every change verified in headless
  Chromium at desktop + mobile, dark + light, with a hard rule: no *perceptible*
  visual change from the remaps (they were called "indistinguishable"; if a fold
  would actually shift what a reader sees, it wasn't done).

### Fixed (this round)
| Finding | Source | Verified by |
|---|---|---|
| Every half-pixel font-size folded to its nearest integer (69 decls; 11.5/12.5→12, 13.5→13, 14.5→14, 15.5/16.5→16, 9.5→10, 10.5→11) | TYPO T3 | Chromium: no size within 0.5px of another; landing/detail/studio unchanged |
| Near-duplicate line-heights folded (1.62/1.65→1.6, 1.55→1.5, 1.4→1.45, 1.03/1.04→1.05); 15→11 values | TYPO T5 | Chromium: leadings unchanged; survivors are per-role, not drift |
| 4pt spacing scale `--s1..--s9` + `--section`/`--section-tight` in `tokens.css`; section rhythm routed through them | LAYOUT L4 | build drift-free; Chromium: section gaps unchanged |
| Off-grid values snapped to grid (22px margin→`--s5`; 9px & 7px gaps→8; 35 decls) | LAYOUT L6 | Chromium: no visible reflow |
| Container ladder confirmed tokenized; grid caps left deliberate | LAYOUT L2 | `--w-page/--w-doc/--w-read` in use |
| **The product, seen working** — an animated *walk-through* of one real `/goal:bug-hunt` run ending on the real `BUGS.md` S2 finding, in the Proof section | SHOWCASE F1 | Chromium: plays on scroll; reduced-motion/no-JS shows final frame (all lines opacity 1); honest "not a screen capture" label |

### Honest about the remap
The audit's *aggressive* target (collapse ~27 sizes to a 9-step scale, folding
14/15/16→one 15) was **declined by design**: those full-pixel steps are perceptible
and folding them shifts running body text. What shipped removes the defect the audit
actually named — the six indistinguishable half-pixel pairs — and puts the off-grid
spacing on a real, tokenized scale, with zero perceptible change. That is the
correct, non-destructive reading of "map every value onto the scale."

### SHOWCASE F1 — built honestly, not faked
F1 asked to *see the product working*. The ideal asset is a real screen recording,
which this environment can't capture — and a *staged* screenshot/GIF would cut
against the site's own "Real reports, not screenshots" stance and reintroduce media
staleness. So instead of fabricating one, the Proof section now animates a
walk-through built **only from real content** (the real slash command, the real
four phases, the real `BUGS.md` finding), labeled "walk-through, not a screen
capture" in the header and caption. It's the honest proxy; a true recording remains
a nice-to-have for a maintainer with capture tooling.

### The one true remainder — a credential, not code
- **`npm publish` (IMPROVEMENTS 11).** The package is publish-ready and the
  Release-triggered workflow ships (`.github/publish.example.yml`); publishing is an
  irreversible, outward-facing action that requires an `NPM_TOKEN` this agent must
  not fabricate and is not authorized to run. It is one maintainer step (add the
  secret, cut a release) — deliberately left to a human, not an unbuilt item.

### Integration with the parallel product-visuals work
`main` had meanwhile merged a parallel implementation (#23) of the same backlog’s
"remainder" — a real Report Studio screenshot (`img/studio.png`), a real
finding→commit before/after, a mobile hero stat-block, retention R1–R4, and
credibility scaffolding (`CREDIBILITY.md`, maintainer credit, an armed adoption
badge). This branch was merged onto it as a **de-duplicated union**: overlapping
features (the retention R2 SW handler, export/import, the welcome-back banner, the
before/after) resolve to `main`’s tested version; this branch’s unique work (the
TYPO/LAYOUT value-remap, SHOWCASE F1, container tokens, ACTIVATION A2/A3, CRO
F1/F5, HIERARCHY F4) layers on top, and the value-remap was re-run over `main`’s
new code so its half-pixels fold too. The Proof section now shows the loop three
honest ways — animated walk-through (F1), real Studio screenshot (F2), real
finding→commit (F3). Verified: `scripts/check` green; exactly one of every
component (no duplication); mobile hero shows the injected 135/21/35; no console
errors. SHOWCASE F2/F5 and PROOF F5/F2 ledgers flipped to the now-live assets.

## Session — open-items backlog, round 2 (2026-07-09)
- Branch: `claude/open-items-backlog-rm6wzx`, restarted off `main` (`f03bc06`, the round-1 squash-merge)
- Focus: after round 1, take the "deferred" findings and build every one that's
  buildable and safe — including the design-judgment calls — with a default
  grounded in each audit's own recommendation, verified in headless Chromium.
  Left only what genuinely needs a human decision, a real media asset, or npm
  credentials.

### Fixed (this round)
| Finding | Source | Verified by |
|---|---|---|
| og.png regenerated to 135/21 + embedded PNG-metadata **drift guard** | SHOWCASE F7 | build fails if og.png's tEXt count ≠ catalog (proven) |
| Studio GitHub-repo input error state (red border + `aria-invalid`) | STATES S4 | Chromium: border `rgb(232,76,61)`, clears on edit |
| Guided next-step hint on copy, naming the brief's output file | ACTIVATION A1 | Chromium: toast "…writes `<OUTPUT>` at the root" |
| Feed the run-tracker from the copy hint ("✓ mark it run") | RETENTION R1 | Chromium: writes `gp-runs` at the moment of action |
| Tee up step 2 (Report Studio link) in the copy hint | ACTIVATION A5 | Chromium: hint links `/studio` |
| Resurface Operator context ("· tuned to <stack>") | RETENTION R4 | Chromium: badge shows the saved stack |
| Manual export/import of local setup (JSON, no backend) | RETENTION R3 | Chromium: round-trips `gp-runs`/`gp-ctx` |
| Decouple `--success`/`--warning`/`--danger` from family/brand hues | COLOR C2–C5 | Chromium: distinct crimson/green in both themes |
| Name the artifact in the hero eyebrow | COMPREHENSION F1 | "A free, open catalog of copy-paste audit prompts" |
| Gloss "brief"; hero offer line; unify start CTAs | COMPREHENSION F3 · CRO F1 · CRO F6 | Chromium |
| "New here? → Day-1 playbook" starter; "Start here" default way-in | ACTIVATION A2 · CRO F2 | Chromium: starter activates day1; badge + primary CTA |
| "See a real report →" link by the finder | ACTIVATION A4 | Chromium: link to `/examples/` |
| Partner contact CTA (routed to the repo's GitHub) | CRO F5 | Chromium: "Partner with us →" |
| Schematic mock text-alt + caption; empty-state → `--dim`; drop-zone border | SHOWCASE F4 · HIERARCHY F7/F3 | Chromium |
| act=red made a distinct, **documented** primary-action convention | HIERARCHY F6 | comment in `TOKENS_CSS` |
| Container tokens + unified gutter/line-height/nav-breakpoint | LAYOUT L1/L3 · TYPO T4 | Chromium: `.wrap` 1120/960/760 @ 24px |
| Kill the last faux-bold (`.drop-big` `--sans`@700 → `--disp`) | TYPO (new) | detail badge weight 600 |
| Fix: `.copyhint{display:flex}` overrode `hidden` → empty toast on load | (regression) | Chromium: hidden on load, shows on copy |

### Also built after the first round-2 pass
COLOR C2–C5 (semantic-colour separation); HIERARCHY F3/F4/F5/F6; COMPREHENSION
F1; CRO F1/F2/F5/F6/F7; ACTIVATION A2/A3/A4/A5; RETENTION R1–R5 (incl. the opt-in
PWA reminder and anonymous cohort analytics); LAYOUT L1/L3 + TYPO T4 (container/
gutter/line-height/nav-breakpoint tokens); SHOWCASE F3 (real inline before/after);
package.json 0.9.0→0.11.0 + a Release-triggered npm-publish workflow; and a
copy-hint show-on-load regression fix. Each verified in headless Chromium.

### The irreducible remainder
- **A dedicated, low-value refactor:** the full spacing/type *value* remap (TYPO
  T3/T5, LAYOUT L2/L4/L6) — its structural "define once" parts shipped (container/
  gutter/line-height/breakpoint tokens); the remaining value-by-value remap is
  what the audit itself calls the "deepest cleanup," with the half-steps
  "indistinguishable" (near-zero user benefit) and real regression + citation-
  restaleness risk. A deliberate pass, not a blind fold-in.
- **Needs a real media asset:** SHOWCASE F1 — a screen recording of an agent run,
  which can't be produced here (and cuts against the site's "real reports, not
  screenshots" stance). SHOWCASE F2's screenshot was declined for the same reason.
- **Needs a credential:** IMPROVEMENTS 11's actual `npm publish` — the automation
  now ships (`.github/publish.example.yml`); it runs once the maintainer adds an
  NPM_TOKEN secret and cuts a release.

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
