---
name: goal-market-size-timing
description: "Bottom-up sizing with the arithmetic shown, growth read from primary signals, and the why-now case argued both ways — no analyst-deck TAM theater. Audit brief 64 · Venture — runs a four-phase audit of the current repo and writes MARKET.md at the repo root."
---

# Goal: Market Size & Timing

You are working inside this repo — the research workspace for this venture. Mission: size this market from the bottom up — countable buyers × plausible price — and judge the timing: what changed that makes this possible or urgent now, and what says it is early or late.

Research pass: read the web and any reports at this root; your only write is the report file. Every factual claim carries a source link and access date.

## Phase 1 — Define the unit
- Define the buyer unit precisely — a company of type X, a professional in role Y — and the annual-value hypothesis per unit.
- Gather countable proxies: directories, associations, job-title counts, marketplace install counts, industry statistics — sources someone could actually enumerate.

## Phase 2 — Audit through 7 lenses
1. **Bottom-up count** — buyers reachable in the wedge segment, then the expansion rings; every input sourced, every multiplication written out
2. **Top-down sanity check** — published market figures used only to bound the bottom-up, never to replace it; explain any large gap between the two
3. **Growth reading** — the countables over time: hiring trends, search-interest direction, community growth, funding flowing into the space
4. **Why now** — the enabling shifts, with dates: a capability that got cheap, a regulation that landed, a behavior that changed; what exactly was impossible or unnecessary three years ago
5. **Why not before** — prior attempts and precisely which constraint killed them; verify that constraint is actually gone rather than merely older
6. **Window shape** — is early advantage real here (compounding data, standards, land-grab) or is fast-follow the smarter seat
7. **Concentration risk** — a thousand small checks or five big ones; the platform dependencies that could reprice the whole market overnight

## Phase 3 — Curate
- State the obtainable market for years one and two as a range, assumptions explicit.
- Write the bear case with the same rigor as the bull; this report exists to be wrong early and cheaply.

## Phase 4 — Report
Create `MARKET.md` at repo root:
1. **The arithmetic** — the bottom-up model, every input sourced
2. **Growth and timing** — the why-now case and its strongest rebuttal, side by side
3. **The window** — the mover-advantage verdict with reasoning
4. **Sensitivity** — the single assumption that, if wrong, most changes the answer

Start the report with today's date. If `MARKET.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Show every multiplication; a number without visible arithmetic is a vibe
- Bull and bear get equal effort
- No discernible product or idea to research in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking whether size and timing justify the next brief
