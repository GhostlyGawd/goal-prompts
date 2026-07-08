---
id: "105"
title: Design-Token Adoption Audit
family: Design
question: is it beautiful?
output: TOKEN-ADOPTION.md
tagline: Whether the design system's tokens are actually used — or whether hardcoded colors, spacing, and type have crept back in and drifted the UI out of sync.
---
# Goal: Design-Token Adoption Audit

You are working inside this repo. Mission: check whether the design tokens are the single source of truth they claim to be — or whether hardcoded values have crept in, quietly drifting the interface out of alignment one one-off at a time.

Read-only pass. Read the token definitions and the styles that should consume them; change nothing but the report file.

## Phase 1 — Find the source of truth
- Locate the token definitions: color, spacing, type, radius, shadow, motion.
- Note how they are meant to be consumed and where they are defined more than once.
- Scan the styles for literal values that should reference a token.

## Phase 2 — Audit through 7 lenses
Cite file and line for every finding.
1. **Color creep** — hex/rgb literals where a color token belongs; near-duplicate one-off colors
2. **Spacing creep** — magic pixel values instead of the spacing scale
3. **Type creep** — ad-hoc font sizes, weights, and line-heights outside the type scale
4. **Token coverage** — surfaces (states, dark mode, borders, shadows) with no token, so people improvise
5. **Duplication & drift** — the same value defined in several places that can fall out of sync
6. **Single source of truth** — whether tokens flow from one definition or are copied per surface
7. **Enforcement** — is there a lint rule or check, or does drift only get caught by eye

## Phase 3 — Curate
- Rank by visible drift and spread: a one-off color repeated across many components outranks a single stray value.
- For each, map the literal to the token it should use, or the token the system is missing.
- Separate "use the existing token" from "the system lacks a token"; both cause creep.

## Phase 4 — Report
Create `TOKEN-ADOPTION.md` at repo root:
1. **Adoption score** — per category (color, spacing, type): tokenized versus hardcoded
2. **Offenders** — the worst hardcoded values with locations and the token they should use
3. **Missing tokens** — the surfaces with no token, so improvisation is inevitable
4. **Enforcement** — the lint rule or check that keeps hardcoded values from returning

## Rules
- One value, one token, one definition; a copied value will drift
- A missing token is a cause of creep, not just the literal that fills it
- Report only — end by asking which drift to correct first
