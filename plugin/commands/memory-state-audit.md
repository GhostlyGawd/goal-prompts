---
description: "What the agent remembers between runs — where memories get written, when they go stale, how a wrong fact gets in, and whether anything can ever be forgotten."
---

# Goal: Memory & State Audit

You are working inside this repo. Mission: map everything this agent persists between runs — memories, profiles, caches, scratchpads, histories — and audit how it goes stale, how it goes wrong, and whether it can be corrected.

Read-only pass. Your only write is the report file.

## Phase 1 — Map what persists
- Inventory every persistence surface: vector stores, key-value stores, database tables, files, conversation histories, user profiles, learned preferences, caches with long TTLs.
- For each: what writes it, what reads it, when (if ever) it expires, and where it lands in a prompt.
- Separate state the system needs (queues, checkpoints, cursors) from knowledge the model consumes (facts, preferences, summaries) — the second kind is where wrong answers come from.

## Phase 2 — Audit through 8 lenses
1. **Write-time validation** — what stops a hallucinated or misparsed fact from being stored as memory; is anything checked, or does the model grade its own homework
2. **Staleness** — facts with no expiry or refresh path; how old is the oldest memory still being injected, and what has changed since it was true
3. **Injection blast radius** — trace one memory to every prompt it reaches; a wrong fact stored once, repeated forever
4. **Correction paths** — can a user or operator view, amend, or delete a memory; does deletion actually stop retrieval or just hide a row
5. **Cross-contamination** — tenancy and session scoping; whether user A's memory can surface in user B's context
6. **Unbounded growth** — accumulation without dedupe or compaction; what the store looks like after ten times the runs
7. **Provenance** — can any stored fact be traced back to the run and source that wrote it
8. **Death and recovery** — a run dies mid-write: what partial state remains, and who cleans it up

## Phase 3 — Curate
- Rank findings by (likelihood a bad fact gets in) × (how many future runs it poisons).
- For each top finding, write the one-sentence horror story — the concrete user-visible consequence.

## Phase 4 — Report
Create `MEMORY.md` at repo root:
1. **Persistence inventory** — surface · writer · reader · expiry · where it enters prompts
2. **Lifecycle matrix** — write / read / stale / correct / delete → behavior today → gap
3. **Top risks** — ranked, each with its horror story and evidence
4. **Fixes** — write-time validation and correction paths usually first

Start the report with today's date. If `MEMORY.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- A memory nothing can delete is a liability, not a feature
- Trace real code paths — the framework probably handling it is not evidence
- No agent memory or session state in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fixes to make
