# Conversion Rate Optimization

*The product's public surfaces audited against conversion best practice, through
the eyes of a first-time visitor who knows nothing about the product or the
niche. Read-only pass over `template.html`, `studio.html`, and the meta/OG/head.*

**Context that shapes every finding:** this is a **free, open, static catalog** —
there is no signup, no checkout, no paid user tier. That is a conversion
*superpower* (the offer is "free, no account, nothing to install, runs in your
own tool") — and the site systematically **underplays it**. The single biggest
CRO theme here is not "add persuasion" but "stop hiding how cheap and safe the
yes is," plus "cut the choice-friction at the moment of action."

The real primary conversion is **copying a brief** (or installing / adding the
MCP). The secondary conversion is **partner/sponsor interest** (the project's
actual revenue path), and that funnel currently has no closing action.

> **Backlog reconciliation (2026-07-09).** Dispositions: **F3** (stale meta/OG
> counts) — **FIXED**: counts injected from source. **F4** (no JSON-LD/canonical)
> — **FIXED**: `SoftwareApplication` JSON-LD + canonical URL added. **F8** (jargon
> in the scan path) — **FIXED**: "MCP" and "conductor" glossed. **F5** (partner funnel has no closing action) — **FIXED**: added a primary
> "Partner with us →" CTA (routed to the repo's GitHub, the honest channel without
> exposing a personal email). **F1**
> (promote the free/no-signup offer) — **FIXED**: the hero offer line leads with
> "free & open · no signup · nothing leaves your machine." **F6** (two "start"
> CTAs) — **FIXED**: the nav "Get started" CTA now points at `#catalog`, the same
> primary destination as the hero. **F2** (default way-in) — **FIXED**: the copy-paste
> way is badged "Start here" with a primary CTA + accent border. **F7** (copyable
> brief near the hero) — **DEFERRED**: the report scopes it as an A/B test, not a
> blind ship.
> See `FIXLOG.md`.

---

## 1 · Funnel map

| # | Surface | The one action it must drive | Who lands / their question | Biggest leak |
|---|---|---|---|---|
| 1 | **Hero** (`template.html:379-398`) | Scroll into value / click "Browse the catalog" | Cold. *"What is this and is it for me?"* | Doesn't name the artifact or the near-zero cost/effort above the fold; two CTAs + a third nav CTA compete (`:374`, `:388-389`). |
| 2 | **Value** (Problem `:401-411` → How `:414-430` → Payoff `:433-456`) | Build belief; keep scrolling to the catalog | Cold→warming. *"Does this fix my inconsistent-agent problem?"* | Strong section — but ~4 screens of reading sit between "interested" and the first copyable card. No shortcut to act. |
| 3 | **Catalog** (`:460-489`, finder `buildFinder()`) | **Tap Copy on a brief** (core conversion) | Warm. *"Which one do I use, and how?"* | Opens on the finder, not on copyable cards; the money action (Copy) is one more step down. |
| 4 | **Ways in** (`:528-553`) | Choose an integration and act | Warm/ready. *"How do I actually start?"* | **Choice friction** — copy / install / MCP presented as three equals; no obvious default. |
| 5 | **Playbooks** (`:493-516`) | Copy a playbook conductor | Warm. *"Is there a done-for-me path?"* | Good. Partner band below it (`:500-515`) has **no closing action** for the revenue funnel. |
| 6 | **Activation** (off-site, in the user's agent) | Paste → get a report | — | Out of scope here; covered in ACTIVATION.md. |

---

## 2 · Findings (lens · location · visitor experience · fix · lift · effort)

Ranked by lift ÷ effort.

### F1 — The offer's best feature (free, no signup, no risk) is a micro-line *(lens 7: pricing & offer / lens 2: value)* — **lift H · effort S · SHIP**
- **Location:** the only above-the-fold mention of cost is the micro line `template.html:391` — "75 briefs · 15 playbooks · install in one line · MIT licensed & free." The risk-reversal that seals it ("Everything stays local", "Read-only by default") is four screens down (`:425-429`).
- **First-time experience:** the visitor reads a benefit ("senior code auditor") but not the *price of trying* — do I sign up? does it cost? will it touch my code? Uncertainty at the top suppresses the scroll.
- **Fix:** promote the offer into the hero as a first-class line or badge row: **"Free & open · no signup · nothing leaves your machine."** Removing perceived cost/risk is the cheapest lift on the page.

### F2 — "Three ways in" has no default → choice friction at the moment of action *(lens 5: friction / lens 3: the one action)* — **lift H · effort S · SHIP**
- **Location:** `template.html:528-552` — "01 · COPY / 02 · INSTALL / 03 · AGENT" as three equal-weight cards.
- **First-time experience:** a ready visitor now has to *evaluate three options* (and two involve shell commands / "MCP") before doing anything. The zero-friction path (copy-paste, "Nothing to install", `:535`) is buried as a peer of the two higher-friction ones.
- **Fix:** make copy-paste the obvious default — badge it "Start here," give it primary visual weight, and demote install/MCP to "also available." Prefer removing the decision over explaining all three equally.

### F3 — Stale counts in the meta/OG tags cost clicks and credibility *(lens 9: findable & shareable)* — **lift M · effort S · SHIP**
- **Location:** meta description `:7` "**75 briefs**"; og:description `:9` "**75 briefs**, 15 playbooks". Actual: **129 briefs, 32 playbooks** (`catalog.json`, `playbooks.json`). (The rendered hero self-heals via JS at `:772-778`, but the tags that Google and social unfurls read do not.)
- **First-time experience:** the search snippet and the shared card — the surfaces that decide the *click* — undersell the catalog by ~40% and disagree with the on-page number a visitor sees after clicking.
- **Fix:** inject real counts into the meta/OG tags from `build.py`. (Shared with COMPREHENSION F2 / SHOWCASE F7.)

### F4 — No structured data or canonical *(lens 9: findable & shareable)* — **lift M · effort S · SHIP**
- **Location:** `template.html` head — zero `application/ld+json`, no `<link rel="canonical">` (confirmed: both absent).
- **First-time experience:** happens *before* the visit — weaker/again inconsistent rich results and a missed shot at SoftwareApplication/FAQ rich snippets that lift organic CTR.
- **Fix:** add JSON-LD (`SoftwareApplication` or `WebSite` + `FAQPage` from the "How it works" Q&A) and a canonical URL. Safe, mechanical.

### F5 — The partner/sponsor funnel has no closing action *(lens 3: the one action / lens 7: offer)* — **lift M · effort S · SHIP**
- **Location:** partner band `:500-515`; its only link is "View the collab template →" (`:513`) — informational, not transactional. No "become a partner / sponsor / get in touch," no contact path.
- **First-time experience:** a prospective sponsor who *is* sold reads the modes ("Themed & limited-time", "Sponsored bundles") and then has nowhere to go. The revenue funnel leaks at the exact point of intent.
- **Fix:** add a primary CTA — "Partner with us →" / "Sponsor a playbook →" — pointing to a contact route (mailto or short form). Keep the template link as secondary.

### F6 — Two competing "start" destinations *(lens 3: the one action)* — **lift L-M · effort S · SHIP**
- **Location:** nav CTA "Get started" → `#start` (`:374`) vs hero primary "Browse the catalog" → `#catalog` (`:388`). Two prominent CTAs send the same intent to different places.
- **First-time experience:** minor disorientation; "Get started" lands on install/MCP options (Ways in) rather than the catalog most visitors want.
- **Fix:** point both at the same next step (recommend `#catalog`), or relabel the nav CTA to match its destination.

### F7 — The money action sits below ~4 screens of value *(lens 5: friction)* — **lift M · effort M · TEST**
- **Location:** the first copyable `.copy` button (`:252`) only appears in the catalog (`:488`), after Problem/How/Payoff.
- **First-time experience:** an action-ready visitor must scroll a long way to *do* something. Long value-first pages convert well for cold traffic but tax warm/returning visitors.
- **Fix (hypothesis):** surface one real, copyable "try this brief" near the hero, or change the hero primary CTA to "Copy your first brief." Worth an A/B test, not a blind change.

### F8 — Jargon in the scan path slows the ten-second read *(lens 8: scannability)* — **lift L · effort S · SHIP**
- **Location:** "conductor" (`:520-522`), "MCP" (`:547-548`), "brief" used before definition (`:386`). (Detailed in COMPREHENSION F3-F5.)
- **Fix:** one-line glosses. Cheap scannability + comprehension win.

### What already converts — keep it
- **Risk reversal is excellent** (`:425-429`): "Read-only by default / It ends by asking / Everything stays local" pre-empts the scariest objection (will it break or leak my code?).
- **Value-not-features is strong** (`:401-410`, `:433-443`): real pain named in developers' own words, capabilities framed as outcomes ("Evidence, not vibes").
- **Copy interaction is clean** (`:252-254`): prominent button, instant "Copied ✓" feedback.
- **Speed & PWA signals** are strong: preloaded fonts, deferred scripts, no heavy media, manifest + service worker. Fast pages convert; don't regress this.

---

## 3 · Top 5 lifts (ranked by leverage)

1. **Promote the free/no-signup/local offer into the hero (F1).** — *Ship first.*
   It's the highest lift for the least work and it removes the top unspoken cost
   at the exact moment the visitor decides whether to invest attention. Nothing
   else converts if they bounce here.
2. **Give "Three ways in" a default: "copy-paste, start here" (F2).** Removes the
   biggest decision-friction on the path to the primary action.
3. **Fix stale counts in meta/OG + add structured data/canonical (F3+F4).** Wins
   happen before the visit — more clicks, more trust on arrival.
4. **Add a closing CTA to the partner band (F5).** The only funnel with actual
   revenue attached currently has no button.
5. **Unify the two "start" CTAs and gloss the jargon (F6+F8).** Small, safe,
   compounding clarity gains.

---

## 4 · Ship vs test

**Ship now — proven best practice, low risk:**
- F1 hero offer prominence · F2 default way-in · F3 meta/OG counts ·
  F4 JSON-LD + canonical · F5 partner CTA · F6 unified start CTA · F8 glosses.

**Test — hypotheses that could cut both ways:**
- F7 surfacing a copyable brief near the hero / changing the hero CTA wording
  (risk: undercuts the value-first narrative for cold traffic — A/B it).
- Adding usage social proof near a CTA (stars, "used by") — depends on assets and
  is the subject of PROOF.md; validate the numbers before displaying them.

**Handle with care (trust/clarity/accessibility):**
- Don't shorten the risk-reversal guards to make room — they carry the trust.
- Keep the fast, media-light first paint when adding any hero badge/visual.

---

## Report only — which lifts do you want me to make?

This was a read-only pass; nothing was changed. The "ship now" set (F1–F6, F8) is
safe, mostly small, and several overlap with fixes proposed in COMPREHENSION.md
and SHOWCASE.md — so they can be batched. F7 and any social-proof additions
should be treated as experiments / are covered by later stages.

Tell me which lifts to implement (any subset), and whether hero-copy changes
should use my proposed wording or your own. I'll make only the changes you pick.
