---
name: goal-in-app-search
description: "The product's own search — whether users can find what they are looking for: relevance, recall, forgiveness, and what happens on zero results. Goal Prompt 107 · Product — inspects the current repo and writes SEARCH.md at the repo root."
---

# Goal: In-App Search Audit

You are working inside this repo. Mission: judge the product's built-in search as a user experiences it — can they find what they came for, is the best result first, and does the product help when nothing matches. This is the in-product find feature, not SEO.

Read-only pass. Run real queries against the product, read the search and indexing code; change nothing but the report file.

## Phase 1 — Search like a user
- Run a set of realistic queries: exact, partial, misspelled, multi-word, and ones that should return nothing.
- Note what comes back, in what order, and how fast.
- Find what is indexed and what is silently unsearchable.

## Phase 2 — Audit through 7 lenses
Cite the query and result for every finding.
1. **Relevance** — do the best matches rank first, or is ordering arbitrary
2. **Recall & coverage** — is everything findable that should be; fields or content missing from the index
3. **Forgiveness** — typos, synonyms, partial matches, case and accent folding
4. **Zero-result states** — a helpful path forward versus a blank dead end
5. **Speed & feedback** — responsiveness, as-you-type feedback, a loading state
6. **Filters & scoping** — useful facets to refine a broad query
7. **Query understanding** — multi-word queries, phrases, and intent, not just substring match

## Phase 3 — Curate
- Rank by how often the query type is used and how badly it fails.
- For each, name the fix — index a field, add synonyms, fix ranking, design the empty state.
- Separate "wrong results" from "no results handling"; both lose the user.

## Phase 4 — Report
Create `SEARCH.md` at repo root:
1. **Query runs** — the test queries, what they returned, and the verdict on each
2. **Findings** — each: lens · query · what failed · the fix
3. **Recall gaps** — the content that should be findable and is not
4. **Zero-result design** — what the product should offer when nothing matches

Start the report with today's date. If `SEARCH.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Judge by real queries and their results, not by the search box's looks
- A confident wrong result is worse than an honest empty state
- No in-app search in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which search fixes to make first
