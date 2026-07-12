# Playbook: All AI-Ethics briefs (conductor)

You are working inside this repo. Mission: execute the **All AI-Ethics briefs** playbook — 5 audit briefs in sequence, each producing one report file at the repo root (or in `reports/`, if the repo has that directory).

Every AI-Ethics brief in the catalog, in order — 116 through 120, one report each.

## Before stage 1
- If `CHARTER.md` exists at the repo root or in `reports/`, read it first — its goals, non-goals, and invariants bound every recommendation in every stage. No charter? Proceed, and suggest 149 · The Charter afterwards.
- Before fetching stage 1, tell the operator in plain words what this playbook will do — one line per stage — and ask for the go-ahead.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. If your harness can run subagents or fresh sessions, run each stage in one — a stage needs only the earlier report files at the repo root and in `reports/`, never this conversation.
3. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
4. Confirm the report file exists (at the repo root or in `reports/`) before moving on.
5. After each stage, tell the operator in two or three plain sentences what it found — the single biggest finding and why it matters for this repo — and what comes next; never advance in silence.
6. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **116 · Bias & Fairness Audit** — fetch https://goal-prompts.vercel.app/raw/116.md → writes `FAIRNESS.md`
2. **117 · Hallucination & Grounding Audit** — fetch https://goal-prompts.vercel.app/raw/117.md → writes `GROUNDING.md`
3. **118 · Prompt-Injection Red-Team** — fetch https://goal-prompts.vercel.app/raw/118.md → writes `REDTEAM.md`
4. **119 · Model Transparency Audit** — fetch https://goal-prompts.vercel.app/raw/119.md → writes `TRANSPARENCY.md`
5. **120 · Training-Data Provenance** — fetch https://goal-prompts.vercel.app/raw/120.md → writes `PROVENANCE.md`

## After the final stage
- Present the strongest findings across every report as one ranked list, in plain words — each with why it matters for this repo; the operator should not need to open a report file to act.
- Then ask which findings to fix. Unless 47 · The Fixer already ran as a stage of this playbook, offer to fetch https://goal-prompts.vercel.app/raw/47.md and implement exactly the operator's picks — one verified commit per finding. The report files stay on disk as the paper trail.
- Prefer a merged plan instead? Fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to fold the reports at the repo root and in `reports/` into one sequenced plan.

## Rules
- If a fetch fails, retry once; if it still fails, use the locally installed /goal:<slug> (or /goal-<slug>) command or the goal-prompts MCP get_brief tool for that stage; if neither exists, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists (at the repo root or in `reports/`), ask whether to re-run or skip that stage.
- A conductor caps at 16 stages — for a longer campaign, split it into two conductors and run them back-to-back.
