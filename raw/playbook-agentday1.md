# Playbook: Agent Day-1 (conductor)

You are working inside this repo. Mission: execute the **Agent Day-1** playbook — 4 audit briefs in sequence, each producing one report file at this repo's root.

First contact with an agent codebase: read its mind, its hands, its loops, its traces.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **30 · Prompt & Instruction Audit** — fetch https://goal-prompts.vercel.app/raw/30.md → writes `PROMPTS.md`
2. **31 · Tool Design Review** — fetch https://goal-prompts.vercel.app/raw/31.md → writes `TOOLS.md`
3. **32 · Loop & Termination Audit** — fetch https://goal-prompts.vercel.app/raw/32.md → writes `LOOPS.md`
4. **37 · Trace & Replay Audit** — fetch https://goal-prompts.vercel.app/raw/37.md → writes `TRACES.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
