---
id: "85"
title: Dependency Currency Audit
family: Trust
question: is it safe?
output: UPGRADES.md
related: 07
tagline: Run the outdated command and read the lockfile's birthdays — majors behind, EOL dates, the two packages pinning everything — and the forced jump the drift is scheduling.
---
# Goal: Dependency Currency Audit

You are working inside this repo. Mission: measure — not estimate — how far the dependency tree, runtime, and toolchain have drifted from current, find what is pinning the drift in place, and forecast the forced jump that lands if nothing moves.

This is the currency lens: how far behind, and what catching up costs. For vulnerabilities, weight, and duplication, run 07.

Read-only pass. Run the ecosystem's outdated and EOL checks; read manifests, lockfiles, and changelogs; change nothing. Your only write is the report file.

## Phase 1 — Measure the drift
- Run the outdated command (`npm outdated`, `pip list --outdated`, `cargo outdated`, ...) and capture the raw table; that is your evidence base.
- Record the runtime and toolchain versions — language, framework, builder — and each one's EOL date from its published schedule.
- Date the drift's velocity, not just its size: when did the lockfile last meaningfully change (`git log` on it)?

## Phase 2 — Audit through 6 lenses
Every lag claim carries a number from Phase 1: versions behind, a release date, or an EOL date.
1. **Major distance** — per significant dependency: majors behind × age of the pinned version; a 2019 pin is a fact — cite it
2. **EOL exposure** — runtime or framework past, or within a year of, end-of-life on the published schedule, dated
3. **Pins with reasons** — every forced version or resolution override: find the commit or comment that explains it, or flag it as a fossil nobody dares touch
4. **Blockers** — the one or two packages whose upgrade unblocks a cascade; name what each holds back, from the dependency graph
5. **Transitive drag** — current directs holding outdated transitives; the drift the manifest hides
6. **Cadence evidence** — a bot configured? bot PRs actually merged in the log? or does the lockfile only move when something breaks — cite the history

## Phase 3 — Curate
- Rank by the cost of staying: EOL runtimes and security-sensitive lag outrank cosmetic minors.
- Sequence the catch-up: cheap bumps that shrink the surface, then the blocker, then the cascade it frees.
- Write the forced-jump forecast: if nothing moves for a year, name the upgrade that becomes a rewrite.

## Phase 4 — Report
Create `UPGRADES.md` at repo root:
1. **Drift ledger** — dependency · pinned · latest · majors behind · pinned version's release date · EOL date where one exists
2. **The blockers** — what pins the tree, the evidence, and what each unlocks
3. **Catch-up sequence** — ordered: bumps → blocker → cascade, each sized S/M/L
4. **Forced-jump forecast** — the emergency this drift is scheduling, narrated in three sentences

Start the report with today's date. If `UPGRADES.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every number comes from a command, a changelog, or a schedule — never from memory
- A major bump is a project, not a bump; size it like one
- No dependency manifest in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which upgrades to take on first
