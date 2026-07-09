---
description: "The screens users meet with nothing yet — first run, no results, cleared, deleted, error-empty — and whether each teaches the next step or just shows a blank and a shrug."
---

# Goal: Empty & Zero-Data States Audit

You are working inside this repo. Mission: audit every screen a user meets when there is nothing to show — first run, no results, filtered-to-nothing, cleared, deleted, error-empty — and find the blanks that abandon the user instead of guiding them forward.

Read-only pass. Trigger the empty states in the running app or trace the components' zero-data branches; your only write is the report file.

## Phase 1 — Find the empties
- For each list, table, search, feed, and detail view, find the code path that renders when the data is empty.
- Classify each: first-use (never had data), no-results (search/filter), cleared (all done), error-empty (load failed), permission-empty (nothing you may see).
- Note what each currently renders — content, illustration, action — or whether it renders nothing at all.

## Phase 2 — Audit through 7 lenses
Cite the component and the empty branch for every finding.
1. **Exists at all** — a designed empty state versus a blank region, a bare "No data", or a broken layout
2. **Explains the why** — does it say why it is empty (new here, no matches, all caught up) so the user is not left guessing
3. **Shows the next step** — a clear primary action to fill it (create, import, clear a filter), not a dead end
4. **Right type, right tone** — first-run welcomes and teaches; no-results helps refine; error-empty offers retry — not one generic blank for all
5. **Empty versus broken** — "nothing here yet" never looks like "it failed", and vice versa
6. **Honest & on-brand** — real copy and voice, not lorem or a stock shrug; illustration that earns its weight
7. **Loading-to-empty** — the skeleton resolves to the empty state cleanly, with no flash of "empty" before data arrives

## Phase 3 — Curate
- Rank by traffic × stranding: a first-run or no-results empty on a core surface outranks a rare error-empty.
- Separate "missing" (nothing designed), "unhelpful" (blank message), and "ambiguous" (empty versus broken).
- For each, name the surface, the empty type, and the copy-plus-action it should show.

## Phase 4 — Report
Create `EMPTYSTATES.md` at repo root:
1. **Empty-state inventory** — surface · empty type · what it renders now · verdict
2. **Findings** — each: lens · component · what the user hits · the fix (copy + action)
3. **First-run priorities** — the onboarding empties to fix first, since they shape the first impression
4. **The pattern** — the empty-state template (headline · reason · action · art) this codebase should reuse

Start the report with today's date. If `EMPTYSTATES.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every finding names the component and the empty branch that renders it
- An empty state is a teaching moment, not an error; it should always offer a next step
- No UI with empty or zero-data states in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which empty states to fix first
