# MARKET.md
*Produced by brief 64 · Market Size & Timing, run against **this repo's own venture: goal-prompts — a catalog of structured audit briefs for coding agents.** Bottom-up from NICHE.md + COMPETITORS.md; DEMAND.md fixes where WTP actually sits. All sources accessed 2026-07-10 unless dated otherwise. Directly-fetched primaries unmarked; analyst/market figures and web-search synthesis marked **[secondary]**.*

**Date:** 2026-07-10

This market has two floors and they are priced differently, so the report models both and never lets one launder the other. **The catalog layer goal-prompts occupies has a dollar-TAM of $0** — it is MIT/free, and every rival is too (DEMAND.md, COMPETITORS.md price row); the "market" there is *attention*, denominated in stars and installs, not revenue. The monetizable market is **one layer over** — the team-audit / managed-review outcome DEMAND.md located WTP in — and that is where the arithmetic below spends its effort.

---

## Phase 1 — The unit

**Buyer unit (dollar side):** not the individual developer. DEMAND.md's central finding is that the individual dev *adopts but does not pay*, and NICHE.md's buyer≠user split says the pen is held by a **DevEx/platform lead or eng manager at a software team that already pays for AI coding tooling** and buys *outcomes* (CodeRabbit-shaped), not text. For goal-prompts specifically that buyer resolves into two SKUs already scaffolded in REVENUE.md: **(A)** a *team-audit / private-catalog engagement* (setup + custom linted briefs + standing CI audits + support — flat fee, deliberately **not** per-seat metered), and **(B)** a *sponsored/collab playbook* bought by a dev-tool marketing budget against goal-prompts' audience.

**Annual-value hypothesis per unit** — anchored on what the team-audit outcome *actually* commands today, revealed by CodeRabbit's own ARR ÷ customers:

| Anchor | Arithmetic | $/customer/yr | Source |
|---|---|---|---|
| CodeRabbit, Sept 2025 | $15M ARR ÷ 8,000 businesses | **≈ $1,875** | `techcrunch.com/2025/09/16/coderabbit-raises-60m-valuing-the-2-year-old-ai-code-review-startup-at-550m/` (fetched) |
| CodeRabbit, 2026 (all customers) | $40M ARR ÷ 15,000 customers | **≈ $2,667** | Sacra (fetched) + `coderabbit.ai` hero (COMPETITORS.md) |
| CodeRabbit, 2026 (paying only) | $40M ARR ÷ 8,000+ paying | **≈ $5,000** | Sacra (fetched) |

So the team-audit outcome commands **≈ $1,900–5,000/customer/yr** in the open market. goal-prompts' lighter offering (setup + support + private catalog, not a managed PR pipeline) plausibly captures a fraction: **$1,000–3,000/team/yr** (SKU A). SKU B (sponsorship) anchors on dev-media placement rates and VoltAgent's sponsor-funded model (COMPETITORS.md): **$500–2,500/placement**, a handful/yr.

**Countable proxies gathered (someone could enumerate these):**

| Countable | Value | Date | Source |
|---|---|---|---|
| Developers on GitHub | **180M+** (+36M/yr, +23%, "one/second") | Octoverse 2025 | `github.blog/…octoverse-a-new-developer…` (fetched) |
| GitHub Copilot total users / paid | **~20M / 4.7M paid** (+75% YoY) | Jul 2025 / Jan 2026 | `getpanto.ai`, `axis-intelligence.com` **[secondary]** |
| Copilot enterprise customers | **~77,000** | FY2024 | `getpanto.ai` **[secondary]** |
| Cursor active devs / businesses / ARR | **~4M / 50,000 / $2B ARR** | Dec 2025–Apr 2026 | `getlatka.com`, `getpanto.ai` **[secondary]**; ARR per NICHE.md (`techcrunch` Apr 2026) |
| Claude Code weekly-active devs | **2M+** (doubled since Jan 1 2026) | Feb 2026 | Anthropic via `linkedin.com/…gptproto` **[secondary]**; run-rate >$2.5B primary (NICHE.md) |
| CodeRabbit customers / paying | **15,000 / 8,000+ paying** | 2026 / Sept 2025 | `coderabbit.ai`, `techcrunch`, Sacra (fetched) |
| Incumbent catalog stars (attention TAM) | **~139k combined** | 2026-07-10 | GitHub API (COMPETITORS.md, fetched) |
| MCP monthly SDK downloads / servers | **97M/mo / 10k+** | Mar 2026 | `digitalapplied.com` **[secondary]**; registry primary (NICHE.md) |
| goal-prompts stars | **0** | 2026-07-10 | `github.com/GhostlyGawd/goal-prompts` |

---

## 1 · The arithmetic

### The two markets, kept separate

| Layer | What it is | Dollar size | How measured |
|---|---|---|---|
| **Catalog TAM** (where goal-prompts sits) | Free, MIT audit-brief catalogs | **$0** | Attention: ~139k combined stars on the four incumbents (awesome-claude-code 49,729 + wshobson 37,762 + aitmpl 28,745 + VoltAgent 23,154 — COMPETITORS.md). goal-prompts = **0**. |
| **Monetizable SAM** (one layer over) | AI code review / team-audit outcome | **$400–600M ARR** narrow **[secondary]**; served proxy CodeRabbit $40M + Greptile + Qodo | Dollars: per-seat/credit subscriptions to teams |

The number to never blur: **the catalog TAM is $0 in revenue.** Everything monetizable requires crossing into the layer over, which is what the funnel below models.

### Top-down bound (used only to cap the bottom-up — no analyst-deck theater)

- **Narrow AI-code-review market: ~$400–600M ARR (2026)** **[secondary]** — tools whose primary job is AI PR review. CodeRabbit alone is $40M of it (~7–10%), growing **700% YoY / 20% per month** (Sacra; TechCrunch). This is the honest SAM ceiling for the outcome goal-prompts' wedge points at.
- **Broader AI-code-review-and-analysis: $2–3B, 30–40% CAGR** **[secondary]** (adds SonarQube/Snyk/Semgrep-class tools). **Comprehensive AI code tools: $9.35B (2026)** **[secondary]** (adds codegen) — outer bound only; most of it is not "audit."
- **Pool of orgs already paying for AI-dev tooling** (the addressable-org denominator, summed from countables): Cursor **50,000** businesses + Copilot **~77,000** enterprise + CodeRabbit **15,000** ≈ **~140,000 org-relationships** buying AI coding/review today. Overlapping, but order-of-magnitude **~10⁵ orgs** with proven budget and behavior.

### Bottom-up SOM — the wedge funnel (every multiplication written out)

goal-prompts is at **0 stars / 0 forks today** (COMPETITORS.md). Every dollar is gated on first earning distribution, so the model is an honest funnel, not a TAM slice. Four inputs, each a range (bear → bull):

**Step 1 — Installs reached in the wedge.** Ceiling anchored on comparable catalogs: awesome-claude-code did 0→49,729★ in ~15 months, but that is *the* outlier; the base rate is a catalog that never clears 1,000. A 0★ entrant executing distribution well:
- Year 1: **1,000 → 5,000** installs (bull assumes an HN front page + awesome-list inclusion — NICHE.md's border control).
- Year 2: **5,000 → 25,000** installs (bull assumes compounding attention).

**Step 2 — Share of installs that are a team with budget.** Copilot converts ~20M users → 4.7M paid (**~23%** to *any* paid, first-party with a credit-card wall); Cursor ~1M DAU → 50k businesses. A free catalog with no wall and near-zero "I'd pay" language (DEMAND.md) is far below that: assume **2% → 5%** of installs are an org that would consider a paid engagement.

**Step 3 — Conversion of those teams to a paid engagement.** Free-catalog→paid-adjacent conversion is essentially unmeasured and, per DEMAND.md's silence test, near-zero today: assume **5% → 20%**.

**Step 4 — × annual value** = **$1,000 → $3,000/team/yr** (SKU A, from Phase 1).

**Worked lines:**

| | Installs | × team-share | × convert | = teams | × $/yr | SKU A | + Sponsorship (SKU B) | **Year total** |
|---|---|---|---|---|---|---|---|---|
| **Y1 bear** | 1,000 | 2% = 20 | 5% = **1** | 1 | $1,000 | $1,000 | ~$0–2k (1 backer) | **≈ $0–3k** |
| **Y1 bull** | 5,000 | 5% = 250 | 20% = **50** | 50 | $3,000 | $150,000 | 4 × $2,000 = $8k | **≈ $158k** |
| **Y2 bear** | 5,000 | 2% = 100 | 5% = **5** | 5 | $1,000 | $5,000 | ~$2k | **≈ $7k** |
| **Y2 bull** | 25,000 | 5% = 1,250 | 20% = **250** | 250 | $3,000 | $750,000 | 12 × $2,500 = $30k | **≈ $780k** |

**Obtainable market, stated as a range (Phase 3):**
- **Year 1: ≈ $0 – $158k.** Expected value sits near the **low end** — the bear (installs stall near 0★, conversion ≈0) is the *base rate* for a new catalog, and DEMAND.md's evidence points hard at the bear's conversion input.
- **Year 2: ≈ $7k – $780k.** The bull is only reachable if Step 1 *and* Step 3 both break in goal-prompts' favor — escaping 0★ **and** proving non-zero catalog→paid conversion, two things the evidence says are individually hard.

**Sanity vs top-down:** even the Y2 bull ($780k) is **0.13–0.20%** of the $400–600M narrow SAM ($780k ÷ $500M = 0.16%). That is an appropriately tiny slice for a 0★ entrant with no PMF proof and a free core — the bottom-up does **not** overshoot the top-down; the large gap between them *is the distribution/conversion chasm*, not a modeling error. If the bottom-up had produced 5% of SAM from 0 stars, that would be the vibe the brief warns against.

---

## 2 · Growth and timing

**Growth reading (the countables, directionally):** every input is pointing up and to the right. Developers: **180M on GitHub, +36M/yr (+23%), one new every second** (Octoverse 2025). AI-coding adoption: **~80% of new GitHub devs used Copilot in week one**; Copilot **4.7M paid (+75% YoY)**; Cursor **$0→$2B ARR in <24 months** (fastest B2B SaaS ever claimed); Claude Code **WAU doubled since Jan 1 2026**, run-rate **>$2.5B**. Money into the *exact adjacent layer*: **CodeRabbit $60M Series B @ $550M (Sept 2025), $40M ARR +700% YoY**; Greptile Series A (Benchmark, ~$180M val); Qodo $40M Series A. The rail: **MCP 97M SDK downloads/mo (Mar 2026)** from ~2M at launch **[secondary]**. The attention pool: catalog stars **0→49k in 15 months**. Nothing here is flat.

**Why-now vs. its strongest rebuttal — side by side:**

| **Why now (bull)** | **Why not / rebuttal (bear)** |
|---|---|
| **The buyer got created and funded 2025–26.** CodeRabbit went $5M→$40M ARR in 12 months (700%); the team-audit outcome is a *proven, growing* line item now, not a 2023 hypothesis. | **Same wave = platform absorption.** Anthropic ships `/security-review` (Aug 2025), Agent Skills, and dynamic workflows (May 2026); the primitive goal-prompts catalogs is being pulled first-party *for free* (DEMAND.md Sub-pain C, NICHE.md weather). Why-now for the buyer is why-now for Anthropic to eat it. |
| **The distribution rail exists and is neutral.** MCP born Nov 2024, donated to the Linux Foundation Dec 2025, 97M downloads/mo — a vendor-neutral, agent-native catalog channel that did not exist three years ago. **[secondary]** | **The rail is owned by the absorbers.** MCP registries + the plugin/skill spec are controlled by the same platforms (Anthropic/Cursor/GitHub) that could reprice or bundle the layer overnight (concentration risk, §3). |
| **The install base crossed mass adoption.** Copilot Free (Dec 2024) → 36M new devs; 2M+ Claude Code WAU. There is finally a large population running agents on *their own repos*. | **WTP stayed at the execution layer, not the catalog.** The "now" that made catalogs *viable* also made them a **$0 commodity** — 139k stars, all MIT (DEMAND.md). What opened is an *attention* window, not a *revenue* one. |
| **The field named itself.** "Harness/context engineering" is the AI Engineer World's Fair 2026 theme; "audit/brief/evidence" is an unowned register (COMPETITORS.md). Category-noun land-grab is live. | **The complaint vocabulary is calm.** People who "keep a running doc of prompts" describe a solved-enough papercut, not an open wound (DEMAND.md). Calm papercuts don't open wallets. |

**Why not before (constraint check):** pre-2024 there was **no agent-native distribution rail** (MCP is Nov-2024), **no mass base of devs running coding agents on their own repos**, and **no proven team-audit buyer**. The prior attempt at "sell the prompt" — PromptBase — stalled at $1.99–9.99, consumer/image-skewed, and is now pivoting away from prompt-sales (COMPETITORS.md **[secondary]**). The constraint that killed it: *prompts are forkable text with no execution/outcome attached and there was no install base to distribute into.* **Half that constraint is now gone** (the rail and the install base exist); **the other half is not** — prompts are still free/forkable text (the MIT norm is structural, DEMAND.md/REVENUE.md). So the *adjacent* constraint lifted; the *catalog-monetization* constraint did not. That asymmetry is the whole investment case and the whole bear case at once.

---

## 3 · The window

**Mover-advantage verdict: real but narrow and time-boxed — first-mover matters only for the category noun and the post-run loop; on the brief *format*, fast-follow is the smarter seat.**

Reasoning, by what actually compounds:
- **The brief format has no moat** — a 4-phase skeleton is copyable in days, and COMPETITORS.md's kill-zone analysis says aitmpl/wshobson could add "audit" agents fast. Being first to *a format* buys nothing.
- **What does compound is distribution + a category noun + the enforced-curation/post-run loop.** The star economy is a genuine network effect (awesome-claude-code's 49k is a moat *as the list*), and "audit/brief/evidence" plus the **report→Studio→Fixer→FIXLOG** loop is territory every rival leaves vacant (COMPETITORS.md gap analysis). First-mover advantage is *real* here — but only if the flag is planted **loudly, before Anthropic ships a first-party audit-workflow catalog** (the most-lethal kill-zone entry, "weeks-to-quarters"). Miss that window and fast-follow — or the platform — takes the seat.
- **Net:** the compounding asset is brand/distribution and the loop, not the prompts. The window is open *now* and closes the quarter Anthropic decides to own "audits." Speed on positioning beats completeness on catalog size.

**Concentration risk — five big ones, not a thousand small checks.** At the catalog layer the *users* are a thousand small free installs (no revenue, no concentration). But every monetizable path is **dangerously platform-concentrated**: every brief run rides Anthropic/Cursor/Copilot **metered tokens**; the distribution rails (MCP registry, plugin/skill spec) are platform-controlled; and sponsorship revenue (SKU B) concentrates on a handful of dev-tool advertisers. **One Anthropic product decision** — ship a first-party audit catalog, or change the skill spec — reprices the entire market overnight. This is the opposite of a resilient many-small-buyers market; the repricing power sits with ~5 actors (Anthropic, Anysphere/Cursor, GitHub/Microsoft, and the top sponsors).

---

## 4 · Sensitivity

**The single assumption that most changes the answer: does free-catalog attention convert to paid-adjacent dollars *at all* (>0%) — Step 3.**

It beats even the distribution input (Step 1) as the swing variable, for a specific reason: the two inputs fail *differently*. Step 1's plausible range is "small vs. medium" (1k vs. 25k installs — a 25× swing on the top line, but still a *number*). **Step 3's bear value is not small — it is structurally zero**, and it is the input with the most disconfirming evidence behind it: DEMAND.md's silence test found **near-zero "I'd pay for a prompt catalog" language anywhere**, and REVENUE.md rules brief-access paywalls both forkable and goodwill-poisoning. If catalog→paid conversion is truly ~0%, then **every row of the funnel collapses to $0 of SKU A regardless of how good distribution gets** — the "monetizable market one layer over" becomes reachable only by *becoming an execution product* (a different company, different report), and goal-prompts' entire obtainable market shrinks to **sponsorship + gratitude (SKU B + backers), i.e. low-four-to-five figures at best**, forever.

Concretely: hold the Y2-bull installs (25,000) and team-share (5%) fixed and vary *only* conversion:
- conversion **20%** → 250 teams → **$750k** SKU A.
- conversion **5%** → 63 teams → **$189k**.
- conversion **0%** (the DEMAND.md-implied floor) → **$0** SKU A — the whole thesis is null on the dollar side.

Distribution (Step 1) is the *gate*; conversion (Step 3) is the *cliff*. If I get one number right before spending a dollar, it is whether a single team will pay for the outcome — which is exactly the open question NICHE.md flagged that only real customer conversations can answer.

**Honest evidence gaps:** goal-prompts' own install/conversion data does not exist (0★, no analytics — REVENUE.md/FUNNEL.md), so Steps 1–3 are reasoned from comparables, not measured. Copilot/Cursor/Claude Code user counts are **[secondary]** aggregator figures (the vendors publish few hard primaries); the AI-code-review market sizes are **[secondary]** analyst ranges used only to bound. CodeRabbit's ARR/customer split is the firmest anchor (TechCrunch + Sacra, fetched). Reddit/directory install counts remain unfetchable (consistent with the companion reports).

*Report only — do size and timing justify the next brief?*
