# MOAT.md
*Produced by brief 66 · Moat & Model Check, run against **this repo's own venture: goal-prompts — a catalog of structured audit briefs for coding agents.** Premises from POSITIONING.md (wedge) + NICHE.md (rituals) + COMPETITORS.md (incumbent moats) + MARKET.md (napkin inputs). All sources accessed 2026-07-10 unless dated otherwise. Directly-fetched primaries unmarked; web-search synthesis marked **[secondary]**.*

**Date:** 2026-07-10

## Premises carried in (Phase 1)

- **Wedge (POSITIONING.md):** Option A — *own the audit loop*. Beachhead = burned solo dev / OSS maintainer; against-frame = *doing nothing well* ("just rerun it"); category = niche-of-one "audit briefs"; onlyness = *the only audit catalog that files a report you can diff and re-run, then carries the finding to a fix log.*
- **Pricing posture (POSITIONING.md §L6, REVENUE.md §2):** **$0 catalog forever**, monetize **adjacent**. Two scaffolded SKUs — **A** = flat team-audit (private catalog + custom linted briefs + standing CI audits + support, *not* per-seat); **B** = sponsored/collab playbooks (already built in `playbooks.json`).
- **Buying rituals (NICHE.md §1):** bottoms-up PLG — install free → show the team → DevEx lead standardizes → security/procurement can only veto. **No trial because no price**; you cannot *sell* into the catalog layer, only get *installed*, then earn budget adjacent. $0 is a **norm, not a decision**; trust ("nothing leaves your machine") is load-bearing product.
- **Incumbent moats (COMPETITORS.md):** CodeRabbit — 15k customers + PR integration + per-repo "Learnings" data + brand (*real, mild*). Free catalogs — the 49k-star network effect (*real, brand*). Anthropic `/security-review` + Agent Skills + dynamic workflows — **owns the rail** (*the only deep moat, and the absorption threat*). The brief **format**: forkable in days, MIT.
- **Revenue-model candidates (Phase 1):** subscription (per-seat *or* flat), usage/metered, transaction take, marketplace take, services-into-product, sponsorship/backers.

---

## 1 · Model verdicts — the candidates, compared

The value event here is **a filed report and the fix it drives** — an *outcome*, recurring but **sporadic** (you audit when you decide to, not every PR). The buyer who pays for outcomes is the DevEx lead (NICHE.md buyer≠user). Every model is judged against those two facts and the $0-catalog norm.

| Candidate | How it would work here | Fit vs. rituals + value event | Verdict |
|---|---|---|---|
| **Per-seat subscription** | Charge $/dev/mo like CodeRabbit ($24–48) | **Mismatch, twice over.** Bills *continuously* against a *sporadic* value event; meters the exact anxiety the market just revolted over (Cursor, Copilot §3); forkable (MIT); POSITIONING explicitly forbids it. | **Reject** |
| **Flat team-audit subscription (SKU A)** | Flat annual fee: private catalog + custom linted briefs + **standing CI audits** + support | **Best fit available.** Flat (no meter → no trust breach); the CI-standing framing converts *sporadic* pain into a *recurring* one; sold as an outcome, not brief access, so it dodges the $0 norm. Still fights the free self-serve substitute. | **Survivor (conditional)** |
| **Usage / metered (e.g. paid MCP calls)** | Meter catalog reads or MCP tool calls | **Mismatch.** Cost-to-serve is ~$0 (the user pays their *own* LLM tokens — REVENUE.md §1), so any meter is a pure value-tax with no cost rationale; detonates the "nothing leaves your machine / no surprise bill" pitch. | **Reject** |
| **Transaction take** | Take a cut of a transaction flowing through the product | **No transaction exists.** Nothing of value is bought *through* goal-prompts; there is no GMV to tax. | **Reject (N/A)** |
| **Marketplace take** | Cut on third-party briefs/playbooks sold in a goal-prompts store | **Norm-blocked *and* rail-blocked.** The $0/MIT norm means there are no brief sales to tax; and Anthropic already **owns the marketplace rail** (`anthropics/claude-plugins-official`, §3) — a store of free things with the platform's store one layer down. | **Reject** |
| **Services-into-product** | Deliver SKU A as a hands-on setup/managed-audit engagement first, productize later | **This *is* how SKU A enters.** Matches "get installed, earn budget adjacent." Honest catch: it starts as **consulting** — founder-hours-bound, non-scaling — and only becomes a business if it productizes, which the $0 norm caps. | **Accept as the entry motion** |
| **Sponsorship / backers (SKU B)** | Sponsored/collab playbooks; GitHub Sponsors button | **Category-proven side-channel** (VoltAgent is sponsor-funded — COMPETITORS.md). But audience-gated: nothing to sell until stars/fetch-counts exist (REVENUE.md §4). | **Accept as complement (audience-gated)** |

**The survivor, defended.** The pick is **flat-fee team-audit (SKU A), delivered services-first, with sponsorship/backers (SKU B) as an audience-gated complement.** It is the *only* model that simultaneously (a) respects the $0-catalog norm by charging for the **outcome and the labor**, never brief access; (b) matches the buyer-buys-outcomes ritual; (c) needs **zero metering plumbing**, so it never breaks the trust posture; and (d) has a real adjacent anchor (CodeRabbit's revealed ≈$1,900–5,000/customer/yr — MARKET.md). Its fatal dependency: it sits **downstream of two things the evidence says are individually hard** — escaping 0★ *and* proving non-zero free→paid-adjacent conversion. The napkin prices that dependency.

---

## 2 · The napkin — unit economics with the arithmetic visible

**Cost side is trivial (so the model cannot lose money — it can only fail to *matter*).** Marginal cost to serve ≈ **$0**: one static Vercel deploy, and the 10–20-min agent run is externalized to the *user's own* API key (REVENUE.md §1). No COGS cliff. The real costs are two: **CAC**, paid in the founder's *time* (the star economy is bought with attention, not cash — NICHE.md §3); and the **human delivery cost of SKU A** (Founder-scale lens 6: no sales cycle at the catalog layer, no compliance/capital blocker, but **one operator's hours are the throughput ceiling on every paid engagement**).

**Value per unit (reused — MARKET.md Phase 1):** CodeRabbit reveals the outcome's price — $40M ARR ÷ 15,000 ≈ **$2,667/yr**, ÷ 8,000+ *paying* ≈ **$5,000**, Sept-2025 $15M ÷ 8,000 ≈ **$1,875** (`techcrunch.com/2025/09/16/coderabbit-raises-60m…`, Sacra — fetched in MARKET.md). goal-prompts' lighter offering captures a fraction: **$1,000–3,000/team/yr (SKU A).** SKU B (MARKET.md: **$500–2,500/placement**) is *conservative* — dev/tech newsletters command **$40–150 CPM** and 50k–100k lists charge **$3,000–7,000/placement** **[secondary]** (`sponsorgap.com/blog/newsletter-sponsorship-rates-2026`, `business.daily.dev/resources/best-developer-newsletters-to-sponsor/`); at a sub-10k early audience, $500–2,500 is the humble, right number. **So conversion, not price, is the optimistic input — corrected next.**

**The one input MARKET.md was optimistic on — corrected against a sourced benchmark.** MARKET.md's funnel used **5% → 20%** for free-catalog→paid-adjacent conversion (Step 3). The honest floor is lower: **developer-tool freemium conversion runs 1–3%** — the *low* end of the general 2–5% SaaS band, with dev tools clustering at **97:3 or 99:1 free:paid** **[secondary]** (`withdaydream.com/library/insights/freemium-conversion-rate`, `firstpagesage.com/seo-blog/saas-freemium-conversion-rates/`). And that 1–3% is *free→paid inside one product behind a credit-card wall.* goal-prompts' "conversion" is free-catalog → paid **adjacent service, with no wall and near-zero "I'd pay" language anywhere** (DEMAND.md silence test). It should therefore sit **at or below the 1–3% floor**, not at 5–20%. Optimism belongs in the plan, not here.

**Worked napkin — installs and team-share from MARKET.md, conversion at the sourced floor:**

| Scenario | Installs | × team-share | × convert | = paying teams | × $/yr | **SKU A** | + SKU B | **Year total** |
|---|---|---|---|---|---|---|---|---|
| **Y2 optimistic** (MARKET.md bull, unchanged) | 25,000 | 5% = 1,250 | 20% = 250 | 250 | $3,000 | $750,000 | ~$30k | **≈ $780k** |
| **Y2 realistic** (conversion → dev-tool floor) | 25,000 | 5% = 1,250 | **1% = 12** | 12 | $3,000 | **$37,500** | ~$20k | **≈ $58k** |
| **Y2 conservative** (mid installs, low share) | 10,000 | 2% = 200 | **1% = 2** | 2 | $2,000 | **$4,000** | ~$5k | **≈ $9k** |
| **DEMAND.md floor** (conversion structurally 0) | 25,000 | 5% = 1,250 | **0% = 0** | 0 | — | **$0** | ~$10–30k | **≈ $10–30k** |

**Where the model breaks — not into loss, into irrelevance.** Cost-to-serve is ~$0, so it can't lose money; but swap MARKET.md's 20% conversion for the *sourced* 1% dev-tool floor and SKU A collapses **~20×**, from three-quarters of a million to **~$4k–38k/yr** — side income, not a company. The break is the **conversion step**, and it is **structural**: no paywall to convert *at*, a $0-norm that forbids one, zero WTP language in the wild. Even $100k of SKU A needs ~50 paying teams — reachable only if the **top** (25k installs × ≥5% team-share) *and* the **bottom** (≥8% conversion, 5–8× the floor) break bullish **at once**. Distribution is the *gate*; conversion is the *cliff* (MARKET.md §4) — and the cliff has the sourced evidence stacked against it.

**Backers, priced honestly.** GitHub Sponsors is one file (REVENUE.md §4.5) — ship it, but expect ~$0 until stars exist: most OSS projects earn essentially nothing (OpenSSL, near-universally deployed, subsisted on ~$2,000/yr pre-Heartbleed), and maintainers clearing $1k/mo almost always **combine ≥2 methods** **[secondary]** (`github.blog/open-source/maintainers/4-trends-shaping-open-source-funding…`). Backers are gratitude, not a model.

---

## 3 · Moat and response — what compounds, who reacts, and how fast

### Moat candidates — each with its compounding mechanism + timeline, or demoted

**The rule (from the brief): a moat states its compounding mechanism and honest timeline, or it is a *head start*.** Applying it ruthlessly:

| Candidate | Compounding mechanism? | Honest status |
|---|---|---|
| **Post-run loop** (report→Studio→47·Fixer→FIXLOG) | *If adopted*, each run accretes a diffable report + fix-log history per repo → switching cost grows. Real mechanism — but needs **loop adoption + 12–24 mo of history**, neither present at 0★. | **Head start** with a *path* to a workflow-depth moat; adoption unproven. |
| **Distribution / brand-in-niche** (star economy) | Stars → awesome-list inclusion → more stars → "the audit catalog" → referral loop. The **one genuine network effect** here (awesome-claude-code's 49k *is* a moat as the list). **12–18 mo** to a defensible base; base rate is *failure* (most never clear 1,000). | **Real mechanism, asset at zero.** A moat to *build* from 0★ — aspiration, not possession. |
| **Category noun** ("audit/brief/evidence") | Own the noun → SEO + mindshare → default answer. Compounds only *after* distribution; **12–24 mo** of loud positioning, and only if no bigger player claims it first. | **Head start.** Undefended alone (Anthropic could label a category "audits" tomorrow). |
| **Machine-enforced quality bar** (the linter) | A quality *signal*, not an accreting asset — no harder to copy over time. **No longer even unique:** Anthropic's official marketplace already gates on *"quality and security standards"* (below). | **Demote to differentiator.** Forkable in days (linter is MIT, in `build.py`). |
| **Proprietary data** | *None — structurally.* The report is written to the **user's** repo; nothing returns (the trust promise). The privacy stance that wins the beachhead **forecloses** CodeRabbit's per-repo "Learnings" data moat — win trust **or** build a data moat, not both. | **Absent by design.** The sharpest structural point here. |
| **Integration lock / regulatory blessing** | None. MIT, forkable, runs in the user's own agent. | **None.** |

**Moat verdict: no moat today, only head starts.** The two with *real compounding mechanisms* — distribution/brand and the loop's workflow depth — are both at **zero** now and require **12–24 months to mature *and* no platform absorption in the interim.** Everything else is a differentiator or head start, several already matched by the platform's own marketplace. Optimism's ceiling: *if* distribution ignites and the loop is genuinely adopted, brand + switching cost could compound into a defensible position in ~2 years — but nothing is owned yet.

### Platform & supplier risk (lens 5) — the dependencies, and how they reprice

Every monetizable path is **dangerously platform-concentrated** (MARKET.md §3): each brief run rides Anthropic/Cursor/Copilot **metered tokens**; the distribution rails (the plugin/skill spec, MCP registries) are platform-controlled. The historical repricing behavior of exactly these dependencies is **aggressive and recent**:

- **Cursor, June–July 2025:** switched the Pro plan from 500 request-based limits to **usage-based API pricing on June 16 2025**; the backlash forced a **public apology July 4 2025** — *"Our recent pricing changes for individual plans were not communicated clearly, and we take full responsibility"* — plus refunds for surprise usage June 16–July 4 (`cursor.com/blog/june-2025-pricing`; `techcrunch.com/2025/07/07/cursor-apologizes-for-unclear-pricing-changes…` **[secondary]**).
- **GitHub Copilot, effective June 1 2026:** **all plans move to usage-based billing** — premium requests replaced by **AI Credits** ($0.01 each), metered on input/output/cached tokens (`github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/`).

**Read:** the layer goal-prompts rides has repriced its own customers *twice in twelve months*, once badly enough to require an apology. A token-price move goal-prompts does not control can make a 10–20-min audit run visibly expensive overnight — which is precisely the kill risk in §4.

### Incumbent response — the strategy-tax read for the top two

**Anthropic (the platform / absorption threat).** *Could they ship it in a quarter?* **They already shipped the rail.** `anthropics/claude-plugins-official` is a live **"official, Anthropic-managed directory of high-quality Claude Code plugins"** — ~**32k stars**, ~790 open issues — gating third-party submissions on *"quality and security standards for approval"* (fetched, `github.com/anthropics/claude-plugins-official`; public-beta **Oct 2025** **[secondary]**, `claudemarketplaces.com`), atop `/security-review` + Agent Skills + dynamic workflows. **Adding an "audits" category to a marketplace that already exists is a content decision — days-to-weeks.** *Strategy tax?* **Negative:** Claude Code monetizes *tokens*, so more audit runs = **more Anthropic revenue** — the worst response profile there is (high capability, total distribution, and an incentive that *rewards* shipping it). The only thing staying their hand is **attention** — `/security-review` hasn't been pushed since 2026-02-11; they plant flags and wander (COMPETITORS.md). That roadmap-attention gap is goal-prompts' entire oxygen supply — not a moat, a countdown.

**CodeRabbit (the execution leader / price ceiling).** *Could they ship a $0 standing-audit catalog in a quarter?* Capability: yes. *Strategy tax:* **high.** Their whole business is per-seat/credit metered review ($24–48/seat, 15k customers, $40M ARR); a free, un-metered, runs-on-your-own-agent audit **cannibalizes the meter and the cloud data-path**. COMPETITORS.md's read holds: *"CodeRabbit could stand up a free OSS standing-audit action — but it fights their per-seat model, so they won't."* They will keep pushing precision + Learnings **up-market**, not chase the $0 solo/OSS floor. **The strategy tax protects goal-prompts from the execution leader.**

**The asymmetry that is the whole problem:** the incumbent goal-prompts is *priced against* (CodeRabbit) is strategy-taxed **out** of copying it; the incumbent that can copy it **trivially and profitably** (Anthropic) **owns the rail goal-prompts rides.**

---

## 4 · Kill list — ranked, with tripwires and pre-tests

Five most-probable causes of death, each with an early-warning signal and a **cheap pre-test runnable before real building** (Phase 3).

**1 · Platform absorption — Anthropic blesses a first-party "audits" catalog.** *Most lethal.* The rail (`claude-plugins-official`), the primitives (`/security-review`, Agent Skills, dynamic workflows), the distribution, and a **negative** strategy tax (audit runs sell tokens) all point one way; only Anthropic's attention is the delay.
- **Tripwire:** an "audit/review/quality" category or a first-party audit-brief bundle appears in `claude-plugins-official`; or `/security-review` gains an `/audit` sibling; or an official "code-audit" Agent Skill ships.
- **Pre-test (days, $0):** **submit goal-prompts to the official plugin directory** (the submission form exists) — if the platform *distributes* you, absorption becomes co-option, not death; if its quality bar rejects you, you've learned the rail is closed *before* betting on it. Pair with a week of desk-scanning Claude Code changelogs + Discord/DevRel for any "audits" roadmap signal.

**2 · The conversion cliff — free attention converts to paid-adjacent dollars at ~0%.** *Most probable death of the dollar thesis.* The napkin's break point; the input with the most disconfirming evidence (dev-tool 1–3% *behind a wall*, and goal-prompts has no wall + no WTP language).
- **Tripwire:** at meaningful install volume, zero inbound "can you set this up for our team," zero paid engagements, flat sponsorship inquiries.
- **Pre-test (days, $0 — the single highest-value one):** ship the `/teams` page + a "set this up for your org →" CTA + a price anchor **now** (REVENUE.md §4 already specs the plumbing), point a little attention at it, and **count inbound intent.** Even 3–5 real "what does it cost / can you do this for us" emails is the cheapest possible proof of non-zero WTP. In parallel, ask the 10 nameable sufferers (DEMAND.md's list) the flat-fee-team-audit question to their face. *This is the one number to get right before spending a dollar* (MARKET.md §4).

**3 · Distribution never ignites — stuck near 0★, invisible.** *The gate.* Base rate for a new catalog is failure (most never clear 1,000 stars; 0★ = invisible past the awesome-list border control — NICHE.md §3).
- **Tripwire:** 3–6 months of consistent shipping and stars stay sub-100; no awesome-list inclusion; no HN front page; `/raw/*` fetch counts flat.
- **Pre-test (days, $0):** take **one loud, well-built swing** — a Show HN + an `awesome-claude-code` inclusion PR + a single strong dogfood report as the hook — and measure the star/fetch response. If a genuine launch cannot clear a few hundred stars, the base-rate bear is confirmed and the entire funnel is moot; learn it cheaply.

**4 · Token repricing / metering contagion — the tokens goal-prompts rides get repriced and finance kills the $0 tool for its downstream bill.** *External, medium probability, recent precedent* (Cursor apologized July 2025; Copilot goes usage-based June 2026 — §3).
- **Tripwire:** a token-price hike or "premium request" reclassification that makes an audit run visibly expensive; a spike in "this brief burned $X of credits" complaints; finance blocking the tool over its token cost.
- **Pre-test (one metered run, ~$):** run the heaviest brief end-to-end at current API rates and **publish the honest token cost.** Confirm a full audit is cents-to-low-dollars. If one run already costs more than the value it returns to a solo dev, the "effortless vs. doing-nothing" wedge is dead on arrival (NICHE.md §1 — you beat "just rerun it" only by being effortless).

**5 · Structural no-moat — the privacy stance forecloses the only data moat, permanently.** *Certain but slow — caps the ceiling rather than killing outright.* "Nothing leaves your machine" means there is no per-repo "Learnings" exhaust to compound (§3); the format is forkable, the quality bar now platform-matched.
- **Tripwire:** an equally-private audit catalog ships (from anyone, or from the platform) — at which point no defensible difference remains.
- **Pre-test (an interview, not a build):** ask the beachhead whether they'd trade some privacy for a compounding cross-run "learnings" feature. If they say no (likely, per NICHE.md's trust rule), **accept that the ceiling is a head-start business** and size the ambition to match — do not raise capital against a moat that structurally cannot exist here.

**Ranking logic:** #1 most *lethal* (negative strategy tax, rail already built), #2 most *probable* killer of the revenue thesis, #3 gates everything upstream, #4 external but precedented, #5 slow but certain (sets the honest ceiling). The two the funnel most needs to survive — **absorption (#1) and conversion (#2)** — are exactly the two the companion reports have circled all along.

---

*Report only — which risks should we pre-test before the verdict?*
