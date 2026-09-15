# Venture workflow implementation and evidence

Specification: [VENTURE_WORKFLOW.md](VENTURE_WORKFLOW.md).

| Task | Requirements | Deliverable | Verification | Status |
| --- | --- | --- | --- | --- |
| T1 | V01–V04,V07,V10–V12 | Canonical venture conductor and generator integration | Python/browser/MCP parity; non-Venture regression | done |
| T2 | V01–V06,V12 | Eight revised briefs | Linter and stage-specific contract tests | done |
| T3 | V07–V09,V11 | JSON schema, read-only validator and usage docs | Disposable-repo valid/invalid state scenarios | done |
| T4 | V06,V10,V13 | Regenerated raw, plugin, skill, catalog distributions | Full scripts/check; package contents | done |
| T5 | V01–V13 | Scenario evaluation and final review | Recorded trial + requirement review + diff check | done |

Dependencies: T1/T2 define the report contract consumed by T3; T4 follows T1–T3;
T5 follows the integrated build. Each task has observable checks rather than a
restatement of its edits. Requirement coverage: every V01–V13 appears above;
standalone, partial and mixed sequences, stopping and recovery are included.

## Task-list review

2026-09-14: checked dependency order, requirement coverage, three conductor paths,
generated artifacts, dirty-tree handling and test limitations. The task list is
ready for implementation. No delegated agents required for implementation.

## Verification record

- Baseline: `scripts/check` passed before source edits.

## Implementation evidence

- T1: `workflows/venture-conductor.md` is canonical. Python renders directly;
  build-generated browser data and catalog.json/MCP render the same template.
  Full [60–67], partial [62,67], mixed [60,47], standalone [67], and selected
  subsequence [60,61,65] have byte-for-byte parity tests. Existing 40-playbook
  browser/Python parity and generic MCP assertions also pass.
- T2: All eight briefs rewritten in place; four phases, one report, existing URLs,
  filenames and root/reports behavior retained. Bodies remain below 4,000 chars.
  Venture lint guards charter, run context, source dates, counterevidence, input
  versions and write boundary. These lexical checks are not semantic certification.
- T3: schema and Python 3.9+ read-only checker exported through raw/ and included
  by npm packaging. Tests cover missing/empty reports, malformed state, unsafe paths,
  changed scope/hashes, missing dependencies, sequential execution, null/early stop,
  pause/failure, no-git and preservation of unrelated content.
- T4: `scripts/check` passed: 179 Python repository tests; 41 engine tests with six
  pre-existing environment skips; installer, JS and MCP suites passed. `npm pack
  --dry-run --json` confirmed validator, schema, catalog and MCP inclusion.
- T5: one synthetic all-eight-stage agent trial preserves TutorFollowup and ends
  insufficient evidence; all stage checks passed. The trial disclosed prior exposure
  to fixture facts before setting bars. Fresh-process recovery verified saved state
  and hashes. Final report review caught missing local Niche interview thresholds,
  which were repaired with a preserved dependency revalidation trail. A separate
  fresh agent recovered scope/authority/next action and identified three further
  test-specificity gaps. Those were repaired; all affected reports were explicitly
  revalidated with original criteria and scope unchanged. Root review checked the
  repaired sections and current validator against the retained artifacts.

## Final review checklist

- [x] V01–V06: operator/discovery handling, fixed scope, original/retrospective bars,
  evidence classes, shortfall handling, counterevidence, one report and body limits.
- [x] V07–V09: persistent index/state, safe output paths, source/input hashes, explicit
  stale/reuse decisions, read-only validation and manual fallback.
- [x] V10–V12: full/partial/mixed integration, independent action gates, non-go pause
  before mixed build stages, explicit-path commit instructions, experimental handoff.
- [x] V13: packaging, regression checks and retained simulated trial evidence.
- [x] Trial repairs and fresh-session review receipts retained in
  `evals/results/venture-workflow-v1/`; final full gate passed.

Limitations: a prompt and optional checker do not enforce behavior inside arbitrary
agent hosts. Semantic evidence quality, decision authority and commercial viability
still require review. This is not a live-market validation, a cross-model efficacy
comparison, a tested Git commit-failure flow, or proof that every network fallback
works. The trial uses authorized offline synthetic sources. Release and deployment remain outside this implementation. Catalog-wide alignment remains outside scope.


## Review disposition

No unresolved blocking implementation findings. Fixed during verification: raw-tool
export was initially removed by output regeneration; malformed state types could
raise instead of returning validation errors; report tests needed local thresholds;
remaining critical unknowns needed explicit follow-up tests. Corresponding regression
checks and instruction refinements are in the final change. A fresh-session review
and original/repair artifacts are retained, including passing and intentionally
failing stale-state check receipts. Captured trial instructions are immutable and
predate the small review-driven wording refinements; current structural validation
also passes on the final retained reports. Live-market efficacy remains unmeasured.

Final receipts: `evals/results/venture-workflow-v1/repository-check.txt`; retained
trial passes the current checker with `--final`. Rebuilding tracked outputs is
idempotent; `git diff --check` passed. Operator approved the reviewed result for commit and pull-request handoff on
`feat/venture-workflow-v1`. No merge or production deployment is included.
