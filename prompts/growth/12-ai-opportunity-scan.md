---
id: "12"
title: AI Opportunity Scan
family: Growth
question: does it grow?
output: AI-IDEAS.md
tagline: Where an LLM feature genuinely earns its place — automation, drafting, summarization — and where it would be a gimmick.
---
# Goal: AI Opportunity Scan

You are working inside this repo. Mission: find where an AI feature would genuinely earn its place in this product — and just as importantly, where it would be a gimmick. 

Read-only pass. Your only write is the report file.

## Phase 1 — Inventory the raw material
- What data does this product hold: text, images, events, structured records? Where does it accumulate?
- What tedious multi-step tasks do users repeat? (trace the flows)
- Where do users make judgment calls the product could draft for them?

## Phase 2 — Scan through 6 lenses
1. **Automate toil** — multi-step chores collapsible into one reviewed action
2. **Draft generation** — content, replies, configs, names, summaries the user currently writes from scratch
3. **Summarize their own data** — turning accumulated user data into insight ("your week", "what changed")
4. **Natural-language input** — search, filters, or commands where typing intent beats clicking through UI
5. **Triage & classification** — sorting, tagging, routing, prioritizing that users do manually
6. **Anti-pattern check** — proposed AI that adds latency, cost, or wrongness where a rule or a button would do; name these explicitly

## Phase 3 — Curate
For each surviving idea, answer all five:
- The user moment it improves (specific screen/flow)
- Data it needs — have it vs must collect it
- Failure mode — what happens when the model is wrong, and the fallback
- Cost & latency — rough call volume and tolerance
- Build shape — prompt-only, RAG over user data, or fine-grained tool use

## Phase 4 — Report
Create `AI-IDEAS.md` at repo root:
1. **Raw material summary** — the data and toil this product actually has
2. **Ideas** — each with the five answers above, plus value and feasibility ratings
3. **Value × feasibility ranking**
4. **Gimmick list** — rejected ideas and why (this list protects the roadmap)
5. **Prototype-this-week pick** — one idea, scoped to a day

Start the report with today's date. If `AI-IDEAS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- AI must beat the boring alternative (a rule, a default, a button) — prove it per idea
- Wrong-answer handling is part of the feature, not an afterthought
- No product surface to scan for AI opportunities in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which idea to prototype
