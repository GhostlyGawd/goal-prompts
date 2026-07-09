# FABLE_BUILD_QUEUE — remaining Fable-only work, prioritized

2026-07-09 · Each item states why Opus cannot safely do it. Everything not
on this list is either done (HARNESS_PLAN §4) or Opus-buildable inside the
rails. Work the list top-down; re-rank only with a DECISIONS.md entry.

## 1. Supervise the first full traversal (decide → build → ship)

Run alongside Opus through the first real Founder Funnel + Build Loop and
review every gate crossing: the verdict's bars, the spec's ACs, the first
BUILDLOG session, the first SHIP-GATE ruling.
**Why not Opus:** the first traversal is the eval of the harness itself —
the judge of whether the gates measure the right things cannot be the agent
being gated. Expect to find lint rules that are too loose (Opus satisfied
the letter, missed the intent) and convert each finding into item 3.

## 2. Author eval rubrics for any judgment-shaped product

If the chosen product's output quality needs rubric scoring (not just
equals/contains/regex), write the rubric and its golden cases, and extend
`template/evals/run.py` if a new expectation type is needed.
**Why not Opus:** the rubric *is* the verification layer for that product
(prior decision: Opus never authors the verification layer). A rubric
written by the agent it judges converges on whatever the agent already does.

## 3. Ratchet observed failures into lint rules (standing)

After every Opus session that produces a new failure mode the hooks missed,
convert it into a deterministic rule: a new `spec_lint.py` check, a new
harness test, a new hook. The known first candidate: product-test weakening
(ADR-8's named residual) — investigate a mutation-style check for the gate
(`144` does it manually today).
**Why not Opus:** these edits live in the protected harness layer, and the
PreToolUse hook blocks Opus there by design. Also: choosing which failures
are worth a rule is exactly the expensive-to-reverse judgment Fable exists
for.

## 4. Second-stack template, only when a verdict demands it

If a go verdict requires a web-facing or Node product the Python template
can't honestly serve, port the harness layer (same four enforcement
moments, same spec grammar) to the new stack at `template-node/` or kin.
**Why not Opus:** a fresh gate can be subtly gameable (async test runners
that swallow failures, lint that doesn't fail the process). Proving a new
gate can fail — and can't be fooled — is verification-layer authorship.

## 5. Report-grammar bridge for SHIP-GATE and BUILDLOG (nice-to-have)

Teach `js/report-parser.js` (and its test suite) the SHIP-GATE scorecard
and BUILDLOG session shapes so Studio and the Fixer consume Build-family
outputs as first-class findings.
**Why not Opus:** touches a parity-tested parser pair
(`tests/report_parser.test.cjs`) in *this* repo, where the linted grammar
is itself a gate other tools rely on; a wrong generalization silently
degrades the Fixer's input. Low urgency — the current grammar already
parses bold-led findings well enough.

## 6. Catalog monetization build-out — parked, revisit on evidence

The sponsored/collab plumbing exists as previews (playbooks.json). Do
nothing until adoption data (stars ≥ the badge threshold at build.py:1298,
or raw/ fetch counts per docs/usage-metrics.md) says there is an audience.
**Why not Opus:** not a capability question — a sequencing decision (ADR-9)
that should not be reopened by an eager session. Listed so it isn't
re-litigated.
