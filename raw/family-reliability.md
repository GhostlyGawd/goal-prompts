# Playbook: All Reliability briefs (conductor)

You are working inside this repo. Mission: execute the **All Reliability briefs** playbook — 4 audit briefs in sequence, each producing one report file at this repo's root.

Every Reliability brief in the catalog, in order — 121 through 124, one report each.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **121 · Graceful Degradation Audit** — fetch https://goal-prompts.vercel.app/raw/121.md → writes `DEGRADE.md`
2. **122 · Failure-Injection Readiness** — fetch https://goal-prompts.vercel.app/raw/122.md → writes `CHAOS.md`
3. **123 · Capacity & Scalability Audit** — fetch https://goal-prompts.vercel.app/raw/123.md → writes `CAPACITY.md`
4. **124 · Abuse & Overload Protection** — fetch https://goal-prompts.vercel.app/raw/124.md → writes `ABUSE.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
