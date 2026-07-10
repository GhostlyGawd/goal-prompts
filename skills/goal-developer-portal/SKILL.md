---
name: goal-developer-portal
description: "The first hour a developer spends with this API — from landing on the docs to a working integration — and where they stall, guess, or give up. Audit brief 115 · API — runs a four-phase audit of the current repo and writes DEVPORTAL.md at the repo root."
---

# Goal: Developer Portal & Onboarding

You are working inside this repo. Mission: judge the developer's first hour — from finding the docs to making a real call work — because adoption is won or lost before they ever build the actual integration.

This judges the portal and docs — the path to a working call. For the ergonomics of the SDK itself, run 112.

Read-only pass. Read the docs, quickstart, reference, and auth setup; follow them yourself if you can. Change nothing but the report file.

## Phase 1 — Onboard yourself
- Start where a new developer starts and try to reach a first successful call.
- Note where you have to guess, search, or leave the docs to make progress.
- Check the path to credentials and authentication.

## Phase 2 — Audit through 7 lenses
1. **Time to first call** — how fast a developer gets from docs to a successful request
2. **Key & auth setup** — getting credentials and authenticating: self-serve, clear, quick
3. **Quickstart honesty** — a copy-paste example that actually works, in the reader's language
4. **Reference quality** — complete, accurate endpoint docs with real request and response examples
5. **Sandbox & testing** — a way to try calls safely: test keys, example data
6. **Errors as docs** — do API errors teach (clear codes, links) or send you back to searching
7. **Discoverability** — can a developer find the one thing they need without reading everything

## Phase 3 — Curate
- Rank by how many developers stall at each point and how early it is in the journey.
- For each, name the fix — a working example, a test key, a clearer reference, a searchable doc.
- Weight the first ten minutes most; that is where people decide to continue or leave.

## Phase 4 — Report
Create `DEVPORTAL.md` at repo root:
1. **First hour, walked** — the path to a working call, with every stall
2. **Findings** — each: lens · location · what a developer hits · the fix
3. **Time-to-integration** — the reality today and the achievable target
4. **Highest leverage** — the fixes that most shorten the path from docs to done

Start the report with today's date. If `DEVPORTAL.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Judge the path to a working call, not the prettiness of the docs
- A quickstart that does not run is worse than none; it burns trust
- No developer portal or public API docs in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which onboarding fixes to make first
