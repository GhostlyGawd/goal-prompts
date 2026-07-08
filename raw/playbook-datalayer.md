# Playbook: Data-Layer Tune-Up (conductor)

You are working inside this repo. Mission: execute the **Data-Layer Tune-Up** playbook — 3 audit briefs in sequence, each producing one report file at this repo's root.

The runtime data layer, end to end: the queries that will not scale, the integrity the schema does not enforce, and whether you could actually recover from data loss.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **87 · Query Performance & N+1 Audit** — fetch https://goal-prompts.vercel.app/raw/87.md → writes `QUERIES.md`
2. **89 · Data Integrity Audit** — fetch https://goal-prompts.vercel.app/raw/89.md → writes `INTEGRITY.md`
3. **91 · Backup & Recovery Audit** — fetch https://goal-prompts.vercel.app/raw/91.md → writes `RECOVERY.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
