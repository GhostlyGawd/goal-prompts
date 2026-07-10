# Goal Prompts

141 mission briefs for Claude Code (or any coding agent). Each one points the agent at your repo, walks it through a 4-phase audit — **Explore → Audit → Curate → Report** — and produces a single evidence-backed report file at your repo root. Then the **Act** family turns those reports into commits.

Every prompt body is under 4,000 characters.

**Live:** https://goal-prompts.vercel.app · **Source:** https://github.com/GhostlyGawd/goal-prompts · MIT licensed

## The site

The catalog is a conversion-shaped storefront: a landing page that explains the
idea to a newcomer (the problem, the four-phase method, the report you get),
then the shop floor — every brief searchable and filterable, colored by family.
Each brief has its own page at **`/b/<id>`** — a visual walkthrough of its
method, its audit lenses, and the report it writes — and every playbook has one
at **`/p/<key>`** with a step-by-step sequence map. Playbooks can also be
merchandised: `playbooks.json` supports themed/limited, co-branded **collab**,
and **sponsored** playbooks (see the partner section on the site and the
`/p/codereview-collab` template).

## Install as slash commands

The Claude Code plugin is the primary path — real namespaced commands:

```
/plugin marketplace add GhostlyGawd/goal-prompts
```

then install **goal** from the marketplace (`/plugin install goal@goal-prompts`).
Every brief becomes `/goal:bug-hunt`, `/goal:prune-audit`,
`/goal:roadmap-synthesis`… Update with `/plugin marketplace update
goal-prompts`; uninstall with `/plugin uninstall goal`.

No plugin support in your harness? The curl installer drops the same command
files into `.claude/commands/goal/`:

```
curl -fsSL https://goal-prompts.vercel.app/install | sh
```

Run from a repo root. These surface un-namespaced as `/goal-bug-hunt`,
`/goal-prune-audit`… (a commands subdirectory does not namespace). Re-run the
installer any time to update; `rm -rf .claude/commands/goal` uninstalls.
Prefer a file? Grab `commands.zip` from the site and extract into
`.claude/commands/`.

## Call it from an agent

The catalog is agent-native — three ways in:

```
claude mcp add goal-prompts -- npx -y github:GhostlyGawd/goal-prompts
```

gives any MCP client six tools — `list_briefs`, `suggest_briefs`, `get_brief`,
`list_playbooks`, `get_playbook`, and `make_conductor` (compose a conductor
from any list of brief ids) — and exposes every brief as an MCP prompt
(`goal-<slug>`), so the whole catalog appears in your client's prompt picker.
Every brief also lives at a stable URL (`/raw/30.md`), every
playbook and every family ships a **conductor** — one prompt that fetches
and runs the whole sequence (`/raw/playbook-day1.md`, `/raw/family-agent.md`)
— and the machine-readable index is at `/catalog.json`.

On the site, open **"aim the briefs at your repo"** to save your stack,
product, and stage — it's appended to every brief you copy as an Operator
context section.

Real output lives in the [sample reports](https://goal-prompts.vercel.app/examples/) —
the Day-1 playbook run against this very repo, and the FIXLOG showing those
reports turned into commits.

## Research a company before it exists

The Venture family (60–67) runs the same machinery *before* there is a
product: create an empty repo as your research workspace, and each brief
web-researches one stage — niche, demand, competitors, market, positioning,
moat — leaving a sourced report at the root. `67 · Venture Verdict` reads
them all and rules go, pivot, or kill against bars written before scoring.
House evidence rules: every claim carries a source and date, arithmetic is
always shown, and the bear case gets the same effort as the bull. Start
with `60 · Opportunity Scan`, or run the whole **Founder Funnel** playbook
with one paste.

## Act on the reports — Report Studio

Audits leave reports at your repo root; the
[Report Studio](https://goal-prompts.vercel.app/studio) turns them into
action. Drop the `.md` files, and every finding becomes a checklist item
with a severity chip. Tick the ones that matter and one tap builds a
targeted **47 · Fixer** prompt containing exactly those findings — paste it
into your agent and it branches, implements one finding per commit, and
verifies each. Everything runs in your browser: no upload, no backend.

Privacy boundary, stated plainly: your code, reports, and setup never leave
your device — briefs run in your agent, and the Studio parses reports in the
tab. The site itself counts anonymous page views and feature events via
Vercel Analytics: no cookies, no cross-site tracking, no report or repo
contents collected — the feature events carry a random local id (`gp-aid`),
and zero-result catalog search terms are counted so search can improve.

## Run it on a schedule

`.github/run-brief.example.yml` is a ready-to-copy GitHub Actions workflow:
every Monday (or on demand) it fetches a brief you pick from
`/raw/<id>.md`, runs it against your repo with Claude Code, and files the
report as an issue — audits as a standing appointment instead of a memory.
Copy it into your repo as `.github/workflows/run-brief.yml` and set the
`ANTHROPIC_API_KEY` secret; details are in the file's header.

## Playbooks

Curated sequences on the site, for when you don't want to choose:

| Playbook | Briefs | When |
|---|---|---|
| Day-1 New Repo | 00 → 01 → 06 → 14 | first contact with a codebase |
| Pre-Launch | 06 · 08 · 23 · 25 | the night before |
| Spring Cleaning | 26 → 27 → 13 → 22 | make it smaller and clearer |
| Weekly Vitals | 29 | ten minutes, every week |
| Agent Day-1 | 30 → 31 → 32 → 37 | first contact with an agent codebase |
| Agent Ship-Check | 35 · 34 · 43 · 38 | before an agent touches real users |
| Triage & Fix | 46 → 47 | recon the repo, run your picks, then commit the findings |
| Retrieval Tune-Up | 33 → 49 → 34 | for RAG-shaped agents: context, retrieval, evals |
| Face-Lift | 54 → 57 → 55 → 56 → 47 | the visual overhaul, ending in commits |
| Founder Funnel | 61 → 62 → 63 → 64 → 65 → 66 → 67 | one niche, end to end, ruled on |
| Gut Check | 62 → 63 → 67 | 72 hours of truth for one idea |
| Experience Optimization | 76 → 77 → 75 → 79 → 80 → 78 → 47 | optimize every surface: comprehension → conversion → retention, ending in commits |

## Use

1. Open `index.html` — the catalog UI. Filter by family, tap **Copy**.
2. Paste the prompt into Claude Code inside the repo you want audited.
3. The agent writes its report (e.g. `BUGS.md`, `PERF.md`) at that repo's root. Prefer a clean root? `mkdir reports` once — every brief writes there instead, and the collectors (28, 29, 46, 47) look in both places.
4. Run `28 · Roadmap Synthesis` to merge every report into one sequenced `ROADMAP.md`, or drop the reports into the **Report Studio** and let `47 · The Fixer` implement them.

## Families

| Family | Question | Prompts |
|---|---|---|
| Venture | is it worth building? | 60–67 |
| Product | what could this be? | 00, 45, 106–108 |
| Quality | does it work? | 01–03, 98–102 |
| Speed | does it scale? | 04, 05, 51, 87, 88, 140 |
| Trust | is it safe? | 06–08, 68, 69, 81–86 |
| Compliance | does it respect the user? | 125–128 |
| Growth | does it grow? | 09–12, 70, 75, 78–80, 109, 110 |
| Team | can others build on it? | 13–15, 52, 72, 94–97 |
| API | will developers adopt it? | 111–115, 136 |
| Clarity | is it understood? | 16–18, 76, 103, 135 |
| Design | is it beautiful? | 54–59, 77, 104, 105, 129–134 |
| Data | is it sound? | 19–22, 71, 89, 90, 138, 139 |
| Ops | does it run? | 23–25, 53, 73, 91–93, 137 |
| Reliability | will it stay up? | 121–124 |
| Subtract | what should go? | 26, 27 |
| Meta | do the reports add up? | 28, 29 |
| Act | does anything change? | 46, 47, 74 |
| Agent | does the agent deliver? | 30–38, 48–50 |
| Automation | does the process hold? | 39–41 |
| AI-UX | does the human trust it? | 42–44 |
| AI-Ethics | is the AI responsible? | 116–120 |

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

The build injects all prompts into `template.html` and writes `index.html`. It fails if any prompt body exceeds 4,000 characters, or breaks any house rule. Run the whole gate — build, linter tests, JS syntax, and the MCP smoke test — in one step:

```
scripts/check
```

## Run your private team catalog

Forks can point every generated surface at their own deployment. Set one
environment variable before the build:

```
GOAL_PROMPTS_BASE=https://audits.your-co.internal python3 build.py
```

The site, `raw/` endpoints, conductors, `catalog.json`, and the URLs
embedded in brief bodies all follow it. The slash-command installer takes
the same idea as an env var: `BASE=https://audits.your-co.internal sh
install`. Unset, the build produces the canonical public site.

## Add a prompt

1. Create `prompts/<family>/NN-slug.md` with the front matter above.
2. Keep the 4-phase skeleton; keep the body under 4k.
3. `scripts/check` — done.

## Contributing

See `CONTRIBUTING.md`. Every push is built on Vercel with `build.py` as a
hard gate — an oversized brief blocks the deploy — and CI
(`.github/workflows/ci.yml`) runs `scripts/check` plus a generated-file
drift check on every push and PR. Ready-to-copy examples (npm publish on
release, scheduled brief runs) live at `.github/*.example.yml`.

## Project layout

Sources you edit: `prompts/`, `playbooks.json`, `template.html`,
`studio.html`, `build.py`, `install`, `mcp/`, `js/` (the site's tested
modules — catalog core, report parser, detail-page helpers), `scripts/`,
`tests/`, `docs/`, `.claude-plugin/marketplace.json`.
Generated by the build (never hand-edit): `index.html`, `raw/`, `b/`, `p/`,
`catalog.json`, `checksums.txt`, `commands.tar.gz`, `commands.zip`,
`plugin/`, `sitemap.xml`, `robots.txt`, `sw.js`, `tokens.css`.
