# NICHE.md
*Produced by brief 61 · Niche Map, run against **this repo's own venture: goal-prompts — a catalog of structured audit briefs (reusable prompts/slash-commands/MCP tools) for coding agents.** All sources accessed 2026-07-10 unless dated otherwise. Claims from directly-fetched primaries are unmarked; general-web-search synthesis is marked **[secondary]**.*

**Date:** 2026-07-10

## 0 · The boundary, and the reports this map must not contradict

**Inside the niche:** installable, reusable *instruction artifacts* that a developer points a coding agent at to audit or improve a repo — slash-commands, subagents, skills (`SKILL.md`), Cursor rules, MCP prompt-catalogs, "awesome" lists, and hand-rolled `.claude/commands`/`dotclaude` repos. The **catalog / command layer**: free, GitHub-distributed, developer-installed, agent-executed. goal-prompts lives here.

**Adjacent-but-out** (each a substitute, ceiling, channel, or threat — not the niche): managed AI code review (CodeRabbit, Greptile, Qodo) — the price ceiling and a substitute, but a pipeline not a catalog; the agents/harnesses themselves (Claude Code, Cursor, Copilot) — the platform the catalog rides, a channel *and* an absorption threat; general prompt marketplaces (PromptBase) — prompts sold, but consumer/image-skewed; spec-driven-development tooling (AWS Kiro, GitHub Spec Kit) — an overlapping belief system, but shipped as IDEs/CLIs, not catalogs.

**Companion reports at this root** (do not contradict): `DEMAND.md` (brief 62, 2026-07-08 — pain is real/frequent but monetized one layer over, in execution), `COMPETITIVE.md` (2026-07-09 — the rival cast + the 0-stars distribution gap), `REVENUE.md` (2026-07-09 — catalog price is $0, money is side-channel). This map reuses their verified backbone and extends it into the lenses they don't cover: watering holes, jargon, rituals, belief, and dated weather. **No claim below contradicts them; where I sharpen one, I say so.**

---

## 1 · The map

### The cast — buyers ≠ users
The defining split of this niche: the **user** (an individual developer running the agent) is usually *not* the **buyer** with budget (a DevEx/platform lead or eng manager), and the person with budget buys *outcomes*, not text.

| Role | Who | What they want | Holds the pen? |
|---|---|---|---|
| **User segment** | Individual devs running Claude Code / Cursor / Copilot | Repeatable, non-random audit output on *their* repo, for $0 | Adopts; rarely pays |
| **Buyer segment** | DevEx / platform engineers, eng managers | Standardized, consistent review across the team; a line item they can defend | Says yes to *outcomes* (CodeRabbit-shaped), skeptical of "free prompts" |
| **Gatekeeper (can only say no)** | Security, procurement, finance | Data-egress/SOC2 safety; no bill-shock | Vetoes; never champions |
| **Incumbents (catalog layer)** | `hesreallyhim/awesome-claude-code` (49.6k★), `wshobson/agents` (37.7k★), `davila7/claude-code-templates`/aitmpl (28.5k★), `VoltAgent/…subagents` (23.1k★), `cursor.directory` (~250k users/mo) | Attention, curation authority | — |
| **Upstarts / substitutes** | `claude-autopilot` (editable-markdown audit), first-party `/security-review`, dynamic workflows, hand-rolled `.claude/commands` | Own the audit-as-markdown pattern | — |
| **The "spreadsheets-and-interns" substitute** | A private running doc of prompts; copy-paste from HN; "just rerun it" | Good-enough, zero-setup | The real competitor — inertia, free |

Star counts and the aitmpl/wshobson/VoltAgent/awesome roster are as verified in `COMPETITIVE.md §1` (2026-07-09); goal-prompts itself = **0 stars, 0 forks** (`github.com/GhostlyGawd/goal-prompts`). The `claude-autopilot` and `/security-review` substitutes are documented in `DEMAND.md` (HN `item?id=48201112`; `github.com/anthropics/claude-code-security-review`).

### Money flows — margin concentrates two layers up from the niche
Reinforces `DEMAND.md`'s central finding: willingness-to-pay is proven and large, but it sits in the platform and the execution/outcome layers — **not** the catalog layer, which is $0 everywhere.

| Layer | Who pays whom | Typical price | Contract shape | Where the margin is |
|---|---|---|---|---|
| **Platform / harness** | dev or org → Anthropic / Anysphere / GitHub | Claude Code Pro **$20**/mo, Max **$100**/**$200**/mo, or API tokens **[secondary]** (`claude.com/pricing`); Cursor ~**$20**/mo + usage credits; Copilot Pro **$10** / Pro+ **$39** / Business **$19**/seat (`github.blog`, 2026) | per-seat subs **+ usage-based credits/tokens** | **Concentrated here.** Anthropic $14B run-rate; Claude Code alone **>$2.5B** run-rate (Feb 2026). Cursor ~$2B ARR |
| **Execution / outcome** (managed review) | org → CodeRabbit / Greptile / Qodo | CodeRabbit **$24**/**$48** seat; Greptile **$30** seat; Qodo **$0–45** seat (`DEMAND.md`, 2026-07-08) | per-seat SaaS, often billed on PR authors; free OSS tier | Real SMB→enterprise margin; CodeRabbit **15,000+** customers |
| **Prompt marketplace** | buyer → seller (rev-share) | PromptBase **$1.99–9.99**/prompt; Select **$14–19**/mo **[secondary]** | one-off + sub, platform cut | **Thin**; image/consumer-skewed, not coding-audit |
| **Catalog / command layer (this niche)** | **nobody pays** | **$0, MIT** | free `curl \| sh` / `/plugin install` | **~zero.** Side-channels only: sponsorship (VoltAgent is "sponsorship-funded"), jobs board (cursor.directory), private/team catalogs (`GOAL_PROMPTS_BASE`) |

Platform revenue is from Anthropic's own Series G page (`anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation`, 2026-02-12) and TechCrunch on Cursor (`techcrunch.com/2026/04/17/…`). The side-channel monetization read is `REVENUE.md §2` and `COMPETITIVE.md §5`.

### Channels & gatekeepers — how a catalog actually reaches a buyer

| Channel | Who controls the gate | How product reaches the buyer | Note |
|---|---|---|---|
| **GitHub star economy** | The awesome-list curators — `hesreallyhim` enforces an explicit *"quality, security, originality"* bar (`COMPETITIVE.md §1`) | Inclusion in an awesome-\* list; a visible star count | **0 stars = invisible.** The list is the front door (49.6k★) |
| **Claude Code plugin marketplace** | Anthropic's plugin spec | `/plugin marketplace add …` | First-party rail — *and* an absorption vector |
| **MCP registries** | Agentic AI Foundation / Linux Foundation; Glama; MCP.so | Catalog exposed as an MCP server + prompts | Official registry; Glama indexes **19,831+** servers, MCP.so **16,000+** **[secondary]** |
| **cursor.directory** | Community/Anysphere-adjacent; submit-on-site | Rules/MCP directory + jobs board | ~250k users/mo, 67k members (`COMPETITIVE.md §1`) |
| **Show HN / Product Hunt** | HN front-page rank; PH voters | Launch-day spike + backlink | The category's proof-of-life ritual |
| **VS Code marketplace / npm** | Microsoft; npm registry | Extension / `npx …` installer | aitmpl's `npx … --agent X --yes` one-item install is the norm |

### The jargon — the words that mark an insider (or an outsider)

| Term | What it means here | Outsider tell |
|---|---|---|
| **slash command / subagent / skill (`SKILL.md`) / hook / plugin** | The packaging formats a catalog ships in | Calling them "macros" or "scripts" |
| **MCP** | Model Context Protocol — the agent-native tool/prompt rail | Not knowing it's now Linux-Foundation-governed |
| **`CLAUDE.md` / rules / `.claude/commands` / dotclaude** | Where repo-level agent instructions live | — |
| **conductor / orchestrator / playbook** | A sequenced multi-brief/agent run | — |
| **harness / harness engineering** | Everything around the model: context, evals, verification, recovery | Thinking the *model* is the product |
| **context engineering** | Karpathy's sharper successor to "vibe coding" **[secondary]** | Still saying "prompt engineering" as a career |
| **vibe coding** | Coding by natural-language vibes (Karpathy, Feb 2025; Collins Word of the Year 2025) **[secondary]** | Using it as a compliment for production work |
| **spec-driven development (SDD) / EARS** | Spec as the executable artifact the agent builds and verifies against | — |
| **evals / LLM-as-judge** | How you prove the agent's output is good, not vibes | — |

The standalone **"prompt engineer"** title is *down ~30% since 2024* (`DEMAND.md` **[secondary]**) — using it unironically now marks you as a year behind the tribe's vocabulary.

### Buying rituals — how a purchase actually happens
Bottoms-up, product-led, almost never an RFP *at the catalog layer*. The motion: an **individual dev installs the free thing** (`curl | sh`, `/plugin install`, copy-paste) → shows the team → a **DevEx lead standardizes it** → **security/procurement can veto** on data-egress but cannot originate. There is **no trial** because there is no price — the "trial" *is* the product; RFPs and seat negotiations appear only **one layer over**, at CodeRabbit/Greptile enterprise. Referral is the dominant discovery act (an HN front page, a Reddit "how I use Claude Code" thread, an X post from a trusted voice). **Consequence:** you cannot sell into this niche, only get *installed*, then earn budget elsewhere. Metering anxiety (below) newly pulls **finance** into the room even for a $0 tool, because the agent it rides bills by the token.

### Weather — the last ~20 months, dated
Mood: **boom + consolidation + metering-anxiety.** The platform layer is a rocket; the harness layer is a knife-fight; users are twitchy about surprise bills and about the platform absorbing every primitive.

| Date | Event | So-what for this niche |
|---|---|---|
| Nov 2024 | Anthropic announces **MCP** (`blog.modelcontextprotocol.io`, "one year" post) | The catalog's agent-native distribution rail is born |
| Feb 2025 | Karpathy coins **"vibe coding"** **[secondary]** | The belief war (vibes vs. discipline) opens; goal-prompts sells discipline |
| Mar 2025 | **OpenAI adopts MCP**; Google DeepMind follows (Apr 2025) **[secondary]** | Cross-vendor — a catalog-as-MCP is viable beyond Anthropic |
| Jun–Jul 2025 | **Cursor usage-based pricing backlash** → public apology **Jul 4 2025** + refunds **[secondary]** | Bill-shock politicizes metering; *trust/no-surprises* becomes a wedge |
| Jul 11–14 2025 | **Windsurf saga**: OpenAI's ~$3B deal collapses (Microsoft IP rights), Google licenses tech for **$2.4B** + hires the CEO, **Cognition** buys the remainder — in ~72h (`techcrunch.com/2025/07/11/…`; `cnbc.com/2025/07/14/…`) **[secondary]** | Consolidation shock — the harness layer is not safe ground |
| Jul 14 2025 | **AWS Kiro** launches — a spec-driven agentic IDE (EARS; requirements/design/tasks.md) **[secondary]** | SDD goes mainstream; "the spec/brief *is* the artifact" validates goal-prompts' model |
| Aug 2025 | Anthropic ships **`/security-review`** (command + GitHub Action) (`DEMAND.md`) | First-party audit-prompt-as-feature — **platform absorption underway** |
| Nov 2025 | **Cursor $2.3B Series D @ $29.3B**; ships proprietary **Composer** model **[secondary]** | Platform margin concentrates; agents get their own models |
| Dec 9 2025 | Anthropic **donates MCP to the Agentic AI Foundation** (Linux Foundation; co-founders Anthropic/Block/OpenAI) (`anthropic.com/news/donating-the-model-context-protocol…`) | The rail becomes vendor-neutral infra — de-risks building on it |
| Feb 12 2026 | **Anthropic Series G: $30B @ $380B**; **$14B** run-rate; Claude Code **>$2.5B** (`anthropic.com/news/…series-g…`) | The platform is a giant; the catalog rides a rocket it doesn't own |
| Apr 2026 | **Cursor in talks: $2B+ @ $50B**; $2B ARR, forecasts **>$6B** by year-end (`techcrunch.com/2026/04/17/…`) | Agent spend is still compounding |
| Jun 1 2026 | **GitHub Copilot → usage-based AI Credits** (`github.blog`) | Metering is now *universal* across all three harnesses |
| Jun 29–Jul 2 2026 | **AI Engineer World's Fair**, SF; theme **"Harness Engineering"** (`ai.engineer/worldsfair/2026`) | The field names itself around *harnesses & context* — exactly what goal-prompts is |

---

## 2 · Watering holes directory — ranked by observed activity for *this* buyer

| # | Venue | Why it ranks | Link | Reachable this pass? |
|---|---|---|---|---|
| 1 | **Hacker News** — Show HN + "how do you actually use Claude Code" threads | Highest-signal density of the exact user + WTP language; every `DEMAND.md` quote lives here | `news.ycombinator.com/item?id=44362244`, `…=48311705`, `…=43412295` | ✓ (fetched in prior passes) |
| 2 | **r/ClaudeAI** (~**992K** members **[secondary]**, `subranking.com/subreddit/ClaudeAI`) | Largest single population of the exact user | `reddit.com/r/ClaudeAI` | ✗ reddit hard-blocks fetch |
| 3 | **r/cursor** (**144K** members, updated 2026-07-08 **[secondary]**, `gummysearch.com/r/cursor`) + **r/ChatGPTCoding** | Volume + candor; r/cursor's dominant discussion mode is literally *"pain & anger"* about the tool | `reddit.com/r/cursor` | ✗ blocked |
| 4 | **Anthropic Discord `#claude-code`** | Highest *density* of the exact user; where first-party changes land first (`DEMAND.md`) | `anthropic.com` → Discord | ✗ no public member count (blank spot) |
| 5 | **GitHub** — the awesome-\* lists' issues/PRs | The curation venue itself; `awesome-claude-code` alone shows ~590 open issues (`COMPETITIVE.md §8`) | `github.com/hesreallyhim/awesome-claude-code` | ✓ |
| 6 | **Latent Space** (swyx) newsletter + podcast (**10M+** readers/listeners in 2025 **[secondary]**) | Where the belief system is *set*; Simon Willison is a recurring guest | `latent.space` | ✓ |
| 7 | **X/Twitter** — Karpathy, Simon Willison, swyx, tool founders | Where the terms ("vibe coding," "context engineering") are *coined* | `simonwillison.net/2025/Mar/19/vibe-coding/` | ✓ |
| 8 | **AI Engineer World's Fair** (`ai.engineer`) | The annual physical gathering; the 2026 theme *is* "Harness Engineering" | `ai.engineer/worldsfair/2026` | ✓ |
| 9 | **cursor.directory** | The Cursor tribe's directory + jobs board (~250k users/mo) | `cursor.directory` | ✗ 403/429 (also blocked in `DEMAND.md`/`COMPETITIVE.md`) |

**Reading it:** the highest-*volume* venues (Reddit) are the ones you cannot fetch, and the highest-*density* one (the Discord) publishes no numbers — so first-hand discovery here still runs through **Hacker News + GitHub**, which is exactly where the loudest buyers already are.

---

## 3 · The unwritten rules

### Respect these (an entrant who breaks one is dismissed)
1. **The catalog price is $0, and it is not a pricing decision — it's a norm.** Every rival is free/MIT; PromptBase is the ceiling and it's pocket-change and off-topic (`DEMAND.md`). Charging for brief *access* is both forkable and goodwill-poisoning (`REVENUE.md §2`, `COMPETITIVE.md §9`). Money is earned **adjacent** — sponsorship, jobs, teams/private catalogs, or the execution outcome — never at the tollgate.
2. **Distribution is a star economy, and the awesome-list is the border control.** 49.6k / 37.7k / 28.5k / 23.1k-star incumbents own the front door; a catalog at **0 stars is invisible** until a curator or an HN front page anoints it. You earn attention *before* you earn anything else — the headline gap in this category is distribution and proof, not features (`COMPETITIVE.md §1`).
3. **Trust and privacy are load-bearing product, not fine print.** "Nothing leaves your machine," no signup, *readable markdown not a black box* (`claude-autopilot`'s exact pitch, `DEMAND.md`). After Cursor's 2025 bill-shock and in a now-universally-metered world, no-surprises provenance is a feature. Break it and the tribe turns — r/cursor's dominant register is already *"pain & anger."*

### Exploit these (beliefs that look ripe to be wrong)
1. **The tribe is quietly abandoning "prompt," and goal-prompts is still standing under it.** The field renamed itself **"harness engineering"** and **"context engineering"** (the 2026 conference theme; Karpathy's own pivot); the "prompt engineer" title is down ~30%. goal-prompts *is* harness/context content mislabeled as a "prompt catalog." Re-badge toward **briefs / audits / evidence** — the words `COMPETITIVE.md §7` already found unowned.
2. **Everyone sells the prompt; nobody owns what happens *after* the run.** The niche's loudest unmet request — reusable, shareable workflows that produce *consistent output* — is aimed **at Anthropic**, not a vendor (`DEMAND.md` Sub-pain C). The report → checklist → commit loop (Report Studio → 47 · The Fixer → FIXLOG) is empty territory every rival leaves vacant (`COMPETITIVE.md §6`).
3. **"More = better" is the incumbents' sacred cow, and their own users are goring it.** 154 subagents, 92 plugins, 100+ templates — and the top recurring complaints are *sprawl, uninstall, and inventory* pain (`COMPETITIVE.md §8`). A **machine-enforced quality bar** (goal-prompts' linter: 4-phase skeleton, ask-first gate, 4k cap, CI-gated) is a counter-belief **no rival can claim**. The status marker to flip: from *catalog size* to *verified curation*.

---

## 4 · Open questions — what only real customer conversations can answer

1. **Will anyone pay for anything here — and for exactly what?** Private/team catalogs, setup+support, or sponsored placement — vs. taking the free fork. `DEMAND.md` found near-zero "I'd pay for a prompt catalog" language; `REVENUE.md` says the rails are "built now, sold later." **Only 10 DevEx/platform leads on the record settle it.**
2. **Does "audit / brief" actually re-frame the buyer, or do they hear "just another awesome list"?** The positioning bet in §3 is untested against a real Claude Code user's ear. Interviews/user tests only.
3. **How many quarters until Anthropic absorbs this?** `/security-review` + dynamic workflows already gesture at a first-party audit-workflow catalog. Whether that's imminent is knowable only from people close to the platform (the Discord, DevRel).
4. **Who truly holds the pen — the individual dev (who won't pay) or the DevEx lead (who buys outcomes like CodeRabbit)?** The whole niche turns on this buyer≠user split, and it can't be resolved from public pages.

**Honest blank spots (the silence test):** **reddit and cursor.directory hard-block fetch** (confirmed again this pass, consistent with `DEMAND.md`/`COMPETITIVE.md`) — so all Reddit and directory figures above are `[secondary]` counts, not first-hand thread text or live stats. **No public Anthropic Discord member count** exists to rank it precisely. **No independent G2/Capterra-style reviews of prompt catalogs exist** — the category is too young and too free to have a review economy. And **later-2026 Cursor mega-round / acquisition rumors** (a widely-circulated "SpaceX $60B" claim) **could not be verified from any primary source** and are deliberately excluded — the last verifiable Cursor fact is the April 2026 TechCrunch "$2B+ at $50B, in talks."

*Report only — which threads should we pull next?*
