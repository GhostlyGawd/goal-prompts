---
id: "78"
title: Retention & Lifecycle Audit
family: Growth
question: does it grow?
output: RETENTION.md
tagline: The return trip: the saved state, resurfaced value, and well-timed nudges that earn a second visit — and the churn cliffs that quietly lose it.
---
# Goal: Retention & Lifecycle Audit

You are working inside this repo. Mission: find why a user would come back — and every place this product lets them drift away. Acquisition fills the top; retention is where the value, and the revenue, actually compounds.

Read-only pass. Trace the code, data model, and any lifecycle messaging; your only write is the report file.

## Phase 1 — Map the return trip
- What is the natural use rhythm — daily, weekly, occasional? Judge it from the job the product does, not from wishful notifications.
- Trace what persists between visits: saved work, history, progress, settings — the reasons a return is worth more than a fresh start.
- Find the lifecycle machinery, if any: welcome flows, digests, re-engagement emails, notifications, streaks, and where they're triggered in code.

## Phase 2 — Audit through 8 lenses
Cite the feature, table, or trigger for every finding.
1. **Reason to return** — a concrete pull for the second and tenth visit, or a tool that's used once and forgotten
2. **Saved state as a hook** — does past work resurface to draw the user back, or is it buried where they'll never revisit it
3. **The empty return** — what a coming-back user sees: their context restored, or a cold start that erases their momentum
4. **Well-timed nudges** — lifecycle messages tied to real user state and value, versus spray-and-pray blasts or silence
5. **Habit and progression** — streaks, milestones, unlocks, or accruing value that makes staying rational — without dark-pattern coercion
6. **Churn cliffs** — the moments users quietly leave: a failed run, a hit limit, an unanswered question, a lapsed subscription with no save
7. **Win-back** — is there any path to re-earn a dormant or cancelled user, or is a leave permanent by default
8. **Is return even measured** — could you read a retention curve or a cohort today, or is churn invisible until revenue drops

## Phase 3 — Curate
- Rank by compounding value: a fix early in the lifecycle pays on every future visit.
- Every finding names the moment a user drifts and the specific pull that would bring them back.
- Prefer resurfacing value the user already created over inventing new reasons to notify them.

## Phase 4 — Report
Create `RETENTION.md` at repo root:
1. **Return-trip map** — visit rhythm · what persists · the pull back · the biggest leak
2. **Findings** — each: lens · location · why users drift here · the fix · effort
3. **The one hook to build** — the single highest-leverage reason-to-return, argued
4. **Instrumentation gaps** — the events and cohorts needed to see retention at all

## Rules
- Retain by delivering value again, never by holding the exit hostage
- Every nudge must be something the user would thank you for receiving
- Count from real user rhythm, not from how often you wish they'd return
- Report only — end by asking which fixes to make
