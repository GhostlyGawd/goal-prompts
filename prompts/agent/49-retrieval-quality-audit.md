---
id: "49"
title: Retrieval Quality Audit
family: Agent
question: does the agent deliver?
output: RETRIEVAL.md
related: 33
tagline: The RAG pipeline end to end — chunking that respects meaning, embeddings that don't drift, a relevance floor, and evals that catch regressions before users do.
---
# Goal: Retrieval Quality Audit

You are working inside this repo. Mission: audit the retrieval pipeline end to end — ingest, chunk, embed, store, query, inject — and find where it feeds the model the wrong context, or the right context mangled.

Read-only pass. Your only write is the report file.

## Phase 1 — Map the pipeline
- Trace one document from source to prompt: ingestion, chunking (size, overlap, boundaries), embedding (model, version), storage (index, metadata), the query path (rewriting, filters, top-k, reranking), and the final injection format.
- Record every knob and its current value: chunk size, k, similarity thresholds, model names, token budgets.

## Phase 2 — Audit through 8 lenses
1. **Chunking fit** — do boundaries respect the content's shape, or do they split tables, code blocks, and arguments mid-thought; inspect real chunks, not the config
2. **Embedding hygiene** — model version pinned; what happens to the existing index when the model changes; queries and documents embedded consistently
3. **Relevance floor** — a minimum-similarity threshold, or does top-k dutifully inject k results even when the best match is garbage
4. **Freshness & sync** — a source document updates or is deleted: how long until the index agrees; do deletes actually propagate
5. **Filters & scoping** — metadata filtering and tenancy applied before injection; whether a query can leak across collections or users
6. **Injection format** — how chunks land in the prompt: deduped, ordered, attributed, inside a token budget — or concatenated and prayed over
7. **Failure behavior** — empty results, store down, timeout: does the agent say so, hallucinate, or quietly answer from priors
8. **Eval coverage** — golden queries with known-correct chunks; recall measured; anything that fails CI when retrieval regresses

## Phase 3 — Curate
- Hand-trace 3 representative queries: what was retrieved, what should have been, and where the pipeline lost it.
- Rank findings by answer-quality impact, not architectural taste.

## Phase 4 — Report
Create `RETRIEVAL.md` at repo root:
1. **Pipeline map** — stage · implementation · knob values · owning file
2. **Three traces** — query → retrieved vs deserved → diagnosis
3. **Findings** — ranked, with evidence
4. **Eval starter** — ten golden queries worth committing this week

Start the report with today's date. If `RETRIEVAL.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Judge retrieval by what reaches the prompt, not by what the store contains
- Every claim about quality needs a traced example behind it
- No retrieval or RAG pipeline in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fixes to make
