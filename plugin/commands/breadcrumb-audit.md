---
description: "Walk the doc-and-tooling link graph from the agent entry file — orphaned docs, unreachable scripts, files outside every stated taxonomy, and unwritten rules."
---

# Goal: Breadcrumb Audit

You are working inside this repo. Mission: map what a reader can actually reach by following links from the repo's entry files — CLAUDE.md / AGENTS.md, README, CONTRIBUTING — and surface everything that exists but is findable only by luck. 52 asks whether an agent can work here; this audit asks whether the repo's own surfaces can be found at all.

Read-only pass. Your only write is the report file.

## Phase 1 — Map the entry points
- Inventory the entry files: CLAUDE.md / AGENTS.md / .cursorrules, README, CONTRIBUTING, any docs index. Note which exist.
- From each, list every file path, link, directory, and command it names. That set is hop 1; anything hop-1 files name is hop 2.
- Inventory the actual surface: docs, scripts, configs, tests, tooling directories.

## Phase 2 — Audit through 8 lenses
1. **Entry reciprocity** — do the entry files name each other? A reader landing on README should be one hop from CLAUDE.md and vice versa — parallel universes are a smell
2. **Two-hop reach** — what fraction of docs, scripts, and tooling is reachable within two hops of an entry file; list the far side
3. **Orphan sweep** — files nothing points at: stale drafts, tools nobody will rediscover, reports whose home was never stated
4. **Taxonomy coverage** — if the entry file classifies the tree (edit these / never edit these / generated), does every top-level file fall under exactly one class; list the unclassified
5. **Generated vs source** — can a newcomer tell what is hand-written from what a build emits, without running the build
6. **Command discoverability** — every dev command (build, test, lint, release, one-off scripts) stated in an entry file, or do some live only in CI configs and shell history
7. **Staleness** — breadcrumbs that lie: paths that moved, commands that changed, docs contradicting the code they describe
8. **Unwritten rules** — conventions the code or CI enforces that no doc states, and stated rules nothing enforces

## Phase 3 — Curate
- For each orphan or unreachable file, decide: link it, classify it, relocate it, or question its existence.
- Rank fixes by how many future wrong turns one sentence or link prevents. A one-line taxonomy entry usually beats a new doc.

## Phase 4 — Report
Create `BREADCRUMBS.md` at repo root:
1. **Reachability map** — entry files found, and what share of the repo they reach in two hops
2. **Broken and missing links** — reciprocity gaps and lying breadcrumbs, with evidence
3. **Orphans and unclassified files** — each with a verdict: link, classify, move, or delete
4. **Fixes** — ranked; cross-linking the entry files and completing the taxonomy usually come first

Start the report with today's date. If `BREADCRUMBS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- A path you can find only by already knowing it is not a breadcrumb — judge reachability from the entry files alone
- Distinguish unreachable from deliberately internal — flag it, don't presume intent
- No documentation surface at all, not even a README? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which breadcrumbs to lay first
