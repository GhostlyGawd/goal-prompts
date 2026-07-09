---
id: "51"
title: Latency Budget Audit
family: Speed
question: does it scale?
output: LATENCY.md
tagline: Where the seconds go. Decomposes p50 and p95 of the runs users feel into stages — queue, retrieval, first token, tools — and names the stage worth attacking.
---
# Goal: Latency Budget Audit

You are working inside this repo. Mission: decompose the latency of the runs users actually feel — p50 and p95, stage by stage — and name the stages worth attacking versus the ones already fine.

Read-only pass. Your only write is the report file. Read existing timers, traces, and logs where they exist; estimate from code where they don't.

## Phase 1 — Define the runs
- Pick the 1–3 user-facing runs that matter: a chat turn, a job, a page, a pipeline.
- Find what timing already exists — logs, traces, metrics, or nothing — and note precisely which stages are measurable today and which will be estimates.

## Phase 2 — Audit through 8 lenses
1. **Stage decomposition** — queue wait, retrieval, prompt assembly, time-to-first-token, generation, tool calls, post-processing: a number or an honest estimate for each
2. **The p95 gap** — what makes the slow tail slow: retries, cold starts, long inputs, contended resources; p95 is a different animal from p50 and gets its own diagnosis
3. **Serial that could be parallel** — awaits in sequence with no data dependency; fan-out opportunities in tool calls and retrieval
4. **Perceived vs actual** — time-to-first-token and streaming: what could render early; a fast-feeling eight seconds beats a silent five
5. **Payload fit** — prompt and context sizes versus need; the tokens that cost milliseconds on every single run
6. **Cache absences** — identical work done repeatedly: embeddings, tool results, static context blocks
7. **Timeout architecture** — per-stage budgets that fail fast, or one global timeout that ships the worst case to the user
8. **Instrumentation gaps** — the stages nobody can measure; you cannot attack what you cannot see

## Phase 3 — Curate
- Build the budget: stage · p50 · p95 · share of total · verdict (fine / attack).
- Rank attacks by seconds saved on the p95 path per unit of effort.

## Phase 4 — Report
Create `LATENCY.md` at repo root:
1. **The budget table** — the full decomposition, measured versus estimated flagged honestly
2. **The p95 story** — what the slow tail is made of
3. **Attacks** — ranked; parallelization and streaming usually beat micro-optimizations
4. **Instrumentation first** — the timers to add wherever an estimate stood in for a number

Start the report with today's date. If `LATENCY.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every number is labeled measured or estimated — never launder a guess
- Optimize the user's clock, not the flame graph's aesthetics
- No user-facing request path in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which attacks to make
