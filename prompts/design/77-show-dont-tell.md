---
id: "77"
title: Show, Don't Tell
family: Design
question: is it beautiful?
output: SHOWCASE.md
example: /SHOWCASE.md
tagline: Are the benefits and the how-it-works shown — product shots, demos, diagrams, before-and-afters — or buried in paragraphs a visitor has to take on faith?
---
# Goal: Show, Don't Tell

You are working inside this repo. Mission: judge whether this product shows its value and its mechanics — through screenshots, demos, diagrams, annotated examples, before-and-afters — or only describes them in prose a visitor has to trust. A benefit shown converts; a benefit asserted gets skimmed.

Read-only pass. Run the app or read the pages, assets, and components that render the public surfaces; your only write is the report file.

## Phase 1 — Inventory what's shown
- Walk the marketing and product surfaces: landing, features, docs home, pricing, empty states.
- Catalogue the visual evidence present: product screenshots, GIFs and video, diagrams, annotated UI, sample output, before/after, example galleries, live demos.
- For each key claim of value, note whether it is shown, told, or both — and where the biggest "trust me" paragraphs sit with nothing to look at.

## Phase 2 — Audit through 7 lenses
Cite the surface and the exact asset or passage for every finding.
1. **Prose where a picture belongs** — benefits described in a wall of text that one screenshot or clip would land instantly
2. **The product, unseen** — does a visitor ever watch the actual thing working before committing, or only read words about it
3. **How it works, undiagrammed** — mechanisms and flows told step-by-step in text where a simple diagram or numbered visual would carry it
4. **Show the outcome** — is the after-state, result, or payoff pictured, or only promised
5. **Annotated over raw** — screenshots and demos that point at what matters, versus bare images a newcomer can't parse
6. **Stale or fake visuals** — placeholder shots, lorem-ipsum demos, or images drifted from the current UI, which cost more trust than they earn
7. **Weight and accessibility** — heavy media that blocks first paint, autoplay that startles, and visuals with no alt or caption for those who can't see them

## Phase 3 — Curate
- Rank by persuasion-per-pixel: which single visual, added or fixed, would move the most understanding.
- Separate "needs a new asset" (design work) from "has an asset, used wrong" (placement, annotation, caption).
- Flag any visual that would mislead if shipped — a demo of a feature that doesn't exist yet is a promise, not a proof.

## Phase 4 — Report
Create `SHOWCASE.md` at repo root:
1. **Show-vs-tell map** — key claims · shown or told today · the visual that would prove it
2. **Findings** — each: lens · location · what a visitor can't currently see · the asset to add or fix · effort
3. **Top 3 visuals to make** — the highest-leverage things to picture, in order
4. **Media hygiene** — what to annotate, caption, compress, or retire

Start the report with today's date. If `SHOWCASE.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- A benefit the visitor can see beats one they have to believe
- Every finding names the passage that should be shown or the asset that fails
- Prefer one honest screenshot over a paragraph of adjectives
- No marketing or product surface to show the product on in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which visuals to make
