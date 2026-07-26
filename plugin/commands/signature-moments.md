---
description: "The moments users remember and retell — the first win, the share-worthy output, the one interaction worth a demo — placed with restraint, never confetti on command."
---

# Goal: Signature Moments Audit

You are working inside this repo. Mission: find the moments this product could be remembered by — and audit whether they're crafted or squandered. People judge an experience by its peak and its ending, then retell it to others. Great products place their best craft precisely there; this brief finds where "there" is. It is the opposite of gimmickry: one earned moment beats ten animations.

Read-only pass. Read the flows, outputs, and celebratory code paths, and run the journeys end to end; your only write is the report file.

## Phase 1 — Map the journeys
- Trace the 2–3 core journeys to their emotional beats: where does the user first get real value? Where does each journey end? What does the product produce that a user might show someone?
- Find any existing celebration, personality, or flourish in code — and note what triggers it and how often it fires.
- Note the surfaces users stare at longest; screen-hours are where craft is actually seen.

## Phase 2 — Audit through 6 lenses
Cite the journey, moment, and file for every finding.
1. **The first win is staged** — the moment the product first proves its worth lands visibly and is acknowledged in proportion; the win that scrolls past silently, indistinguishable from a loading state
2. **Peaks get the craft** — the best-made screen is the one at each journey's emotional high point; polish budgeted to a marketing page while the moment of value looks default
3. **Endings, not dead stops** — each journey closes with the result, its meaning, and a natural next step; the flow that ends on a bare form-submitted page
4. **Output worth showing** — what the product produces (report, artifact, page, export) is composed well enough to screenshot into a group chat unedited; the artifact is the product's ambassador to people who've never opened it
5. **Personality in its place** — voice and wit live in low-stakes moments (empty states, loading, success) and never in errors, billing, deletion, or anything blocking work
6. **Restraint** — celebration scales down with repetition and honors the user's achievement, not the product's feature; confetti on the 400th save, streak-shame, and self-congratulating toasts all read as needy

## Phase 3 — Curate
- Rank by retelling odds: the moment most likely to be described to a colleague outranks everything.
- Separate "unstaged peak" (value lands silently), "squandered ending", "unshareable output", and "misplaced flourish".
- Name the one interaction that could become this product's signature — the thing someone demos unprompted. If nothing qualifies, name the closest candidate and the gap.

## Phase 4 — Report
Create `SIGNATURE.md` at repo root:
1. **Moment findings** — each: lens · journey · file · what happens now · the crafted version
2. **The signature candidate** — the one moment to over-invest in, and why this one
3. **Output audit** — each shareable artifact: current state · what would make it show-worthy
4. **Restraint list** — every flourish to remove or decay with repetition

Start the report with today's date. If `SIGNATURE.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every recommendation is anchored to an observed moment in a real journey — no generic "add delight" advice
- Any proposed flourish states its decay rule: what happens on the tenth time
- No user-facing journeys in this repo (pure library, infra)? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which moment to make the signature first
