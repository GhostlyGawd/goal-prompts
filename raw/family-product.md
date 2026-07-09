# Playbook: All Product briefs (conductor)

You are working inside this repo. Mission: execute the **All Product briefs** playbook — 5 audit briefs in sequence, each producing one report file at the repo root (or in `reports/`, if the repo has that directory).

Every Product brief in the catalog, in order — 00 through 108, one report each.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. If your harness can run subagents or fresh sessions, run each stage in one — a stage needs only the earlier report files at the repo root and in `reports/`, never this conversation.
3. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
4. Confirm the report file exists (at the repo root or in `reports/`) before moving on.
5. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **00 · Product Improvement Discovery** — fetch https://goal-prompts.vercel.app/raw/00.md → writes `IMPROVEMENTS.md`
2. **45 · Feedback Loop Audit** — fetch https://goal-prompts.vercel.app/raw/45.md → writes `FEEDBACK.md`
3. **106 · Notification & Email Audit** — fetch https://goal-prompts.vercel.app/raw/106.md → writes `NOTIFICATIONS.md`
4. **107 · In-App Search Audit** — fetch https://goal-prompts.vercel.app/raw/107.md → writes `SEARCH.md`
5. **108 · Account Lifecycle Audit** — fetch https://goal-prompts.vercel.app/raw/108.md → writes `LIFECYCLE.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge the reports at the repo root and in `reports/` into one sequenced plan.

## Rules
- If a fetch fails, retry once; if it still fails, use the locally installed /goal:<slug> (or /goal-<slug>) command or the goal-prompts MCP get_brief tool for that stage; if neither exists, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists (at the repo root or in `reports/`), ask whether to re-run or skip that stage.
- A conductor caps at 16 stages — for a longer campaign, split it into two conductors and run them back-to-back.
