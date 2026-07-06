# Playbook: Day-1 New Repo (conductor)

You are working inside this repo. Mission: execute the **Day-1 New Repo** playbook — 4 audit briefs in sequence, each producing one report file at this repo's root.

First contact with an unfamiliar codebase: what is it, is it broken, is it safe, can I work on it.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **00 · Product Improvement Discovery** — fetch https://goal-prompts.vercel.app/raw/00.md → writes `IMPROVEMENTS.md`
2. **01 · Bug Hunt** — fetch https://goal-prompts.vercel.app/raw/01.md → writes `BUGS.md`
3. **06 · Security & Privacy Audit** — fetch https://goal-prompts.vercel.app/raw/06.md → writes `SECURITY.md`
4. **14 · New-Dev Onboarding Audit** — fetch https://goal-prompts.vercel.app/raw/14.md → writes `DX.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
