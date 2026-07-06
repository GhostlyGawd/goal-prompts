# Goal Prompts

Thirty mission briefs for Claude Code (or any coding agent). Each one points the agent at your repo, walks it through a 4-phase audit — **Explore → Audit → Curate → Report** — and produces a single evidence-backed report file at your repo root.

Every prompt body is under 4,000 characters.

**Live:** https://goal-prompts.vercel.app · **Source:** https://github.com/GhostlyGawd/goal-prompts · MIT licensed

## Install as slash commands

```
curl -fsSL https://goal-prompts.vercel.app/install | sh
```

Run from a repo root. Every brief becomes a native Claude Code command:
`/goal:bug-hunt`, `/goal:prune-audit`, `/goal:roadmap-synthesis`…
Prefer a file? Grab `commands.zip` from the site and extract into
`.claude/commands/`.

## Playbooks

Curated sequences on the site, for when you don't want to choose:

| Playbook | Briefs | When |
|---|---|---|
| Day-1 New Repo | 00 → 01 → 06 → 14 | first contact with a codebase |
| Pre-Launch | 06 · 08 · 23 · 25 | the night before |
| Spring Cleaning | 26 → 27 → 13 → 22 | make it smaller and clearer |
| Weekly Vitals | 29 | ten minutes, every week |

## Use

1. Open `index.html` — the catalog UI. Filter by family, tap **Copy**.
2. Paste the prompt into Claude Code inside the repo you want audited.
3. The agent writes its report (e.g. `BUGS.md`, `PERF.md`) at that repo's root.
4. Run `28 · Roadmap Synthesis` last — it merges every report into one sequenced `ROADMAP.md`.

## Families

| Family | Question | Prompts |
|---|---|---|
| Product | what could this be? | 00 |
| Quality | does it work? | 01–03 |
| Speed | does it scale? | 04–05 |
| Trust | is it safe? | 06–08 |
| Growth | does it grow? | 09–12 |
| Team | can others build on it? | 13–15 |
| Clarity | is it understood? | 16–18 |
| Data | is it sound? | 19–22 |
| Ops | does it run? | 23–25 |
| Subtract | what should go? | 26–27 |
| Meta | do the reports compose? | 28–29 |

## Develop

Source of truth is `prompts/<family>/<id>-<slug>.md`. Each file is front matter + prompt body:

```
---
id: "07"
title: Dependency Health Check
family: Trust
question: is it safe?
output: DEPS.md
tagline: One line shown on the card.
---
# Goal: ...
(the copyable prompt body)
```

Rebuild the site after editing:

```
python3 build.py
```

The build injects all prompts into `template.html` and writes `index.html`. It fails if any prompt body exceeds 4,000 characters.

## Add a prompt

1. Create `prompts/<family>/NN-slug.md` with the front matter above.
2. Keep the 4-phase skeleton; keep the body under 4k.
3. `python3 build.py` — done.

## Contributing

See `CONTRIBUTING.md`. Every push is built on Vercel with `build.py` as a
hard gate — an oversized brief blocks the deploy. An optional GitHub
Actions workflow lives at `.github/ci.example.yml`.
