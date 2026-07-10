---
description: Screenshot every page × theme from brand.json host config (or --assert for the gateable health check: loads, no console errors, tokens resolve, fonts load).
---

Run `node design-engine/tools/shots.cjs $ARGUMENTS` from the repo root
(needs playwright-core + Chromium; PW_CHROMIUM overrides autodetection).
Without flags it writes screenshots to design-engine/out/shots/ — read the
images and summarize what you see per page/theme. With --assert report the
health results.
