# Playbook: eCommerce Optimization (conductor)

You are working inside this repo. Mission: execute the **eCommerce Optimization** playbook — 6 audit briefs in sequence, each producing one report file at this repo's root.

Optimize the whole funnel for a first-time visitor: audit every conversion surface, then cut friction, sharpen the visual hierarchy, tighten the copy, and make it findable — and the Fixer ships the highest-leverage lifts as commits.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **75 · Conversion Rate Optimization** — fetch https://goal-prompts.vercel.app/raw/75.md → writes `CRO.md`
2. **09 · Funnel Friction Audit** — fetch https://goal-prompts.vercel.app/raw/09.md → writes `FUNNEL.md`
3. **54 · Visual Hierarchy Audit** — fetch https://goal-prompts.vercel.app/raw/54.md → writes `HIERARCHY.md`
4. **17 · Copy & Voice Audit** — fetch https://goal-prompts.vercel.app/raw/17.md → writes `COPY.md`
5. **70 · SEO & Discoverability** — fetch https://goal-prompts.vercel.app/raw/70.md → writes `SEO.md`
6. **47 · The Fixer** — fetch https://goal-prompts.vercel.app/raw/47.md → writes `FIXLOG.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
