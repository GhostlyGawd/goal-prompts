---
name: goal-model-transparency
description: "Diff what the UI says about the AI against what the code does — disclosure strings quoted, dropped confidence traced, retention claims checked against real payloads. Audit brief 119 · AI-Ethics — runs a four-phase audit of the current repo and writes TRANSPARENCY.md at the repo root."
---

# Goal: Model Transparency Audit

You are working inside this repo. Mission: diff the product's story about its AI against its code. Every claim the UI makes — "AI-generated", "we never store your data", an answer delivered with total confidence — is checkable here: find the disclosure strings that ship, the model calls they describe, and the gaps between them.

Read-only pass. Your only write is the report file.

## Phase 1 — Collect both sides of the diff
- Grep the shipped copy: disclosure strings, AI badges, tooltips, empty-state text, claims in templates ("AI", "generated", "assistant", "never trained on").
- Find the model calls: which code paths invoke a model, what the request payload actually contains, what comes back (confidence, citations, model ids), and what of it the UI keeps or drops.
- Map each AI touchpoint to the disclosure a user actually sees there — or to none.

## Phase 2 — Audit through 6 lenses
Label every finding **measured** (both sides cited from code) or **suspected** (one side inferred); an unlabeled finding doesn't ship.
1. **Undisclosed AI** — model output reaching the user with no cue in the rendering component; cite the component and the missing string
2. **Confidence dropped on the floor** — the API returns scores, citations, or caveats the UI discards; file:line where the signal dies
3. **Copy vs payload** — data-use claims ("not stored", "never trained on") diffed against the request the code sends and any retention or vendor training flag you can find
4. **Capability overstatement** — UI copy promising what the prompt or model config can't back: "understands", "always accurate", against temperature, truncation, and absent retrieval
5. **Version silence** — model ids pinned in config while the UI implies one stable "AI"; behavior can change under users with no cue
6. **Recourse reality** — the "talk to a human" or feedback affordance: trace where its handler actually sends things, or whether the button is decorative

## Phase 3 — Curate
- Rank by miscalibrated trust: an undisclosed AI decision outranks a missing model name.
- Write each fix as the artifact itself: the string to add, the field to surface, the claim to correct.
- Keep measured and suspected findings in separate ranks; every suspected one names the check that would confirm it.

## Phase 4 — Report
Create `TRANSPARENCY.md` at repo root:
1. **The honesty diff** — touchpoint · what the user is told (quoted, file:line) · what the code does (file:line) · gap
2. **Findings** — each: measured/suspected · lens · trust risk · the fix, written out
3. **Dropped signals** — the confidence, citations, and ids the backend has and the UI hides
4. **Priority** — the three corrections that most recalibrate user trust

Start the report with today's date. If `TRANSPARENCY.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Quote the string and cite the call — a claim about the product's honesty must itself show its evidence
- Under-disclosure and over-warning are both findings; noise teaches users to ignore the truth
- No model output reaching a user in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which transparency gaps to close first
