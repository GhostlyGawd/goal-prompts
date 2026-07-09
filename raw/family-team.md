# Playbook: All Team briefs (conductor)

You are working inside this repo. Mission: execute the **All Team briefs** playbook — 9 audit briefs in sequence, each producing one report file at the repo root (or in `reports/`, if the repo has that directory).

Every Team brief in the catalog, in order — 13 through 97, one report each.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. If your harness can run subagents or fresh sessions, run each stage in one — a stage needs only the earlier report files at the repo root and in `reports/`, never this conversation.
3. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
4. Confirm the report file exists (at the repo root or in `reports/`) before moving on.
5. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **13 · Tech Debt Map** — fetch https://goal-prompts.vercel.app/raw/13.md → writes `DEBT.md`
2. **14 · New-Dev Onboarding Audit** — fetch https://goal-prompts.vercel.app/raw/14.md → writes `DX.md`
3. **15 · Design System Consolidation** — fetch https://goal-prompts.vercel.app/raw/15.md → writes `DESIGN-SYSTEM.md`
4. **52 · Agent Readiness Audit** — fetch https://goal-prompts.vercel.app/raw/52.md → writes `AGENT-READINESS.md`
5. **72 · Ownership & Bus Factor** — fetch https://goal-prompts.vercel.app/raw/72.md → writes `OWNERSHIP.md`
6. **94 · Inner-Loop Speed Audit** — fetch https://goal-prompts.vercel.app/raw/94.md → writes `INNERLOOP.md`
7. **95 · Debuggability Audit** — fetch https://goal-prompts.vercel.app/raw/95.md → writes `DEBUG.md`
8. **96 · CI Feedback-Loop Audit** — fetch https://goal-prompts.vercel.app/raw/96.md → writes `CIFEEDBACK.md`
9. **97 · Decision-Record Audit** — fetch https://goal-prompts.vercel.app/raw/97.md → writes `DECISIONS.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge the reports at the repo root and in `reports/` into one sequenced plan.

## Rules
- If a fetch fails, retry once; if it still fails, use the locally installed /goal:<slug> (or /goal-<slug>) command or the goal-prompts MCP get_brief tool for that stage; if neither exists, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists (at the repo root or in `reports/`), ask whether to re-run or skip that stage.
- A conductor caps at 16 stages — for a longer campaign, split it into two conductors and run them back-to-back.
