---
id: "31"
title: Tool Design Review
family: Agent
question: does the agent deliver?
output: TOOLS.md
tagline: Your tools are an API whose consumer is a model — audit names, descriptions, error contracts, and guards on destructive actions.
---
# Goal: Tool Design Review

You are working inside this repo. Mission: review the tools exposed to your agents as what they are — an API whose consumer is a model — and find where the design invites wrong calls, dead ends, or damage.

Read-only pass. Your only write is the report file.

## Phase 1 — Inventory the toolbox
- List every tool/function an agent can call: name, description, parameters, what actually executes.
- Which loops or agents can call which tools; which tools touch the outside world.
- If traces exist: which tools get called most, and which calls fail most.

## Phase 2 — Audit through 8 lenses
1. **Misleading surface** — names and descriptions that make the model pick the wrong tool or wrong moment
2. **Parameter footguns** — ambiguous types, formats described nowhere, optionals that silently default to something surprising
3. **Error contract** — failures returning actionable text the model can adapt to, vs stack traces, nulls, or silence
4. **Granularity** — too atomic (routine jobs need 12-call chains) or too broad (one mega-tool misused)
5. **Destructive gaps** — delete/send/pay/write tools with no confirmation step, dry-run mode, or undo
6. **Overlap** — two tools doing the same job, chosen inconsistently
7. **Missing tools** — hacks in traces or prompts where the agent works around a tool that should exist
8. **Return bloat** — tool results dumping thousands of tokens into the window when a summary would serve

## Phase 3 — Curate
- Every finding names the failure it produces: wrong call, wasted loop, or real damage
- Prefer fixing descriptions and errors first — cheapest lever on agent behavior

## Phase 4 — Report
Create `TOOLS.md` at repo root:
1. **Tool table** — name · job · calls the outside world? · risk · issues found
2. **Description rewrites** — worst 3, before/after, ready to paste
3. **Error contract standard** — the one shape every tool failure should return
4. **Guard plan** — which tools get confirms, dry-runs, or scoped permissions
5. **Add/merge/kill list**

## Rules
- Judge tools from the model's seat: only what the description says exists
- An error a model can't act on is a dead end, not error handling
- Report only — end by asking which changes to make
