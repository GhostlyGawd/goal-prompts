# Spacing & Layout Audit — LAYOUT.md

Read-only reverse-engineering of the spacing system across `template.html`,
`build.py`→`SITE_CSS`, `studio.html`, `vitals.html`. Every value is grepped
from those files with counts; selectors and lines are cited.

**Headline:** the *patch layer is essentially empty* — one deliberate negative
margin, zero layout `!important`, no absolute-position alignment hacks. That's
real discipline and rare. The debt is elsewhere: there is **no spacing scale**
(≈30 distinct values, and the 2nd- and 4th-most-common gaps — 9px and 7px — sit
off any 4/8 grid), and the three hand-authored stylesheets **diverge** on the
things that should be shared: container width (1060 / 940 / 760), gutter
(22 / 20), section rhythm (60 / 46 / 40 / 34), and the nav breakpoint
(720 / 680 / 640). Fix the system, not the instances.

> **Backlog reconciliation (2026-07-09).** This audit's specific widths and line
> numbers predate the redesign (the landing `.wrap` is now 1120px, tokens moved to
> `tokens.css`). Dispositions: **L1** (container widths) — **FIXED**: the four `.wrap`
> widths now come from `--w-page/--w-doc/--w-read` tokens with a single `--gutter`
> (24px), ending the 24/22/20 drift. **L3** (nav breakpoint) — **FIXED**: unified
> to 720px (detail pages were 680). **L2/L4/L5/L6** (max-width ladder, section
> rhythm, per-grid breakpoints, margin-vs-gap) — **DEFERRED** as one dedicated
> systematization pass. Note: **L5** breakpoint *tokens* are infeasible in raw CSS
> (`@media` can't take `var()`), so breakpoint values are unified, not tokenized. Rationale: the redesign already
> centralized color/type/radius/motion-adjacent tokens in `tokens.css` (partial
> progress on the "define once" goal), but a full spacing + breakpoint + container
> scale touches hundreds of hand-tuned values across four files and would shift
> every line citation in the design reports — high churn best done deliberately,
> not folded into this correctness-and-a11y pass. The clean "patch layer" this
> audit praised remains clean. See `FIXLOG.md`.

---

## 1 · The spacing census

### Distinct values in use (gap ∪ margin ∪ padding-axis)
`0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 26, 30,
32, 34, 40, 44, 46, 56, 60, 66` — **~30 distinct steps.** A tokenized 4/8 scale
has ~8.

### Gaps, by frequency (the tell)
```
8px ×17   9px ×13   12px ×10   7px ×8   18px ×7   10px ×7   6px ×5
5px ×4    16px ×4   14px ×4    4px ×3   20px ×3   13px ×3   11px ×2 …
```
Against a strict **8pt** grid {8,16,24,32,40,48}, only ≈24% of gap usage is on
it; against a **4pt** grid ≈41%. So **~59% of gaps are off even a 4pt grid** —
and the off-grid values aren't rare exceptions: `9px` (×13) and `7px` (×8) are
the 2nd and 4th most common gaps in the whole codebase. This isn't an 8pt system
with drift; it's continuous ~1px hand-tuning.

### Paddings — 40+ distinct compound values
`12px 14px`, `9px 11px`, `6px 12px`, `9px 15px`, `8px 14px`, `8px 13px`,
`7px 12px`, `6px 10px`, `12px 18px`, `12px 16px`, `12px 15px`, `11px 14px`,
`10px 14px`, `9px 12px`, `8px 11px`, `5px 9px`, `5px 8px`, `4px 9px`,
`4px 10px`, `2px 7px` … Button/chip insets alone span a dozen near-identical
pairs that a 3-step inset scale (`sm/md/lg`) would cover.

### Margins — ~20 distinct
Top values: `12px ×11`, `4px ×10`, `22px ×10`, `8px ×9`, `14px ×9`, `10px ×8`,
`16px ×7`, `6px ×6`, `2px ×6`, `20px ×5`, then `34, 30, 26, 24, 32, 18 …`.
`22px` (off-grid) is a top-3 margin — it's also the page gutter (below).

### The patch layer — a clean bill *(strength)*
- **Negative margins: one.** `top:-11px` on `.phase .step` (`build.py:397`) —
  a deliberate badge sitting on a card's top border, not a hack.
- **`!important`: zero in layout.** The only four hits are
  `*{transition:none!important}` inside `@media(prefers-reduced-motion)` —
  correct usage.
- **`position:absolute`: 6 total, all decorative** — hero/dhero radial
  `::before` gradients, the `.pnode::after` connector line, the `.phase .step`
  badge. None are alignment patches.
- **Transforms are interaction-only** — `scale(.96/.97)` on `:active`,
  `translateY(-1/-2/-3px)` on card hover, `rotate(90deg)` on chevrons. No static
  positioning nudges.

There is nothing to *delete* here — the debt is missing tokens, not accumulated
hacks.

---

## 2 · Alignment & container findings

### L1 — Three "content widths," all named `.wrap`
| File | `.wrap` max-width | gutter | Line |
|---|---|---|---|
| `template.html` (landing) | **1060px** | `0 22px` | `:48` |
| `build.py` (detail pages) | **940px** | `0 22px` | `:332` |
| `studio.html` / `vitals.html` | **760px** | `0 20px` | `:37` / `:35` |

Different widths are *defensible* (2-col landing vs article vs reading tool),
but three values share one class name with no token, and the **gutter drifts
22 → 20px** with no reason — so nav and content edges land on a 2px-different
column between the marketing pages and the tools.

### L2 — 13 distinct `max-width` values, no ladder
`340, 420, 460, 560, 640, 680, 700, 720, 760, 820, 860, 940, 1060`. Several
double as breakpoints (below) and as component caps. There's no discernible
container ladder — each grid picked its own ceiling.

### L3 — The same nav hides at three breakpoints
The identical nav-links component collapses at **720px** (landing,
`template.html:62`), **680px** (detail, `build.py:346`), and **640px**
(Studio/Vitals, `studio.html:50`, `vitals.html:48`). Between 640–720px the same
site shows full nav on one page and a hidden nav on another. One shared
breakpoint token fixes all three.

### L4 — Section vertical rhythm is four different numbers
"A section" pads `60px 0` on the landing (`.blk`, `template.html:111`),
`46px 0` when `.tight` (`:112`), `40px 0` on detail pages
(`section.blk`, `build.py:382`), and the tools use `header 34px` + `main 22px`
(`studio.html:51,61`). The hero is `66px 0 60px` (`:83`). Vertical rhythm should
be one scale; today it's ad-hoc per surface.

### L5 — 11 breakpoints, none shared
`420, 460, 560, 640, 680, 700, 720, 760, 820, 860` plus reduced-motion. Grids
reflow at a dozen widths — `.hero-in`@860, `.store`@860→560, `.method`@820→460,
`.lenses`@640, `.val`@820, `.ways`@820/760, `.quotes`@760, `.proof`@700,
`.pipe`@760→420. A user dragging a window resize sees the page rearrange at ten
unrelated points instead of 2–3 deliberate ones.

### L6 — Components own their outer margins (partial)
**82 `margin-top` declarations** (39 landing / 25 detail / 10 studio / 8 vitals)
push components down from the inside (`margin-top:22px`, `:20px`, `:16px`…)
rather than parents composing space with `gap`. In a mostly flex/grid layout
this is only mild chaos, but it's why the same visual "section gap" is written
as `22px` in one place and `26px` in another — the value travels with the child.

---

## 3 · Density verdicts (per key screen)

| Screen | Density | Verdict |
|---|---|---|
| **Landing** (`/`) | Airy — `.blk 60px 0`, hero `66px`, `gap:44px` | **Chosen & right.** A marketing page should breathe; it does. |
| **Catalog list** | Dense — `.card` `16px 16px 14px`, `margin-bottom:10px`, meta `gap:10px` | **Chosen & right** for scanning 75 rows. |
| **Brief/playbook detail** | Medium — `section.blk 40px 0`, `.method gap:12px` | **Chosen & right** for reading. |
| **Report Studio** | Tight — `main 22px`, `.find 11px 12px`, `margin-bottom:8px` | **Chosen & right** for a work tool. |

Density is a **genuine strength** — each surface's tightness fits its job. The
problem is never *how much* space but *which arbitrary value*: the airy landing
and the tight tool are both built from the same unscaled grab-bag, so the
rhythm reads as slightly off even when the density is correct.

---

## 4 · Fixes (one token beats forty edits)

1. **Adopt a spacing scale and map to it.** A 4pt base covers the real range:
   `4, 8, 12, 16, 24, 32, 40, 48, 64` (tokens `--s1…--s9`). Map today's ~30
   values onto it: `2/3→` none/4, `5/6/7→` (round to `4` or `8`), `9/10/11→8`,
   `13/14/15→12 or 16`, `18→16`, `22→24`, `26→24`, `30/34→32`, `46→48`, `56→…`,
   `60/66→64`. The two biggest offenders (`9px`, `7px` gaps) collapse into `8`.
   Deletes ~20 values with almost no visible change.
2. **One container token set.** Define `--w-page 1060`, `--w-doc 940`,
   `--w-read 760`, `--gutter 22` (pick one gutter — 22 or 24 — and drop the 20).
   Point every `.wrap`/`.topnav-in` at them; the 2px edge drift (L1) disappears.
3. **One breakpoint set.** Reduce to ~3 shared tokens (e.g. `sm 560`,
   `md 760`, `lg 960`) and route L3/L5 through them so the nav — and every grid
   — reflows at the same widths on every page.
4. **One vertical-rhythm token.** Replace the 60/46/40/34 section paddings (L4)
   with `--section` (+ a `--section-tight`) so "a section" means one thing.
5. **Prefer parent `gap` over child `margin-top`** for new work (L6); no need to
   rewrite 82 sites at once, but stop adding to them.
6. **Patch layer: nothing to delete** — it's already clean. Keep it that way by
   fixing systems (above), not adding instances.

Ranked by screens straightened per token: **#2 + #3** touch every page for two
tiny token blocks; **#1** is the deepest cleanup; **#4** is quick polish.

---

*Report only — nothing edited; every value grepped from source. The
highest-leverage change is **the shared container + breakpoint tokens (#2, #3)**
— they align all four surfaces for a few lines. **Which fixes should I make?***
