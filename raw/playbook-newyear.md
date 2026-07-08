# Playbook: New-Year Reset (conductor)

You are working inside this repo. Mission: execute the **New-Year Reset** playbook — 4 audit briefs in sequence, each producing one report file at this repo's root.

A themed start-of-year sweep: read the vitals, prune the dead weight, simplify what remains, and synthesize next year's roadmap — one seasonal bundle.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **29 · Recurring Health Check** — fetch https://goal-prompts.vercel.app/raw/29.md → writes `HEALTH.md`
2. **26 · Prune Audit** — fetch https://goal-prompts.vercel.app/raw/26.md → writes `PRUNE.md`
3. **27 · Simplification Pass** — fetch https://goal-prompts.vercel.app/raw/27.md → writes `SIMPLIFY.md`
4. **28 · Roadmap Synthesis** — fetch https://goal-prompts.vercel.app/raw/28.md → writes `ROADMAP.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
