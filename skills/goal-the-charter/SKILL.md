---
name: goal-the-charter
description: "Excavates what this product is meant to be — from README promises, docs, and the commit record — and drafts the one-page contract every future session starts from. Audit brief 149 · Mission — runs a four-phase audit of the current repo and writes CHARTER.md at the repo root."
---

# Goal: The Charter

You are working inside this repo. Mission: recover this product's intent from the evidence and write it down — `CHARTER.md`, one page stating the problem, the user, the job, the non-goals, and what done means right now — so every future session, human or agent, starts from the same contract instead of from the memory of an old chat.

Like 142's spec, the report *is* the artifact: your only write is the charter file. (142 is the big sibling for repos on the goal-prompts template harness; this brief needs no harness.)

## Phase 1 — Excavate the intent
- Read what the repo claims: README and any marketing or docs copy (the promises), package metadata descriptions, CLAUDE.md / AGENTS.md (what agents are currently told), any spec, roadmap, or TODO files.
- Read what the repo did: skim the commit log's arc — what was built first, what recently, what was started and quietly abandoned.
- Collect every contradiction between claim and code, and every question only the operator can answer. Ask those now — invented answers poison a contract.

## Phase 2 — Draft through 7 lenses
1. **Problem** — the pain this exists to remove, in one sentence its user would recognize
2. **User** — the one primary user; a charter with three users has none
3. **The job** — the single job the product does; if the evidence shows two products, the operator picks
4. **Non-goals** — what this will not do or become; the load-bearing section — every abandoned tangent in the history is a candidate, and scope creep dies here, in writing
5. **Invariants** — what must stay true through any change: privacy stance, zero-dependency, offline-first, tone, pricing posture
6. **Now / Next / Not-now** — the current milestone as five or fewer outcomes, the next one, and the parked list
7. **Done looks like** — for each Now outcome, one observable check a stranger could run or see

## Phase 3 — Reconcile and tighten
- Contradictions table: claim · where stated · what the code and history show · proposed ruling. The operator rules; the charter records only what survived evidence or an explicit answer.
- Cut to one page. A charter nobody re-reads is chat context with a filename.
- Propose the wiring that makes it durable: one line in the agent entry file (CLAUDE.md / AGENTS.md) — read `CHARTER.md` before changing product behavior — and a cadence for 150 · Drift Audit to re-check it.

## Phase 4 — Report
Write `CHARTER.md` at repo root: **Problem**, **User**, **The job**, **Non-goals**, **Invariants**, **Now / Next / Not-now**, **Done looks like** — then **Open questions** (what only the operator can settle) and **Contradictions found** (the table, with proposed rulings).

Date the header. If `CHARTER.md` already exists from a previous run, this is an amendment, not a rewrite: read it first, lead with what changed and why, and never silently drop a ratified non-goal — strike it with a dated note, so the history of intent survives.

## Rules
- Answers you don't have come from the operator, never from imagination
- Every charter line traces to evidence or to an operator answer given in this run
- One page. Past that, cut the charter, not the reader's patience
- A `reports/` directory at the repo root changes nothing here: `CHARTER.md` always lives at the root, where every future session can meet it
- Report only — end by asking the operator to ratify the charter, settle the open questions, and approve the entry-file pointer
