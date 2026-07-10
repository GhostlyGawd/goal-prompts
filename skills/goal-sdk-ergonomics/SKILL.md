---
name: goal-sdk-ergonomics
description: "The client libraries developers use to call this product — how fast they reach a first successful call, and how the SDK behaves when things go wrong. Audit brief 112 · API — runs a four-phase audit of the current repo and writes SDK.md at the repo root."
---

# Goal: SDK Ergonomics Audit

You are working inside this repo. Mission: judge the client library a developer installs to use this product — whether it gets them to a working call quickly, reads the way they think, and fails in ways they can handle.

This judges the SDK itself — the library in the developer's editor. For the docs-and-portal first hour around it, run 115.

Read-only pass. Read the SDK surface, its examples, and its error handling; try the quickstart if you can. Change nothing but the report file.

## Phase 1 — Take the first call
- Follow the quickstart from install to a first successful request; time it and note every snag.
- Read the public surface: the methods, their names, and their shapes.
- Trigger an error and see what the SDK gives you back.

## Phase 2 — Audit through 7 lenses
1. **Time to first call** — steps from install to a working request; whether the quickstart is honest
2. **Surface & naming** — methods that match how developers think; discoverable, consistent
3. **Defaults** — sensible defaults, minimal required config, safe-by-default behavior
4. **Error handling** — typed, catchable errors with context, not opaque failures
5. **Types & autocomplete** — typed surfaces that let the editor teach the API
6. **Built-in resilience** — retry, timeout, and pagination handled so every user isn't reinventing them
7. **Consistency & docs** — consistent patterns across methods; examples that actually run

## Phase 3 — Curate
- Rank by how many developers hit each and how early: a confusing first call outranks a rare edge method.
- For each, name the change — a clearer name, a default, a typed error, a retry built in.
- Note where a small ergonomic fix would cut real support load.

## Phase 4 — Report
Create `SDK.md` at repo root:
1. **First call, walked** — the path from install to success, with every snag
2. **Findings** — each: lens · location · what a developer feels · the fix
3. **Time-to-first-call** — the count today and the achievable minimum
4. **Highest leverage** — the handful of changes that most improve adoption and cut support

Start the report with today's date. If `SDK.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- The SDK is the API's user interface; judge it as a product, not a wrapper
- A good default removes a decision; a typed error removes a support ticket
- No SDK or client library in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which SDK improvements to make first
