# Retention & Lifecycle Audit — re-run

**Date: 2026-07-09** · read-only pass over `template.html`, `build.py` (SW +
detail-page builders), `js/gp-detail.js`, `b/`, `p/`, `vitals.html`,
`studio.html`, `mcp/server.cjs`, `plugin/`, `install`, `.github/*.example.yml`,
`README.md`, `docs/usage-metrics.md`. Companion reports from today's playbook:
FUNNEL.md, CRO.md, SEO.md, REVENUE.md — cross-referenced, not duplicated.

---

## 0 · What changed since the last run (~4 months ago)

**All five prior findings (R1–R5) shipped, verified in current source:**

- **R1 — the run-tracker is fed at the moment of action.** Copying a brief on
  the landing page optimistically records the run with an easy undo
  (`template.html:1136-1143`), and the post-copy hint carries a "✓ mark it run"
  button (`:901-917`). The nudge engine no longer runs dark.
- **R2 — the opt-in weekly Vitals reminder exists.** A footer toggle
  (`:760`, `:1422-1459`) requests Notification permission and registers a
  `vitals-weekly` periodicSync; the service worker shows the notification and
  focuses/opens the site on click (`build.py:286-307`).
- **R3 — export/import setup.** Footer "export setup" / "import a backup"
  round-trips every `gp-*` localStorage key as a JSON file (`:1385-1420`) —
  covering runs, context, sequence, Studio triage, and Vitals history.
- **R4 — Operator context resurfaces warmly.** A "Welcome back — your briefs
  are tuned to *stack · product*" banner renders above the catalog on any
  return with saved context (`renderCtxWarm`, `:848-862`, `#ctxwarm` `:582`).
- **R5 — cohort instrumentation started.** An anonymous id + first-seen-week
  (`gp-aid`/`gp-fsw`, `:874-880`) ride events routed through `track()`
  (`:881-883`), and `nudge_shown` / `nudge_clicked` / `mark_run` /
  `reminder_opt_in` events exist (`:1142`, `:1210-1212`, `:1440`).

**The product's perimeter changed underneath those fixes:** 141 briefs, a
Claude Code **plugin as the README's primary install**, **MCP prompts**
(every brief in the client's prompt picker), 141 `/b/<id>` + 35 `/p/<key>`
detail pages that are now the best-indexed entry points (per SEO.md), a
**Vitals Viewer** page (`/vitals`) that turns HEALTH.md history into
sparklines, a ready-to-copy **scheduled run-brief GitHub Action**
(`.github/run-brief.example.yml`), ranked search, and a light theme.

**Consequence — the retention problem moved.** Last run's diagnosis was "the
engine is dark" (no trigger data). The engine is lit now, but three new seams
opened: (1) every shipped retention fix is **landing-page-only** while entry
traffic shifted to detail pages that have none of it — and no analytics at
all; (2) the reminder chain shipped with **three broken links** (fires blind,
no PWA-install path, returns unattributable); (3) the single best
accruing-value surface, the **Vitals Viewer, is an orphan** — zero inbound
links from anywhere on the site.

---

## 1 · Return-trip map

- **Visit rhythm — still episodic with one weekly anchor.** The job (audit a
  repo) is event-driven: new repo, pre-launch, post-refactor. The one designed
  recurring ritual is **Weekly Vitals (29)** — "ten minutes, every week"
  (`README.md:112`; brief 29 is "Designed to re-run weekly" and appends a
  dated history table). Count retention from that weekly cadence.
- **A structural shift: for the best-retained users, the "return" no longer
  happens on the site.** Plugin (`/goal:<slug>`) and installer
  (`/goal-<slug>`) users carry the whole catalog inside their editor; MCP
  users have every brief as a prompt (`mcp/server.cjs:319-337`). That is
  retention *success* — the product lives where the work is — but it means the
  site's returning-user job narrows to three pulls: **fresh trends**
  (`/vitals`), **triage** (`/studio`, `gp-studio-reports`/`-checks`,
  `studio.html:270-271`), and **what's new** in the catalog.
- **What persists (localStorage, per-device):** `gp-runs` (with timestamps),
  `gp-seq`, `gp-ctx`, `gp-theme`, `gp-remind`, `gp-aid`/`gp-fsw`,
  `gp-studio-reports`/`gp-studio-checks`, and `gp-vitals-texts` — the pasted
  HEALTH.md history that makes each week's run worth more than the last
  (`vitals.html:145`). Export/import covers all of it (`:1388`).
- **The pull back:** the two in-page nudges (roadmap ≥5 runs, stale Vitals
  >7d — `renderNudge`, `:1192-1213`), the welcome-back context banner, the
  opt-in weekly notification, Studio triage, and — off-site — the report
  history accruing in the user's own repo.
- **The biggest leak:** the weekly-Vitals loop is built but **disconnected**.
  The nudge, the notification, the viewer, and the scheduler all exist and
  none of them link to each other — and the viewer is unreachable entirely.

---

## 2 · Findings (lens · location · why users drift · fix · effort)

Ranked by compounding value.

### R6 — The Vitals Viewer is an orphan page *(lens 2: saved state as a hook · lens 5: progression)* — **HIGH · effort S**
- **Location:** `/vitals` is precached by the SW (`build.py:1379`) and listed
  in `sitemap.xml:5` — but has **zero inbound links**: not in the landing
  page's nav or footer (`template.html` contains no `/vitals` href), not on
  `b/29.html`, not on `p/vitals.html`, not in the stale-Vitals nudge (links
  `#29` only, `:1204`), not in the SW notification (`data.url: "/#29"`,
  `build.py:295`).
- **Why users drift:** the viewer is the product's only *progression* surface
  — each weekly paste adds a sparkline point (`gp-vitals-texts`,
  `vitals.html:145,298`), which is exactly the accruing value that makes
  staying rational. A user who runs Vitals weekly never learns the trends
  page exists; the ritual feels like Groundhog Day instead of a growing
  history, and the tenth visit has no more pull than the second.
- **Fix:** link `/vitals` from the stale-Vitals nudge and the SW
  notification URL, from `b/29`'s deliverable section, from `p/vitals`, and
  from the site footer. Resurfacing value the user already created — the
  cheapest, highest-leverage fix in this report.

### R7 — Every retention fix is landing-page-only; detail pages are a parallel cold world *(lens 3: the empty return · lens 8: measurement)* — **HIGH · effort M**
- **Location:** the 141 `b/` + 35 `p/` pages run `js/gp-detail.js`. Context
  rides copies and the hint can mark a run (`gp-detail.js:17-37,71-78`) —
  good — but there is **no welcome-back banner, no nudges, no optimistic
  run-mark on copy** (hint-button only), and **no analytics script at all**
  (`grep -c _vercel b/29.html` → 0; `gp-detail.js` emits zero events;
  confirmed independently by REVENUE.md §167).
- **Why users drift:** per SEO.md the detail pages are now the best-indexed
  entry points, so a *returning* user arriving via Google gets a cold start —
  no "welcome back," no stale-Vitals pull, no roadmap nudge — and the
  operator can't even see that the visit happened. The retention machinery
  guards the front door while traffic moved to the side doors.
- **Fix:** add the insights snippet + `copy_prompt`-equivalent events to the
  detail-page template (`build.py` head builder), and a slim shared
  welcome-back/nudge strip (the logic is ~30 lines; `gp-detail.js` already
  reads `gp-runs`/`gp-ctx`).

### R8 — The weekly reminder chain has three broken links *(lens 4: well-timed nudges · lens 6: churn cliffs)* — **HIGH · effort M**
- **(a) It fires blind.** The SW shows "Weekly Vitals is due" unconditionally
  on every `periodicsync` tick (`build.py:290-297`) — it can't read
  `localStorage`, so it never checks `runs["29"]`. A user who ran Vitals
  yesterday still gets nudged, directly contradicting the opt-in toast's
  promise: "When Weekly Vitals goes 7+ days stale, your browser will nudge
  you" (`template.html:1451`). Every nudge must be one the user would thank
  you for; a wrong "it's due" teaches them to disable notifications — a
  one-way churn cliff. **Fix:** mirror `runs["29"]` + `remind.on` into
  IndexedDB (or the Cache API) in `saveRuns()`/`saveRemind()`, and have the
  SW check staleness before showing.
- **(b) The background path is unreachable.** periodicSync needs an
  *installed* PWA (Chromium), but nothing anywhere suggests installing —
  no `beforeinstallprompt` handling, no install hint on any surface. Most
  opt-ins end at the fallback toast ("no background-reminder support",
  `:1452`), i.e. the reminder quietly doesn't exist. **Fix:** when the user
  opts in and `periodicSync` is absent, offer the PWA install right there —
  the one moment installing has a stated benefit.
- **(c) It's buried.** The toggle lives in a footer buildnote (`:760`) below
  the fold, next to "reset run tracker." The natural moment to offer it is
  right after a Vitals run is marked — intent proven, timing honest. (Minor:
  the "🔔" glyph is outside the repo's stated mono-Unicode icon set per
  CLAUDE.md.)

### R9 — A reminder-driven return is invisible; retention events carry no cohort id *(lens 8: is return even measured)* — **HIGH (operator) · effort S**
- **Location:** `track()` attaches `aid`/`fsw` (`:881-883`), but the
  retention-specific events bypass it and call `window.va` raw:
  `nudge_shown`/`nudge_clicked` (`:1210-1212`), `mark_run` (`:1142`),
  `reminder_opt_in` (`:1440`). The code even disagrees with itself — `:871`
  says R5 shipped, while `:1137` and `:1209` say "R5 stays off." The SW
  notification opens plain `/#29` with no source marker and emits nothing
  (`build.py:295-307`): there is no `reminder_fired` and no way to
  distinguish a notification-driven return from an organic one.
- **Why it matters:** you can now count nudges shown but still cannot answer
  the only question that justifies them — *do they bring anyone back?* The
  one hook built since the last audit ships unmeasurable.
- **Fix:** route all events through `track()`; set the notification URL to
  `/#29?src=reminder` and emit `reminder_return` on load when present;
  emit `pwa_installed` from the `appinstalled` event.

### R10 — Installed surfaces freeze at install; no freshness pull, no win-back *(lens 1: reason to return · lens 7: win-back)* — **MED · effort M**
- **Location:** the plugin bundles the catalog at build time (updates only
  via a manual `/plugin marketplace update`, `README.md:31`); the curl
  installer requires a re-run (`install:10`); the MCP server reads its own
  pinned `catalog.json` — by design it "never drifts from the installed
  version" (`mcp/server.cjs:5-6`). `CHANGELOG.md` exists but is not published
  as a page; nothing anywhere says "what's new."
- **Why users drift:** the catalog grew 129 → 141 in two days and a plugin
  user will never hear. For the best-converted users (installed = the
  retention-grade conversion, per CRO.md §4), a lapse is permanent by
  default: no surface ever gives them a reason to come back or re-sync.
- **Fix:** publish `/changelog` from `CHANGELOG.md` at build time and link it
  site-wide; have the MCP `list_briefs`/`list_playbooks` footer line include
  the installed version ("goal-prompts v0.12.0 — check
  goal-prompts.vercel.app/changelog for newer briefs"); print the same
  pointer at the end of `install`.

### R11 — The strongest habit machine is README-only *(lens 5: habit · lens 4: nudges)* — **MED-HIGH · effort S**
- **Location:** `.github/run-brief.example.yml` — a Monday-cron GitHub Action
  that runs a chosen brief and files the report as an issue ("audits as a
  standing appointment instead of a memory," `README.md:94-101`). It appears
  nowhere on the site: not on the landing page, not on `b/29`, not on
  `p/vitals`, not in any post-copy hint.
- **Why users drift:** this is the one retention device that keeps working
  *after the user forgets the product exists* — honest, opt-in, and delivered
  where they already live (GitHub issues). Hiding it in the README means the
  ritual depends on human memory, which is the thing it was built to replace.
- **Fix:** merchandise it at the moment of proven intent — after a Vitals
  copy/mark-run ("make it a standing appointment →") and on `b/29` /
  `p/vitals`.

### R12 — "Nothing leaves your machine" vs. an undocumented persistent analytics id *(lens 6: churn cliff — trust)* — **MED · effort S**
- **Location:** the hero promises "nothing leaves your machine" (`:502`)
  while `gp-aid` — a persistent random id — now rides analytics events
  (`:874-883`). The last report shipped this with an explicit caveat:
  "document it, prefer opt-in." It shipped undocumented; no footer note, no
  README mention, no docs page.
- **Why users drift:** the promise is the acquisition hook for exactly the
  privacy-conscious audience most likely to check — and one HN comment
  pointing at `gp-aid` next to that hero line churns them permanently.
  Trust cliffs are the least recoverable kind.
- **Fix:** one honest footer/docs line ("anonymous, cookie-less usage events
  via Vercel Insights; a random local id, no PII; your runs/context never
  leave the device") — or make the id opt-out. Cheap insurance.

### What already retains — keep it
- **Copy-marks-a-run + undo** (`:1136-1143`) — the engine's fuel line, fixed.
- **Two honest, state-tied nudges** (`:1192-1213`), now instrumented as shown.
- **The welcome-back context banner** (`:848-862`) — accrued value, felt.
- **Export/import** (`:1385-1420`) — the new-device cold start has an answer.
- **Report history in the user's own repo** (HEALTH.md's append-only history
  table; every report a standing artifact) — value that accrues *off-site*,
  immune to cleared storage.

---

## 3 · The one hook to build

**Close the Weekly Vitals loop.** Not a new feature — a set of links between
four pieces that already exist: the stale-Vitals nudge (`:1202-1204`), the
opt-in notification (`build.py:290-297`), the Vitals Viewer's accruing
sparklines (`vitals.html`), and the Monday cron workflow
(`.github/run-brief.example.yml`).

The argument: last audit's "one hook" (the reminder) was built, but it shipped
as an island — it fires blind (R8a), mostly can't be delivered (R8b), links to
a brief instead of the user's own trend history (R6), and can't be measured
(R9). Meanwhile the product's genuinely differentiated retention asset — a
*growing, week-over-week health history of a repo the user cares about* — is
split between an orphan page and a README section. Wire it end to end:
nudge/notification → `/vitals` ("here's your history, 6 runs and climbing") →
"make it a standing appointment" (the workflow). Every piece is honest,
opt-in, and resurfaces value the user already created; the second and tenth
visits each arrive with strictly more to show than the last. R6 + R11 are
small; R8a/R9 are the wiring; R8b is the delivery. Together they finish the
hook this product has been building for two audits.

---

## 4 · Instrumentation gaps (to see retention at all)

- **Route every event through `track()`** so `aid`/`fsw` ride
  `nudge_*`, `mark_run`, and `reminder_opt_in` — today the retention events
  are the ones you can't cohort (R9). Resolve the contradictory R5 comments
  (`:871` vs `:1137`/`:1209`) one way or the other, deliberately.
- **Reminder attribution:** `?src=reminder` on the notification URL +
  `reminder_return` on load; `pwa_installed` via `appinstalled`. Without
  these, R2's ROI is unknowable forever.
- **Detail-page analytics** (R7): the fastest-growing entry surface currently
  reports nothing — neither acquisition nor return.
- **The installed-user blind spot:** plugin and installer users generate zero
  site traffic; conductor stages do fetch `/raw/<id>.md`. The design for
  counting those fetches exists (`docs/usage-metrics.md`) but "nothing in
  this document is live." Turning on Option 1 (Vercel log filtering — zero
  code) is the only way to see whether installed users are alive at all.
- **Cohort readout:** with `aid`+`fsw` on all events, week-N return curves
  are derivable from Vercel Insights custom-event exports today; no backend.
- **The standing tension:** all of this brushes "nothing leaves your machine"
  — keep it anonymous, aggregate, and *documented* (R12), and prefer counting
  paths (`raw/*.md` per day) over people wherever a path answers the question.

---

## Report only — which fixes do you want me to make?

Nothing was changed in this pass. The cheapest compounding wins are **R6**
(link the orphaned Vitals Viewer — pure HTML/href work) and **R11** (surface
the scheduled workflow at the moment of intent); **R9** (event routing +
reminder attribution) is small and makes everything else measurable; **R8**
(staleness-aware SW + PWA install offer) finishes the reminder honestly;
**R7** (detail-page parity + analytics) is the biggest build; **R10**
(publish `/changelog`, version pointers) and **R12** (document the analytics
id) round it out. Tell me which to implement — and for R12, whether you'd
rather document the anonymous id or drop it.
