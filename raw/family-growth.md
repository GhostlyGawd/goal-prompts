# Playbook: All Growth briefs (conductor)

You are working inside this repo. Mission: execute the **All Growth briefs** playbook — 11 audit briefs in sequence, each producing one report file at this repo's root.

Every Growth brief in the catalog, in order — 09 through 80, one report each.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **09 · Funnel Friction Audit** — fetch https://goal-prompts.vercel.app/raw/09.md → writes `FUNNEL.md`
2. **10 · Competitive Gap Scan** — fetch https://goal-prompts.vercel.app/raw/10.md → writes `COMPETITIVE.md`
3. **109 · Forms & Validation Audit** — fetch https://goal-prompts.vercel.app/raw/109.md → writes `FORMS.md`
4. **11 · Monetization Map** — fetch https://goal-prompts.vercel.app/raw/11.md → writes `REVENUE.md`
5. **110 · Checkout & Payment Flow Audit** — fetch https://goal-prompts.vercel.app/raw/110.md → writes `CHECKOUT.md`
6. **12 · AI Opportunity Scan** — fetch https://goal-prompts.vercel.app/raw/12.md → writes `AI-IDEAS.md`
7. **70 · SEO & Discoverability** — fetch https://goal-prompts.vercel.app/raw/70.md → writes `SEO.md`
8. **75 · Conversion Rate Optimization** — fetch https://goal-prompts.vercel.app/raw/75.md → writes `CRO.md`
9. **78 · Retention & Lifecycle Audit** — fetch https://goal-prompts.vercel.app/raw/78.md → writes `RETENTION.md`
10. **79 · Social Proof & Credibility** — fetch https://goal-prompts.vercel.app/raw/79.md → writes `PROOF.md`
11. **80 · Activation & First-Win Audit** — fetch https://goal-prompts.vercel.app/raw/80.md → writes `ACTIVATION.md`

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
