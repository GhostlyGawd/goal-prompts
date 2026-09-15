---
id: "63"
title: Competitor Teardown
family: Venture
question: is it worth building?
output: COMPETITORS.md
example: /examples/venture/COMPETITORS.md
tagline: Everyone already fighting for this money — features, pricing, positioning, and traction compared, their customers' complaints mined, and the gaps nobody covers.
---
# Goal: Competitor Teardown

Mission: Find defensible entry gaps among everyone competing for the selected buyer’s budget.

Read repo instructions, CHARTER.md and relevant notes/reports at root and in reports/. Charter constraints bound recommendations. In a conductor, read INDEX.md and venture-run.json for scope, criteria, decisions and input versions; otherwise record these in this report. Your only write is this report. No outreach, purchases or code changes.

## Phase 1 — Anchor
- Read applicable NICHE.md and DEMAND.md; freeze buyer, pain and budget. Missing inputs reduce confidence; do not substitute another venture.
- Bound the roster to relevant direct products, adjacent tools, agencies, internal builds and doing nothing. Record selection/search limits.

## Phase 2 — Investigate
1. **Promises** — short attributed homepage claims, clustered by buyer and job.
2. **Pricing/features** — capabilities, billing units, tiers and pricing dates from primary pages; mark Contact Us as unknown.
3. **Complaints** — distinguish cross-vendor problems from one vendor’s defects; note review bias.
4. **Traction** — reviews, hiring, community and marketplace presence as proxies, not revenue or market share.
5. **Excluded buyers** — evidence of both unmet need and ability to pay.
6. **Release activity** — dated changelogs and direction; no unsupported abandonment claims.
7. **Defenses** — contracts, switching costs, integrations, data or distribution with mechanisms.
8. **Response/graveyard** — likely incumbent copying and prior attempts; separate documented failure causes from inference.

## Phase 3 — Decide
- Classify gaps as underserved, unserved-for-a-reason or unknown. Require evidence of demand plus weak supply before calling a gap an opportunity.
- Rank two or three wedges if supported; explain what invalidates each and conflicts with earlier reports.

## Phase 4 — Report
Create `COMPETITORS.md` at repo root:
1. **Matrix** — scope, roster, promise, pricing and traction proxies.
2. **Complaint synthesis** — evidence and sampling limitations.
3. **Gap analysis** — demand, supply, why open, prior attempts and counterevidence.
4. **Wedge shortlist** — recommendation and cheapest disconfirming test, budget and success/stop criteria.

Start with today's date. If `COMPETITORS.md` already exists, read it first and lead with what changed; preserve prior work before an authorized replacement. Include scope, input versions, stable finding IDs, evidence, counterevidence and next steps; use the conductor's metadata when supplied.

## Rules
- Separate direct evidence, proxies, inference and assumptions. Material factual claims need source links and access dates; date events too. Repeated citations are not independent evidence. Disclose inaccessible sources and shortfalls; never invent quotes or numbers.
- Include meaningful counterevidence and what would change the recommendation. Stop at the agreed research budget; if none, state a bounded search plan and unresolved gaps.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Before asking, present the top findings as a ranked list in plain words.
- No defined buyer/pain to compare after clarification? Write a one-paragraph null report with the missing prerequisite. An inaccessible pricing page is an unknown, not a null market.
- Report only — end by asking which gap merits further evaluation; do not change the venture without recorded authority.
