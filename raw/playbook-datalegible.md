# Playbook: Make Data Legible (conductor)

You are working inside this repo. Mission: execute the **Make Data Legible** playbook — 4 audit briefs in sequence, each producing one report file at this repo's root.

The visualization pass: make every chart tell the truth, every dashboard answer its question at a glance, the number that matters win the eye, and the palette stay readable for everyone.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **131 · Data Visualization Audit** — fetch https://goal-prompts.vercel.app/raw/131.md → writes `DATAVIZ.md`
2. **132 · Dashboard & Density Audit** — fetch https://goal-prompts.vercel.app/raw/132.md → writes `DASHBOARD.md`
3. **54 · Visual Hierarchy Audit** — fetch https://goal-prompts.vercel.app/raw/54.md → writes `HIERARCHY.md`
4. **56 · Color & Contrast Audit** — fetch https://goal-prompts.vercel.app/raw/56.md → writes `COLOR.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
