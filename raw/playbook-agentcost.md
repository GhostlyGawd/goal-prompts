# Playbook: Agent Cost Control (conductor)

You are working inside this repo. Mission: execute the **Agent Cost Control** playbook — 3 audit briefs in sequence, each producing one report file at this repo's root.

For AI-agent teams: the token economics of the loop, whether the model tier fits the job, and the context engineering that stops you paying for tokens you do not need.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **38 · Token Economics Audit** — fetch https://goal-prompts.vercel.app/raw/38.md → writes `TOKENS.md`
2. **36 · Model Strategy Review** — fetch https://goal-prompts.vercel.app/raw/36.md → writes `MODELS.md`
3. **33 · Context Engineering Audit** — fetch https://goal-prompts.vercel.app/raw/33.md → writes `CONTEXT.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
