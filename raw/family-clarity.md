# Playbook: All Clarity briefs (conductor)

You are working inside this repo. Mission: execute the **All Clarity briefs** playbook — 6 audit briefs in sequence, each producing one report file at this repo's root.

Every Clarity brief in the catalog, in order — 16 through 135, one report each.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **16 · Documentation Audit** — fetch https://goal-prompts.vercel.app/raw/16.md → writes `DOCS.md`
2. **17 · Copy & Voice Audit** — fetch https://goal-prompts.vercel.app/raw/17.md → writes `COPY.md`
3. **18 · API Contract Review** — fetch https://goal-prompts.vercel.app/raw/18.md → writes `API.md`
4. **76 · Comprehension Audit** — fetch https://goal-prompts.vercel.app/raw/76.md → writes `COMPREHENSION.md`
5. **103 · Error-Message Audit** — fetch https://goal-prompts.vercel.app/raw/103.md → writes `ERRORS.md`
6. **135 · CLI Tool UX Audit** — fetch https://goal-prompts.vercel.app/raw/135.md → writes `CLI.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
