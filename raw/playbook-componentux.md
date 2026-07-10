# Playbook: Component UX (conductor)

You are working inside this repo. Mission: execute the **Component UX** playbook — 5 audit briefs in sequence, each producing one report file at the repo root (or in `reports/`, if the repo has that directory).

Audit the workhorse UI components one by one — the overlays that interrupt, the tables people work in, the microcopy that guides, and every interactive state — then the Fixer turns the findings into verified commits.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. If your harness can run subagents or fresh sessions, run each stage in one — a stage needs only the earlier report files at the repo root and in `reports/`, never this conversation.
3. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
4. Confirm the report file exists (at the repo root or in `reports/`) before moving on.
5. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **146 · Modal, Dialog & Overlay Audit** — fetch https://goal-prompts.vercel.app/raw/146.md → writes `OVERLAYS.md`
2. **147 · Tables & Data-Grid Audit** — fetch https://goal-prompts.vercel.app/raw/147.md → writes `TABLES.md`
3. **148 · UI Microcopy & Labeling Audit** — fetch https://goal-prompts.vercel.app/raw/148.md → writes `MICROCOPY.md`
4. **58 · Interaction States & Motion Audit** — fetch https://goal-prompts.vercel.app/raw/58.md → writes `STATES.md`
5. **47 · The Fixer** — fetch https://goal-prompts.vercel.app/raw/47.md → writes `FIXLOG.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge the reports at the repo root and in `reports/` into one sequenced plan.

## Rules
- If a fetch fails, retry once; if it still fails, use the locally installed /goal:<slug> (or /goal-<slug>) command or the goal-prompts MCP get_brief tool for that stage; if neither exists, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists (at the repo root or in `reports/`), ask whether to re-run or skip that stage.
- A conductor caps at 16 stages — for a longer campaign, split it into two conductors and run them back-to-back.
