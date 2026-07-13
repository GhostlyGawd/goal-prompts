---
name: goal-license-compliance
description: "Every dependency's license, the ones incompatible with how you ship, the attribution you owe, and the copyleft reaching into your own source. Goal Prompt 69 · Trust — inspects the current repo and writes LICENSES.md at the repo root."
---

# Goal: License & Compliance

You are working inside this repo. Mission: know exactly what you are allowed to do with the code you ship — your dependencies' licenses, the ones incompatible with how you distribute, the attribution you owe, and any copyleft reaching into your source.

Read-only pass. Your only write is the report file.

## Phase 1 — Establish the ground truth
- What is *this* project's license, and how does it actually ship — SaaS, distributed binary, npm package, static site, container?
- Enumerate dependencies (direct and transitive) with their declared licenses; note anything unlicensed or custom.
- Include the non-code too: fonts, icons, images, sample data, vendored snippets.

## Phase 2 — Audit through 7 lenses
1. **Compatibility** — each dependency's license against how you ship; the combination that violates a term (GPL in a proprietary binary, AGPL behind a network service)
2. **Copyleft reach** — strong copyleft (GPL/AGPL/LGPL) in the tree: does linkage or distribution trigger obligations you are not meeting
3. **Attribution owed** — MIT/BSD/Apache require notices; is there a NOTICE or third-party-licenses file, and is it complete and current
4. **Unknown & custom** — packages with no SPDX license, "UNLICENSED", or bespoke terms nobody has read
5. **Assets & fonts** — bundled fonts, icon sets, images, and copied snippets; their licenses are the ones teams forget
6. **Your own license** — present, correct for your intent, copyright line not a placeholder; LICENSE matches package metadata
7. **Provenance** — vendored or copy-pasted code with no origin recorded; generated blocks with unclear terms

## Phase 3 — Curate
- Separate genuine risk (a license that forbids how you ship) from hygiene (a missing NOTICE line).
- For each real conflict: the obligation, the trigger, and the cleanest exit (replace, isolate, relicense, comply).
- Rank by exposure: what ships to whom.

## Phase 4 — Report
Create `LICENSES.md` at repo root:
1. **Verdict** — clear to ship as-is? the single biggest legal risk in one line
2. **Inventory** — dependency · license · direct/transitive · verdict against your distribution
3. **Conflicts** — each: what · why it triggers · obligation · remedy · effort
4. **Attribution gap** — what a compliant NOTICE file must add
5. **This project** — license correctness and any fix

Start the report with today's date. If `LICENSES.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Report the terms and the conflict; flag anything genuinely unclear for a human lawyer rather than guessing
- Judge against how this project actually ships, not licenses in the abstract
- No dependencies or bundled third-party code in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which conflicts to resolve first
