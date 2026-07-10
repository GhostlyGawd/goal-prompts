---
name: goal-debuggability
description: "How hard it is to find out why something broke — whether the system helps a developer localize a failure or forces guesswork. Audit brief 95 · Team — runs a four-phase audit of the current repo and writes DEBUG.md at the repo root."
---

# Goal: Debuggability Audit

You are working inside this repo. Mission: judge how quickly a developer can go from "something is wrong" to "here is exactly why" — whether the code, logs, and tooling localize a failure or leave you guessing.

Read-only pass. Read logging, error handling, and observability setup; trace a real recent failure if you can. Change nothing but the report file.

## Phase 1 — Diagnose something
- Pick a plausible failure (or a real recent bug) and try to diagnose it using only what the system provides.
- Note where you could see what happened and where the trail went cold.
- Check what a developer would reach for first: logs, a stack trace, a reproduction.

## Phase 2 — Audit through 7 lenses
1. **Reproducibility** — can a reported bug be reproduced locally; seed data, fixtures, a way to replay
2. **Developer logging** — logs present, structured, and at a level that lets you trace a failure
3. **Error context** — do errors carry inputs, ids, and a stack, or vanish into a generic message
4. **Stack traces & source maps** — do production errors point back to real code
5. **Correlation** — request ids and tracing to follow one operation across layers or services
6. **Local debugging** — breakpoints, a REPL, running a single failing path in isolation
7. **State inspection** — can you see the data and state at the moment of failure

## Phase 3 — Curate
- Rank by how much each gap slows a real diagnosis, weighted by how often that area breaks.
- For each, name the instrumentation that would have made the failure obvious.
- Separate "add logging" from "the design hides state"; flag the structural ones.

## Phase 4 — Report
Create `DEBUG.md` at repo root:
1. **A diagnosis, walked** — tracing a real failure, and where the trail went cold
2. **Findings** — each: gap · location · how it slows diagnosis · the fix
3. **Instrumentation plan** — the logs, ids, and hooks that would make failures self-explaining
4. **Quick wins** — the two changes that most improve time-to-root-cause

Start the report with today's date. If `DEBUG.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Judge the path to root cause, not the presence of a logger
- Context at the point of failure beats a wall of logs after it
- No runtime code to debug in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which debuggability gaps to close first
