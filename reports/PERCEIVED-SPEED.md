# PERCEIVED-SPEED.md — Perceived Speed Audit

All Craft Goal Prompts · stage 3/5 · brief 154

2026-07-26 · brief 154 · second run (same day as the first)

What changed since the last run: all nine waits treated. Fixes shipped on
`claude/product-engagement-stickiness-1cril7` (merged as #42). W1, W3, W4,
W6, W8 and W9 were re-verified in a real Chromium during the fix session;
W2's timeout race and W5's bodies.json sourcing are verified by construction
plus the green gate (the first run's slow-origin harness wasn't rebuilt for
the re-check — noted honestly; the code path is small and single-purpose).
The first run's headline stands: the product was already mostly fast and
honestly presented. The frozen-silence seams are closed.

## 1 · Wait findings

- **FIXED W1 · S2 — The hero quickstart (and every card Copy) froze for the bodies.json download.** `copyBrief` now paints "copying…" + `aria-busy` synchronously in the click; `feedback()` clears the busy state on success and the fail path restores the real markup (the label snapshot is taken *before* the busy text, so the pill's markup survives).
- **FIXED W2 · S2 — Network-first HTML with no timeout wasted the warm cache.** The service worker races the fetch against a 2.5s timeout that falls back to cache; a hanging network can no longer beat a byte-identical cached page. The deploy story holds: the cache version is a content hash, so a deploy self-invalidates on the next good fetch.
- **FIXED W3 · S2 — Studio's GitHub load was one flat "loading…" and its rate-limit failure lied.** The button narrates each phase ("listing repo…" → "rate-limited — probing likely filenames…" → "fetching N reports…"), and a 403 is reported as a rate limit with honest advice, never as "no reports".
- **FIXED W4 · S3 — Step copy stayed clickable mid-fetch and lost the copy on WebKit.** The button disables during the fetch (no more duplicate requests) and the copy runs through a gesture-synchronous ClipboardItem whose text resolves when the body lands — `copyBrief`'s WebKit-safe pattern, now shared.
- **FIXED W5 · S3 — Step copies polluted the /raw/ usage metric.** Steps source their bodies from bodies.json (SW-precached) with /raw/ as fallback only; the agents' endpoint keeps honest counts.
- **FIXED W6 · S3 — The newcomer's primary CTA arrived last on a slow load.** The quickstart ships in the built HTML as a visible link to `/b/01` at button weight beside the CTAs; JS upgrades it in place to the one-click copy. No JS, no wait — the door is in the first paint.
- **FIXED W7 · S4 — The 10–20 minute wait started unstated.** Both post-copy toast forms name it: "… it writes `BUGS.md` (~15 min)".
- **FIXED W8 · S4 — Quick view popped in two motions.** The loading state reserves min-height so the body lands in one.
- **FIXED W9 · S4 — The Studio demo fetched four samples serially.** Parallel fetch, ordered add; the progressive per-file render kept.

## 2 · The hot path, updated

Copy → paste → report: the copy acknowledges within a frame in every cache
state (W1), the door is visible at first paint (W6), the paste moment states
its price (W7), the conductor still narrates the long middle, and the weekly
return is served from cache when the network dawdles (W2). The target the
first run set is the shipped behavior.

## Rules note

- Before asking, the findings above are the ranked list — all closed.
- Report only — re-run this brief after the next fetch-path or service-worker
  change, ideally with the slow-origin harness rebuilt for W2.
