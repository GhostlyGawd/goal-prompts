---
id: "120"
title: Training-Data Provenance
family: AI-Ethics
question: is the AI responsible?
output: PROVENANCE.md
tagline: Whether the data used to train, fine-tune, or retrieve is licensed, clean, and free of the PII and contamination that create legal and quality risk.
---
# Goal: Training-Data Provenance

You are working inside this repo. Mission: trace the data behind the product's models — training sets, fine-tuning data, and retrieval corpora — and judge whether it is licensed for this use, free of unconsented personal data, and uncontaminated. If the product only calls a hosted model, focus on retrieval and prompt data.

Read-only pass. Read the data-loading, fine-tuning, and indexing code and any dataset docs; change nothing but the report file.

## Phase 1 — Inventory the data
- List every dataset the product trains on, fine-tunes on, or retrieves from.
- For each, find where it came from and under what terms.
- Note whether personal or user data is among it.

## Phase 2 — Audit through 7 lenses
1. **Source & licensing** — where the data came from and whether its license permits this use
2. **PII in data** — personal data in training sets or corpora, and the basis for using it
3. **Consent & terms** — data scraped or reused against its terms; user data used to train without disclosure
4. **Contamination** — test or eval data leaking into training; benchmark leakage inflating results
5. **Copyright & attribution** — copyrighted content whose reproduction creates exposure
6. **Lineage** — can you trace what went into a model or index, and remove a source if required
7. **Retention & deletion** — can specific data be deleted from datasets and downstream indexes on request

## Phase 3 — Curate
- Rank by legal exposure and quality impact: unlicensed data or PII with no basis outranks a minor attribution gap.
- For each, name the control — a license check, a PII scrub, a lineage record, a deletion path.
- Separate a legal risk from a quality risk; both matter, differently.

## Phase 4 — Report
Create `PROVENANCE.md` at repo root:
1. **Data inventory** — dataset · source · license · contains PII?
2. **Findings** — each: risk (legal or quality) · dataset · the issue · the control
3. **Lineage & deletion** — the tracking and removal capability to build
4. **Priority** — the exposures to remediate first

Start the report with today's date. If `PROVENANCE.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- If you cannot say where the data came from, you cannot defend using it
- Contamination invalidates your evals before it ever reaches production
- No training or fine-tuning data in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which data risks to address first
