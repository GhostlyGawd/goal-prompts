---
id: "86"
title: Keyboard & Screen-Reader Flow
family: Trust
question: is it safe?
output: A11Y-DEEP.md
related: 08
tagline: Walk the product the way assistive-tech users do — keyboard only, then with a screen reader — and find every place that path breaks.
---
# Goal: Keyboard & Screen-Reader Flow

You are working inside this repo. Mission: go past the automated accessibility checks and walk the real interaction paths — operate everything by keyboard, then trace what a screen reader would announce — and find where a non-mouse, non-sighted user gets stuck.

This is the deep assistive-tech walk. For the broad end-to-end accessibility pass along the core journey, run 08 first.

Read-only pass. Drive the UI, read the components and markup; change nothing. Your only write is the report file.

## Phase 1 — Walk the core flows
- Pick the product's main journeys and operate each using only the keyboard — no mouse at all.
- For the same flows, trace the accessibility tree: what name, role, and state each control exposes.
- Note where you get trapped, lost, or given no feedback.

## Phase 2 — Audit through 7 lenses
Cite the component or screen for every finding.
1. **Keyboard reachability** — every interactive control operable without a mouse; no keyboard traps
2. **Focus order & visibility** — logical tab order, a visible focus ring, focus moved on route and modal changes
3. **Semantic structure** — real landmarks, headings, lists, and buttons instead of div-soup
4. **Name, role, state** — controls that announce what they are and their state (pressed, expanded, selected)
5. **Live regions** — async updates, toasts, and errors announced rather than silent
6. **Forms & errors** — labels tied to inputs; errors announced and associated with the field
7. **Media & motion** — captions and alt text present; `prefers-reduced-motion` honored

## Phase 3 — Curate
- Rank by how completely a finding blocks the task: a keyboard trap on checkout outranks a missing heading.
- Map each to the WCAG criterion it fails, so fixes are auditable.
- Prefer fixes that use native semantics over ARIA patches.

## Phase 4 — Report
Create `A11Y-DEEP.md` at repo root:
1. **Keyboard walk** — each core flow, where it breaks, and the blocking severity
2. **Screen-reader walk** — what is announced vs what should be, per control
3. **Findings** — each: WCAG criterion · location · who it blocks · the fix
4. **Highest-impact fixes** — the handful that unblock the most real AT users

Start the report with today's date. If `A11Y-DEEP.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Test the path, not just the snapshot; automated scans miss the flow
- Native semantics first; ARIA is a patch, not a foundation
- No keyboard-operable UI in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which accessibility fixes to make first
