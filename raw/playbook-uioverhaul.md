# Playbook: Total UI Overhaul (conductor)

You are working inside this repo. Mission: execute the **Total UI Overhaul** playbook — 6 audit briefs in sequence, each producing one report file at this repo's root.

The interaction-and-UI sweep: navigation, menus, every interactive state, the empty screens, and the icon language — then the Fixer turns the findings into verified commits.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **129 · Navigation & Wayfinding Audit** — fetch https://goal-prompts.vercel.app/raw/129.md → writes `NAVIGATION.md`
2. **130 · Menu & Command Surface Audit** — fetch https://goal-prompts.vercel.app/raw/130.md → writes `MENUS.md`
3. **58 · Interaction States & Motion Audit** — fetch https://goal-prompts.vercel.app/raw/58.md → writes `STATES.md`
4. **133 · Empty & Zero-Data States Audit** — fetch https://goal-prompts.vercel.app/raw/133.md → writes `EMPTYSTATES.md`
5. **134 · Iconography & Visual Language Audit** — fetch https://goal-prompts.vercel.app/raw/134.md → writes `ICONOGRAPHY.md`
6. **47 · The Fixer** — fetch https://goal-prompts.vercel.app/raw/47.md → writes `FIXLOG.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
