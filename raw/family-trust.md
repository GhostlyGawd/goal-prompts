# Playbook: All Trust briefs (conductor)

You are working inside this repo. Mission: execute the **All Trust briefs** playbook — 11 audit briefs in sequence, each producing one report file at this repo's root.

Every Trust brief in the catalog, in order — 06 through 86, one report each.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **06 · Security & Privacy Audit** — fetch https://goal-prompts.vercel.app/raw/06.md → writes `SECURITY.md`
2. **07 · Dependency Health Check** — fetch https://goal-prompts.vercel.app/raw/07.md → writes `DEPS.md`
3. **08 · Accessibility Audit** — fetch https://goal-prompts.vercel.app/raw/08.md → writes `A11Y.md`
4. **68 · Localization Readiness** — fetch https://goal-prompts.vercel.app/raw/68.md → writes `I18N.md`
5. **69 · License & Compliance** — fetch https://goal-prompts.vercel.app/raw/69.md → writes `LICENSES.md`
6. **81 · Secrets & Credential Hygiene** — fetch https://goal-prompts.vercel.app/raw/81.md → writes `SECRETS.md`
7. **82 · Access-Control & Authorization Audit** — fetch https://goal-prompts.vercel.app/raw/82.md → writes `ACCESS.md`
8. **83 · Input & Injection Audit** — fetch https://goal-prompts.vercel.app/raw/83.md → writes `INJECTION.md`
9. **84 · Threat Model & Abuse Cases** — fetch https://goal-prompts.vercel.app/raw/84.md → writes `THREATS.md`
10. **85 · Dependency Currency Audit** — fetch https://goal-prompts.vercel.app/raw/85.md → writes `UPGRADES.md`
11. **86 · Keyboard & Screen-Reader Flow** — fetch https://goal-prompts.vercel.app/raw/86.md → writes `A11Y-DEEP.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
