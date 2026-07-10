---
description: Run the WCAG contrast gate over brand.json — every text/accent role × surface × theme plus the categorical set. Exit code is the verdict.
---

Run `python3 design-engine/tools/contrast.py --report $ARGUMENTS` from the
repo root. Report pass/fail, quote any violations verbatim, and point at
design-engine/out/contrast-report.txt for the full matrix. If it fails,
propose the smallest palette adjustment that clears the floor — never
propose lowering a threshold.
