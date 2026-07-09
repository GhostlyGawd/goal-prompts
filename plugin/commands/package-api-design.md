---
description: "Read the package the way a stranger's bundler does — every export weighed, typed, and judged: the accidental API, the semver debt, and what the next major must break."
---

# Goal: Library & Package API Design

You are working inside this repo. Mission: audit this package's public surface the way its consumers experience it — every export is a promise, every type is documentation, every past release is a semver precedent — and find the API that shipped by accident.

Read-only pass. Read the entry points, types, manifest, and release history; build the package if you can. Your only write is the report file.

## Phase 1 — Enumerate the promises
- List everything actually importable: the entry points the manifest exposes (`exports`, `main`, module roots) and every symbol reachable through them — not what the README says, what the resolver finds.
- Diff that list against the documented surface: the exports no doc mentions are still API, someone depends on them.
- Read the release history (tags, changelog) and note the versioning discipline it reveals.

## Phase 2 — Audit through 7 lenses
Cite the export, file:line, or the release that set the precedent.
1. **The accidental API** — internals reachable via deep imports or re-export sprawl; helpers exported "temporarily" years ago; everything public that never chose to be
2. **Naming as a system** — do exports read as one vocabulary (create/make/build chosen once, consistent argument order), or as strata of different eras
3. **Types that teach** — do signatures make misuse unrepresentable and let the editor teach the API, or is it `options: any` all the way down
4. **Semver honesty** — past minors that broke consumers (check the changelog against the diffs); the unreleased breaking change sitting on main right now
5. **Weight & shaking** — can a bundler take one function without the whole package: side effects on import, `sideEffects` flag, ESM/CJS duality, heavy deps a consumer inherits
6. **Error contract** — what throws vs returns, typed errors consumers can catch, failure behavior documented per export or discovered in production
7. **Deprecation hygiene** — a marked, dated path from old API to new, or removals that arrive as surprises

## Phase 3 — Curate
- Rank by consumer blast radius: a break in the most-imported export outranks ten awkward names.
- Sort every finding into: fix in a patch, fix in a minor, or owes the next major — that sorting is the release plan.
- The surface should shrink: every export kept must justify itself.

## Phase 4 — Report
Create `PACKAGE.md` at repo root:
1. **Surface ledger** — export · documented? · typed? · used in any example? · verdict: keep / deprecate / hide
2. **Findings** — each: lens · location · consumer impact · the fix · patch, minor, or major
3. **The next major, rehearsed** — everything worth breaking at once, with the migration note each break owes
4. **Semver debt** — the precedents already set (accidental API, past sneaky breaks) and what honoring them costs

Start the report with today's date. If `PACKAGE.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- What the resolver can reach is the API, whatever the docs claim
- Every proposed break names its migration path; a major version is a promise too
- No published or publishable package in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which surface changes to plan first
