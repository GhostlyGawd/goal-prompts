---
description: "Point it at a diff, branch, or PR: blast radius, the tests that should exist, the migration and rollback story, and a go / no-go with the risks ranked."
---

# Goal: Change Risk Review

You are working inside this repo. Mission: assess one proposed change — a diff, a branch, or a PR — before it merges. Not a whole-repo audit: this brief is scoped to what the change touches and what it puts at risk. Read-only; the code change already exists, you only judge it.

Establish the diff first (`git diff main...HEAD`, a PR, or the range you are given). Your only write is the report file.

## Phase 1 — Scope the change
- Summarize what the change does and why, from the diff and its description.
- List every file touched and trace outward one hop: who calls this, what depends on the changed behavior?
- Flag the high-consequence surfaces in the diff: auth, money, data writes, migrations, public contracts, config.

## Phase 2 — Audit through 8 lenses
Cite the hunk (file:line in the diff) for every finding.
1. **Blast radius** — what breaks if this is wrong; how far the change reaches beyond the files it edits
2. **Test coverage** — does the change add or update tests for its new behavior and edge cases, or ship untested; which path has no assertion
3. **Backward compatibility** — changed API shapes, schemas, config keys, or events that existing clients, data, or callers still rely on
4. **Migration & data** — schema or data migrations in the diff: reversible, safe under load, ordered against the code change (see 71)
5. **Rollback story** — can this be reverted cleanly, or does it strand data and need a forward-fix; are feature flags used for risky paths
6. **Security surface** — new inputs, permissions, dependencies, or secrets introduced by the change (see 06)
7. **Hidden coupling** — shared state, globals, or ordering the change quietly depends on or breaks
8. **Scope creep** — unrelated edits riding along that dilute review and widen the risk

## Phase 3 — Curate
- Separate merge-blockers (untested money path, irreversible migration) from nits (a rename).
- For each risk: the failure it could cause in production and the smallest thing that would de-risk it.
- Weigh the change's value against its risk honestly.

## Phase 4 — Report
Create `CHANGE-RISK.md` at repo root:
1. **Go / no-go** — a one-line verdict and the top risk if it ships as-is
2. **Change summary** — what it does, what it touches, blast radius
3. **Risks** — each: Concern · Lens · Hunk (file:line) · Failure mode · De-risk step · Blocker or not
4. **Missing tests** — the specific cases worth adding before merge

Start the report with today's date and name the change under review. If `CHANGE-RISK.md` already exists, it almost certainly reviewed a different change — note which change it covered, then replace it; only diff against it if it reviewed this same change.

## Rules
- Judge only the change and what it touches, not the whole repo
- Every risk cites a hunk and names a concrete failure mode
- No pending or recent change to review in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which blockers to resolve before merge
