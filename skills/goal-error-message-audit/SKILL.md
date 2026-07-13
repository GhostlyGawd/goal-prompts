---
name: goal-error-message-audit
description: "Every message the product shows when something goes wrong — whether it says what happened, why, and what to do next, or leaves the user stuck. Goal Prompt 103 · Clarity — inspects the current repo and writes ERRORS.md at the repo root."
---

# Goal: Error-Message Audit

You are working inside this repo. Mission: read every message the product shows when something fails, and judge whether it helps the user recover or abandons them — because an error is the moment trust is won or lost.

Read-only pass. Collect the user-facing error strings and where they fire; change nothing but the report file.

## Phase 1 — Collect the errors
- Find the user-facing error messages: validation, failed actions, network errors, permissions, empty vs broken.
- Note where each appears and how often that path is likely hit.
- Distinguish messages users see from internal logs.

## Phase 2 — Audit through 7 lenses
Cite the string and its location for every finding.
1. **Actionability** — does it say what to do next, or just announce failure
2. **Cause clarity** — plain language about what went wrong versus codes, jargon, or raw exceptions
3. **Blame & tone** — messages that scold the user versus ones that own the problem and help
4. **Leakage** — stack traces, internal ids, or sensitive detail shown to end users
5. **Consistency** — the same failure worded differently across the app; inconsistent placement
6. **Recovery path** — a way forward (retry, undo, contact, alternative) versus a dead end
7. **Empty vs error** — distinguishing "nothing here yet" from "something broke"

## Phase 3 — Curate
- Rank by frequency × how stuck the message leaves the user: a common dead-end outranks a rare ugly one.
- Rewrite the worst offenders — same meaning, clear cause, a next step.
- Note the patterns: one generic handler often explains dozens of bad messages.

## Phase 4 — Report
Create `ERRORS.md` at repo root:
1. **Worst offenders** — ranked by frequency × stuckness, each with location
2. **Rewrites** — the current message and a better one, side by side
3. **Leakage** — the messages exposing internals, flagged for immediate fix
4. **Voice guide** — the rules for error copy: cause, next step, own it, no jargon

Start the report with today's date. If `ERRORS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every error names the cause and a next step; failure is not a next step
- Never show a user a stack trace or an internal id
- No user-facing error messages in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which messages to rewrite first
