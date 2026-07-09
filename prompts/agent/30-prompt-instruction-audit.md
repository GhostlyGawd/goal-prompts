---
id: "30"
title: Prompt & Instruction Audit
family: Agent
question: does the agent deliver?
output: PROMPTS.md
tagline: Every system prompt in the repo: contradictions, dead instructions, bloat, and injection surface — with a consolidation plan.
---
# Goal: Prompt & Instruction Audit

You are working inside this repo. Mission: audit every prompt this product sends to a model — system prompts, templates, few-shot examples, inline instructions — for contradictions, rot, bloat, and injection risk.

This audits prompt quality. For the defensive guard architecture around the agent, run 35; to attack the product's AI like an adversary, run 118.

Read-only pass. Your only write is the report file.

## Phase 1 — Find every prompt
- Locate them all: prompt files, template strings, f-strings in code, few-shot examples, instructions concatenated at call sites.
- For each: which model receives it, at what temperature, for what job, roughly how many tokens.
- Are prompts versioned and diffable, or scattered string literals?

## Phase 2 — Audit through 8 lenses
Cite the file and line for every finding.
1. **Contradictions** — instruction A vs instruction B; prompt rules vs tool descriptions; system vs few-shot behavior
2. **Dead instructions** — rules about features, formats, or tools that no longer exist
3. **Bloat** — repeated emphasis, ALL-CAPS inflation, boilerplate the model demonstrably ignores; tokens paid on every call
4. **Vague directives** — "be helpful, be accurate" vs testable instructions with defined behavior
5. **Format gaps** — downstream parsing assumes structure the prompt never actually demands
6. **Example rot** — few-shots contradicting current rules or demonstrating retired formats
7. **Injection surface** — user or retrieved content interpolated without delimiters, fencing, or role separation
8. **Sprawl** — the same rule copy-pasted across prompts, each copy drifting independently

## Phase 3 — Curate
- Rank by blast radius: prompts on the hot path outrank one-off utilities
- Every claim of "the model ignores this" needs a mechanism or trace evidence, not vibes

## Phase 4 — Report
Create `PROMPTS.md` at repo root:
1. **Prompt inventory** — location · model · job · est. tokens · version-controlled?
2. **Findings** — each: issue · lens · evidence · fix · risk of changing it
3. **Consolidation plan** — shared rules extracted to one source, per-prompt deltas
4. **First rewrite** — the worst prompt, before/after sketch, and how to eval the change before shipping (see 34)

Start the report with today's date. If `PROMPTS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Prompt changes are behavior changes: every fix names its eval or rollback plan
- Shorter and testable beats longer and reassuring
- No prompts or agent instructions in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which rewrites to make
