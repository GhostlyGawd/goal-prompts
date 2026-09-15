# Venture workflow v1

Status: implemented; verification and review evidence in VENTURE_WORKFLOW_TASKS.md, 2026-09-14. Operator authorized the complete
spec → tasks → build → verification → review process. Scope is Venture first.

## Outcome and boundaries

Help an operator select one venture worth testing, evaluate it against explicit
constraints and evidence, and choose the cheapest test that could overturn the
decision. Eight reports are evidence, not the success metric. Preserve the static,
stdlib-only, host-portable product; no scheduler, hosted state, autonomous outreach,
UI redesign, or catalog-wide contract migration.

## Requirements and acceptance

| ID | Requirement | Acceptance example |
| --- | --- | --- |
| V01 | Read charter and operator context; distinguish discovery from evaluating an existing venture. Ask only for missing decisions that affect scope. | An empty repo can discover candidates after intake; absence of code is not a null trigger. |
| V02 | Freeze explicit decision bars before conclusions; retain revisions and exposure to prior evidence. | Standalone verdict with prior conclusions labels its bars retrospective. |
| V03 | Select one venture after 60 and one wedge after 65, by operator or explicit delegation. | No selection means dependent stages wait; no silent candidate drift. |
| V04 | Declare ordered dependencies, stage closing decisions, research budgets and early-stop rules. | Weak demand permits insufficient evidence; a pivot invalidates affected reports. |
| V05 | Distinguish direct evidence, proxies, inference and assumptions, with source/access dates and counterevidence. | Repeated citations are one source; quota shortfalls are disclosed. |
| V06 | Preserve one report per brief, root-or-reports paths, four phases, ≤4,000 body characters, and research-only writes. | Standalone installed brief works without conductor or validator. |
| V07 | Conductor creates/updates INDEX.md and venture-run.json in reports from preflight onward, with recovery decisions and versions. | Fresh session resumes using files without conversation; unrelated index content survives. |
| V08 | Reuse requires scope/freshness review; content hashes identify changed reports and dependencies. | Changed input rejects a dependent report until rerun or explicitly revalidated. |
| V09 | Validate structural readiness with an optional stdlib CLI; never imply semantic truth or runtime control. | Missing/empty report, wrong scope, stale hash or invalid state returns nonzero. |
| V10 | Use the same venture conductor text across Python build, browser and MCP; support partial/mixed sequences. | Full Venture, [62,67], and [60,47] have parity; non-Venture conductors remain unchanged. |
| V11 | Research authorization does not authorize outreach, spending or code edits. Respect prior authorization and explicit commit preference. | Dirty tree is preserved; explicit path staging never sweeps unrelated changes. |
| V12 | End with go/pivot/kill/insufficient evidence and ranked experiments with success/stop criteria. | Fixer offered only for selected implementation; handoff works after early stop. |
| V13 | Verify packaging, compatibility and scenario behavior; record limitations honestly. | Build/check and scenario tests pass; agent trials retain their actual transcript. |

## State and validation boundary

The conductor owns `reports/INDEX.md` and `reports/venture-run.json`; workers write
only their assigned report. Both paths preserve existing content/history before
replacement. Report paths stay `reports/FILE.md`; root reports can be adopted only
after scope review. The JSON format and runnable example live in
`workflows/venture-run.schema.json` and `docs/venture-workflow.md`.

States: pending, running, complete, reused, null, blocked, failed, stale, skipped.
Only complete/reused reports qualify as evidence; null describes inapplicability,
not lack of accessible evidence. Blocked/failed/stale/skipped are not completion.
Missing evidence can produce a complete report with an insufficient-evidence
conclusion. A stopped run may be a successful decision but is not an eight-stage
completion. At most one stage runs at a time.

Each report declares run ID, scope revision and brief ID. Each finished stage
records source identity, report hash, input report hashes, finding IDs and decisions.
Changing scope increments its revision and marks dependent work stale. Hashes detect
unrecorded changes; they do not prove that human revalidation was justified.

The validator is read-only. It checks JSON shape, safe relative paths, known Venture
outputs, report metadata/sections, report and dependency hashes, status/order and
terminal-run consistency. The agent checks evidence relevance, contradictions,
arithmetic, and whether decisions were legitimately delegated. It can perform the
same checks manually if Python/the optional tool is unavailable.

## Compatibility decisions

- Specialize any conductor containing 60–67, including mixed sequences. Other
  stages retain their own action gates; never describe an action brief as read-only.
- Reuse one canonical template, distributed through generated browser data and
  catalog data for MCP. Raw URLs, slugs, report names and installer grammar stay stable.
- Longer run instructions live in the conductor. Briefs remain self-contained and
  contain their own evidence/scope/standalone fallback rules.
- Preserve reports/ rather than introduce reports/venture/: this avoids breaking
  existing collectors. Run IDs and revisions separate histories.

## Spec review

Baseline `scripts/check`: passed (163 build tests; 41 engine tests, 6 environment
skips; installer, JS and MCP checks passed). Reviewed against CLAUDE.md, CHARTER.md,
CONTRIBUTING.md and PRODUCT_ALIGNMENT.md. Resolved: index created early supersedes
Venture's final-only index; conductor metadata is an explicit write exception;
insufficient evidence is not a null/kill; existing venture bypasses candidate
generation only by recorded reuse/skip; partial sequences cannot invent inputs.
No outstanding product decision blocks implementation. Catalog-wide alignment
drafts remain outside scope. Verification evidence will be recorded in the task file.
