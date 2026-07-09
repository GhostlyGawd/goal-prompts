# Playbook: All Clarity briefs (conductor)

You are working inside this repo. Mission: execute the **All Clarity briefs** playbook — 6 audit briefs in sequence, each producing one report file at the repo root (or in `reports/`, if the repo has that directory).

Every Clarity brief in the catalog, in order — 16 through 135, one report each.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. If your harness can run subagents or fresh sessions, run each stage in one — a stage needs only the earlier report files at the repo root and in `reports/`, never this conversation.
3. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
4. Confirm the report file exists (at the repo root or in `reports/`) before moving on.
5. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **16 · Documentation Audit** — fetch https://goal-prompts.vercel.app/raw/16.md → writes `DOCS.md`
2. **17 · Copy & Voice Audit** — fetch https://goal-prompts.vercel.app/raw/17.md → writes `COPY.md`
3. **18 · API Contract Review** — fetch https://goal-prompts.vercel.app/raw/18.md → writes `API.md`
4. **76 · Comprehension Audit** — fetch https://goal-prompts.vercel.app/raw/76.md → writes `COMPREHENSION.md`
5. **103 · Error-Message Audit** — fetch https://goal-prompts.vercel.app/raw/103.md → writes `ERRORS.md`
6. **135 · CLI Tool UX Audit** — fetch https://goal-prompts.vercel.app/raw/135.md → writes `CLI.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge the reports at the repo root and in `reports/` into one sequenced plan.

## Rules
- If a fetch fails, retry once; if it still fails, use the locally installed /goal:<slug> (or /goal-<slug>) command or the goal-prompts MCP get_brief tool for that stage; if neither exists, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists (at the repo root or in `reports/`), ask whether to re-run or skip that stage.
- A conductor caps at 16 stages — for a longer campaign, split it into two conductors and run them back-to-back.
