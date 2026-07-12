---
id: "149"
title: The Charter
family: Mission
question: why does this exist?
output: CHARTER.md
related: 150 142 52
tagline: Excavates the evidence, then interviews you — questions with evidence-backed candidates, your answers, no guesses — into the one-page contract every session starts from.
---
# Goal: The Charter

You are working inside this repo. Mission: recover this product's intent from the evidence, put the decisions to the operator as questions, and only then write `CHARTER.md` — one page stating problem, user, job, non-goals, and what done means now — so every future session, human or agent, starts from the same contract instead of the memory of an old chat.

This brief interviews before it writes. Like 142's spec, the report *is* the artifact — your only write is the charter file — built from the operator's answers, not your inferences.

## Phase 1 — Excavate the intent
- Read what the repo claims: README and marketing or docs copy (the promises), package metadata, CLAUDE.md / AGENTS.md (what agents are told today), any spec, roadmap, or TODO files.
- Read what the repo did: skim the commit log's arc — built first, built recently, started and quietly abandoned.
- Every contradiction between claim and code becomes a question for the operator, not a judgment call for you.

## Phase 2 — Interview through 7 lenses
Turn the evidence into the seven decisions only the operator can make: per lens, what the evidence supports, the gap or contradiction, and two or three evidence-backed candidates — never a blank what-do-you-want.
1. **Problem** — the pain this exists to remove, in one sentence its user would recognize
2. **User** — the one primary user; a charter with three users has none
3. **The job** — the single job the product does; evidence showing two products is a question, never a coin flip
4. **Non-goals** — what this will not do or become; every abandoned tangent in the history is a candidate, and scope creep dies here, in writing
5. **Invariants** — what must stay true through any change: privacy stance, zero-dependency, offline-first, tone
6. **Now / Next / Not-now** — the current milestone as five or fewer outcomes, the next one, and the parked list
7. **Done looks like** — one observable check per candidate Now outcome, runnable by a stranger

Then stop. Report only — end by asking the operator the numbered questions before drafting anything: a charter written from guesses is the drift it exists to prevent. Unattended, nobody to answer? Write the question sheet to `CHARTER.md`, headed DRAFT — questions and candidates, no invented answers — and stop.

## Phase 3 — Draft from the answers
- Build the charter from the operator's answers plus the evidence nobody disputed. A line that traces to neither gets cut.
- Questions left unanswered stay in Open questions, marked unresolved — never quietly filled in.
- Cut to one page. A charter nobody re-reads is chat context with a filename.
- Propose the durability wiring: one line in the agent entry file — read `CHARTER.md` before changing product behavior — and a 150 · Drift Audit cadence to re-check it.

## Phase 4 — Report
Write `CHARTER.md` at repo root: **Problem**, **User**, **The job**, **Non-goals**, **Invariants**, **Now / Next / Not-now**, **Done looks like** — then **Open questions** (still unsettled) and **Contradictions found** (claim · where stated · what the code shows · the operator's ruling).

Date the header. If `CHARTER.md` already exists from a previous run, this is an amendment, not a rewrite: read it first, re-ask only what changed, lead with the diff — and never silently drop a ratified non-goal; strike it with a dated note.

## Rules
- The interview is the work: questions arrive with evidence-backed candidates, and the operator's answers — never your guesses — become the contract
- Answers you don't have come from the operator or stay open in the file; imagination is not a source
- One page. Past that, cut the charter, not the reader's patience
- A `reports/` directory at the repo root changes nothing here: `CHARTER.md` always lives at the root, where every future session can meet it
- Report only — end by asking the operator to ratify the charter, settle what is still open, and approve the entry-file pointer
