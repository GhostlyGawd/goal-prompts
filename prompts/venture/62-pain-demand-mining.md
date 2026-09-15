---
id: "62"
title: Pain & Demand Mining
family: Venture
question: is it worth building?
output: DEMAND.md
example: /reports/DEMAND.md
tagline: Proof people actually hurt — verbatim complaints mined from reviews and forums, search and hiring signals, and what they already pay to make the pain stop.
---
# Goal: Pain & Demand Mining

Mission: Determine whether the selected pain is frequent, severe and connected to actual spending; complaints alone do not prove demand.

Read repo instructions, CHARTER.md and relevant notes/reports at root and in reports/. Charter constraints bound recommendations. In a conductor, read INDEX.md and venture-run.json for scope, criteria, decisions and input versions; otherwise record these in this report. Your only write is this report. No outreach, purchases or code changes.

## Phase 1 — Anchor
- State who hurts, when, doing what, using the selected venture and NICHE.md where applicable. Explicitly label missing inputs and provisional hypotheses.
- List sources where evidence should exist and the search budget before mining. Preserve decision bars; do not lower them after seeing evidence.

## Phase 2 — Investigate
1. **Complaints** — aim for 15–30 short accurate quotes from independent people, linked and dated. Respect quotation limits; report fewer with the reason rather than pad.
2. **Workarounds** — spreadsheets, automation, staff or services actually used; quantify costs only when supported.
3. **Spend** — evidence people buy a remedy, with buyer, amount and context; vendor pricing alone is not adoption.
4. **Signals** — search language and hiring needs; distinguish measured trends from impressions.
5. **Severity** — concrete lost time, revenue or operational consequences versus mild annoyance.
6. **Frequency** — recurring trigger and affected workflow; note sampling bias.
7. **Silence** — search coverage, missing evidence, restricted access and evidence against the hypothesis; absence is not automatically no demand.

## Phase 3 — Decide
- Grade severity, frequency, independent evidence and spend separately with scales and reasons. Show arithmetic if combining scores, and never average away an unmet hard bar.
- Give the strongest opposing interpretation equal effort. Recommend continue, refine/pivot, stop or gather evidence; distinguish unknown from demonstrated failure.

## Phase 4 — Report
Create `DEMAND.md` at repo root:
1. **Evidence wall** — source, short quote, date, sub-pain, independence and limitations.
2. **Spend/workarounds** — solution, cost, adoption evidence and unknowns.
3. **Assessment** — criteria versus evidence, counter-read and uncertainty.
4. **Next test** — where to reach ten relevant people, questions, success/stop criteria; no outreach.

Start with today's date. If `DEMAND.md` already exists, read it first and lead with what changed; preserve prior work before an authorized replacement. Include scope, input versions, stable finding IDs, evidence, counterevidence and next steps; use the conductor's metadata when supplied.

## Rules
- Separate direct evidence, proxies, inference and assumptions. Material factual claims need source links and access dates; date events too. Repeated citations are not independent evidence. Disclose inaccessible sources and shortfalls; never invent quotes or numbers.
- Include meaningful counterevidence and what would change the recommendation. Stop at the agreed research budget; if none, state a bounded search plan and unresolved gaps.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Before asking, present the top findings as a ranked list in plain words.
- No identifiable pain hypothesis after scope clarification? Write a one-paragraph null report. Sparse evidence for a defined pain instead yields an insufficient-evidence assessment.
- Report only — end by asking whether to continue, pivot the pain or gather evidence; record a necessary decision before dependent work.
