# CONDUCTOR_SPEC — the master conductor, mapped to real brief numbers

2026-07-09 · Status: designed; the two machine-facing conductors already
exist as generated artifacts. Rationale for the shape (a deviation from the
"one artifact" prior decision): DECISIONS.md ADR-5.

## Why not one conductor

The catalog's conductors are generated (`conductor()`, build.py:191), capped
at 16 stages (build.py:200), parity-checked across build.py, mcp/server.cjs
and js/catalog-core.js by the MCP smoke test — and they assume one repo for
the whole run. The founder→operator journey crosses a repo boundary (the
research workspace → the product repo that 141 creates) and passes two
human decision points that are already ask-first gates inside briefs. So
the master conductor is an operator runbook that chains two stock,
generated conductors; the gates inside 67, 141, 142, 143 and 144 are the
branch logic.

## The map, with real ids

| Leg | Artifact | Stages | Repo | Human gate at the end |
|---|---|---|---|---|
| Decide | `raw/playbook-founderfunnel.md` | 61 Niche Map → 62 Pain & Demand → 63 Competitor Teardown → 64 Market Size & Timing → 65 Positioning Wedge → 66 Moat & Model → 67 Venture Verdict | research workspace | 67 asks: accept go / pivot / kill |
| Build | `raw/playbook-buildloop.md` | 141 Scaffold the Rails → 142 Spec the Product → 143 Implement to Spec → 144 Ship Gate | product repo (created by 141) | 141 asks before instantiating; 142 asks to ratify the spec; 143 asks the scope; 144 asks ship or hold |
| Operate | standing loop, no conductor | 29 Weekly Vitals (weekly) · 46 Audit Triage → 47 The Fixer (on accumulated findings) · 144 re-run before releases | product repo | 29/46 end by asking; 47 gates on scope |

Stage arithmetic: 7 + 4 = 11 conductor stages, both legs under the 16 cap.
Playbook keys: `founderfunnel` (existing), `buildloop` (added this session).

## The operator runbook (the "one artifact", operator-facing)

Paste into Claude Code, one leg at a time:

**Leg 1 — in an empty research-workspace repo:**
> Fetch https://goal-prompts.vercel.app/raw/playbook-founderfunnel.md and
> execute it. The niche to research is: `<OPERATOR FILLS THIS IN>`.

Stop condition: `VERDICT.md` rules. Kill → archive the workspace, keep what
transfers. Pivot → re-run the named leg. Go → Leg 2.

**Leg 2 — in the directory where the product repo should be created:**
> Fetch https://goal-prompts.vercel.app/raw/playbook-buildloop.md and
> execute it. The go verdict is in `<path-to-workspace>/VERDICT.md`; copy
> the venture reports it cites into the new repo's `reports/` when 141
> scaffolds it.

Operator duties surface at 141's gate (create the GitHub repo, make the
`check` workflow a required status check, set CODEOWNERS) and 142's gate
(ratify the spec). Stop condition: `SHIP-GATE.md` rules ship.

**Leg 3 — standing, weekly, in the product repo:**
> Fetch https://goal-prompts.vercel.app/raw/29.md and execute it.

Monthly or on accumulated findings:
> Fetch https://goal-prompts.vercel.app/raw/playbook-triagefix.md and
> execute it.

Re-run 144 before anything meaningful ships to users.

## Handoff contract between the legs

- Leg 1 → Leg 2: `VERDICT.md` (plus the six reports it scores) is the only
  carried state; 141 quotes the ruling, 142 reads POSITIONING/DEMAND/NICHE
  from `reports/` for the Job and Buyer sections.
- Leg 2 → Leg 3: `SPEC.md`'s Kill criteria section becomes 29's first
  watch-list (144 Phase 4 writes exactly this restatement).
- All state is files at a repo root — no conversation memory, matching the
  conductors' own rule that a stage needs only earlier report files.

## Deferred (recorded, not blocking)

- A `/raw/`-served copy of this runbook (would need a build.py output; the
  GitHub raw URL of this spec serves the purpose meanwhile).
- Headless scheduling of Leg 3 (cron → Claude Code headless) — pointless
  before a product exists (HARNESS_PLAN §4).
