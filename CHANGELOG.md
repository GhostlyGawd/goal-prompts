# Changelog

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
