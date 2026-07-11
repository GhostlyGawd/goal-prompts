# COMPETITORS.md
*Produced by brief 63 · Competitor Teardown, run against **this repo's own venture: goal-prompts — a catalog of structured audit briefs for coding agents.** Scoped from NICHE.md + DEMAND.md. All sources accessed 2026-07-10 unless dated otherwise. Directly-fetched primaries unmarked; general-web-search synthesis marked **[secondary]**.*

**Date:** 2026-07-10

Everyone below competes for one job — *"have my repo audited by the coding agent I already run"* — at four layers of the stack (NICHE.md §0). The money is proven one layer **over** (execution/outcomes), the attention one layer **under** (free catalogs at 23k–50k★), and goal-prompts is the 0★ entrant in the seam. Prices, star counts, and the CodeRabbit hero were re-verified live today; quotes I couldn't fetch first-hand are marked **[secondary]**, and the silence test is called at the end.

## The matrix

| Competitor · layer | Positioning (their words / page) | Price | Traction proxy | Source (2026-07-10) |
|---|---|---|---|---|
| **CodeRabbit** · execution | *"Cut code review time & bugs in half, instantly"* — AI PR review | Free · **$24**/user/mo Pro · **$48** Pro+ · Enterprise "Contact us" | *"6M Repositories," "75M Defects found," "Most installed AI App," "Trusted by 15,000+ customers"*; Jensen Huang: *"We're using CodeRabbit all over NVIDIA"* | `coderabbit.ai`, `coderabbit.ai/pricing` |
| **Greptile** · execution | *"Greptile Now Runs Your Code"* (TREX) — full-codebase-graph review | Free (50 credits) · **$30**/seat (50 credits, then **$1**/credit) · Enterprise custom | Series A led by Benchmark; **~$180M** val (DEMAND.md **[secondary]**); free for OSS, 50% off <$2M-rev startups | `greptile.com/pricing` |
| **Qodo** (ex-CodiumAI) · execution | *"Code Quality that Scales with Your Team"* | **$30**/mo Pro Team (≤30 users, credits **$0.012** ea) · Enterprise custom (30+) | Customers on page: **Intel, NVIDIA, Walmart, Intuit, Box, monday.com**; ~1M dev users, ~100 staff (DEMAND.md/**[secondary]**) | `qodo.ai/pricing` |
| **hesreallyhim/awesome-claude-code** · catalog | *"A hand-picked collection of the finest resources… quality, security, originality"* | **$0**, curated list | **49,729★**, 4,325 forks, **613 open issues**, pushed 2026-07-10 | GitHub API (fetched) |
| **wshobson/agents** · catalog | *"Multi-harness agentic plugin marketplace for Claude Code, Codex CLI, Cursor, OpenCode, GitHub Copilot, Gemini CLI"* | **$0**, MIT | **37,762★**, 4,048 forks, **1** open issue, pushed 2026-07-08 | GitHub API (fetched) |
| **davila7/claude-code-templates** (aitmpl) · catalog | *"CLI tool for configuring and monitoring Claude Code"* — 100+ agents/commands/MCPs + dashboard | **$0**, MIT | **28,745★**, 3,156 forks, **191 open issues**, pushed 2026-07-10 | GitHub API (fetched) |
| **VoltAgent/awesome-claude-code-subagents** · catalog | *"100+ specialized Claude Code subagents…"* | **$0**, sponsor-funded | **23,154★**, 2,704 forks, pushed 2026-07-10 | GitHub API (fetched) |
| **cursor.directory** · catalog | Rules + MCP directory + jobs board for Cursor | **$0** (jobs board) | ~250k users/mo, 67k members (COMPETITIVE.md, HN #43412295) **[secondary]** | Show HN #43412295 |
| **claude-autopilot** · catalog/upstart | *"Every phase is an editable markdown skill. Not a black-box pipeline"* | **$0** | Show HN, 2026-05-19 (DEMAND.md) | HN `item?id=48201112` |
| **PromptBase** · marketplace | *"Prompt Marketplace"* — Image/Text/Video/**Code** categories, image-dominant | Prompts **$1.99–9.99**; Select **$14–19**/mo (DEMAND.md **[secondary]**) | Largest paid prompt marketplace; category cooling **[secondary]** | `promptbase.com/marketplace` |
| **Anthropic `/security-review`** · platform | *"AI-powered security review GitHub Action using Claude…"* — first-party, `.claude/commands`-installable | **$0**, MIT (+ metered agent tokens) | **5,516★**, 585 forks, **76 open issues**; created 2025-08-04, pushed **2026-02-11** | GitHub API (fetched) |
| **Status quo** · doing-nothing | *"I keep a running doc of prompts that work well"* (sukit, HN) | **$0** | Ubiquitous default; the real competitor (NICHE.md §1) | HN `item?id=44362244` |
| **goal-prompts** *(the entrant)* | *"Turn your coding agent into a senior code auditor"* — 141 linted 4-phase audit briefs | **$0**, MIT | **0★, 0 forks** (as of COMPETITIVE.md 2026-07-09) | `github.com/GhostlyGawd/goal-prompts` |

Also in-field but folded into prose below: **Cursor rules** and **GitHub Copilot** (platform primitives that ship the audit-instruction slot natively), and `rohitg00/awesome-claude-code-toolkit` (2,278★, DEMAND.md) as a second-tier catalog.

## Positioning claims — the cluster

Three registers, and the whitespace between them:
- **Execution vendors lead with the outcome + a number:** *"cut… in half," "75M defects," "quality that scales."* They sell a metric, not a method. The word they all lean on is **"review"** — and increasingly **"runs your code"** (Greptile's TREX). *Grounding the finding* is their differentiation axis (CodeRabbit's "judge model," Greptile's codebase graph).
- **Catalog vendors lead with a count + a format noun:** *"100+ subagents," "92 plugins," "the finest collection."* Their free differentiation is **size**; the nouns they own are **agents / subagents / templates / rules / awesome-list** (COMPETITIVE.md §7).
- **Platform leads with "first-party + free":** `/security-review` needs no vendor — *"copy `security-review.md` into `.claude/commands/`"* (DEMAND.md).

The words **nobody** owns, and goal-prompts already half-claims: **audit · brief · report · evidence.** Every rival says "review" (a verb that ends when the comment is posted) or "agent/prompt" (an input); none says "audit that produces a filed report you can diff." That register is free — but its H1 currently dilutes back into the crowded *"copy-paste for Claude Code, Cursor, and any coding agent"* line (COMPETITIVE.md §7). Stop saying "prompt"; the tribe already stopped ("harness/context engineering," "prompt engineer" title down ~30%, NICHE.md **[secondary]**).

## Feature & pricing matrix — the packaging tricks, and what hides behind "Contact us"

The execution layer's tricks, from their own pages today:
- **CodeRabbit meters *reviews per developer*** — Pro caps **5**, Pro+ **10**; MCP connections **5 → 15**; unit-test generation and merge-conflict resolution are Pro+-only; **RBAC/SSO, API access, self-hosting, SLA, dedicated CSM all sit behind Enterprise "Contact us."** The $24 headline is a throttled tier.
- **Greptile meters *credits*** — 50/mo free and per seat, **$1 per extra credit**, and a "TREX review" burns **3 credits**. Self-hosting, SSO/SAML, GitHub Enterprise and a DPA are Enterprise-only. Discounting (OSS-free, 50%-off-startups) is the land-grab lever.
- **Qodo meters *credits at $0.012*** (2,500 ≈ 18 reviews) and gates the actually-differentiating features — **self-learning, cross-repo context, BYOK, on-prem, audit logs** — behind Enterprise. The $30 "Pro Team" is a funnel to a demo.

The catalog layer has no pricing to trick: it is **$0/MIT universally** (NICHE.md §1). Its "packaging" is install friction — aitmpl's `npx … --agent X --yes` one-item install and VoltAgent's fetch-one skill are the norm; goal-prompts' installer/plugin is all-141-or-nothing (COMPETITIVE.md §3). The hidden cost the free tiers don't print: **they ride metered agents** — every `/security-review` or catalog run bills Anthropic/Cursor/Copilot by the token, which is why finance now sits in a $0 tool's buying room (NICHE.md §1).

## Complaint synthesis — market truths vs per-vendor ceilings

**Market truth #1 — noise is the category disease.** Across the execution layer the shared gripe is signal-to-noise: *"if your developers learn to ignore the bot, the bot stops helping."* Head-to-head benchmark writeups put **Greptile at 11 false positives to CodeRabbit's 2** (while Greptile caught 82% of bugs to CodeRabbit's 44%), and report teams on large repos triaging **30–50% of Greptile's findings** by hand **[secondary]**. CodeRabbit's own Trustpilot reviewers call the review *"really underwhelming… most suggestions completely irrelevant or unhelpful"* and *"recommending useless things out of context"* **[secondary]**. This is the whole market's ceiling: more findings ≠ more trust, and quarantining/commenting isn't fixing. It is **the same "and then what?" the flaky-test sample found** — the field converges on *detect → comment → dashboard* and buyers ask what changed.

**Market truth #2 — the free catalogs drown their own users in inventory.** The catalog layer's shared gripe is *sprawl and lifecycle*. First-hand on aitmpl today: **#649 "How to uninstall completely a skill, agent, command, hooks…?"**, **#617 "local components manager dashboard with inventory, safe uninstall, and uninstall history,"** **#621 "Analytics dashboard shows 0 conversations on Windows despite thousands of valid JSONL files,"** **#631 "Support for `CLAUDE_CONFIG_DIR`"** (`github.com/davila7/claude-code-templates/issues`, fetched). awesome-claude-code carries **613 open issues** and periodic "legacy" churn; VoltAgent/wshobson ship 100–200 units with no per-item quality gate. **"More = better" is the sacred cow their own users are goring** (NICHE.md §3).

**Per-vendor ceilings:**
- **CodeRabbit / Greptile / Qodo:** the ceiling is *procurement and precision* — a new **per-seat/credit line item** that must out-signal free OSS tiers and the platform's own bundled review, on a noise problem none has solved. Qodo's tell is structural: it had to **rebrand from CodiumAI (test-gen) and raise $40M Series A in Sept 2024** to climb from a point tool into a "code-quality platform" **[secondary]** — the single-purpose niche didn't hold.
- **aitmpl:** the ceiling is *the tooling it chose to build* — a dashboard, analytics, Cloudflare tunnels — which contradicts "nothing leaves your machine" and shows the maintenance bill (#621 broken on Windows). Their management pain is the cost of features goal-prompts deliberately didn't build (COMPETITIVE.md §9).
- **cursor.directory / rules:** *flakiness and staleness* — *"the rules aren't any better… It doesn't really work,"* coverage gaps, newcomers asking how to even use a rule (HN #43412295, prior-fetched) **[secondary]**.
- **Anthropic `/security-review`:** the ceiling is *scope and neglect* — one narrow security prompt, **76 open issues, and no push since 2026-02-11** (fetched). The platform planted the flag and wandered off; that gap between first-party ambition and first-party upkeep is the entrant's oxygen.

**Honest evidence gap (the silence test):** Reddit, G2 and Capterra hard-block fetch (consistent with DEMAND.md/NICHE.md), so the CodeRabbit/Greptile complaint quotes above are **[secondary]** (Trustpilot + benchmark writeups via search), not primaries. The aitmpl issues and every star count/pricing figure **are** first-hand. And the loudest silence remains: **no one anywhere asks to *buy* a prompt catalog** (DEMAND.md) — the catalog complaints are about managing free things, never about paying for a better one.

## Traction proxies — ranked

1. **CodeRabbit** — the only competitor citing hard commercial scale: **15,000+ customers, 6M repos, 75M defects, "most installed AI App,"** named CTOs + Jensen Huang. Strongest signal in the set (`coderabbit.ai`, fetched).
2. **awesome-claude-code (49,729★)** — the category's front door; still shipping daily (613 open issues = live curation debt *and* engagement).
3. **wshobson/agents (37,762★)** — 4,048 forks, **1** open issue: tidy, heavily-forked, now explicitly multi-harness.
4. **Qodo** — Intel/NVIDIA/Walmart logos + ~1M dev users **[secondary]**; the $40M Series A dates the money. **aitmpl (28,745★)** trails with **191 open issues** — the highest support-load-per-star here.
5. **VoltAgent (23,154★)** + **Greptile (~$180M val)** — strong, each with an asterisk (sponsor-funded; noise reputation).
6. **Anthropic `/security-review` (5,516★)** — small stars, infinite distribution (it's *in the product*); platform reach is the real proxy.
7. **goal-prompts (0★)** — invisible. **The headline gap is distribution and proof, not features** (COMPETITIVE.md §1).

## The ignored segment

Every execution vendor's pricing and language points **up-market**: *"scales with your team," "institutional security,"* RBAC/SSO/SLA behind Enterprise, per-seat/credit meters. That excludes the exact population feeling the pain most acutely — the **individual dev and the small/OSS team running Claude Code on a repo nobody's paying $24–48/seat to review.** The free tiers toss them a bone (50 credits, OSS-free) precisely to convert them later. Meanwhile the catalog layer *includes* that dev but hands them a **154-item pile to self-assemble**, not a consistent audit. So the ignored segment is specific: *someone who wants a repeatable, evidence-producing audit, for $0, without babysitting a bot's false positives or curating a 100-agent inventory.* That segment isn't poor — it's the entire bottoms-up install base (NICHE.md's user≠buyer split) — it's merely **unmonetizable per-seat, so everyone underserves the outcome and overserves either the enterprise or the catalog count.**

## Release pulse

- **Catalog layer: sprinting.** awesome-claude-code, aitmpl, and VoltAgent all pushed **2026-07-10**; wshobson **2026-07-08**. This is a knife-fight, not maintenance decay.
- **Execution layer: sprinting on precision.** Greptile shipped a **v4** aimed at noise (accepted-comment rate reportedly **30%→43%**, +74% accepted comments) and **TREX** ("now runs your code") **[secondary]**; CodeRabbit ships "Learnings" (stored false-positive corrections) and benchmark-marketing. The direction is unanimous: **fix the noise, move from commenting toward acting.**
- **Platform: coasting on the specific artifact.** Anthropic's `/security-review` repo **hasn't been pushed since 2026-02-11** — but the *primitive* advanced around it (Agent Skills, dynamic workflows, 2026-05). Absorption is happening at the platform level, not in that one repo.
- **PromptBase / marketplaces: in decline of thesis** — *"browsing Stack Overflow when your IDE already has the answer,"* pivoting from prompt-sales to app-sales **[secondary]**.

## Moat inspection

| Competitor | What actually protects it | Head start, or real moat? |
|---|---|---|
| **CodeRabbit** | 15k customers, PR-workflow integration, accumulated "Learnings" per repo, brand ("most installed") | **Real, mild** — a data/relationship moat + distribution; assailable on noise & price, not on logos |
| **Greptile / Qodo** | Codebase-graph / context-engine tech; enterprise contracts (Qodo) | **Head start** — replicable capability; Qodo's rebrand proves the point tool wasn't defensible alone |
| **awesome-claude-code** | Curator authority + 49k-star network effect (the front door) | **Real, brand** — hard to unseat as *the list*; but it curates, it doesn't build |
| **wshobson / VoltAgent / aitmpl** | Star count, fork base, codegen pipeline (wshobson), sponsor relationships (VoltAgent) | **Head start** — forkable by definition (all MIT); the moat is attention, not code |
| **Anthropic `/security-review` + primitives** | It owns the rail — the agent, the plugin spec, the token meter | **The only deep moat in the field** — and the absorption threat (NICHE.md weather) |
| **Status quo** | Inertia, $0, zero-setup, cultural entrenchment | **The hardest opponent** — you beat another vendor by being better; you beat "just rerun it" only by being *effortless*  |

## The kill zone — what each incumbent could copy fastest

- **Anthropic** could ship a first-party **audit-workflow catalog** tomorrow — it already has `/security-review` + Agent Skills + dynamic workflows and the distribution to make it default. **Weeks-to-quarters; most lethal.** This is the kill zone the companion reports keep circling.
- **awesome-claude-code** could add an *"audits/briefs"* section curating goal-prompts' format in **a day** — but it curates links; it won't build the linter or the loop.
- **aitmpl / wshobson** could add "audit" agents with a 4-phase skeleton **fast** — the *format* is copyable in days. What they won't copy (against their own count-maximizing incentive): a **machine-enforced quality gate that caps their catalog size**, and a **report→Fixer→FIXLOG execution loop** nobody in the arena owns (COMPETITIVE.md §6).
- **CodeRabbit** could stand up a **free OSS standing-audit action** — but it fights their per-seat model, so they won't.

**Read:** the brief *format* has no moat (copyable in days); the **linter-enforced curation + published dogfood reports + the post-run loop** are copyable-but-unincentivized for everyone except Anthropic — whose copy is the existential one.

## Gap analysis

| Gap | Evidence it's real | Why it's open (hard vs worthless) | Graveyard check |
|---|---|---|---|
| **Own the post-run loop** — report → checklist → one-commit-per-finding → FIXLOG | DEMAND.md Sub-pain C: users begging *Anthropic* for *"sharable and repeatable workflows… consistency of quality"*; every execution vendor stops at "comment," every catalog stops at "prompt" | **Open because hard** — needs an opinionated report grammar + execution bridge + verification, not text; catalogs chase item count, vendors chase per-seat PR comments — neither is built to own "after the run" | No entrant owned prompt→report→commit; execution vendors own "fix" but black-box + per-seat. Underserved, empty **[secondary on demand quotes: primary HN]** |
| **Verified curation** — a machine-enforced quality bar vs catalog size | Rivals' own users goring "more=better": aitmpl #649/#617/#621 (uninstall/inventory/broken analytics), awesome-list 613 open issues, 100–200-item piles with no gate | **Open because unfashionable** — a linter/CI gate *caps* your count, which fights the star-economy incentive (bigger list = more stars); it's against everyone's growth math, not technically hard | Curated-but-small lists stay hobby-scale; no one productizes a *gated* catalog. Underserved, open-against-incentive |
| **The $0 standing team audit** — free counter to per-seat managed review | CodeRabbit/Greptile/Qodo all per-seat/credit ($24–48 / $30 / $30), language excludes solo+OSS+small teams; the ignored segment feels flakiness most | **Mixed** — hard on the "produce consistent free output riding metered agents" axis; **worthless-to-monetize** on the revenue axis (the whole DEMAND.md/REVENUE.md finding: catalog price = $0) | The vendors' own **free OSS tiers already occupy this floor**; the pure-catalog layer has **zero revenue**. Underserved on *outcome*, unserved-**for-a-reason** on *money* |
| **Re-badge off "prompt" → audit/brief/evidence** | Field renamed itself harness/context engineering (2026 conf theme); "prompt engineer" −30%; marketplaces cooling (*"Stack Overflow when your IDE already has the answer"*) **[secondary]** | **Open because incumbents are anchored** — everyone's SEO, repo name, and star history is staked to "agents/prompts/rules/templates"; abandoning your own winning noun is unfashionable, not hard | PromptBase & peers are the graveyard of "sell the prompt" — survivors pivot to *apps* **[secondary]**. The noun itself is depreciating. Underserved positioning gap |
| *Multi-harness native output (Cursor/Codex/Gemini)* | wshobson already ships 5 harnesses; cursor.directory owns Cursor | **Unserved-for-a-reason as a *wedge*** — it's **table stakes** the leaders already fill, not a green field; matching Cursor is catch-up, chasing five is their strategy (COMPETITIVE.md §9) | Not a graveyard — a crowded field. Listed to show discipline: **not** a gap to build positioning on |

## The wedge shortlist

The two-to-three a 0★ newcomer could actually win — each traces to something **already in this repo**, so it's execution, not a new build:

1. **Own "the audit loop."** Lead with **brief → report → Studio → 47·Fixer → FIXLOG** as one motion, not with catalog size. It's the one gap **open because it's hard**, it answers the field's unanimous *"and then what?"*, and **no rival owns post-run** — the execution vendors black-box it per-seat, the catalogs stop at the prompt. *Risk:* it's the exact thing Anthropic could absorb first — ship it loud before the platform does. (Traces to `studio.html`, prompt 47, `FIXLOG.md`, `examples/`.)
2. **Publish the quality bar / verified curation.** A "why these briefs don't rot" page: the linter, the CI gate, the 4k cap, the ask-first gate — aimed squarely at the category's noise-and-sprawl complaints (aitmpl inventory pain, Greptile false positives). It's the **counter-belief no rival can claim** because claiming it caps their count. *Risk:* it only bites once you have enough briefs and enough proof to matter — pair it with surfacing `/examples/` where a star count would sit. (Traces to `build.py` linter, `tests/test_build.py`.)
3. **Re-badge to audits/evidence + the $0 standing team audit.** Stop competing as "a prompt catalog" (a depreciating noun in a cooling market) and take the unowned *audit/brief/evidence* register; package `run-brief.example.yml` + `GOAL_PROMPTS_BASE` as the **free, private-catalog counter to CodeRabbit's per-seat** for the ignored solo/OSS/small-team segment. *Risk:* the free tiers of the paid vendors already sit on this floor and it carries no revenue — win *distribution and trust* here, then monetize adjacent (sponsorship/private catalogs), never at the tollgate (NICHE.md §3, REVENUE.md).

*Report only — which gap should we build positioning around?*
