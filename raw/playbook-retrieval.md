# Playbook: Retrieval Tune-Up (conductor)

You are working inside this repo. Mission: execute the **Retrieval Tune-Up** playbook — 3 audit briefs in sequence, each producing one report file at this repo's root.

Make RAG answers better: see what enters the window, audit the retrieval pipeline, then lock quality with evals.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **33 · Context Engineering Audit** — fetch https://goal-prompts.vercel.app/raw/33.md → writes `CONTEXT.md`
2. **49 · Retrieval Quality Audit** — fetch https://goal-prompts.vercel.app/raw/49.md → writes `RETRIEVAL.md`
3. **34 · Eval Coverage Audit** — fetch https://goal-prompts.vercel.app/raw/34.md → writes `EVALS.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
