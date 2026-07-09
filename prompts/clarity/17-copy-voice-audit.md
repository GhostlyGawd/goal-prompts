---
id: "17"
title: Copy & Voice Audit
family: Clarity
question: is it understood?
output: COPY.md
tagline: Extract every user-facing string; hunt jargon, vague CTAs, and unhelpful errors; rewrite the worst ten before/after.
---
# Goal: Copy & Voice Audit

You are working inside this repo. Mission: extract the words users actually see — buttons, errors, empty states, emails — and audit them for clarity, consistency, and helpfulness. Then rewrite the worst offenders.

Read-only pass. Your only write is the report file.

## Phase 1 — Extract the strings
- Pull user-facing text from components, templates, locale files, email templates, and validation messages.
- Note where strings live: centralized, scattered, hardcoded?
- From the strings alone, describe the voice this product currently has — it has one, chosen or not.

## Phase 2 — Audit through 7 lenses
1. **Jargon leaks** — internal or technical terms surfacing in UI ("entity", "payload", table names)
2. **Vague actions** — "Submit", "OK", "Continue" where the button should say what happens ("Save changes", "Send invite")
3. **Unhelpful errors** — messages stating failure without the next step; blame-the-user phrasing
4. **Tone drift** — formal here, jokey there; exclamation inflation
5. **Terminology splits** — one concept, multiple names across screens (project/workspace/board)
6. **Empty states** — screens that describe emptiness instead of inviting the first action
7. **Destructive ambiguity** — delete/cancel confirmations where the safe choice isn't obvious

## Phase 3 — Curate
- Pick the 10 worst strings by user impact (frequency × confusion)
- Build the glossary: one name per concept, chosen from what's already most used

## Phase 4 — Report
Create `COPY.md` at repo root:
1. **Voice snapshot** — the tone the strings imply today, in three sentences
2. **Worst 10, rewritten** — each: location · before · after · why
3. **Terminology glossary** — concept → the one name, plus the names to retire
4. **Voice rules** — 5 bullets future copy must follow
5. **String hygiene** — centralization fixes if strings are scattered

Start the report with today's date. If `COPY.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every rewrite must be usable verbatim — real copy, not direction
- Buttons say what they do; errors say what to do next
- No user-facing copy in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which rewrites to apply
