---
id: "50"
title: Multi-Agent Topology Review
family: Agent
question: does the agent deliver?
output: TOPOLOGY.md
tagline: For systems with more than one agent — role overlap, orchestration fit, communication overhead, and whether the split earns its complexity.
---
# Goal: Multi-Agent Topology Review

You are working inside this repo. Mission: review how multiple agents (or roles, sub-agents, specialized prompts) are decomposed and wired — and judge whether the multi-agent structure earns its coordination cost or should collapse.

Read-only pass. Your only write is the report file. If the system is single-agent, say so and stop early.

## Phase 1 — Map the topology
- Identify every distinct agent/role: its job, its prompt, its tools, its model.
- Draw the wiring: who calls whom, who orchestrates, how work and results flow (supervisor, pipeline, peer-to-peer, blackboard?).
- Trace one real task through the whole topology, counting the hops and handoffs.

## Phase 2 — Audit through 7 lenses
1. **Role clarity** — crisp non-overlapping responsibilities, or agents with fuzzy duplicated jobs doing each other's work
2. **Decomposition fit** — the split matching the problem's real seams, or an org-chart imposed on a task that one capable agent would handle better
3. **Orchestration pattern** — the control structure suiting the workflow; a rigid pipeline forcing back-and-forth, or free-for-all where a supervisor is needed
4. **Communication overhead** — tokens and latency spent passing context between agents; re-establishing shared state each hop (ties to 41)
5. **Error propagation** — one agent's bad output flowing downstream unchecked; no validation at the seams; failure blame hard to locate
6. **Context fragmentation** — each agent seeing only its slice, so decisions get made without the whole picture; the left hand not knowing the right
7. **Collapse test** — for each agent, ask honestly: would merging it into a neighbor reduce coordination cost with no capability loss?

## Phase 3 — Curate
- Every finding weighs capability gained against coordination cost paid
- Name what the topology gets right — genuine specialization worth keeping — so it isn't flattened blindly

## Phase 4 — Report
Create `TOPOLOGY.md` at repo root:
1. **Topology map** — agents, their jobs, and the wiring diagram in words; the traced task with its hop count
2. **Findings** — each: issue · lens · evidence · fix
3. **Merge/split recommendations** — which agents to combine, which responsibilities to re-cut, and why
4. **Seam validation plan** — where to add checks between agents (ties to 34)
5. **The simplest topology that works** — the proposed structure, and the one change toward it

## Rules
- Multi-agent is a cost, justified only by capability a single agent can't reach; make each agent defend its existence
- More agents is not more capable — coordination is where agent systems rot
- Report only — end by asking which changes to make
