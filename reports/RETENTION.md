# Retention & Lifecycle Audit

*Why would a user come back — and where does this product let them drift away?
Read-only pass over the client state (localStorage), the in-page nudges, the PWA,
and the analytics events.*

**Constraint that shapes everything:** no account, no backend, no email — by
design ("nothing leaves your machine"). So every retention lever is **client-side
(localStorage) or PWA**, and every nudge is **pull-only** — it can reward a return
but cannot *cause* one. Retention must be earned by a warm return and an honest,
opt-in reminder, never by holding an exit hostage (there is no exit to hold).

**Verdict:** the machinery is better than the category usually gets — the site
already ships **two smart, state-triggered, genuinely thankable nudges**
(`renderNudge()`, `template.html:961-979`) and persists real cross-visit state.
But the retention engine has a **starved fuel line**: both nudges fire only when
the run-tracker is populated, and the tracker is fed by a *manual* "mark run"
(`:613`) while the actual audit happens **off-site in the user's agent**. Users
who never mark a run get **no nudges ever** — the engine runs dark. On top of
that, retention is **unmeasurable** today (anonymous events only), and any
new device is a **cold start**.

> **Backlog reconciliation (2026-07-09).** Dispositions: **R1** (feed the run-tracker from copy) — **FIXED**: the post-copy hint carries a
> "✓ mark it run" button that records the run at the moment of action. **R4**
> (resurface Operator context) — **FIXED**: the context badge now reads "· tuned to
> <stack>". **R3** (export/import state) — **FIXED**:
> footer "export setup"/"import setup" round-trips all local state as a JSON file,
> no backend. **R2** (opt-in PWA reminder) — **FIXED**: a footer "🔔 remind me weekly" toggle
> requests Notification permission and registers a periodicSync for a weekly Vitals
> reminder (best-effort; installed-PWA/Chrome for background delivery). **R5**
> (retention instrumentation) — **FIXED**: an anonymous, non-PII cohort id +
> first-seen-week rides the already-anonymous analytics events, plus
> nudge_shown/clicked — gp-runs stays local. All five R-findings now addressed. These are product
> features, and R2/R3/R5 deliberately brush the "nothing leaves your machine"
> promise, which the report flags as needing the maintainer's call before building.
> Out of scope for a correctness-and-a11y backlog pass; captured here as the
> retention roadmap. See `FIXLOG.md`.

---

## 1 · Return-trip map

- **Natural rhythm — episodic, with one weekly anchor.** The job (audit a repo) is
  event-driven: new repo, pre-launch, post-refactor, agent onboarding. The single
  designed *recurring* ritual is **Weekly Vitals (`29`)** — "ten minutes, every
  week" (`README.md:86`; `playbooks.json:5` "Re-run every week"). Count retention
  from *this* rhythm, not from a daily-active fantasy.
- **What persists (localStorage, same device/browser only):**
  - `gp-runs` — which briefs marked run + timestamps (`:603`)
  - `gp-seq` — the custom conductor sequence, restored in the seqbar (`:620`)
  - `gp-ctx` — Operator context (stack/product/stage/notes), re-applied to every copy (`:669`)
  - `gp-studio-reports` / `gp-studio-checks` — loaded reports + checked findings (`studio.html:250-251`)
  - `gp-theme` — theme
- **The pull back:** (a) a new audit need; (b) the two in-page nudges when the user
  returns; (c) the Studio triage waiting where they left it; (d) the PWA icon, if
  installed. The strongest *designed* pull is the stale-Vitals nudge.
- **The biggest leak:** the nudges are **pull-only and starved** — they can't reach
  a user who left, and they don't fire at all unless runs were manually marked.
  The reason-to-return exists but rarely gets delivered.

---

## 2 · Findings (lens · location · why users drift · fix · effort)

Ranked by compounding value (earliest-in-lifecycle first).

### R1 — The retention engine is starved of trigger data *(lens 2: saved state as a hook · lens 5: habit)* — **HIGH · effort S**
- **Location:** `renderNudge()` (`:961-979`) keys entirely off `runs[...]`; runs are set only by the manual "mark run" button (`runLabel` `:612-616`, toggled at `:925-932`). The real run happens off-site in the agent.
- **Why users drift:** a user copies a brief, gets a report *in their repo*, and never returns to tap "mark run." `gp-runs` stays empty → **both** the roadmap nudge (`:966`) and the stale-Vitals nudge (`:973`) never fire → the product has no reason-to-return to show. The best machinery on the site is dark for most users.
- **Fix:** feed the tracker where the action already is — prompt "mark this run?" in the post-copy hint (ties to ACTIVATION A1), or optimistically record a run on `copy_prompt` (`:938`) with an easy undo. A populated tracker is the prerequisite for every other hook here.

### R2 — Excellent nudges, but pull-only — they can't reach a user who left *(lens 4: well-timed nudges · lens 7: win-back)* — **HIGH · effort M**
- **Location:** the nudges render in-page (`listEl.prepend`, `:970`/`:977`); the service worker (`SERVICE_WORKER` in `build.py`) has **no push, notification, or periodicSync** (confirmed absent). The PWA is installable/offline but never re-engages.
- **Why users drift:** the stale-Vitals message — "Weekly Vitals is stale — last run 8d ago" (`:976`) — is exactly the nudge that should arrive *while the user is away*, but it only shows if they happen to come back on their own. The one honest, no-backend win-back lever (an **opt-in** reminder from the installed PWA) is untapped.
- **Fix:** offer an explicit opt-in ("remind me weekly to run Vitals") that uses the Notification API / periodic background sync from the installed PWA — no account, no server, fully local and consented. This turns the existing designed ritual into a real habit loop. (See "The one hook," below.)

### R3 — A new device or cleared storage is a total cold start *(lens 3: the empty return)* — **MED · effort M · tension**
- **Location:** all state is `localStorage`, per-device/per-browser (`:603,620,669`; `studio.html:250-251`). No sync.
- **Why users drift:** a dev who audits from a laptop and returns on a work machine loses their runs, their **Operator context** (the tailoring that makes returning better than starting fresh), their saved sequence, and their Studio triage. The warm return silently becomes a cold one.
- **Fix (honest, within constraints):** offer a **manual export/import** of state (a small JSON "backup your setup" / "restore") — portable without a backend and without breaking "nothing leaves your machine." Don't add silent cloud sync; that would trade away the core promise. Flag the tradeoff rather than resolve it unilaterally.

### R4 — Operator context is a strong hook that never resurfaces *(lens 2: saved state as a hook)* — **MED · effort S**
- **Location:** `gp-ctx` (`:669`) is applied silently inside `withContext()` (`:672-680`) on copy; on return it's collapsed inside the `<details>` "aim the briefs at your repo" (`:467-477`), marked only by a small "· applied to every copy" (`:468`).
- **Why users drift:** the single richest reason a return beats a fresh start — "your briefs are already tailored to *your* stack" — is nearly invisible. A returning user doesn't feel the accrued value.
- **Fix:** on a return with saved context, surface it warmly ("Briefs tuned to *Next.js + Supabase* — change →") so the persisted value is felt, not hidden. Resurfacing value the user already created > inventing new notifications.

### R5 — Retention is unmeasurable today *(lens 8: is return even measured)* — **HIGH (for the operator) · effort M**
- **Location:** analytics are anonymous action events via Vercel Insights — `copy_prompt`, `copy_conductor`, `copy_install`, `copy_mcp`, `share_link`, `search_zero`, `copy_*_conductor` (`:745,923,938,1007,1024,1052,1093-1115`). No identity; `gp-runs` never leaves the device.
- **Why it matters:** you cannot distinguish a returning user from a new one, cannot draw a retention curve or cohort, and cannot tell whether the nudges (R1/R2) actually bring anyone back. Churn is invisible until traffic sags. (See "Instrumentation gaps.")
- **Fix:** add a non-PII anonymous client id + first-seen bucket to events, and instrument the nudges. Detailed below.

### What already retains — keep it
- **Two honest, well-timed nudges** (`:961-979`): the roadmap nudge resurfaces the
  user's *own reports* ("You've run N briefs — their reports are sitting in your
  repo… compose them: #28"), and the stale-Vitals nudge rebuilds a weekly habit.
  Both are state-tied, non-coercive, and exactly what this brief asks for — protect
  them; just *fuel* (R1) and *deliver* (R2) them.
- **Rich local persistence** — runs, sequence, context, and Studio triage all
  survive a same-device return (lens 3).
- **A designed weekly ritual** — Weekly Vitals gives retention a real cadence to
  build on (lens 1).
- **PWA foundation** — installable + offline via `sw.js`; the substrate for R2's
  opt-in reminder already exists.

---

## 3 · The one hook to build

**An opt-in weekly reminder for Weekly Vitals, delivered by the installed PWA.**

The argument: the product *already knows the right thing to say at the right time*
— "Weekly Vitals is stale — last run 8d ago" (`:976`). Its only failure is
**reach**: that message waits on a page the drifted user isn't visiting. Every
other lever here rewards a return; this is the sole honest lever that can *cause*
one without a backend or an email address. It builds on machinery that already
exists (the stale-Vitals nudge + the run-tracker + the service worker), it targets
the product's one genuine recurring rhythm, and it's something a user who opted in
would thank you for — a ten-minute health check on a repo they chose to watch, not
spam.

Sequence it right: **R1 first** (make runs real, so the tracker knows Vitals was
ever run), then this reminder on top. The teed-up second action is the report
itself → the Report Studio → the Fixer, closing the acquisition-to-habit loop.

---

## 4 · Instrumentation gaps (to see retention at all)

Today you can see *actions*, never *cohorts*. To make return visible without
breaking local-first (keep it aggregate, non-PII, ideally documented/opt-in):

- **Anonymous client id + first-seen week** (localStorage, not PII) attached to
  events, so returning vs new and week-N-return cohorts become visible.
- **Nudge instrumentation:** emit `nudge_shown` / `nudge_clicked` for the roadmap
  and Vitals nudges — the only way to know if R1/R2 actually retain.
- **Run signal:** emit `mark_run` (and, if R1 auto-infers from copy, `run_inferred`)
  to connect activation → repeat use.
- **PWA lifecycle:** `pwa_installed`, `reminder_opt_in`, `reminder_fired`,
  `reminder_return` — to measure the one hook end to end.
- **Cohort readout:** first-visit week → subsequent return events; approximable
  entirely client-side from the anonymous id + first-seen stamp.
- **Tension to flag, not silently cross:** any of this leaves the device, which
  brushes against "nothing leaves your machine." Keep it anonymous and aggregate,
  document it, and prefer opt-in — don't trade the core promise for a dashboard.

---

## Report only — which fixes do you want me to make?

This was a read-only pass; nothing was changed. The highest-leverage, in-lifecycle
fix is **R1** (feed the run-tracker where the action is) — it's small, front-end
only, and it lights up the good nudges that already exist; it also dovetails with
ACTIVATION A1. **R4** (resurface Operator context) is cheap. **R2** (opt-in PWA
reminder) is the biggest reason-to-return but a larger build. **R3** (export/import)
and **R5** (retention instrumentation) both touch the local-first promise — I'd
want your call on the tradeoff before touching them.

Tell me which fixes to implement (any subset), and your stance on the local-first
tradeoffs in R3/R5. I'll make only the changes you pick.
