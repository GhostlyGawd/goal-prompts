---
id: "102"
title: Test-Pyramid Balance
family: Quality
question: does it work?
output: PYRAMID.md
tagline: The shape of the suite — whether the mix of unit, integration, and end-to-end tests gives fast, reliable confidence or a slow, brittle inversion.
---
# Goal: Test-Pyramid Balance

You are working inside this repo. Mission: judge the shape of the test suite — the balance of unit, integration, and end-to-end tests — and whether it buys fast, reliable confidence or a slow, flaky, top-heavy mess.

Read-only pass. Read the tests, their layers, and their run times; change nothing but the report file.

## Phase 1 — Measure the shape
- Count tests by layer: unit, integration, end-to-end.
- Note how long each layer takes and how much of total suite time it consumes.
- Sketch the current shape: pyramid, hourglass, ice-cream cone, or hollow.

## Phase 2 — Audit through 7 lenses
1. **The shape** — the actual ratio of unit to integration to e2e; top-heavy, hollow, or balanced
2. **Slow-test concentration** — how much suite time a few heavy tests consume
3. **Redundant coverage** — the same logic verified at three levels; e2e doing a unit test's job
4. **Gaps by layer** — logic with no unit test; integrations with no integration test
5. **Confidence per second** — where the suite buys the most assurance per unit of runtime
6. **Brittleness** — layers that break on unrelated changes and need constant upkeep
7. **Missing layer** — a whole category absent: no integration tests, no smoke test

## Phase 3 — Curate
- Rank changes by confidence gained or time saved: pushing a slow e2e check down to a unit test often wins both.
- For each imbalance, say what to add, move down a layer, or delete.
- Protect real coverage; the goal is a better shape, not fewer tests.

## Phase 4 — Report
Create `PYRAMID.md` at repo root:
1. **Current shape** — counts and time by layer, and the shape they form
2. **Imbalances** — where it is inverted, hollow, or redundant, with evidence
3. **Rebalance plan** — tests to add, push down, or remove, each with the payoff
4. **Target shape** — the mix to aim for and the first move toward it

## Rules
- Favor the cheapest layer that can catch the bug
- Deleting a redundant slow test is a win, not a loss of coverage
- Report only — end by asking which rebalancing to do first
