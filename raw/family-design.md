# Playbook: All Design briefs (conductor)

You are working inside this repo. Mission: execute the **All Design briefs** playbook — 7 audit briefs in sequence, each producing one report file at this repo's root.

Every Design brief in the catalog, in order — 54 through 77, one report each.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **54 · Visual Hierarchy Audit** — fetch https://goal-prompts.vercel.app/raw/54.md → writes `HIERARCHY.md`
2. **55 · Typography Audit** — fetch https://goal-prompts.vercel.app/raw/55.md → writes `TYPOGRAPHY.md`
3. **56 · Color & Contrast Audit** — fetch https://goal-prompts.vercel.app/raw/56.md → writes `COLOR.md`
4. **57 · Spacing & Layout Audit** — fetch https://goal-prompts.vercel.app/raw/57.md → writes `LAYOUT.md`
5. **58 · Interaction States & Motion Audit** — fetch https://goal-prompts.vercel.app/raw/58.md → writes `STATES.md`
6. **59 · Brand Coherence Audit** — fetch https://goal-prompts.vercel.app/raw/59.md → writes `BRAND.md`
7. **77 · Show, Don't Tell** — fetch https://goal-prompts.vercel.app/raw/77.md → writes `SHOWCASE.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
