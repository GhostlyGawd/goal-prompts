# ROADMAP.md — Unified Roadmap Synthesis

**Date: 2026-07-11** · produced by brief 28 · Roadmap Synthesis (re-run), read-only over
every audit report at the repo root and in `reports/`. **Second run** — a prior `ROADMAP.md`
(2026-07-09) synthesized the *product-improvement* reports; this run leads with what changed,
then folds the seven **Founder Funnel** venture reports + the **PIVOT** verdict on top.

**How to read this.** Every item traces to a source report; nothing new is smuggled in.
Tags: **`test`** — a $0 validation gate (the pivot's pre-tests) · **`ship`** — buildable in
this repo now · **`ext`** — needs maintainer accounts/decisions (cannot be built here) ·
**`gated`** — deliberately blocked on a signal, data, or decision · **`done`** — shipped.
Impact/effort are recalibrated on the **pivot's** scale: "impact" now means *moves the
validation question or protects the moat/trust*, not *storefront optimization*.

---

## What changed since 2026-07-09

The last roadmap was a **product-optimization** plan: see the funnel, close the silent
stalls, patch honesty drift, then spend the visibility. Its ~50 ship items were built (0.14.0,
PR #27), and 0.15.0/0.16.0 added the ledger redesign, the design engine, BLINDSPOTS, and the
breadcrumb pass. Three things then changed the frame underneath it:

1. **A full Founder Funnel ran (NICHE · DEMAND · COMPETITORS · MARKET · POSITIONING · MOAT ·
   VERDICT) and returned a verdict: PIVOT — axis: product.** Not a kill (pain is real,
   recurring, sufferer-verbatim; the first ten are nameable; timing is genuinely 2026), and
   not "keep optimizing the storefront." Two bars hard-failed: **competitive survivability**
   (the "own-the-loop" wedge has no moat against an Anthropic that can copy it *trivially and
   profitably* — MOAT: "no moat today, only head starts") and **economics** (at the sourced
   1–3% dev-tool conversion floor the dollar thesis collapses ~20× into $9k–58k side income —
   MOAT napkin). Both fails share one root: **the money and the only path to a moat live in
   the outcome/loop (report→Studio→47·Fixer→FIXLOG), not in the $0 forkable catalog text.**
   The ruling: keep the customer and the pain, move the paid surface to the loop, and
   **validate willingness-to-pay CHEAPLY before building anything more.**

2. **BLINDSPOTS.md (2026-07-10, meta-audit) independently reached the same conclusion** the
   old roadmap didn't digest: "a beautifully machined answer to the wrong layer… verifying
   the verifiable proxy instead of the value." It ruled the old plan's own tell — *50
   storefront items shipped while the three audience-creating items (measurement, npm, launch)
   stayed open and the R62 pivot decision stayed deferred.* That decision is **now taken**
   (VERDICT = pivot). BLINDSPOTS also contributes a fresh backlog the old roadmap never saw.

3. **Four pivot changes shipped to `main`** (commits 54ae65f, ae724d5) — marked **done**
   below, not re-listed as todo: (a) re-badged the register to *audit/brief/evidence*;
   (b) made the report→Fixer→FIXLOG loop legible in the Proof section; (c) locked the `/teams`
   WTP surface (competitor $24–48 anchor, $0 DIY floor, "on request", one intent CTA);
   (d) surfaced the machine-enforced quality-bar claim, linking `/quality`. All four are
   TDD-locked in `tests/test_build.py`.

**Net effect on the roadmap.** The product backlog is *substantially built*. The frontier is
no longer construction — it is **validation**. The old Themes A–H (funnel, handoff, trust,
SEO, retention, forms, differentiation, revenue rails) are ~90% shipped and roll up into
"Already done." What re-organizes everything now is one thesis:

> **Own the audit loop — and prove the hope for ~$0 before building against it.**
> The evidence says the catalog-as-company fails on moat and conversion; the operator's hope
> (that free attention converts, that the loop accretes switching cost, that the flag gets
> planted before Anthropic bothers) is *plausible but unproven*. The whole "Now" is the six
> cheap pre-tests that test that hope — and the one measurement that reads them.

The single biggest re-prioritization: the old roadmap filed raw-fetch counting (R05) as a
low-drama "flag to the maintainer." **Post-pivot it is the measurement spine** — every
validation gate returns an unreadable signal without it (BLINDSPOTS F1: "optimizing a ratio
whose numerator is invisible").

---

## 1 · Sources

**Read this run — the seven venture reports (fresh effort):** NICHE (61) · DEMAND (62) ·
COMPETITORS (63) · MARKET (64) · POSITIONING (65) · MOAT (66) · VERDICT (67).
**Read this run — reports the old roadmap predates:** BLINDSPOTS (meta-audit, 2026-07-10) ·
BREADCRUMBS (145).
**Carried forward from the 2026-07-09 synthesis** (their product items already digested there,
statuses updated below): FUNNEL · COMPETITIVE · REVENUE · AI-IDEAS · SEO · CRO · RETENTION ·
PROOF · ACTIVATION · FORMS · CHECKOUT (null) · BUGS · SECURITY-AUDIT · IMPROVEMENTS · DX ·
CREDIBILITY · COMPREHENSION · BRAND · HIERARCHY · COLOR · LAYOUT · TYPOGRAPHY · STATES ·
SHOWCASE · FIXLOG.
**Total on hand:** 34 audit reports (27 product + 7 venture) + this ROADMAP. `reports/` is the
write target and it exists — writing here.

**Missing — and which absence would most change this roadmap:**
- **The WTP / launch signal is the missing evidence that would most change the roadmap — and
  it is not an in-repo audit.** VERDICT, MARKET §4 and NICHE §4 all rule that the one number
  that decides the thesis (does free attention convert to a paid dollar; does a genuine launch
  clear a few hundred stars) is knowable *only* from real customer conversations + a real
  launch. No further desk audit substitutes. **Run the pre-tests (§4 Now), not another brief.**
- **An EVALS / brief-efficacy report — the highest-value absent *in-repo* audit.** BLINDSPOTS
  F4/§8.4: the linter verifies *shape* (4-phase, ask-first, 4k cap), never *substance* — "a
  hollow brief that pattern-matches passes clean." The pivot just made the quality-bar claim
  prominent (shipped item d); nothing proves it. Seeded-defect fixtures + expected-findings
  assertions would convert the claim from shape to truth. No brief for this exists yet.
- **A11Y.md (brief 86)** — still absent; FORMS FV3 (every error unannounced to screen readers)
  + BLINDSPOTS §5.5 (zero a11y verification while selling brief 86) make it the top
  product-hygiene gap. It won't change the *strategic* sequence, so it sits in Later.
- **PERF.md** — SEO-2's 572 KB homepage + BLINDSPOTS #6 (catalog ships twice, 228 KB;
  bodies.json 420 KB precached) would size the payoff of the body-stripping work. Later.
- **OPPORTUNITIES.md (Founder Funnel stage 60)** — absent *by design*; the funnel starts at 61
  and the venture is fixed. VERDICT confirms the ruling survives its absence completely.

---

## 2 · Unified backlog (deduped)

Grouped by the pivot's logic. `sources` cite the reports each item traces to; nothing here is
new. The ~50 shipped product items + the 4 pivot changes are rolled into **Already done** at
the end rather than re-listed.

### A — Validation gates (the pivot's $0 pre-tests) — *the whole reason to re-run*

| id | item | tag | sources | impact | effort | deps |
|---|---|---|---|---|---|---|
| G1 | **Test WTP before building** — point a little attention at the (now-locked) `/teams` surface, **count inbound intent**, and in parallel ask DEMAND's ten named sufferers the flat-fee-team-audit question to their face. 3–5 real "what does it cost / can you do this for us" emails = the cheapest proof of non-zero WTP. Zero intent → demote to attention-play + SKU B only. | test | VERDICT act.1 · MOAT kill#2 · DEMAND "ten people" · REVENUE §3.2/§4 · MARKET §4 | H | S | M1 (counting) + G2 (attention to measure) |
| G2 | **One loud distribution swing** — Show HN + an `awesome-claude-code` inclusion PR + this repo's own BUGS.md hero finding as the dogfood hook; measure the star/fetch response. Can't clear a few hundred stars → the base-rate bear is confirmed and the funnel is moot. Doubles as the only lever the survivability fail leaves: **speed** — plant "audits/briefs" as the category noun before the platform owns it. | test/ext | VERDICT act.2 · MOAT kill#3 · NICHE §3 · COMPETITORS traction · (old R60 launch half) | H | S | M1, M2 (install path), U1+U2 (don't launch into a broken funnel) |
| G3 | **Prove the loop is the product** — demonstrate report→Studio→47·Fixer→FIXLOG as one motion **end-to-end on a real external repo**, not self-dogfood. The only surface with a *path* to a moat (accreting per-repo report+fix history → switching cost). Can't beat "just rerun it" → the product-axis pivot reverts toward kill. | test | VERDICT act.3 · MOAT §3 loop · COMPETITORS wedge 1 · BLINDSPOTS §7 | H | M | none (uses shipped loop) |
| G4 | **Submit goal-prompts to `anthropics/claude-plugins-official`** — the absorption pre-test. Distributed → absorption becomes co-option; rejected on its quality bar → you learned the rail is closed before betting on it. | test/ext | MOAT kill#1 pre-test | M-H | S | M2 helps |
| G5 | **Publish the honest token cost** of the heaviest brief run at current API rates — confirm a full audit is cents-to-low-dollars. If one run costs more than it returns to a solo dev, the "effortless vs. doing-nothing" wedge is dead on arrival. | test | MOAT kill#4 pre-test · NICHE §1 | M | S | none |
| G6 | **Ask the beachhead the privacy-vs-"learnings" question** — would they trade privacy for a compounding cross-run feature? A "no" (likely) means the ceiling is a head-start business; size ambition to match, don't raise against a moat that structurally can't exist. | test | MOAT kill#5 pre-test · NICHE §4 | M | S | part of G1 interviews |

### B — Measurement & external unlocks (carried open; they *enable* the gates)

| id | item | tag | sources | impact | effort | deps |
|---|---|---|---|---|---|---|
| M1 | **Turn on `/raw/*` + `commands.tar.gz` fetch counting** (Vercel log filter, zero code — `middleware.js.example` is inert on purpose). *Re-prioritized from a footnote to the measurement spine:* without it G1/G2 return no readable signal. | ext | old R05 · FUNNEL §4.3 · REVENUE §4.4 · BLINDSPOTS §1.3/F1 | H | S | Vercel dashboard |
| M2 | **npm publish + MCP-registry listing** — package is publish-ready, workflow ships; gives the launch (G2) an install path and feeds G4. | ext | old R59 · IMPROVEMENTS 11 · CREDIBILITY 3 · BLINDSPOTS §1.2 | H | S | NPM_TOKEN + release |
| M3 | **`.github/FUNDING.yml` + Sponsors footer link** — SKU B's only rail; one file. Expect ~$0 until stars exist; ship anyway (MOAT: "backers are gratitude, not a model"). | ext | old R53 · REVENUE §2/§4.5 · MOAT §2 | L-M | S | Sponsors profile exists |
| M4 | **R60 residuals** — confirm the dormant hero star-badge threshold (25); rule quotes real-or-illustrative. *The Discussions dead-end is resolved:* `PARTNER_CTA_URL` now points at a GitHub **issue**, which resolves. | ext | old R60 · CREDIBILITY · PROOF NF3 | M | — | maintainer calls |

### C — Launch-blockers (BLINDSPOTS P0s the pivot pulls INTO Now — you can't Show HN into these)

| id | item | tag | sources | impact | effort | deps |
|---|---|---|---|---|---|---|
| U1 | **Mobile nav amputates the catalog** — at ≤720px the nav drops *Catalog*; Studio/Vitals/Examples show zero nav links; the mobile landing is 12,418px of scroll. A launch drives mobile traffic into a dead end. Add a disclosure menu; keep Catalog + CTA. | ship | BLINDSPOTS §4 P0-1 | H | S-M | none |
| U2 | **The proof surface dead-ends into raw markdown** — `examples/` cards link to `/reports/*.md` as an unstyled text dump with no nav or way back. The single most persuasive artifact (the dogfood report the launch points at) renders as a wall of text. Render reports to styled HTML (the CHANGELOG→changelog.html machinery exists) or open in Studio. | ship | BLINDSPOTS §4 P0-2 · SHOWCASE · PROOF | H | M | none |

### D — Claim-defense & product-truth (BLINDSPOTS, re-weighted by the pivot)

| id | item | tag | sources | impact | effort | deps |
|---|---|---|---|---|---|---|
| T1 | **Brief-efficacy evals** — seeded-defect fixtures + expected-findings assertions; publish pass rates on `/quality`. *The pivot made the quality-bar claim load-bearing (shipped item d); this is the audit that makes it true.* | ship | BLINDSPOTS F4/§8.4 · POSITIONING C · COMPETITORS wedge 2 · FABLE_BUILD_QUEUE 2 | H | M | none |
| T2 | **Search silently collapses recall** — landing search runs metadata-only, merges bodies in only on *zero* results ("top 1 for 'security'" while the chip says 11). Idle-prefetch `bodies.json` (already SW-precached) and always full-text. | ship | BLINDSPOTS §3.1/§4 P1-3/F5 | M-H | S-M | none |
| T3 | **Trust orphans** — no `SECURITY.md` (and `vercel.json` redirects `/SECURITY.md` to a marketing report); copied prompts are unversioned (a report can't be traced to the brief text that made it); `gp-aid` persistent id vs the "no tracking" claim has no privacy page/opt-out; no consumer-side "spot-check citations before ticking Fixer boxes" guidance. *These defend the "evidence, not vibes" moat the pivot leans on.* | ship | BLINDSPOTS §5.1/§5.2/§5.4/§5.6 · PROOF NF2 · RETENTION R12 | M-H | S-M | none |
| T4 | **Architecture paydown** — search logic triplicated (site fuzzy vs MCP word-boundary; parity guard misses the divergence — highest-leverage fix); detail-page inline JS never syntax-checked (183 pages); 16-stage conductor cap is a build failure Design is one brief from hitting; SITE_CSS inlined into 183 committed files. | ship | BLINDSPOTS §3.1/§3.2/§3.5/§3.3 | M | M-L | none |
| T5 | **Prune — apply Subtract to itself** — 37 playbooks → ~15; designate a hub brief per large family; mandate `related:` inside the overlap clusters (Design 54–59/132, growth 09/75/80/109/110, testing 02/100–102); trim the 7-channel/21-family surface. | ship | BLINDSPOTS F6/§6/§8.7 | M | M | none |
| T6 | **Commit to the diff loop as the retention spine** — generalize vitals/HEALTH.md and the universal dated re-run rule to every report re-run (the compounding-switching-cost mechanism G3 tests). | ship | BLINDSPOTS §7/§8.6 · MOAT §3 · RETENTION | M | M | after G3 proves it |
| T7 | **Coverage-gap briefs** (demand-ranked) — mobile-native, supply-chain security, pricing & packaging, background jobs/queues, alert/pager health, realtime/offline sync. Plus **A11Y (86)** + a PERF pass. | ship | BLINDSPOTS §6 · FORMS FV3 | M | M-L | none |
| T8 | **Promote three brief shapes to first-class** — Monitor (29), Generator (47/142 gate → artifact), Scored-gate (144 → machine-parseable), the shapes the Studio parser most wants. | ship | BLINDSPOTS §6/F2 | M | M | none |

### E — Revenue (built; deliberately HELD until G1 returns a positive signal)

| id | item | tag | sources | impact | effort | deps |
|---|---|---|---|---|---|---|
| X1 | **SKU A — flat team-audit, services-first** (private catalog + custom linted briefs + standing CI audits + support; *never* per-seat). The survivor model, delivered as an engagement first, productized only if WTP proves out. | gated/ext | MOAT §1 · MARKET Phase 1 · REVENUE §2 | M | — | **hard-gated on G1** |
| X2 | **`/partners` rate-card upgrade + post-activation backer nudge** — do NOT build further until audience/WTP exists; the surfaces already ship. | gated | REVENUE §4.3/§3.3 · old R55/R56 · BLINDSPOTS §8.7 | L | S-M | G1 + M1 numbers + M3 |

### F — Carried Later (data- / decision- / moat-gated)

| id | item | tag | sources | impact | effort | deps |
|---|---|---|---|---|---|---|
| L1 | Offline search-alias table, tuned by `search_zero` misses | gated | old R51 · AI-IDEAS 5 | M-L | M | `search_zero` data (needs M1) |
| L2 | Real 10–15s screen recording of a brief run | ext | old R61 · SHOWCASE F1 · CREDIBILITY 1 | M | — | capture tooling |
| L3 | BREADCRUMBS residue — *largely applied in 0.16.0* (vitals/examples/manifest/metrics now classified in CLAUDE.md); remaining: name `vercel.json` in README, the two unwritten build gates in CONTRIBUTING, the CONTRIBUTING→CLAUDE.md backlink | ship | BREADCRUMBS §Fixes | L | S | none |

### Already done (rolled up — so nothing looks lost)

**Shipped in 0.14.0 (PR #27):** the entire old Themes A–H product backlog — R01–R52, R54–R56,
R63–R66 (funnel instrumentation, handoff/copy-hint fixes, honesty-drift batch, SEO quick-wins +
static catalog, Weekly-Vitals loop, forms integrity, skills-tree/Brief-Forge/differentiation
bets, revenue rails incl. `/teams` + `/partners` pages). **Shipped 0.15.0/0.16.0:** ledger
redesign, design engine, breadcrumb cross-links, dogfood reports to `reports/`.
**Shipped in the pivot (54ae65f/ae724d5):** register re-badge (POSITIONING/COMPETITORS/NICHE) ·
loop legible in Proof (VERDICT act.3 / old R50) · `/teams` WTP surface locked (VERDICT act.1 /
old R52+R55) · quality-bar claim surfaced (COMPETITORS wedge 2 / old R50). **Decision taken:**
**R62** (proceed/pivot/drop) — VERDICT ruled **PIVOT — axis: product**. **Closed earlier:**
BUGS 1–5, SECURITY 1–4, COMPREHENSION, LAYOUT, TYPOGRAPHY, STATES, HIERARCHY, COLOR, BRAND,
SHOWCASE F2–7, DX, IMPROVEMENTS (except publish = M2). CHECKOUT: null by design.

---

## 3 · Themes — root causes worth one structural fix

1. **The whole product was built to verify the proxy, not the value** (BLINDSPOTS' one-line
   verdict, and VERDICT's independently). Lint the skeleton not the efficacy; guard the
   conductor text not the search semantics; optimize the funnel not the traffic; mark the
   finding fixed without wiring the fix. **One structural fix, not five patches:** stop
   building storefront and *measure the value* — G1+G2+M1 turn "installs → confirmed run →
   inbound WTP" into observable numbers. Everything tagged `gated` is downstream of this.
2. **The money and the only moat-path both sit one layer over, in the loop — not the catalog.**
   DEMAND ("WTP is High for execution, ~Zero for the catalog"), MARKET (catalog TAM = $0),
   MOAT (no data moat by design; the loop is the only candidate with a compounding mechanism),
   COMPETITORS (post-run loop is "the one gap open because hard") all name the same seam. **One
   fix:** make the loop the product — G3 proves it on a real repo, T6 makes the diff-history
   the retention spine, and the catalog demotes to a top-of-funnel *attention* asset.
3. **Distribution is the gate and the clock — 0★ is invisible, and the window closes when
   Anthropic decides to own "audits."** NICHE §3 (the star economy is border control), MARKET
   §3 (first-mover matters only for the noun + loop, *only if the flag is planted loudly
   first*), MOAT kill#1 (negative strategy tax; "not a moat, a countdown"). **One fix:** the
   loud launch (G2) is not marketing polish — it is the existential first test *and* the only
   defense the survivability fail leaves (speed).
4. **The quality-bar claim is now load-bearing but unproven.** The pivot surfaced
   "machine-enforced quality bar" as a headline differentiator (shipped) precisely because
   POSITIONING/COMPETITORS/NICHE agree it's the one counter-belief no rival can copy — while
   BLINDSPOTS F4 shows the linter checks shape, not substance. **One fix:** T1 (efficacy evals
   published on `/quality`) makes the claim true, or the pivot's own differentiation is vibes.
5. **Honesty drift is now a moat threat, not cosmetics.** The pivot bets everything on
   "evidence, not vibes"; T3's orphans (no SECURITY.md, unversioned copied prompts, the gp-aid
   vs "no tracking" gap, no consumer-side report-judgment guidance) each quietly contradict it.
   Cheap to fix, expensive to be caught on at launch.

---

## 4 · Sequence & milestones

### Conflicts, ruled

- **THE hinge: venture "test WTP before building revenue" vs product "build the rails now."**
  REVENUE.md sequenced monetization as *plumbing built now, sold later* and proposed the
  `/partners` rate-card + backer nudge as next steps. MOAT/MARKET/VERDICT overrule that: at the
  **sourced 1–3% dev-tool conversion floor** (MOAT corrected MARKET's optimistic 5–20% against
  a benchmark — and won the argument, because the number is *sourced*, more conservative, and
  structurally right: converting free→paid *with no wall* is strictly harder than the walled
  comparable). **Ruled with MOAT/VERDICT:** the rails are already built; more revenue plumbing
  is wasted motion until *one team says "I'd pay."* The next revenue action is a **$0 WTP test
  (G1)**, not a rate card. X1/X2 are `gated` on G1's signal. *The evidence favors the pessimist
  here, and the pivot's discipline forbids letting optimism launder the napkin.*
- **BLINDSPOTS "demote /teams+/partners to a contact line" vs VERDICT "keep /teams as the WTP
  test surface."** Reconciled: **keep** the minimal, now-locked `/teams` surface (it *is* the
  cheap test the pivot needs — price anchor + one intent CTA already shipped); **hold** any
  further `/partners` build (X2). Minimal surface as instrument, no further plumbing.
- **Old roadmap's Theme H "revenue rails = inventory to accumulate" is downgraded.** It wasn't
  wrong in 0.14.0 (rails are cheap); the pivot re-weights it: inventory with a structurally-null
  conversion step is not an asset until the step is proven non-zero.
- **R05 (raw-fetch counting): old "low-drama external" → now the measurement spine.** Re-ruled
  up (M1, H-impact) because every validation gate is unreadable without it (BLINDSPOTS F1).
- **Carried from 2026-07-09 (still valid):** homepage weight — SEO-1 static cards shipped;
  SEO-2 body-stripping stays sequenced behind, now folded into a PERF pass (T7/Later).

### Now (1–2 weeks) — *prove the hope for ~$0, and don't launch into a broken funnel*

The pivot's entire near-term: run the six cheap pre-tests, turn on the one measurement that
reads them, give the launch an install path, and fix the two P0s a Show HN would expose.
Nothing here builds new product surface; it *tests the surface that exists.*

**Test (gates):** G1 · G2 · G4 · G5 · G6 · (G3 kick-off).
**Enable — flag to maintainer immediately (they gate the gates):** M1 (raw-fetch counting) ·
M2 (npm publish) · M3 (FUNDING.yml).
**Ship (launch-blockers):** U1 (mobile nav) · U2 (styled report pages).
*Why this order:* the launch (G2) is the gate everything upstream feeds and the only defense
speed buys — but it is worthless if the numerator is invisible (M1), has no install path (M2),
or drives mobile traffic into a dead end and the proof into a text dump (U1/U2). WTP (G1) is
measured *from* the attention G2 creates, so they run together, not in series.

### Next (a month) — *react to the signal; make the two claims the pivot leaned on TRUE*

Branch on what Now returned. If WTP/distribution fire: stand up the SKU-A delivery motion (X1)
and pay down what a scaling launch would strain. Either way: defend the differentiation the
pivot made prominent.

**Ship:** T1 (efficacy evals — make the quality bar true) · T2 (full-text search) · T3 (trust
orphans — defend "evidence not vibes") · T4 (architecture paydown) · G3 (finish the
external-repo loop proof) · M4 (R60 residuals).
**Gated:** X1 (SKU-A engagement) — *only if G1 returned real intent.*
*Why this order:* Now proved (or killed) the thesis; Next spends the proof — T1/T3 close the
gap between the claims the pivot shipped and the substance behind them, before a bigger
audience arrives to check.

### Later — *moat-, data-, and decision-gated*

**Ship:** T5 (prune — Subtract on itself) · T6 (diff-loop retention spine, after G3) · T7
(coverage-gap briefs + A11Y + PERF) · T8 (promote brief shapes) · L3 (breadcrumb residue).
**Gated:** X2 (`/partners` + backer nudge, after WTP) · L1 (search aliases, after `search_zero`
data) · L2 (screen recording).
*Why last:* every item here is deliberately blocked on a positive WTP signal, accumulated data,
a maintainer decision, or the loop being proven first — starting earlier means building against
numbers that don't exist yet, exactly the failure mode BLINDSPOTS diagnosed.

---

## 5 · Merge log (deduplications — nothing lost)

- **The pivot decision** ← DEMAND's proceed/pivot/drop question (old **R62**) + all six funnel
  reports → **VERDICT: PIVOT — axis: product.** R62 is closed, not open.
- **WTP validation** ← VERDICT act.1 + MOAT kill#2 + DEMAND "ten people" + REVENUE §3.2/§4 +
  MARKET §4 → **G1**; the `/teams` *surface* it tests is **done** (pivot item c / old R52+R55).
- **Distribution swing** ← VERDICT act.2 + MOAT kill#3 + NICHE §3 + COMPETITORS traction +
  old **R60** launch half → **G2** (G2 subsumes R60's "Show HN to earn first stars"; R60's
  Discussions concern is resolved — CTA repointed to Issues; residuals → M4).
- **Own the loop** ← VERDICT act.3 + COMPETITORS wedge 1 + POSITIONING Option A + old **R50**
  (loop-legibility half, now **done**) → the *legibility* shipped; the *external-repo proof*
  is **G3**; the *retention-spine* half is **T6**.
- **Revenue model** ← REVENUE.md's five tiers **merged with** MOAT §1 / MARKET Phase 1:
  strongest framing kept is **MOAT's** (flat team-audit services-first = SKU A; sponsorship
  audience-gated = SKU B; reject per-seat/usage/transaction/marketplace). The evidence favors
  MOAT's **sourced 1–3% conversion ceiling** over REVENUE's un-benchmarked optimism, so both
  SKUs are **gated (X1/X2)**, not scheduled.
- **Quality bar** ← POSITIONING C + COMPETITORS wedge 2 + NICHE exploit 3 (the *claim*, now
  **done**/surfaced) **+** BLINDSPOTS F4 (the *proof*, still open) → **T1** makes the shipped
  claim true.
- **Measurement** ← old **R05** + FUNNEL §4.3 + REVENUE §4.4 + BLINDSPOTS §1.3/F1 → **M1**,
  re-ruled from footnote to spine.
- **Analytics/trust honesty** ← PROOF NF2 + RETENTION R12 (gp-aid disclosure) + BLINDSPOTS
  §5.4 (gp-aid privacy) + §5.1 (no SECURITY.md) + §5.2 (unversioned prompts) → **T3**.
- **Proof placement** ← old R25/R27 (**done** — hero pointer, examples section) **+**
  BLINDSPOTS §4 P0-2 (the reports render as a text dump) → the *new, open* half is **U2**.
- **Old Themes A–G product backlog** (R01–R52, R54–R56, R63–R66) → rolled into **Already done**
  (0.14.0), not re-listed.
- **BREADCRUMBS** ← brief 145 residue; the four headline fixes were **largely applied in
  0.16.0** (CLAUDE.md now classifies vitals/examples/manifest/metrics); the small remainder →
  **L3**.
- **CHECKOUT.md** merged as a null (no payment surface by design); its only successors are the
  gated revenue SKUs (X1/X2).

---

*Report only — synthesis, no code changed. Should we adjust the sequence — e.g. is the launch
swing (G2) too early before the P0 fixes (U1/U2) land, should brief-efficacy evals (T1) move
into Now to defend the quality-bar claim the moment it went live, or should any revenue item be
un-gated?*
