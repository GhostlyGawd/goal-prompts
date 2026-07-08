---
id: "85"
title: Dependency Currency Audit
family: Trust
question: is it safe?
output: UPGRADES.md
tagline: How far the dependency tree has drifted and how risky it is to catch up — the upgrade debt that compounds until a forced, painful jump.
---
# Goal: Dependency Currency Audit

You are working inside this repo. Mission: measure how far behind the dependencies, runtime, and toolchain have fallen, and how hard it would be to catch up — so the next upgrade is a routine step, not an emergency rewrite.

Read-only pass. Read manifests, lockfiles, and release notes; run read-only version checks; change nothing. Your only write is the report file.

## Phase 1 — Take inventory
- List direct dependencies with current vs latest version, and the language/runtime/build-tool versions.
- Flag the ones that matter: framework, database driver, auth, anything security-sensitive or load-bearing.
- Note the update mechanism, if any: a bot, a cadence, or only-when-it-breaks.

## Phase 2 — Audit through 7 lenses
1. **Version lag** — how many majors/minors behind each significant dependency runs
2. **End-of-life** — packages past support, abandoned, or with no release in a long time
3. **Breaking-change exposure** — deps pinned for a reason whose upgrade forces code changes
4. **Runtime & toolchain currency** — language, framework, and build tools nearing or past EOL
5. **Transitive drift** — outdated indirect deps held back by a lagging direct one
6. **Upgrade blockers** — the one or two packages that hold everything else back
7. **Update hygiene** — whether upgrades happen on a routine or only under duress

## Phase 3 — Curate
- Rank by risk of staying: EOL and security-sensitive lag outrank a cosmetic minor.
- Sequence the upgrades — what unblocks the most, and what must go first.
- Distinguish a safe bump from a migration; size each honestly.

## Phase 4 — Report
Create `UPGRADES.md` at repo root:
1. **Currency table** — dependency · current · latest · lag · EOL status
2. **Forced-jump risks** — where staying put sets up a painful, all-at-once upgrade later
3. **Upgrade path** — a sequenced plan: quick bumps first, migrations scoped and ordered
4. **Cadence** — the bot or routine that keeps drift from returning

## Rules
- Currency is a security posture; unmaintained code is a latent vulnerability
- Size migrations honestly — a major bump is a project, not a bump
- Report only — end by asking which upgrades to take on first
