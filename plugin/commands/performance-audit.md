---
description: "The broad latency pass — wasted renders, main-thread stalls, startup waterfalls — ranked by what the user actually feels on common paths."
---

# Goal: Performance Audit

You are working inside this repo. Mission: find where this product wastes time and bytes, and rank the wins by latency the user actually feels on common paths.

This is the broad pass across every layer. When the database is the suspect, go deep with 87; when the payload is, 88; when caching is, 140.

Read-only pass: build, measure, profile — but change nothing. Your only write is the report file.

## Phase 1 — Measure what's measurable
- Build the app; record bundle sizes and build time.
- Time the test suite and any measurable startup path.
- Identify the 3 heaviest pages/endpoints by code inspection: most data fetched, most rendered, most computed.

## Phase 2 — Audit through 7 lenses
Cite location and estimated cost for every finding.
1. **Payload** — bundle size, missing code-splitting, unoptimized images/fonts, oversized JSON responses
2. **Render waste** — unnecessary re-renders, unmemoized expensive work, layout thrash, long lists without virtualization
3. **Query cost** — N+1 patterns, over-fetching, queries in loops, missing indexes implied by access patterns
4. **Missing caches** — repeated identical fetches/computations with no memo or cache layer
5. **Main-thread blockers** — heavy synchronous work where users are waiting
6. **Startup cost** — cold-start waterfalls, sequential awaits that could be parallel, eager work that could be lazy
7. **Memory growth** — unbounded caches, retained references, growing arrays

## Phase 3 — Curate
- Rank by user-felt impact on common paths — not micro-benchmarks
- For each finding, estimate the gain: order of magnitude is fine (ms saved, kb removed)
- Kill anything that trades meaningful complexity for negligible gain

## Phase 4 — Report
Create `PERF.md` at repo root:
1. **Current numbers** — everything measured in Phase 1
2. **Findings** — each: Name · Location · Cost today (estimate) · Fix · Expected gain · Effort S/M/L
3. **Quick wins vs deep work** — the split, with the top quick win spelled out
4. **Measurement plan** — how to verify each gain after fixing

Start the report with today's date. If `PERF.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- A perf claim needs a number or a mechanism — no vibes
- Optimize the common path before the edge case
- No runtime hot paths in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which wins to take
