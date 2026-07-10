---
name: goal-multi-agent-topology
description: "Is the org chart of agents earning its overhead — role clarity, orchestration fit, the communication tax, and what one agent with better tools would do instead. Audit brief 50 · Agent — runs a four-phase audit of the current repo and writes TOPOLOGY.md at the repo root."
---

# Goal: Multi-Agent Topology Review

You are working inside this repo. Mission: map how the agents are organized — who does what, who talks to whom, who decides — and judge whether the topology earns its coordination overhead.

Read-only pass. Your only write is the report file.

## Phase 1 — Map the organization
- List every agent: role, model, system prompt, tools it holds, who spawns it, what it returns.
- Draw the message paths: orchestrator to worker, peer to peer, shared memory, queues. Note what each hop serializes and re-explains.
- Name the topology honestly: pipeline, supervisor/workers, router, swarm — or accidental.

## Phase 2 — Audit through 8 lenses
1. **Role clarity** — can each agent's job be stated in one line that no sibling's line overlaps; overlap is where duplicated work and contradictions breed
2. **Topology fit** — the single-agent counterfactual: would one agent with these tools and a better prompt do the same job; what does the split actually buy
3. **Communication tax** — tokens spent describing work to other agents versus doing the work; count it on a real run
4. **Handoff loss** — what context survives each hop; the summary that dropped the one constraint that mattered
5. **Failure propagation** — one agent errs or stalls: who notices, what retries, and whether partial results poison downstream agents
6. **Authority** — two agents disagree: who rules, or does the loudest last message win; any deadlock or ping-pong paths
7. **Observability** — one request traceable across all agents with correlated ids, or N disconnected logs
8. **Cost multiplication** — the same documents and instructions billed through every agent's context window; measure the duplication

## Phase 3 — Curate
- Price a representative run: total tokens, the share spent on coordination, wall-clock lost to hops.
- Write the counterfactual honestly: what a simpler topology would cost, and what it would lose.

## Phase 4 — Report
Create `TOPOLOGY.md` at repo root:
1. **Org chart** — agent · role · model · tools · spawned by
2. **The coordination tax** — the arithmetic from a real run
3. **Findings** — ranked by cost × confusion
4. **Restructure options** — merge, split, or re-wire; each with what it saves and what it risks

Start the report with today's date. If `TOPOLOGY.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- More agents is a cost, not an achievement — the burden of proof is on the split
- Judge from real traces where they exist, code paths where they don't
- No multi-agent system in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which changes to make
