---
id: "46"
title: Audit Triage
family: Act
question: does anything change?
output: TRIAGE.md
tagline: The router. Fifteen minutes of recon that names which briefs this repo actually needs, in what order, and which families it can skip with a clear conscience.
---
# Goal: Audit Triage

You are working inside this repo. Mission: run a fast recon — fifteen minutes, not a deep audit — and decide which goal-prompts briefs this repo actually needs, in what order, and which it can safely skip.

Read-only pass. Your only write is the report file.

## Phase 1 — Fingerprint the repo
- What is it: product type, stack, rough size, age, activity (skim the last 90 days of git log)?
- What exists: tests? CI? deploy config? docs? schema/migrations? auth? payments? LLM calls, agent loops, tool definitions, vector stores?
- Prior audit reports at the repo root or in `reports/`? Note them — they change what to recommend.
- Fetch the live catalog once for ids and taglines: `curl -s https://goal-prompts.vercel.app/catalog.json`. If offline, the signal map below carries the id ranges you need.

## Phase 2 — Score through 10 signals
Each signal is evidence → the briefs it implicates. Cite the evidence, not vibes.
1. **Blast radius** — auth, payments, PII, or user-generated content present → Trust (06–08) stops being optional
2. **Quality debt** — missing or failing tests, swallowed errors, TODO density → Quality (01–03)
3. **Scale pressure** — traffic-facing hot paths, growing data, latency complaints → Speed (04–05, 51)
4. **Agent surface** — LLM calls, loops, tools, retrieval, memory, multiple agents → Agent (30–38, 48–50), Automation (39–41), AI-UX (42–44)
5. **Team surface** — more than one contributor, onboarding pain, coding agents expected → Team (13–15, 52)
6. **Ops reality** — real deploys, multiple environments, config sprawl, incident history → Ops (23–25, 53)
7. **Data gravity** — schema, analytics, retention obligations → Data (19–22)
8. **Entropy** — dead code, stale docs, drifted names → Subtract (26–27), Clarity (16–18)
9. **Face value** — user-facing UI with inconsistent type, color, or spacing; missing hover and focus states → Design (54–59)
10. **Pre-product** — an empty repo, a research workspace, an idea instead of a codebase → Venture (60–67): research the market before auditing the code

## Phase 3 — Curate
- Pick 3–7 briefs, no more. Triage that recommends everything recommends nothing.
- Sequence them: cheap-and-revealing first, deep-and-dependent later.
- Default adds worth considering: 00 for anything with users; 28 to merge the reports after any multi-brief run.
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
