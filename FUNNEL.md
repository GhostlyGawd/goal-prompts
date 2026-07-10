# FUNNEL.md — Funnel Friction Audit

**Date:** 2026-07-09
**Auditor:** funnel-friction brief, read-only pass
**Prior run:** none — no previous `FUNNEL.md` existed; this is the first funnel audit.

---

## 0 · The funnel, reconstructed

This product has **no signup, no account, no backend**. The funnel it actually has:

```
Entry            →  Choose           →  Copy (handoff)     →  First value        →  Habit
landing / b/<id>    catalog, 6         clipboard leaves      report file lands     run tracker, nudges,
/ p/<key> / README  chooser surfaces   the site              in the user's repo    Studio, reminder
```

The "aha" is **a report file appearing at the user's repo root** — and it happens
*off-product*, inside the user's own coding agent, ~10–20 minutes after the last
click the site ever sees. Site-side the path is astonishingly short (one tap can
put a runnable brief on the clipboard); the funnel's risk is concentrated in the
**handoff** and in the fact that everything after the copy is invisible.

### Counted path — fastest route (dev with an agent already installed)

| # | User action | Surface | Cost |
|---|------------|---------|------|
| 1 | Load `goal-prompts.vercel.app` | landing | 1 wait — index.html is 580 KB raw / **~165 KB gzipped**, single request, + 140 KB fonts |
| 2 | Tap the "New here? Copy your first brief" pill | hero (`#quickstart`, template.html:503) | 1 tap → brief 01 on clipboard, toast explains next step |
| 3 | Switch to agent inside the target repo | *off-site* | 1 context switch |
| 4 | Paste + Enter | *off-site* | 1 action |
| 5 | Wait for the agent run | *off-site* | ~10–20 min |
| 6 | Open `BUGS.md` | *off-site* | first value |

**In-site: 1 screen, 1 tap, 0 fields, 0 decisions** (the pill decides for you).
Total user actions to value: **3 + one long wait**. That is already near the floor.

### Counted path — typical browse route

1 load → 1 click ("Browse the catalog", anchor jump) → **1 big decision** (141 briefs,
21 families, 35 playbooks, six competing chooser mechanisms) → optional 1 click
(quick view) → 1 tap (Copy) → same off-site tail. **~4 taps + 1 heavy decision.**

### Counted path — the README's "primary path" (plugin)

1 tap (copy `/plugin marketplace add GhostlyGawd/goal-prompts`) → paste in Claude
Code → **a second command** (`/plugin install goal@goal-prompts`) that the site's
copy button does *not* copy and that lives in 12px fine print (template.html:661)
→ type `/goal:bug-hunt`. **4 actions, one of them easy to never discover.**

---

## 1 · Funnel map

| Stage | Steps today | Friction found | Proposed fix | Expected effect | Effort |
|---|---|---|---|---|---|
| **Entry** | 1 load, value prop + CTA above fold | Value prop is clear and CTA ("Browse the catalog") matches what happens. Weight: ~165 KB gz HTML because all 141 brief bodies ship inline (`__PROMPTS_JSON__`) — a deliberate offline/search tradeoff, acceptable on one request. Real gap: `/b/<id>` and `/p/<key>` pages — the SEO/shared-link **side doors** — carry no analytics at all, so entry mix is unknown (see §4). | Leave the page as is; instrument the side doors. | Know where users actually enter | S |
| **Entry (hero)** | 3 CTAs + nav "Get started" + JS-injected quickstart pill | The single best newcomer action (quickstart pill — 1 tap to a runnable brief) is visually **third**, `hidden` until JS runs, styled as a dashed afterthought under two bigger buttons. | Promote the quickstart pill to a peer of the primary CTA (or make "Browse the catalog" secondary); keep it one tap. | More users take the 1-tap path instead of entering the 141-brief decision field | S |
| **Signup** | **0 screens, 0 fields, 0 walls** | None. "no signup · nothing leaves your machine" is stated in the hero micro-line and is true. The optional "aim the briefs at your repo" box (4 fields) is correctly optional and auto-filled by repo-recommend. | Nothing. Do not add capture here. | — | — |
| **Choose** (pre-activation) | 1 decision among 141 briefs, mediated by **six** parallel choosers: search, "start with a goal" finder, 3-question picker, repo-recommend, the 46-Triage nudge, family chips | Choice overload at the exact moment of highest intent. Each chooser is individually good; together they are a menu of menus. The picker and repo-recommend are both collapsed `<details>` — two more "decide how to decide" steps. | Collapse to a hierarchy: quickstart pill (no choice) → "recommend for my repo" (one field) → search/browse for the rest. Fold the 3-question picker into repo-recommend's fallback rather than a sibling. Removes a chooser; adds nothing. | Fewer stalls at the catalog; higher copy rate per catalog visit | M |
| **Activation — copy handoff** | Copy (1 tap) → toast tells the user to paste "inside your repo" | **(a) Plugin two-command trap:** `#copyinstall` copies only the marketplace-add line; the install command is fine print. A user who runs command 1 and stops has installed nothing and gets no error — the canonical silent stall. **(b) Mobile dead-end:** on a phone the clipboard lands on the wrong device; the toast still says "Paste into Claude Code…" with no bridge (no "email/QR/link to yourself"; the raw URL `/raw/01.md` is copyable but never offered at this moment). **(c) `copy failed`** state on catalog cards leaves button text only — no fallback link to `/raw/<id>.md` (detail pages have that fallback for *fetch* failures, template card copies don't). | (a) Make the copy button copy **both lines** (Claude Code executes them sequentially when pasted, and even as two pastes the user now *has* both). (b) On coarse-pointer/small viewports, swap the post-copy toast for "on your phone? copy this URL instead → `/raw/<id>.md`" — one existing artifact, zero new steps. (c) On copy failure, replace the button with a link to `/raw/<id>.md`, same pattern as gp-detail.js:116–121. | (a) removes the highest-severity silent stall on the "primary path"; (b) rescues the mobile share-traffic cohort; (c) closes a dead end | S / S / S |
| **Activation — first run** | Paste → ~10–20 min agent wait → report file | The wait is inherent (it's the product). But the site's only guidance is a 9-second toast, and if the run fails or the report never appears, the product never knows and offers nothing. There is no "what a run looks like / what can go wrong" one-pager linked at the moment of copy — the run-replay figure exists but lives far down the page. | Link "what happens next →" (the run-replay anchor or `/examples/`) inside the post-copy toast. Zero new steps, reuses existing content. | Fewer abandoned first runs; user knows the 15-min wait is normal | S |
| **Habit** | Run tracker (auto-marked), roadmap nudge at ≥5 runs, stale-Vitals nudge at >7 d, welcome-back Operator-context banner, custom sequences, Studio checklist state, export/import, opt-in weekly reminder | **(a) Runs are fabricated:** copying auto-marks a brief "run" (template.html:1136–1143), so the tracker, both nudges, and the `mark_run` event all fire off *copies that may never have been pasted* — the habit mechanics are keyed to a fake signal (the toast's "✓ mark it run" then shows for an already-marked brief). **(b)** The only pull mechanism — the weekly Vitals reminder — is a 🔔 fine-print button in the **footer** (template.html:760), Chromium-only for true background push. **(c)** All state is device-bound localStorage; work-laptop vs home = two strangers (export/import exists but is manual, also footer-buried). | (a) Stop auto-marking on copy; let the toast's existing "✓ mark it run" button be the (honest) confirmation — this *removes* code and un-fakes three downstream mechanics. (b) Offer the reminder toggle once, inline, after the first stale-Vitals nudge renders — the one moment it's relevant. (c) Accept device-bound as the privacy stance; surface "export setup" in the welcome-back banner instead of the footer. | Habit loop keyed to real runs; the one retention lever becomes findable | S / S / S |
| **Studio (act loop)** | Drop files (1 drag) or 1 tap on "try it on this repo's own reports" → check findings → 1 tap "Copy Fixer prompt" | Genuinely good: sample-data demo button, paste and GitHub loaders, saved progress, selection permalinks. Minor: a first-time visitor landing on `/studio` with no reports sees the demo button third in a row of four equal-weight buttons. | Give the demo button primary styling when zero reports are loaded. | Faster Studio aha for cold visitors | S |
| **Silent stalls** (cross-stage) | — | Ranked: 1. plugin second-command trap · 2. mobile copy dead-end · 3. no-agent visitor (page assumes a coding agent exists; no "don't have one?" line anywhere) · 4. post-run failure invisible · 5. `copy failed` dead end. | Fixes above; for (3) one line in "Three ways in": "New to coding agents? Start with Claude Code →". | — | S |
| **Instrumentation** | See §4 | The two transitions that define this funnel — **copy → real run** and **detail-page entry → copy** — are respectively falsified and unmeasured. | §4 event list; flip on `/raw/*` log counting per `docs/usage-metrics.md` Option 1 (zero code). | The funnel becomes observable | S–M |

---

## 2 · The biggest leak

**The handoff — and the fact that it is both unmeasured and actively falsified.**
Everything before the clipboard is excellent: zero fields, one tap to a runnable
brief, honest copy, sample reports one click away. But the product's aha happens
minutes later in someone else's terminal, and the site's knowledge of that
transition is *worse than nothing*: copying a brief optimistically marks it "run"
(template.html:1136), fires `mark_run {from:"copy"}`, feeds the run counter, and
arms the ≥5-runs roadmap nudge — so a user who copied five briefs onto a phone
clipboard and never ran one looks identical to the ideal activated user, both in
analytics and in the UI's own habit mechanics. Meanwhile the honest usage signal
the project already designed — counting `GET /raw/<id>.md` (docs/usage-metrics.md)
— is explicitly not live, and the highest-intent surfaces (`/b/<id>` pages, where
shared links and search traffic land on a page whose whole job is one Copy
button) ship **no analytics script at all**. The two cheapest fixes in this report
(stop auto-marking; count raw fetches from Vercel logs) would, together, make the
funnel's central transition visible for the first time — and position × severity
says nothing else matters until you can see whether copies become runs.

## 3 · Step-count budget

| Path | User actions to first value today | Achievable minimum | Gap |
|---|---|---|---|
| Copy-paste (hero quickstart) | load + 1 tap + switch + paste = **3 actions** + 15-min wait | 3 (paste and the run are irreducible; the wait *is* the product) | **0 — at floor.** Protect it; promote it. |
| Copy-paste (browse) | load + 1 click + 1 decision-among-141 + 1–2 taps + paste ≈ **5** | 4 (one chooser, not six) | −1 decision |
| Plugin | copy + paste + *discover fine print* + `/plugin install` + `/goal:…` = **5, one undiscoverable** | 4, all visible (copy both commands in one tap) | −1 silent stall |
| Studio | 1 tap (demo) → value on screen | 1 | 0 — at floor |
| Mobile visitor | **∞ — no path to value exists today** | 2 (copy raw URL → open on desktop later) | the whole cohort |

## 4 · Instrumentation gaps

**Live today** (Vercel Web Analytics, landing + Studio only, with anonymous
`aid`/`fsw` cohort fields): `copy_prompt{id,src}`, `copy_conductor`,
`copy_family_conductor`, `copy_custom_conductor`, `copy_install`, `copy_mcp`,
`share_link`, `mark_run{from:"copy"}` (fabricated — see §2), `nudge_shown/clicked`,
`reminder_opt_in`, `picker_plan`, `repo_recommend`, `search_zero`,
`studio_load_report`, `studio_load_github`, `studio_copy_fixer{n}`.

**Needed to see this funnel:**

1. **`/b/<id>` + `/p/<key>` pages are dark** — build.py's detail builders emit no
   insights script and gp-detail.js contains zero `va()` calls. Add the script tag
   in the builders and fire `copy_prompt{id, src:"detail"}` / `copy_step` from
   gp-detail.js. Without this, share links (`share_link` is tracked at send but
   not receive) and SEO entries are invisible end to end.
2. **Real-run signal** — stop conflating copy with run: keep `copy_prompt`, fire
   `mark_run` only from the explicit "✓ mark it run" button. Copy-to-confirmed-run
   ratio becomes the funnel's core conversion number.
3. **Raw-fetch counting** — activate docs/usage-metrics.md Option 1 (Vercel log
   filter on `pathname:/raw/`, zero code). Covers conductors, MCP, curl installer,
   CI — every consumer the browser events can't see. Note the doc's claim that
   "the site ships no analytics" is now stale and should be corrected when touched.
4. **Install completion** — `copy_install` measures intent only. The tarball
   fetch (`commands.tar.gz` in the same log filter) is the completion signal for
   the curl path; count it.
5. **Funnel-position events** — `catalog_reached` (first scroll/anchor into
   `#catalog`), `quickview_open{id}`, `examples_viewed`. Three events give
   drop-off between entry → choose → copy, which today is inferred from nothing.

---

*Read-only audit — no code was changed. Which of these fixes should be built
first: the plugin copy-both-commands fix, un-faking mark-run, lighting up the
detail-page analytics, the mobile copy bridge, or turning on raw-fetch counting?*
