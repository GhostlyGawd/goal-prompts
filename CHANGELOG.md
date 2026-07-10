# Changelog

## 0.13.0 — 2026-07-10
- Growth remediation pass: an 11-stage growth-conductor run against this
  repo's own surfaces (Funnel, Competitive, Revenue, AI, SEO, CRO, Retention,
  Proof, Activation, Forms, Checkout — all reports in the repo root) was
  synthesized into `ROADMAP.md` and shipped as one branch:
  - **Honest measurement:** copying a brief no longer auto-marks it as run —
    only the hint's explicit "✓ mark it run" and the card toggle record runs;
    funnel events (`catalog_reached`, `quickview_open`, `examples_viewed`,
    `copy_install`, `mark_run`, reminder round-trips) ride a shared `track()`
    with attribution; `raw/` and `prompts/` are noindexed so raw fetches stay
    a clean usage metric; the stale no-analytics line in the usage-metrics
    doc corrected.
  - **Handoff fixes:** plugin install rendered as numbered copyable steps on
    the landing and all 141 `b/` pages; every copy control is success-gated
    (a failed clipboard write shows an "open raw" link instead of a false
    "Copied"), coarse-pointer devices get a `/raw/<id>.md` bridge; conductor
    copies name the reports they write; the detail-page hint tees up Report
    Studio.
  - **Trust & honesty:** offer/risk-reversal micro-line on all 176 detail
    pages (honesty-forked for the Fixer); the hero dogfood claim rescoped to
    be literally true per leg, linter-enforced; an analytics disclosure
    naming Vercel Analytics and exactly what's counted; merchandising window
    chips gated by the viewer's clock (no stale "January drop" in July); the
    XSS evidence card repointed at a verifiable BUGS.md finding.
  - **Detail-page parity:** all 176 `b/`/`p/` pages get the landing's
    analytics, success-gated copy events, and a dismissible welcome-back
    strip; per-URL sitemap lastmod from a content-hash state file; og/
    twitter/canonical tags completed across studio, vitals, and /examples/.
  - **Retention circuit closed:** the Vitals Viewer is now linked from every
    place that mentions Weekly Vitals; the opt-in reminder is staleness-aware
    (skips if Vitals ran <7 days ago, gated in the service worker and covered
    by a Node suite); a PWA install offer where periodic sync needs it;
    `/changelog` rendered from this file; "make it a standing appointment"
    links to the scheduled-run workflow at the mark moment.
  - **Forms integrity:** Studio pastes infer a report name from the markdown
    and never silently overwrite; all five destructive actions use the same
    two-step arm pattern; `role=status` live regions and error states on
    every async input; fuzzy zero-state search fallback (distance-1) in
    catalog core.
  - **SEO structural:** the homepage ships a static crawlable catalog (141
    brief + 35 playbook links) that JS hydrates on boot; brief bodies moved
    out of the inline payload to a precached `bodies.json` — index.html
    drops 595k → 231k raw (61% lighter); 35 per-playbook OG cards with a
    build-time drift guard; JSON-LD (BreadcrumbList + HowTo / ItemList) on
    all 176 detail pages.
  - **Distribution:** a `skills/` output tree (one SKILL.md per brief);
    `BRIEF=<id|slug>` single-brief installer (SHA-verified, hermetically
    tested) with a per-brief install line on `b/` pages; a native
    `cursor-commands.zip`; the Brief Forge authoring meta-prompt quoting the
    linter's literal rules (drift-tested); Studio gains **Copy Synthesis
    prompt** beside the Fixer; a build-generated `/quality` page explaining
    why the briefs don't rot, every claim evidence-linked.
  - **Revenue rails, honest:** `/teams` and `/partners` pages productizing
    only what exists today (fork support, standing-audit action, plugin/MCP/
    skills distribution) with pricing "on request"; both partner CTAs
    unified on a working GitHub issue template; a post-activation backer
    nudge shipped dark until a real backer URL exists.
  - **Design system:** one severity ramp in the token source consumed by
    Studio chips and the landing run-replay (AA text contrast in both
    themes, measured); API and Reliability family hues de-collided with a
    test-pinned minimum distance across all 21 families; motion tokens named
    once; `j`/`k` keyboard navigation over visible catalog cards; family
    chips on cards where color was the only family signal.

## 0.12.0 — 2026-07-09
- End-to-end remediation pass across every layer, driven by a full review:
  - **Linter & contract guards:** numeric id ordering; new build-failing rules
    for duplicate/reserved output filenames, id/filename drift, id format,
    `example:` targets, `related:` ids, tagline quoting, and family icon
    coverage. Brief contract hardened repo-wide: dated re-run-aware Phase 4,
    an optional `reports/` directory for clean roots, and a null-report escape
    for briefs whose subject can be absent — all linted, permanently.
  - **Brief content:** 46 Audit Triage routes all 21 families; disambiguation
    pointers across every confusion cluster (07↔85, 05↔123, 08↔86, …); the six
    weakest briefs rewritten to the house standard; `example:` links to the
    real dogfood reports; six new audits — 135 CLI Tool UX, 136 Library API
    Design, 137 Infra-as-Code, 138 Event Contracts, 139 Data Pipeline Quality,
    140 Caching Strategy. **141 briefs.**
  - **MCP & conductors:** id normalization (`get_brief("6")` works), honest
    error ranges, a `list_playbooks` tool, the MCP **prompts** capability
    (every brief in your client's prompt picker as `goal-<slug>`), stemmer and
    word-boundary matching fixes, and conductor stage-isolation + fetch-fallback
    + reports/ awareness — kept identical across build.py, server.cjs, and the
    site by a parity guard in the smoke test.
  - **Distribution:** a Claude Code plugin as the primary install
    (`/plugin marketplace add GhostlyGawd/goal-prompts` → real `/goal:bug-hunt`
    names), generated from the briefs at build time; the curl installer gains a
    checksum fallback chain, stale-file removal, a `.version` stamp, and a
    hermetic test; CI workflow activated with an airtight rebuild-drift check;
    a ready-to-copy scheduled run-brief workflow; usage-metrics design doc.
  - **Landing page:** ranked live search, a 3-question picker, per-repo
    recommendations from a public GitHub repo, honest dogfood evidence tiles
    replacing paraphrased quotes, toolbar diet, Audit Triage callout, lazy
    quick-views and client-composed conductors (smaller page), and an
    a11y/mobile batch.
  - **Studio, theme, detail pages:** the report parser extracted to
    `js/report-parser.js` and made truthful under test — ###-titled findings
    parse, severity/fixed read only from label positions, code fences are
    inert, unrecognized blocks are counted and disclosed; bulk severity chips,
    post-copy guidance, and share-selection permalinks; an OS-light default
    theme with family accents darkened to ≥3:1 in light mode; detail pages get
    saved-context copies, `related:` cross-links, and per-step playbook copy.
  - **Tests:** the Python linter suite grew 25 → 65 tests, plus three Node
    suites (catalog core, report parser, MCP smoke + parity) and the hermetic
    installer test — all wired into `scripts/check` and CI.
- Open-items backlog pass — accessibility, activation, and anti-staleness fixes
  drawn from the self-audit report gallery:
  - **Accessibility:** keyboard focus rings restored on every text input; the
    `--faint` text tier lifted to WCAG AA in both themes; mono/sans faux-bold
    eliminated; a real text alternative for the schematic report mock; the
    Studio's GitHub-repo input now shows an error state on a failed load.
  - **Activation & clarity:** copying a brief now shows a guided next-step hint
    naming the report file it writes; the hero names the artifact ("a
    ready-made, copy-paste prompt") and leads with the free / no-signup / local
    offer; "MCP" and "conductor" are glossed; the partner band is labeled an
    example; the installer's SHA-256 verification is surfaced at the install line.
  - **Anti-staleness:** every public brief/playbook/family count is injected from
    the catalog (meta, OG, hero, chart, and the `og.png` share card), and the
    build now fails if the README, family taxonomy, or `og.png` count drift.
  - **Also:** a mobile horizontal-overflow fix in the catalog finder; canonical
    URL + `SoftwareApplication` JSON-LD; shared disabled/press states; and a
    per-finding disposition recorded in every design/experience report.
  - **Design-system systematization:** a 4pt spacing scale (`--s1..--s9`,
    `--section`/`--section-tight`) added to the token source; every half-pixel
    font size folded to its nearest integer and the biggest off-grid gaps/margins
    snapped to the grid (all imperceptible — TYPO T3/T5, LAYOUT L2/L4/L6); and the
    Proof section gains an honest animated *walk-through* of one real `bug-hunt`
    run ending on the real `BUGS.md` finding — reduced-motion-safe and explicitly
    labeled "not a screen capture" (SHOWCASE F1).
  - **Product proof & credibility (integrated):** a real Report Studio screenshot
    captured from the live tool, a real finding→commit before/after, a mobile hero
    stat-block, retention (copy-marks-a-run, welcome-back banner, export/import,
    opt-in weekly reminder), a maintainer credit, and an armed adoption badge that
    turns on only once GitHub stars are real (SHOWCASE F2/F3/F5, PROOF F2/F5,
    RETENTION R1–R4). No social proof is fabricated.
- Mobile landing-page pass. The page ran ~8 phone-screens of marketing
  before the catalog, and the filter bar overflowed on phones:
  - **Hero** drops the briefs-per-family chart on phones (it only scrolled
    sideways and delayed the value) and leads with the promise + one
    primary action; the nav "Get started" is demoted to an outline so a
    single filled CTA wins per viewport (Hierarchy audit F1).
  - **Catalog filter bar** is now opaque when pinned — cards no longer
    bleed through its transparent lower edge — and the 21 family + 30
    playbook chips collapse into single swipeable rows instead of ~8
    stacked rows.
  - **Funnel:** the playbook storefront moves below the catalog, so the
    catalog is reachable in roughly half the scroll. Its entry points
    still live in the catalog's "start with a goal" chips and filter row.
  - **Catalog cards** demote the brief id and promote the title (Hierarchy
    audit F2), and the footer drops the how-to-use steps and second
    install box that duplicated "Three ways in".
- Visual identity refresh: a **light theme** alongside the dark one (a header
  toggle; the choice persists in `localStorage`), self-hosted full-coverage
  Schibsted Grotesk (display) + IBM Plex Sans (UI) replacing Archivo, and every
  brand asset — OG cards, home share card, PWA icons, manifest, favicons —
  unified on the `#131417` ink and the 4-bar mark. Design tokens now live in one
  source (`tokens.css`) linked by every surface. (An earlier build shipped the
  webfonts accidentally ASCII-subset, so the live site fell back to system
  fonts; the full subsets fix that.)
- Six UI/UX Design briefs, each the standard read-only 4-phase audit:
  129 Navigation & Wayfinding, 130 Menu & Command Surface, 131 Data
  Visualization, 132 Dashboard & Density, 133 Empty & Zero-Data States,
  134 Iconography & Visual Language — plus three design playbooks: Wayfinding
  (129 → 130 → 54 → 104), Make Data Legible (131 → 132 → 54 → 56), and Total
  UI Overhaul (129 → 130 → 58 → 133 → 134 → 47). 135 briefs, 35 playbooks
- Self-audit sample-report gallery expanded: the Design family run against this
  repo (HIERARCHY, TYPOGRAPHY, COLOR, LAYOUT, STATES, BRAND) and the experience
  suite (COMPREHENSION, SHOWCASE, PROOF, RETENTION, ACTIVATION) — read-only
  audits of goal-prompts' own surfaces, dogfooded.

## 0.11.0 — 2026-07-08
- Forty-eight briefs and four new families, taking the catalog to 129
  briefs across 21 families — each the standard read-only 4-phase audit
  that leaves one evidence-backed report:
  - Security suite (Trust): 81 Secrets & Credential Hygiene, 82 Access-
    Control & Authorization, 83 Input & Injection, 84 Threat Model &
    Abuse Cases; plus 85 Dependency Currency and 86 Keyboard & Screen-
    Reader Flow
  - Speed: 87 Query Performance & N+1, 88 Bundle & Asset Weight
  - Data: 89 Data Integrity, 90 Metric Definition Consistency
  - Ops: 91 Backup & Recovery, 92 Feature-Flag & Rollback Readiness,
    93 Vendor Lock-In
  - DX suite (Team): 94 Inner-Loop Speed, 95 Debuggability, 96 CI
    Feedback-Loop; plus 97 Decision-Record
  - Quality: 98 Concurrency & Race-Condition, 99 Type-Safety, 100 Test-
    Quality, 101 Flaky-Test, 102 Test-Pyramid Balance
  - 103 Error-Message (Clarity); 104 Mobile & Responsive and 105 Design-
    Token Adoption (Design); 106 Notification & Email, 107 In-App Search,
    108 Account Lifecycle (Product); 109 Forms & Validation, 110 Checkout
    & Payment (Growth)
  - API (new family): 111 Webhook Design, 112 SDK Ergonomics, 113 API
    Versioning & Deprecation, 114 Rate-Limit & Quota Design, 115 Developer
    Portal & Onboarding
  - AI-Ethics (new family): 116 Bias & Fairness, 117 Hallucination &
    Grounding, 118 Prompt-Injection Red-Team, 119 Model Transparency,
    120 Training-Data Provenance
  - Reliability (new family): 121 Graceful Degradation, 122 Failure-
    Injection Readiness, 123 Capacity & Scalability, 124 Abuse & Overload
    Protection
  - Compliance (new family): 125 Consent & Cookie, 126 Data-Subject-
    Rights, 127 Encryption & Key Management, 128 Audit-Trail
- Fifteen playbooks: Harden Before Ship, Data-Layer Tune-Up, DX Tune-Up,
  Test Confidence, Ship a Public API, Responsible AI Review, Production
  Resilience, Privacy & Compliance, Make It Fast, Inherit a Codebase,
  Refactor Safely, Cost Down, Agent Cost Control, plus a themed (New-Year
  Reset) and a sponsored (Sponsored Speed Bundle) merchandising example.
  129 briefs, 32 playbooks

## 0.10.0 — 2026-07-08
- Five briefs that optimize the whole visitor experience — comprehension,
  visual proof, conversion credibility, retention, and activation — each
  the standard read-only 4-phase audit that leaves one evidence-backed
  report:
  - 76 Comprehension Audit (Clarity): does a newcomer form the right
    mental model — what it is, who it's for, how it works — from the first
    screen, or does the curse of knowledge win — writes COMPREHENSION.md
  - 77 Show, Don't Tell (Design): are benefits and mechanics shown —
    screenshots, demos, diagrams, before/after — or asserted in prose the
    visitor must take on faith — writes SHOWCASE.md
  - 78 Retention & Lifecycle Audit (Growth): the return trip — saved
    state, resurfaced value, well-timed nudges, and the churn cliffs that
    quietly lose users — writes RETENTION.md
  - 79 Social Proof & Credibility (Growth): the testimonials, logos,
    counts, and guarantees that turn a skeptical stranger into a believer,
    placed where the decision is made — writes PROOF.md
  - 80 Activation & First-Win Audit (Growth): the first session from empty
    account to first win, and the inspiring next step that seeds a habit —
    writes ACTIVATION.md
- One playbook: Experience Optimization (76 → 77 → 75 → 79 → 80 → 78 → 47),
  the get-it/want-it/keep-it arc that audits every surface a visitor meets
  for comprehension, conversion, and retention, then ships the biggest
  lifts as commits. 81 briefs, 17 playbooks

## 0.9.0 — 2026-07-07
- Seven briefs closing the biggest coverage gaps, each the standard
  read-only 4-phase audit that leaves one evidence-backed report:
  - 68 Localization Readiness (Trust): hardcoded strings, locale-blind
    number/date formatting, plural and RTL gaps — writes I18N.md
  - 69 License & Compliance (Trust): dependency license compatibility,
    copyleft reach, attribution owed — writes LICENSES.md
  - 70 SEO & Discoverability (Growth): titles, crawlability, structured
    data, social unfurls — writes SEO.md
  - 71 Migration Safety (Data): table locks, reversibility, timed-out
    backfills, expand/contract ordering — writes MIGRATIONS.md
  - 72 Ownership & Bus Factor (Team): git-history truck factor, orphaned
    code, single points of human failure — writes OWNERSHIP.md
  - 73 Telemetry & SLOs (Ops): the positive side of observability —
    metric/trace/log coverage and SLOs, not just crash detection —
    writes TELEMETRY.md
  - 74 Change Risk Review (Act): the first diff-scoped brief — blast
    radius, missing tests, rollback story, go/no-go — writes CHANGE-RISK.md
- Two playbooks: Ship to the World (68 → 08 → 70, reach & inclusion) and
  OSS Release-Ready (06 → 07 → 69, safe to make public). 75 briefs,
  13 playbooks

## 0.8.0 — 2026-07-07
- Paid down the whole IMPROVEMENTS.md opportunity map (the v0.7 self-audit
  re-run) via 47 · The Fixer, one finding per commit:
- Share cards for every brief: the 22 briefs added since 0.5 (Act, Design,
  Venture, 48–53) had no OG image, so their `/b/<id>` pages unfurled a 404.
  `scripts/og.py` generates cards from front matter and the build now fails
  if a brief ships without one
- Self-hosted fonts: Archivo + IBM Plex Mono vendored as woff2 (OFL),
  dropping the site's last runtime third party — closes SECURITY 4
- Offline PWA: a build-generated service worker precaches the shell and
  fonts (content-hash cache version); the catalog, Studio, and new Vitals
  Viewer work offline
- Vitals Viewer (/vitals): drop brief 29's HEALTH.md history and every
  vital becomes a sparkline with run-over-run deltas — client-side
- Report Studio loads reports straight from a public GitHub repo, no
  download step; the report grammar is now documented and linted, and the
  Studio surfaces the impact chip
- Venture family dogfooded: a sourced Gut Check (62 → 63 → 67) on a real
  candidate niche, live in the sample gallery — every claim linked and dated
- Zero-result search suggests the closest briefs (the MCP server's
  rarity-weighted scoring, in-page) and logs the miss; run tracker keeps
  timestamps and nudges when Weekly Vitals goes stale; playbook chips copy
  their conductor in one tap
- sitemap.xml + robots.txt from the build; families injected from one
  source instead of hand-synced; MCP version reads from package.json;
  3-digit hash-router ids; MCP package made publish-ready (npm publish
  itself still pending credentials). 68 briefs, 11 playbooks

## 0.7.0 — 2026-07-06
- Venture family (is it worth building?): eight briefs that research a
  company before it exists — 60 Opportunity Scan, 61 Niche Map, 62 Pain &
  Demand Mining, 63 Competitor Teardown, 64 Market Size & Timing,
  65 Positioning & Wedge, 66 Moat & Model Check, 67 Venture Verdict.
  Repo-as-workspace: each brief web-researches one stage and leaves a
  sourced report; 67 rules go/pivot/kill against bars set before scoring
- Family evidence rules: every claim carries a source link and date,
  arithmetic is shown, and disconfirming evidence gets equal effort
- Two playbooks: Founder Funnel (61→67, the whole pipeline) and Gut Check
  (62·63·67, 72 hours of truth). Audit Triage (46) learns the pre-product
  signal. 68 briefs, 11 playbooks; the catalog now opens with Venture

## 0.6.0 — 2026-07-06
- Design family (is it beautiful?): six briefs for UI, web, and graphic
  design — 54 Visual Hierarchy, 55 Typography, 56 Color & Contrast,
  57 Spacing & Layout, 58 Interaction States & Motion, 59 Brand Coherence.
  Evidence rules of the house: every visual claim cites a selector, token,
  or computed ratio
- Face-Lift playbook: 54 → 57 → 55 → 56 → 47 — audit the visuals, then the
  Fixer turns the findings into commits
- Audit Triage (46) learns the Design signal; run-all-6 family conductor at
  /raw/family-design.md. 60 briefs, 9 playbooks

## 0.5.0 — 2026-07-06
- Act family (does anything change?): 46 Audit Triage routes a repo to the
  briefs it needs; 47 The Fixer turns audit reports into verified commits,
  one finding per commit on its own branch
- Report Studio (/studio): drop your reports, findings become a checklist
  with severity chips, and checked findings become a targeted Fixer prompt —
  entirely client-side
- Six new audits: 48 Memory & State, 49 Retrieval Quality, 50 Multi-Agent
  Topology, 51 Latency Budget, 52 Agent Readiness, 53 Config & Environment;
  two new playbooks (Triage & Fix, Retrieval Tune-Up). 54 briefs, 8 playbooks
- Custom conductors: compose any sequence of briefs into one conductor
  prompt — '+ seq' on the site, make_conductor over MCP, plus per-family
  'run all' conductors at /raw/family-<slug>.md
- Paid down the self-audit debt the sample reports named: stemmed and
  rarity-weighted suggest_briefs (IMPROVEMENTS 1); sample-report chips on
  audited cards (IMPROVEMENTS 2); scripts/check one-command gate and a real
  MCP smoke test (DX 1); linter tests including the lens-scoping regression
  (DX 2); baseline security headers (SECURITY 3); FIXLOG.md records it
- Fork support: GOAL_PROMPTS_BASE rewrites every generated surface for teams
  running a private catalog

## 0.4.0 — 2026-07-06
- Agent-native catalog: stable raw URLs per brief, playbook conductors,
  machine-readable catalog.json, and a zero-dependency MCP server
  (list_briefs / suggest_briefs / get_brief / get_playbook)
- Context configurator: aim every copied brief at your stack and stage
- Dogfood gallery at /examples/ — Day-1 playbook run on this repo;
  two bugs it found (copy-label race, empty-state self-XSS) fixed here
- Installer now verifies a published sha256 and warns before overwriting
- Brief linter in the build: 4-phase skeleton, Rules section, ask-first
  ending, lens counts — enforced on every deploy
- Per-brief share pages (/b/30) with individual OG cards; discuss links;
  ctrl/cmd-K; PWA manifest and icons

## 0.3.0 — 2026-07-06
- 16 new briefs (30–45) for AI-agent products, in three new families:
  Agent (does the agent deliver?), Automation (does the process hold?),
  AI-UX (does the human trust it?), plus Feedback Loop Audit in Product
- Two new playbooks: Agent Day-1 and Agent Ship-Check
- Catalog copy de-hardcoded from "30"; OG image regenerated

## 0.2.0 — 2026-07-06
- Slash-command installer: `curl -fsSL https://goal-prompts.vercel.app/install | sh`
  installs all briefs as `/goal:*` Claude Code commands (+ commands.zip)
- Deep links: `/#07` opens and highlights a brief; per-card link button
- Run tracker: mark briefs as run (stored locally), progress in masthead,
  nudge toward #28 Roadmap Synthesis after 5 runs
- Playbooks: Day-1 New Repo · Pre-Launch · Spring Cleaning · Weekly Vitals
- OG image, favicon, meta descriptions for link unfurls
- Repo scaffolding: CI (build + drift check), MIT license, templates
- build.py now emits deterministic command archives

## 0.1.0 — 2026-07-06
- 30 briefs across 11 families, each < 4k chars
- Catalog site with search, family filters, one-tap copy
- `build.py` pipeline: prompts/*.md → index.html
- Deployed to https://goal-prompts.vercel.app
