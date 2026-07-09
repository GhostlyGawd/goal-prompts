---
id: "122"
title: Failure-Injection Readiness
family: Reliability
question: will it stay up?
output: CHAOS.md
tagline: Whether the system is ready to be tested against failure — and what would actually happen if its key dependencies died — before a real incident runs the experiment.
---
# Goal: Failure-Injection Readiness

You are working inside this repo. Mission: reason through what breaks when each key dependency fails, find the untested assumptions and single points of failure, and identify the failure experiments worth running deliberately — before production runs them for you.

Read-only pass. Read the architecture, health checks, and recovery behavior; change nothing but the report file.

## Phase 1 — Inventory dependencies and assumptions
- List every dependency whose failure could hurt, and what the system assumes about each staying up.
- Find the components with no redundancy — the ones whose loss is fatal.
- Note what health and readiness signals exist.

## Phase 2 — Audit through 7 lenses
1. **Dependency inventory** — every external dependency whose failure could hurt, mapped
2. **Known failure modes** — for each, what happens today if it is slow, erroring, or gone
3. **Single points of failure** — the components with no redundancy whose loss is fatal
4. **Health & readiness** — do health signals actually reflect the ability to serve, or just "process is up"
5. **Recovery behavior** — restart, reconnect, and self-heal under partial failure
6. **Observability under failure** — would you see what broke, quickly, when it does
7. **Safe-to-test** — can failure be injected in a controlled way (staging, a game day) without real harm

## Phase 3 — Curate
- Rank by likelihood × blast radius: a fragile single point of failure on the critical path tops the list.
- For each, note the assumption to test and how to test it safely.
- Separate "we know it fails badly" from "we don't know what happens"; the unknowns are the point.

## Phase 4 — Report
Create `CHAOS.md` at repo root:
1. **Failure matrix** — dependency × what happens when it fails today
2. **Single points of failure** — the fatal, unredundant components, ranked
3. **Untested assumptions** — the beliefs about resilience nobody has verified
4. **Experiments** — a prioritized set of failure tests to run safely, each with what it would prove

Start the report with today's date. If `CHAOS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- An untested resilience assumption is a hope with good PR
- Design the experiment to be safe first; a game day should not become an incident
- No production service to inject failure into in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which failure experiments to run first
