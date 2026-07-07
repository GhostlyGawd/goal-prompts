# Changelog

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
