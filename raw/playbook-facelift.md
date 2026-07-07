# Playbook: Face-Lift (conductor)

You are working inside this repo. Mission: execute the **Face-Lift** playbook — 5 audit briefs in sequence, each producing one report file at this repo's root.

The visual overhaul: hierarchy first, then layout, type, and color — and the Fixer turns the findings into commits.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **54 · Visual Hierarchy Audit** — fetch https://goal-prompts.vercel.app/raw/54.md → writes `HIERARCHY.md`
2. **57 · Spacing & Layout Audit** — fetch https://goal-prompts.vercel.app/raw/57.md → writes `LAYOUT.md`
3. **55 · Typography Audit** — fetch https://goal-prompts.vercel.app/raw/55.md → writes `TYPOGRAPHY.md`
4. **56 · Color & Contrast Audit** — fetch https://goal-prompts.vercel.app/raw/56.md → writes `COLOR.md`
5. **47 · The Fixer** — fetch https://goal-prompts.vercel.app/raw/47.md → writes `FIXLOG.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
