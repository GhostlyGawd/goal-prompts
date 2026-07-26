# SIGNATURE.md — Signature Moments Audit

All Craft Goal Prompts · stage 5/5 · brief 156

2026-07-26 · brief 156 · second run (same day as the first)

What changed since the last run: all six moment findings and the restraint
list closed; the signature candidate's shape is pinned by test. Fixes
shipped on `claude/product-engagement-stickiness-1cril7` (merged as #42),
verified in a real Chromium during the fix session. Two output-audit items
remain open by nature, named at the end — both need artifacts only a real
external run can produce.

## Moment findings

- **FIXED M1 — The loop's proof moment was silent.** A same-name re-add now diffs the fixed flags and posts the receipt in the existing note register — "BUGS.md: 1 finding closed since the last load · 1 still open" — and fixed rows sink: `--sev-fixed` border, dimmed, sorted after open findings, the redundant FIXED title prefix stripped beside the chip. Decay is built in: the line renders only when the closed count is > 0.
- **FIXED M2 — Vitals painted wins as regressions.** A lower-is-better map covers brief 29's canonical vitals (fails, build seconds, vulns, outdated, lint/type errors, TODOs); a falling build time now renders success-green, and a metric the map can't judge — LOC — gets the neutral tone it can honestly claim, arrow intact. Verified against the sample history.
- **FIXED M3 — The weekly page shipped half-open.** Vitals carries Studio's one-line `[hidden]{display:none!important}` pin; the fresh-load view is clean.
- **FIXED M4 — Single briefs ended as a file path, not a felt win.** Every one of the 157 briefs now carries "present the top findings as a ranked list in plain words" before its ask-first gate — added mechanically, enforced by a new linter rule, documented in CONTRIBUTING. The ending is the debrief in miniature at every scale.
- **FIXED M5 — The first win was diluted by a four-path menu.** The first-copy toast carries paste + "what happens next →" (and now "no report? →" for the silent-failure exit); the Day-1 tee waits for the proven-intent moment (first marked run). 
- **FIXED M6 — The one milestone voice was an undismissable ask.** Both catalog nudges take a × — the roadmap milestone dismisses forever (the backer nudge's pattern), stale-Vitals dismisses for the current stale period and may honestly return on a new one.

## Restraint list

- **FIXED R1 — The post-copy explainer never decayed.** Once any run is marked, the toast collapses to the short form; the full explainer is for people the product hasn't met.
- **FIXED R2 — covered by M6's dismissals.**
- **FIXED R3 — covered by M5's tee timing.**

The first run's grep-clean bill of health still holds: no confetti, no
streaks, nothing celebrating the product instead of the user's work.

## The signature candidate, updated

The conductor's closing debrief is now **pinned, not just specified**: the
catalog-core suite asserts its three beats — the ranked list in plain words,
the "which findings to fix" ask, the paste-ready handoff block — so the
shape can't drift silently, and M4 gives single briefs the same ending
grammar. Still open, by nature: staging the debrief itself — one real
transcript excerpt in the gallery and on the playbook pages' ending box —
wants the debrief of an actual external run, not a mockup, and none has
been captured yet. Same for the output audit's INDEX.md/PR handoff item:
unproven in public until a real external before/after exists (CHARTER
Now #1). Both are artifacts to capture, not code to write.

## Rules note

- Before asking, the findings above are the ranked list — closed except the
  two capture-an-artifact items named above.
- Report only — the next re-run should happen after the first real external
  playbook run, which is also what those two open items are waiting for.
