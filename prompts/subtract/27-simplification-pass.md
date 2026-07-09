---
id: "27"
title: Simplification Pass
family: Subtract
question: what should go?
output: SIMPLIFY.md
tagline: Abstractions with one implementation, pass-through layers, config nobody changes — ranked by clarity gained per risk.
---
# Goal: Simplification Pass

You are working inside this repo. Mission: find the complexity that isn't earning its keep — abstractions with one implementation, layers that only forward, flexibility nobody uses — and rank the simplifications by clarity gained per risk taken.

Read-only pass. Your only write is the report file.

## Phase 1 — Find where understanding is expensive
- Pick 2–3 core features and trace them end to end. Count the hops: files touched, layers crossed, indirections followed to answer "where does this actually happen?"
- Note where you had to hold the most in your head. That's where simplification pays.

## Phase 2 — Audit through 7 lenses
1. **One-implementation abstractions** — interfaces, base classes, and strategy patterns with exactly one concrete case
2. **Pass-through layers** — functions and services that only forward to another with no added value
3. **Frozen config** — options and parameters that have had one value forever: inline them
4. **Unused flexibility** — generalization for cases that never arrived; plugin systems with one plugin
5. **Stored derivables** — state that's cached-and-synced when it could simply be computed
6. **Cleverness tax** — code requiring archaeology to decode, where the boring version is 3 lines longer and instantly clear
7. **Imported ceremony** — patterns sized for a 200-engineer org living in a small codebase

## Phase 3 — Curate
- For each: current shape → simpler shape, lines removed, hops removed, risk
- Also list complexity that EARNS its place — load-bearing abstraction to explicitly keep

## Phase 4 — Report
Create `SIMPLIFY.md` at repo root:
1. **Hop counts** — the traced features and their indirection tally, before
2. **Simplifications** — each: location · current → simpler · lines/hops removed · risk · effort
3. **Ranked by clarity-per-risk**
4. **Keep list** — complexity that's justified, so nobody "simplifies" it later
5. **Before/after sketch** — the top item shown both ways

Start the report with today's date. If `SIMPLIFY.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Simple means fewer concepts to hold, not fewer characters
- Never remove flexibility that's actually exercised — check callers first
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which simplifications to make
