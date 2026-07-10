# FORMS.md — Forms & Validation Audit

**Date:** 2026-07-09
**Auditor:** forms-validation brief, read-only pass
**Prior run:** none — no previous `FORMS.md` existed; this is the first forms audit.

---

## 0 · Scope — what "forms" means here

This product has **no signup, no checkout, no settings backend**. Nothing here is a
classic account form, so the classic killers (password rules, required email,
verification walls) are structurally absent — that is the site's single biggest
forms win and it should stay that way.

What stands between a user and what they want is a set of **client-side input
surfaces**, all localStorage-backed, all verified live in headless Chromium
(pages served over HTTP; behavior identical on the deployed site — `file://`
differs only in `RAW_BASE`/fetch fallbacks, which both pages already guard):

| # | Form | Where |
|---|------|-------|
| F1 | Catalog search + family/playbook chips | `template.html:612–619, 1339–1344`, `js/catalog-core.js` |
| F2 | 3-question picker ("help me choose") | `template.html:1551–1607`, `catalog-core.js pickerPlan` |
| F3 | Repo-recommend ("recommend for my repo") | `template.html:588–595, 1609–1677` |
| F4 | Operator context ("aim the briefs at your repo") | `template.html:600–610, 1362–1368`, mirrored in `js/gp-detail.js:17–26` |
| F5 | Custom conductor sequence builder | `template.html:795–831, 1461–1467` |
| F6 | Report Studio — drop / paste / GitHub loader / selection | `studio.html:218–254, 520–713`, `js/report-parser.js` |
| F7 | Vitals Viewer — drop / paste | `vitals.html:114–133, 296–335` |
| F8 | Footer state tools — export / import backup, reset, reminder | `template.html:759–760, 1370–1459` |

`b/<id>` and `p/<key>` detail pages contain **no editable inputs** — only hidden
`<textarea>` copy sources (`build.py:800–805`) — and `examples/` has none.

---

## 1 · Form scores

| Form | Fields (req/opt) | Validation quality | Error recovery | Grade |
|------|------------------|--------------------|----------------|-------|
| F1 Search | 1 (0 req) | live filter, ranked fallback, zero-state with suggestions | n/a — nothing to lose | **A** |
| F2 Picker | 3 chips (0 req — answers optional, toggleable) | none needed | n/a | **A** |
| F3 Repo-recommend | 1 + button | specific messages for bad ref / 404 / 403 / offline; Enter handled; no double-submit | input preserved ✔; error is color+text only, no `aria-invalid`, hint not live | **B+** |
| F4 Operator context | 4 (0 req) | none needed; saved per keystroke | **clear = one-click irreversible wipe of all 4** | **B** |
| F5 Sequence builder | 0 typed fields | 16-stage cap enforced with explanatory toast ✔ | clear has no confirm (moderate rebuild cost) | **A−** |
| F6 Studio paste | 2 (0 req, name defaults) | empty-text caught; **duplicate-name overwrite is silent** | error hides the form; Enter in name is a no-op; note not announced | **C+** |
| F6 Studio GitHub loader | 1 + button | **best field on the site**: Enter, disabled-while-loading, `aria-invalid`, `.is-error`, error clears on input, value preserved | ✔ | **A** |
| F6 Studio selection/Fixer | checkboxes | disabled-until-selected ✔, persisted, share-link recovery ✔, lost-check note on re-add ✔ | ✔ exemplary | **A** |
| F7 Vitals paste/drop | 1 (0 req) | empty caught; no dated-table → helpful note ✔ | **no per-file remove; duplicates accumulate**; only nuke-all | **B−** |
| F8 Import backup | 1 file | bad JSON → clear toast ✔; `gp-seq` re-validated ✔ | overwrites matching keys with no preview/confirm | **B** |

Verified live: two unnamed pastes in the Studio → first report silently gone
(`["pasted.md · 1 finding"]`, only "Finding Beta" survives); empty paste → note
appears but the pastebox hides itself; Enter in the name field does nothing;
`ghref` garbage → `aria-invalid="true"`, value preserved; `rrin` garbage →
message shown but `aria-invalid` **null**; bad backup JSON → correct toast;
reset run tracker → correct two-step arm ("clear 1 run mark? click again").

---

## 2 · Findings

**FV1 · Studio paste · name field — silent overwrite on the default name.**
`addReport` (`studio.html:521–540`) replaces any same-named report without asking.
The name field defaults to `pasted.md`, so the natural flow — paste report A, add;
paste report B, add — **destroys report A with zero feedback** (the lost-checks
note at `:534–539` only fires when *checked* findings vanish). Confirmed headlessly.
*Fix:* when the incoming name already exists and the user didn't type it, suffix it
(`pasted-2.md`) — or better, **infer the name** from the first `#` heading or a
`^[A-Z-]+\.md` token in the pasted text and show it in the chip. One-line guard,
removes the field's whole failure mode.

**FV2 · Studio paste · whole form — failure hides the form; success ergonomics uneven.**
`pasteadd` (`:562–567`) unconditionally clears the textarea and hides the box, so on
the empty-input error the user's *form disappears* while the note ("That file looked
empty" — wrong noun for a paste) shows below. And unlike `ghref` (`:656–658`),
Enter in the name field submits nothing — there is no `<form>`. *Fix:* early-return
without hiding on failure; reword to "That paste looked empty"; add the same
Enter-to-add handler `ghref` has.

**FV3 · All pages · error notes are invisible to screen readers.**
Studio `#note` (`studio.html:239`), Vitals `#note` (`vitals.html:129`), and the
landing's `#rrhint` (`template.html:592`) carry every failure message yet have no
`role="status"`/`aria-live` (the landing toast `#copyhint` does, `:634`). A
screen-reader user who mistypes a repo ref gets silence. *Fix:* `role="status"` on
all three; on `rrin`, mirror `ghref`'s `aria-invalid` + `.is-error` treatment —
today its error state is color + hint text only.

**FV4 · Operator context · clear button — one click wipes four fields, no undo.**
`ctxclear` (`template.html:1366–1367`) instantly deletes stack/product/stage/notes.
The same footer holds a two-step armed reset (`:1370–1384`) and the Studio confirms
clear-all — this is the one destructive control with no gate, on the form whose
content users hand-typed. *Fix:* reuse the two-step arm pattern ("clear 4 saved
fields? click again"), or restore-on-next-click undo.

**FV5 · Vitals · loaded texts — no per-file remove, duplicates accumulate.**
`addText` (`vitals.html:296–298`) appends every drop/paste to `gp-vitals-texts`
forever; re-dropping the same HEALTH.md each week silently grows storage, and the
only recovery is nuke-all (`:320–323`, native `confirm`). The Studio already solved
this with removable per-report chips. *Fix:* dedupe identical texts on add; give
run chips (or file chips) an `×` like the Studio's repchips.

**FV6 · Studio · demo button — dead after success.**
`demobtn` (`studio.html:663–677`) sets "loaded ✓" and never re-enables. Remove all
reports afterwards and the demo can't be re-run without a page reload — a stuck
control in the first-visit path ACTIVATION.md leans on. *Fix:* re-enable with the
usual 1.6s `feedback()` reset.

**FV7 · Confirm-pattern inconsistency across destructive actions.**
Landing reset = two-step arm (`template.html:1370`); Studio clear-all = native
`confirm()` (`studio.html:679`); Vitals clear = native `confirm()` (`vitals.html:321`);
Studio `unsel` and landing `seqclear` = no gate at all (persisted state, moderate
rebuild cost). *Fix:* one pattern (the two-step arm — it's the house style and
isn't blockable like `confirm()`) for all five.

**FV8 · Studio/Vitals pasteboxes · 12px inputs zoom the viewport on iOS.**
`.pastebox input, textarea` are `font-size:12px` (`studio.html:84–87`,
`vitals.html:69`); iOS Safari force-zooms any focused input under 16px, jarring the
paste flow on mobile. Landing inputs (14–15px, `template.html:230, 238`) are close
but also under the threshold. *Fix:* ≥16px on mobile via a media query.

**FV9 · Studio GitHub loader — silent 12-file cap and merge semantics.**
`loadFromGitHub` slices to 12 report files without saying so (`studio.html:611`)
and loaded reports *merge into* whatever is already loaded, replacing same-named
ones. Fine defaults — but a one-line note ("first 12 shown") when the cap bites
would keep it honest. Low.

**FV10 · localStorage quota failures are swallowed everywhere.**
Every `save()` is `try{…}catch(e){}` (`studio.html:269`, `vitals.html:144`,
`template.html:781…`). Paste a very large report and it renders this session but
silently fails to persist — gone on reload with no warning. *Fix:* on catch in the
Studio/Vitals `save()`, surface the existing note ("Couldn't save on this device —
storage is full; this report won't survive a reload"). Low likelihood, confusing
when hit.

**FV11 · Search — graceful zero state, but typos strand the user.**
`"zzqxzz"` → correct empty state; but a plain typo (`"preformance"`) also yields
nothing: the scorer stems but doesn't fuzzy-match, so `closest()` offers no
"closest matches" row precisely when it's most needed. *Fix (optional):* a cheap
edit-distance-1 fallback in `closestScored` before giving up. Low — chips and the
finder are one click away.

**Positive findings worth protecting:** F2's picker is model field economy (three
optional questions, answer after one); F3 auto-fills the Operator-context stack
from analysis (infer-don't-ask, disclosed inline, never clobbers a saved value,
`template.html:1660–1669`); F6's content-hash check keys survive re-adds and
*explain themselves* when they can't (`studio.html:534–539`); every fetch button
disables while in flight — no double-submit anywhere; `gp-detail.js:115–121`
degrades a failed fetch-copy into an "open raw ↗" link instead of a dead button.

---

## 3 · Cuts — remove, defer, or infer

The catalog already runs near the theoretical minimum (zero required fields
site-wide), so the cut list is short and it's all *infer*:

1. **Infer the Studio paste name (F6/FV1)** — highest leverage: derive from the
   pasted markdown's first heading / ALL-CAPS token; keep the field as an
   override. Kills the silent-overwrite trap *and* one decision.
2. **Vitals name-lessness is already correct** — don't add a name field; add
   dedupe instead (FV5).
3. **Nothing to cut in Operator context** — all four fields optional, labeled,
   and one (`stack`) is already auto-inferred by F3. Keep.

---

## 4 · Priority — by drop-off risk on the highest-traffic surfaces

| # | Fix | Form | Why first |
|---|-----|------|-----------|
| 1 | FV1 suffix-or-infer duplicate paste names | Studio | silent data loss in the core "act on it" flow; user never learns it happened |
| 2 | FV2 don't hide the pastebox on failure + Enter-to-add + wording | Studio | error appears as the form vanishes — textbook lost-input feel |
| 3 | FV3 `role="status"` on the three note elements + `aria-invalid` on `rrin` | Studio, Vitals, landing | every error message on the site is currently unannounced |
| 4 | FV4 two-step arm on `ctxclear` | landing | only ungated destructive control over hand-typed input |
| 5 | FV5 dedupe + per-file remove | Vitals | weekly-loop surface accretes junk with no recovery short of nuke-all |
| 6 | FV6 re-enable demo button | Studio | stuck control on the first-visit demo path |
| 7 | FV7 unify confirm patterns · FV8 16px mobile inputs · FV9 cap note · FV10 quota note · FV11 fuzzy fallback | all | consistency & polish tier |

Items 1–2 and 4–6 are each a handful of lines in one file; item 3 is three
attribute additions plus one `setAttribute` pair.

---

*Report only — no code was changed.* **Which form fixes should I make first — the Studio paste-name overwrite and failure-handling pair (1–2), the screen-reader error announcements (3), or the destructive-action gates (4–7)?*
