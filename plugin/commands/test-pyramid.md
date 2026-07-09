---
description: "Count and time the suite by layer, draw the shape it actually makes, and compute confidence-per-second — the number that says which tests earn their runtime."
---

# Goal: Test-Pyramid Balance

You are working inside this repo. Mission: measure the test suite's real shape — count and time every layer, draw it — and find where confidence is bought at the wrong price: e2e tests doing a unit test's job, seams with no cheap layer under them at all.

Read-only pass. Run the suite or its layers to get real timings if you can; change nothing but the report file.

## Phase 1 — Classify and count
- Sort every test into a layer by what it touches, not by its directory name: unit (no I/O), integration (real DB, network, or filesystem in fixtures), e2e (browser or full-process driver). Note the tests whose directory lies about their layer.
- Count per layer and time per layer — run the suite if possible, else read CI logs. Real seconds, not folklore.
- Record the ten slowest tests by name, with seconds each.

## Phase 2 — Audit through 6 lenses
Every claim names tests by file, with counts or seconds.
1. **Misfiled confidence** — e2e or integration tests asserting pure logic; name the test and the function it round-trips the world to reach
2. **The missing layer** — a whole category absent: no integration seam between mocks and browser, or no smoke test at all; name what nothing covers
3. **Triple coverage** — the same behavior asserted at two or three layers; cite the redundant pair and which is cheaper
4. **The slow ten** — for each of Phase 1's ten: what it uniquely proves, or whether a lower layer already proves it
5. **Mock drift** — unit-layer mocks encoding shapes the integration layer or real fixtures contradict; the pyramid's layers disagreeing with each other
6. **Confidence per second** — per layer: what only that layer can catch, against the seconds it costs; the worst ratio is the rebalancing target

## Phase 3 — Curate
- Rank moves by seconds saved × confidence kept: pushing one slow e2e assertion down to a unit test usually wins both.
- Every move is concrete: this test → this layer, or delete — with the replacement named before the deletion.
- Protect the irreplaceable: the one true smoke test that proves the app boots stays, whatever it costs.

## Phase 4 — Report
Create `PYRAMID.md` at repo root:
1. **The shape, drawn** — an ASCII silhouette of the suite: one row per layer, width proportional to test count, annotated with seconds
2. **Confidence-per-second table** — layer · tests · seconds · what only it catches · verdict: grow / hold / shrink
3. **The slow ten** — each: seconds · what it proves · keep, push down, or delete
4. **Rebalance plan** — ordered moves, each with the seconds saved and the coverage that replaces it

Start the report with today's date. If `PYRAMID.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Counts and seconds come from running the suite or CI logs, never from directory names
- A redundant slow test is deleted only after its replacement exists; order matters
- No test suite to balance in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which rebalancing to do first
