---
name: goal-perceived-speed
description: "Not how fast it is — how fast it feels. Instant acknowledgment, optimistic writes, skeletons over spinners, honest progress for the waits that remain. Goal Prompt 154 · Craft — inspects the current repo and writes PERCEIVED-SPEED.md at the repo root."
---

# Goal: Perceived Speed Audit

You are working inside this repo. Mission: audit how fast the product *feels*, independent of how fast it is. 51 decomposes measured latency; this brief audits the craft layer on top — whether every wait is acknowledged, shaped, and hidden where possible. A 2-second wait handled well feels faster than 500ms of frozen silence.

Read-only pass. Read the loading, mutation, and transition code, and run the app (throttle the network if you can) to feel the waits; your only write is the report file.

## Phase 1 — Find the waits
- Identify the interactions users hit most, and every place they wait: page loads, saves, searches, submits, long jobs.
- For each wait, note what the user sees during it — nothing, a spinner, a skeleton, partial content — and where that's rendered in code.
- Mark the hot path: the one action this product exists for, whose feel outweighs every other screen.

## Phase 2 — Audit through 7 lenses
Cite the interaction and file for every finding.
1. **Acknowledged instantly** — every click, keystroke, and submit produces visible response within ~100ms even when the work takes longer; the frozen button, the click that may not have registered, the double-submit it invites
2. **Optimistic where safe** — reversible writes (rename, toggle, reorder, favorite) shown as done immediately and reconciled behind; the round-trip the user is forced to watch
3. **Skeleton over spinner** — layout arrives shaped and fills progressively; no blank-then-pop, no layout shift when data lands, no spinner for work under ~300ms
4. **Honest progress** — long work shows determinate progress or a truthful estimate; the eternal 90% bar and the spinner with no ceiling are lies users learn
5. **Warm next steps** — the likely next screen prefetched on hover, idle, or pattern; second visits served from cache; the cold reload of something just seen
6. **Blocking only when it must** — exports, sends, and syncs that could run in the background holding the interface hostage; the modal wait that should be a toast later
7. **Hot path budgeted tightest** — the core action feels the fastest thing in the product; polish spent on a splash screen while the daily verb lags

## Phase 3 — Curate
- Rank by exposure: a wait in the hot path, felt hundreds of times a day, outranks a slow settings save.
- Separate "unacknowledged" (worst — feels broken), "unshaped" (blank or spinner), and "dishonest" (fake progress).
- For each, name the technique that fits: optimism, skeleton, prefetch, background, or honest progress.

## Phase 4 — Report
Create `PERCEIVED-SPEED.md` at repo root:
1. **Wait findings** — each: lens · interaction · file · what the user sees now · the treatment
2. **The hot path** — the core action's current feel, step by step, and its target
3. **Optimism candidates** — the reversible writes safe to show as done immediately
4. **Honesty fixes** — every progress indicator that overpromises

Start the report with today's date. If `PERCEIVED-SPEED.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every finding names what the user sees during the wait — observed, not assumed
- Optimistic UI is only recommended with its failure story: what the user sees when the write fails
- No interactive user-facing surface in this repo (pure library, batch pipeline)? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Before asking, present the top findings as a ranked list in plain words
- Report only — end by asking which wait to make disappear first
