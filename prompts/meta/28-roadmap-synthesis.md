---
id: "28"
title: Roadmap Synthesis
family: Meta
question: do the reports compose?
output: ROADMAP.md
tagline: The capstone. Reads every audit report in the repo, dedupes overlapping findings, and merges them into one sequenced plan.
---
# Goal: Roadmap Synthesis

You are working inside this repo. Mission: read every audit report at the repo root — the outputs of prior goal prompts — and merge them into one deduplicated, dependency-aware, sequenced roadmap.

This is synthesis, not re-auditing: work from the reports, dipping into code only to resolve conflicts. Your only write is the report file.

## Phase 1 — Collect
- Find the audit reports at repo root: IMPROVEMENTS.md, BUGS.md, PERF.md, SECURITY.md, TESTING.md, and any others matching this family.
- List what exists and what's missing; note which absent audits would most change this roadmap.

## Phase 2 — Normalize
- Extract every item into one pool: source report · name · impact · effort · tags.
- Dedupe: the same underlying issue often surfaces in multiple audits (a god file flagged by DEBT and HOTSPOTS; a slow query in PERF and COSTS). Merge them, keeping all evidence and the strongest framing.
- Find themes: many items, one root cause — name the root cause as its own item.

## Phase 3 — Sequence
- Score globally: impact, effort, risk — recalibrated across all reports on one scale.
- Map dependencies BETWEEN items: fixes that unlock others, refactors that make features cheap, tests that de-risk migrations.
- Balance the mix: pure risk-reduction and pure growth are both losing strategies; interleave them.

## Phase 4 — Report
Create `ROADMAP.md` at repo root:
1. **Sources** — reports found, reports missing, and the audit to run next
2. **Unified backlog** — deduped table: item · sources · impact · effort · dependencies
3. **Themes** — root causes worth one structural fix instead of five patches
4. **Three milestones** — Now (1–2 weeks) · Next (a month) · Later — each with its items and the one-line story of why this order
5. **Merge log** — what was deduplicated, so nothing looks lost

## Rules
- Every roadmap item traces to a source report — no new findings smuggled in
- When reports disagree on priority, say so and rule with reasoning
- Report only — end by asking whether to adjust the sequence
