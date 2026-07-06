---
id: "35"
title: Guardrails Audit
family: Agent
question: does the agent deliver?
output: GUARDRAILS.md
tagline: A defensive review of your agent's blast radius — injection paths, unvalidated outputs, over-broad permissions, ungated irreversible actions.
---
# Goal: Guardrails Audit

You are working inside this repo. Mission: a defensive review of your own agent system — map what untrusted content can reach the model, what the model can do to the world, and where the gap between those two is unguarded.

Read-only pass. Your only write is the report file.

## Phase 1 — Map the two surfaces
- **Inputs**: every path untrusted content enters model context — user messages, retrieved documents, web content, file uploads, tool results.
- **Powers**: every tool ranked by blast radius — read-only, writes-internal, touches-the-outside-world, irreversible.
- Whose credentials does the agent run with, and how scoped are they?

## Phase 2 — Audit through 7 lenses
Cite locations; keep risk descriptions to the one or two lines needed to justify each fix — this is a defensive report.
1. **Injection paths** — untrusted content placed adjacent to instructions; tool results and retrieved docs treated as trusted voice
2. **Output validation** — model output parsed, executed, rendered, or forwarded without deterministic checks (queries, shell strings, HTML, URLs, addresses)
3. **Permission scope** — agent credentials broader than the task needs; one key for read and destroy
4. **Irreversible gates** — delete, send, publish, pay: which run with no confirmation, dry-run, or review step (see 43)
5. **Exfiltration channels** — the combination of can-read-secrets and can-make-requests, unmediated
6. **Blast limits** — the maximum damage of one compromised or confused run: bounded by anything?
7. **Refusal visibility** — when the model balks or a guard fires, is it logged and reviewed, or invisible?

## Phase 3 — Curate
- Severity = reachability × blast radius; name the preconditions honestly
- Prefer systemic guards (validation layer, scoped creds, action gates) over per-spot patches

## Phase 4 — Report
Create `GUARDRAILS.md` at repo root:
1. **The two-surface map** — inputs table and powers table
2. **Findings** — each: severity · location · risk (1–2 lines) · fix · effort
3. **Systemic guards to adopt** — the three that eliminate classes
4. **Fix-this-week list**

## Rules
- Assume any content the agent reads may be adversarial; design for it
- A guard nobody can see firing is a guard nobody maintains
- Report only — end by asking which guards to build
