# CHARTER.md — goal-prompts

**Status: DRAFT** · 2026-07-12 · produced by 149 · The Charter's own method, unattended
rule applied: this is the question sheet plus what the evidence supports — no invented
answers. The four operator rulings at the bottom are open; nothing here is ratified
until the operator answers, and then this header changes and the rulings are folded in.

## Problem
Builders using coding agents lose the plot: intent lives in dead chat threads, agents
optimize generic best practice instead of *this repo's* goals, scope drifts, and "did it
actually get better?" has no evidence. (DEMAND.md: 12 dated sufferer quotes; the drift
pain is also this product's own origin story.)

## User
The burned solo builder / OSS maintainer running a coding agent on a repo they care
about (POSITIONING.md beachhead). The DevEx/platform lead is the later *buyer*, not the
first felt user (VERDICT.md keeps "burned dev → their DevEx lead").

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

## Now (the validation frontier — ROADMAP 2026-07-11; construction is not the frontier)
1. **Prove the loop beats "just re-run it"** on a real external repo — report → Studio →
   47 · Fixer → FIXLOG as one motion. Done looks like: a published examples/ entry with
   the reports, the commits, and a before/after.
2. **Measurement spine** — raw-fetch counting live, so validation gates return a
   readable signal. Done looks like: weekly numbers a human actually reads.
3. **WTP signal** — /teams surface is live; count inbound intent. Done looks like:
   inbound "what does it cost / set this up" emails tallied against the tripwires.
4. **Distribution swing** — Show HN + awesome-list PR, star/fetch response measured.
5. *Pending ruling Q1* — charter-as-input wired across conductors, the copy path, and
   the Fixer.

## Next
Receipts-to-be-featured bar (*pending Q3*) · cadence packaging: one paste installs the
weekly Action (*after Q1*) · felt-value signal in Studio (*pending Q4*).

## Not-now
Second-stack template (queue #4) · catalog monetization plumbing (queue #6) · hosted
memory of any kind · new families beyond need.

## Done looks like (for the pivot's hope, before building against it)
3–5 real inbound intents on /teams · one external maintainer keeps the cadence
unprompted after the loop demo · a real repo shows 4+ consecutive weekly re-runs with
trend arrows moving the right way.

## Open questions — the operator's rulings
- **Q1 · Loop memory** — what accretes per-repo so the loop beats a fresh re-run:
  (a) charter + audit memory as the catalog-wide input contract · (b) reports-only,
  as today · (c) a dedicated state layer.
- **Q2 · First felt user (next 90 days)** — (a) burned solo builder · (b) DevEx lead ·
  (c) agents-as-users.
- **Q3 · Proof bar** — (a) receipts required to be featured · (b) receipts for every
  playbook · (c) dogfood only.
- **Q4 · Value signal** — (a) anonymous Studio thumbs + ten sufferer interviews ·
  (b) thumbs only · (c) interviews only · (d) neither yet.

## Contradictions found
- ADR-9 ("Weekly Vitals on shipped products, not catalog traffic, is the number that
  matters") vs. today's ask to center the catalog user's felt value → resolved by the
  VERDICT's refinement: the loop is the product and the catalog is its funnel; felt
  value in the loop and switching-cost moat are the same requirement. Operator confirms
  via Q1/Q2.
- README sells "works out of the box" while nothing enforces *outcome* quality on
  playbooks (only brief *format* is machine-enforced) → operator rules via Q3.
