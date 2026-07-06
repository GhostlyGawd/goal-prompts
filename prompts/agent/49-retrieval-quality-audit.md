---
id: "49"
title: Retrieval Quality Audit
family: Agent
question: does the agent deliver?
output: RETRIEVAL.md
tagline: The RAG pipeline end to end — chunking, embedding fit, relevance floors, and whether retrieval quality is measured or merely hoped.
---
# Goal: Retrieval Quality Audit

You are working inside this repo. Mission: audit the retrieval pipeline that feeds the model — ingestion, chunking, embedding, search, ranking — and find where irrelevant, missing, or malformed context is quietly degrading answers.

Read-only pass. Your only write is the report file.

## Phase 1 — Trace the pipeline
- Map it end to end: source documents → chunking → embedding → index → query → ranking → what lands in context.
- Record the choices: chunk size and overlap, embedding model, index type, top-k, any re-ranking or filtering.
- Trace one real query: what got retrieved, and was it actually what the question needed?

## Phase 2 — Audit through 7 lenses
1. **Chunking** — chunks cut mid-thought, too large (diluted) or too small (contextless); is structure (headings, code blocks) respected or shredded?
2. **Embedding fit** — model suited to the domain and query style; asymmetric query-vs-document handling; staleness if content changed but embeddings didn't
3. **Relevance floor** — top-k taken blindly with no score threshold, so weak matches pad the window on narrow queries
4. **Recall gaps** — content that should be findable but isn't: metadata not indexed, synonyms missed, one embedding space for genuinely different content types
5. **Ranking** — nearest-neighbor order trusted as relevance order; no re-ranking where it would clearly help
6. **Duplication & noise** — near-duplicate chunks crowding out diversity; boilerplate retrieved repeatedly
7. **Measurement** — is retrieval quality evaluated at all (recall@k, human spot-checks), or inferred from downstream vibes (ties to 34)

## Phase 3 — Curate
- Separate retrieval failures from generation failures: bad answer from bad context is a retrieval bug, and this report only owns the former
- Rank by how often the flaw corrupts a real query × how badly

## Phase 4 — Report
Create `RETRIEVAL.md` at repo root:
1. **Pipeline snapshot** — the stages and every parameter chosen
2. **Findings** — each: stage · issue · evidence (the traced query helps) · fix · effort
3. **Chunking & floor fixes** — the two cheapest high-impact levers, concretely
4. **Retrieval eval plan** — a small labeled query set and the metric to track (see 34)
5. **The first change** — biggest answer-quality gain per unit effort

## Rules
- Diagnose retrieval by what actually entered the window, not by pipeline intent
- No retrieval change ships without a way to measure whether recall improved
- Report only — end by asking which fixes to make
