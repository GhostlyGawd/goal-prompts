# Playbook: Test Confidence (conductor)

You are working inside this repo. Mission: execute the **Test Confidence** playbook — 4 audit briefs in sequence, each producing one report file at this repo's root.

Earn a green suite you can trust: find the coverage gaps, strengthen the tests that assert nothing, kill the flakes, and rebalance a top-heavy pyramid.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **02 · Test Gap Audit** — fetch https://goal-prompts.vercel.app/raw/02.md → writes `TESTING.md`
2. **100 · Test-Quality Audit** — fetch https://goal-prompts.vercel.app/raw/100.md → writes `TESTQUALITY.md`
3. **101 · Flaky-Test Audit** — fetch https://goal-prompts.vercel.app/raw/101.md → writes `FLAKY.md`
4. **102 · Test-Pyramid Balance** — fetch https://goal-prompts.vercel.app/raw/102.md → writes `PYRAMID.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
