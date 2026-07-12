# Playbook: Privacy & Compliance (conductor)

You are working inside this repo. Mission: execute the **Privacy & Compliance** playbook — 4 audit briefs in sequence, each producing one report file at the repo root (or in `reports/`, if the repo has that directory).

The operational-privacy layer regulators actually check: honest consent, real data-subject rights, encryption and key management, and a trustworthy audit trail.

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
1. **125 · Consent & Cookie Audit** — fetch https://goal-prompts.vercel.app/raw/125.md → writes `CONSENT.md`
2. **126 · Data-Subject-Rights Readiness** — fetch https://goal-prompts.vercel.app/raw/126.md → writes `DSAR.md`
3. **127 · Encryption & Key Management** — fetch https://goal-prompts.vercel.app/raw/127.md → writes `ENCRYPTION.md`
4. **128 · Audit-Trail Audit** — fetch https://goal-prompts.vercel.app/raw/128.md → writes `AUDITLOG.md`

## After the final stage
- Present the strongest findings across every report as one ranked list, in plain words — each with why it matters for this repo; the operator should not need to open a report file to act.
- Then ask which findings to fix. Unless 47 · The Fixer already ran as a stage of this playbook, offer to fetch https://goal-prompts.vercel.app/raw/47.md and implement exactly the operator's picks — one verified commit per finding. The report files stay on disk as the paper trail.
- Prefer a merged plan instead? Fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to fold the reports at the repo root and in `reports/` into one sequenced plan.

## Rules
- If a fetch fails, retry once; if it still fails, use the locally installed /goal:<slug> (or /goal-<slug>) command or the goal-prompts MCP get_brief tool for that stage; if neither exists, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists (at the repo root or in `reports/`), ask whether to re-run or skip that stage.
- A conductor caps at 16 stages — for a longer campaign, split it into two conductors and run them back-to-back.
