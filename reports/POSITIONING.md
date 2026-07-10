# POSITIONING.md
*Produced by brief 65 · Positioning & Wedge, run against **this repo's own venture: goal-prompts — a catalog of structured audit briefs for coding agents.** Synthesized from NICHE.md + DEMAND.md + COMPETITORS.md + MARKET.md, with competitor copy checked live. All sources accessed 2026-07-10 unless dated otherwise. Directly-fetched primaries unmarked; web-search synthesis marked **[secondary]**.*

**Date:** 2026-07-10

## Phase 1 — inputs loaded, and what's missing

**Extracted from the four reports.** *Beachhead candidates:* the burned individual dev / OSS maintainer who hand-rolls prompts and gets *"50% … messy"* output (DEMAND.md); the DevEx/platform lead who buys *outcomes* not text (NICHE.md buyer≠user split, MARKET.md buyer unit); the catalog-fatigued power user drowning in 100+ ungated agents (COMPETITORS.md market-truth #2). *Shared complaints:* execution-layer **noise/false positives** ("most suggestions … irrelevant"), catalog-layer **sprawl/inventory** (aitmpl #649 "how to uninstall"), and the universal **"and then what?"** — nobody owns post-run (COMPETITORS.md gap #1). *Crowded claim-space:* everyone says **review** (a verb that ends at the comment) or **agent/prompt/rules/templates** (an input + a count); the words **audit · brief · report · evidence** are unowned (COMPETITORS.md).

**Missing inputs, and what the absence costs this brief:**
- **No customer interviews** (NICHE.md open Qs #1/#2/#4: *will anyone pay, does "audit/brief" reframe, who holds the pen*). This is the biggest confidence hit — the recommendation's core bet (distribution-first, monetize-adjacent) is reasoned from comparables, not validated against a buyer's ear.
- **No Reddit/G2/Capterra primary complaint text** (hard-blocked every prior pass). Objection-map language leans on HN primaries + the reports' **[secondary]** Trustpilot/benchmark quotes, not first-hand review-site objections from the beachhead.
- **No live goal-prompts analytics (0★, no funnel data — MARKET.md).** Every stress-test verdict below is judgment, not measured conversion. The one number that decides the whole thesis — does free attention convert to a paid dollar (MARKET.md's cliff) — remains un-measured.

---

## 1 · Options table

Three internally-consistent options. Columns are the lenses: beachhead (L1) · against-frame (L2) · category (L3) · onlyness (L4) · price (L6). Onlyness claims verified against live competitor copy in §3.

| | **A — Own the audit loop** *(recommended)* | **B — The standing team audit, no per-seat bill** | **C — The catalog that can't rot** |
|---|---|---|---|
| **Beachhead (L1)** | The **burned solo dev / OSS maintainer** who already hand-rolls prompts and no longer trusts one-off agent output (DEMAND.md's *sukit/jamesponddotco* sufferer). Reachable on HN + GitHub — the only fetchable watering holes (NICHE.md §2). The on-ramp to the buyer. | The **DevEx/platform lead on a small-to-mid team** already paying for an agent, who wants consistent review but won't add a $24–48/seat line item and fears egress (MARKET.md buyer unit; COMPETITORS.md "ignored segment"). Holds the pen. | The **catalog-fatigued Claude Code power user** buried under 100+ ungated agents/plugins, filing *"how do I uninstall"* issues (COMPETITORS.md market-truth #2). |
| **Against-frame (L2)** | Against the **habit of doing nothing well** — the private prompt doc and *"just rerun it"* that file no evidence and have no follow-through (NICHE.md §1's real competitor). | Against a **competitor** — per-seat managed review (CodeRabbit/Greptile/Qodo): the meter, the noise, the cloud data-path. | Against a **workaround** — the sprawling mega-catalog / awesome-list; *"more = better"* (NICHE.md §3). |
| **Category (L3)** | **Claim a niche of one:** "audit briefs / the audit-loop catalog." Anchored to the known noun *catalog* for findability, modified by the unowned *audit* register. Education cost, but the SEO/star land-grab is live (MARKET.md §2). | **Join an existing category:** "AI code review" — cheap to explain (everyone knows it), but you fight on CodeRabbit's turf and it's the *execution* layer goal-prompts isn't. | **Claim a niche of one:** "the linter-gated / verified-curation catalog." The quality bar *is* the noun. |
| **Onlyness (L4)** | *The only **audit catalog** that turns your coding agent into a repeatable, evidence-producing audit — explore→audit→**report you can diff and re-run** — and carries the finding through to a fix log — for **devs who've stopped trusting one-off prompts.*** | *The only **standing team audit** that runs on the coding agent **you already pay for** and files a report **you own** — no per-seat bill, nothing leaves your machine.* | *The only agent catalog where **every brief passes a machine-enforced quality bar** — 4-phase, ask-first, size-capped, CI-gated — so nothing in it rots.* |
| **Price posture (L6)** | **Disruptor $0** catalog (a norm, not a decision — NICHE.md §3); monetize **adjacent** on the outcome (flat team-audit $1–3k/yr, *not* per-seat — MARKET.md SKU A). $0 signals trust + kills bill-shock. | **Disruptor $0** as the explicit weapon: "$0 standing audit vs. their $24–48/seat." The flat-vs-per-seat contrast *is* the wedge. | **$0**; here the **gate**, not the price, is the differentiator (every rival is $0 too). |
| **Education cost** | Medium — recombines known words (*audit*, *report*); the loop needs one demo. | **Low** — "code review" is understood; but highest **camouflage** risk (§3). | **High** — "linter-gated catalog" must be explained before it lands. |

---

## 2 · The recommended wedge — **Option A: Own the audit loop**

**Why A wins the pick.** All four reports triangulate on the same seam. COMPETITORS.md's gap analysis calls the post-run loop the one gap *"open because hard"* — every execution vendor stops at *comment*, every catalog stops at *prompt*, and **no rival owns "after the run."** MARKET.md's window verdict says the assets that *compound* are *"distribution + a category noun + the enforced-curation/post-run loop"* — and that first-mover advantage is real *"only if the flag is planted loudly, before Anthropic ships a first-party audit-workflow catalog."* NICHE.md §3's exploitable beliefs are exactly A's raw material: re-badge off the depreciating *"prompt,"* own the vacant post-run loop, flip the status marker from catalog *size* to *verified curation*. And DEMAND.md fixes why A beats a pure-catalog play: WTP lives in the **execution/outcome** layer, and the loop (report→Studio→47·Fixer→FIXLOG) is the *only* thing in this repo that bridges toward it.

**Why not B or C first.** B is the buyer-first, monetize-now option — attractive — but its category choice ("AI code review") is the crowded claim-space itself, and the stress test (§3) rates its one-liner as **camouflage** against CodeRabbit's near-identical live copy. You'd be the $0 knock-off of *"The leader in AI code reviews,"* fighting a 15,000-customer incumbent on its own noun. C is a genuine counter-belief no rival can copy (they'd have to cap their count), but it *"only bites once you have enough briefs and proof to matter"* (COMPETITORS.md) and carries the highest education cost — it's a supporting proof, not a headline. **A is the superset:** it *contains* C's verified-curation as an objection answer and sets up B's outcome as its adjacent monetization, while keeping the least-crowded noun. Its real strike — a nonzero education cost (the brief's rule: *education is a cost, not a cleverness*) — is bounded, because *audit* and *report* are understood words recombined, not a coined term; that cost is smaller than B's camouflage risk.

**The against-frame, defended.** A is positioned against *doing nothing well* — the private prompt doc, copy-paste-from-HN, *"just rerun it."* NICHE.md §1 names this the **real competitor** (inertia, free, entrenched), and MARKET.md's moat table agrees: *"you beat 'just rerun it' only by being effortless."* Positioning against the status quo (not against CodeRabbit) is what lets A avoid B's camouflage trap — you're not the cheaper reviewer, you're the thing that turns a habit into filed, diffable evidence.

### Objection map (the beachhead's top five *no*s → the positioning answer)

| # | Objection (real language) | Positioning answer |
|---|---|---|
| 1 | *"I already keep a running doc of prompts that work well."* — sukit, HN #44362244 (DEMAND.md) | The value was never the prompt text — it's the **repeatable, filed evidence** your doc can't produce and the **fix log** your doc can't carry. Your doc reruns *differently* every time; a brief runs the same four phases and files a report you can diff. |
| 2 | *"Isn't this just another awesome list?"* (NICHE.md open Q#2) | Awesome-claude-code is *"a hand-picked collection"* (live, 2026-07-10) — **human** curation, **613 open issues**. Every goal-prompts brief passes a **machine** linter (4-phase, ask-first, size cap, CI-gated) and ends in a filed report. A gated catalog, not a pile. |
| 3 | *"Anthropic will just ship this first-party for free."* (DEMAND.md Sub-pain C; the absorption threat) | They shipped one narrow slice — `/security-review`, *"an AI-powered security review … for security vulnerabilities"* — **76 open issues, no push since 2026-02-11** (COMPETITORS.md). The platform planted a flag and wandered off. A owns the *whole* audit surface **and** the post-run loop the platform hasn't built. |
| 4 | *"The bot's findings are noise — most suggestions are irrelevant."* (CodeRabbit Trustpilot; Greptile 11 FPs — COMPETITORS.md **[secondary]**) | Briefs are **read-only and ask-first**: you read the finding — severity, location, fix sketch — before one line changes (see this repo's own BUGS.md S2 hero finding). You're not triaging a bot's 30–50% noise; you're approving evidence. |
| 5 | *"Why pay when it's MIT and forkable?"* (DEMAND.md silence test; REVENUE.md) | You **never** pay for briefs — the catalog is $0 forever. If you ever pay, it's for the **outcome**: a private team catalog + standing CI audits + support (MARKET.md SKU A), a flat fee, never a per-seat meter, never at the tollgate (NICHE.md §3). |

---

## 3 · Message drafts & the stress test

Each one-liner set beside the **nearest competitor's actual live homepage copy** (fetched 2026-07-10). Verdict = distinct **·** believable **·** wanted, or **camouflage**.

| Option — our one-liner | Nearest competitor's real copy (verbatim, live) | Verdict |
|---|---|---|
| **A:** *"Point your coding agent at your repo and get back a filed, evidence-backed report you can diff, re-run, and act on — the same four phases every time."* | **CodeRabbit** (`coderabbit.ai`): H1 *"Cut code review time & bugs in half, instantly."* / *"The leader in AI code reviews."* | **Distinct + wanted.** They sell a *metric on a comment*; A sells a *filed artifact + a loop*. Different noun (*report/diff* vs *review*), the one Sub-pain C begs for. Believable because the repo dogfoods it (`/examples/`). |
| **B:** *"A standing audit for your whole team — running on the agent you already pay for. No per-seat bill, nothing leaves your machine."* | **Greptile** (`greptile.com`): H1 *"The AI Code Reviewer."* / *"AI agents that review and test pull requests with full context of the codebase."* / *"Merge 4X Faster, Catch 3X More Bugs."* | **Believable but camouflage-risk.** The "no per-seat / on your own machine" clause *is* distinct against their cloud+seat model — but the frame still lives inside *"AI code review,"* so at a glance B reads as a cheaper Greptile. Distinct only if the price/egress contrast leads. |
| **C:** *"Not 154 agents to babysit — a small catalog where every brief passes a machine-enforced quality bar, so nothing rots."* | **awesome-claude-code** (`github.com/hesreallyhim/awesome-claude-code`): *"A hand-picked collection of the finest of resources…"* (49.7k★, 613 open issues) | **Distinct + believable, education-heavy.** *"Machine-enforced"* vs *"hand-picked"* is a true, uncopyable contrast — but "quality bar" is a benefit you must *demonstrate*, so it wants a proof page, not a hero line. |

**Onlyness verification (L4) — no rival page says our claim.** Checked live 2026-07-10: **CodeRabbit** = *"Cut code review time & bugs in half"*; **Greptile** = *"The AI Code Reviewer"* (COMPETITORS.md logged the campaign line *"Greptile Now Runs Your Code"* the same day — both run on the page); **Qodo** (`qodo.ai`) = *"Govern code at the speed AI writes it"*; **/security-review** = *"…security review GitHub Action … for security vulnerabilities"*; **awesome-claude-code** = *"a hand-picked collection."* **None** says *report you can diff*, *report you own*, *standing audit on the agent you already pay for*, or *machine-enforced quality bar*. The audit·brief·report·evidence register is confirmed unclaimed.

### Supporting claims (three per option, each traceable)

**Option A — Own the audit loop**
1. *"Every brief runs the same four phases — explore, audit, curate, report — and files one evidence-backed report at your repo root."* — the 4-phase skeleton the linter enforces (CLAUDE.md); current hero sub (template.html).
2. *"No bot triage. Briefs are read-only and ask first — you read the finding before a single line changes."* — ask-first gate (CLAUDE.md); answers the noise complaint (COMPETITORS.md market-truth #1).
3. *"The report doesn't die in a comment thread — carry it through to a fix log, so 'and then what?' finally has an answer."* — the post-run loop gap (COMPETITORS.md #1; DEMAND.md Sub-pain C); traces to `studio.html`, prompt 47, FIXLOG.

**Option B — The standing team audit**
1. *"CodeRabbit charges $24–48 per seat to comment on your PRs. goal-prompts files the same class of evidence for $0, on the agent your team already runs."* — live CodeRabbit pricing + DEMAND.md spend table.
2. *"No new vendor in your data path — every brief runs locally in your agent; nothing leaves your machine."* — NICHE.md §3 trust rule; CodeRabbit/Greptile are cloud pipelines.
3. *"The same audit, every engineer, every repo — consistency your team can standardize on."* — DEMAND.md Sub-pain C (*"consistency of quality"*); MARKET.md buyer unit.

**Option C — The catalog that can't rot**
1. *"Every brief is linter-gated: 4-phase skeleton, ask-first, size cap, CI-enforced — a bar no hand-picked list enforces."* — CLAUDE.md linter; live *"hand-picked"* contrast.
2. *"Rivals ship 100–200 units with no per-item gate; their own users file 'how do I uninstall this.' Trustworthy curation means installing fewer things, not more."* — COMPETITORS.md aitmpl #649/#617; NICHE.md §3.
3. *"Read any brief in five minutes — plain markdown, no black box."* — echoes claude-autopilot's winning pitch (DEMAND.md); goal-prompts is readable markdown.

---

## 4 · Flip conditions — facts that would change the pick

1. **A buyer will pay *now*.** If interviews (NICHE.md open Q#1/#4) show DevEx leads will buy a standing team audit today, flip to **B** — monetize immediately rather than A's distribution-first, monetize-later. The whole A-vs-B choice is really *distribution-first vs. revenue-first*, and only a real *yes* on WTP settles it.
2. **Anthropic ships a first-party audit-workflow catalog.** The most-lethal kill-zone entry (MARKET.md window, *"weeks-to-quarters"*). If it lands before A's flag is planted, retreat to **C** — verified curation is the one thing the platform is *disincentivized* to copy (it caps count) — or pivot to a pure execution product (a different company).
3. **"Audit/brief" tests as "just another awesome list."** If a user test fails NICHE.md open Q#2, the niche-of-one noun didn't take; fall back to **B**'s join-an-existing-category ("AI code review, $0") where comprehension is free.
4. **Catalog→paid conversion proves structurally 0%** (MARKET.md's cliff/sensitivity). Then positioning that promises a monetizable wedge is moot — optimize A purely for *attention*, monetize only SKU B (sponsorship) + gratitude, and drop the team-audit claim from the hero.
5. **Sprawl fatigue turns out louder than inconsistency pain.** If the market's dominant complaint is inventory/uninstall (aitmpl) rather than *"50% messy"* output, **C**'s against-sprawl frame out-pulls A's against-doing-nothing — promote the quality bar from proof to headline.

---

*Report only — which option should we carry into the verdict?*
