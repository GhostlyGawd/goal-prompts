# REVENUE.md — Monetization Map

**Date:** 2026-07-09
**Auditor:** monetization-map brief, read-only pass
**Prior run:** none — no previous `REVENUE.md` existed; this is the first monetization map.
**Companion evidence:** `COMPETITIVE.md` §5 (category pricing norms, written today) and
`FUNNEL.md` §4 (instrumentation gaps, written today) are cited below rather than re-derived.

---

## 0 · The honest headline

This is not a null report — a real monetizable surface exists and is already half-built —
but every proposal below is bounded by one fact: **the repo shows 0 stars / 0 forks**
(`metrics.json`, `COMPETITIVE.md` §1) and the site publishes no usage numbers. The two
viable revenue lines (sponsorship inventory and a teams offering) are both sold *against an
audience*, and the audience is currently unproven and unmeasured. Monetization work here is
mostly **plumbing built now, sold later** — plus one genuinely zero-cost quick win
(a Sponsors button). Distribution remains job #1; nothing below should displace it.

---

## 1 · Current model snapshot

**What exists today: free, everywhere, on purpose.**

- **Price:** $0. MIT-licensed (`LICENSE`, `package.json`), stated in the footer
  ("Free & MIT-licensed", `template.html:759`). No tiers, no trials, no accounts —
  "no signup · nothing leaves your machine" is a load-bearing brand promise
  (`template.html`, hero micro-line; `FUNNEL.md` §1 confirms zero capture).
- **Billing code:** none. No payment processor, no checkout, no `FUNDING.yml` in
  `.github/` (verified absent), no GitHub Sponsors link, no donation link anywhere on any
  surface. The word "revenue" appears in exactly one user-facing sentence
  (`template.html:731`).
- **The one revenue system that IS built — sponsorship/collab merchandising, minus the
  checkout.** `playbooks.json` supports `type: themed | collab | sponsored`, `partner
  {name, blurb, cta}`, `accent`, `window`, `preview`; the build renders a Partnerships
  band on the landing page (`template.html:725–745`: "Playbooks are also how the project
  sustains itself… the content is shared and so is the revenue") and a partner block on
  every partner playbook's `/p/<key>` page (`build.py:1069–1081`). Two placeholder
  placements ship live as worked examples: `/p/codereview-collab` (collab template) and
  `/p/sponsored-example` (sponsored bundle), both `preview: true`, both honestly badged
  and labeled "example… no real partnership implied." This is inventory without a cash
  register — see §4.

**What is expensive to serve — and is the cost gated?**

Marginal cost is ~zero and therefore nothing is gated, correctly:

- The site is one static deploy on Vercel (`vercel.json`: `outputDirectory: "."`, no
  functions, no storage) — ~165 KB gz landing page + immutable fonts (`FUNNEL.md` §0).
- The actually expensive compute — the 10–20-minute agent run — is **externalized to the
  user's own Anthropic API key** (the briefs run in the user's agent; the scheduled
  workflow explicitly requires the user's `ANTHROPIC_API_KEY`, `README.md:101`). The
  product's COGS design is: the user pays the LLM, Vercel's free tier pays the bandwidth,
  the maintainer pays only in time.
- Consequence for packaging: there is **no cost-based rationale for usage gates**. Any
  gate would be a value gate on convenience/placement/service, never a metering gate.

**What do power users do that casual users don't?** (inferred from features + data model)

| Power-user behavior | Evidence |
|---|---|
| Compose custom brief sequences / conductors | custom-sequence builder + `make_conductor` MCP tool (`README.md:56`, `template.html` custom pills) |
| Persist Operator context (stack/product/stage) appended to every copy | "aim the briefs at your repo" localStorage box |
| Run standing scheduled audits in CI | `.github/run-brief.example.yml` |
| Self-host a **private team catalog** on an internal domain | `GOAL_PROMPTS_BASE` rebases every generated surface (`build.py:23`, `README.md:184–196`); `BASE=` in `install:14` |
| Drive the report → checklist → Fixer commit loop | Report Studio (`studio.html`), brief 47, `FIXLOG.md` |
| Consume the catalog machine-to-machine | MCP server (`mcp/server.cjs`), `catalog.json`, stable `/raw/*` URLs |

The last four cluster into one persona: **a team running recurring private-repo audits on
internal infrastructure**. That is the only persona here with organizational budget.

**What leaks?** Nothing leaks in the "unenforced paywall" sense — everything is free by
design. The leaks are *unsold value*: (a) the sponsorship inventory has no price, no
private contact channel, and no audience numbers to sell against; (b) the private team
catalog — the one feature "none of the free rivals productize" (`COMPETITIVE.md` §5) — is
given away as a README paragraph with no offer attached; (c) there is no way to give the
project money at all, even for someone who wants to.

**Enforcement:** nothing to enforce; no limits exist in code. §6-lens "plumbing gaps" is
therefore inverted here: the gap is not upgrade/cancel mechanics but the *absence of any
transaction path whatsoever*.

---

## 2 · Packaging proposal

Constraint honored throughout: **MIT + "the market has set that expectation at zero"**
(`COMPETITIVE.md` §5, §9). Content paywalls are both unenforceable (fork it) and
goodwill-poisoning. Every tier below monetizes *placement, service, or gratitude* — never
brief access. The "still generous free story" is trivially strong: the free tier is the
entire current product, forever.

| Tier | One-line job | Who pays | Willingness-to-pay signal |
|---|---|---|---|
| **Free** (= everything today) | The whole catalog, plugin, MCP, Studio, conductors, examples — the distribution engine. | nobody | Category price is $0 universally (`COMPETITIVE.md` §2 price row); generosity IS the growth strategy at 0 stars. |
| **Backers** (GitHub Sponsors) | Let grateful users say thanks; fund maintenance. | individuals | Weakest signal but zero cost: VoltAgent (23k★) is explicitly "sponsorship-funded" (`COMPETITIVE.md` §1); standard OSS pattern. Expect ~$0 until stars exist — ship it anyway because it costs one file. |
| **Sponsored & collab playbooks** | Sell curated attention: a dev-tool brand wraps a real, linted, useful sequence — disclosed, capped, revenue-shared for collabs. | dev-tool marketing budgets | The category's proven monetization: VoltAgent routes ALL promotion through paid sponsorship; promo-PR pressure on rivals (`COMPETITIVE.md` §5, §8) proves vendors already *push* money at catalogs like this. The rendering system is already built (`playbooks.json`, `build.py:1069`). Sellable only once `/raw/*` fetch counts exist (see §3/§4). |
| **Goal Prompts for Teams** | A working private audit pipeline: internal catalog (`GOAL_PROMPTS_BASE`), org-specific custom briefs passing the linter, standing CI audits — sold as setup + support, not as gated software. | eng managers / platform teams | Adjacent price ceiling: CodeRabbit at ~$24–48/user/mo for automated review (`COMPETITIVE.md` §1); this repo's free GitHub Action already delivers the standing-audit outcome at $0 (`COMPETITIVE.md` §6.4), so the paid layer is the *implementation and the custom content*, priced flat (e.g., setup engagement + optional support retainer) — no per-seat metering to build or enforce. |

**Deliberately not proposed:** paid brief packs, a pro tier of the Studio, metered MCP,
accounts of any kind. Each violates either the MIT reality, the privacy stance
(`template.html` "nothing leaves your machine"), or the do-not-copy list already ruled on
in `COMPETITIVE.md` §9.

---

## 3 · Upgrade moment placements

"Upgrade" here means the moment a free user (or a sponsor prospect) is warmest. All
placements are dim, honest, and skippable — this product's trust posture is its moat.

1. **Sponsor prospects — the Partnerships band, post-proof.** Already correctly placed:
   the band sits directly after the before/after "The fix — commit 683dff5" proof block
   (`template.html:718–745`), i.e., right after the product demonstrates it works. Keep
   the position; fix the broken conversion path behind it (§4 items 1–3). Trigger: none
   needed — it's a B2B surface, always-on.
2. **Teams — the two moments a team self-identifies.** (a) The README "Run your private
   team catalog" section (`README.md:184–196`) and (b) the moment someone builds with
   `GOAL_PROMPTS_BASE` set / runs `BASE=… sh install`. Today both dead-end into DIY. Add
   one line in each: "Want this set up for your org, with your own briefs? →" linking a
   `/teams` (or README anchor) offer. This doubles as `COMPETITIVE.md` §10 bet 3 — the
   "for teams" page is simultaneously positioning and the only pricing page this product
   needs.
3. **Backers — the success high point, not the entry.** The run tracker already fires a
   roadmap nudge at ≥5 marked runs (`FUNNEL.md` §1 Habit row). That is the one success
   high point the site can see. After that nudge has fired once (i.e., a genuinely
   activated user), show — once — a dismissible footer-weight line: "Five audits in. If
   these earn their keep, there's a Sponsors button." Guard: only after FUNNEL.md's
   mark-run un-faking lands, otherwise the trigger fires on five *copies* and the ask
   reads as spam to a user who got nothing yet. Until then, the Sponsors link lives
   statically in the footer next to "Built by @GhostlyGawd" (`template.html:758`).
4. **Sponsors — themed drops as the recurring inventory unit.** `window` +
   `type: themed` (Ship-It Week, New-Year Reset in `playbooks.json`) already model
   seasonal placements. Each themed drop's `/p/<key>` page is a natural "this slot,
   next season: yours" footnote once real traffic numbers exist. Trigger: calendar.
5. **Anti-placements (churn risks, flagged per Phase 3):** never inject sponsored cards
   into the 6-card featured storefront grid ahead of organic playbooks (currently safe:
   `preview` playbooks are excluded from pills, `template.html:1042`, and neither example
   is `featured`); never put a sponsor ask in the post-copy toast (the activation-critical
   surface `FUNNEL.md` needs for run guidance); never weaken the "Sponsored" badge
   disclosure that `build.py`/`template.html` already render. Aggressive versions of any
   of these would poison the exact trust the catalog sells.

---

## 4 · Friction fixes (the willing payer's path today), ranked

There is no checkout; the entire payment funnel is two links. Both are broken-ish:

1. **The two partner CTAs point at different destinations.** Landing band → GitHub
   *issue* (`template.html:741`, `issues/new?title=Partnership+inquiry`); every `/p/`
   partner block → GitHub *Discussions* (`build.py:1080`,
   `discussions/new?category=ideas`) — which fails outright if Discussions isn't enabled
   on the repo. Unify on one destination and verify it resolves. (S)
2. **No private channel.** A sponsor negotiating budget will not open a public GitHub
   issue titled "Partnership inquiry" as their first move. Add an email (or a private
   contact form is overkill — email suffices) alongside the public link. (S)
3. **Nothing says what anything costs or includes.** No rate card, no placement specs
   (duration? homepage band vs `/p/` page? what does "revenue is split" mean for
   collabs?). A prospect must reverse-engineer the offer from two placeholder playbooks.
   One `/partners` page (or a section on the collab template page): the three formats,
   what each includes, honest "early — audience numbers on request" framing, and a price
   anchor once there is anything to anchor to. (M)
4. **No audience proof to sell against — the real blocker.** `docs/usage-metrics.md`
   states "Nothing in this document is live"; `/b/` and `/p/` pages ship no analytics at
   all (`FUNNEL.md` §4.1). Sponsorship CPMs are sold on numbers. Turning on raw-fetch
   counting (Vercel log filter, zero code — `FUNNEL.md` §4.3) is therefore *revenue*
   infrastructure, not just funnel infrastructure. (S–M, and already top of FUNNEL.md's
   list for independent reasons.)
5. **No way to give money at all.** Add `.github/FUNDING.yml` + GitHub Sponsors (or Ko-fi)
   and the footer link from §3.3. One file + one anchor. (S)
6. **Failed payment / cancel / downgrade:** n/a — and if the Teams offer ships as
   flat-fee engagements + optional retainer (per §2), it stays n/a: no subscription
   plumbing, no metering, no cancel flow to build. That simplicity is itself the correct
   packaging decision for a one-maintainer product.

---

## 5 · Quick wins vs structural changes

**Quick wins (each ≤ a day, none touches the free experience):**
- `FUNDING.yml` + Sponsors button in the footer (§4.5) — first dollar becomes *possible*.
- Unify the two partner CTAs on one working destination + add an email (§4.1–2).
- One-paragraph "want this run for your org?" pointer in the README teams section and on
  the collab template page (§3.2, §4.3-lite).
- Flip on `/raw/*` fetch counting from Vercel logs (§4.4) — the number every future
  revenue conversation depends on.

**Structural (weeks, sequenced after distribution work):**
- The `/partners` page with formats + specs, upgraded with real fetch/traffic numbers
  once they exist (§4.3) — then actively close ONE real collab playbook to replace the
  placeholder; a live co-branded sequence is worth more than any rate card.
- **Goal Prompts for Teams** as a defined offer (private catalog setup, custom linted
  briefs, standing-audit CI wiring, support retainer) with the `/teams` page as its
  pricing surface (§2, §3.2) — this is also `COMPETITIVE.md` §10 differentiation bet 3,
  so the same work serves positioning and revenue at once.
- The post-activation backer nudge keyed to *real* runs (§3.3) — blocked on FUNNEL.md's
  mark-run fix by design.

**Sequencing truth:** quick wins now (they're free and honest), sponsorship sales only
after the metrics + proof work lands, Teams as the slow B2B play. Revenue expectation in
the current 0-star state is roughly zero regardless — build the rails, keep shipping
distribution.

---

*Read-only audit — no code, content, or config was changed.* Which of these should I
make: the quick-win set (FUNDING.yml + unified partner CTA + email + raw-fetch counting),
the `/partners` rate-card page, the Teams offer page, the post-activation backer nudge —
or a specific combination?
