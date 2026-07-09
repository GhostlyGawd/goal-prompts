# Color & Contrast Audit — COLOR.md

Read-only extraction of the palette this product *ships* — every hex, rgba, and
`color-mix()` in `template.html`, `build.py`→`SITE_CSS`, `studio.html`,
`vitals.html` — audited for coherence, contrast, meaning, and dark-mode
integrity. Every color claim carries its value + file; every contrast claim
carries a computed WCAG ratio (sRGB, `scratchpad/contrast.py`).

**Headline:** the surface ramp and primary text are clean and pass
comfortably. Three real problems: (1) the `--faint` text tier **fails AA
everywhere** (2.55–3.06:1); (2) **meaning is overloaded** — one green is both
"success" and a brand family, amber carries four unrelated jobs, and "danger"
is spread across three different reds; (3) the categorical system has **17
hues**, well past the point of reliable distinction. This is a dark-only site
(no `prefers-color-scheme` anywhere — `grep` = 0 hits).

> **Backlog reconciliation (2026-07-09).** This audit predates the palette
> redesign, so its specific hexes, the "dark-only / no `prefers-color-scheme`"
> claim, and the "17 families" count are stale — the site now ships a dark **and**
> a light theme across 21 families, tokenized once in `tokens.css`. Dispositions:
> **C1** (`--faint` fails AA) — **FIXED**: `--faint` now clears 4.5:1 on ink,
> panel, and panel-2 in both themes (dark `#8B8D95`, light `#6A6C73`).
> **C9** (dead `--panel-3`) — **FIXED**: removed. **C2–C7** (green/amber/red
> meaning overload, two severity ramps, 17 hues) — **RE-ASSESS**: measured against
> the old palette that no longer ships; they warrant a fresh Color audit, not the
> pre-redesign fixes. **C8** (color as sole family signal) — **DEFERRED** (a
> per-card family tag is a design call). See `FIXLOG.md`.

---

## 1 · The real palette (clustered, with counts + roles)

**36 distinct hex values** + 6 `rgba()` + 19 `color-mix()` calls. Clustered:

### Surfaces — dark ramp (tokenized)
| Token | Hex | Uses | Role |
|---|---|---|---|
| `--ink-2` | `#0F1319` | 7 | deepest — code bg, nav/report bars |
| `--ink` | `#14181E` | 8 | page background |
| `--panel` | `#1B212B` | 4→many | cards, chips, inputs |
| `--panel-2` | `#202834` | 4 | elevated panels, `.out` badge |
| `--panel-3` | `#27313F` | **0** | **dead token** — defined `template.html:30`/`build.py:321`, consumed nowhere |

### Text tiers
| Token/hex | Uses | Role | Note |
|---|---|---|---|
| `#FFF` | 4 | brightest (hover text) | untokenized |
| `--text` `#E2E6EC` | 4 | primary body/headings | ✓ |
| `#C7CEDA` | 7 | code / `.cmd` text | untokenized light gray |
| `#C6CEDA` | 7 | prose / lede / rules | untokenized light gray |
| `#C4CBD8` | 7 | prose **and** Meta family | untokenized; **doubles as a family hue** |
| `--dim` `#8B96A5` | 6 | secondary text | ✓ |
| `--faint` `#5C6675` | 4 | meta, captions, timestamps, placeholders | **fails AA — §2** |

The three light grays `#C7CEDA / #C6CEDA / #C4CBD8` are visually one color
(ΔL ≈ 1–3) doing one job — the classic "#333 next to the #343434," and none is
a token.

### Borders
`--line` `#2A3340`, `--line-2` `#37424F`, plus a one-off `#3A4452`
(`studio.html:134`, `.c-low` border — outside every token set).

### Brand / accent
`--amber` `#E8B44C` (×20, the most-used color), `--amber-2` `#F2CE7C` (hover),
`--fc` `#E8B44C` (family-color default), `--good` `#52C280`,
`--act` `#E84C3D` (Studio only). Dark inks on accents: `#12161C` (on amber/fc),
`#0C1510` (on green), `#1A1205` (on nav CTA) — three near-blacks for one job.

### Categorical / data-viz — the 17 family colors (`build.py:30`)
`Venture #C878F0 · Product #E8B44C · Quality #E8705F · Speed #4D9FFF ·
Trust #52C280 · Growth #A98CF5 · Team #3FC1C9 · Clarity #9AD4E8 ·
Design #5CE8A0 · Data #F0904A · Ops #B4C64A · Subtract #E87FB0 ·
Meta #C4CBD8 · Act #E84C3D · Agent #8B7CF8 · Automation #E8DE5A · AI-UX #F06FD8`

### Severity (two conflicting ramps)
- Landing `.art` (`template.html:105`): S1 `#E8705F` · S2 `#E8B44C` · S3 `#8B96A5`
- Studio `.c-*` (`studio.html:131`): S1 `#FF6B5C` · S2 `#F0904A` · S3 `#E8B44C` · low `#8B96A5` · fixed `#52C280`

Same labels, different colors: "S1" is coral on the landing, red in Studio;
"S2" is amber on the landing, orange in Studio.

---

## 2 · Contrast table (computed sRGB ratios)

Body text needs **4.5:1**; large text (≥24px, or ≥18.7px bold) and UI need **3:1**.

| Pair | Ratio | 4.5 | 3.0 | Where it appears |
|---|---|---|---|---|
| `--text #E2E6EC` on `--panel` | **12.90** | ✅ | ✅ | all body/headings |
| `--dim #8B96A5` on `--panel` | **5.39** | ✅ | ✅ | `.lead`, taglines |
| `--dim #8B96A5` on `--panel-2` | **4.95** | ✅ | ✅ | `.out` badge |
| prose `#C6CEDA` on `--ink` | 11.23 | ✅ | ✅ | `.prose`, `.lede` |
| `--amber #E8B44C` on `--ink` | 9.38 | ✅ | ✅ | links, kickers |
| dark `#12161C` on `--amber` btn | 9.56 | ✅ | ✅ | primary button text |
| **`--faint #5C6675` on `--ink`** | **3.06** | ❌ | ✅ | `.micro`,`.buildnote`,`.crumb` |
| **`--faint #5C6675` on `--panel`** | **2.78** | ❌ | ❌ | `.card-meta`, `.chip .n`, hints |
| **`--faint #5C6675` on `--panel-2`** | **2.55** | ❌ | ❌ | `.out` sub-text, badges |
| **`--fc` Act `#E84C3D` on `--panel`** | **4.26** | ❌ | ✅ | `.detail`,`.kicker`,`.pid` (11.5–12px) on Act family/pages |
| `--fc` Agent `#8B7CF8` on `--panel` | 4.88 | ⚠️ | ✅ | same, marginal |
| `--fc` Quality `#E8705F` on `--panel` | 5.32 | ✅ | ✅ | marginal-ish |
| `--fc` Trust/Design/Speed… on `--panel` | 5.7–10.4 | ✅ | ✅ | most families pass |
| `--line #2A3340` vs `--panel` (border) | 1.27 | — | ❌ | card/panel outlines (non-text) |
| focus ring `--amber` on `--ink` | 9.38 | — | ✅ | `:focus-visible` — good |

**Failures, by user harm:**
1. **`--faint` fails at every surface** — and it's used for *real* content
   (meta rows, timestamps, input placeholders, captions). Worst tier, most
   widespread, smallest type. **#1 harm.**
2. **Act-red `#E84C3D` as small colored text = 4.26** (and Agent 4.88) — the
   `.detail`/`.kicker`/`.pid` labels fail AA on the Act family and on any
   detail/playbook page whose accent is Act.
3. Card/panel borders at 1.27:1 are below 3:1, but cards also separate by
   surface fill, so this is low harm (decorative boundary).

---

## 3 · Findings (ranked — meaning first, then contrast, then sprawl)

### C1 — `--faint` is a readability failure across the whole site *(fix first)*
`--faint:#5C6675` (`template.html:31` et al.) computes **3.06 / 2.78 / 2.55**
on ink / panel / panel-2 — below AA (4.5) everywhere, below even 3:1 on panels.
It's applied to genuine content at 11–12.5px: `.card-meta`, `.micro`,
`.buildnote`, `.fine`, `.chip .n`, `.ctxbody .hint`, input placeholders.
Computed fixes (same calculator): `#848E9C` clears ink 5.37 / panel 4.87 /
panel-2 4.48 (≈AA); `#8A94A2` clears panel-2 strictly. But that value nearly
equals `--dim` — which is the real tell: **`--faint` should not carry reading
text.** Promote real content to `--dim` and keep a (lightened) faint only for
decorative glyphs where 3:1 suffices.

### C2 — Green means three things; one hex means two *(semantic collision)*
`--good:#52C280` (success) is the **identical hex** to the **Trust** family
color `#52C280` (`build.py:32`), and **Design** is a third green `#5CE8A0`. So a
green check, a "Trust" brief border, and a "Design" accent are the same or
near-same color with unrelated meanings. If Trust or Design content ever sits
near a success state, "done/good" and "this family" are indistinguishable.

### C3 — Amber `#E8B44C` carries four unrelated jobs
One hex is simultaneously: brand primary (`--amber`), the default family color
(`--fc`), the **Product** family (`build.py:31`), and **severity-3** in Studio
(`.c-s3`, `studio.html:133`). "Brand," "Product," and "medium severity" cannot
be told apart. Severity especially should never borrow the brand hue.

### C4 — "Danger" is three different reds, and one of them is also "action"
`Act/--act #E84C3D`, `Quality #E8705F`, and severity-1 `#FF6B5C` are three reds
with no single authority. Worse, `#E84C3D` is **both** the Studio *primary
action* button (`.fixbtn`, `studio.html:162`) **and** the Act *family/danger*
hue — a "do this" and a "danger" reading on one color. And the top-severity
color changes between surfaces (coral `#E8705F` on the landing vs `#FF6B5C` in
Studio — C6).

### C5 — Orange `#F0904A` = Data family **and** severity-2
`Data #F0904A` (`build.py:34`) is the same hex as Studio's `.c-s2`
(`studio.html:132`). The severity ramp (`#FF6B5C → #F0904A → #E8B44C`) is built
entirely from family/brand hues, so severity and family are unreadable together.

### C6 — Two severity ramps for the same concept
Landing `.art` S1/S2/S3 = `#E8705F/#E8B44C/#8B96A5` (`template.html:105`) vs
Studio `.c-s1/2/3` = `#FF6B5C/#F0904A/#E8B44C` (`studio.html:131`). Pick one
severity ramp and share it; today the marketing illustration and the tool
disagree on what "S1" looks like.

### C7 — 17 categorical hues exceed reliable distinction
The family palette (`build.py:30`) — the core "color = family" system — packs
**three purples** (`Growth #A98CF5`, `Agent #8B7CF8`, `Venture #C878F0`),
**three warm-reds** (`Quality #E8705F`, `Act #E84C3D`, `Data #F0904A`), **two
greens** (`Trust`/`Design`), and **two blues** (`Speed #4D9FFF`,
`Clarity #9AD4E8`). Adjacent in the hero `.spectrum` (`template.html:348`)
these are hard to separate, and for red-green/blue-yellow colorblindness the
warm-red and purple trios collapse. Because family is often signaled by color
alone on a card (left-border `#fc` + number; the family *name* is only in the
section header), a colorblind user can't map many cards to a family (C8).

### C8 — Color as sole signal (localized)
Mostly OK — severity chips carry text labels ("S1"), focus is an *outline* not a
hue. But an individual catalog card encodes its family **only** by color
(`.card{border-left:3px solid var(--fc)}` `template.html:240`, `.num` color);
the family name isn't on the card. Add a text/(icon) family tag per card, or
rely on the section header being always visible.

### C9 — Sprawl: dead + one-off + untokenized values
`--panel-3 #27313F` is defined twice and used **zero** times. `#3A4452`
(`studio.html:134`) is a one-off border gray outside the token set. Three light
body grays (`#C7CEDA/#C6CEDA/#C4CBD8`) and three dark inks
(`#12161C/#0C1510/#1A1205`) are untokenized near-duplicates. `#FFF` (×4) is an
untokenized brightest-text.

### What's already good
Surface ramp is a real, ordered dark system; `--text`, `--dim`, prose grays,
amber, and all dark-on-accent button texts pass comfortably (7–14:1);
interactive states are mostly derived systematically (`filter:brightness` on
hover, `opacity` on disabled); focus rings are high-contrast outlines.

---

## 4 · The token proposal (smallest palette covering today's uses)

**Surfaces (4):** `--ink-2 #0F1319`, `--ink #14181E`, `--panel #1B212B`,
`--panel-2 #202834`. *Delete `--panel-3`.*

**Text (4):** `--text #E2E6EC`, `--body` (one gray, replacing the C7/C6/C4
trio — keep `#C6CEDA`), `--dim #8B96A5`, `--faint` **lightened to ≥#848E9C** and
reserved for decorative/large text only.

**Ink-on-accent (1):** collapse `#12161C/#0C1510/#1A1205` → one `--on-accent
#111`.

**Brand (2):** `--brand #E8B44C` + `--brand-hi #F2CE7C` (hover).

**Semantic states (3), each a distinct hue not shared with a family or brand:**
`--success` (keep green **but** stop reusing it as the Trust family hex — give
Trust a different green or rename), `--warning`, `--danger` — pick **one** red
for danger and stop using it as a primary-action fill.

**One severity ramp (shared):** e.g. `S1 → S2 → S3 → low → fixed`, defined once
and imported by both the landing illustration and Studio.

**Categorical (family):** keep the 17 for identity, but (a) never rely on it as
the *sole* signal (C8), and (b) reserve `--danger`/`--success`/`--warning` as
semantic tokens *distinct* from any family hex so meaning never collides with
identity (C2–C5).

Net: removes 1 dead token, ~5 untokenized near-duplicates, and — most
importantly — **decouples meaning from brand identity** and lifts `--faint`
above the AA line.

---

*Report only — nothing edited; contrast math in `scratchpad/contrast.py`. The
highest-harm, lowest-risk fix is **C1** (lighten `--faint` / stop using it for
content text — one token, site-wide AA win); the highest-*value* fixes are
**C2–C5** (separate semantic state colors from brand/family hexes).
**Which fixes should I make?***
