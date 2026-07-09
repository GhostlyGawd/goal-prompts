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

You are working inside this repo — the research workspace for this venture. Mission: build the honest map of everyone competing for this budget — direct, indirect, and the status quo — then find the gaps that are open because they are hard versus open because they are worthless.

Research pass: read the web and any reports at this root; your only write is the report file. Every factual claim carries a source link and access date.

## Phase 1 — Build the roster
- Enumerate the field: direct products, adjacent tools stretching in, agencies and consultants, internal builds, and doing-nothing. Scope from NICHE.md and DEMAND.md if present.
- For each, pull the primaries: homepage promise, pricing page, changelog or release cadence, review profiles, and public traction signals.

## Phase 2 — Tear down through 8 lenses
1. **Positioning claims** — each competitor's one-line promise in their own words, clustered; the words everyone uses are free differentiation for whoever stops using them
2. **Feature and pricing matrix** — capabilities × tiers × prices from their own pages; note the packaging tricks and what each hides behind Contact Us
3. **Their customers' complaints** — mine each vendor's negative reviews: shared gripes are market truths, unique gripes are that vendor's ceiling
4. **Traction proxies** — review counts and velocity, hiring, marketplace presence, community size; ranked, with sources
5. **The ignored segment** — who every vendor's pricing, onboarding, or language excludes; is that segment poor, or merely unfashionable
6. **Release pulse** — changelog cadence and direction; who is sprinting, who is coasting, who is in maintenance-mode decay
7. **Moat inspection** — what actually protects each incumbent: data, integrations, contracts, brand, switching costs — versus mere head start
8. **The kill zone** — what each incumbent could most easily copy from a new entrant, and how fast

## Phase 3 — Curate
- Name each gap and classify it: underserved (evidence of demand, weak supply) or unserved-for-a-reason.
- Pull the graveyard: prior startups that tried each gap, and what the record says killed them.

## Phase 4 — Report
Create `COMPETITORS.md` at repo root:
1. **The matrix** — roster with positioning, pricing, and traction
2. **Complaint synthesis** — market truths versus per-vendor ceilings
3. **Gap analysis** — gap · evidence it is real · why it is open · graveyard check
4. **The wedge shortlist** — the 2–3 entries a newcomer could actually win

Start the report with today's date. If `COMPETITORS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Their pages and their customers' words — never marketing-versus-marketing speculation
- Every gap must survive the why-is-this-open question in writing
- No discernible product or idea to research in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which gap to build positioning around
