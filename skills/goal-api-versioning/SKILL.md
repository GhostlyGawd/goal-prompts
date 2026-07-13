---
name: goal-api-versioning
description: "How the API evolves without breaking the people who built on it — the versioning scheme, breaking-change discipline, and how deprecations are announced and retired. Goal Prompt 113 · API — inspects the current repo and writes VERSIONING.md at the repo root."
---

# Goal: API Versioning & Deprecation

You are working inside this repo. Mission: judge how this API changes over time — whether it can add and evolve without breaking existing integrations, and whether deprecations are announced, dated, and migratable rather than sprung on people.

Read-only pass. Read the API surface, its versioning, and its change history; change nothing but the report file.

## Phase 1 — Learn how it changes
- Identify the versioning scheme, if any, and how consistently it is applied.
- Look at recent changes: which were additive and which broke callers.
- Find how deprecations are currently signaled and communicated.

## Phase 2 — Audit through 7 lenses
1. **Versioning scheme** — a clear, consistent scheme (URL, header, or date) applied everywhere
2. **Breaking-change discipline** — a defined line for what counts as breaking, enforced not ad hoc
3. **Backward compatibility** — additive by default; old clients keep working
4. **Deprecation process** — how a deprecation is announced, signaled (headers, docs), and dated
5. **Sunset & migration** — a real timeline and a migration path, not an indefinite "deprecated"
6. **Change communication** — a changelog and notifications where consumers actually learn of changes
7. **Undocumented surface** — the fields and endpoints people depend on that were never meant to be public

## Phase 3 — Curate
- Rank by how many integrations a change would break and how little warning they'd get.
- For each gap, name the fix — a scheme, a compatibility rule, a deprecation header, a sunset policy.
- Separate a one-time cleanup from the ongoing policy that prevents the next break.

## Phase 4 — Report
Create `VERSIONING.md` at repo root:
1. **Current practice** — the versioning and deprecation reality today
2. **Breaking-change risks** — the changes or habits that will break callers, by exposure
3. **Policy** — the versioning scheme, compatibility rules, and deprecation timeline to adopt
4. **Signals** — the headers, changelog, and notices that keep consumers informed

Start the report with today's date. If `VERSIONING.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every consumer is code you cannot see; break it and you break trust silently
- A deprecation without a date and a migration path is just a warning nobody acts on
- No public API surface in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which versioning changes to make first
