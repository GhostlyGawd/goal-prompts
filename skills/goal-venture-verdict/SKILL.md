---
name: goal-venture-verdict
description: "The decider. Reads every venture report at this root, scores the candidate against bars set before scoring, and rules go, pivot, or kill — reasoning shown. Audit brief 67 · Venture — runs a four-phase audit of the current repo and writes VERDICT.md at the repo root."
---

# Goal: Venture Verdict

You are working inside this repo — the research workspace for this venture. Mission: read every venture-research report at this root and rule — go, pivot, or kill — against explicit bars written before scoring, so the decision is made by evidence rather than by sunk enthusiasm.

Synthesis pass: work from the reports, dipping into the web only to resolve conflicts. Your only write is the report file.

## Phase 1 — Collect and set the bars
- Inventory the reports: OPPORTUNITIES, NICHE, DEMAND, COMPETITORS, MARKET, POSITIONING, MOAT. Note what is missing and whether a verdict survives the absence.
- Before reading any conclusions, write the bars: minimum evidence of pain, minimum reachable buyers, maximum competitive heat, required why-now strength, acceptable kill risks. Bars first, scores second — that ordering is the entire point of this brief.

## Phase 2 — Score through 6 lenses
1. **Pain reality** — DEMAND's evidence wall against its bar: verbatim density, recency, and spend proof
2. **Path to ten customers** — a nameable route from the watering holes in NICHE to the beachhead in POSITIONING; if the first ten buyers cannot be described as types-with-addresses, that is the finding
3. **Competitive survivability** — the chosen wedge against the incumbent-response read in MOAT; who blinks
4. **Economics floor** — the napkin at conservative inputs, still worth the operator's time or not
5. **Timing conviction** — the why-now case net of its own rebuttal in MARKET
6. **Disconfirmation audit** — did every report's bear case get real effort; quote the strongest objections still standing

## Phase 3 — Curate
- Score each bar; no averaging away a failed one. A single hard fail is a kill or a pivot — name which, and if a pivot, name the axis: customer, pain, or product.
- Separate what the evidence says from what the operator hopes; both belong in the report, labeled.

## Phase 4 — Report
Create `VERDICT.md` at repo root:
1. **The bars** — exactly as written before scoring
2. **The scorecard** — bar versus evidence, report by report
3. **The ruling** — go, pivot (with axis), or kill, in one paragraph of plain reasoning
4. **If go** — the first three actions and the tripwires from MOAT; if kill — what this research taught that transfers to the next candidate

Start the report with today's date. If `VERDICT.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Bars are set before evidence is weighed and never adjusted afterward
- A verdict that ignores a hard fail is not a verdict
- No venture-research reports to rule on in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking whether the operator accepts the ruling or wants a bar challenged
