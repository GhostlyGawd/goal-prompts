# Playbook: All Agent briefs (conductor)

You are working inside this repo. Mission: execute the **All Agent briefs** playbook — 12 audit briefs in sequence, each producing one report file at this repo's root.

Every brief in the Agent family, run in sequence.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **30 · Prompt & Instruction Audit** — fetch https://goal-prompts.vercel.app/raw/30.md → writes `PROMPTS.md`
2. **31 · Tool Design Review** — fetch https://goal-prompts.vercel.app/raw/31.md → writes `TOOLS.md`
3. **32 · Loop & Termination Audit** — fetch https://goal-prompts.vercel.app/raw/32.md → writes `LOOPS.md`
4. **33 · Context Engineering Audit** — fetch https://goal-prompts.vercel.app/raw/33.md → writes `CONTEXT.md`
5. **34 · Eval Coverage Audit** — fetch https://goal-prompts.vercel.app/raw/34.md → writes `EVALS.md`
6. **35 · Guardrails Audit** — fetch https://goal-prompts.vercel.app/raw/35.md → writes `GUARDRAILS.md`
7. **36 · Model Strategy Review** — fetch https://goal-prompts.vercel.app/raw/36.md → writes `MODELS.md`
8. **37 · Trace & Replay Audit** — fetch https://goal-prompts.vercel.app/raw/37.md → writes `TRACES.md`
9. **38 · Token Economics Audit** — fetch https://goal-prompts.vercel.app/raw/38.md → writes `TOKENS.md`
10. **48 · Memory & State Audit** — fetch https://goal-prompts.vercel.app/raw/48.md → writes `MEMORY.md`
11. **49 · Retrieval Quality Audit** — fetch https://goal-prompts.vercel.app/raw/49.md → writes `RETRIEVAL.md`
12. **50 · Multi-Agent Topology Review** — fetch https://goal-prompts.vercel.app/raw/50.md → writes `TOPOLOGY.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
