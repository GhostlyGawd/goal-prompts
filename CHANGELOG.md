# Changelog

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
