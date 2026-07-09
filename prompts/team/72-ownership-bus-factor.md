---
id: "72"
title: Ownership & Bus Factor
family: Team
question: can others build on it?
output: OWNERSHIP.md
tagline: Read git history for the human risks — files only one person understands, critical paths with a truck factor of one, and the knowledge that leaves when they do.
---
# Goal: Ownership & Bus Factor

You are working inside this repo. Mission: read the history for human risk — the files only one person has ever touched, the critical paths whose every author has left, and the knowledge that walks out the door when one person does.

Read-only pass. Lean on `git log`, `git blame`, and `git shortlog`. Your only write is the report file.

## Phase 1 — Reconstruct who knows what
- Build a picture from history: per area, who authored it, who last touched it, how concentrated the authorship is.
- Cross-reference with the blast zones — auth, payments, data, the build — from earlier audits or a quick read.
- Note the signals of departure: top authors with no commits in the last N months.

## Phase 2 — Audit through 7 lenses
Name files and contributors (by handle) for every finding.
1. **Truck factor** — areas where one author owns nearly all the knowledge; the count of people whose loss would strand a critical path
2. **Orphaned code** — files whose every significant author has gone quiet or left; owned by nobody now
3. **Critical-path concentration** — the money/auth/data paths cross-referenced with ownership: single points of human failure
4. **Silent complexity** — high-churn or high-complexity files (see 22) that also have exactly one author: hardest to hand off
5. **CODEOWNERS reality** — is there an ownership file, and does it match who actually commits, or is it aspirational
6. **Documentation cover** — do the single-owner areas have any written explanation, or does the knowledge live only in one head
7. **Onboarding barrier** — the areas a new hire could never safely touch without the one person who understands them

## Phase 3 — Curate
- Separate genuine risk (a critical path with a truck factor of one) from the harmless (a solo-owned throwaway script).
- For each risk: what breaks if that person is unavailable, and the cheapest way to spread the knowledge (pairing, docs, a guided change).
- Rank by criticality × concentration.

## Phase 4 — Report
Create `OWNERSHIP.md` at repo root:
1. **Bus-factor verdict** — the lowest truck factor on a critical path, named
2. **Risk map** — area · primary owner · # who understand it · criticality · status
3. **Orphans** — code no active contributor owns
4. **De-risk plan** — the three handoffs worth doing first, and how

Start the report with today's date. If `OWNERSHIP.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- History is evidence; name the files and the commit pattern behind each claim
- Describe roles and risk, not judgments of people
- No multi-contributor history in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which handoffs to start
