# Activation & First-Win Audit

**Date:** 2026-07-09 · read-only pass (re-run; previous ACTIVATION.md was ~4 months old)

*The first session, from cold arrival to first real win. No signup exists here, so
"empty account" = a first-time visitor with an un-audited repo, and the **first win
= a real report file (e.g. `BUGS.md`) appearing at their repo root with true
findings.** Everything between arrival and that file is tax. Structure end-to-end
is FUNNEL.md's beat; persuasion is CRO.md's — this pass is the first session
itself: landing → pick → copy → run → report, plus Studio, plugin, and MCP first-runs.*

---

## 0 · What changed since the last run

The previous report's backlog (A1–A5) was dispositioned as **fixed**, and most of it
genuinely shipped — the catalog also grew 135 → **141 briefs** (21 families,
35 playbooks), and two whole new first-run surfaces exist (the Claude Code
**plugin** and **MCP prompts**). Verified against source:

| Old finding | Claimed | Verified today |
|---|---|---|
| A1 — guided hint on copy | FIXED | **Partial.** `showCopyHint()` exists (template.html:895) and fires from the hero quickstart (:1690), the Triage callout (:1358), the 3-question picker (:1596), and every `/b/<id>` page (gp-detail.js:97). **It never fires from the catalog card's own Copy button** (`btn.onclick`, template.html:1133–1144) — the exact location the original A1 named. Git history confirms it was never wired there (checked f03bc06 → 4b534a6 → f04ba76 → HEAD). |
| A2 — a "start here" default | FIXED | Yes — finder starter "New here? Start with the Day-1 playbook →" (:1526–1527) plus the "Start here" badge on way 01 (:651). |
| A3 — hero quickstart | FIXED | Yes — the "New here? Copy your first brief" pill (:503, JS :1679–1692), defaulting to 01 · Bug Hunt. But it has a silent-failure bug (AN2 below). |
| A4 — real report near the finder | FIXED | Yes — "See a real report one wrote →" in the catalog lead (:580). |
| A5 — tee up step 2 in the hint | FIXED | On the landing page only. The detail-page rebuild of the hint (gp-detail.js:69–70) **drops the Report Studio tee-up**. |

Also new since last run, and good for the first session: ranked "best matches"
search with a closest-matches zero state (:1224–1266), the run-replay walk-through
of a real run (:679–690), the Studio screenshot (:704–707), and the Studio's
demo/paste/GitHub loaders. The remaining activation debt is concentrated in one
place: **the majority copy path — browsing the catalog and tapping Copy on a card —
is the one path that still goes silent at the handoff.**

---

## 1 · First-session walk (screen by screen to the first win)

**Path A — the guided path (hero quickstart).**
1. Land on the hero. "no signup · nothing leaves your machine" is stated up front (:502). *Zero setup tax.*
2. Tap **"New here? Copy your first brief"** (:503) → brief 01 on the clipboard, toast names the whole workflow: *paste into Claude Code/Cursor inside your repo → it writes `BUGS.md` → then drop it in the Report Studio* (:895–907). **This is model activation copy** — action, expected artifact, and second step in one breath. *(But see AN2: the toast fires even if the clipboard write failed.)*
3. Off-site: open agent in the repo, paste, wait ~10–20 min. **First win: `BUGS.md` lands.**
On-site cost: **1 tap, 0 fields, 0 decisions.** At the floor.

**Path B — the browse path (the majority route; "Browse the catalog" is the primary CTA, :499).**
1. Scroll or jump to the catalog. Greeted by a *guided* launcher, not a blank canvas: Day-1 starter, 4 goal pills, 21 family questions with example brief + output each (`buildFinder()`, :1523–1549). *Strength retained.*
2. Choose among 141 briefs mediated by six chooser mechanisms (starter, goals, picker, repo-recommend, Triage nudge, search/chips). FUNNEL.md §1 already ranks this "menu of menus"; from the first-session seat the starter does give one unmistakable newcomer door, so the decision is survivable. *Stall: moderate.*
3. Tap **Copy** on a card → button flips to "Copied ✓" (:865–870), the run auto-marks (:1136–1143) — **and nothing tells them what to do next.** No toast, no output reminder beyond the small `→ BUGS.md` chip (:1102). The newcomer's thought: *"Copied… into what, exactly?"* The workflow prose lives one scroll away (:580, :653) — not at the click. *Stall: the unguided handoff, again — the single most expensive moment of the product, now fixed on four minor paths and still open on the main one.*
4. Same off-site tail → first win.

**Path C — playbook / "running start"** (where the A2 starter actually routes): the Day-1 filter view offers "copy conductor" (:1279–1281; storefront `cc` :972–976; family "run all N" :1302–1309; custom `seqcopy` :1461). Every one of these confirms with a bare **"✓"** — no hint, ever, despite the conductor being the *newcomer-recommended* artifact and the least self-explanatory one (it runs 4 briefs and writes 4 files).

**Path D — side doors (`/b/<id>`, search/shared-link entries).** Excellent first-run pages: hero Copy with the hint, "How to run it" section, three ways in, full verbatim brief, real-report link (b/01.html). The hint is the weaker variant (no Studio tee-up, gp-detail.js:69–70).

**Path E — plugin / installer / MCP.**
- The curl installer's post-install message is the best "inspiring next step" in the product: it prints four named starter commands and the update/uninstall story (install:53–60).
- The plugin path has **no equivalent first-run moment**: after `/plugin install goal@goal-prompts`, 141 `/goal:<slug>` commands appear with no "try this first" anywhere — plugin.json's description doesn't name one (plugin/.claude-plugin/plugin.json). And reaching that point crosses the **two-command trap** (site copies only command 1 of 2; the install command is 12px fine print, template.html:661) — CRO NF3 / FUNNEL §1; endorsed, not re-counted here.
- MCP first-run is genuinely newcomer-shaped: `suggest_briefs` takes a plain-words goal, and every brief lands in the client's prompt picker (mcp/server.cjs:51–112).

**Path F — Studio first-run.** The best empty state in the product: drop zone with instructions, a **"try it on this repo's own reports"** demo button (studio.html:226, :663–677), honest empty text (:243), and a post-Fixer hint that names `FIXLOG.md` and closes the loop (:688–698). Sample data before any work — textbook.

---

## 2 · Time-to-first-win: today vs achievable minimum

| Path | On-site actions today | Handoff guidance | Minimum |
|---|---|---|---|
| Hero quickstart | 1 tap, 0 decisions | full hint (unless clipboard silently failed — AN2) | **at floor** — protect it |
| Browse + card Copy | ~3–4 taps + 1 decision-of-141 | **none** (AN1) | same taps + the same hint the other paths already have |
| Playbook conductor | 2 taps (starter → copy conductor) | **none** (AN4) | + one hint naming stage 1's output |
| Plugin | 2 commands, one undiscoverable | terminal is silent until `/goal:` works | 1 visible two-line copy (CRO NF3) + a named first command (AN5) |
| Studio | 1 tap (demo) | complete | at floor |
| Mobile visitor | no path to the win | — | out of scope here; FUNNEL §3 owns it |

The off-site run (~10–20 min) is irreducible — it *is* the product. The avoidable
tax left is no longer "no guidance exists" (last run's problem) but **guidance
inconsistently applied: the most-used path and the newcomer-recommended path are
the two that got none.**

---

## 3 · Findings (lens · location · what a newcomer feels · fix · effort)

Ranked by distance to the first win.

### AN1 — The main card Copy is the last unguided handoff *(lens 3: guided first action · lens 2: time-to-first-win)* — **HIGH · effort S**
- **Location:** `btn.onclick`, template.html:1133–1144 — copies, flips to "Copied ✓", auto-marks the run, returns. `showCopyHint` (:895) is called from every copy affordance *except this one* (verified across git history; never wired). FUNNEL.md's stage table ("Copy (1 tap) → toast tells the user to paste") over-credits this path — correct the record.
- **Newcomer feels:** *"Copied ✓ … now what?"* The exact stall the old A1 described, still live on the highest-traffic button; the fix shipped everywhere but where the finding pointed.
- **Fix:** add `showCopyHint(p.output, p.id)` inside `btn.onclick` — one line. Since this path auto-marks the run, either suppress the hint's "✓ mark it run" button when `runs[id]` is already set (mirror gp-detail.js:73's `hasRun` check) or adopt FUNNEL's un-fake-the-mark fix and let the hint's button be the honest confirmation.

### AN2 — The quickstart pill claims success even when the copy failed *(lens 8: recover from a false start · lens 7: reassurance)* — **MED-HIGH · effort S**
- **Location:** template.html:1685–1691 — `navigator.clipboard.writeText(txt).catch(function(){})` swallows failure, then `showCopyHint(...)` runs unconditionally; the pill itself never changes state (no `feedback()`, no "copy failed").
- **Newcomer feels:** the guided path's *one* action silently no-ops (clipboard permission denied, non-secure context): the toast says "Paste into Claude Code…", they paste **nothing**, and their very first impression is "it doesn't work."
- **Fix:** route the pill through the existing `copyText()` (which has the textarea fallback and the "copy failed" state) and call `showCopyHint` only in the success callback.

### AN3 — Two "New here?" doors point at two different first wins *(lens 3: guided first action)* — **MED · effort S (a decision, mostly)*
- **Location:** hero pill → copies brief **01** solo (:1683); finder starter → filters to the **Day-1 playbook**, 4 briefs + a conductor (:1526–1527).
- **Newcomer feels:** the site says "new? do this" twice and the two answers differ in size by 4×. Either is defensible; both at once dilutes the guidance the product worked to add.
- **Fix:** pick one canonical first win — the single brief is the shorter path to a report (the brief's own rule: shorter path beats longer tour) — and make Day-1 the *teed-up second step* (the quickstart hint can end "…then run the rest of Day-1"). Keep the starter, but as "then:" not a rival "start:".

### AN4 — Conductor copies get "✓" and no handoff, on the path the starter recommends *(lens 3 · lens 6: inspiring next step)* — **MED · effort S**
- **Location:** storefront `cc` (:972–976), playbook-filter bar (:1279–1281), family "run all N" (:1302–1309), custom `seqcopy` (:1461–1466) — all `copyText(..., "✓ …")`, no hint.
- **Newcomer feels:** they took the recommended running start and got *less* guidance than a single-brief copy — a conductor is the artifact most in need of "paste it in your agent; it runs N stages and writes N files."
- **Fix:** a conductor variant of `showCopyHint` — "Paste into your agent inside the repo — it runs N briefs and writes `X.md`, `Y.md`… (~15 min each)."

### AN5 — The plugin's first run lands in 141 commands with no named first command *(lens 3 · lens 6)* — **MED · effort S**
- **Location:** plugin/.claude-plugin/plugin.json + .claude-plugin/marketplace.json descriptions; contrast install:53–60, where the curl path prints "In Claude Code, try: /goal-bug-hunt · /goal-audit-triage · /goal-roadmap-synthesis".
- **Newcomer feels:** installed the "primary path" (README:23) and now faces the same 141-way choice, inside a slash-command picker with no finder to help.
- **Fix:** name the starters in the plugin/marketplace descriptions ("start with `/goal:audit-triage` or `/goal:bug-hunt`"); they surface at install/browse time. Pairs with the two-command trap fix (CRO NF3 / FUNNEL — that one gates *reaching* this moment at all).

### AN6 — Detail pages get the hint minus the momentum *(lens 6: inspiring next step)* — **MED-LOW · effort S**
- **Location:** gp-detail.js:69–70 — "…it writes `BUGS.md` at the root (or in reports/)." Full stop. The landing version (template.html:899–900) adds "then drop it in the Report Studio."
- **Newcomer feels:** nothing wrong — they just never learn the loop. And side-door visitors (SEO, shared links) are the *coldest* cohort, the ones who most need step 2 named. (Adjacent to RETENTION R7's "detail pages are a parallel cold world".)
- **Fix:** add the Studio link to `showHint()` in gp-detail.js — the two hint builders should say the same thing.

### AN7 — Nothing at the copy moment says what the 15-minute wait looks like *(lens 7: progress & reassurance)* — **LOW-MED · effort S**
- **Location:** the run-replay figure (:679–690) teaches exactly this — four ✓ phases ending in a report line — but sits in Proof, far below the catalog, and isn't linked from any hint.
- **Newcomer feels:** mid-run doubt: *"is it doing anything? is this normal?"* — the product's one unavoidable dark stretch, with an existing reassurance asset unused at the moment it's needed.
- **Fix:** FUNNEL already proposes "what happens next →" in the post-copy toast (linking the run-replay anchor or `/examples/`). Endorsed as-is; zero new content.

### AN8 — "copy failed" is a dead end on cards *(lens 8: recover from a false start)* — **LOW · effort S**
- **Location:** template.html:930 — the fallback path's failure leaves button text "copy failed" and nothing else; gp-detail.js:115–121 shows the better pattern (degrade to an "open raw ↗" link).
- **Fix:** on failure, offer `/raw/<id>.md` — same artifact, one more click. (Also flagged in FUNNEL §1c.)

### What already activates well — keep it
- **The hero quickstart + hint** is the complete activation move: one tap, no choice, the workflow, the artifact, and step 2 all named (:503, :895–907) — modulo AN2.
- **The finder is a guided launcher**, and the Day-1 starter gives cold newcomers one door (:1526).
- **Studio's first-run is exemplary** — demo button, honest empty state, saved progress, and a closing hint that names `FIXLOG.md` (studio.html:226, :243, :688–698). Sample data beats blank canvas, and this page proves it.
- **Detail pages are self-sufficient first-run surfaces** — copy with hint, "How to run it," the verbatim brief, and a real report link (b/01.html).
- **The installer's outro** (install:53–60) is the best post-win "try these next" in the product — the pattern AN5 wants copied.
- **False starts stay cheap** — read-only briefs, ask-first gates, zero-result search recovers with ranked closest matches (:1246–1261), two-step-confirm tracker reset (:1370), export/import backup (:1386).
- **Near-zero setup tax** — nothing demanded up front; Operator context is optional and even auto-filled by repo-recommend (:1662–1665).

---

## 4 · The one change

**Finish A1 where it was originally aimed: wire the guided hint into the catalog
card's Copy button** (AN1 — one line in `btn.onclick`, template.html:1133), with the
markrun state made honest, and give the conductor buttons their own variant (AN4).
This closes the last silent handoffs on the two paths newcomers actually take —
the browse-and-copy majority and the starter-recommended playbook — using a
component that already exists, is already tested by four other call sites, and
already tees up the second step (the Report Studio) so the first win rolls into
the loop instead of ending at "done." The second step it tees up: `BUGS.md` →
Studio → a targeted 47 · Fixer run → the first *commit*, which is the win that
builds the habit.

---

## Report only — which fixes do you want me to make?

Nothing was changed in this pass. **AN1** (hint on card Copy) and **AN2**
(quickstart false-success) are the highest-leverage and both are small, safe,
front-end-only; **AN4/AN6** are the same component reused; **AN3** needs a
one-line decision (which "new here" door is canonical); **AN5** is description
text; **AN7/AN8** ride along with FUNNEL's toast work. Tell me which to
implement — any subset — and for AN3, whether the canonical first win is the
single starter brief or the Day-1 playbook.
