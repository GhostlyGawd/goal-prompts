# COMPOUNDING.md — Compounding Value Audit

All Craft Goal Prompts · stage 4/5 · brief 155

2026-07-26 · brief 155 · first run (no prior COMPOUNDING.md found)

Method: read every persistence path in the source pages (template.html,
studio.html, vitals.html, js/gp-detail.js, js/report-parser.js,
js/catalog-core.js, mcp/server.cjs, install) and the accrual rules in the
briefs themselves, then ran the built site in a real Chromium twice — a fresh
profile, and a profile seeded as a "tenth visit" (10 run marks, saved Operator
context, a 3-stage custom sequence, 4 weeks of HEALTH.md history, a loaded
Studio report). Where a sibling report from this run already owns a finding
(DEFAULTS Q2/Q3/Q4, POLISH S2, RETENTION R6), it is cited, not re-counted.

This product's per-user state lives in two layers, and the report treats them
separately because they compound differently:

- **Layer A — the browser** (`gp-*` localStorage on the site pages): run marks,
  context, triage, trend history. Per-device, wiped by a cleared cache,
  covered by export/import.
- **Layer B — the user's own repo**: dated reports that diff against their
  last run, HEALTH.md's append-only history table, FIXLOG.md, CHARTER.md,
  DEBRIEF.md's history rows, INDEX.md per playbook run. This is the layer
  CHARTER.md:48 names as the moat ("the repo's accreting audit memory … is
  the loop's moat mechanism"), it survives everything, and it is where the
  hundredth session is actually supposed to beat the first.

The headline: **Layer B is a genuinely well-built compounding asset — 155 of
157 briefs carry "read the previous report first and lead with what changed"
— but its centerpiece, the charter, only feeds back into playbook runs. Every
single-brief copy, the majority path, ignores it.** Layer A deposits well and
surfaces most of it back; its gaps are one weekly-loop reset (Studio checks),
one invitation to destroy your own work (the sequence cap), and the absence of
any surface that states what you've built.

## 1 · Asset inventory

What accrues today: store · surfaced where · verdict.

| Deposit | Store | Surfaced where | Verdict |
|---|---|---|---|
| Run marks + last-run timestamp | `gp-runs` (template.html:1014, gp-detail.js:44) | hero stat "157 Goal Prompts · 10 run here" (:1416–1423); "✓ run · 3d ago" card labels in browse mode (:1043–1047, observed); roadmap/stale-Vitals nudges (:1654–1680); welcome-back strip on `b/`/`p/` pages (gp-detail.js:230–275); backer-nudge trigger (:1635) | **working** — the best-fed, best-surfaced deposit (but see C5: only the *last* run per brief survives) |
| Operator context | `gp-ctx` (:1089) | appended to every copy (`withContext`, :1092–1100, gp-detail.js:32–41); "Welcome back — tuned to Next.js + Supabase · invoicing SaaS" banner (renderCtxWarm :1104–1116, observed on the seeded profile) | **working** |
| Custom conductor sequence | `gp-seq` / `gp-seqused` (:1051–1055) | the seq bar ("01 → 06 → 47", observed) | **inert-ish** — one unnamed slot; see C3 |
| Studio reports + triage checks | `gp-studio-reports` / `gp-studio-checks` (studio.html:308–309) | full restore on return (observed: "BUGS.md · 2 findings", "0 of 2 selected"); ✓ fixed chips round-trip from re-run reports (report-parser.js:37–48) | **working, with a weekly reset** — see C2 |
| Vitals trend history | `gp-vitals-texts` (vitals.html:189) | sparklines + deltas + run chips (observed: 4 run chips, 3 metric tiles from seeded HEALTH.md) | **working** — dedupe on re-drop (vitals.html:367–370); but the file must be hauled back by hand every week (DEFAULTS Q1/Q2 own the loader half) |
| Prefs: theme, reminder, dismissals | `gp-theme`, `gp-remind`, `gp-wb-hide`, `gp-backer-done` | theme applied pre-paint on every page; reminder toggle state | **working** |
| Paste draft | sessionStorage `gp-studio-draft` (studio.html:683–697) | restored with the box reopened | **working** (deliberately ephemeral) |
| Analytics cohort ids | `gp-aid` / `gp-fsw` | never user-facing | plumbing |
| **Repo: dated re-run diffs** | every report file the briefs write | "If X.md already exists from a previous run, read it first and lead with what changed since" — in 155/157 briefs (only 74 and 143 lack it, both arguably per-change by design) | **working** — the core mechanic |
| **Repo: HEALTH.md history table** | append-only rows, never edited (prompts/meta/29-health-check.md:38) | trend arrows in the report itself; sparklines if hauled to /vitals | **working** |
| **Repo: FIXLOG.md** | append-only sessions (prompts/act/47-the-fixer.md:41–54) | read by nothing — no brief reads it back; see C7 | **inert on re-runs** |
| **Repo: CHARTER.md** | written by 149, amended not rewritten (149:43) | read by conductors (catalog-core.js:170, mcp/server.cjs:208) and briefs 149/150 only — the only 2 of 157 briefs that mention it | **inert on the majority path** — see C1 |
| **Repo: INDEX.md + per-stage commits** | conductor after-run (catalog-core.js:184, :179) | "recover the whole run with one `git log --grep`"; the next session's entry point | **working** — quietly excellent |

What natural use produces but the product discards: search queries
(`query`, template.html:1007 — never stored), 3-question-picker answers
(catalog-core.js:197–199 — recomputed every visit), the "recommend for my
repo" analysis and the repo ref itself (DEFAULTS Q2 — asked twice, remembered
zero times), every run of a brief before the latest (C5), and which playbook
a user is mid-way through (run marks are per-brief; `activePb` never
persists, so a half-finished 5-stage playbook looks like 3 unrelated runs).

## 2 · Compounding findings

Ranked by leverage: data already accrued but never surfaced first.

**C1 · S1 · lens 2 (value surfaced back) — The charter compounds only
through conductors; the single-brief path, the majority path, never reads
it.** The data: a user who runs 149 owns a ratified CHARTER.md whose entire
purpose is to bind every future session (CHARTER.md:46–49 — "the
catalog-wide input contract"; Now #5 names the wiring as the next build).
Where it actually fires today: the conductor preamble (catalog-core.js:170)
and the MCP conductor text (mcp/server.cjs:208) — playbook runs only. Where
it doesn't: `withContext()` appends only `gp-ctx` (template.html:1092–1100,
byte-identical twin in gp-detail.js:32–41), so the hero quickstart, every
card Copy, and every `b/<id>` copy ship charter-blind; MCP `get_brief`
returns the raw body (server.cjs:267–272); the installed `/goal-*` commands
and skills are raw brief bodies; and only 2 of 157 briefs mention CHARTER.md
at all (grep over prompts/: 149, 150). So the product's own moat mechanism
is dark on the paths most users take most often — the tenth solo-brief run
is exactly as generic as the first. The mechanism to build: one line in both
`withContext()` copies ("If CHARTER.md exists at the repo root, read it
first — its goals, non-goals, and invariants bound every recommendation"),
the same line appended by `get_brief` and baked into the command/skill
packaging preamble in build.py. Effort S — it is the same sentence the
conductor already carries — and it converts an already-accrued asset into
working input on every copy.

**C2 · S2 · lens 5 (compounding, not hoarding) — The weekly re-run wipes
Studio triage.** The data: finding keys are content hashes of
`report|title|text.slice(0,120)` (report-parser.js:59), and render prunes
any check whose key no longer matches a loaded finding (studio.html:475–479).
A re-run report — the product's own cadence — rewrites dates, line numbers,
and evidence, so every still-open finding the user had queued for the Fixer
loses its check; the product knows and apologizes ("previously checked
findings … cleared — re-check what still applies", studio.html:613–618)
instead of re-attaching. POLISH S2 fixed the accidental-remove case with
undo; this is the systemic case. Mechanism: on replace, re-attach checks by
`report|title` match (fall back to the full hash for renamed findings) —
the parser already extracts a stable title. The user gains: triage survives
the refresh, so the Studio half of the weekly loop accumulates decisions
instead of resetting them.

**C3 · S2 · lens 3 (early investment invited) — The sequence builder invites
ownership, then caps it at one unnamed slot and tells the user to destroy
it.** The data: `gp-seq` is a single anonymous array; at the 16-stage cap
the toast reads "copy this sequence, clear it, and build part 2"
(template.html:1060–1062) — the product's only instruction that ends in
deleting your own work. There is no name field, no second slot, no "your
conductors" anywhere; the MCP `make_conductor` even accepts a `name`
argument (server.cjs:288) that the site never lets you save. Mechanism:
named saved sequences (`[{name, ids}]` under a `gp-` key so the existing
export sweep at :1946 covers it automatically), a "save as…" on the seq
bar, and a small "your conductors" row beside the storefront playbooks.
The user gains: their own playbooks become owned, reusable artifacts — the
classic small act of ownership that visibly improves the next session.

**C4 · S2 · lens 7 (the asset made visible) — Nothing states what the user
has built.** The data: the entire inventory surface is five words —
"157 Goal Prompts · 10 run here" (renderStats, template.html:1416–1423,
observed). Yet the browser already knows enough for a real inventory line:
runs by family with timestamps (`gp-runs`), weeks of vitals history
(`gp-vitals-texts` row counts — vitals.html:306 computes them per chip),
findings loaded and triaged (`gp-studio-reports`/`-checks`), context saved
(`gp-ctx`). Mechanism: one "what you've built here" block next to the
export/import controls (:1974–1978) — "10 briefs run across 6 families ·
4 weeks of vitals history · 2 findings in triage · context saved" — stated
as inventory, with "export setup" directly beneath it so the backup button
finally has a visible referent. The user gains: time-to-irreplaceable
becomes something they can see; the operator gains: the export path gets
used before the cache-clear, not after.

**C5 · S3 · lens 1 (deposits exist) — Per-brief run history is overwritten
to a single timestamp.** The data: `runs[id] = Date.now()` on every mark
(template.html:1265, gp-detail.js:45) — a user who has run Bug Hunt six
times looks identical to one who ran it once. The repo layer holds the real
history (dated diffs), but the site can never say "✓ run ×6 · last 3d" or
show a cadence. Mechanism: store a small capped array of timestamps per id
(same key, backward-compatible read); surface the count in `runLabel()`
(:1043). Cheap, and it makes the weekly ritual's rhythm visible where the
marks already show.

**C6 · S3 · lens 1/2 (discarded) — Searches, picker answers, and the repo
recommendation evaporate.** The data: `query` lives in a variable
(template.html:1007); the 3-question picker's situation/pain/time answers
(catalog-core.js:197–199) and the "recommend for my repo" result are
recomputed from scratch every visit; the repo ref itself is DEFAULTS Q2
(`gp-repo` doesn't exist — the fix named there also feeds this). Mechanism,
accrual-from-natural-use only: a recent-searches row (cap 5) under the
search box, and the picker pre-selecting last time's answers. Rank low —
recommend only the pieces that pay back in the same session; recent
searches do, a search-history archive would be hoarding.

**C7 · S3 · lens 5 (repo layer) — Nothing reads FIXLOG.md back.** The data:
47 appends an append-only session log (prompts/act/47-the-fixer.md:41–54)
and the Studio's Fixer prompt does the same (studio.html:365), but no
audit brief's re-run pass mentions it — a re-run discovers a finding is
gone by re-auditing, and can't credit the fix to its commit. Mechanism: one
clause in the re-run rule of the diff-carrying briefs (or just in 29 and
46, the recurring ones): "if FIXLOG.md exists, credit fixed findings to
their logged commits in the diff." The user gains: the diff section reads
"fixed by fix/goal-2026-07-19" instead of "no longer present" — receipts,
which is the loop's stated register (CHARTER.md "evidenced").

Curation: **discarded → start keeping:** C5, C6 (+ `gp-repo`, owned by
DEFAULTS Q2). **Inert → surface it:** C1 (the charter — the cheapest,
biggest win in this report), C2 (checks across re-runs), C7 (FIXLOG).
**Invisible → show the asset:** C4. **Investment invited then dropped:** C3.

## 3 · Time-to-irreplaceable

Today, measured against a fresh profile in the same browser session:

- **Session 1:** the repo layer starts compounding immediately — the first
  report is already the next run's diff target (155/157 briefs). On-site,
  the first visit and second are nearly identical.
- **Session 2:** with saved context, the return is visibly warmer — the
  "tuned to *stack · product*" banner (observed). First felt difference.
- **Session ~3:** a repo with a charter, one re-run diff, and a FIXLOG entry
  is strictly better than a fresh clone for any agent that reads them — this
  is where "meaningfully better than fresh" lands today, *but only on the
  conductor path* (C1).
- **Session 5:** run count crosses the nudge thresholds (roadmap :1661,
  backer :1635); the seeded tenth visit showed the full return surface:
  stat line, context banner, roadmap nudge, saved sequence, restored triage,
  4-run sparklines.
- **Beyond 5:** the on-site curve flattens — the tenth visit has nothing the
  fifth doesn't except longer sparklines, and the roadmap milestone can even
  mask the recurring stale-Vitals pull (DEFAULTS Q3). The repo curve keeps
  climbing, invisibly.

What shortens it: **C1** moves the repo layer's compounding from session ~3
(first playbook) to session 2 (any copy after running 149) and extends it to
every path; **C4** makes the accrual visible at whatever session it reaches;
**C3** adds an ownership deposit available in session 1.

## 4 · Portability check

- **Exportable:** everything. "export setup" sweeps every `gp-*` key into a
  dated JSON file (template.html:1944–1952); import validates, filters
  `gp-seq` against the live catalog, and reloads (:1953–1972). Any key added
  under the `gp-` prefix joins the backup automatically — a genuinely good
  convention. Not exported: the IndexedDB `gp-sw` mirror (rebuilt on the
  next save — :1022–1035) and the sessionStorage draft (ephemeral by
  design). Both correct omissions.
- **The repo layer is portability itself:** plain markdown in the user's own
  git. Reports, charter, FIXLOG, and history tables leave with the repo, work
  without the site, and would keep compounding even if the catalog vanished —
  the briefs' re-run rules travel inside every installed command
  (`install:1–90` writes them into `.claude/commands/goal/`).
- **What that says:** no lock-in was found anywhere — no data held hostage,
  no export tax, no proprietary format. Stickiness here is entirely of the
  earned kind, which means the product's only retention lever is making the
  accrued asset *worth more* (findings above), and the charter's moat claim
  (CHARTER.md:48) is structurally honest. One seam: the export/import
  controls exist only in the landing-page footer — Studio and Vitals, the
  two pages holding the heaviest per-device state, offer no path to a backup
  from where that state lives.

What already compounds and should be protected as-is: run marks with honest
ago-labels, the context banner, the welcome-back strips, Vitals' duplicate
guard and sparklines, the ✓ fixed round-trip from re-run reports, the
Studio's lost-checks honesty note, and — the sleeper — the conductor's
INDEX.md plus per-stage commit trail, which turns every playbook run into a
git-greppable session another agent can resume cold.
