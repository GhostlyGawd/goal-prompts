---
description: "Every cache from CDN headers to that module-level dict — keys, TTLs, who invalidates what — the stale read, the stampede, and the key that leaks between users."
---

# Goal: Caching Strategy Audit

You are working inside this repo. Mission: find every cache this system runs — declared or accidental — and audit the three questions each must answer: what is the key, when does it die, and who kills it early. A cache with no answer to the third question is a staleness bug on a timer.

Read-only pass. Your only write is the report file.

## Phase 1 — Census the caches
- Inventory every layer: CDN and HTTP cache headers, reverse proxies, Redis/memcached, ORM and query caches, memoization decorators, and the module-level dicts and lazy globals that are caches without admitting it.
- For each: the key composition, the TTL (or its absence), the eviction policy, and every code path that invalidates it — file:line.
- Mark what each cache fronts: whose data, how hot, how expensive to recompute.

## Phase 2 — Audit through 7 lenses
Every finding cites the cache, its key, and the code path.
1. **Key hygiene** — user-, tenant-, or locale-scoped data under a key missing that scope: the cache that serves one user's data to another; audit every key's composition against what it stores
2. **Invalidation reality** — for each write path that changes cached data: trace to the invalidation call, or record "expiry only" and compute the staleness window users actually see
3. **TTL rationale** — every TTL justified by how stale is acceptable, or a folklore constant copied between configs; no TTL at all means forever
4. **Stampede paths** — a hot key expires under load: single-flight lock, jitter, stale-while-revalidate, or a thundering herd onto the database
5. **Layer coherence** — the same data cached at CDN, app, and query layers with different lifetimes: compute the worst-case disagreement a user can observe
6. **Negative & error caching** — errors and empty results: cached so failures hammer nothing, or uncached so every miss retries; a cached 500 with a long TTL is an outage extender
7. **Unbounded growth** — the memo dicts and key-per-user caches with no eviction: today's optimization, next quarter's memory leak

## Phase 3 — Curate
- Rank correctness above speed: a cross-user leak or unkillable stale read outranks any hit-rate win.
- For each, name the mechanism: a scoped key, an invalidation hook, single-flight, stale-while-revalidate, an LRU bound.
- Note what isn't cached but should be — repeated identical reads on the hot path are the flip side of the same audit.

## Phase 4 — Report
Create `CACHES.md` at repo root:
1. **Cache ledger** — cache · key composition · TTL · invalidation path (file:line) or "expiry only" · stampede guard · bound
2. **The staleness story** — the worst user-visible stale read possible today, narrated: the write, the windows, what the user sees
3. **Findings** — each: lens · cache · risk · the mechanism to fix it · effort
4. **Missing caches** — the hot, repeated, identical reads with no cache in front of them

Start the report with today's date. If `CACHES.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every cache answers three questions — key, death, early death; "expiry only" is an answer and a finding
- A cache is a correctness feature that happens to be fast; audit it like one
- No caching layers — declared or accidental — in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which caches to fix first
