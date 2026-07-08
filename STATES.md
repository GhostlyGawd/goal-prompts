# Interaction States & Motion Audit — STATES.md

Read-only trace of every interactive species' state matrix and every animation's
job, across `template.html`, `build.py`→`SITE_CSS`, `studio.html`,
`vitals.html`. States are read from real selectors (a style that exists only in
a mockup does not exist here).

**Headline:** motion is a **strength** — a tight duration set (`.1 / .15 / .2 /
.4s`), one purposeful entrance keyframe, and `prefers-reduced-motion` honored in
**all four** files. Feedback is good too (copy actions flash "Copied ✓"; the
async GitHub loader shows `"loading…"` + disables). The problems are **focus**:
the site's **highest-traffic input — the catalog search — has its focus ring
suppressed** by `outline:0`, and the same bug hits the four context inputs and
Studio's paste/repo inputs. Focus visibility outranks all polish, so those lead.

---

## 1 · The state matrix (species × states)

✓ defined · ✗ missing · ⚠ broken/overridden · — n/a

| Species (selector) | Default | Hover | Focus-visible | Active/press | Disabled | Loading | Success/toggle |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| `.btn-primary/.btn-ghost` | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ `.done` |
| `.copy` (card) `template:249` | ✓ | ✓ | ✓ | ✓ | — | — | ✓ `.done` |
| `.nav-cta` `template:60` | ✓ | ✓ | ✓ | ✗ | — | — | — |
| `.iconbtn` (run/seq/link/paste) | ✓ | ✓ | ✓ | ✗ | ✗ | — | ✓ `.on` |
| `.fixbtn` (Studio) `studio:162` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (JS) | ✓ `.done` |
| `.cc / .cp` (copy) | ✓ | ✓ | ✓ | ✗ | — | — | ✓ `.done` |
| `.seqcopy` `template:276` | ✓ | ✓ | ✓ | ✓ | — | — | ✓ `.done` |
| `.view` quick-view (`<button>`) | ✓ | ✓ | ✓ | ✗ | — | — | ✓ chev+aria |
| Links `a` (nav/footer) | ✓ | ✓* | ✓ | — | — | — | — |
| Inline prose links (color-only) | ✓ | ✗ | ✓ | — | — | — | — |
| **`.search input` `template:216`** | ✓ | — | **⚠ suppressed** | — | — | — | ✗ error |
| **`.ctxbody input` ×4 `template:209`** | ✓ | — | **⚠ suppressed** | — | — | — | ✗ error |
| **`.pastebox input/textarea` `studio:84`** | ✓ | — | **⚠ overridden** | — | — | — | ✗ error |
| `#ghref` repo input | ✓ | — | ⚠ overridden | — | — | ✓** | ✗ (note only) |
| Checkbox `studio:118` | ✓ | ✗ | ✓ | — | — | — | ✓ `:checked` |
| Toggle chips `[aria-pressed]` | ✓ | ✓ | ✓ | ✗ | — | — | ✓ pressed |
| `.drop` zone `studio:64` | ✓ | ✓ | ✓ | — (`.over`) | — | — | — |
| Clickable cards (`.pcard/.storecard/.seqcard/.lens`) | ✓ | ✓ | ✓ | ✗ | — | — | — |

\* some `a` have hover, some don't. \** button shows `"loading…"`, input itself unstyled.

**The broken/empty cells that matter:** the four ⚠ input rows (focus), the
absent input **error** column (whole column empty), and the absent **disabled**
style on `.btn` (only `.fixbtn` has one).

---

## 2 · Focus & feedback findings (ranked — focus first, it's a11y not polish)

### S1 — The catalog search input has no visible focus *(highest traffic)*
`.search input{…border:0;outline:0}` (`template.html:216`). The landing page's
**only** focus rule is the global `:focus-visible{outline:2px solid var(--amber)}`
(`template.html:50`), specificity **(0,1,0)**. The input's own rule is
**(0,1,1)** and sets `outline:0`, so it wins *even while focused* — the ring
never renders. A keyboard user tabbing into the site's primary control (search
across 75 briefs) sees **nothing**. There is no `input:focus-visible` override
on the landing to rescue it (grep = none). **Fix:** add
`.search input:focus-visible{outline:2px solid var(--amber);outline-offset:2px}`
(or drop the `outline:0`).

### S2 — The four context inputs, same bug
`.ctxbody input{…outline:0}` (`template.html:209`) — `#cstack`, `#ctype`,
`#cstage`, `#cnotes`. Specificity (0,1,1) > global (0,1,0) → focus ring
suppressed. Same one-line fix per the input group.

### S3 — Studio/Vitals paste & repo inputs: focus ring overridden by source order
Studio *does* declare `input:focus-visible{outline:2px…}` (`studio.html:82`),
but the base `.pastebox input,.pastebox textarea{…outline:0}` (`studio.html:84`)
has **equal specificity (0,1,1)** and comes **later**, so the cascade picks
`outline:0` in the focused state too. The intent is there; source order defeats
it. **Fix:** move the `:focus-visible` rule after the base, or raise its
specificity (`.pastebox input:focus-visible`). Same in `vitals.html:69/71`.

### S4 — No input error state anywhere *(whole column empty)*
The GitHub-repo loader can fail (bad slug, private repo, network); today failure
is signaled only by `.note` text (`studio.html:226`) while the offending input
stays visually neutral — no red border, no `aria-invalid`. Add an `.is-error`
input treatment tied to the same failure path that writes `.note`.

### S5 — `.btn` has no disabled style
Only `.fixbtn:disabled` (`studio.html:169`, `opacity:.45;cursor:not-allowed`)
exists. If any `.btn`/`.copy`/`.iconbtn` is ever disabled it is
indistinguishable from enabled — a latent trap. Define one shared
`:disabled`/`[aria-disabled]` treatment.

### S6 — Press feedback is inconsistent
`:active{transform:scale(.96/.97)}` is defined only on `.btn`, `.copy`,
`.fixbtn`, `.seqcopy`. The many `.iconbtn` controls (mark-run, +seq, link,
paste, clear), `.nav-cta`, and `.view` have **no** press state, so some buttons
"give" under a click and others feel dead. Extend the `:active` scale to all
button species (one rule on a shared class).

### S7 — Inline prose links: color-only affordance, no hover
Anchors like `<a style="color:var(--fc)">Report Studio</a>`
(`build.py:784`) and the Studio footer links carry color but no underline and no
`:hover`, so link-ness rests on hue alone (ties to COLOR C8: color as sole
signal). Add `text-decoration` or a hover underline to inline content links.

### Feedback that's already right (keep)
- **Copy actions acknowledge instantly** — `.done`/flash swaps text to
  "Copied ✓" within one frame (`DETAIL_JS`, `template` `copyText`). No dead air.
- **Async loading is honest** — `ghload`/`demo` set `disabled=true` +
  `textContent="loading…"` then `"loaded ✓"` (`studio.html:611,623,630`).
- **`.fixbtn` disables at zero selection** (`studio.html:490`) with the count
  text explaining why — good disabled clarity.
- **No spinner flash / layout shift** — the catalog renders from inlined JSON
  (no async), so no skeletons are needed.

---

## 3 · Motion inventory

| Animation | Job | Duration · Easing | Verdict |
|---|---|---|---|
| `.card` `rise` entrance — fade + `translateY(8px)`, staggered `≤420ms` (`template:240,242,848`) | orient — rows entering the list | `.4s` · `cubic-bezier(.2,.7,.3,1)` | **Keep**, but consider skipping the stagger on *filter re-render* (it replays on every keystroke). |
| Card/panel hover lift `translateY(-1/-2/-3px)`, `.seqcard translateX(3px)` | confirm the hover target | `.15s` · ease | **Keep** |
| `:active` press `scale(.96/.97)` | confirm the press | `.1s` · ease | **Keep** — extend to all buttons (S6) |
| Chevron `rotate(90deg)` (`.view`, `.full`, `.ctx`) | connect open ↔ closed | `.2s` · ease | **Keep** |
| Button `filter:brightness()` hover | confirm | `.15s` · ease | **Keep** |
| `.card.flash` outline on hash-nav | orient — "here's the one you clicked" | — | **Keep** |
| Text/`.done` swaps ("Copied ✓") | confirm the copy | JS, ~1.6s revert | **Keep** |

**Durations in use:** `.1s ×6`, `.15s ×38` (the workhorse), `.2s ×4`, `.4s ×1`
— all inside the 100–300ms UI band (entrance at 400ms is fine). **Easings:** the
implicit default `ease` on every transition + one `cubic-bezier(.2,.7,.3,1)` for
the entrance. Essentially **one motion vocabulary already** — it just isn't
named. Nothing here is decoration-without-meaning; nothing to cut.

**Reduced motion (strength):** honored in all four files —
`@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}`
(`template:320`, `build:493`) plus `scroll-behavior:auto`; Studio/Vitals kill
transitions (`studio:182`, `vitals:89`). No autoplay, no parallax. Solid.

---

## 4 · The motion tokens to standardize

The values are already consistent; give them names so new components inherit
them instead of re-typing `.15s`:

```
--dur-press: .1s;    /* :active */
--dur-state: .15s;   /* hover, color/border/filter */
--dur-move:  .2s;    /* chevrons, expand/rotate */
--dur-enter: .4s;    /* list entrance */
--ease:       ease;                        /* all state transitions */
--ease-enter: cubic-bezier(.2,.7,.3,1);    /* entrance only */
```

Then the fixes above are cheap: one shared `:focus-visible` rule for inputs
(S1–S3), one `.is-error` input state (S4), one `:disabled` treatment (S5), and
one `:active` on a shared button class (S6).

---

*Report only — states traced from real selectors; nothing edited. The must-fix
is **S1–S3 (input focus visibility)** — it's an accessibility defect on the
primary search control, not polish. **Which fixes should I make?***
