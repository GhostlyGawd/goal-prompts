# Venture workflow agent trial — 2026-09-14

**SIMULATION ONLY.** This is behavioral QA using one synthetic packet, not real venture evidence. No live browsing, outreach, purchase, implementation, publishing or commit occurred. All writes were under `/tmp/venture-trial.OqM7Pp`. No git repository was initialized; the conductor's no-git path was exercised.

## Observed result

- Completed 60–67 sequentially for fixed `tutorfollowup-us@1`; preserved the selected venture and exercised delegated continuation/wedge selection without pivoting.
- Saved six explicit original decision bars before report conclusions. Fixture facts were already known and that exposure is disclosed; this was not blind preregistration.
- Created a synthetic source packet without fabricated quotes or external source links. Calendar success remains counterevidence. Competitor pricing is not adoption; contact count is not a customer count.
- Ruled **insufficient evidence**, with all six bars unknown. No missing evidence was converted into a kill verdict or falsely strong differentiation.
- Wrote index/state before work, persisted running/complete transitions with dated authority receipts, and verified every prior report hash before downstream stages.
- Eight stage structural checks and the final check returned exit 0. No validator failure occurred.

## Actual final checker output

Command: `python3 sources/venture_check.py /tmp/venture-trial.OqM7Pp --final`

```text
PASS structural readiness only; evidence quality and decision authority require review
Exit code: 0
```

Raw output: `audit/check-final.txt`; per-stage outputs: `audit/check-60.txt` through `audit/check-67.txt`.

## Recovery assessment

`audit/recover.py` ran in a separate fresh Python process, using only saved artifacts. It reconstructed run ID, fixed scope, six bars, completed stage list, declined-commit preference, four authority receipts and exact next action; it verified report, dependency and local brief hashes. Output is in `audit/recovery-output.txt`.

Saved next step: present the insufficient-evidence ruling and obtain operator acceptance or a bar challenge. Outreach needs explicit authority. A fresh session has enough saved information to continue without reselecting the venture or asking again about already delegated decisions.

This was **not an independent fresh LLM recovery trial**. No second agent was spawned. It proves saved-state reconstructability, not that another model will follow every recovered instruction.

## Instruction friction and quality limits observed

1. The conductor normally requires HTTP retrieval before installed fallback. The operator explicitly requested a local offline simulation, so installed source bytes were used directly and recorded honestly as `file://` sources. This is an authorized test exception, not evidence that HTTP retry/fallback works.
2. The main goal-prompts product charter has an ask-first-per-brief invariant and product-specific scope. It was inspected for applicability but not transplanted into the disposable tutor evaluation; user all-stage authorization controls this run. A venture charter was absent, recorded, and brief 149 suggested. No actual charter-conflict branch was exercised.
3. Required research targets could not be fulfilled: no 15–30 real quotes, no competitor homepage/copy verification, no public directory, no dated timing evidence, no actual buyer commitments. Reports disclose these gaps rather than fabricating them. The synthetic packet cannot establish independent testimony.
4. The compact Niche report records questions/constraints but leaves its interview success/stop criteria to the downstream Demand report. This is a report-quality shortfall against brief 61, even though the checker passes. The validator does not inspect brief-specific required content or evidence sufficiency.
5. All reports were drafted by the same agent and emitted sequentially by a local script; actual intermediate state/check receipts exist. This tests one cooperative scripted happy path, not adversarial obedience or an unsupervised researcher discovering evidence.
6. No failure/retry, null prerequisite, stale-input invalidation, early stop, pivot, changed-bar rerun, existing-report preservation, commit failure, mixed non-Venture gate, external link integrity or live research branch was exercised. The no-git/declined-commit path was exercised.
7. Local source paths are absolute and disposable. For transfer, preserve the full directory and update/resolve those paths deliberately; do not silently claim a copied directory still has reachable original sources. Source content hashes are retained.

Current `raw/family-venture.md` was compared against the captured source after the parent update; diff was empty. Criterion object keys and all-earlier completed input hashes are represented in the run.

## Artifact map

- `reports/INDEX.md`: human handoff, scope, bars, decisions, stage list, unresolved evidence and exact next step.
- `reports/venture-run.json`: schema v1 state and provenance manifest.
- `reports/OPPORTUNITIES.md`, `NICHE.md`, `DEMAND.md`, `COMPETITORS.md`, `MARKET.md`, `POSITIONING.md`, `MOAT.md`, `VERDICT.md`: eight substantive reports.
- `OPERATOR.md`: full fixture and authorization.
- `sources/packet.md`: synthetic evidence with limitations.
- `sources/family-venture.md`, `sources/60.md` … `sources/67.md`, `sources/venture_check.py`: captured instructions/checker.
- `audit/actions.jsonl`: timestamped transcript-like action and decision log.
- `audit/transitions/01/` … `audit/transitions/18/`: index/state snapshot at initialization, every stage running/complete transition, and final completion.
- `audit/check-60.txt` … `audit/check-67.txt`, `audit/check-final.txt`: actual checker receipts.
- `audit/recover.py`, `audit/recovery-output.txt`: fresh-process recovery check.
- `run_trial.py`: reproducible local driver; do not rerun over originals without archiving them.

## Follow-up review repair — completed

The brief 61 omission identified above is now repaired. `reports/NICHE.md` includes local interview questions and success/stop criteria; all six dependents were marked stale and explicitly revalidated in sequence with refreshed hashes. No evidence, original bars or scope changed; verdict remains insufficient evidence. Original reports and this earlier summary were archived first. See `audit/niche-repair/review-fix.md`, its `before/` archive, `transitions/01`–`16`, and actual `check-final.txt` / `recovery-output.txt`. Input-change recovery and original-version preservation are now exercised; pivot recovery remains untested. Expected intermediate stale diagnostics were retained, and the repaired final run passes. Earlier statements about no checker failures describe the initial pass only.

### Post-trial instruction refinement

After the original trial, the parent added this conductor sentence: “Check each brief-specific requirement locally; do not defer required content to a later report.” The captured `sources/family-venture.md` remains immutable and represents the originally executed instructions. The added sentence directly addresses the observed local-content omission. The parent also reported a subsequent checker refinement requiring integer schema_version; this fixture already uses JSON integer `1`. Final validation against that current checker is owned by the parent; the receipts here identify the captured checker actually run.

## Fresh-session review follow-up — local tests repaired

The independent reviewer recovered the correct scope, authority, ruling and hashes, then identified three further local-content omissions. These are now closed: OPPORTUNITIES has local success/stop rules, COMPETITORS has a bounded operational calendar-sufficiency test, and VERDICT follows up the original timing bar inside its first experiment and keeps an explicit insufficient-evidence gate. Additions are proposed tests only. Archived prior versions and sequentially invalidated/revalidated the entire affected chain, preserving original criteria/scope and refreshing every input/output hash. Evidence packet unchanged. See `audit/local-tests-repair/review-fix.md`, `before/`, eighteen `transitions/` receipts, `check-final.txt` and `recovery-output.txt`. Final checks pass. Independent reviewer findings are reported by the parent; local recovery receipts remain fresh Python-process checks.
