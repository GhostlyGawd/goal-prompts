---
id: "46"
title: Audit Triage
family: Act
question: does anything change?
output: TRIAGE.md
related: 47
tagline: The router. Fifteen minutes of recon that names which briefs this repo actually needs, in what order, and which families it can skip with a clear conscience.
---
# Goal: Audit Triage

You are working inside this repo. Mission: run a fast recon — fifteen minutes, not a deep audit — and decide which goal-prompts briefs this repo actually needs, in what order, and which it can safely skip.

Read-only pass. Your only write is the report file.

## Phase 1 — Fingerprint the repo
- What is it: product type, stack, rough size, age, activity (skim the last 90 days of git log)?
- What exists: tests? CI? deploy config? docs? schema/migrations? auth? payments? LLM calls, agent loops, tool definitions, vector stores?
- Prior audit reports at the repo root or in `reports/`? Note them — they change what to recommend.
- Fetch the full index once: `curl -s https://goal-prompts.vercel.app/catalog.json`. The signal map below routes by family question and names only marquee ids; the catalog carries the rest.

## Phase 2 — Score through 12 signals
Evidence → the family it implicates, named by its question, with marquee ids. Cite the evidence, not vibes.
1. **Blast radius** — auth, payments, PII, user content → Trust, "is it safe?" (06, 81, 84; 08 if UI); regulated users or deletion duties → Compliance (125, 126)
2. **Quality debt** — failing tests, swallowed errors, TODO density → Quality, "does it work?" (01, 02, 98)
3. **Scale pressure** — hot paths, growing tables, latency complaints → Speed, "does it scale?" (04, 87, 88, 140)
4. **Uptime stakes** — a service users depend on staying up → Reliability, "will it stay up?" (121, 123, 124)
5. **Agent surface** — LLM calls, loops, tools, retrieval → Agent, "does the agent deliver?" (30, 34, 35); model-step pipelines → Automation (39); humans reviewing AI output → AI-UX (43)
6. **AI with consequences** — a model deciding about people or reading untrusted content → AI-Ethics, "is the AI responsible?" (116–118)
7. **Growth pull** — public funnel, pricing, signups → Growth, "does it grow?" (09, 75, 80); users already inside → Product, "what could this be?" (00, 108)
8. **Developer surface** — a public API, SDK, or package → API, "will developers adopt it?" (112, 115); contract fog → Clarity 18
9. **Team surface** — multiple contributors, onboarding pain → Team, "can others build on it?" (13, 14, 94)
10. **Back-of-house gravity** — deploys, environments, incidents → Ops, "does it run?" (23, 73, 137); schema, migrations, analytics → Data, "is it sound?" (19, 21, 71)
11. **Entropy & face value** — dead code, stale docs → Subtract (26, 27), Clarity, "is it understood?" (16, 76); drifted type, color, spacing → Design, "is it beautiful?" (54, 56, 133)
12. **Pre-product** — an idea instead of a codebase → Venture, "is it worth building?" (60→67 as a sequence): research the market before auditing the code

## Phase 3 — Curate
- Pick 3–7 briefs, no more. Triage that recommends everything recommends nothing.
- Sequence them: cheap-and-revealing first, deep-and-dependent later.
- Default adds worth considering: 00 for anything with users; 28 to merge the reports after any multi-brief run; 74 when the question is one diff, not the repo.
- Name every family you skipped and the evidence that made skipping safe.

## Phase 4 — Report
Create `TRIAGE.md` at repo root:
1. **Fingerprint** — the repo in five lines
2. **Run these** — order · brief id and title · the evidence that earns it · the report it writes
3. **Skipped** — family · why this repo doesn't need it (yet)
4. **After the run** — 28 merges the reports into a roadmap; 47 turns findings into commits

Start the report with today's date. If `TRIAGE.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Every recommendation cites this repo's evidence, never generic best practice
- Fifteen minutes of recon; if a question needs deeper digging, that is what the recommended brief is for
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which of the recommended briefs to run
