---
id: "15"
title: Design System Consolidation
family: Team
question: can others build on it?
output: DESIGN-SYSTEM.md
tagline: Census the drifted colors, spacing, and duplicate components; propose the token set and migration order to unify them.
---
# Goal: Design System Consolidation

You are working inside this repo. Mission: census the visual drift — every near-duplicate color, arbitrary spacing value, and re-implemented component — and propose the token system and migration order that unifies them.

Read-only pass. Your only write is the report file.

## Phase 1 — Take the census
Count, don't estimate. Grep the styles and components:
- Distinct color values (how many near-identical grays and brand shades?)
- Distinct font sizes, weights, and line heights
- Distinct spacing values, radii, shadows, z-indexes
- Component duplicates: how many button/input/modal/card implementations exist?

## Phase 2 — Audit through 6 lenses
1. **Color sprawl** — cluster near-duplicates; name the intended color each cluster wants to be
2. **Spacing drift** — arbitrary values vs an implied scale; propose the scale the code is already reaching for
3. **Type chaos** — sizes/weights outside any scale; heading styles re-declared per page
4. **Component duplicates** — for each cluster: which implementation wins and why
5. **System bypasses** — inline styles and one-off overrides defeating existing tokens/components
6. **State inconsistency** — hover, focus, disabled, error styled differently across components

## Phase 3 — Curate
- Every consolidation names keep / merge / kill per variant, with usage counts
- Order migration by risk: tokens first (mechanical), shared components second, page cleanups last

## Phase 4 — Report
Create `DESIGN-SYSTEM.md` at repo root:
1. **Census numbers** — the before: counts per category
2. **Proposed tokens** — colors, spacing scale, type scale, radii/shadows — derived from what the code already wants
3. **Component consolidation list** — keep/merge/kill with usage counts and winning implementation
4. **Migration order** — sequenced lowest-risk first, each step shippable
5. **Projected after-numbers** — the census once complete

Start the report with today's date. If `DESIGN-SYSTEM.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Derive the system from the code's existing center of gravity — don't import a foreign aesthetic
- Mechanical, reviewable migrations beat big-bang rewrites
- No design system or shared UI components in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which migration step to take
