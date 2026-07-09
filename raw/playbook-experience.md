# Playbook: Experience Optimization (conductor)

You are working inside this repo. Mission: execute the **Experience Optimization** playbook — 7 audit briefs in sequence, each producing one report file at the repo root (or in `reports/`, if the repo has that directory).

Get it, want it, keep it — walk every surface a visitor meets and optimize the whole experience: does a newcomer understand it, are the benefits shown not told, do the conversion surfaces and their proof earn the yes, does the first session land a win, and does anything bring them back — then the Fixer ships the biggest lifts as commits.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. If your harness can run subagents or fresh sessions, run each stage in one — a stage needs only the earlier report files at the repo root and in `reports/`, never this conversation.
3. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
4. Confirm the report file exists (at the repo root or in `reports/`) before moving on.
5. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **76 · Comprehension Audit** — fetch https://goal-prompts.vercel.app/raw/76.md → writes `COMPREHENSION.md`
2. **77 · Show, Don't Tell** — fetch https://goal-prompts.vercel.app/raw/77.md → writes `SHOWCASE.md`
3. **75 · Conversion Rate Optimization** — fetch https://goal-prompts.vercel.app/raw/75.md → writes `CRO.md`
4. **79 · Social Proof & Credibility** — fetch https://goal-prompts.vercel.app/raw/79.md → writes `PROOF.md`
5. **80 · Activation & First-Win Audit** — fetch https://goal-prompts.vercel.app/raw/80.md → writes `ACTIVATION.md`
6. **78 · Retention & Lifecycle Audit** — fetch https://goal-prompts.vercel.app/raw/78.md → writes `RETENTION.md`
7. **47 · The Fixer** — fetch https://goal-prompts.vercel.app/raw/47.md → writes `FIXLOG.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge the reports at the repo root and in `reports/` into one sequenced plan.

## Rules
- If a fetch fails, retry once; if it still fails, use the locally installed /goal command or the goal-prompts MCP get_brief tool for that stage; if neither exists, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists (at the repo root or in `reports/`), ask whether to re-run or skip that stage.
- A conductor caps at 16 stages — for a longer campaign, split it into two conductors and run them back-to-back.
