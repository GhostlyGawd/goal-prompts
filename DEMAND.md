# DEMAND.md
*Produced by brief 62 · Pain & Demand Mining, run against **this repo's own venture: goal-prompts — a catalog of structured audit briefs (reusable prompts/slash-commands) for coding agents.** This is the venture dogfooding itself on its own market, not the flaky-test sample under `examples/venture/`. All sources accessed 2026-07-08. Claims from directly-fetched primaries are unmarked; claims from general-web search synthesis are marked **[secondary]**.*

## The pain hypothesis
Developers running coding agents (Claude Code, Cursor, Copilot) point the agent at their own repo to audit or improve it — and get **inconsistent, shallow, unrepeatable results**, because they hand-write one-off prompts from scratch each session. Who hurts: individual developers and small teams using agentic coding tools, plus the DevEx/platform engineers who own code quality. When: **per session, per repo, per PR** — a recurring tax, not an occasional one. Doing what: writing ad-hoc audit/review prompts, keeping private prompt docs, copy-pasting from "awesome" lists. The pain goal-prompts targets: **there is no structured, repeatable, evidence-producing catalog of audit workflows to aim the agent at.**

Where evidence would live if this were real (the search plan): GitHub "awesome" lists and dotfiles repos of `.claude/commands`; Hacker News "how do you use it" threads; r/ClaudeAI, r/cursor, r/ChatGPTCoding; prompt marketplaces (PromptBase); the pricing/adoption pages of AI code-review vendors (CodeRabbit, Greptile, Qodo); and first-party primitives (Anthropic slash commands, Cursor rules).

## The evidence wall

### Sub-pain A — Without structure, agent output is "random" (severity markers)
From *Ask HN: How Do You Actually Use Claude Code Effectively?* (`https://news.ycombinator.com/item?id=44362244`, 2025-06-24):
- **sukit:** *"about 50% of the time, the result is so messy that cleaning it up takes more time than just writing it."* — the sharpest severity marker in the set: the tool is net-negative half the time without discipline.
- **achempion:** *"Is it possible to develop an intuition where it would do a decent job … or the result is always random?"* — trust erosion, stated as a question.
- **rajeshpatel15:** *"Be uncomfortably explicit in prompts: Claude Code in particular is very sensitive to ambiguity."* — the fix *is* structure; the pain is its absence.

### Sub-pain B — Developers hand-roll their own prompt/command libraries (the workaround census)
Every one of these is a purchase order for a curated catalog — people are already building it themselves, one repo at a time:
- **sukit** (same thread, 2025-06-24): *"I keep a running doc of prompts that work well and bad habits to avoid."*
- **sminchev**, *AI Isn't Bad. Your Prompts Are* (`https://news.ycombinator.com/item?id=47508529`, 2026-03-24): *"When working with Claude Code, I usually save my prompts in slash commands. Instead of writing the prompts, I call the slash command."*
- **idopmstuff**, *Agent Skills* (`https://news.ycombinator.com/item?id=46872620`, 2026-02-03): *"I set up slash commands for each of them. Each slash command starts by reading from a .md file of instructions."*
- **jamesponddotco**, *Getting good results from Claude Code* (`https://news.ycombinator.com/item?id=44840334`, 2025-08-08): *"Eventually, I need to come up with a 'dotclaude' repository with these and a few others I use."* — someone narrating the exact artifact goal-prompts ships.
- **iBelieve**, *Schedule tasks on the web* (`https://news.ycombinator.com/item?id=47539320`, 2026-03-27), pasting his real daily audit prompt: *"Please look at the commits on the `develop` branch from the previous day … see if there are any newly introduced bugs, sloppy code, missed functionality, poor security, missing documentation, etc."* — an ad-hoc version of a goal-prompts brief, run daily.

**The census at scale (GitHub star counts, authoritative via GitHub API, 2026-07-08):**
- `hesreallyhim/awesome-claude-code` — **49,183 stars**, 4,283 forks; created 2025-04-19 (≈49k stars in ~15 months) — `https://github.com/hesreallyhim/awesome-claude-code`
- `VoltAgent/awesome-claude-code-subagents` — **23,010 stars** — `https://github.com/VoltAgent/awesome-claude-code-subagents`
- `rohitg00/awesome-claude-code-toolkit` — **2,278 stars**, self-described "135 agents, 35 skills, 42 commands, 176+ plugins…" — `https://github.com/rohitg00/awesome-claude-code-toolkit`
- `cursor.directory` — **48,000+ developers / 68,700 members** curating shareable rules & MCP configs **[secondary]** — `https://cursor.directory/`

### Sub-pain C — Unmet demand for *shareable, repeatable, consistent* workflows (and the platform is already moving in)
From *Dynamic Workflows in Claude Code* — the HN thread on **Anthropic's own** launch post (`https://news.ycombinator.com/item?id=48311705`, 2026-05-28; story: `https://claude.com/blog/introducing-dynamic-workflows-in-claude-code`):
- **stvpwrs:** *"Will workflows be reusable? I have a big use case of sharable and repeatable workflows for projects."*
- **rsstack:** *"Will you document how to (AI-)author and share reusable workflows between team members, to ensure some consistency of quality?"*
- **vblanco**, on the same job-to-be-done: *"applying the same prompts across a whole codebase or just in parallel."*

That the loudest requests here are aimed *at Anthropic* is the tell for the counter-read: the primitive is being pulled into the platform. **Anthropic already ships `/security-review`** as a built-in slash command **and** a GitHub Action (since 2025-08-06), customizable by copying `security-review.md` into `.claude/commands/` — i.e., a first-party audit-prompt-as-feature, free, using goal-prompts' exact distribution model (`https://github.com/anthropics/claude-code-security-review`).

A live competitor validating the same "audit = editable markdown phases" model — **axledbetter01**, *Show HN: claude-autopilot* (`https://news.ycombinator.com/item?id=48201112`, 2026-05-19): *"Every phase is an editable markdown skill. Not a black-box pipeline … plain markdown you can read in 5 minutes, audit, edit, swap any phase."*

## Spend and workaround table
The job-to-be-done — "have my codebase automatically audited/reviewed" — is monetized heavily. The catch: the money sits in the **execution layer**, one step over from the **prompt/catalog layer** goal-prompts occupies.

| Solution | Layer | Price signal | Adoption signal | Source (2026-07-08) |
|---|---|---|---|---|
| **CodeRabbit** | Execution (managed PR review) | Free · **$24**/user/mo (Pro) · **$48**/user/mo (Pro+) · Enterprise custom | **"6M Repositories," "75M Defects found," "Trusted by 15,000+ customers," "Most installed AI App"**; *"We're using CodeRabbit all over NVIDIA" — Jensen Huang* | `coderabbit.ai` + `coderabbit.ai/pricing` |
| **Greptile** | Execution (codebase-graph review) | Free (50/mo) · **$30**/user/mo | Series A led by Benchmark; **~$180M valuation**; YC-incubated **[secondary]** | `costbench.com/software/ai-code-review/greptile/` |
| **Qodo** (ex-CodiumAI) | Execution (rules-based review) | $0–**$45**/user/mo | Case study: *"saved over 450,000 developer hours in a year at a Global Fortune 100 retailer"* **[secondary]** | `baeseokjae.github.io/posts/ai-code-review-tools-2026/` |
| **PromptBase** | Prompt (marketplace) | Prompts **$1.99–$9.99**; Select sub **$14–19**/mo | Top sellers report **$500–$5,000/mo**; catalog skews image/consumer, thin on coding **[secondary]** | `promptbase.com/marketplace` |
| **awesome-* lists / `/security-review` / hand-rolled `.claude/commands`** | Prompt (the status quo) | **Free** | 49k+23k+ stars; first-party & DIY | GitHub, above |

**Reading the table:** willingness-to-pay is *proven* and *large* — but for **outcomes** (CodeRabbit at 15,000+ paying customers, Greptile at a $180M valuation), not for **prompts**. The prompt/catalog row is entirely free. PromptBase is the one place prompts are sold, and it monetizes at pocket-change and skews away from coding.

### The remaining lenses, quickly
- **Search & hiring signals:** the standalone "prompt engineer" title is **down ~30% since 2024**, while roles *requiring* prompt-engineering skills are up **~3×** **[secondary]** — the skill is diffusing into every dev job, not concentrating into a buyable role. Bullish on ubiquity of the pain; bearish on "prompts" as a standalone product line.
- **Frequency & trigger:** strong and recurring — per-session, per-repo, per-PR; iBelieve reviews *"the previous day"*'s commits (daily); CodeRabbit fires per-PR. This pain has the recurring trigger that pain-without-a-trigger lacks.
- **The silence test:** two loud absences. (1) **Reddit and the review sites (G2/Capterra) were unreachable this pass** — reddit hard-blocked fetch, cursor.directory rate-limited (HTTP 429) — so this wall leans on Hacker News + GitHub + vendor primaries; independent dated review-site complaints are a genuine gap. (2) The more damning silence: **nobody is asking to *buy* a prompt catalog.** The sentiment is uniformly *"I built my own slash commands,"* never *"I wish someone sold me these."* Absence of willingness-to-pay language, exactly where it should appear, is data.

## The verdict (graded, arithmetic visible)
- **Severity: Medium.** Real friction and trust erosion (*"always random,"* *"50% … messy"*), but the prevailing vocabulary is workaround-**calm** (*"I usually save my prompts in slash commands"*), not nightmare/compliance/losing-revenue language. People route around this papercut placidly.
- **Frequency: High.** Per-session / per-repo / per-PR / daily. Best-scoring dimension.
- **Evidence density: Medium–High.** 12 dated verbatim quotes + 49k/23k-star workarounds + hard primary spend numbers — but thin on independent review-site complaints (blocked) and near-zero direct "I'd pay for a prompt catalog."
- **Spend proof: Split — High for the execution layer, ~Zero for the catalog layer.** CodeRabbit/Greptile/Qodo prove teams pay $24–48/dev/mo for the *outcome*; the *prompts* that produce it are free everywhere goal-prompts would compete.
- **Rough grade = Medium × High × Medium–High × (High execution / ~Zero catalog) → real, frequent, monetized pain — but the money is one layer over from where a free prompt catalog sits.** Verbatim echo of the sample's ruling: *promising pain, contested monetization.*

## The honest counter-read (equal weight)
The same evidence reads cleanly as **"real pain, not a company":**
1. **The workaround is free, excellent, and abundant.** A 49k-star hand-curated list, a 23k-star subagent collection, cursor.directory, and first-party `/security-review` all cost $0. A free catalog competing against free catalogs has no pricing power, and goal-prompts is itself MIT-licensed and free — there is no revenue line to defend.
2. **WTP lives in execution, not text.** Buyers pay CodeRabbit/Greptile for the managed pipeline, the bug-catch rate, the PR integration — none of which a markdown catalog provides. The prompt is the commodity; the moat is the machinery around it.
3. **Platform absorption is underway** (the flaky-test-in-CI pattern, repeating). Anthropic ships `/security-review`, Agent Skills, and **dynamic workflows**; Cursor ships rules + a directory. The primitive goal-prompts catalogs is being pulled into the platforms for free — and the users in Sub-pain C are asking *Anthropic*, not a third party, to build it.
4. **The complaint vocabulary is calm.** People who *"keep a running doc of prompts"* are describing a solved-enough annoyance, not an open wound. Calm papercuts don't open wallets.
5. **PromptBase is the ceiling, and it's low.** The one dedicated prompt marketplace clears $1.99–$9.99 a prompt and skews to image/consumer work — the closest proxy for "will devs pay for prompts" says: barely.

The bull's fair rebuttal, for balance: the sheer **72,000+ combined stars** on curated agent-resource lists is enormous *attention* and proof of a real job-to-be-done; a catalog that is genuinely better — evidence-producing, composable, agent-native over MCP, with an **execution bridge (Report Studio → 47 · The Fixer)** that turns reports into commits — could win distribution and then monetize the *execution* layer it already reaches, plus private/team catalogs. Notably, goal-prompts already has that bridge; the layer that monetizes is the one it half-built.

## The ten people (where to find ten sufferers to talk to this week)
1. **The HN commenters themselves** — sukit, jamesponddotco, sminchev, stvpwrs, rsstack — all reachable via their HN profiles on the threads above.
2. **Contributors and issue-openers on `hesreallyhim/awesome-claude-code`** (584 open issues) — people actively curating commands right now.
3. **`cursor.directory` rule submitters** — they've already published a reusable prompt; ask what they wish existed.
4. **Authors of public `dotclaude` / `.claude/commands` repos** — GitHub code search for `.claude/commands` surfaces developers who built exactly this by hand.
5. **`claude-code-templates` / plugin-registry publishers** — distribution-minded builders in the same lane.
6. **DevEx/platform engineers at CodeRabbit/Greptile customers** — they bought the *outcome*; find them via those vendors' public case studies and engineering blogs.
7. **The Anthropic Discord `#claude-code` channel** — highest-density population of the exact user.
8. **r/ClaudeAI and r/cursor "how do you use it" thread posters** — once reachable; the silence-test gap to close first.
9. **`claude-autopilot` (and similar Show HN) users** — they chose an *editable-markdown-audit* product; ask why, and what's missing.
10. **Maintainers who committed a `CLAUDE.md` + `.claude/commands/` to a public repo** — GitHub code search; they've paid the DIY cost this catalog would erase.

---

*Report only. The pain is real and recurring and the spend is proven — but it sits one layer over (execution/outcomes), not on the prompt catalog itself. Should we **proceed** (build toward the execution/outcome wedge the Fixer already gestures at), **pivot the pain** (e.g. from "catalog of prompts" to "managed audits/team catalogs that monetize the outcome"), or **drop it** (free workarounds are good enough and the platforms are absorbing the primitive)?*
