---
name: goal-localization-readiness
description: "Hardcoded strings, locale-blind number and date formatting, and layouts that break in translation — every gap between you and a non-default-locale user. Goal Prompt 68 · Trust — inspects the current repo and writes I18N.md at the repo root."
---

# Goal: Localization Readiness

You are working inside this repo. Mission: find everything standing between this product and a user who does not read your default locale — strings welded into code, formatting that assumes one country, and layouts that shatter when the text changes length or direction.

Read-only pass. Run the app in another locale if you can. Your only write is the report file.

## Phase 1 — Find the seams
- Is there an i18n framework at all (message catalogs, string ids, a `t()` call), or is English the source of truth in JSX and templates?
- Where do locale, currency, and timezone come from — the user, the browser, or a hardcoded default?
- Count the surfaces: UI strings, emails, PDFs, push/SMS, error messages, seed data.

## Phase 2 — Audit through 8 lenses
Cite file and line for every finding.
1. **Hardcoded strings** — user-facing text sitting in code instead of a catalog; the ones a translator will never see
2. **Concatenation** — sentences built by gluing fragments and variables; word order that only works in English
3. **Plurals & gender** — "1 item(s)", hand-rolled `n === 1` branches, no plural-category support
4. **Number & currency** — `toFixed`, manual `$` prefixes, thousands separators assumed; money rendered without its locale
5. **Dates & time** — `MM/DD/YYYY`, hardcoded month names, UTC shown raw, relative time in English only
6. **Layout elasticity** — fixed widths and truncation that assume short text; German and Finnish run 30–40% longer
7. **Direction** — any RTL support (`dir`, logical CSS properties), or is `left`/`right` baked into every margin
8. **Sorting & search** — locale-aware collation and case-folding, or byte-order sorts that mis-order accented names

## Phase 3 — Curate
- Separate structural gaps (no framework, no plural support) from leaks (one untranslated string).
- Rank by reach: what every non-default-locale user hits first vs a corner nobody visits.
- Pick one screen and localize it end to end on paper — the exercise surfaces the systemic blockers.

## Phase 4 — Report
Create `I18N.md` at repo root:
1. **Readiness verdict** — framework present? source of truth for locale? the one-line honest state
2. **Findings** — each: Name · Lens · Location (path:line) · Who hits it · Fix sketch · Effort S/M/L
3. **One screen, localized** — the walkthrough and every blocker it exposed
4. **Sequence** — the order that unlocks the most locales for the least work

Start the report with today's date. If `I18N.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- A finding cites code; "probably not translated" is a task, not a finding
- Judge by what a real locale would break, not by string count
- No user-facing strings in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which locales and fixes to prioritize
