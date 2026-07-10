# Conversion Rate Optimization — re-run

**Date:** 2026-07-09 · read-only pass over `template.html`, `build.py` (detail-page
builders), `b/`, `p/`, `examples/`, `studio.html`, `README.md`, `playbooks.json`.
Companion reports from today's run: FUNNEL.md (structure), SEO.md (discoverability),
REVENUE.md (monetization) — cross-referenced, not duplicated.

## What changed since the last run (~4 months ago)

**All eight findings from the previous CRO.md shipped, and they held up.** Verified
in current source:

- **F1** hero offer — "free & open · no signup · nothing leaves your machine" is the
  hero micro-line (`template.html:502`). ✔
- **F2** default way-in — "01 · COPY" carries a "Start here" badge, primary styling,
  and its own primary CTA (`:650-655`). ✔
- **F3** meta/OG counts — injected from source as `__N_BRIEFS__`/`__N_PLAYBOOKS__`
  (`:7-9`, `build.py:1286`). ✔
- **F4** JSON-LD + canonical — `SoftwareApplication` schema with `price: 0` and
  `<link rel="canonical">` (`:16`, `:19`). ✔
- **F5** partner CTA — "Partner with us →" exists (`:741`). ✔ (but see NF5)
- **F6** unified start CTAs — nav "Get started" and hero primary both → `#catalog`
  (`:485`, `:499`). ✔
- **F7** hero quickstart — shipped as a one-tap "Copy your first brief" pill with
  `src:hero` analytics (`:503`, JS `:1679-1692`). ✔ (but see NF1)
- **F8** jargon — "brief" glossed inline in the hero sub (`:497`), "MCP (Model
  Context Protocol)" spelled out (`:667`), "conductor" gets a tooltip (`:640`). ✔

**The product underneath grew a whole new perimeter:** 141 briefs (was 129), 35
playbooks, 141 static `/b/<id>` pages + 35 `/p/<key>` pages (now the best-indexed
entry points per SEO.md), an `/examples/` proof gallery, a run-replay and
before/after proof section, plugin distribution as the README's "primary path,"
MCP prompts, a 3-question picker, repo-recommend, and a merchandised playbook
storefront (badges, seasonal windows, collab/sponsored types). This re-run's theme:
**the landing page now converts well; the leaks moved to the side doors, the
install path's second step, and a few trust details in the merchandising.**

---

## 1 · Funnel map

| # | Surface | The one action it must drive | Who lands / their question | Biggest leak |
|---|---|---|---|---|
| 1 | **Landing hero** (`template.html:490-515`) | One tap into value: browse or quickstart-copy | Cold. *"What is this, is it for me, what does trying cost?"* | The best newcomer action (quickstart pill) is styled as a footnote below two bigger buttons (NF1). |
| 2 | **Side doors** — `/b/<id>` (141), `/p/<key>` (35) | Tap "Copy this prompt" / "Copy the conductor" | **Cold, from search/shared links.** *"Can I trust pasting this? What does it cost?"* | The offer + risk-reversal that carry the landing page (free, no signup, read-only, local) never reach these pages (NF2). |
| 3 | **Catalog** (`:577-622`) | Tap Copy on a brief — the core conversion | Warm. *"Which one?"* | Six chooser mechanisms stacked before the list; assists compete with the action (NF7, structure covered in FUNNEL.md). |
| 4 | **Ways in / install** (`:646-672`) | Complete an install (the retention-grade conversion) | Ready. *"How do I make this permanent?"* | The plugin path's **required second command exists nowhere on the site** — a copied step 1 dead-ends (NF3). |
| 5 | **Proof + Examples** (`:675-723`, `/examples/`) | Believe → return to catalog | Skeptical. *"Is this real?"* | Strong (real reports, real commits, honest "walk-through, not a screen capture" label). Leak is off-page: examples unfurl with no OG card (SEO-4). |
| 6 | **Partner band** (`:726-745`) | A sponsor inquiry — the revenue conversion | Warm prospect. *"How do I start, discreetly?"* | Only channel is a **public** GitHub issue; the two partner CTAs point at different destinations (NF5, detailed in REVENUE.md §4). |
| 7 | **Activation** (off-site, post-copy) | Paste → report lands | — | Out of scope; the post-copy toast (`showCopyHint`, `:895-907`) bridges it well. ACTIVATION.md's stage. |

---

## 2 · Findings

### NF1 — The one-tap conversion is dressed as a footnote *(lens 3: the one action / lens 1: above the fold)* — **lift M-H · effort S · TEST**
- **Location:** hero quickstart pill `template.html:503` — rendered `hidden` until JS
  (`:1684`), styled 13px with a *dashed* border (`:88`), placed third under two
  full-weight buttons ("Browse the catalog", "See how it works", `:499-500`).
- **First-time experience:** the visitor's cheapest possible yes — one tap puts a
  runnable brief on the clipboard — reads as an afterthought. Visual hierarchy says
  "browse 141 things"; value hierarchy says "just take this one."
- **Fix:** promote the pill to a peer of the primary CTA (solid border, same row or
  directly under it), or make it the primary and demote "Browse the catalog."
  FUNNEL.md flags the same element structurally; the persuasion risk cuts the other
  way too — the catalog *is* the product tour — so **A/B it** using the existing
  `src:hero` copy event vs `copy_prompt` from the catalog.

### NF2 — 176 side-door pages never state the offer or the risk-reversal *(lens 4: trust / lens 7: offer)* — **lift M-H · effort S · SHIP**
- **Location:** the `/b/<id>` hero CTA block (`build.py:823-827` → e.g. `b/47.html`)
  and `/p/<key>` conductor block. `grep -c "free" b/47.html` → **0**; "no signup"
  and "nothing leaves your machine" appear nowhere; "read-only" appears only if the
  brief body happens to say it. The landing page's trust triad (`:543-545`) doesn't
  exist here.
- **First-time experience:** SEO.md shows these are the pages a cold searcher
  actually lands on. They see a big "Copy this prompt" button and a wall of prompt
  text — with no answer to *"is this free?"* and *"is it safe to paste this into
  the agent that can edit my code?"* The exact objections the homepage pre-empts
  are unanswered at the exact CTA that matters.
- **Fix:** one generated micro-line under the detail-hero CTA row in `build.py`:
  "Free & open · no signup · read-only — it ends by asking · nothing leaves your
  machine." One template edit fixes all 176 pages.

### NF3 — The "primary path" install dead-ends after step 1 *(lens 5: friction / lens 4: trust)* — **lift H · effort S · SHIP**
- **Location:** landing "02 · INSTALL" card copies `/plugin marketplace add
  GhostlyGawd/goal-prompts` (`:660`); the **required** second command
  `/plugin install goal@goal-prompts` (README.md:29) appears **nowhere in
  template.html or any `b/` page** (`grep -c "plugin install"` → 0). Its only trace
  is 12px fine print: "then install **goal** from the marketplace" (`:661`).
- **First-time experience:** a ready visitor copies the one visible command, pastes
  it, gets a marketplace added — and **no commands appear**. Without step 2 the
  honest conclusion is "it's broken." A failed first experience on the path README
  calls primary is the most expensive kind of leak: it converts, then refunds
  itself with interest.
- **Fix:** render both commands as numbered copyable steps (1 · add marketplace,
  2 · install goal) on the landing card and the `b/` "02 · INSTALL" way
  (`build.py:908-911`). FUNNEL.md counts the steps; this is the persuasion cost.

### NF4 — Stale and unverifiable merchandising chips on an "evidence, not vibes" brand *(lens 4: trust)* — **lift L-M · effort S · SHIP (carefully)**
- **Location:** `/p/newyear` renders the chip **"January drop"** (`playbooks.json`
  `window`, rendered unconditionally at `build.py:994`) — it is **July**. `shipit`
  wears "Seasonal · Featured this season" permanently. Day-1's badge is **"Most
  popular"** (`playbooks.json`) on a site with 0 public stars and no visible usage
  numbers.
- **First-time visitor experience:** a January label in July signals an
  unmaintained site; an unverifiable superlative on a page whose own hero promises
  "evidence, not vibes" invites exactly the skepticism the proof section works so
  hard to defuse.
- **Fix:** date-gate `window` chips at build time (hide when expired) or drop the
  stale ones; either back "Most popular" with the real `copy_conductor` analytics
  ("most-copied playbook") or soften to "Start here." Cheap, and it protects the
  site's strongest asset — its honesty (the "example" partner card at `:739-740`
  and the "walk-through, not a screen capture" tag at `:680` set the standard).

### NF5 — The revenue conversion demands a public confession *(lens 5: friction / lens 6: objections)* — **lift M · effort S · SHIP**
- **Location:** "Partner with us →" → `github.com/.../issues/new?title=Partnership+inquiry`
  (`:741`); the `/p/` partner blocks point at GitHub *Discussions* instead
  (REVENUE.md §4.1).
- **First-time experience:** a sponsor's first move becomes a **public** post
  titled "Partnership inquiry," visible to competitors, before any conversation.
  Most will simply not.
- **Fix:** one private channel (email or form) as the primary contact on both
  surfaces, GitHub as secondary. REVENUE.md owns the full treatment; it is also a
  straight CRO fix.

### NF6 — The hero sub is one 34-word, triple-em-dash sentence *(lens 8: scannability)* — **lift L · effort S · SHIP**
- **Location:** `:497` — "Point it at your repo. Every brief — a ready-made,
  copy-paste prompt — runs the same four-phase audit and files **one
  evidence-backed report** you can act on — no more random, throwaway results."
- **First-time experience:** in the ten-second skim, three dashes force a re-read;
  the payoff clause ("no more random, throwaway results") arrives after the
  visitor has already skipped ahead.
- **Fix:** split: "Every brief is a ready-made, copy-paste prompt. It runs the
  same four-phase audit and files **one evidence-backed report** you can act on —
  not another wall of random, throwaway output."

### NF7 — Six assists stand between the headline and the goods *(lens 5: friction)* — **lift M · effort M · TEST**
- **Location:** between the `#catalog` H2 (`:579`) and the card list (`:621`):
  triage nudge (`:581`), 3-question picker (`:584`), repo-recommend (`:588`),
  the 21-row finder (`:597`), the 4-field "aim the briefs" box (`:600`), then
  search + 22 family chips + playbook chips (`:612-619`).
- **First-time experience:** each helper is individually good; stacked, the moment
  of action reads like a form. The finder's own "New here? Start with Day-1"
  starter is the best of the six — and it sits below three collapsed disclosures.
- **Fix (hypothesis):** collapse picker + repo-recommend into one "help me choose"
  disclosure and move "aim the briefs" below the toolbar; keep the Day-1 starter
  at the top. FUNNEL.md maps this structurally — **test**, don't blind-ship, since
  the assists exist because 141 choices genuinely need triage.

### NF8 — The click before the visit *(lens 9: findable & shareable)* — **defer to SEO.md**
The head is now in good shape (dynamic counts, canonical, JSON-LD with `price: 0`).
The remaining CTR-deciders are already specified in SEO.md and matter for
conversion: `/examples/` — the site's best proof asset — unfurls as a bare URL
(SEO-4); all 35 playbooks share one generic OG image (SEO-3); the homepage's 141
briefs are invisible to non-rendering crawlers (SEO-1). Not re-litigated here.

### What already converts — keep it
- **Hero offer line** (`:502`) and the trust triad (`:543-545`) — the previous
  run's top fixes, intact and load-bearing.
- **Dogfooding proof chain** (`:675-723`, `/examples/`): real reports → real
  commits, self-labeled honestly. Rare and persuasive; NF4 is about protecting it.
- **Post-copy toast** (`:895-907`): tells the visitor exactly what happens next
  and bridges to the Studio — the activation handoff is well-written.
- **Star-count honesty**: `__GH_STARS__` renders nothing below a threshold
  (`build.py:1300-1304`) instead of bragging "0 stars." Correct instinct.
- **Speed & weight discipline**: single-request page, preloaded fonts, no media.
  (SEO-2 notes the 507 KB inline JSON tradeoff; don't regress it further.)

---

## 3 · Top 5 lifts (ranked by leverage)

1. **NF3 — show the plugin install's second command. *Ship first.*** It is the only
   place on the site where a converting visitor follows instructions and gets a
   result that looks broken. One line of HTML on two templates; protects the path
   README calls primary.
2. **NF2 — offer + risk-reversal micro-line on all 176 detail pages.** One
   `build.py` edit puts the homepage's best-performing trust copy at the CTA the
   cold search traffic actually sees.
3. **NF4 — retire "January drop" / gate the merchandising chips.** Minutes of work;
   an expired seasonal label quietly poisons every other claim on the site.
4. **NF5 — a private partner channel.** The only funnel with money in it currently
   asks strangers to negotiate in public (with REVENUE.md's fuller fix).
5. **NF1 — weight the quickstart pill like the conversion it is** — behind an A/B
   against the existing `src:hero` event, since it competes with the catalog tour.

## 4 · Ship vs test

**Ship now — proven best practice, low risk:**
NF2 (detail-page offer line) · NF3 (two-step install) · NF4 (chip gating — keep
badges only where verifiable) · NF5 (private partner contact) · NF6 (hero sub
split).

**Test — could cut both ways:**
NF1 (promote the quickstart pill — may cannibalize catalog browsing, which is the
product tour; measure `copy_prompt src:hero` vs catalog copies) · NF7 (collapsing
the chooser stack — the assists earn their keep for some segments; watch
`repo_recommend` / picker events before removing anything).

**Handle with care:**
- Never add urgency or popularity claims that can't be backed by a number the site
  actually has — the brand *is* "evidence, not vibes" (NF4's flip side).
- The trust triad and detail-page "It ends by asking" copy carry the safety story;
  shorten nothing there to make room for offers.
- Any hero change must preserve the fast, media-light first paint; NF1's pill
  should also get a no-JS fallback (`hidden` today means no JS = no pill).

---

## Report only — which lifts do you want me to make?

Nothing was changed in this pass. The ship set (NF2, NF3, NF4, NF5, NF6) is small,
independent, and mostly single-template edits in `build.py` / `template.html`;
NF5 pairs naturally with REVENUE.md's quick wins and NF8 with SEO.md's. NF1 and
NF7 should run as experiments against the analytics events that already exist.
Tell me which findings to implement (any subset) and I'll make only those changes.
