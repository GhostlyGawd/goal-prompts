# CONDUCTOR_SPEC — the master conductor, mapped to real brief numbers

2026-07-09 · Status: **implemented** as the generated conductor of the
`zerotoship` playbook. Revision history: the first draft of this spec split
the journey across a separate "research workspace" repo and the product
repo (DECISIONS.md ADR-5); the operator corrected the premise — this whole
system is used by people **on their actual repos** — which dissolved the
repo boundary and restored the original "one artifact" decision
(DECISIONS.md ADR-11).

## The design

Everything runs in the user's actual repo: the Venture briefs write their
research reports at that repo's root (or `reports/`, per the standing
convention every brief already honors), `141` installs the harness into
that same repo — greenfield or grafted onto existing code — and the Build
loop runs where the code lives.

With one repo end to end, the master conductor is one generated artifact:

| Artifact | Stages | Human gates along the way |
|---|---|---|
| `raw/playbook-zerotoship.md` | 61 Niche Map → 62 Pain & Demand → 63 Competitor Teardown → 64 Market Size & Timing → 65 Positioning Wedge → 66 Moat & Model → 67 Venture Verdict → 141 Scaffold the Rails → 142 Spec the Product → 143 Implement to Spec → 144 Ship Gate | 67 asks accept go / pivot / kill; 141 asks before installing anything; 142 asks to ratify the spec; 143 asks the scope; 144 asks ship or hold |

Stage arithmetic: 7 + 4 = 11 stages, under the 16-stage conductor cap
(build.py:200). The go/no-go is not conductor logic: `67`'s own ask-first
gate is the branch point, and the conductor's standing rule ("honor each
brief's own rules, including ending by asking") pauses the run there. A
kill or pivot simply means the operator stops or re-runs a stage instead
of continuing — no conditional grammar needed.

Subset entry points, for repos that don't need the whole arc:

- `raw/playbook-founderfunnel.md` (61→67) — decide only; already existed.
- `raw/playbook-buildloop.md` (141→144) — the operator already knows what
  to build (or wrote a one-paragraph verdict by hand) and wants the rails,
  the spec, the loop, and the gate.
- `raw/family-build.md` — auto-generated family conductor, identical stages
  to buildloop.

## The operate loop (recurring, so never a conductor)

After `SHIP-GATE.md` rules ship, the repo enters the standing loop — same
repo, no handoff:

- Weekly: `raw/29.md` (Weekly Vitals; its first watch-list is the Kill
  criteria restated by 144's Phase 4).
- On accumulated findings: `raw/playbook-triagefix.md` (46 → 47).
- Before anything meaningful ships to users: re-run `144`.

Conductors model sequences with an end; the operate loop is a cadence.
Scheduling it (cron → headless Claude Code) stays deferred until there is
a shipped product to operate (HARNESS_PLAN §4).

## State contract

All state is files at the repo root (or `reports/`): the venture reports
feed 67; `VERDICT.md` is quoted by 141 and mined by 142 for the Job and
Buyer sections; `SPEC.md` binds 143 and 144; `SHIP-GATE.md` seeds 29.
No stage needs conversation memory — which is exactly the conductors' own
rule ("a stage needs only the earlier report files").

## What the operator actually runs

In the actual repo, one line:

> Fetch https://goal-prompts.vercel.app/raw/playbook-zerotoship.md and
> execute it. The idea to pressure-test is: `<one sentence>`.

Operator duties surface as gate questions when the run reaches them
(GitHub push, required status check, CODEOWNERS handle, spec ratification,
build scope, ship/hold).
