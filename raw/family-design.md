# Playbook: All Design briefs (conductor)

You are working inside this repo. Mission: execute the **All Design briefs** playbook — 15 audit briefs in sequence, each producing one report file at the repo root (or in `reports/`, if the repo has that directory).

Every Design brief in the catalog, in order — 54 through 134, one report each.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. If your harness can run subagents or fresh sessions, run each stage in one — a stage needs only the earlier report files at the repo root and in `reports/`, never this conversation.
3. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
4. Confirm the report file exists (at the repo root or in `reports/`) before moving on.
5. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **54 · Visual Hierarchy Audit** — fetch https://goal-prompts.vercel.app/raw/54.md → writes `HIERARCHY.md`
2. **55 · Typography Audit** — fetch https://goal-prompts.vercel.app/raw/55.md → writes `TYPOGRAPHY.md`
3. **56 · Color & Contrast Audit** — fetch https://goal-prompts.vercel.app/raw/56.md → writes `COLOR.md`
4. **57 · Spacing & Layout Audit** — fetch https://goal-prompts.vercel.app/raw/57.md → writes `LAYOUT.md`
5. **58 · Interaction States & Motion Audit** — fetch https://goal-prompts.vercel.app/raw/58.md → writes `STATES.md`
6. **59 · Brand Coherence Audit** — fetch https://goal-prompts.vercel.app/raw/59.md → writes `BRAND.md`
7. **77 · Show, Don't Tell** — fetch https://goal-prompts.vercel.app/raw/77.md → writes `SHOWCASE.md`
8. **104 · Mobile & Responsive Audit** — fetch https://goal-prompts.vercel.app/raw/104.md → writes `MOBILE.md`
9. **105 · Design-Token Adoption Audit** — fetch https://goal-prompts.vercel.app/raw/105.md → writes `TOKEN-ADOPTION.md`
10. **129 · Navigation & Wayfinding Audit** — fetch https://goal-prompts.vercel.app/raw/129.md → writes `NAVIGATION.md`
11. **130 · Menu & Command Surface Audit** — fetch https://goal-prompts.vercel.app/raw/130.md → writes `MENUS.md`
12. **131 · Data Visualization Audit** — fetch https://goal-prompts.vercel.app/raw/131.md → writes `DATAVIZ.md`
13. **132 · Dashboard & Density Audit** — fetch https://goal-prompts.vercel.app/raw/132.md → writes `DASHBOARD.md`
14. **133 · Empty & Zero-Data States Audit** — fetch https://goal-prompts.vercel.app/raw/133.md → writes `EMPTYSTATES.md`
15. **134 · Iconography & Visual Language Audit** — fetch https://goal-prompts.vercel.app/raw/134.md → writes `ICONOGRAPHY.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge the reports at the repo root and in `reports/` into one sequenced plan.

## Rules
- If a fetch fails, retry once; if it still fails, use the locally installed /goal:<slug> (or /goal-<slug>) command or the goal-prompts MCP get_brief tool for that stage; if neither exists, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists (at the repo root or in `reports/`), ask whether to re-run or skip that stage.
- A conductor caps at 16 stages — for a longer campaign, split it into two conductors and run them back-to-back.
