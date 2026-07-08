# Playbook: Ship-It Week (conductor)

You are working inside this repo. Mission: execute the **Ship-It Week** playbook — 5 audit briefs in sequence, each producing one report file at this repo's root.

A limited, themed sprint for launch season — hunt the bugs, lock the doors, make it fast, rehearse the bad day, and get found. One themed bundle, five reports, ready to ship.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **01 · Bug Hunt** — fetch https://goal-prompts.vercel.app/raw/01.md → writes `BUGS.md`
2. **06 · Security & Privacy Audit** — fetch https://goal-prompts.vercel.app/raw/06.md → writes `SECURITY.md`
3. **04 · Performance Audit** — fetch https://goal-prompts.vercel.app/raw/04.md → writes `PERF.md`
4. **25 · Incident Readiness Review** — fetch https://goal-prompts.vercel.app/raw/25.md → writes `RELIABILITY.md`
5. **70 · SEO & Discoverability** — fetch https://goal-prompts.vercel.app/raw/70.md → writes `SEO.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
