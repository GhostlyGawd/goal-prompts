# INDEX.md — All Craft Goal Prompts run

2026-07-26 · playbook: **All Craft Goal Prompts** (5 stages, briefs 152–156) ·
branch `claude/product-engagement-stickiness-1cril7` · one commit per report
(`git log --grep "All Craft Goal Prompts"`). CHARTER.md was read first and
bounds every recommendation. Stage 1 was **skipped**: `POLISH.md` was already
brief 152's report from earlier the same day (second run, all findings fixed
and re-verified), so a third same-day run would have diffed against itself.

## Stages

1. **152 · Fit & Finish Audit** — https://goal-prompts.vercel.app/raw/152.md →
   `POLISH.md` · pre-existing same-day report, stage skipped · 8 findings from
   run 1, **all closed** in run 2 · next step per the report itself: re-run
   after the next stretch of UI work.
2. **153 · Smart Defaults & Anticipation Audit** —
   https://goal-prompts.vercel.app/raw/153.md → `DEFAULTS.md` · **10 findings**
   (1 S1, 3 S2, 6 S3) · next: make Studio's GitHub loader read `reports/` (the
   product's own default output dir); remember the repo ref once (`gp-repo`)
   and prefill it everywhere it's asked; stop the roadmap-milestone rule from
   permanently suppressing the stale-Vitals nudge.
3. **154 · Perceived Speed Audit** —
   https://goal-prompts.vercel.app/raw/154.md → `PERCEIVED-SPEED.md` ·
   **9 findings** (3 S2, 3 S3, 3 S4), all browser-observed under throttling ·
   next: paint a synchronous "copying…" state on cold-cache copy clicks (6.1 s
   frozen button observed); give the service worker's network-first HTML fetch
   a timeout-to-cache fallback; make Studio's GitHub load narrate its phases
   and stop mis-reporting rate-limits as "no reports".
4. **155 · Compounding Value Audit** —
   https://goal-prompts.vercel.app/raw/155.md → `COMPOUNDING.md` ·
   **7 findings** + asset inventory across both persistence layers · next:
   append the read-the-charter line to every single-brief copy path (only
   conductors carry it today); re-attach Studio triage checks by report+title
   on re-run instead of pruning them; show a "what you've built here"
   inventory beside the export controls.
5. **156 · Signature Moments Audit** —
   https://goal-prompts.vercel.app/raw/156.md → `SIGNATURE.md` · **6 moment
   findings** + 6-artifact output audit; restraint audit clean (no confetti to
   remove — the gaps are silent peaks) · next: stage the post-Fixer "findings
   closed" receipt in Studio; fix Vitals' lower-is-better metrics rendering
   danger-red and its permanently visible paste box (`[hidden]` CSS pin);
   give single briefs the conductor's debrief ending.

## Where to start

A session with no memory of this run: read this file, then the report whose
area you're touching. The cross-cutting theme of the run — the first visit is
in good shape; the **return loop** (reload after a Fixer run, the weekly
Vitals ritual, the re-run diff) is where value lands silently, gets reset, or
never uses what the product already remembers.
