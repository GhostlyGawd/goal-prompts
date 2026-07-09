---
id: "22"
title: Git Hotspot Mining
family: Data
question: is it sound?
output: HOTSPOTS.md
tagline: Mine the git history for churn, bug magnets, coupled files, and bus-factor silos — predict where the next bug lands.
---
# Goal: Git Hotspot Mining

You are working inside this repo. Mission: mine the git history for what the code alone can't tell you — where change concentrates, where bugs cluster, which files secretly move together, and where knowledge lives in one head.

Read-only pass: git log analysis only. Your only write is the report file.

## Phase 1 — Extract the history
Run read-only git analysis (adjust ranges to repo age):
- Churn leaders: file change frequency (git log with name-only output, aggregated)
- Fix magnets: files most present in commits whose message contains fix/bug/hotfix
- Coupling: files that repeatedly appear in the same commits
- Authorship: files/areas with a single significant author

## Phase 2 — Interpret through 6 lenses
1. **Churn × size** — files both large and frequently edited: the highest-risk quadrant
2. **Bug magnets** — the fix-commit leaders; is each inherently hard, or badly structured?
3. **Temporal coupling** — files that change together but live far apart: a hidden dependency or a missing abstraction
4. **Knowledge silos** — single-author critical areas: the bus-factor map
5. **Stale foundations** — old, untouched code that everything depends on; is stability maturity or fear?
6. **Trajectory** — is churn concentrating (a hardening core) or spreading (architecture erosion)?

## Phase 3 — Curate
- Numbers required: every claim carries its counts
- Cross-check against the code: history flags, code confirms

## Phase 4 — Report
Create `HOTSPOTS.md` at repo root:
1. **Hotspot ranking** — file · commits · fix-commits · size · verdict
2. **Coupling pairs** — with the suggested resolution: merge, extract shared piece, or accept
3. **Silo map** — area · owner · risk · suggested pairing or docs
4. **Prediction** — where the next bug statistically lands, and the preemptive move
5. **Refactor targets** — justified by history, not taste

Start the report with today's date. If `HOTSPOTS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- History over opinion: churn data outranks aesthetic judgments
- A hotspot earns refactoring only if it's still changing
- No meaningful git history (fresh or shallow clone) in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which target to address
