---
description: "Can a newcomer explain back what this is, who it's for, and how it works after one screen — or does the curse of knowledge leave them guessing?"
---

# Goal: Comprehension Audit

You are working inside this repo. Mission: judge whether a first-time visitor forms a correct mental model of this product — what it is, who it's for, how it works, and why it beats the alternative — from the public surfaces alone. Not "is the copy nice" but "did they actually get it."

Read-only pass. Run the app or read the pages, components, and copy a newcomer meets first; your only write is the report file.

## Phase 1 — Meet it cold
- Find the first surfaces a stranger hits: landing hero, README, docs home, empty app state, the first screen after signup.
- For each, write the mental model it's trying to plant in one sentence: "this is an X that helps Y do Z."
- Record your own honest read after ten seconds on each — then audit the gap between the two.

## Phase 2 — Audit through 8 lenses
Cite the surface and the exact words or element for every finding.
1. **What is this** — is the category named in plain words in the first screenful, or must the reader infer it from features and hope
2. **Who it's for** — is the audience named, or is everyone addressed and no one recognized
3. **How it works** — is the mechanism shown at least once (a diagram, a three-step, a worked example), or asserted as magic
4. **Curse of knowledge** — terms, acronyms, and concepts used before they're defined; insider framing that assumes the reader already knows the space
5. **The one-sentence test** — could a stranger repeat back what this does after one screen; where the sentence would come out wrong
6. **Concrete over abstract** — real examples, numbers, and outputs versus adjectives and category nouns ("powerful", "platform", "solution")
7. **Progressive disclosure** — is depth layered so a skimmer gets the gist and a digger gets the detail, or is it all-or-nothing
8. **Why this, why now** — is the alternative (a rival, a spreadsheet, doing nothing) named and beaten, or is the product described in a vacuum

## Phase 3 — Curate
- Rank misunderstandings by cost: a wrong "what is this" loses the visitor before anything else can help.
- Every finding names the surface, the confusing element, and the wrong belief a newcomer walks away with.
- Separate "never explained" from "explained too late" from "explained in jargon."

## Phase 4 — Report
Create `COMPREHENSION.md` at repo root:
1. **Mental-model gap** — intended one-liner vs the honest ten-second read, per key surface
2. **Findings** — each: lens · location · what a newcomer misunderstands · the fix
3. **First-screen rewrite** — what the hero or opening must say so a stranger gets it in one glance
4. **Explain-it-back script** — the three sentences a newcomer should be able to repeat, and where each is taught today

Start the report with today's date. If `COMPREHENSION.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Speak for someone who has never seen this product or its category
- Comprehension before persuasion: they can't want what they don't understand
- Every finding cites the exact words or element that misleads — no vague "unclear"
- No public surface a newcomer meets in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fixes to make
