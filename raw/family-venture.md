# Playbook: All Venture briefs (conductor)

You are working inside this repo. Mission: execute the **All Venture briefs** playbook — 8 audit briefs in sequence, each producing one report file at this repo's root.

Every Venture brief in the catalog, in order — 60 through 67, one report each.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **60 · Opportunity Scan** — fetch https://goal-prompts.vercel.app/raw/60.md → writes `OPPORTUNITIES.md`
2. **61 · Niche Map** — fetch https://goal-prompts.vercel.app/raw/61.md → writes `NICHE.md`
3. **62 · Pain & Demand Mining** — fetch https://goal-prompts.vercel.app/raw/62.md → writes `DEMAND.md`
4. **63 · Competitor Teardown** — fetch https://goal-prompts.vercel.app/raw/63.md → writes `COMPETITORS.md`
5. **64 · Market Size & Timing** — fetch https://goal-prompts.vercel.app/raw/64.md → writes `MARKET.md`
6. **65 · Positioning & Wedge** — fetch https://goal-prompts.vercel.app/raw/65.md → writes `POSITIONING.md`
7. **66 · Moat & Model Check** — fetch https://goal-prompts.vercel.app/raw/66.md → writes `MOAT.md`
8. **67 · Venture Verdict** — fetch https://goal-prompts.vercel.app/raw/67.md → writes `VERDICT.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
