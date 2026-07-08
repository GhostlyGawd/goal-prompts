# Playbook: All AI-Ethics briefs (conductor)

You are working inside this repo. Mission: execute the **All AI-Ethics briefs** playbook — 5 audit briefs in sequence, each producing one report file at this repo's root.

Every AI-Ethics brief in the catalog, in order — 116 through 120, one report each.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **116 · Bias & Fairness Audit** — fetch https://goal-prompts.vercel.app/raw/116.md → writes `FAIRNESS.md`
2. **117 · Hallucination & Grounding Audit** — fetch https://goal-prompts.vercel.app/raw/117.md → writes `GROUNDING.md`
3. **118 · Prompt-Injection Red-Team** — fetch https://goal-prompts.vercel.app/raw/118.md → writes `REDTEAM.md`
4. **119 · Model Transparency Audit** — fetch https://goal-prompts.vercel.app/raw/119.md → writes `TRANSPARENCY.md`
5. **120 · Training-Data Provenance** — fetch https://goal-prompts.vercel.app/raw/120.md → writes `PROVENANCE.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
