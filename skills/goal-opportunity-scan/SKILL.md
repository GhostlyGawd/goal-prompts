---
name: goal-opportunity-scan
description: "The candidate field. Turns your edges, interests, and constraints plus live market signals into 10-15 scored venture candidates — divergence before any deep dive. Goal Prompt 60 · Venture — inspects the current repo and writes OPPORTUNITIES.md at the repo root."
---

# Goal: Opportunity Scan

Mission: Generate and compare venture candidates that fit the operator, or assess an already selected venture without silently replacing it.

Read repo instructions, CHARTER.md and relevant notes/reports at root and in reports/. Charter constraints bound recommendations. In a conductor, read INDEX.md and venture-run.json for scope, criteria, decisions and input versions; otherwise record these in this report. Your only write is this report. No outreach, purchases or code changes.

## Phase 1 — Anchor
- Establish skills, audience/access, time, capital, goals and exclusions. Use supplied context; ask for missing constraints that change selection. An empty codebase is valid. Do not invent a founder persona.
- Record discovery versus evaluation mode and decision bars before research conclusions. Label bars retrospective if prior conclusions were seen. For an existing venture, keep it fixed unless a switch is authorized.

## Phase 2 — Investigate
1. **Complaints** — recurring task failures, linked to real people and current workarounds.
2. **Shifts** — dated technical, behavioral, regulatory or platform changes; why they enable an entry now.
3. **Unbundling** — expensive bundles or fragmented workflows with observable switching demand.
4. **Transfer** — practices useful in one industry that might solve an evidenced problem in another.
5. **Infrastructure** — recurring needs behind a growing activity, with reachable buyers.
6. **Operator edge** — specific access, distribution or expertise; distinguish known assets from assumptions.
7. **Incumbent decay** — verified complaints and release history, without equating silence to abandonment.
8. **Disconfirmation** — failed attempts, switching barriers and evidence the buyer will not pay.

## Phase 3 — Decide
- In discovery, aim for 10–15 distinct candidates if evidence supports them; explain shortfalls. Score pain, reachability, operator fit and timing 1–5 (higher is better); score competitive pressure separately (higher is worse). Justify each score; do not hide hard failures in totals.
- Recommend one candidate against the top alternatives. Selection requires the operator or explicit delegation; record authority before deep research.

## Phase 4 — Report
Create `OPPORTUNITIES.md` at repo root:
1. **Operator and bars** — resources, constraints, assumptions and criteria with timing.
2. **Field** — candidate ID, buyer, pain, solution hypothesis, geography, evidence and scores.
3. **Shortlist** — top three with strongest counterevidence; fewer if justified.
4. **Next decision** — recommended candidate, tradeoff, selection authority and cheapest test with success/stop criteria.

Start with today's date. If `OPPORTUNITIES.md` already exists, read it first and lead with what changed; preserve prior work before an authorized replacement. Include scope, input versions, stable finding IDs, evidence, counterevidence and next steps; use the conductor's metadata when supplied.

## Rules
- Separate direct evidence, proxies, inference and assumptions. Material factual claims need source links and access dates; date events too. Repeated citations are not independent evidence. Disclose inaccessible sources and shortfalls; never invent quotes or numbers.
- Include meaningful counterevidence and what would change the recommendation. Stop at the agreed research budget; if none, state a bounded search plan and unresolved gaps.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Before asking, present the top findings as a ranked list in plain words.
- No usable operator context or research direction after intake? Write a one-paragraph null report explaining what is needed; do not treat absence of product code as inapplicability.
- Report only — end by asking which candidate to select; use a selection already supplied or explicitly delegated.
