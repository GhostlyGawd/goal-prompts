---
id: "109"
title: Forms & Validation Audit
family: Growth
question: does it grow?
output: FORMS.md
tagline: Every form in the product — whether it asks the least, validates kindly, and recovers gracefully, or leaks users at the moment they try to give you something.
---
# Goal: Forms & Validation Audit

You are working inside this repo. Mission: judge every form that stands between a user and what they want — signup, checkout, settings, creation — and find where field count, harsh validation, or lost input make people give up.

Read-only pass. Fill out the forms, read their validation code; change nothing but the report file.

## Phase 1 — Fill them out
- Complete the product's important forms, including making mistakes on purpose.
- Note every field, when errors appear, and what happens to your input on failure.
- Count the fields that are required versus the ones that could be optional, deferred, or inferred.

## Phase 2 — Audit through 7 lenses
Cite the form and field for every finding.
1. **Field economy** — every field justified; the ones to cut, defer, or infer
2. **Inline validation** — errors shown at the right moment (on blur or submit, not every keystroke), near the field
3. **Error recovery** — input preserved on failure; clear, specific messages; nothing retyped
4. **Input ergonomics** — right input types, autofill, sensible defaults, formatting help
5. **Progress & length** — long forms broken into steps with progress; save-and-resume where it matters
6. **Accessibility** — labels tied to inputs, focus management, errors announced
7. **Submission feedback** — disabled while submitting, success confirmation, no double-submit

## Phase 3 — Curate
- Rank by drop-off risk: friction on the signup or checkout form outranks a rarely used settings field.
- For each, name the fix — cut a field, fix the validation timing, preserve input.
- The best fix is often a shorter form; look to remove before you look to polish.

## Phase 4 — Report
Create `FORMS.md` at repo root:
1. **Form scores** — each significant form: field count, validation quality, recovery
2. **Findings** — each: form · field · the friction · the fix
3. **Cuts** — the fields to remove, defer, or infer, highest-leverage first
4. **Priority** — the fixes on the highest-traffic forms, ordered by drop-off risk

## Rules
- The shortest form that does the job wins; cut before you polish
- Never make a user retype what an error threw away
- Report only — end by asking which form fixes to make first
