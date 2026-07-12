# CHARTER.md — goal-prompts

**Status: DRAFT — partially ratified** · 2026-07-12 · produced by 149 · The Charter's
own method. Amendment, same day: the operator answered the interview — Q1 and Q2 are
ratified and folded in below; Q3 and Q4 were superseded by two operator findings (F1,
F2 under *Operator interview findings*) that reframe them, and the two refined
questions now sit in *Open questions*. No answer was invented at any step.

## Problem
Builders using coding agents lose the plot: intent lives in dead chat threads, agents
optimize generic best practice instead of *this repo's* goals, scope drifts, and "did it
actually get better?" has no evidence. (DEMAND.md: 12 dated sufferer quotes; the drift
pain is also this product's own origin story.)

## User
The burned solo builder / OSS maintainer running a coding agent on a repo they care
about (POSITIONING.md beachhead). The DevEx/platform lead is the later *buyer*, not the
first felt user (VERDICT.md keeps "burned dev → their DevEx lead").
**Ratified (Q2, 2026-07-12):** the next 90 days optimize the solo builder's felt loop —
aligned, visible progress, comes back. /teams stays live as a passive WTP test only.

## The job
Turn "my AI audits and improves my repo" from a prompt-engineering project into a
copy-paste **loop** that is: aligned (knows the repo's intent), acted (ends in verified
commits), evidenced (receipts and trends), and compounding (each run more personal than
the last). The catalog is how you enter the loop; the loop is the product (VERDICT
2026-07-10; ADR-9 as refined by the pivot).

## Non-goals
- No SaaS backend, no accounts, no hosted state: code, reports, and setup never leave
  the user's machine. Anonymous countable events only.
- No orchestrator/framework (ADR-7) — the loop runs on whatever agent harness the user
  already has.
- Not a general prompt marketplace: one linted grammar, one published bar (/quality).
- No catalog monetization now: sponsored/collab plumbing stays shelved until adoption
  signals (ADR-9; FABLE_BUILD_QUEUE #6). The catalog stays free and forkable — it is
  the attention asset, not the revenue surface.

## Invariants
- Ask-first gate on every brief; audits read-only; evidence or a null report, never
  invented findings (linter-enforced, tests pin the linter).
- One report file per brief, ≤4,000 chars per body, dated re-runs that diff against
  the last run.
- stdlib-only build; the ledger design direction (ADR-12, ADR-13).
- Decisions land append-only in DECISIONS.md.
- **Ratified (Q1, 2026-07-12):** `CHARTER.md` is the catalog-wide input contract —
  conductors, the site's copy path, and the Fixer read it, and its non-goals bound
  every recommendation. The repo's accreting audit memory (charter + dated reports +
  FIXLOG + debrief history) is the loop's moat mechanism.
- **The loop lives in the conversation (F1/F2):** a user must never need to understand
  the catalog's architecture to get value — the next step is offered in-session, and
  no browser surface is ever a required hinge.

## Now (the validation frontier — ROADMAP 2026-07-11; construction is not the frontier)
1. **Prove the loop beats "just re-run it"** on a real external repo — report → Studio →
   47 · Fixer → FIXLOG as one motion. Done looks like: a published examples/ entry with
   the reports, the commits, and a before/after.
2. **Measurement spine** — raw-fetch counting live, so validation gates return a
   readable signal. Done looks like: weekly numbers a human actually reads.
3. **WTP signal** — /teams surface is live; count inbound intent. Done looks like:
   inbound "what does it cost / set this up" emails tallied against the tripwires.
4. **Distribution swing** — Show HN + awesome-list PR, star/fetch response measured.
5. **Charter-as-input** (ratified Q1) — wired across conductors, the copy path, and
   the Fixer; the next build.
6. **Collapse the loop into the conversation** (from F1/F2) — every solution playbook
   ends with the agent presenting curated findings and asking which to fix, in the
   same session; Studio repositioned as optional triage for big report stacks, never
   the required path. Done looks like: paste once → audits → "which do I fix?" →
   verified commits + FIXLOG, zero browser.

## Next
Receipts-to-be-featured bar (*open Q3′ — after the loop is legible*) · cadence
packaging: one paste installs the weekly Action · a quantitative felt-value signal,
placed only where the ICP actually looks (*open Q4′*).

## Not-now
Second-stack template (queue #4) · catalog monetization plumbing (queue #6) · hosted
memory of any kind · new families beyond need.

## Done looks like (for the pivot's hope, before building against it)
3–5 real inbound intents on /teams · one external maintainer keeps the cadence
unprompted after the loop demo · a real repo shows 4+ consecutive weekly re-runs with
trend arrows moving the right way.

## Operator interview findings (2026-07-12 — user #1, the ICP)
- **F1 · The loop is illegible to its own ICP.** Verbatim: "I have no idea what [the
  Fixer] even does — that's the problem, I don't understand how this all works." The
  product may never require understanding its architecture; legibility of the next
  step is a product requirement, not documentation's job.
- **F2 · Studio is friction, not value, for the agent-native ICP.** Verbatim: "I never
  use Studio… an extra annoying step that I can't see the value in." Consequence:
  Studio must be optional, and any telemetry placed there would measure a surface the
  ICP skips — the numerator would still be invisible (BLINDSPOTS).

## Open questions — the operator's rulings
- **Q1 · Loop memory** — **RATIFIED (a)**: charter + audit memory as the catalog-wide
  input contract.
- **Q2 · First felt user** — **RATIFIED (a)**: the burned solo builder.
- **Q3′ · Loop shape & proof** — make the in-conversation ending (Now #6) the default
  for every solution playbook, then apply receipts-to-be-featured (a real-repo run
  with published FIXLOG + before/after) as the bar? Or receipts first?
- **Q4′ · Value signal** — interviews-first is confirmed by this very exchange. Is
  there any place an agent-native user would actually see a lightweight quantitative
  signal (within the privacy invariant), or do we hold with fetches + FIXLOGs-in-the-
  wild + interviews?

## Contradictions found
- ADR-9 ("Weekly Vitals on shipped products, not catalog traffic, is the number that
  matters") vs. today's ask to center the catalog user's felt value → resolved by the
  VERDICT's refinement: the loop is the product and the catalog is its funnel; felt
  value in the loop and switching-cost moat are the same requirement. Operator confirms
  via Q1/Q2.
- README sells "works out of the box" while nothing enforces *outcome* quality on
  playbooks (only brief *format* is machine-enforced) → operator rules via Q3′.
- The site and README center Studio as the loop's hinge ("Act on the reports — Report
  Studio") while the ICP finds it skippable friction (F2) — and the direct path (an
  "Ends in commits" playbook chaining straight into 47) already exists but is buried.
  → resolved by Now #6: the conversation is the loop; Studio is optional triage.
