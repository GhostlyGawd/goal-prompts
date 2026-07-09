# Playbook: All Speed briefs (conductor)

You are working inside this repo. Mission: execute the **All Speed briefs** playbook — 6 audit briefs in sequence, each producing one report file at the repo root (or in `reports/`, if the repo has that directory).

Every Speed brief in the catalog, in order — 04 through 140, one report each.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. If your harness can run subagents or fresh sessions, run each stage in one — a stage needs only the earlier report files at the repo root and in `reports/`, never this conversation.
3. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
4. Confirm the report file exists (at the repo root or in `reports/`) before moving on.
5. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **04 · Performance Audit** — fetch https://goal-prompts.vercel.app/raw/04.md → writes `PERF.md`
2. **05 · 10x Stress Review** — fetch https://goal-prompts.vercel.app/raw/05.md → writes `SCALE.md`
3. **51 · Latency Budget Audit** — fetch https://goal-prompts.vercel.app/raw/51.md → writes `LATENCY.md`
4. **87 · Query Performance & N+1 Audit** — fetch https://goal-prompts.vercel.app/raw/87.md → writes `QUERIES.md`
5. **88 · Bundle & Asset Weight Audit** — fetch https://goal-prompts.vercel.app/raw/88.md → writes `BUNDLE.md`
6. **140 · Caching Strategy Audit** — fetch https://goal-prompts.vercel.app/raw/140.md → writes `CACHES.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge the reports at the repo root and in `reports/` into one sequenced plan.

## Rules
- If a fetch fails, retry once; if it still fails, use the locally installed /goal:<slug> (or /goal-<slug>) command or the goal-prompts MCP get_brief tool for that stage; if neither exists, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists (at the repo root or in `reports/`), ask whether to re-run or skip that stage.
- A conductor caps at 16 stages — for a longer campaign, split it into two conductors and run them back-to-back.
