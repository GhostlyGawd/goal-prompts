# ROADMAP.md — Unified Roadmap Synthesis

**Date: 2026-07-09** · produced by brief 28 · Roadmap Synthesis, read-only over the audit
reports at the repo root. First run — no previous `ROADMAP.md` existed.

**How to read this.** Every item traces to a source report; nothing new is smuggled in.
Each item carries a tag:
**`ship`** — buildable in this repo now · **`test`** — an A/B-style hypothesis needing
traffic (only its instrumentation should be built) · **`external`** — needs maintainer
accounts, credentials, assets, or decisions (cannot be built here) · **`done`** — already
shipped per FIXLOG/source. No item proposes fabricating proof or metrics.

---

## 1 · Sources

**Fresh (today, 2026-07-09 — the Growth playbook run):**
FUNNEL.md · COMPETITIVE.md · REVENUE.md · AI-IDEAS.md · SEO.md · CRO.md (re-run) ·
RETENTION.md (re-run) · PROOF.md (re-run) · ACTIVATION.md (re-run) · FORMS.md ·
CHECKOUT.md (**null report** — no payment surface exists; correct, no items).

**Older, largely reconciled** (dispositions in FIXLOG.md, PRs #19–#24, and each report's
own ledger): BUGS.md, SECURITY-AUDIT.md, IMPROVEMENTS.md, DX.md, CREDIBILITY.md,
COMPREHENSION.md, DEMAND.md, BRAND.md, HIERARCHY.md, COLOR.md, LAYOUT.md, TYPOGRAPHY.md,
STATES.md, SHOWCASE.md. Fully closed: BUGS, SECURITY-AUDIT, COMPREHENSION, LAYOUT,
TYPOGRAPHY. The open remainder from the rest is carried into the backlog below (§2,
items R59–R66); everything else in them is `done`.

**Missing reports that would most change this roadmap:**
- **A11Y.md (brief 86, Keyboard & Screen-Reader Flow)** — FORMS FV3 found that *every
  error message on the site is unannounced to screen readers*; a dedicated pass would
  likely widen that finding. **Run this next.**
- **PERF.md** — SEO-2 identifies the 572 KB homepage as the only Core Web Vitals
  liability; a perf audit would size R29's payoff before that M-effort change.
- **Fresh COLOR/TYPO re-audit** — FIXLOG itself notes the existing COLOR findings
  (C6–C8) measure a pre-redesign palette that no longer ships; re-audit before acting.
- TESTING.md / DEPS.md — lower urgency: `scripts/check` + 65 linter tests + three Node
  suites already gate the build; the repo is zero-runtime-dependency by design.

---

## 2 · Unified backlog

Impact/effort are recalibrated on one scale across all reports (H/M/L, S/M/L).
`where` cites the files a ship item touches.

### Theme A — Observability (see the funnel at all)

| id | item | tag | sources | impact | effort | deps | where |
|---|---|---|---|---|---|---|---|
| R01 | Un-fake `mark_run`: stop auto-marking on copy; the hint's explicit "✓ mark it run" becomes the honest signal | ship | FUNNEL §2/§4.2 · ACTIVATION AN1 · RETENTION R9 · REVENUE §3.3 | H | S | none — unlocks R08, R56, R57 | template.html |
| R02 | Detail-page analytics + retention parity: insights script + copy events on all 176 `/b`/`/p` pages, slim welcome-back/nudge strip | ship | FUNNEL §4.1 · RETENTION R7 · REVENUE §4.4 | H | M | none | build.py, js/gp-detail.js |
| R03 | Route all events through `track()` (aid/fsw on nudge/mark/reminder events); `?src=reminder` + `reminder_return`; `pwa_installed`; resolve the contradictory R5 comments | ship | RETENTION R9/§4 | M-H | S | none | template.html, build.py (SERVICE_WORKER) |
| R04 | Funnel-position events: `catalog_reached`, `quickview_open`, `examples_viewed` | ship | FUNNEL §4.5 | M | S | none | template.html |
| R05 | Turn on `/raw/*` + `commands.tar.gz` fetch counting (usage-metrics Option 1, Vercel log filter — zero code); correct the stale "no analytics" line in the doc when touched | **external** (Vercel dashboard) + ship (doc line) | FUNNEL §4.3–4 · REVENUE §4.4 · RETENTION §4 · PROOF §4 · COMPETITIVE §4 | H | S | R06 cleans the metric | docs/usage-metrics.md (doc fix only) |
| R06 | `X-Robots-Tag: noindex` for `/raw/` + `/prompts/` (SEO-8) — dedupes crawl surface and de-pollutes R05's metric | ship | SEO-8 | M | S | none | vercel.json |

### Theme B — The handoff (close the silent stalls)

| id | item | tag | sources | impact | effort | deps | where |
|---|---|---|---|---|---|---|---|
| R07 | Plugin two-command trap: copy/show **both** commands as numbered steps on landing + `/b` install ways | ship | FUNNEL §1 · CRO NF3 · ACTIVATION path E | H | S | none | template.html, build.py |
| R08 | Wire `showCopyHint` into the catalog card's own Copy button — the last unguided handoff | ship | ACTIVATION AN1 | H | S | pair with R01 | template.html |
| R09 | Quickstart pill false-success: route through `copyText()`, hint only on success | ship | ACTIVATION AN2 | M-H | S | none | template.html |
| R10 | Conductor hint variant ("runs N briefs, writes X.md, Y.md…") on all four conductor copy affordances | ship | ACTIVATION AN4 · FUNNEL path C | M | S | none | template.html |
| R11 | Detail-page hint gets the Studio tee-up (parity with landing hint) | ship | ACTIVATION AN6 | M-L | S | none | js/gp-detail.js |
| R12 | Mobile copy bridge: on coarse-pointer, post-copy toast offers the `/raw/<id>.md` URL instead | ship | FUNNEL §1/§3 | M-H | S | none | template.html |
| R13 | `copy failed` on cards degrades to an "open raw ↗" link (pattern exists in gp-detail.js) | ship | FUNNEL §1c · ACTIVATION AN8 | L | S | none | template.html |
| R14 | "what happens next →" link in the post-copy toast (run-replay anchor / `/examples/`) | ship | FUNNEL §1 · ACTIVATION AN7 | M | S | none | template.html |
| R15 | Name a first command in plugin/marketplace descriptions ("start with `/goal:audit-triage`") | ship | ACTIVATION AN5 | M | S | none | build.py (plugin generator) |
| R16 | Pick the canonical "New here?" door (solo brief vs Day-1) and make the other the teed-up step 2 | ship (needs one maintainer call) | ACTIVATION AN3 | M | S | decision | template.html |
| R17 | One line for the no-agent visitor: "New to coding agents? Start with Claude Code →" | ship | FUNNEL silent stall 3 | L-M | S | none | template.html |
| R18 | Studio demo button gets primary styling when zero reports are loaded | ship | FUNNEL §1 Studio | L | S | none | studio.html |

### Theme C — Trust & honesty (protect the brand's one asset)

| id | item | tag | sources | impact | effort | deps | where |
|---|---|---|---|---|---|---|---|
| R19 | Offer/risk-reversal micro-line ("Free · no signup · read-only — ends by asking · local") + generic "see real sample reports ↗" fallback on all 176 detail pages | ship | CRO NF2 · PROOF NF6 | H | S | none | build.py |
| R20 | Rescope the "**every** brief is dogfooded" claim to the true, still-strong statement | ship | PROOF NF1 | H | S | none | template.html |
| R21 | One-line analytics disclosure reconciling "nothing leaves your machine" with the Vercel beacon + `gp-aid` | ship | PROOF NF2 · RETENTION R12 | M-H | S | none | template.html, studio.html, vitals.html, README.md |
| R22 | Date-gate merchandising `window` chips (kill "January drop" in July); back "Most popular" with real data or soften to "Start here" | ship | CRO NF4 | M | S | none | build.py, playbooks.json |
| R23 | Repoint the XSS evidence card at BUGS.md finding 2 (verifiable) instead of the squashed release commit | ship | PROOF NF4 | M | S | none | template.html |
| R24 | MCP `npx -y` line gets the inspect-the-source reassurance (mirror the curl line's treatment) | ship | PROOF NF5 | M | S | none | template.html, build.py |
| R25 | Hero dogfood pointer where rivals put star counts ("run against this repo's own code — read the reports →") + dormant hero star-badge slot (≥ threshold) | ship | PROOF NF3 (placement) / NF7 · COMPETITIVE §3.1 | M-H | S | none | template.html, build.py |
| R26 | Split the 34-word triple-em-dash hero sub | ship | CRO NF6 | L | S | none | template.html |
| R27 | Third `/examples/` section linking today's growth reports (fresh, self-critical dogfood) | ship | PROOF NF8 | L | S | none | examples/index.html |

### Theme D — SEO & reach (open the side doors)

| id | item | tag | sources | impact | effort | deps | where |
|---|---|---|---|---|---|---|---|
| R28 | **SEO-1**: static homepage catalog (build-emitted brief/playbook link list, JS-enhanced) — the biggest reach item | ship | SEO-1 · CRO NF8 | H | M | none | build.py, template.html |
| R29 | **SEO-2**: strip brief bodies from inline `DATA`; fetch `raw/<id>.md` at copy time; keep offline via SW | ship | SEO-2 | M-H | M | after R28; don't regress offline/one-request (CRO §2 keep-list) | build.py, template.html |
| R30 | SEO quick-win batch: OG/canonical on `/examples/` (SEO-4); canonicals on studio/vitals (SEO-5); sitemap `<lastmod>` (SEO-7); `og:site_name` + image dims + twitter tags (SEO-9) | ship | SEO-4/5/7/9 · CRO NF8 | M | S | none | examples/index.html, studio.html, vitals.html, build.py |
| R31 | Per-playbook OG cards (SEO-3) | ship | SEO-3 | M | M | none | scripts/og.py, build.py |
| R32 | JSON-LD (BreadcrumbList + content schema) on 176 detail pages (SEO-6); fix h2→h4 heading skip (SEO-10) | ship | SEO-6/10 | M | M | none | build.py |

### Theme E — The retention loop (close the Weekly Vitals circuit)

| id | item | tag | sources | impact | effort | deps | where |
|---|---|---|---|---|---|---|---|
| R33 | Link the orphaned Vitals Viewer: from the stale-Vitals nudge, SW notification URL, `b/29`, `p/vitals`, footer | ship | RETENTION R6 | H | S | none | template.html, build.py |
| R34 | Staleness-aware reminder: mirror `runs["29"]`/`remind.on` into IndexedDB so the SW checks before notifying | ship | RETENTION R8a | H | M | none | build.py (SERVICE_WORKER), template.html |
| R35 | PWA install offer when periodicSync is absent at opt-in; move the reminder offer to the moment a Vitals run is marked; swap the 🔔 for an in-set glyph | ship | RETENTION R8b/c | M | S-M | R34 first | template.html |
| R36 | Publish `/changelog` from CHANGELOG.md; version pointer in MCP tool footers and `install` outro | ship | RETENTION R10 | M | M | none | build.py, mcp/server.cjs, install |
| R37 | Surface `.github/run-brief.example.yml` at the moment of intent (post-Vitals hint, `b/29`, `p/vitals`) — "make it a standing appointment →" | ship | RETENTION R11 · COMPETITIVE §6.4 | M-H | S | none | template.html, build.py |

### Theme F — Forms & input integrity

| id | item | tag | sources | impact | effort | deps | where |
|---|---|---|---|---|---|---|---|
| R38 | Studio paste: infer/suffix duplicate names (kills silent data loss); don't hide the pastebox on failure; Enter-to-add; reword "file"→"paste" | ship | FORMS FV1/FV2 | H | S | none | studio.html |
| R39 | `role="status"` on the three note elements; `aria-invalid` + `.is-error` on `rrin` | ship | FORMS FV3 | M | S | none | studio.html, vitals.html, template.html |
| R40 | Unify destructive-action gates on the two-step arm (ctxclear, Studio clear-all, Vitals clear, unsel, seqclear) | ship | FORMS FV4/FV7 | M | S | none | template.html, studio.html, vitals.html |
| R41 | Forms polish tier: Vitals dedupe + per-file remove (FV5); demo re-enable (FV6); ≥16px mobile inputs (FV8); GitHub 12-file cap note (FV9); quota-failure note (FV10); fuzzy zero-state (FV11) | ship | FORMS FV5/6/8–11 | L-M | S | none | vitals.html, studio.html, template.html, js/catalog-core.js |

### Theme G — Competitive table stakes & AI-shaped features

| id | item | tag | sources | impact | effort | deps | where |
|---|---|---|---|---|---|---|---|
| R42 | Emit a parallel skills tree (`SKILL.md` format) from the build | ship | COMPETITIVE §3.2 | M-H | M | none | build.py |
| R43 | Per-brief install: `BRIEF=NN sh install` flag and/or per-brief download on `/b/<id>` | ship | COMPETITIVE §3.3 | M | S-M | none | install, build.py |
| R44 | Make the Cursor claim true (one `.cursor` emitter in build) **or** narrow the meta copy — one target, not five | ship (either branch buildable) | COMPETITIVE §3.4/§9 | M | M | decision: emit vs narrow | build.py or template.html |
| R45 | On-site contribution ask ("add a brief →" in footer/catalog; linter is the moderation story) | ship | COMPETITIVE §3.5 | M | S | pairs with R46 | template.html |
| R46 | **Brief Forge**: authoring meta-prompt (skeleton + linter rules + exemplars + iterate-until-green loop), linked from CONTRIBUTING/README | ship | AI-IDEAS 1 · COMPETITIVE §3.5 · REVENUE §2 (Teams production line) | H | S | none | docs/, CONTRIBUTING.md, README.md |
| R47 | Semantic-linter CI pass (advisory PR comment) shipped as an example workflow; activation needs the maintainer's API key | ship (file) + external (key) | AI-IDEAS 2 | M-H | S | key in Actions | .github/ |
| R48 | Studio "Copy Synthesis prompt" — `buildSynthesis()` sibling of `buildFixer` + selbar button (brief 28's method, targeted) | ship | AI-IDEAS 3 · COMPETITIVE §6.2 | M | S | none | studio.html |
| R49 | "Have your agent fill this in" copy-link on the Operator-context box | ship | AI-IDEAS 4 | M | S | none | template.html |
| R50 | Own "the audit loop" + publish the quality bar: lead positioning with brief → report → Studio → Fixer → FIXLOG; a "why these briefs don't rot" page (linter rules, CI gate, 4k cap, ask-first) | ship | COMPETITIVE §10 bets 1–2 · §6.1 | M-H | M | none | template.html, build.py (new page) |
| R51 | Offline-generated search alias table, tuned by `search_zero` misses | ship (Later) | AI-IDEAS 5 | M-L | M | accumulate `search_zero` data first (R02/R04); parity guard in scripts/mcp-smoke.cjs | js/catalog-core.js, mcp/server.cjs, new script |

### Theme H — Revenue rails (build now, sell later)

| id | item | tag | sources | impact | effort | deps | where |
|---|---|---|---|---|---|---|---|
| R52 | Unify the two partner CTAs on one working destination + add a private email channel | ship (needs the email from maintainer) | CRO NF5 · REVENUE §4.1–2 | M | S | maintainer supplies address; note `/p/` CTA targets Discussions, which isn't enabled (→ R60) | template.html, build.py |
| R53 | `.github/FUNDING.yml` + footer Sponsors link | **external** (GitHub Sponsors profile must exist first) | REVENUE §4.5/§5 | M | S | maintainer account setup | .github/FUNDING.yml once enabled |
| R54 | "Want this set up for your org? →" pointer lines in README teams section + collab template page | ship | REVENUE §3.2 | M | S | none | README.md, build.py |
| R55 | `/teams` offer page + `/partners` rate-card page (formats, specs, "audience numbers on request") | ship (pages) + **external** (pricing/offer decisions; real numbers from R05) | REVENUE §5 · COMPETITIVE §10 bet 3 | M-H | M | R05 for numbers; maintainer pricing call | build.py, template.html |
| R56 | Post-activation backer nudge (once, dismissible, after a real ≥5-run milestone) | ship (Later) | REVENUE §3.3 | M | S | **hard-gated on R01** (else it fires on copies) + R53 | template.html |

### Tests (traffic hypotheses — build only instrumentation now)

| id | item | tag | sources | impact | effort | deps | where |
|---|---|---|---|---|---|---|---|
| R57 | Promote the hero quickstart pill to a peer of the primary CTA | **test** | CRO NF1 · FUNNEL §1 (conflict ruled §4 below) | M-H | S | R01/R02/R04 baseline; measure `copy_prompt src:hero` vs catalog copies | template.html |
| R58 | Collapse the six-chooser stack (fold picker into repo-recommend fallback; move "aim the briefs" below toolbar) | **test** | FUNNEL §1 Choose · CRO NF7 | M | M | watch `picker_plan`/`repo_recommend` events first | template.html |

### Carried over from the older reports (the open remainder)

| id | item | tag | sources | impact | effort | deps | where |
|---|---|---|---|---|---|---|---|
| R59 | npm publish + MCP-registry listing (package publish-ready; workflow ships) | **external** (NPM_TOKEN + release) | IMPROVEMENTS 11 · CREDIBILITY 3 · PROOF §4 | H | S (maintainer) | — | — |
| R60 | The CREDIBILITY decisions: enable Discussions, confirm star threshold (25), quotes real-or-illustrative, a launch ("Show HN") to earn first stars | **external** (maintainer decisions/accounts) | CREDIBILITY · PROOF NF3 (earning) · COMPETITIVE §1 | H | — | R60 unblocks R52's Discussions link and wakes R25's badge | — |
| R61 | Real 10–15s screen recording of a brief run (MP4/WebM + poster) | **external** (capture tooling; honest walk-through already ships) | SHOWCASE F1 · CREDIBILITY 1 | M | — | — | — |
| R62 | DEMAND's strategic proceed/pivot/drop call on the execution-wedge opportunity | **external** (founder decision) | DEMAND | — | — | informed by R05 data + COMPETITIVE/REVENUE | — |
| R63 | Card meta row: collapse 7–8 controls behind one "more" affordance | ship (Later; design judgment) | HIERARCHY F4 | M | M | consider alongside R58's test | template.html |
| R64 | One shared severity ramp; categorical-hue distinction; family not signaled by color alone | ship (Later — **re-audit first**; findings are pre-redesign per FIXLOG) | COLOR C6–C8 · FIXLOG follow-up | M | M | fresh color audit | build.py (TOKENS_CSS), template.html |
| R65 | Name the motion tokens (`--dur-*`/`--ease*`) — additive only | ship (Later) | STATES §4 | L | S | none | build.py (TOKENS_CSS) |
| R66 | `j/k` keyboard navigation | ship (Later) | DX (deferred) · IMPROVEMENTS qw4 | L | S | none | template.html |

### Already done (verified — listed so nothing looks lost)

BUGS 1–5, SECURITY 1–4 (all closed by 0.4–0.8) · COMPREHENSION F1–F5 · LAYOUT L1–L6 ·
TYPOGRAPHY T1–T5 · STATES S1–S7 · HIERARCHY F1–F3/F5–F7 · COLOR C1–C5/C9 · BRAND B1–B5,
and **B6** (the Unicode icon set is now blessed and documented in CLAUDE.md — the one
residual, the off-set 🔔 glyph, is folded into R35) · SHOWCASE F2–F7 (F1's honest
walk-through shipped; the real recording is R61) · RETENTION R1–R5 · ACTIVATION A1–A5
(A1's catalog-card gap re-opened as R08) · prior CRO F1–F8 · prior PROOF F1/F3–F6 ·
IMPROVEMENTS 1–16 except the publish itself (R59) · DX 1–4 · og.png regeneration + drift
guard · CHECKOUT: null by design — nothing to do until a payment path exists (R53/R55).

---

## 3 · Themes — root causes worth one structural fix

1. **The funnel's central transition is invisible *and* falsified.** One root cause —
   copy-time auto-marking plus zero measurement of the copy→run handoff — underlies
   FUNNEL §2, RETENTION R9, ACTIVATION AN1's mark-run entanglement, and REVENUE's gated
   backer nudge. One structural fix: **R01 + R02 + R03 + R05** make copy→confirmed-run
   the product's core conversion number. Nearly everything tagged `test` or revenue-
   related is downstream of this.
2. **The retention/trust machinery guards the front door while traffic moved to the
   side doors.** SEO.md proves `/b`/`/p` are the best-indexed entries; CRO NF2, PROOF
   NF6, RETENTION R7, ACTIVATION AN6 all describe the same asymmetry. One structural
   fix: a **detail-page parity pass in `build.py` + `gp-detail.js`** (R02 + R19 + R11 +
   R24) — one template edit fixes 176 pages at a time.
3. **Guidance shipped everywhere except where the finding pointed.** The copy-hint
   exists and is good; it's missing precisely on the highest-traffic paths (card Copy,
   conductors, plugin step 2). R07–R10 + R15 are one component reused, not new design.
4. **Honesty drift under growth.** The site's moat is "evidence, not vibes," and growth
   introduced small overclaims: "every brief" (R20), "January drop" in July (R22), the
   undisclosed analytics id (R21), the unfalsifiable commit citation (R23). Each is a
   one-line fix; together they are brand maintenance, the cheapest high-impact batch here.
5. **Proof exists; placement and third-party corroboration don't.** First-party proof is
   excellent and buried (R25, R27); third-party proof is structurally blocked on four
   maintainer decisions (R59, R60, R61) that no amount of in-repo work substitutes for.
6. **The revenue system is inventory without a cash register.** Sponsorship rendering,
   Teams self-hosting, and standing audits all exist as features; none has a transaction
   path or an audience number. Rails (R52–R55) are cheap; selling waits on R05's numbers.

---

## 4 · Conflicts, ruled

- **Auto-mark on copy:** RETENTION lists it under "what already retains — keep it";
  FUNNEL calls it the funnel's central falsification. **Ruled with FUNNEL:** measurement
  integrity wins — R01 removes the auto-mark, and R08's hint button (already the honest
  pattern on detail pages) keeps the retention fuel line lit without faking it.
- **Quickstart pill promotion:** FUNNEL says ship (S); CRO says A/B (it competes with the
  catalog tour). **Ruled with CRO:** tagged `test` (R57) — instrumentation already exists.
- **Chooser-stack collapse:** FUNNEL proposes the fix; CRO warns the assists earn their
  keep for some segments. **Ruled with CRO:** tagged `test` (R58).
- **Homepage weight:** FUNNEL calls the inline blob "acceptable"; SEO-2 calls it the CWV
  liability. **Ruled: sequence, don't choose** — R28's static cards first (pure win),
  then R29's body-stripping with the offline story preserved via the service worker.

---

## 5 · Three milestones

### Now (1–2 weeks) — *see the funnel, close the silent stalls, patch the honesty drift*
Nothing here needs traffic or taste; it's the instrumentation everything else reads,
plus every S-effort stall and overclaim fix. Risk-reduction (trust, data loss) is
interleaved with growth (SEO quick wins, handoff fixes) on purpose.

**Ship:** R01, R02, R03, R04, R06 · R07, R08, R09, R10, R11, R12, R13, R14, R15, R17,
R18 · R19, R20, R21, R22, R23, R24, R25, R26, R27 · R30 · R33, R37 · R38, R39, R40 · R52.
**External — flag to maintainer now (they gate later milestones):** R05 (flip on Vercel
log counting), R53 (Sponsors profile), R59 (npm publish), R60 (Discussions / threshold /
quotes / launch).

### Next (a month) — *spend the visibility: reach, the retention loop, differentiation*
With the funnel observable, open the side doors to crawlers, finish the Weekly Vitals
circuit end-to-end, ship the differentiation bets that need no traffic, and run the two
experiments against the new baseline.

**Ship:** R16 · R28 → R29 · R31, R32 · R34, R35, R36 · R41 · R42, R43, R44, R45, R46,
R47, R48, R49, R50 · R54.
**Test:** R57, R58 (against Now's instrumentation).

### Later — *traffic- and decision-dependent: revenue offers, deferred design judgment*
Everything here is deliberately blocked on data (R05's numbers, `search_zero` volume),
maintainer decisions (pricing, DEMAND), or a fresh audit — starting it earlier would
mean selling against no numbers or restyling against stale findings.

**Ship:** R51 (after search data) · R55 (pages; offers after R05 + pricing call) · R56
(after R01 + R53) · R63, R64 (after a fresh color audit), R65, R66.
**External:** R61 (recording), R62 (DEMAND call), and the ongoing earning half of R60.

---

## 6 · Merge log (deduplications — nothing lost)

- **Copy≠run / mark-run integrity** ← FUNNEL §2 + §4.2, RETENTION R9, ACTIVATION AN1
  (mark-state branch), REVENUE §3.3 gating → **R01** (+R03).
- **Detail pages are dark/cold** ← FUNNEL §4.1, RETENTION R7, REVENUE §4.4 → **R02**.
- **Raw-fetch counting** ← FUNNEL §4.3–4, REVENUE §4.4, RETENTION §4, PROOF §4,
  COMPETITIVE §4 (cursor.directory transparency pattern) → **R05**.
- **Plugin second-command trap** ← FUNNEL §1 activation row, CRO NF3, ACTIVATION path E →
  **R07**.
- **Detail-page trust line + evidence link** ← CRO NF2 + PROOF NF6 (same `build.py`
  pass) → **R19**.
- **Analytics-vs-promise disclosure** ← PROOF NF2 + RETENTION R12 → **R21**.
- **Partner channel** ← CRO NF5 + REVENUE §4.1–2 → **R52**; the `/p/` Discussions
  dead-end also feeds R60.
- **Proof where star counts sit** ← PROOF NF3 (placement) + NF7 + COMPETITIVE §3.1 →
  **R25**; the earning half split out as **R60** (external).
- **Post-copy "what happens next"** ← FUNNEL §1 + ACTIVATION AN7 (AN7 explicitly
  endorses FUNNEL's fix) → **R14**; copy-failure fallback ← FUNNEL §1c + AN8 → **R13**.
- **Quickstart pill** ← FUNNEL entry-hero + CRO NF1 → **R57** (test; conflict ruled §4).
- **Chooser overload** ← FUNNEL Choose row + CRO NF7 → **R58** (test).
- **Standing-audit surfacing** ← RETENTION R11 + COMPETITIVE §6.4 → **R37**; its
  productization ← COMPETITIVE bet 3 + REVENUE §5 → **R55**.
- **Contribution path** ← COMPETITIVE §3.5 + AI-IDEAS 1 (Forge is the enabling half) →
  **R45 + R46**.
- **SEO-8's noindex** double-counted as metric hygiene for R05 → single item **R06**.
- **npm publish** ← IMPROVEMENTS 11 + CREDIBILITY 3 + PROOF §4 (honest downloads
  number) → **R59**.
- **Product-seen-working** ← SHOWCASE F1 + CREDIBILITY 1: the honest walk-through is
  `done`; only the real recording remains → **R61**.
- **BRAND B6** closed by CLAUDE.md's documented icon set; its 🔔 residual (also
  RETENTION R8c's aside) folded into **R35**.
- **CHECKOUT.md** merged as a null: its absence-of-payment finding is *by design* per
  REVENUE §1; the only successors are R53/R55.

---

*Report only — synthesis, no code changed. Should I adjust the sequence — e.g. pull any
of the Next differentiation bets (skills output, Brief Forge, SEO-1) into Now, push the
forms batch back, or reorder the external asks to the maintainer?*
