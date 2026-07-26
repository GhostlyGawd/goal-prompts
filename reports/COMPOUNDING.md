# COMPOUNDING.md — Compounding Value Audit

All Craft Goal Prompts · stage 4/5 · brief 155

2026-07-26 · brief 155 · second run (same day as the first)

What changed since the last run: all seven findings closed, shipped on
`claude/product-engagement-stickiness-1cril7` (merged as #42) and verified
in a real Chromium during the fix session. The first run's structural read
stands — Layer B (the user's repo) was already a well-built compounding
asset; the fixes wired its centerpiece into the majority path and stopped
Layer A's weekly resets.

## Compounding findings

- **FIXED C1 · S1 — The charter compounded only through conductors.** Every single-brief copy now appends the charter line ("If CHARTER.md exists at the repo root or in reports/, read it first…") via both `withContext` twins (template.html + gp-detail.js, kept byte-identical). Conductors keep their own copy in the preamble — nothing doubles. The tenth solo-brief run is no longer as generic as the first.
- **FIXED C2 · S2 — The weekly re-run wiped Studio triage.** On a same-name re-add, checks re-attach by normalized title (the FIXED/FIX/IMPROVE/NEW tag vocabulary stripped before comparing — without that, nothing ever matched). Verified: check a finding, re-add the post-Fixer version, the still-open finding stays checked and the receipt line posts.
- **FIXED C3 · S2 — The sequence builder capped ownership at one unnamed slot.** "save as…" on the seq bar names a sequence into `gp-seqs` (capped, export-swept); saved conductors render as a "your conductors" row under the storefront with copy and delete. The 16-stage toast still arms — but building part 2 no longer means destroying part 1.
- **FIXED C4 · S2 — Nothing stated what the user has built.** A "What you've built here" line renders beside the export controls — runs by family, vitals sources, reports and triage in the Studio, context saved — inventory, not guilt, with the backup button directly beneath its referent.
- **FIXED C5 · S3 — Run history was overwritten to a single timestamp.** A capped `gp-runhist` array accrues beside `gp-runs` (readers of the old shape untouched); run labels show "✓ run ×3 · 2d ago".
- **FIXED C6 · S3 — Searches evaporated.** A recent-searches row (cap 5) renders under the toolbar when the box is empty; only queries that actually found something are kept. The picker half of this finding was already obsolete — the 3-question picker left in the redesign.
- **FIXED C7 · S3 — Nothing read FIXLOG.md back.** Briefs 29 and 46 — the recurring ones — now credit fixed findings to their logged commits in re-run diffs, so "no longer present" becomes a receipt.

## Portability check, updated

Still no lock-in anywhere. Every new key landed under the `gp-` prefix, so
the export/import sweep covers all of it with zero new code — the first
run's "genuinely good convention" doing exactly what it promised. The one
seam named in run 1 (Studio and Vitals offer no backup path from where the
state lives) is partially eased — the welcome-back banner now carries
"export setup →" — and fully closing it stays a fair item for the next run.

## Rules note

- Before asking, the findings above are the ranked list — all closed.
- Report only — re-run after the next persistence-layer change; the
  time-to-irreplaceable curve should be re-measured with real seeded
  profiles then.
