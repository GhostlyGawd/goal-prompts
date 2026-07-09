---
description: "Kill every dependency on paper — trace the actual catch, timeout, and fallback code, or its absence — and script the game day before production improvises one."
---

# Goal: Failure-Injection Readiness

You are working inside this repo. Mission: kill each dependency on paper and trace, in the code, what actually happens — not what the architecture diagram promises. The deliverable is a death table backed by file:line evidence and a game-day script worth running.

Read-only pass. Your only write is the report file.

## Phase 1 — Build the kill list
- Enumerate the dependencies from the code, not from memory: every client constructor, connection string, SDK import, and external URL in config. Each is a thing that can die.
- For each, find its call sites and mark the ones on the user-facing critical path.
- Note which have any redundancy — replicas, fallbacks, queues — and which are load-bearing singletons.

## Phase 2 — Kill each through 6 lenses
Every verdict cites the handling code — the try/catch, timeout, retry, circuit, fallback — or names its absence, by file:line. "Probably fine" is not a finding.
1. **Hard down** — the call throws: trace the exception's path to the user; crash, hang, or degrade — at boot and mid-request separately
2. **Slow, not dead** — find the timeout configured on each client, or prove it's missing; an unset timeout is an infinite one
3. **Erroring at 10%** — intermittent failure: does retry logic exist, is it bounded, and does it shed load or amplify it into a storm
4. **Wrong answers** — the dependency returns 200 with garbage: what validates responses before they reach business logic
5. **Health-check honesty** — read what the health endpoint actually verifies; "process is up" while every downstream is dead is a lie that routes traffic
6. **Detection** — for each kill, name the alert, log line, or metric that would fire; if you can't cite one, the failure is invisible

## Phase 3 — Curate
- Rank by blast radius × likelihood; the unredundant dependency on the money path tops the list.
- Split findings into known-bad (the code handles it wrongly — cited) and unknown (no handling found; the experiment exists to find out).
- For each unknown, design the cheapest safe experiment: what to kill, where (staging, a game day), and the abort condition.

## Phase 4 — Report
Create `CHAOS.md` at repo root:
1. **The death table** — dependency · kill method · predicted behavior · handling code (file:line) or "none found" · detection signal
2. **Single points of failure** — the load-bearing singletons, ranked
3. **Game-day script** — the top 3 experiments: steps, expected outcome, feared outcome, abort condition
4. **The first fix** — the one timeout, fallback, or health-check correction that removes the most risk before any experiment runs

Start the report with today's date. If `CHAOS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every prediction cites the handling code or names its absence — an untested resilience assumption is a hope with good PR
- Experiments are safe by design: staging first, abort conditions always; a game day must not become an incident
- No external dependencies whose failure could hurt in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which failure experiments to run first
