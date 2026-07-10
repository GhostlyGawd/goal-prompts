# RETROS — what past programs taught the engine

Append-only. Each entry is a program that ran through the engine, what
happened, and the rules it left behind. Skills consult this the same way
they consult anti-slop.md: these are enforced lessons, not war stories.

## 2026-07 — Auditorium (rejected at Phase 6)

**What happened.** A full rebrand program: name, mark, palette, type, art
direction from an operator mood board, applied across every surface. Every
gate was green — contrast matrix, brand lint, QA matrix, contact sheets —
and every gate *artifact* was approved by the operator. When the finished
product deployed to a live preview and the operator explored it as a user,
they rejected the entire direction. The branch was stripped back to
engine-only; the system survives as
`library/proposals/auditorium.brand.json`.

**Lessons (enforced):**

1. **Put the LIVE product in front of the operator at the earliest possible
   gate.** Approving a specimen, a strategy artifact, or a mockup is not
   approving the product. A deployed preview of the real thing is the only
   artifact that predicts the operator's final reaction. If a direction can
   be applied to one real page and deployed cheaply, do that *before*
   building the rest.
2. **Operator taste overrides any green gate.** The gates are floors
   (contrast, health, consistency), not judges of direction. "All checks
   passed" is necessary, never sufficient. Do not argue a rejection with
   gate evidence.
3. **Cheap rollback is a feature — keep paying for it.** The strip-back was
   possible in hours because brand.json was the single source, the site
   regenerated from it, and application commits were separable from engine
   commits. Preserve that separability in every program: engine changes and
   brand-application changes in distinct commits, proposals kept as files
   (`library/proposals/`), history never squashed across that line.
4. **Gate artifacts must be the thing, not a description of the thing.**
   Mid-program, text-table presentations failed twice before visual,
   self-contained artifacts landed (see techniques/presentation-protocol.md,
   which this program wrote). Presentation debt compounds into misalignment.
5. **More operator reference material up front, smaller reversible steps.**
   The direction stabilized only after the operator supplied a 5-image mood
   board. Ask for boards/references at kickoff, and sequence application so
   any single step can be reverted without unwinding the program.
