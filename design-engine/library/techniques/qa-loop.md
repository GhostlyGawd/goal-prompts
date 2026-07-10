# Technique — the QA loop (no ship without it)

Judgment becomes artifacts and exit codes (the host's ADR-1). A visual
change is NOT done at "the gate is green" — the gate checks logic and
tokens, not design. The loop:

1. `sh scripts/check` — logic, tokens, contrast, tests (exit codes).
2. `node design-engine/tools/shots.cjs --matrix --assert` — every page ×
   theme × {390, 768, 1280}: loads, zero console errors, tokens resolve,
   fonts load, NO horizontal overflow. Exit code.
3. `node design-engine/tools/shots.cjs --matrix` then
   `python3 design-engine/tools/qa_sheet.py` — ONE contact sheet of every
   page/theme/viewport. Review the sheet, not a favorite screenshot:
   - consistency: is any page wearing a different product's chrome?
   - the design-review rubric (health → hierarchy → consistency →
     accessibility → board fidelity → anti-slop → craft) over the sheet
   - mobile column read end-to-end, not glanced
4. Interaction states: exercise the flows that changed (motion_preview.cjs
   with --click, or the host's flow shooter e.g. studio-shot) — static
   loads don't show open/hover/checked states.
5. Findings from 3–4 get fixed or explicitly deferred IN WRITING before
   ship. "Looked at the landing" is not a QA pass.

First run of this loop caught: Studio + Vitals still wearing the previous
design after a site-wide rebrand (only their heads had been updated) —
invisible to single-page review, obvious on the sheet.
