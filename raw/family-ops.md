# Playbook: All Ops briefs (conductor)

You are working inside this repo. Mission: execute the **All Ops briefs** playbook — 4 audit briefs in sequence, each producing one report file at this repo's root.

Every Ops brief in the catalog, in order — 23 through 53, one report each.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **23 · Release Pipeline Audit** — fetch https://goal-prompts.vercel.app/raw/23.md → writes `RELEASE.md`
2. **24 · Cost Audit** — fetch https://goal-prompts.vercel.app/raw/24.md → writes `COSTS.md`
3. **25 · Incident Readiness Review** — fetch https://goal-prompts.vercel.app/raw/25.md → writes `RELIABILITY.md`
4. **53 · Config & Environment Audit** — fetch https://goal-prompts.vercel.app/raw/53.md → writes `CONFIG.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
