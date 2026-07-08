# Playbook: Make It Fast (conductor)

You are working inside this repo. Mission: execute the **Make It Fast** playbook — 5 audit briefs in sequence, each producing one report file at this repo's root.

A speed-only sweep: profile the hot paths, hold a latency budget, fix the queries that will not scale, cut the bundle the browser downloads, and mine the churny hotspots.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **04 · Performance Audit** — fetch https://goal-prompts.vercel.app/raw/04.md → writes `PERF.md`
2. **51 · Latency Budget Audit** — fetch https://goal-prompts.vercel.app/raw/51.md → writes `LATENCY.md`
3. **87 · Query Performance & N+1 Audit** — fetch https://goal-prompts.vercel.app/raw/87.md → writes `QUERIES.md`
4. **88 · Bundle & Asset Weight Audit** — fetch https://goal-prompts.vercel.app/raw/88.md → writes `BUNDLE.md`
5. **22 · Git Hotspot Mining** — fetch https://goal-prompts.vercel.app/raw/22.md → writes `HOTSPOTS.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
