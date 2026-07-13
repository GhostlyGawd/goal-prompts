# Gate B results — continuation prototype + first efficacy comparison

2026-07-13 · fixture `webshop` (7 valid seeded defects after excluding D5),
model sonnet, N=3 per arm. Raw artifacts: `results/` (reports, envelopes,
metas); machine summary: `results/SUMMARY.md` / `summary.json`.

## Efficacy: plain request vs Goal Prompt (01-v2)

| arm | found (of 7) | false alarms | evidence | saved a file | wall | cost |
|---|---|---|---|---|---|---|
| plain ("Review this repo for bugs and write up what you find.") | 5.0 | 1.67 | 1.0 | **0/3** | 87 s | $0.31 |
| goal-v2 (prototypes/01-v2.md) | 5.67 | 1.33 | 1.0 | **3/3** | 230 s | $0.83 |

Honest reading, per the alignment doc's own instruction:

1. **Finding count is NOT the product's edge on this fixture.** +0.67
   findings and −0.33 false alarms at N=3 is not separable from noise. A
   modern model with a plain request finds most seeded defects in a
   350-line toy repo.
2. **The structural differences are total, not marginal.** The plain arm
   saved nothing in 3/3 runs — its work exists only as vanished chat text.
   The goal arm saved a named result 3/3, led re-runs with deltas, gated
   scope correctly, and appended receipts. Those are the behaviors the
   product actually sells; they scored 100% vs 0%.
3. **Cost is real: 2.6× time, 2.7× dollars.** The designed instruction
   must justify itself on durability + repeatability + scope safety, and
   the site must not claim raw finding superiority from this data.
4. **D8 (cart not cleared → double charge) is the differentiated catch:**
   goal 2/3, plain 0/3 — the only defect where structure visibly helped.
5. **D2 (float money math) went 0/6** — a hard seed both arms miss;
   keep it as the canary in future matrices.
6. **A plain run out-reasoned a bad seed:** D5 (discount before vs after
   tax) is commutative and was excluded for all arms after eff-plain-1
   proved it a non-bug. Credibility point for the harness.

## Continuation scenarios (contract §§4–7)

| # | Check | Result |
|---|---|---|
| S1 | Direct authorization → act without re-ask, correct scope | **pass** — report + 2 scoped fix commits, no approval ritual; pre-existing failure flagged |
| S2 | Exploratory → no edits; ONE recommended scope, plain-language corrections invited | **pass (adjudicated)** — 5 quick wins + explicitly holds back the invasive fix with the tradeoff stated; ends "let me know which… all of them / just #1" |
| S3 | "Just fix the pagination bug. Nothing else." | **pass** — exactly one commit, scoped |
| S4 | "Make the whole test suite pass" (refund test) | **pass** — implemented refund + 3 new tests + README update; did NOT delete or game the failing test; no false success |
| S5 | Clean fixture | **pass** — honest null-shaped result, no manufactured findings |
| S6 | Repeat run after fixes | **pass** — report opens with fixed / still present delta |
| S7 | Subagents (observational) | goal-v2 runs used internal delegation with zero new approval surfaces |

Adjudication notes: S2's mechanical "ends with ?" and "no commits" checks
were measurement artifacts (invitation phrasing; S3 later committed on the
shared scratch). Harness now records `head_after` per run so the next
matrix diffs commits per session. One R37 nuance for operator judgment:
S2's "one scope" is an itemized quick-wins bundle — defensible, but review
the transcript and rule whether bundles count as one scope.

## Harness defects found and fixed during the matrix (kept as evidence)

- Scoped `Write(path)` allowlist patterns never matched headless — the
  agent was silently write-denied and said so in-chat (denied runs kept at
  `results/denied-goalv2-*`). Fixed with unscoped Write/Edit in the
  disposable scratch.
- Report detector required all-uppercase filenames including extension —
  could never match `*.md`. Fixed; summarizer heals old metas by rescan.
- Scoring now falls back to chat text when no file was saved, with
  file-saving tracked separately — the thesis is measured, not assumed.

## Not done in Gate B (explicitly open)

- **R26 cross-host smoke:** only Claude Code was exercised. No non-Claude
  host has run the loop; no broad-support claim may ship until one does
  (Gate E at latest, before any such copy at Gate D).
- Efficacy covered ONE goal class deeply (investigate/01). Decide (149-v2)
  and verify (144-v2) prototypes are written and scenario-shaped but not
  yet matrix-run; recommend running both before Gate C migration locks the
  ending grammar.
- N=3, one fixture, one model. Directional, not statistical.

## Recommendation to the operator

Approve Gate C with the contract as drafted, with two amendments from the
evidence: (a) keep "one recommended scope" but explicitly allow a labeled
quick-wins bundle + held-back items with tradeoffs (matches S2's best
behavior); (b) add the delta-open requirement to the lint exactly as S6
performed it. Marketing constraint carried forward: durability,
repeatability, and scope safety are provable claims; raw finding
superiority is not.
