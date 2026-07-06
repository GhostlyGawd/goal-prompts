---
id: "48"
title: Memory & State Audit
family: Agent
question: does the agent deliver?
output: MEMORY.md
tagline: What the agent carries between runs — persistence scope, staleness, contradictory facts, and memory injected as truth without provenance.
---
# Goal: Memory & State Audit

You are working inside this repo. Mission: audit everything the agent remembers across turns and runs — where it lives, how it's written and read, and where stale or wrong memory silently poisons behavior.

Read-only pass. Your only write is the report file.

## Phase 1 — Map what persists
- Find every store that survives a single model call: conversation history, summaries, user profiles, extracted facts, vector memory, scratchpads, caches.
- For each: what writes it, what reads it, its lifetime, and whether anything ever invalidates or expires it.
- Trace one real path: a fact learned in run A — how does it reach run B, and in what form?

## Phase 2 — Audit through 7 lenses
Cite the store and the code for every finding.
1. **Write discipline** — what gets remembered, and why that and not everything: is capture deliberate or accidental accumulation?
2. **Staleness** — facts true when written, wrong now (a changed preference, a closed account); is there any recency or re-validation?
3. **Contradiction** — two memories that disagree; which wins, and does anything detect the conflict?
4. **Provenance** — memory injected into context as fact with no source, confidence, or timestamp; the model can't weigh what it can't see the origin of
5. **Unbounded growth** — memory that only accumulates; what happens to relevance and token cost at run 1,000
6. **Read relevance** — is the right memory retrieved for the moment, or is everything dumped in regardless (overlaps 33)
7. **Correctness of extraction** — where an LLM writes memory, does it hallucinate facts that then harden into permanent truth

## Phase 3 — Curate
- Rank by blast radius × persistence: a wrong fact re-injected every run outranks a one-off
- Every finding names the failure it produces: wrong answer, contradiction, drift, or cost

## Phase 4 — Report
Create `MEMORY.md` at repo root:
1. **Memory map** — store · written by · read by · lifetime · invalidation
2. **Findings** — each: issue · lens · evidence · fix · risk
3. **Provenance plan** — how memory should carry source, confidence, and recency into context
4. **Lifecycle policy** — expiry, conflict resolution, and growth limits per store
5. **The first fix** — highest-poison memory, before/after

## Rules
- Memory injected as fact is a claim the model can't question — treat provenance as mandatory
- A memory system with no forgetting is a bug with a long fuse
- Report only — end by asking which fixes to make
