# Show, Don't Tell

*Does this product **show** its value and mechanics — screenshots, demos,
diagrams, annotated examples, before/afters — or only **describe** them in prose
a visitor has to trust?*

Read-only pass over the public surfaces: landing (`template.html`), Report Studio
(`studio.html`), sample reports (`examples/index.html`), and the repo's actual
media assets.

**Verdict:** the *method* is shown well — the four-phase pipeline is a real
diagram, and per-brief social cards are auto-generated on-brand. But the
**product is never seen working**. The only raster assets in the entire repo are
OG share cards (`og/<id>.png`) — brief *metadata*, not the product. There is **no
screenshot, GIF, or video** of an agent running a brief, of a real report, or of
the Studio UI. The site even leans into this with the headline *"Real reports,
not screenshots"* (`template.html:562`) — honest positioning, but it has become a
reason to show a visitor nothing at all. A stranger must *believe* the core
promise ("turn your agent into a senior code auditor") because they never get to
*watch* it happen.

> **Backlog reconciliation (2026-07-09).** Dispositions: **F6** (partner
> placeholder reads as unfinished) — **FIXED**: the band is now labeled an example
> with "no real partnership implied." **F3** (finding → commit before/after) — **FIXED**: a real
> inline before/after (a BUGS.md S2 finding → the FIXLOG commit that fixed it) now
> sits in the Proof section — real artifacts, no screenshot, can't drift. **F2**
> (the Studio, pictured) — **DECLINED (by design)**: an embedded self-screenshot
> would contradict the site's own "Real reports, not screenshots" stance and
> reintroduce media-staleness (F7). **F1** (the product never seen
> working) — **ADDRESSED (round 3, honestly)**: the Proof section now carries an
> animated *walk-through* of one real run — the `/goal:bug-hunt` command, the four
> phases completing, and the real `BUGS.md` S2 self-XSS finding it produces — built
> only from real content and labeled “walk-through, not a screen capture” in both
> the header and caption. It plays once when scrolled into view and falls back to a
> static final frame under `prefers-reduced-motion`/no-JS (verified: all lines
> opacity 1). This is *not* the captured screen recording F1 ideally wants — a real
> capture can’t be recorded in this environment, and a staged one would cut against
> “Real reports, not screenshots” — it’s the honest, non-fabricated proxy: it shows
> the loop working using only real artifacts. A true recording stays a nice-to-have
> for a maintainer with capture tooling. **F4**
> (schematic report mock) — **FIXED**: the mock now carries a real text
> alternative (`role=img` + `aria-label`) and a visible "the shape of every
> report" caption instead of `aria-hidden`. **F5** (mobile hero has no visual) —
> **ADDRESSED**: the hero micro line (live counts) and the quickstart button are
> always visible on mobile, so the phone hero shows scope + an action, not pure
> prose; a dedicated sparkline stays optional polish. **F7** (static `og.png` can
> drift) — **FIXED**: `og.png` was regenerated to the live 135/21 counts,
> `scripts/og.py` embeds the brief count as PNG metadata, and the build now fails
> if it drifts. See `FIXLOG.md`.

---

## 1 · Show-vs-tell map

| Key claim of value | Shown or told today | The visual that would prove it |
|---|---|---|
| "Turn your coding agent into a senior code auditor" — *it actually works* | **Told** — no footage of a run anywhere | A GIF/clip: paste a brief into Claude Code → agent audits → `BUGS.md` appears |
| "Every brief runs the same four-phase audit" | **Shown** ✓ — pipeline diagram (`:418-424`) | Already proven — keep |
| "one evidence-backed report you can act on" | **Shown as schematic** — `BUGS.md` mock (`:446-454`), `aria-hidden`; real files linked at `/examples/` | A real, annotated `BUGS.md` excerpt (real severity chip, real `file:line`) |
| "17 families, one question each" — *scope* | **Shown** ✓ on desktop — bar chart (`:394-397`); **hidden on mobile** (`:102`) | A lightweight mobile fallback stat/sparkline |
| "Report Studio turns findings into a Fixer prompt" | **Told on landing** (`:566-570`); live demo only *after* clicking through to `/studio` | Annotated screenshot of the Studio mid-use, embedded in the Proof card |
| "those reports turned into commits" — *the payoff/after* | **Told** (`:563`) + linked FIXLOG | A before/after: one finding beside the commit/diff that fixed it |
| "install in one line" / slash commands | **Shown** ✓ — the command string is visible (`:542`) | Optional: a 2s terminal clip of `/goal:bug-hunt` |

Pattern: **how it works** and **what you get (structure)** are shown; **that it
works** and **the outcome (after-state)** are only told.

---

## 2 · Findings (lens · location · what a visitor can't see · asset · effort)

Ranked by persuasion-per-pixel.

### F1 — The product is never seen working *(lens 2: the product, unseen)* — **HIGH · effort M**
- **Location:** whole site. Confirmed by asset inventory — the only images in the repo are `og/*.png` share cards (generated by `scripts/og.py` from front matter) and one static `og.png`. Zero screenshots, GIFs, or video.
- **What a visitor can't see:** the single most important thing — an agent actually ingesting a brief and producing a report. The promised loop (copy → paste → audit → report at repo root) is asserted in the hero (`:386`) and never witnessed.
- **Asset to add:** one 10–15s screen capture (or a 3-frame annotated strip) of a real run in Claude Code, ending on the report file appearing. Place it in the hero or the "Evidence, not vibes" Payoff section.

### F2 — The Studio is sold in prose on the page that sells it *(lens 1: prose where a picture belongs)* — **HIGH · effort S**
- **Location:** Proof section, `template.html:556-571` — "every finding becomes a checklist item with a severity chip… one tap builds a targeted Fixer prompt," followed only by a text link "Open the Report Studio →".
- **What a visitor can't see:** the Studio's genuinely photogenic UI — the checklist, the severity chips, the checked-state highlight, the "build Fixer prompt" button (`studio.html:108-120`, `:210`). Ironically the Studio itself *does* show its value (it has a working "try it on this repo's own reports" demo button, `studio.html:210`) — but nobody sees that until they've already clicked away from the landing page.
- **Asset to add:** one annotated screenshot of the Studio mid-use, embedded in the Proof card. The tool is live, so capturing it is near-zero design work.

### F3 — The payoff (findings → commits) is told, never pictured *(lens 4: show the outcome)* — **MED-HIGH · effort M**
- **Location:** Proof card "Real reports, not screenshots" (`:562-564`) and `examples/index.html:52-56` (the FIXLOG card) — "the findings above became eight commits… one per finding, each verified."
- **What a visitor can't see:** the *after-state*. The most persuasive artifact this project owns — "a finding turned into a real commit" — exists (FIXLOG.md) but is only linked, never shown as a before/after.
- **Asset to add:** a two-panel before/after — a real `BUGS.md` finding on the left, the commit/diff that resolved it on the right.

### F4 — The one outcome visual is a schematic, and hidden from screen readers *(lens 4 / lens 5)* — **MED · effort S**
- **Location:** the sample report mock, `template.html:446-454`. It is hand-built HTML showing section *titles* ("Summary", "Findings", "Verification plan", "Top 3 to fix first") with generic descriptions, and it carries `aria-hidden="true"` (`:446`).
- **What a visitor can't see:** a *real* finding. It shows the report's shape, not its substance — no real severity+confidence chip, no real `file:line` citation, the very things the Payoff list promises two columns over (`:440-443`).
- **Asset to fix:** replace the schematic with a real (truncated) `BUGS.md` finding, or caption the mock honestly as "the shape of every report." Either way, give it a text alternative.

### F5 — The mobile hero has no visual at all *(lens 7: weight & accessibility)* — **MED · effort S**
- **Location:** `template.html:102` — `@media(max-width:820px){.chartblock{display:none}}`, with the comment "the chart is a desktop flourish… drop it."
- **What a visitor can't see:** on phones (likely most social traffic) the only scope visual is removed, leaving a pure-prose hero. Dropping the heavy-scrolling chart is the right call; showing *nothing* is not.
- **Asset to add:** a lightweight static fallback — a single stat block ("129 briefs · 17 families") or a simplified sparkline — so the mobile hero still shows scope.

### F6 — A placeholder visual reads as "unfinished" to real users *(lens 6: stale or fake visuals)* — **LOW-MED · effort S**
- **Location:** partner band, `template.html:500-515` — a fake "Partner Tool" with a placeholder "P" logo (`:511`) and "Partner Tool × Goal Prompts".
- **What it costs:** it's intentional (a sales example for prospective partners), but a first-time *user* sees a lorem-ipsum logo on a live marketing page and may read the whole site as half-built. A fake visual costs more trust than it earns when the audience is wrong.
- **Fix:** caption it explicitly as an example/template, or visually mark it as a mock so it doesn't read as a real, empty partnership slot.

### F7 — The site-wide OG card is a static file that can drift *(lens 6: media hygiene)* — **LOW · effort M**
- **Location:** `template.html:10` references `/og.png`; `build.py:906` only *points* at the URL — the 40 KB `og.png` is a hand-made static asset, not build-generated (unlike the per-brief cards).
- **What it costs:** the single most-shared visual can silently fall out of date (e.g., an old brief count — see COMPREHENSION F2). A misleading share card is a promise the page can't keep.
- **Fix:** regenerate `og.png` from live data; ideally build-generate it the way `scripts/og.py` generates the per-brief cards.

### What already works — keep it
- **Pipeline diagram** (`:418-424`) — the method is shown, annotated, and weightless (CSS/SVG). Model example.
- **Per-brief OG cards** (`scripts/og.py`) — every shared brief URL gets a real, on-brand 1200×630 card built from its own front matter; `build.py` fails if one is missing. Excellent hygiene.
- **The Studio's live demo path** — "try it on this repo's own reports" (`studio.html:210`) and the GitHub loader (`:209`) let a visitor *see real findings* without owning any. This is show-don't-tell done right; it just needs to be advertised earlier.
- **Fast, calm media** — no autoplay, no first-paint-blocking images, fonts preloaded. Good accessibility baseline to build on.

---

## 3 · Top 3 visuals to make

1. **A run, captured.** A 10–15s GIF/clip (or 3-frame annotated strip): paste a
   brief into Claude Code → the agent audits → `BUGS.md` appears at repo root.
   This proves the hero's central claim and is the highest-leverage pixel on the
   site. *(F1)*
2. **The Studio, pictured.** An annotated screenshot of the Report Studio
   mid-use — loaded findings, severity chips, checked items, the "build Fixer
   prompt" button — dropped into the landing Proof card. *(F2)*
3. **The before/after.** One real `BUGS.md` finding beside the commit/diff that
   fixed it — the FIXLOG loop, made visible. *(F3)*

---

## 4 · Media hygiene

- **Annotate/replace:** swap the schematic sample report (`:446-454`) for a real
  truncated excerpt, or caption it clearly as "structure, not a real finding";
  give it a text alternative (it's currently `aria-hidden`).
- **Fallback:** give the mobile hero a lightweight visual for the dropped chart
  (`:102`).
- **Verify/regenerate:** confirm the static `og.png` reflects the real catalog
  (129 briefs); move it into the build.
- **Caption:** mark the partner-band placeholder (`:500-515`) as an example so
  users don't read it as unfinished.
- **On any new media:** ship alt text + captions, keep it compressed, and never
  autoplay — preserve the current fast, calm first paint.

---

## Report only — which visuals do you want me to make?

This was a read-only pass; nothing was changed. The top three (F1–F3) are the
highest-leverage, but F2 (Studio screenshot) and F4/F5 (real report excerpt,
mobile fallback) are the cheapest and can land without any capture tooling.

Tell me which visuals to produce or which fixes to apply — note that F1 and F3
need a real screen capture I can't record from here, so for those I can instead
scaffold the markup/placement and captions and mark exactly where the asset
drops in. I'll make only what you pick.
