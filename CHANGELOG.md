# Changelog

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
