# Visual Hierarchy Audit — HIERARCHY.md

Read-only pass over the rendered surfaces of this site: the landing page
(`template.html`), the generated brief/playbook detail pages
(`build.py` → `SITE_CSS`, `brief_detail`, `playbook_detail`), and the two
standalone tools (`studio.html`, `vitals.html`). Every claim below cites the
selector, token, or measured value that decides the emphasis. No screenshots —
the styles are the evidence.

The site has one strong idea working for it: **color = family, everywhere**
(`--fc` swapped per `.f-*` class, `build.py:30` / `template.html:38`). That
gives the catalog a real structural signature. The hierarchy problems are
almost all *over*-emphasis — arbitrary tokens shouting, and two "primary"
actions competing — not a lack of styling. Fixes are therefore mostly
subtraction.

> **Backlog reconciliation (2026-07-09).** Dispositions: **F1** (two competing
> amber primaries) — **DONE** in the mobile landing pass: the nav "Get started"
> CTA is now a ghost/outline (`background:transparent;border:1px solid
> var(--line-3)`), so one filled primary wins per viewport. **F2** (brief id
> louder than the title) — **DONE** in the same pass: cards demote the id and
> promote the title. **F3–F7** (Studio drop-zone weight, meta-row tiering,
> hero-illustration contrast, cross-page primary color; empty-state recovery is **F7 → FIXED**, moved to `--dim`) —
> **DEFERRED**: these are subjective visual-hierarchy calls best made with a
> designer's eye on the rendered result. See `CHANGELOG.md` (Unreleased) and
> `FIXLOG.md`.

---

## 1 · Screen table

| Screen | Should win | Actually wins | The deciding styles |
|---|---|---|---|
| **Landing hero** (`/`) | The H1 promise + the one primary CTA "Browse the catalog" | A three-way split: H1, the decorative `.art` report mockup, and **two** amber primaries | `.hero-in{grid-template-columns:1.05fr .95fr}` `template.html:83`; `.art{box-shadow:0 30px 70px -40px rgba(0,0,0,.9)}` `:96`; nav `.nav-cta` amber `:60` **and** hero `.btn-primary` amber `:67` visible together |
| **Catalog card** (core value, ×75) | The brief **title** + the **Copy** action | The brief **id number** (20px, family color) ties Copy for loudest element; the title reads as neutral body text | `.num{font-size:20px;font-weight:600;color:var(--fc)}` `:245`; `.copy{background:var(--fc)}` `:249`; `.ct{...color:var(--text)}` `:247` |
| **Card meta row** | Copy (above) wins; one clear secondary (Details) | Nothing — 7–8 controls all at 11.5px mono, near-equal weight | `.card-meta{font-size:11.5px}` `:252`; `.out`,`.detail`,`.view`,`.iconbtn` all ≈11.5px `:253–262`; row assembled `template.html:912` |
| **Brief detail hero** (`/b/NN`) | "Copy this prompt" primary | It does win locally — but the sticky nav `.nav-cta` "Get started" (amber, filled) competes above it | cta built `build.py:577`; `.nav-cta{background:var(--amber)}` `build.py:344` |
| **Studio, entry** (`/studio`) | The `.drop` zone — load a report | The nav "Get started" CTA: on first load it is the **only** filled/loud control; the actual first action is a quiet dashed panel | `.drop{border:1.5px dashed var(--line);background:var(--panel)}` `studio.html:64–68`; `.cta{background:var(--amber)}` `studio.html:48` |
| **Studio, loaded** | "Copy Fixer prompt" | It wins — red `.fixbtn` in a fixed bar | `.fixbtn{background:var(--act)}` `studio.html:162`; `.selbar{position:fixed;bottom:0}` `:154` |
| **Catalog empty state** | The recovery path (closest matches) | The apology text; recovery buttons sit below at `--faint` | `.empty{color:var(--faint);font-size:13px}` `template.html:267`; recovery `.iconbtn`s `:956` |

---

## 2 · Findings (ranked by attention misallocated)

### F1 — Two amber "primaries" compete on every page *(highest impact)*
The sticky nav ships a filled-amber CTA "Get started" → `#start`
(`.nav-cta`, `template.html:60`, `build.py:344`) on **every** page. On the
landing hero it sits directly above a second filled-amber primary, "Browse the
catalog" → `#catalog` (`.btn-primary`, `:67`, markup `:343`). Two primaries
pointing at two different anchors = zero primaries; the eye can't tell which is
*the* next step, and the two goals (install vs. browse) cannibalize each other.
The same amber nav CTA out-shouts the intended primary on the brief detail hero
and, worst of all, on Studio entry (F3).

### F2 — The brief-id number is the loudest thing in a catalog card
`.num` renders the catalog id at `font-size:20px;font-weight:600;color:var(--fc)`
(`template.html:245`) — larger and color-saturated — while the title `.ct` it
sits beside is `17.5px` in neutral `var(--text)` (`:247`). The id is the least
meaningful token on the card (an arbitrary catalog number); the title is what a
scanning user actually reads. Emphasis is inverted: the loudest treatment is
spent on the least information. Compounded when a playbook filter is active and
a filled-amber `.stepno` "step N" badge stacks on top (`:246`, `:853`).

### F3 — Studio's real first action is the quietest control on screen
The intended entry action is the drop zone, styled as a low-contrast dashed
panel: `border:1.5px dashed var(--line);background:var(--panel)`
(`studio.html:64–68`). On first load, before any report exists, the only
filled/high-contrast control anywhere is the nav "Get started" CTA
(`.cta`, amber, `studio.html:48`) — which navigates *away* from Studio. The
squint test picks the wrong element: the loudest thing points off-page while the
job-to-be-done recedes into the background.

### F4 — The card meta row is 7–8 controls at one weight
`meta.append(out, info, det, view, run, sq, share)` plus an optional `ex`
(`template.html:912–913`) puts up to eight controls in one row, every one at
`~11.5px` mono (`.card-meta:252`, `.out:253`, `.detail:255`, `.view:257`,
`.iconbtn:261`). Only `.detail` "Details →" carries color (`--fc`, weight 600,
`:255`), so the one genuinely useful secondary — open the full page — is barely
distinguished from four power-user toggles (mark run, +seq, link, sample). When
everything is a chip, nothing is a button.

### F5 — Decorative severity chips borrow primary-level contrast (hero)
The hero `.art` is explicitly illustrative (`aria-label`, `template.html:351`),
yet its S1/S2/S3 severity chips are filled at full saturation — `.s1{background:#E8705F}`,
`.s2{background:#E8B44C}`, `.s3{background:#8B96A5}` (`:105`) — and the whole card
carries a 70px drop shadow (`.art{box-shadow:0 30px 70px -40px}`, `:96`). A
decoration is drawing eye-weight that rivals the real CTA. High contrast should
be reserved for what the user must act on.

### F6 — The "primary action" color is not stable across pages
Everywhere except Studio, the do-this signal is amber / the family `--fc`
(nav CTA, `.btn-primary`, `.copy`). Studio redefines the accent to red
`--act:#E84C3D` (`studio.html:31`) and uses it for the H1 tick, drop-hover,
every finding's left border, and the primary `.fixbtn` (`:57,69,113,162`). A
user who learned "amber = act" on the catalog meets a red primary on Studio.
The emphasis convention resets between pages, so the strongest hierarchy cue —
color — stops being reliable. (Also relevant to the Brand audit.)

### F7 — Empty state hides its own recovery path
On a zero-result search the heading is `.empty{color:var(--faint);font-size:13px}`
(`template.html:267`) — the faintest text token on the site — and the "closest
matches" recovery buttons render as ordinary dim `.iconbtn`s (`:956`). The one
moment a user is stuck, the way out is the quietest thing on the page. The logic
is good (`closest(query,3)`, `:951`); only the emphasis is wrong.

---

## 3 · Fixes (demotions first — the fastest hierarchy fix is quieting what shouts)

1. **Resolve the double primary (F1).** Demote the nav CTA to a ghost/outline
   treatment (drop `background:var(--amber)` on `.nav-cta`, `template.html:60`
   / `build.py:344`; give it `.btn-ghost`-style border) so exactly one filled
   amber primary is visible per viewport. One-line change, repo-wide effect.
2. **Demote the card id, promote the title (F2).** Drop `.num` to `~13px`,
   `color:var(--faint)`, and lift `.ct` to `font-weight:800` (`template.html:245,247`).
   The id becomes a quiet label; the title becomes the focal point it should be.
3. **Make Studio's drop zone the loud element (F3).** Give `.drop` a solid
   accent border and a filled or tinted CTA affordance on load
   (`studio.html:64`); it should out-weigh the nav CTA, not lose to it.
4. **Collapse the meta row to one tier + a "more" (F4).** Keep `.detail`
   "Details →" visible; fold run / +seq / link / sample behind a single
   overflow affordance (they're power-user actions). Reduces per-card chrome
   across all 75 rows (`template.html:912`).
5. **Quiet the hero illustration (F5).** Reduce `.art` shadow and desaturate or
   outline the S1/S2/S3 chips (`template.html:96,105`) so the decoration stops
   competing with the CTA.
6. **Standardize the primary color (F6).** Either keep Studio on the family/amber
   primary, or make "act = red" a deliberate, documented convention used
   *only* for destructive/commit-adjacent actions everywhere. Pick one.
7. **Promote the empty-state recovery (F7).** Raise `.empty` text to `--dim`
   and give the "closest matches" buttons a slightly stronger affordance
   (`template.html:267,956`).

Ranked by attention reclaimed per line changed: **1, 2, 3** are near-free and
fix the three squint-test failures; 4 is the biggest chrome reduction but
touches more markup; 5–7 are polish.

---

## 4 · The one rule

**One filled color per viewport, and spend it on the single action you want
next.** In this codebase "filled `--fc`/amber (or `--act`)" *is* the primary
signal — so every extra filled control (a second CTA, an id number, a
decorative badge) is a tax on the one that matters. Emphasis here is a fixed
budget: promote by demoting everything else. Any element that isn't the
screen's job should be a border, a chip, or `--dim` text — never a fill.

---

*Report only. These are proposed demotions, not changes — nothing has been
edited. **Which of these fixes should I make?** (F1's single-line nav-CTA
demotion and F2's card-id/title swap are the highest attention-per-line and a
good first commit.)*
