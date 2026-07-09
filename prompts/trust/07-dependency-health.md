---
id: "07"
title: Dependency Health Check
family: Trust
question: is it safe?
output: DEPS.md
related: 85
tagline: Vulnerable, abandoned, oversized, or duplicated packages — the full health check on every dependency this project stands on, with removal candidates named.
---
# Goal: Dependency Health Check

You are working inside this repo. Mission: assess every dependency this project stands on — vulnerable, abandoned, oversized, duplicated — and produce a safe upgrade and removal plan.

This is the full health check — vulnerabilities, abandonware, weight, duplication. For pure version-lag and the cost of catching up, run 85.

Read-only pass: inspect manifests and lockfiles, run audit/outdated tooling. Your only write is the report file.

## Phase 1 — Inventory
- Count direct vs transitive dependencies per manifest.
- Run the ecosystem's audit and outdated commands; capture the raw counts.
- Note anything pinned oddly, forked, or vendored.

## Phase 2 — Audit through 7 lenses
1. **Known vulnerabilities** — from audit output; note which are reachable in this codebase vs theoretical
2. **Abandonware** — no release in 2+ years, archived repos, sole-maintainer risk on critical paths
3. **Version lag** — majors behind; size the breaking distance for each big jump
4. **Heavyweights** — large packages used for one function; note the native or small replacement
5. **Duplicates & overlaps** — two libraries doing the same job (dates, HTTP, state)
6. **License risk** — anything incompatible with how this project ships
7. **Hygiene** — missing lockfile, loose version ranges, install scripts from untrusted packages

## Phase 3 — Curate
- Order upgrades safest-first: patch bumps → minors → risky majors
- Every removal candidate names its replacement (native API, stdlib, or nothing)
- Estimate blast radius per change: files touched, APIs changed

## Phase 4 — Report
Create `DEPS.md` at repo root:
1. **Health snapshot** — counts: total, vulnerable, outdated, abandoned
2. **Upgrade sequence** — ordered list: package · from → to · risk · what might break · effort
3. **Removal candidates** — package · used for · replacement · size saved
4. **One-command wins** — safe fixes runnable today
5. **Watch list** — fine now, risky later

Start the report with today's date. If `DEPS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Reachability matters: a vuln in an unused code path is lower priority — say so
- Never recommend a major upgrade without naming its breaking changes
- No third-party dependencies in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which changes to apply
