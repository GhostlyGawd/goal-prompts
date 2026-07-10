# BLINDSPOTS.md — deep-dive meta-audit of goal-prompts

- date: 2026-07-10
- method: five parallel audit tracks (UX-from-rendered-pixels, build architecture,
  catalog content, product strategy, adversarial cross-cutting sweep), synthesized.
  Not the output of a catalog brief; a one-off meta-audit of the whole product.
- scope: every system and surface — site, briefs, build, distribution channels,
  business pages, and the repo's own decision/report corpus.

## 0 · The one-paragraph verdict

The product is a beautifully machined answer to the wrong layer of the question.
Its own dogfood reports already knew this: DEMAND.md locates willingness-to-pay
in the execution layer and "~Zero" in the catalog layer; COMPETITIVE.md names the
headline gap as "distribution and proof, not features"; docs/usage-metrics.md
designs the usage instrument and states "Nothing in this document is live." The
repo then shipped ~50 storefront optimizations while the three items that create
an audience (npm publish, launch, measurement) stayed open and the pivot decision
(ROADMAP R62) stayed permanently deferred. Every blind spot below is a variation
on one failure mode: **verifying the verifiable proxy instead of the value** —
lint the skeleton not the efficacy, guard the conductor text not the search
semantics, optimize the funnel not the traffic, mark the finding fixed without
wiring the fix.

## 1 · The unknown knowns — admitted in this repo's own documents, ignored by the product

Each of these is written down, in this repo, by this project's own process — and
the shipped state contradicts it.

1. **"The money is one layer over" — decision never taken.** DEMAND.md's closing
   verdict (execution wedge vs catalog) was filed as ROADMAP R62 "external
   (founder decision)" and never ruled on. ADR-9 answered a different question
   (Build-family products) without ruling on the wedge.
2. **"Distribution and proof, not features" — then a 50-item feature sprint.**
   COMPETITIVE.md §1 vs ROADMAP's execution log: R01–R52 shipped; R59 (npm
   publish), R60 (launch/Discussions), R61 (demo recording) — the only
   audience-creating items — remain open. metrics.json: 0 stars, 0 forks.
3. **The usage instrument is designed, zero-code, and off.** docs/usage-metrics.md
   ("Nothing in this document is live"), middleware.js.example ("INERT ON
   PURPOSE"), five separate reports flagging raw-fetch counting as the gating
   instrument (FUNNEL §4.3, REVENUE §4.4, RETENTION §4, PROOF §4, COMPETITIVE §4).
   CLAUDE.md sells raw/ fetch counts as "an honest usage metric"; nothing counts
   them. Consequence: the maintainer cannot answer "which briefs get run" for
   ANY channel — plugin/installer/MCP users generate zero observable events.
4. **ADR-9 parked monetization; /teams and /partners shipped anyway.** The
   append-only decision log — the asset the whole harness thesis depends on —
   is contradicted by build.py's teams_page/partners_page, selling against an
   audience REVENUE.md calls "unproven and unmeasured," with a partner CTA
   pointing at GitHub Discussions, which is not enabled.
5. **The flagship loop leaks on its own repo.** ACTIVATION.md §0: a finding was
   dispositioned **fixed** while "the fix shipped everywhere but where the
   finding pointed." RETENTION R12: gp-aid shipped undocumented against the
   prior report's explicit instruction. The report→Fixer→FIXLOG loop is the
   product's differentiation and it demonstrably drops findings.
6. **Briefs can produce confident, verifiable, worthless output — and nothing
   evals them.** ADR-12: ten design passes "produced changes users could not
   perceive… design edits shipped on plausibility alone." The fix (render the
   pixels) was applied to this repo's own workflow only — never generalized to
   the 146 briefs sold to users. FABLE_BUILD_QUEUE item 2 admits rubric evals
   are the missing layer; unstaffed.
7. **The harness has never been traversed.** HARNESS_PLAN §8's done-criteria
   (one product repo, first dollar, three HEALTH.md rows) don't exist;
   FABLE_BUILD_QUEUE item 1 admits "the first traversal is the eval of the
   harness itself." ADR-9's revenue theory rests on an untested path.

## 2 · The underlying logical flaws

- **F1 — A conversion-shaped storefront with no traffic and no conversion
  signal.** The site is meticulously instrumented for on-page events while the
  product's actual conversion (a brief getting *run*) happens off-site, 10–20
  minutes after the last click (FUNNEL.md), on channels that emit nothing.
  Optimizing a ratio whose numerator is invisible and whose denominator is ~0.
- **F2 — The report is treated as the product; the user wants the change.**
  The read-only-report formula is the catalog's identity, and the repo has
  already quietly invented every escape hatch — 47 (fixer), 29 (monitor),
  142 (generator), 144 (scored gate) — without promoting any to a first-class
  brief shape. 123/146 briefs use the literal header "Audit through N lenses";
  78 land on exactly 7. The formula is audibly mechanical.
- **F3 — Static prompt text is the commodity layer.** The durable assets here
  are the report grammar, the linter, the diff/re-run rule, and the Studio→Fixer
  loop — all of which point at an execution product (scheduled runner, trend
  dashboards) that exists only as an example YAML file and one page (vitals)
  reachable mainly from the footer.
- **F4 — Quality gates verify shape, never substance.** The linter checks the
  4-phase skeleton, char cap, and ask-first gate; a hollow brief that
  pattern-matches passes clean. No seeded-defect evals, no cross-brief
  similarity check, no consumer-side "how to judge a report" guidance anywhere.
- **F5 — "stdlib-only" drifted into "one language" dogma.** Node is already a
  first-class runtime (MCP server, test suites, syntax gates), yet search logic
  is triplicated across Python/Node/browser with a string-matching parity guard
  that misses the part that actually diverged. The honest constraint is "no
  runtime deps, no build-time npm install," not "one language."
- **F6 — Strategy by accretion.** 7 distribution channels, 37 playbooks,
  21 families, 146 briefs — each addition individually defensible
  (COMPETITIVE.md "table stakes"), collectively an unprioritized surface that
  multiplies maintenance and dilutes the story. The repo ships a *Subtract*
  family and has never applied it to itself at the product level.

## 3 · Architecture blind spots (ranked, with effort)

1. **Search semantics silently diverge across runtimes.** Site: substring +
   edit-distance fuzzy (js/catalog-core.js); MCP server: word-boundary regex,
   no fuzzy (mcp/server.cjs:157). The smoke-test parity guard checks conductor
   *text* only. Fix: add `js/` to npm files, make server.cjs require
   catalog-core, delete the duplicates and the guard. ~half a day; highest
   leverage in the repo.
2. **Detail-page inline JS is never syntax-checked.** scripts/check parses
   inline scripts in index/studio/vitals only; the 183 generated b/ and p/
   pages carry Python-string JS with no gate. Fix: extend the vm.Script loop
   to one sample of each. ~10 lines.
3. **~17KB of SITE_CSS inlined into each of 183 committed pages** (~3MB
   duplication; one CSS tweak rewrites 183 tracked files, destroying diffs and
   blame). Fix: emit site.css and link it (tokens.css already proves the
   pattern). ~1 hour.
4. **Page chrome exists in 4+ hand-maintained copies with no guard** — the
   theme-toggle script alone has four literal copies (build.py, template.html,
   studio.html, vitals.html). Fix: shared chrome.css + js/theme.js, or generate
   studio/vitals heads from build.py. ~1 day.
5. **A growth ceiling encoded as a build failure.** The 16-stage conductor cap
   (build.py:205) × auto-built family conductors: Design is at 15 briefs; the
   17th fails the whole build with no splitting mechanism. Fix: auto-chunk
   family conductors. ~half a day.
6. **The catalog ships twice in index.html** (injected JSON + server-rendered
   cards, 228KB), and the SW precaches bodies.json (420KB) + 5 fonts for every
   visitor on first paint. No pagination story at 300 briefs. ~1–2 days.
7. **Behavioral test void.** 1,320 lines of inline template.html JS get only a
   parse check; js/gp-detail.js (runs on all 183 detail pages) has no suite;
   vitals.html reimplements its own untested markdown-table parser instead of
   using the *tested* js/report-parser.js. One jsdom smoke of render() covers
   more product surface than everything else combined.
8. **build.py is a god-module** (8 responsibilities, 2,274 lines). Mechanical
   split into lint/render/assets. ~1 day, no behavior change.
9. **Ungated assets institutionalize silent staleness** — metrics.json and
   img/studio.png refresh out-of-band with no age check; committed zips bloat
   .git (26MB) monotonically.

## 4 · UX / navigation findings (from rendered pixels)

**P0**
1. **Mobile nav amputates the product.** At ≤720px the nav drops How-it-works
   and *Catalog*; ≤480px drops the CTA; no hamburger. Studio/Vitals/Examples
   show **zero** nav links on mobile. The mobile landing page is 12,418px tall
   and the only route to the catalog is scroll. Fix: mobile disclosure menu;
   if pruning, keep Catalog + CTA, drop the secondaries.
2. **The proof surface dead-ends into raw markdown.** examples/ cards link to
   /reports/*.md — unstyled plain text, no nav, no way back. The single most
   persuasive artifact renders as a text dump. Fix: render reports to styled
   HTML (the CHANGELOG→changelog.html machinery already exists) or open them
   in the Studio.

**P1**
3. **Search silently collapses recall.** Landing search runs on metadata only;
   bodies merge in only on *zero* results — "top 1 for 'security'" while the
   Trust chip says 11. Fix: idle-prefetch bodies.json and always search full
   text (it's already SW-precached), or upgrade when results < N.
4. **Half the site hangs off the footer.** Vitals, examples, quality, teams,
   partners, changelog have no top-nav or breadcrumb presence; b//p/ pages get
   breadcrumbs, tool pages don't. Promote Vitals next to Studio (they're a
   pair) and unify the breadcrumb pattern.
5. **The playbook storefront is an unexplained chip wall** — ~31 bare chips
   after the 6 featured cards, no descriptions or grouping. Group by intent or
   reuse the quick-view pattern.
6. **Two different sites' navs** — landing (uppercase mono, "Browse catalog")
   vs every generated subpage (sentence-case sans, "Get started"). Per
   DESIGN_DIRECTION rule 4, the subpages are off-direction.

**P2** — chips/buttons below 44px touch size; first-viewport text-wrap glitches
(hero callout, orphaned ▸ chevron); quick view opens an unframed full-viewport
text wall with the close affordance scrolled away; keyboard nav (/, Cmd+K, j/k)
fully wired but hinted nowhere; Studio/Vitals open empty instead of auto-loading
the sample (the "no visualizations" complaint is mostly this); the example
filename — the row's concrete payload — is what mobile truncation cuts.

**Counter-evidence (complaints that don't reproduce):** progressive disclosure
exists (the pick-a-question gate before the card wall); motion is present,
tasteful, and reduced-motion-aware; copy feedback (toast + mark-it-run) is
excellent; no horizontal scroll at 390px; dark mode is clean everywhere; the
"ledger" direction is being executed *well* — the problems are navigation
plumbing, search recall, and empty-by-default tools, all fixable inside the
existing direction. The one direction-level friction is mono-metadata density
at 12px on small screens, which needs a mobile relaxation, not a redesign.

## 5 · Cross-cutting orphans

1. **Fetch-and-execute trust chain.** Conductors tell agents to curl live URLs
   and "execute exactly as written," then 47/Studio-Fixer modifies code; the
   installer's checksums come from the same origin they'd defend against. No
   version pinning, no per-brief hashes, no threat model. (The MCP server's
   local input validation is clean.)
2. **Copied prompts are unversioned snapshots.** The installer and MCP stamp
   versions; the two most-promoted flows (copy button, raw/ URLs) don't — so a
   report can never be traced to the brief text that produced it, and the
   linted "lead with what changed" re-run rule can't distinguish brief drift
   from repo drift. Fix: one provenance line in raw bodies + report footers.
3. **No vulnerability-disclosure path** — no SECURITY.md anywhere, and
   vercel.json permanently redirects /SECURITY.md to a marketing audit report.
   build.py even reserves SECURITY.md as a protected community filename.
4. **gp-aid vs the privacy claim.** A persistent per-device id attached to
   every analytics event, plus logged search terms, alongside "no cookies, no
   cross-site tracking" — GDPR-wise a durable identifier is consent-scoped like
   a cookie. No privacy page, no opt-out, no rotation.
5. **Zero accessibility verification while selling an a11y brief** (86). Hand-
   authored a11y is genuinely good; nothing guards it — no axe/pa11y in
   scripts/check, and among 28 dogfood reports there is no A11Y.md.
6. **Consumer-side report judgment is nobody's job.** Nothing anywhere says
   "spot-check citations before ticking Fixer boxes"; hallucinated-but-well-
   formatted findings flow straight into code changes.
7. **Plugin staleness** — no version anywhere in plugin command files; no
   in-product "you're N versions behind."
8. **manifest.json drifted from the ledger palette** (#131417 vs #15120D), no
   maskable icons, no build gate — unlike the count-guarded OG cards.
9. **i18n has neither an implementation nor an ADR** saying "deliberately never"
   — the only major axis with no recorded decision.

**Clean (checked):** stars badge threshold-gating, README count gates, CI drift
guard (airtight), sitemap/robots, CHANGELOG discipline, Studio parser's honest
degradation on malformed input.

## 6 · Content: catalog health, gaps, and shapes

- **Overlap clusters to merge or signpost:** Design micro-lenses 54–59 + 132
  (six audits citing the same CSS); Growth conversion path 09/75/80/109/110;
  dependency pair 07/85; findability quartet 14/16/52/145; testing quartet
  02/100/101/102. The hub-and-spoke signposting that 118 does well ("for the
  defensive review, run 35") is missing exactly where it's needed; `related:`
  is sparsely used in these clusters.
- **Real coverage gaps (ranked by demand):** mobile-native (iOS/Android — zero
  coverage), supply-chain security (lockfiles, provenance, CI secret exfil —
  distinct from 07/85's dependency *quality*), classic ML/data-science (the
  Agent family is LLM-only), pricing & packaging, background jobs & queues,
  alert quality/pager health, realtime & offline sync correctness, support ops.
  Honorables: experimentation rigor, cloud-bill/IaC cost, docs-site IA.
- **Non-gaps (verified before claiming):** frontend perf, i18n, a11y, incident
  response, repo DX, DB perf, licensing, email, search, IaC, growth loops.
- **Shapes to promote from exception to first-class:** **Monitor** (29 is the
  prototype; the linter already forces the diff grammar on every brief — vitals
  is its surface), **Generator** (Phase-2 scope gate like 47/142, deliverable
  is the artifact: the missing tests, evals, runbooks), **Scored gate** (144
  generalized: bars before scoring, binary ruling, machine-parseable — what the
  Studio parser most wants). The 4,000-char cap is a non-issue (median 2,711).
- **Choice architecture:** 146 briefs are navigable only through 37 playbooks,
  which are themselves too many to scan. Prune playbooks to ~15, designate a
  hub brief per large family, mandate `related:` inside overlap clusters.

## 7 · Are goal prompts the right implementation?

**As content, yes. As the product layer, no — and the repo's own reports said
so first.**

The strongest case FOR the current form: zero backend, zero COGS, the only
machine-enforced quality bar in the category, a parseable report grammar
feeding a closed loop no rival owns, privacy as differentiation, and one
markdown source compiling to every packaging that survives harness churn.

The strongest case AGAINST: DEMAND.md — willingness-to-pay "High for the
execution layer, ~Zero for the catalog layer"; "nobody is asking to buy a
prompt catalog"; platform absorption underway (first-party /security-review,
skills, workflows). Static prompt text is the commodity layer, and the paste
model structurally blinds the product to its own value delivery.

The 10x version is already half-built in four disconnected places: the
GitHub-Action runner (one example file), report diffing over time (vitals +
the universal dated re-run rule), brief evals (template/evals/run.py exists
for downstream products, never pointed at the briefs themselves), and team
rebasing (GOAL_PROMPTS_BASE). The composition — **a runner that executes
versioned, eval-tested briefs on a schedule and renders repo-health trends
from the diff grammar, with the free catalog as its acquisition engine** — is
the product the evidence supports.

## 8 · Ranked action plan

1. **Take the R62 decision.** Rule on the execution wedge explicitly, in
   DECISIONS.md. Everything else sequences behind this.
2. **Flip on measurement + ship the three external unlocks** (raw-fetch
   counting per docs/usage-metrics.md, npm publish, launch/Discussions).
   Hours of work; currently gating every other prioritization.
3. **Fix the P0/P1 UX plumbing** (mobile nav, styled report pages, full-text
   search, footer-orphan surfaces, playbook chip wall, nav consistency) —
   all inside the existing design direction.
4. **Build brief-efficacy evals** (seeded-defect fixtures + expected-findings
   assertions; publish pass rates on /quality). Converts the quality claim
   from shape to truth; answers the ADR-12 failure class.
5. **Pay down the architecture quadruplication** (shared search module, linked
   site.css, shared chrome, detail-page JS gate, conductor-cap chunking).
6. **Commit to the diff loop as the retention spine** (generalize
   HEALTH.md/vitals to every report re-run).
7. **Prune: channels, playbooks, overlap clusters; enforce or supersede ADR-9**
   (teams/partners down to a contact line until adoption exists).
8. **Close the trust orphans** (SECURITY.md, provenance stamps on copied
   prompts, consumer-side report-judgment guidance, gp-aid privacy page).
