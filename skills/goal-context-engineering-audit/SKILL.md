---
name: goal-context-engineering-audit
description: "Reconstruct what actually enters the model's window each step — stale payloads, token hogs, retrieval junk, and buried instructions. Audit brief 33 · Agent — runs a four-phase audit of the current repo and writes CONTEXT.md at the repo root."
---

# Goal: Context Engineering Audit

You are working inside this repo. Mission: reconstruct what actually enters the model's context window on a typical step — every section, every token — and find what's stale, bloated, missing, or buried.

Read-only pass. Your only write is the report file.

## Phase 1 — Reconstruct the window
- For the main agent loop, assemble a real example of one step's full input: system prompt, history, retrieved content, tool results, user message.
- Measure or estimate tokens per section. Draw the pie.
- Trace where each section comes from and what decides its size.

## Phase 2 — Audit through 8 lenses
1. **Stale payloads** — old tool results and resolved errors re-sent on every subsequent step, forever
2. **Token hogs** — one section dominating the window; full-file dumps where excerpts would serve
3. **Retrieval quality** — top-k taken on faith: no relevance floor, duplicates, chunks cut mid-thought
4. **History policy** — unbounded transcript vs summarization vs truncation; what information each choice silently loses
5. **Memory hygiene** — persisted facts that are wrong, expired, or contradictory, injected as truth
6. **Ordering** — critical instructions buried mid-window where attention is weakest; latest-and-loudest drowning the objective
7. **Duplication** — the same content arriving via two paths (in the prompt AND retrieved)
8. **Format waste** — verbose JSON, base64 blobs, or logs where a compact rendering carries the same signal

## Phase 3 — Curate
- Price each waste finding: tokens × calls per run × runs per day
- Flag anything whose removal risks capability — cutting context is a behavior change

## Phase 4 — Report
Create `CONTEXT.md` at repo root:
1. **Window anatomy** — section · tokens · source · verdict (keep/shrink/cut/move)
2. **Waste ranked** — with the arithmetic
3. **Retrieval fixes** — floors, dedupe, chunking changes
4. **Target budget** — the proposed window layout, section by section
5. **Eval note** — how to verify quality holds after each cut (see 34)

Start the report with today's date. If `CONTEXT.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every token in the window should earn its place on the current step
- Never ship a context cut without an eval or rollback plan
- No LLM context assembly in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which changes to make
