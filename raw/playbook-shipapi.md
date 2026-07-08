# Playbook: Ship a Public API (conductor)

You are working inside this repo. Mission: execute the **Ship a Public API** playbook — 6 audit briefs in sequence, each producing one report file at this repo's root.

Everything a developer meets when they build on you: webhooks, the SDK, versioning, rate limits, and the first-hour docs — then the Fixer ships the fixes as commits.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **111 · Webhook Design Audit** — fetch https://goal-prompts.vercel.app/raw/111.md → writes `WEBHOOKS.md`
2. **112 · SDK Ergonomics Audit** — fetch https://goal-prompts.vercel.app/raw/112.md → writes `SDK.md`
3. **113 · API Versioning & Deprecation** — fetch https://goal-prompts.vercel.app/raw/113.md → writes `VERSIONING.md`
4. **114 · Rate-Limit & Quota Design** — fetch https://goal-prompts.vercel.app/raw/114.md → writes `QUOTAS.md`
5. **115 · Developer Portal & Onboarding** — fetch https://goal-prompts.vercel.app/raw/115.md → writes `DEVPORTAL.md`
6. **47 · The Fixer** — fetch https://goal-prompts.vercel.app/raw/47.md → writes `FIXLOG.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
