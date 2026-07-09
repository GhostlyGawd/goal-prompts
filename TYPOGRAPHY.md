# Typography Audit — TYPOGRAPHY.md

Read-only inventory of every way this product sets type, across the four style
sources: `template.html` (landing), `build.py`→`SITE_CSS` (detail pages),
`studio.html`, and `vitals.html`. Every number below is grepped from those
files; each carries its selector and line.

**Headline:** two families, sanely chosen, with genuinely good *measure* — but
the size scale has accreted to **~27 distinct sizes**, six of them separated by
a single indistinguishable half-pixel, and the font economics run exactly
backwards: the build ships and precaches a mono weight **no rule uses**
(`plexmono-500`, 14.9 KB) while **eleven selectors** request a mono weight that
**isn't shipped** (700 → faux bold). The deliverable is a smaller system.

> **Backlog reconciliation (2026-07-09).** This audit predates the font redesign
> (Archivo → Schibsted Grotesk for display, IBM Plex Sans added for UI), so its
> family names and per-size line numbers are stale. Dispositions: **T1** (mono
> @700 faux-bold) — **FIXED**: the three surviving `--mono` @700 badges retargeted
> to the shipped 600. **T2** (unused `plexmono-500`) — **ALREADY DONE**: the 500
> face was dropped in the redesign; only 400/600 ship. **T4** (same role typed 3
> ways) — **FIXED**: body line-height unified to one `--lh-body` token (was
> 1.6/1.62/1.5 across stylesheets). **T3/T5** (font-size + line-height value
> sprawl) — **DEFERRED**: collapsing ~27 sizes to a 9-step scale is a large,
> citation-shifting refactor best done as its own pass against the new fonts.
> New minor issue found & **FIXED**: `.drop-big` requested `--sans` @700 where
> Plex Sans ships only 400/600 (a fresh faux-bold) — retargeted to `--disp`
> (Schibsted Grotesk, real 700). The Studio checkbox `✓` glyph at 700 is left
> as-is (an imperceptible synthesized weight on one symbol). See `FIXLOG.md`.

---

## 1 · The inventory (measured)

### Families — 2, well-formed
| Token | Stack | Loaded as |
|---|---|---|
| `--sans` | `'Archivo', system-ui, -apple-system, 'Segoe UI', sans-serif` | one **variable** woff2, `font-weight:100 900` (`build.py:316`) |
| `--mono` | `'IBM Plex Mono', ui-monospace, 'SF Mono', Menlo, Consolas, monospace` | three static woff2: 400/500/600 (`build.py:317–319`) |

Defined identically in all four files (`template.html:33`, `studio.html:32`,
`vitals.html:30`, `build.py:324`). Fallback stacks are metric-adjacent and
sensible. `font-display:swap` on all 16 faces.

### Font-size — ~27 distinct values (the problem)
**Fixed px (18 values), with usage counts:**

```
12px ×33   13px ×23   12.5px ×17   11.5px ×16   14px ×13   16px ×10
13.5px ×10 11px ×10   15px ×9      10.5px ×8    15.5px ×7   14.5px ×5
20px ×3    19px ×3    17px ×3      17.5px ×1    10px ×1     9.5px ×1
```
**Fluid `clamp()` (8 ranges):** `44/9vw/72` (×2, `studio.html:56`,`vitals.html:54`),
`38/6vw/62` (`template.html:86`), `30/5.6vw/50` (`build.py:376`),
`24/4vw/38` (`template.html:74`), `22/3.4vw/30` (`build.py:384`),
`20/3vw/26` (`build.py:486`), `16/2.4vw/20` (`build.py:377`),
`16/2.2vw/19` (`template.html:88`). Plus `.88em` for `code` (×2).

The tell-tale of accretion — **six half-pixel pairs**, each visually identical:
`11/11.5`, `12/12.5`, `13/13.5`, `14/14.5`, `15/15.5`, `17/17.5`. There is no
ratio; the 11–17.5px band holds **15+ separate decisions**.

### Font-weight — 6 real weights
`700 ×27`, `600 ×23`, `800 ×10`, `500 ×9`, `900 ×5`, `400 ×4`. (The `100 ×4`
hits are only the `font-weight:100 900` bound in the four Archivo `@font-face`
blocks — 100 is never applied to text.) All six render from the Archivo
variable font. **Mono weights requested: 400, 600, and 700** — see §4.

### Line-height — 15 distinct values
`1.5 ×13`, `1.45 ×6`, `1.7 ×2`, `1.62 ×2`, `1.6 ×2`, `.95 ×2`, then singletons
`1.65, 1.55, 1.4, 1.35, 1.3, 1.25, 1.05, 1.03, 1.0`. The **body role alone
carries three**: `1.6` (`template.html:46`), `1.62` (`build.py:330`), `1.5`
(`studio.html:36`) — the three stylesheets have drifted.

### Letter-spacing — 12 distinct values
Headings negative (`-.01`, `-.015`, `-.02`, `-.03em`), eyebrows/kickers positive
(`.1`, `.12`, `.14`, `.16em`). Discipline is *directionally* right (tight
display, tracked-out uppercase) but four near-identical negatives could be two.

---

## 2 · The proposed scale (map every value onto it)

Keep the two families and the fluid-heading idea. Collapse the fixed-size sprawl
to **five UI steps** and the eight clamps to **four**. ~27 sizes → **9**.

**Fixed UI scale (≈1.18 ratio, no half-pixels):**
| Step | Size / LH | Role | Absorbs today |
|---|---|---|---|
| `t-micro` | 11px / 1.4 | uppercase mono eyebrows, kickers, labels (tracking carries them) | 9.5, 10, 10.5, 11 |
| `t-meta` | 12px / 1.45 | chips, meta rows, captions, code-in-UI | 11.5, 12, 12.5 |
| `t-sec` | 13px / 1.5 | taglines, secondary body, helper text | 13, 13.5 |
| `t-body` | 15px / 1.6 | UI base / running body | 14, 14.5, 15, 15.5, 16 |
| `t-sub` | 18px / 1.3 | card titles, sub-heads (H3/H4) | 17, 17.5, 19, 20 |

**Fluid headings (4 clamps):**
| Step | Clamp | Role | Absorbs |
|---|---|---|---|
| `t-lede` | `clamp(16px,2.4vw,20px)` / 1.5 | ledes/subs | `16/2.2vw/19` |
| `t-h2` | `clamp(22px,3.4vw,30px)` / 1.05 | section H2 | `20/3vw/26`, `24/4vw/38` |
| `t-title` | `clamp(30px,5.6vw,50px)` / 1.03 | page/detail H1 | — |
| `t-display` | `clamp(38px,6vw,62px)` / 1.0 | landing/hero display | **`44/9vw/72`** (unify Studio & Vitals onto this) |

**Weights:** four is plenty — `400` body, `600` mono/UI emphasis, `700` sans
strong, `900` display. Retire the sparse `500` (9 uses → fold into 600 or 400)
and `800` (10 uses → fold into 700 or 900) unless a specific pairing needs them.

**Deletions:** ~13 fixed sizes, 4 clamps, ~10 line-heights, ~4 letter-spacing
values, and (see §4) one whole font file. Nothing above changes what a reader
perceives — the half-steps were never distinguishable.

---

## 3 · Findings (ranked by reading improved per change)

### T1 — Faux bold: mono @700 requested, never shipped *(most visible defect)*
IBM Plex Mono ships **only 400/500/600** (`build.py:317–319`, `fonts/`), yet
**eleven selectors set `var(--mono)` at `font-weight:700`**, forcing the browser
to *synthesize* bold — smeared, uneven stems, worst at the 11–13px sizes where
these live: `.nav-cta` (`template.html:60`,`build.py:344`), `.stepno` (`:246`),
`.badge` (`template.html:166`), `.art .sev` (`:104`), `.pnode .dot` (`:129`),
`.phase .step` (`build.py:397`), `.lens .i` (`:405`), `.seqstep .node` (`:466`),
`.topnav .cta` (`studio.html:48`, `vitals.html:46`). Fix: retarget all to `600`
(shipped) — or ship a 700 face. Retargeting is the smaller system.

### T2 — Font economics run backwards *(free bytes)*
`plexmono-latin-500.woff2` (**14,888 B**) is declared (`build.py:318`),
**precached by the service worker** (`build.py:994` → `sw.js`), yet **zero rules
request mono @500** — every `font-weight:500` in the codebase inherits *sans*
(`.eyebrow b`, `.quote .q`, `.hero .micro b`, `.empty b`). So the build ships +
downloads a face nobody renders, while omitting the 700 face eleven selectors
ask for (T1). Drop the 500 face → **reclaim ~14.9 KB (~18% of the ~80 KB font
payload)** with no visual change.

### T3 — Half-pixel size accretion *(scale has no spine)*
The 11–17.5px band holds 15+ sizes including six 0.5px-apart pairs
(`11/11.5`, `12/12.5`, `13/13.5`, `14/14.5`, `15/15.5`, `17/17.5`; counts in
§1). No two adjacent steps are distinguishable, so the "hierarchy" they imply
doesn't read. Collapse to the five-step UI scale in §2.

### T4 — The same role is typed three different ways across stylesheets
The three hand-authored stylesheets have drifted on shared roles:
- **Body line-height:** `1.6` (`template.html:46`) vs `1.62` (`build.py:330`)
  vs `1.5` (`studio.html:36`).
- **`.badge` weight:** `700` (`template.html:166`) vs `600` (`build.py:366`).
- **Page-H1 display:** `clamp(38,6vw,62)` (landing) vs `clamp(44,9vw,72)`
  (Studio `:56`, Vitals `:54`) — same role, two sizes.
One shared token block would end the drift.

### T5 — Line-height sprawl (15 values, §1)
Fold to five roles: display `1.0`, heading `1.05`, sub `1.3`, body `1.6`,
mono/code `1.5`. Removes ~10 improvised values.

### What's already good (leave it)
- **Measure is disciplined.** Nearly every prose block is `ch`-constrained
  inside the 45–75 target: `.hero p.sub` 52ch (`:88`), `.sub` 58ch
  (`studio.html:58`), `.lead` 60ch (`:75`) / 64ch (`build.py:385`), `.prose`
  68ch (`:386`), `.turn` 70ch (`:122`), `.dhero .lede` 60ch (`:377`). Keep.
- **The neglected text isn't neglected:** form labels (`.ctxbody label`
  `template.html:208`), captions (`.drop-small` `studio.html:73`), code, and
  empty states are each deliberately styled, not inherited.
- **Fluid headings** already form a real scale — just too many steps (§2).

---

## 4 · Font economics — loaded vs. used

| File | Bytes | Status |
|---|---|---|
| `archivo-latin-var.woff2` | 34,928 | **used** — one variable file covers every sans weight (400/500/600/700/800/900). Efficient. |
| `plexmono-latin-400.woff2` | 14,708 | **used** — mono body/labels default weight. Preloaded (`build.py:536`). |
| `plexmono-latin-600.woff2` | 15,620 | **used** — mono emphasis (buttons, kickers, badges). |
| `plexmono-latin-500.woff2` | 14,888 | **UNUSED** — declared + precached, requested by no rule. **Reclaim.** |
| *(mono 700)* | — | **MISSING** — requested by 11 selectors (T1); currently faux-synthesized. |

**Total shipped ≈ 80.1 KB. Immediately reclaimable ≈ 14.9 KB** by deleting the
500 face (drop `@font-face` `build.py:318` + the `precache` entry `build.py:994`
+ the file). Net after also fixing T1 (retarget 700→600): **–14.9 KB and zero
faux bold**, no faces added. Only preload the two above-the-fold faces (already
done: archivo-var + plexmono-400).

---

*Report only — measured values only, nothing edited. The two highest-leverage,
lowest-risk changes are **T1** (retarget the 11 mono-700 selectors to 600 —
kills all faux bold) and **T2** (drop the unused `plexmono-500` — reclaims
~14.9 KB); they're one small commit together. **Which fixes should I make?***
