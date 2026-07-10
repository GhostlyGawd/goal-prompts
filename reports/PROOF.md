# Social Proof & Credibility — re-run

**Date: 2026-07-09.** Read-only pass over the proof-carrying surfaces: landing
(`template.html` / built `index.html`), the 141 `/b/<id>` + 35 `/p/<key>` detail
pages (`build.py` builders), `/examples/`, `studio.html`, `README.md`, the
`install` script, `CREDIBILITY.md`, `metrics.json`, and the git history behind
every on-page citation. Companion reports from today's run: COMPETITIVE.md
(0-star reality vs 23k–50k-star rivals), CRO.md (persuasion mechanics — not
duplicated here), REVENUE.md (partner flow).

**Honesty note (unchanged house rule):** every recommendation below is *collect
real proof* or *place existing real proof better*. Nothing here suggests
fabricating a testimonial, a logo, or a number.

---

## What changed since the last PROOF.md

The previous report's fixes shipped, and most held up under re-inspection:

- **F1 (checksum reassurance at `curl | sh`) — SHIPPED, half.** The install line
  now reads "SHA-256 verified when your shell has a hash tool · read the script
  first" with a link to `/install` (`template.html:661`) — honest even about the
  no-hash-tool fallback, which matches the script's real behavior
  (`install:26-43`). **But the MCP `npx -y github:…` line (`:668`) never got its
  half** — see NF5.
- **F3 (unverifiable HN quotes) — RESOLVED beyond the ask.** The three anonymous
  quotes are gone entirely. In their place: three *linked, first-party evidence
  cards* (`template.html:522-526`) — the sample-report gallery, a real S2
  self-XSS finding with a commit link, and the FIXLOG. Strictly better than
  linking the quotes. (One residue: NF4.)
- **F4 (proof stranded at the bottom) — SHIPPED.** Proof now sits beside claims:
  the Problem section itself is evidence, the catalog lead links "See a real
  report one wrote →" (`:580`), and 20 brief detail pages carry "See a real
  report ↗" at the copy CTA (`build.py:825-827`).
- **F5 (no human) — SHIPPED.** Footer: "Built by @GhostlyGawd, an independent
  developer · using it? tell me how ↗" (`:758`, verified in built `index.html`).
- **F6 (partner band implies a partnership) — SHIPPED.** "example" pill +
  "No real partnership implied." (`:739-740`), plus a real "Partner with us →"
  CTA.
- **F2 (no third-party proof) — ARMED, still dark.** `metrics.json` holds the
  real count (still `{"stars": 0, "forks": 0}`); `build.py:1298-1304` renders a
  stargazers badge only at ≥25 stars. Nothing faked, nothing shown. The
  strategy is documented in `CREDIBILITY.md` — whose four maintainer decisions
  (star threshold, npm publish, quotes real-or-illustrative, enable Discussions)
  **are all still open**.

New proof assets that didn't exist last time: an animated **run walk-through**
honestly labeled "walk-through, not a screen capture" (`:679-690`), a **real
Report Studio screenshot** captured from the live tool (`img/studio.png`,
`scripts/studio-shot.cjs`, `:704-707`), a **finding → commit before/after**
whose commit I verified in git (`683dff5` matches the claim exactly, `:709-722`),
a **venture dogfood** wing in `/examples/` ending in a self-disconfirming
"pivot" verdict, and plugin distribution as the README's primary path.

The two structural gaps from last time are narrower but **still the story**:
(1) zero third-party evidence anyone else uses it, and (2) a few claims and
decision points where the proof isn't where the doubt is. Plus one new problem
the growth created: the flagship dogfood claim now **overclaims**.

---

## 1 · Proof inventory

| Signal | Where it lives | The claim it backs | How credible |
|---|---|---|---|
| **Dogfood evidence cards** (gallery link · S2 XSS finding + commit · FIXLOG link) | Problem section `template.html:522-526` | "Structure fixes inconsistency — and we prove it on ourselves" | **High** — every card links to an inspectable artifact |
| **Sample-report gallery** (Day-1 + Venture, 8 real reports) | `/examples/index.html`; linked from hero lead, catalog lead, 20 `/b/` pages | "This is the output you can expect" | **High** — real files, real findings, reproducible via the Day-1 conductor |
| **Venture verdict = "pivot," not "go"** | `examples/index.html:112,126` | "The method is honest, not a hype engine" | **High** — self-disconfirming proof, the rarest kind |
| **Run walk-through** | Proof section `:679-690` | "Here's what a run looks like" | **High** — labeled "walk-through, not a screen capture" twice; ends on a real finding that exists in BUGS.md |
| **Finding → commit before/after** | `:709-722` | "Findings become commits" | **High** — commit `683dff5` verified: message and diff match the page's claim |
| **Real Studio screenshot** | `:704-707` | "The Studio is a real tool" | **High** — captured from the live page by script, alt text describes real reports |
| **Read-only · ends by asking · local** guard cards | `:542-546` | "Safe for your code" | **High** — linter-enforced on every brief; verifiable in any brief's text |
| **Checksum-verified installer** + on-page note | `install:26-43`; note at `:661` | "Safe to `curl \| sh`" | **High** — now visible at the decision (was buried last run) |
| **"The exact prompt" transparency block** | every `/b/` page ("Nothing hidden — this is the whole brief, verbatim") | "You can read what you're about to paste" | **High** |
| **Maintainer identity** | footer `:758` | "A real person stands behind this" | **Med** — real handle, honest "independent developer"; no name/face/origin story yet |
| **Counts (141 briefs · 35 playbooks)** | hero micro `:502`, meta/OG, JSON-LD | Scope | **High** — build-injected from source, can't drift |
| **MIT / free / no signup / local** | hero micro `:502`, JSON-LD `:19`, footer `:759` | "No cost, no lock-in, no exfiltration" | **High** — but see NF2 for the one crack |
| **Armed star badge** | `build.py:1298-1304` + `metrics.json` | (adoption — once real) | **Hidden at 0 — honest**; placement will be footer-only when it wakes (NF7) |
| **"Every brief is dogfooded before it ships"** | evidence card `:523` | The flagship trust claim | **Overclaimed — see NF1** |

Pattern: first-party proof went from good to excellent — layered, linked, and
honestly labeled. Third-party proof is still **zero** (0 stars, no testimonials,
no named users, npm unpublished, Discussions off). The site compensates about as
well as honesty allows; the remaining fixes are precision (don't overclaim) and
placement (finish the decision-point coverage).

---

## 2 · Findings (lens · location · doubt · fix · effort)

Ranked by doubt removed at the moment of decision.

### NF1 — The flagship proof claim overclaims, and shrinks under scrutiny *(lens 7: freshness & honesty · lens 2: specific over generic)* — **HIGH · effort S**
- **Location:** evidence card `template.html:523` — "**Every brief** is
  dogfooded on this repo before it ships — the reports the briefs wrote sit at
  the repo root, in the open, linked as live samples **from their briefs**."
- **The check a skeptic runs:** 141 briefs; ~26 reports at the root; 20 of 141
  detail pages link a sample. No PERF.md, DEPS.md, A11Y.md… for the majority of
  the catalog. The site's best proof asset is fronted by its one falsifiable
  sentence — on a page whose whole stance is "evidence, not vibes," an
  overclaim costs double.
- **Fix (pick one):** (a) scope it honestly — "The Day-1, design, growth and
  venture playbooks have all been run against this repo — every report they
  wrote sits at the root, in the open"; or (b) make it true, and turn the gap
  into a linter rule later. Option (a) is a one-line edit and loses nothing: the
  true number (~26 real reports) is still more output-proof than any rival shows.

### NF2 — "Nothing leaves your machine" shares a page with an analytics beacon, and nothing reconciles them *(lens 8: transparency · lens 7: honesty)* — **MED-HIGH · effort S**
- **Location:** hero micro `:502` ("nothing leaves your machine") and Studio sub
  (`studio.html:214`, "no upload, no backend") vs `/_vercel/insights/script.js`
  loaded on landing, Studio, and Vitals (`template.html:24`,
  `studio.html:21`, `vitals.html:20`) plus a locally-generated anonymous cohort
  id attached to events (`template.html:874-882`). No privacy note anywhere on
  the site or README explains the boundary.
- **The doubt:** the claim is *true in spirit* — your code, reports, and setup
  never touch a server — but the exact visitor this site courts (a developer
  about to paste an agent prompt) is the one who opens devtools, sees a
  first-party analytics beacon with an `aid`, and re-reads the promise as
  marketing. Trust, once dented on the honesty axis, takes the dogfood proof
  down with it.
- **Fix:** one honest line where the claim is made or in the footer: "Your code,
  reports, and setup never leave your device. The site itself counts page views
  with cookie-free, anonymous analytics — no code or repo data is ever sent."
  Optionally link the analytics snippet in source. Cheap, and it converts a
  latent gotcha into a transparency signal.

### NF3 — Third-party proof is still zero, and the honest substitute isn't where a star count would sit *(lens 6: numbers that reassure · lens 3: proof at the decision)* — **MED-HIGH · effort S (placement) + external (earning)**
- **Location:** whole site — confirmed absence, unchanged from last run.
  `metrics.json` = 0 stars / 0 forks; badge armed but dark; no testimonials, no
  named users, no npm downloads (unpublished); COMPETITIVE.md: rivals lead with
  23k–50k stars.
- **The doubt:** "am I the first person to ever run one of these?" First-party
  proof shows it *works*; nothing shows it's *used*.
- **Fix (placement, now):** put the proof-of-output where rivals put the star
  count — one line in the hero region, e.g. under the micro-line: "run against
  this repo's own code — read the reports →" (COMPETITIVE.md recommends the
  same; today the first dogfood link is a scroll below the fold). **Fix
  (earning, maintainer):** the four open decisions in `CREDIBILITY.md` — enable
  Discussions, npm publish (creates an honest downloads number), confirm the
  star threshold, and a launch that could earn the first stars. All four have
  been pending since that plan was written.

### NF4 — The XSS evidence card cites a squashed release commit a checker can't actually verify *(lens 5: credibility of the source)* — **MED · effort S**
- **Location:** evidence card `:524` — "fixed the same release" links "fixed in
  0.4 ↗" to commit `d041b3f`. Verified in git: that commit is the *entire 0.4.0
  release* (hundreds of files). The fix is genuinely in there, but a visitor who
  clicks to check finds an unreviewably huge diff with no XSS mention in the
  message — the citation is real yet functionally unfalsifiable, which reads
  like hand-waving on the site's most security-flavored claim.
- **Fix:** point the link at the verifiable artifact instead: `/BUGS.md`
  (finding 2 states location, trigger, root cause, and "FIXED in 0.4 — built
  with `textContent`"), or keep both — "BUGS.md, finding 2 ↗ · shipped in 0.4".
  The before/after block lower down already models this correctly (its commit
  `683dff5` is small and exactly matches its claim).

### NF5 — The MCP `npx -y` line is still bare — the un-shipped half of old F1 *(lens 3: proof at the decision · lens 8: security)* — **MED · effort S**
- **Location:** Ways in, way 03 (`:668`): `claude mcp add goal-prompts -- npx -y
  github:GhostlyGawd/goal-prompts` — auto-executes code from a stranger's repo,
  shown with only a copy button; the sibling curl line got its reassurance,
  this one didn't. Same gap on the `/b/` pages' way-03 (raw URL — lower fear)
  and the plugin marketplace line (mitigated by Claude Code's own trust UI, but
  a "MIT · source on GitHub" nod costs nothing).
- **Fix:** mirror the install line's treatment: "runs the zero-dependency server
  straight from the public source — inspect `mcp/server.cjs` ↗" linking the
  GitHub path.

### NF6 — 121 of 141 detail pages ask for the paste with no proof in eyeshot *(lens 3: proof at the decision · lens 1: proof beside the claim)* — **MED · effort S**
- **Location:** `build.py:825-827` adds "See a real report ↗" to a brief's hero
  CTA only when `example:` front matter exists (20 briefs). The other 121 — the
  cold-search side doors per SEO.md — offer a "Copy this prompt" button with no
  evidence link near it; the footer "fine" line (`b/*.html`) carries MIT/free
  but sits at the very bottom. (CRO.md NF2 covers the missing *risk-reversal
  triad* on these pages; this finding is the missing *evidence* — fix them in
  the same `build.py` pass.)
- **Fix:** in the detail-hero builder, fall back to a generic
  "See real sample reports ↗ → /examples/" ghost link when no per-brief example
  exists, ideally alongside CRO NF2's one-line offer/guard micro-line.

### NF7 — When the star badge finally wakes, it wakes in the footer *(lens 3 · lens 6)* — **LOW · effort S (forward-looking)**
- **Location:** `build.py:1303-1304` injects `__GH_STARS__` into the footer
  buildnote (`template.html:758`) — the weakest placement on the page for the
  moment the project finally has a third-party number to show.
- **Fix:** when it crosses the threshold, render it in the hero micro-line
  (next to "free & open") as well as the footer. Zero cost today — the change
  can ship now and stays invisible until the number is real.

### NF8 — Today's eight growth reports are proof that isn't merchandised *(lens 1 · lens 7: freshness)* — **LOW · effort S**
- **Location:** FUNNEL.md, COMPETITIVE.md, REVENUE.md, AI-IDEAS.md, SEO.md,
  CRO.md, RETENTION.md (+ this file) sit at the root, dated today — fresh,
  self-critical dogfood including a competitive scan that openly records the
  0-star gap. `/examples/` still shows only Day-1 + Venture.
- **Fix:** add a third gallery section ("Growth · the whole funnel, audited")
  linking a few of them. Self-critical reports *are* the brand; freshness dates
  are visible in the files. (Also keeps `/examples/` from reading as a one-time
  stunt — its Day-1 reports are from 0.4.)

### What already earns trust — keep and protect
- **Linked, layered dogfood** — gallery → finding → commit → FIXLOG is a proof
  chain no rival shows (COMPETITIVE.md confirms).
- **Honest labeling under constraint** — "walk-through, not a screen capture,"
  the "example" partner pill, the checksum note admitting its fallback, the
  badge that refuses to show a zero. This discipline *is* the moat; NF1/NF2 are
  the two places it slipped.
- **The transparency block on every `/b/` page** — "nothing hidden, verbatim"
  is the right reassurance at the copy decision.
- **The "pivot" verdict** — still the single most trustworthy artifact on the
  site.

---

## 3 · Proof at the decision (what to place at each, in order)

1. **Hero CTA (`:498-503`):** keep the offer micro-line; add the one-line
   dogfood pointer ("run against this repo's own code — read the reports →")
   where a rival's star badge would sit. *(NF3)* Later: the star count joins it
   at ≥ threshold. *(NF7)*
2. **Catalog copy buttons (`:580`, cards):** already covered — sample-report
   link in the lead + per-card transparency. No change.
3. **`/b/<id>` "Copy this prompt" (141 pages):** generic sample-gallery link on
   the 121 pages lacking one *(NF6)*, plus CRO NF2's offer/guard micro-line.
4. **Install `curl | sh` (`:661`):** shipped last round — keep.
5. **MCP `npx -y` line (`:668`):** "runs from public source — inspect
   `mcp/server.cjs` ↗". *(NF5)*
6. **Studio drop zone (`studio.html:214`):** "no upload, no backend" is right;
   append the analytics-honesty clause or footer-link it. *(NF2)*
7. **Partner "Partner with us →" (`:741`):** example label shipped; REVENUE.md
   handles the channel (public issue → private option).

---

## 4 · Proof to earn (collect, never invent)

Unchanged in kind since last run — none has been collected yet, and
`CREDIBILITY.md`'s four maintainer decisions are still the bottleneck:

- **First stars** — a launch ("Show HN" with the dogfood/pivot story as the
  hook); the armed badge then turns itself on.
- **An honest downloads number** — publish the MCP server/installer to npm
  (workflow already exists at `.github/publish.example.yml`).
- **First attributable testimonials** — enable GitHub Discussions; the footer
  "using it? tell me how ↗" already points at Issues; publish only real, linked
  quotes.
- **A usage signal that keeps the local-first promise** — `docs/usage-metrics.md`
  already designs it (per-path `raw/*.md` fetch counts, no identifiers); fold
  monthly counts into `metrics.json` when adoption justifies it.
- **A fuller maintainer note** — the 1–2 sentence origin story CREDIBILITY.md
  asked for; still absent.

---

## Report only — which fixes do you want me to make?

Nothing was changed in this pass. The ship-now, fully honest set: **NF1**
(rescope the "every brief" claim — one line, protects the flagship proof),
**NF2** (one-line analytics disclosure), **NF4** (repoint the XSS citation at
BUGS.md), **NF5** (inspect-the-source note on the MCP line), **NF6 + NF7 +
NF8** (build.py sample-link fallback, hero badge slot, gallery section — all
small). **NF3's earning half** needs you: the four CREDIBILITY.md decisions
(Discussions, npm, threshold, launch). Tell me which subset to implement.
