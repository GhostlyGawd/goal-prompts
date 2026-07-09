# Activation & First-Win Audit

*The first session, from cold arrival to first real win — and whether it leaves a
newcomer able and inspired to do the next thing. Read-only pass over the catalog
(`template.html`), the Report Studio (`studio.html`), and the seed/sample logic.*

**Reframing for a no-account product:** there is no signup here, so "empty
account" = **a first-time visitor with an un-audited repo**, and the **first win
= a real report file (e.g. `BUGS.md`) appears at their repo root with true
findings about their code.** Everything between arrival and that file is tax.

**Verdict:** the on-site path is short and low-tax, the catalog opens on a
*guided* launcher (not a blank canvas), sample data is excellent, and false
starts cost nothing. The activation weakness is the **handoff**: the first win
happens *off-site, in the user's agent*, and the product goes silent at the exact
moment it should hand the newcomer their next action. After "Copied ✓," nothing
says *"now paste this into Claude Code or Cursor at your repo root — it will write
`BUGS.md`."* Combined with no recommended "first brief," a cold newcomer must
**choose from 129 briefs and then guess the workflow** — the two costs standing
between them and the win.

> **Backlog reconciliation (2026-07-09).** Dispositions: **A1–A5** (next-step hint
> on copy; a recommended "start here" brief; a hero quickstart; a real report
> excerpt near the finder; post-win momentum) — **A1 is now FIXED** (the copy→paste next-step hint shipped, naming the brief's output file); **A2 is now FIXED** (a "New here? Start with the Day-1 playbook →" starter leads the finder); **A3–A5 DEFERRED**. These are UX/product
> additions; A2 needs a decision on *which* default starter and A3 is explicitly an
> A/B hypothesis, not a blind change. (The choice-overload framing cites 129
> briefs; the catalog is now 135.) Captured as the activation roadmap. See
> `FIXLOG.md`.

---

## 1 · First-session walk (screen by screen to the first win)

**Path traced: copy-paste (the zero-install default).** Install (`curl | sh`) and
MCP are alternatives; both add setup tax and are covered as variants.

1. **Land on the hero** (`:379-398`). Newcomer thought: *"What is this — and what do I do?"* (Comprehension gaps in COMPREHENSION.md.) No "new here, start here" cue. → *tax: orientation.*
2. **Scroll through Problem → How → Payoff** (`:401-456`). Good belief-building, but ~4 screens before anything is doable. → *tax: distance to first action (CRO F7).*
3. **Reach the catalog** (`:460-489`). The **finder** (`buildFinder()`) greets with "start with a goal" (4 playbooks) + 17 family questions. **Strength — a guided launcher, not a dead blank state.** But: which *one* brief should a first-timer run? No default. → *stall: choice overload across 129 briefs.*
4. **Pick a brief, tap Copy** (`.copy`, `:252`). Button flips to **"Copied ✓"** (`:692`) for 1.6s — and that's all. **No instruction on what to do with the copied text.** → *stall: the unguided handoff — the single most expensive moment.*
5. **Leave the site, open their agent, paste** (off-site). The newcomer must already know: paste into Claude Code/Cursor, inside the repo, and wait. Prose says so at `:463` and `:535` — but not where they just clicked.
6. **Agent runs the 4-phase audit → writes the report.** **First win** — `BUGS.md` appears with real findings. The card did show the expected output ("→ BUGS.md", `.out` `:256`), so the newcomer at least knows the filename to look for. Good.

**Where a newcomer stalls:** step 3 (which brief?) and step 4 (now what?). Both
are *before* the win, so both are maximally expensive.

---

## 2 · Time-to-first-win: today vs achievable minimum

| | Today (copy path) | Achievable minimum |
|---|---|---|
| On-site actions | scroll ~4 sections → open finder → choose family/goal → scan cards → Copy (~3-4 clicks + a choice) | land → "New? copy this one" → Copy (1 click, no choice) |
| Handoff | **unguided** — newcomer infers "paste in agent" | **named** — "paste into your agent at repo root → writes BUGS.md" |
| Choosing | from 129 briefs / 17 families / 32 playbooks | one sensible default (or the Day-1 playbook) |
| Off-site run | 4-phase audit in the agent (unavoidable, and the point) | same |

The product can't shrink the off-site run (that's the value). It *can* remove the
two avoidable costs: **the choice** and **the guessed handoff.**

---

## 3 · Findings (lens · location · what a newcomer feels · fix · effort)

Ranked by distance to the first win.

### A1 — The copy → paste → report handoff is unguided *(lens 3: guided first action · lens 2: time-to-first-win)* — **HIGH · effort S**
- **Location:** the Copy button feedback, `template.html:692` / `:938` — flips to "Copied ✓" and reverts; no next step. The workflow instruction lives only as prose at `:463` and `:535`, not at the click.
- **Newcomer feels:** *"Okay, it's copied… now what? Where does this go?"* If they don't already know the agent workflow, momentum dies holding a clipboard.
- **Fix:** on copy, show the next action inline — a one-time hint/toast: **"Paste into Claude Code or Cursor inside your repo — it'll write `<output>` at the root."** Use the brief's own `output` field so it's specific. Cheapest, highest-leverage activation fix on the site.

### A2 — No recommended "first brief" → choice overload at the threshold *(lens 3: guided first action)* — **MED-HIGH · effort S**
- **Location:** catalog `:460-489`; confirmed absence of any "new here / start here / try this first" affordance.
- **Newcomer feels:** *"129 briefs, 17 families, 32 playbooks — where do I even start?"* Choice right before the first win is the costliest kind.
- **Fix:** offer a single obvious starter — a "New here? Run this first" card defaulting to a broadly-useful brief (e.g. `01 · Bug Hunt`) or the **Day-1 playbook** (which also pre-sequences steps 2-4). The finder's "start with a goal" is close; make one path unmistakably the newcomer's. (Ties to CRO F2.)

### A3 — The first doable action sits below ~4 value screens *(lens 2: time-to-first-win)* — **MED · effort M · test**
- **Location:** first `.copy` only appears in the catalog (`:488`), after Problem/How/Payoff.
- **Newcomer feels:** an action-ready visitor scrolls a long way before they can *do* anything.
- **Fix (hypothesis):** a compact quickstart near the hero ("New? Copy one brief, paste it in your agent") that jumps to the default starter. A/B it against the value-first flow. (Shared with CRO F7.)

### A4 — The finished outcome isn't shown at the deciding moment *(lens 4: seed & sample data)* — **MED · effort S**
- **Location:** at the catalog, the only report visual is the *schematic* mock in Payoff (`:446-454`, `aria-hidden`); the real reports are on a separate page (`/examples/`).
- **Newcomer feels:** *"What will I actually get?"* — decided without seeing a real finished report inline.
- **Fix:** surface one real example near the finder ("see a real report this wrote →" / an inline excerpt). Sample beats schematic. (Ties to SHOWCASE F4.)

### A5 — Momentum after the first win relies on content, not capture *(lens 6: the inspiring next step)* — **MED · partly by design · effort S-M**
- **Location:** the win is off-site; with no account/email, the product can't re-engage directly. Next-step scaffolding exists but is diffuse — playbooks (`:493-516`), each brief "ends by asking," `28 · Roadmap Synthesis` (referenced in conductors), and the Studio "loop" (`studio.html:239`).
- **Newcomer feels:** after `BUGS.md` lands — *"Nice… is that it?"* unless they already knew the loop.
- **Fix:** tee up step 2 *inside* the A1 hint ("then drop `BUGS.md` into the Report Studio, or run the Day-1 playbook for the full sweep") and lean on the two capture mechanics that already exist: the **PWA install** (manifest + `sw.js`) and the **run-tracker** ("✓ run · Nd ago", `runLabel` `:612`; "N run here" `:777`). Deepened in RETENTION.md.

### What already activates well — keep it
- **The finder is a guided launcher** (`buildFinder()`), not an empty canvas (lens 1, 3).
- **Sample data is excellent** — `/examples/` real reports + the Studio's "try it on this repo's own reports" demo (`studio.html:210`) let a newcomer see the product work before doing any work (lens 4).
- **Near-zero setup tax** on the default path — "Nothing to install" (`:535`); nothing is demanded up front (lens 5).
- **False starts are free and safe** — copy another brief at no cost; briefs are read-only and ask-first; run-tracker has a reset (`:585`) (lens 8).
- **Cross-visit progress exists** — the run-tracker doubles as a light "you've done N" signal (lens 7).

---

## 4 · The one change

**Add a guided first-win quickstart** that collapses the two avoidable costs into
one move:

1. **Default the choice** — a "New here? Run this first" starter (a single
   broadly-useful brief, or the Day-1 playbook) so a cold newcomer doesn't pick
   from 129. *(A2)*
2. **Name the handoff on copy** — replace the bare "Copied ✓" with the exact next
   action and expected file: *"Paste into Claude Code/Cursor at your repo root —
   it'll write `BUGS.md`."* *(A1)*
3. **Tee up step 2** — same hint ends with *"then drop the report into the Report
   Studio, or run the Day-1 playbook for the full sweep."* *(A5)*

This attacks choice overload *and* the unguided handoff — the two stalls that sit
directly between a newcomer and the first win — and it breaks the product's
silence at the one off-site moment that decides activation. The teed-up second
step turns a single win into the start of the loop.

---

## Report only — which fixes do you want me to make?

This was a read-only pass; nothing was changed. **A1 (next-step on copy)** and
**A2 (a "start here" default)** are the highest-leverage and both are small,
safe, front-end-only changes that also satisfy CRO F2 and feed RETENTION. **A4**
(real example near the finder) is cheap too. **A3** is a layout hypothesis worth
testing rather than shipping blind.

Tell me which fixes to implement (any subset), and — for A2 — whether the default
starter should be a single brief (which one) or the Day-1 playbook. I'll make only
the changes you pick.
