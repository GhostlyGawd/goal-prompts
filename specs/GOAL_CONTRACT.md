# GOAL_CONTRACT — shared safety, result, and continuation schema (DRAFT v1)

Status: Gate A draft, **awaiting operator ratification** (see
specs/ALIGNMENT_BUILD.md, Ratification block). Once ratified, every clause
marked [lint] becomes a failing exit code in build.py before any prompt is
migrated (TDD: rule first, red on the old catalog where it must be, then
migration turns it green). Clauses marked [bdd] are verified by scripted
end-to-end runs with kept transcripts.

Derived from PRODUCT_ALIGNMENT.md; supersedes nothing until ratified.

## 1. Classes (internal only — never public vocabulary)

- **investigate** — reads, writes its result file, changes nothing else.
- **decide** — the result file IS the artifact (spec, charter, verdict).
- **act** — may change files within authorized scope (today: 47, 141, 143).
- **verify** — runs checks, records outcomes, changes nothing.

Class lives in front matter (`class:`). [lint: every prompt has a valid class;
class determines which ending grammar applies]

## 2. Universal result contract (all classes)

1. Exactly one named Markdown result per prompt. [lint: exists today — keep]
2. Result location: repo root, or `reports/` when it already exists.
   [lint: body wording matches ratified location decision]
3. Result starts with the date. On re-run with a prior result present, it
   opens with the delta: **fixed / still present / new / regressed**.
   [lint: re-run clause present in body]
4. Evidence rules: conclusions carry their evidence; uncertainty is recorded
   honestly; a null result is legitimate. [lint: evidence + null-result
   clauses present]
5. When `CHARTER.md` exists, its goals/non-goals/invariants bound every
   recommendation. [lint: charter clause present — shipped for conductors in
   0.19.0, extends to prompt bodies]

## 3. The six-step baseline (all classes)

Inspect relevant files → evaluate through the prompt's lenses → keep only
supported conclusions → save the named result → offer continuation in the
same conversation when actionable work exists → verify any changes and record
outcomes. [lint: phase skeleton updated from 4-phase to include the
continuation ending; sections may keep current names]

## 4. Authorization grammar (replaces blanket ask-first)

The ending of every prompt follows this logic, stated in the body:

- If the user's **original request already authorized** the work (an explicit
  "fix/change/implement X"), proceed within that stated scope without a
  redundant approval question. [lint: "already authorized" branch present]
- Otherwise (exploratory or audit request): present **one reasoned
  recommended scope** and wait for ordinary-language authorization before any
  edit. [lint: recommendation + wait branch present]
- Publishing, deploying, sending, merging, or other outward actions always
  require their own explicit authority, regardless of prior scope. [lint:
  outward-action clause present in act-class prompts]
- Exploratory authorization is never inferred into edit authorization. [bdd]

## 5. Recommendation contents (act-capable continuations)

A recommendation states: supporting evidence · causal path to user/product
impact · confidence and why · what files/behavior would change · effort and
why · what is deliberately left alone and that tradeoff · how the work will
be checked. [lint: recommendation field list present in ending grammar]
It is one recommended scope with natural-language corrections welcomed — not
a menu, not buttons. [copy rule + bdd]

## 6. Verification recording (act + verify classes)

Checks record four outcomes distinctly: passed · failed · skipped ·
inconclusive, and distinguish **pre-existing** failures from **introduced**
failures. Never claim success on a broken or untested result. [lint: outcome
vocabulary present; bdd: introduced-vs-pre-existing scenario]
Receipts append to the run record (FIXLOG grammar unchanged).

## 7. Same-conversation continuation

The user never needs a second session, Studio, or the word "Fixer" to act on
findings. The coordinating agent may delegate to subagents internally;
subagents must not surface new approval steps, lose scope, or change the
user-facing contract. [bdd on all four classes; copy rule for site]

## 8. Portability

Bodies describe **capabilities** (inspect files, search, run checks, edit
within scope, use version control when available, delegate when useful) —
never host-proprietary commands or Claude-only syntax. [lint: banned-token
scan over bodies]
Host adapters (plugin, MCP, skills) may map capabilities to native features;
every native path keeps a portable fallback. Advertised integrations must
pass the smoke test: inspect → write result → gate correctly → continue →
verify, on one primary agent and at least one non-Claude host. [bdd
checklist per host, committed]

## 9. Size and style

Bodies stay ≤ 4,000 characters (CHARTER invariant). Plain language;
product-internal taxonomy never appears in user-facing copy. [lint: existing
size gate; copy tests at Gate D]

## 10. Migration rule

No public mixing of contracts: all 152 prompts migrate, or exceptions are
explicitly versioned/deprecated/removed, before the new behavior is presented
as the product. [lint: contract-version front matter; build fails on mixed
versions at release]
