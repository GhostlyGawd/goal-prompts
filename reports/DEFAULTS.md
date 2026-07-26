# DEFAULTS.md — Smart Defaults & Anticipation Audit

All Craft Goal Prompts · stage 2/5 · brief 153

2026-07-26 · brief 153 · second run (same day as the first)

What changed since the last run: all ten findings closed. The fixes shipped
on `claude/product-engagement-stickiness-1cril7` (merged as #42), and every
one was verified in a real Chromium against the built site during the fix
session — the same reproductions the first run used, re-run green. The
first run's headline stands: the first visit was already excellent. The
return loop now uses what the product remembers.

## 1 · Question findings

- **FIXED Q1 · S1 — Studio's GitHub loader can't see `reports/`.** The loader now lists `/contents/reports` beside the root and the raw-URL probe tries `reports/<name>` first (studio.html `loadFromGitHub`/`ghProbeCommon`). Verified: a repo whose reports live only in `reports/` loads them; the "no reports" message now names both locations.
- **FIXED Q2 · S2 — The repo reference was asked twice, remembered never.** A ref that works is saved as `gp-repo` and prefills Studio's box, the landing analyzer, and Vitals' new fetch button. Verified: set in one surface, appears in the others; still a plain editable field.
- **FIXED Q3 · S2 — The roadmap milestone permanently outranked stale Vitals.** The ladder is reordered on the landing page and the detail-page strip: time-keyed staleness first. Verified with a seeded profile (6 runs, Vitals 9 days stale): the stale-Vitals nudge renders, not the milestone.
- **FIXED Q4 · S2 — Detail pages hid run state the device stores.** gp-detail.js renders "✓ run · 3d ago" beside the brief CTA and a mark on each already-run sequence step, display-only from `gp-runs`. Verified on `/b/01` with a seeded run.
- **FIXED Q5 · S3 — The browse gate re-asked a proven regular.** Any run mark now boots the catalog open (`browsing = true` at restore time). Verified: the seeded profile lands on cards, a fresh profile still meets the gate.
- **FIXED Q6 · S3 — Conductor copies dropped the Operator context.** `makeConductor()` is the one choke point and now appends the same context block every single-brief copy carries; the playbook-page CTA does the same via `ctxBlock`. The conductor keeps its own charter line, so nothing doubles.
- **FIXED Q7 · S3 — The fallback probe guessed 11 names while the catalog knows 157.** The probe now fetches `/catalog.json`, probes the run-marked briefs' output files first, then the standbys.
- **FIXED Q8 · S3 — `product` stayed blank after a call that carried it.** When the field is empty, the analyzer fetches the repo description and saves it with the stack's exact pattern — announced ("✓ saved …"), mirrored into the form, editable.
- **FIXED Q9 · S3 — The coarse-pointer branch removed the correct path.** The post-copy toast now shows the paste guidance *and* the raw-URL bridge; the wrong guess costs nothing.
- **FIXED Q10 · S3 — Vitals had no fetch path.** With a remembered `gp-repo`, the page offers one-tap "refresh HEALTH.md from ⟨owner/repo⟩" (reports/ first, then root); the duplicate guard still absorbs re-fetches.

## 2 · The memory map, updated

New keys since run 1, all under the `gp-` prefix so the export/import backup
sweeps them automatically: `gp-repo` (the remembered ref), `gp-runhist`
(per-brief run history, COMPOUNDING C5), `gp-seqs` (named conductors,
COMPOUNDING C3), `gp-recent` (recent searches, C6), and the per-period nudge
dismissal keys (`gp-nudge-*`). Nothing that reset to factory in run 1 still
does.

## 3 · First-run delta

Unchanged by design — the first run was two actions and zero fields, and
stays so. The run-2..N delta the first report asked for is now the shipped
behavior: land in your catalog, one-tap reload from the remembered repo,
`reports/` found, Vitals refreshes itself, zero retyped fields in the loop.

## Rules note

- Before asking, the top findings above are the ranked list — all closed.
- Report only — nothing further to fix from this brief's lens; re-run after
  the next stretch of onboarding or persistence work.
