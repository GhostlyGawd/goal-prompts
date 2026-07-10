# COMPETITIVE.md — Competitive Gap Scan

**Date:** 2026-07-09
**Auditor:** competitive-gap brief, read-only pass + web research
**Prior run:** none — no previous `COMPETITIVE.md` existed; this is the first competitive scan.

**Evidence notes.** The live site (goal-prompts.vercel.app) is network-blocked from this
environment, so "us" is reconstructed from source (`README.md`, `template.html`, `build.py`,
`prompts/`, `playbooks.json`) — which is the source of truth anyway. Two rival surfaces
returned 403/429 to direct fetches (`cursor.directory`, `coderabbit.ai/pricing`); for those I
cite the Show HN thread (fetched in full) and multiple independent pricing writeups surfaced
by search, and I flag them as second-hand where used. Everything else below was retrieved
directly. No competitor feature in this report is imagined.

---

## 1 · Arena summary

**Category:** prompt/command catalogs for AI coding agents — specifically, installable
libraries of reusable instructions (commands, agents, skills, rules) for Claude Code and
its peers. Goal Prompts' niche inside it: **audit briefs** — 141 read-only, four-phase,
report-writing missions (`README.md:3`), delivered as a web catalog, a Claude Code plugin,
a curl installer, an MCP server, and raw URLs.

**Audience:** individual developers and small teams already running Claude Code (secondarily
Cursor/any agent — the meta description claims both, `template.html:7`), who want structured
repo audits rather than ad-hoc "find bugs" prompts. No signup, no backend, MIT.

**The rivals a prospective user actually compares** (all retrieved 2026-07-09):

| Rival | One line |
|---|---|
| **davila7/claude-code-templates** (aitmpl.com) | 100+ agents/commands/MCPs/hooks/skills with an npx one-item installer, web dashboard, analytics + health-check tooling; 28.5k stars. (github.com/davila7/claude-code-templates) |
| **wshobson/agents** | 92 plugins → 199 agents, 162 skills, 106 commands, generated from one Markdown source for five harnesses (Claude Code, Codex, Cursor, OpenCode, Gemini); tiered model assignment; 37.7k stars. (github.com/wshobson/agents) |
| **VoltAgent/awesome-claude-code-subagents** | 154+ subagents in 10 categories, four install paths incl. plugin marketplace, a companion `/subagent-catalog:search` skill; sponsorship-funded; 23.1k stars. (github.com/VoltAgent/awesome-claude-code-subagents) |
| **hesreallyhim/awesome-claude-code** | The category's front door: 49.6k-star curated list of commands/skills/plugins/hooks, explicit "quality, security, originality" bar, CSV index. (github.com/hesreallyhim/awesome-claude-code) |
| **cursor.directory** | The same shape for Cursor: rules + MCP directory + jobs board, ~250k users/mo, 67k members, open source, free. (Show HN #43412295, fetched; scale figures from the founder in-thread; feature summary via mcpize.com/alternatives/cursor-directory) |
| *Adjacent ceiling:* **CodeRabbit** | Paid automated PR review — the "just buy the audit outcome" alternative: Free for OSS, Pro ~$24/user/mo, Pro+ ~$48 (search-verified across docs.coderabbit.ai/management/plans, costbench.com, dev.to pricing writeups; direct pricing page 403'd). |

**Distribution reality check:** GhostlyGawd/goal-prompts shows **0 stars, 0 forks**
(github.com/GhostlyGawd/goal-prompts, fetched today). The rivals above hold 23k–50k stars.
The product gap analysis below matters, but the headline gap in this category is
distribution and proof, not features.

---

## 2 · Comparison table

| Capability | Us | aitmpl | wshobson/agents | VoltAgent | awesome-claude-code | cursor.directory |
|---|---|---|---|---|---|---|
| Web catalog with per-item pages | ✓ (`/b/<id>`, `/p/<key>`) | ✓ (aitmpl.com, beta) | GitHub only | GitHub only | GitHub only | ✓ |
| Claude Code plugin install | ✓ (`/plugin marketplace add`) | ✓ | ✓ | ✓ | n/a (list) | n/a |
| Install ONE item without the rest | ✗ (copy-paste only; installer/plugin = all 141) | ✓ (`npx … --agent X --yes`) | per-plugin (92 units) | ✓ (fetch skill / manual copy) | n/a | ✓ (copy/download per rule) |
| MCP server exposing the catalog | ✓ (6 tools + every brief as an MCP prompt) | ✗ (ships third-party MCPs, not a catalog server) | ✗ | partial (catalog *skill*) | ✗ | MCP listed, "brewing" per founder |
| Skills (SKILL.md) format | ✗ (commands only) | ✓ | ✓ (162 skills) | agents format | curates skills | n/a |
| Multi-harness output (Cursor/Codex/Gemini) | ✗ (claims "Cursor, and any coding agent" in meta copy; ships Claude-Code-shaped artifacts) | Claude Code | ✓ five harnesses from one source | Claude Code | Claude Code | Cursor |
| Curated sequences (playbooks/orchestrators) | ✓ 12+ playbooks + per-family conductors | ✗ | ✓ (16 orchestrators) | ✗ | ✗ | ✗ |
| Machine-enforced quality bar on every entry | ✓ (linter: 4-phase skeleton, ask-first gate, <4k chars — `build.py`, CI-gated) | ✗ | ✗ (conventions, not a linter gate) | ✗ | editorial review | ✗ (community submissions) |
| Output loop (report → checklist → commits) | ✓ (Report Studio + 47 Fixer + FIXLOG) | ✗ | ✗ | ✗ | ✗ | ✗ |
| Sample outputs published | ✓ (`/examples/` — Day-1 run against this very repo) | ✗ | ✗ | ✗ | ✗ | ✗ |
| Scheduled/standing runs | ✓ (`.github/run-brief.example.yml`) | ✗ | ✗ | ✗ | ✗ | ✗ |
| Self-host / private team catalog | ✓ (`GOAL_PROMPTS_BASE` rebase of every surface) | ✗ | fork | fork | n/a | fork |
| Community submission path surfaced in-product | weak (CONTRIBUTING.md exists; site doesn't ask) | ✓ (attribution pipeline) | ✓ | ✓ (PRs, with anti-promo policy) | ✓ (the whole model) | ✓ (submit on site) |
| Social proof (stars, users, live stats) | **0 stars; site shows no usage numbers** | 28.5k★ | 37.7k★ | 23.1k★ | 49.6k★ | 250k users/mo + public live-stats dashboard |
| Price | free, MIT | free, MIT | free | free (sponsor-funded) | free | free (jobs board) |

---

## 3 · Table stakes we lack (ranked by user expectation)

1. **Social proof, or an honest substitute — S.** Every rival's first screen is a star
   count; cursor.directory's founder answers "how did you grow" with a *public live-stats
   dashboard link* (HN thread). This site shows zero usage evidence (and at 0 GitHub stars,
   a star badge would hurt). The honest substitute already exists in-repo and is buried:
   the `/examples/` sample reports and the FIXLOG are proof-of-output no rival has —
   promote them to where a star count would sit. (Evidence: all five rival repo pages;
   HN #43412295.)

2. **Skills (SKILL.md) format — M.** The ecosystem's recommended packaging moved:
   Claude Code v2.1.101 made `.claude/skills/<name>/SKILL.md` the recommended form
   (code.claude.com/docs, via search; aitmpl and wshobson both ship skills). Goal Prompts
   ships commands only. `build.py` already generates the plugin from one source; emitting
   a parallel skills tree is a build change, not a content change.

3. **Install one brief, not 141 — S/M.** aitmpl's core UX is
   `npx claude-code-templates --agent X --yes`; VoltAgent ships a fetch-one skill;
   cursor.directory is copy/download-per-rule. Goal Prompts' installer and plugin are
   all-or-nothing (fine), but a user who wants just `/goal:bug-hunt` as a *persistent
   command* has no path short of hand-copying a file. A `BRIEF=01 sh install` flag or
   per-brief download on `/b/<id>` matches the norm cheaply.

4. **Make the multi-harness claim true or narrow it — M.** The meta description promises
   "Claude Code, Cursor, and any coding agent" (`template.html:7`). Copy-paste does work
   anywhere — but wshobson generates *native* artifacts for five harnesses from one
   source, and Cursor users have a whole directory of their own. Either emit a
   `.cursor/commands`/rules artifact from `build.py` (it already templates everything) or
   soften the claim before a Cursor user bounces off a Claude-shaped install page.

5. **Ask for contributions where users are — S.** All five rivals grow on community
   submissions; cursor.directory added submit-on-site within a day of being asked (HN
   thread). `CONTRIBUTING.md` exists but the site never asks. One "add a brief →" link in
   the footer/catalog is enough; the linter is already the moderation story.

---

## 4 · Patterns worth learning (theirs, proven)

- **aitmpl — component manager thinking.** Their top recurring issues are *uninstall and
  inventory* ("How to uninstall completely a skill, agent, command…?", issue #649; "local
  components manager dashboard… safe uninstall", #617). Users treat installed prompts as
  managed software. Goal Prompts' uninstall is one honest `rm -rf` line in the README —
  keep that, but say it at install time, not only in docs.
- **VoltAgent — the catalog reachable from inside the session** (`/subagent-catalog:search`).
  Goal Prompts' MCP server already does this better (six tools + prompt picker) — it's a
  parity-plus feature currently presented as an afterthought in "Call it from an agent".
- **wshobson — model-tier guidance per unit.** Each agent declares which model tier it
  wants (Opus for architecture/security, Haiku for fast ops). Briefs could carry an
  optional `effort:`/model hint in front matter — cheap metadata, real operator value.
- **cursor.directory — radical transparency as marketing.** Open-sourcing the site and
  publishing the live analytics dashboard *is* their credibility engine. This repo is
  already open source with a documented zero-code metrics option (`docs/usage-metrics.md`);
  publishing the numbers once they exist is the same move.

---

## 5 · Pricing & packaging norms

The direct category's price is **zero, universally**. Monetization where it exists is
side-channel: VoltAgent explicitly routes promotion through **sponsorship** ("we don't
accept PRs whose primary purpose is to promote a product… sponsorship is the supported
pathway"); cursor.directory runs a **jobs board**; aitmpl is unmonetized MIT. The paid
ceiling is the adjacent outcome product: CodeRabbit at ~$24–48/user/mo for automated PR
review, free for OSS repos.

**Where this product sits:** correctly at $0, and — unusually — already built for the
category's actual monetization pattern: `playbooks.json` supports `sponsored`/`collab`/
`partner` merchandising fields rendered on the storefront (CLAUDE.md, README:16–19).
That is the VoltAgent sponsorship model with better surface area. The other latent
package is the **private team catalog** (`GOAL_PROMPTS_BASE` rebases every generated
surface to an internal domain) — none of the free rivals productize self-hosting.
Do not paywall briefs; the market has set that expectation at zero.

---

## 6 · Underleveraged strengths (real, in-repo, mostly unsurfaced)

1. **The linter is the moat and it's invisible.** No rival machine-enforces entry quality;
   this repo CI-gates every brief on structure, the ask-first safety gate, and a 4k cap
   (`build.py`, `tests/test_build.py`, Vercel build gate). Rival pain runs the other way:
   "the rules aren't any better… It doesn't really work" (HN, on Cursor rules). "Every
   brief passes a published linter" is a trust claim worth a page.
2. **The output loop.** Report Studio → targeted 47-Fixer prompt → one commit per finding,
   with a real FIXLOG. Every rival stops at "here's a prompt"; none owns what happens
   *after* the run.
3. **Playbooks/conductors.** Sequenced, one-paste multi-brief runs (12+ playbooks, family
   conductors). Only wshobson has an analogue (orchestrators); no directory-style rival does.
4. **Standing audits at $0.** The `run-brief.example.yml` GitHub Action is a scheduled
   audit-as-issue — functionally CodeRabbit's standing-review value at zero dollars,
   currently one paragraph deep in the README.
5. **The Venture family.** Web-research briefs that run *before a repo exists* — nothing
   comparable anywhere in the arena surveyed.

---

## 7 · Positioning gaps

Words the rivals own: **"agents"** (wshobson, VoltAgent), **"subagents"** (VoltAgent),
**"templates"** (aitmpl), **"rules"** (cursor.directory), **"awesome/curated list"**
(hesreallyhim). Words nobody owns and this product already half-claims: **"audits"**,
**"briefs"**, **"reports"**, **"evidence"**. The H1 — "turn your coding agent into a
senior code auditor" — is differentiated; the meta description then dilutes it back into
the crowded "copy-paste … for Claude Code, Cursor, and any coding agent" register. Lean
audit-first: the rival complaint record (flaky rules, unmanageable installs, 154-agent
sprawl) is exactly the noise "141 linted briefs, one report format, one loop to commits"
cuts through.

---

## 8 · Their users' complaints (openings)

| Rival | Recurring pain (evidence) | Opening for us |
|---|---|---|
| cursor.directory / rules category | Rules flaky and poorly documented; "the rules aren't any better… It doesn't really work"; coverage gaps ("cannot identify a single… React that is not Nextjs"); newcomers ask *how to even use* a rule; staleness worry as models change (HN #43412295, fetched) | Briefs are self-contained missions, not ambient config — they either produce the report or visibly fail. Say that. Publish the linter. |
| aitmpl | Uninstall/inventory confusion (#649, #617); analytics broken on Windows (#621); config-dir edge cases (#631) (github issues page, fetched) | Zero-state simplicity: no daemon, no dashboard, `rm -rf` uninstall. Their management pain is the cost of the tooling we chose not to build (see §9). |
| VoltAgent / wshobson | Scale itself: 154 subagents / 92 plugins with no per-item quality gate; promo-PR pressure requiring an explicit anti-promo policy | Curation + machine-enforced floor as the counter-position. |
| awesome-claude-code | 590 open issues; list churn ("legacy" resources split out) — curation debt at scale | A built catalog with CI, checksums, and stable raw URLs is a product, not a list. |
| CodeRabbit (adjacent) | Per-seat cost scales with team; billed on PR authors (pricing writeups, search-verified) | The $0 standing-audit GitHub Action, aimed at OSS/small teams. |

---

## 9 · Do-not-copy list

- **aitmpl's analytics/monitoring suite** (live session dashboards, conversation monitor,
  Cloudflare tunnels). It contradicts this product's stated stance — "no signup · nothing
  leaves your machine" (`template.html:502`) — and their own tracker shows the maintenance
  bill (Windows analytics broken, #621). The privacy stance *is* the differentiation.
- **cursor.directory's community platform** (accounts, jobs board, member counts). Needs
  their 250k users/mo to function; adds a backend to a deliberately backend-free product.
- **The 150+ item arms race** (VoltAgent, wshobson). Growing the count dilutes the one
  thing rivals can't say — every entry passes the same linter. Growth should come from
  families/playbooks, not raw brief inflation.
- **Multi-harness maximalism** (wshobson's five harnesses). Matching Cursor (one emitter
  in `build.py`) is a table stake; chasing Codex/Gemini/OpenCode parity is their strategy —
  they have 92 plugins and Python codegen infrastructure to amortize it. One extra target,
  not five.
- **Paid briefs / marketplace pricing.** The category price is zero; the paid layer that
  works here is sponsorship + private catalogs, both already scaffolded.

---

## 10 · Stakes vs bets — the shortlist

**Match (table stakes):** skills-format output (M) · per-brief install (S/M) · make the
Cursor claim real or narrow it (M) · surface proof (`/examples/`, FIXLOG, metrics) where
rivals put star counts (S) · ask for contributions on-site (S).

**Differentiation bets (each traces to something already in the repo):**

1. **Own "the audit loop."** Position and package brief → report → Studio → Fixer →
   FIXLOG as one product motion; lead the landing page with the loop, not the catalog
   size. No rival owns post-run. (Traces to: `studio.html`, prompt 47, `FIXLOG.md`,
   `examples/`.)
2. **Publish the quality bar.** A "why these briefs don't rot" page: the linter's rules,
   the CI gate, the 4k cap, the ask-first gate — aimed squarely at the category's
   flakiness/slop complaints. (Traces to: `build.py` linter, `tests/test_build.py`,
   CONTRIBUTING.)
3. **Productize the standing audit + private catalog.** Elevate `run-brief.example.yml`
   and `GOAL_PROMPTS_BASE` from README paragraphs into a "for teams" page — the free
   counter-position to CodeRabbit's per-seat pricing and the one packaging story no free
   rival has. (Traces to: `.github/run-brief.example.yml`, README "Run your private team
   catalog", `install` BASE support.)

---

*Report only — no changes were made.* The stakes and bets above are ranked and scoped:
**which moves should I make — the table-stakes fixes (skills output, per-brief install,
Cursor parity, proof surfacing), one of the three differentiation bets, or a specific
combination?*
