# DX Audit — New-Dev Onboarding

**Date: 2026-07-12.** First run — no prior `DX.md` existed.

Scope note: git history shows a single author (Ghostlyyy, 5 commits), but the repo ships CONTRIBUTING.md, a PR template, a PR-gating CI workflow, and adoption/growth docs — contributors are clearly expected, so a full report (not a null report) applies. Everything below was executed in a sandbox clone at current HEAD (`2d5e317`); every command and error message is what actually happened.

## 1. Time-to-first-PR estimate

**Today: roughly half a day (3.5–5 hours)** for a small, competent dev's first merged-quality PR. Almost none of it is tooling wait — the machine loop is sub-second — it is almost entirely discovery of undocumented process traps.

| Stage | Time | Why |
| --- | --- | --- |
| Clone → green `make verify` + `make demo` | ~5 min | Flawless. Zero deps beyond Python 3.11, zero secrets, verify passes in 0.8s |
| Understand the model (README, MASTER.md, templates, `.ai/`) | 60–90 min | Heavy conceptual load: Outcome→Opportunity→Bet→PRD→Spec→Ticket→Trace→Loop |
| Create a valid ticket + trace record | 60–90 min | Scaffold fails validation as generated; 19-field JSON trace record; template/format mismatch; ID conventions must be reverse-engineered |
| Run the governed loop | 30–60 min | Documented example commands fail; three undocumented ordering/state gotchas |
| Open PR, survive CI scope gate | ~30 min | First PR is rejected by CI for including its own ticket file (verified locally) |

With the fixes in section 3, the same path is ~1.5–2 hours, dominated by legitimate reading.

## 2. Stumble log — the walk, step by step

### Clone → install
- `git clone` + Python 3.11.15 + GNU Make: no installation step exists or is needed. **Works.**
- Stumble (minor): the README has no clone/prerequisites line at all (zero matches for "clone"/"install"); "Python 3.11+" appears once in prose, not in Quick start. `scripts/ados.py` has no version guard, so an older system Python would fail with a raw traceback rather than "requires Python 3.11+" (not directly verified — only 3.11 available here).

### Configure (secrets/env)
- **No env vars, no secrets, no config to obtain from anyone.** Only `USER` is read, for actor defaults. This is a genuinely excellent zero-bootstrap story. No blocker requires another human until R2/R3 approval, which is by design (`ados.py approve`).

### Run (seed data)
- `make demo`: completed in **0.07s**, printed the two output paths, produced a populated metrics table (16 metrics), `observability/reports/dashboard.html`, alerts JSON, and demo events. Outputs are deterministic — ran it twice, `git status` stayed clean. A new dev sees the product working, not a blank shell. **Works.**

### Verify (tests)
- `make verify` out of the box: **passed, 30/30 tests, 0.797s total.** `make test` alone: ~0.5s. README's "100 master obligations" claim checks out exactly (`docs/trace/master-compliance.json` has 100 requirement entries). **Works.**

### Make a change — the README "Daily workflow", followed literally
This is where reality diverges. Each item below is a verified stumble:

1. **Step 6 fails verbatim.** `python scripts/ados.py loop plan --ticket TICKET-001` → `ERROR: ticket must be Ready or In Progress` (exit 2). Both shipped tickets are `Status: Complete`, so there is no ticket in the repo on which the documented loop commands work. The error doesn't say what the ticket's current status is or what to do instead.
2. **The README's scaffold example creates a duplicate ID.** The Commands table says `new ticket --id TICKET-002 --title "Example"` — TICKET-002 already exists. The CLI silently created a second `docs/tickets/TICKET-002-example.md` with the same ID, and `make validate` flagged only its placeholder links, **not the duplicate ID**.
3. **The freshly scaffolded ticket fails validation as generated.** `make validate` → `ERROR TICKET_PRD: no requirement link` / `ERROR TICKET_SPEC: no spec acceptance link`. Misleading: the links exist but are the template placeholders (`PRD-NNN-R01`). The error doesn't say where valid IDs live (`docs/prd/`, `docs/specs/`). With real IDs (`PRD-001-R01`, `SPEC-001-A01`), validate passed.
4. **"Record scoped actions" never names the command.** Step 8 says record actions; the subcommand is `loop record-action --ticket X --description ... --paths ...`, discoverable only via `ados.py loop --help` or source.
5. **`loop verify` prints a bare `failed` — nothing else, exit 0.** The cause (the ticket's placeholder `<reproducible command>` returned 2) is only recoverable from `observability/events/loops.jsonl`; command stdout/stderr are captured and discarded (`governance.py:158`).
6. **Loop state snapshots the ticket at `loop start`.** After fixing the ticket's Verification to `make test`, verify still returned `failed` in 0.07s — the old placeholder command was frozen in `observability/events/active-runs.json`. You must stop (with `--outcome failure`) and restart the loop. Undocumented, as is "only one loop may be active in this checkout".
7. **README steps 9 and 10 are in the wrong order.** `loop stop --outcome success` → `ERROR: successful loop requires passing verification`, and after that: stop requires Completion Notes and User Outcome Review to not contain "Pending" — but the README says to update completion notes in step 10, *after* stopping in step 9. Followed literally, step 9 always fails on a scaffolded ticket.
8. After resolving notes: full loop completed; `loop verify` with a real command took **0.708s**. The inner edit→verify loop is superb once you're through the traps.
9. **Trace record friction:** `docs/trace/TEMPLATE.md` is a markdown *table*, but the canonical `docs/trace/traceability.json` wants a 19-field JSON object per record. Hand-editing errors produce `ERROR TRACE_TARGET: unknown requirement: PRD-001-R19` / `unknown test: TEST-999` — correct but with no pointer to where requirement IDs (PRD files) or test IDs (docstrings in `tests/test_*.py`, e.g. `"""TEST-019 ... """`) are defined. Editing the trace without rerunning export gives `ERROR GENERATED_DRIFT: .ai/requirements/traceability.csv` without naming the fix (`python scripts/ados.py product export`).

### Open a PR
10. **The first PR is rejected by CI — verified locally.** Committed a scoped change (ticket allows `README.md`) plus the new ticket file, then ran the CI gate exactly as `governance.yml` does: `python ci/validate_pr_scope.py --body "Implements TICKET-003" --base <base>` → `Files outside ticket scope: docs/tickets/TICKET-003-my-first-change.md` (exit 1). `check_scope` has no carve-out for the ticket file itself, `docs/trace/traceability.json`, or regenerated `.ai/requirements/` views — a ticket must list *its own file* in Files Allowed. Nothing documents this; the shipped examples never hit it because their Files Allowed is effectively the whole repo (TICKET-002 lists every top-level path), which also teaches the wrong scoping habit.
11. Contribution conventions: PR template and body contract (must contain `TICKET-NNN`) are real and enforced; CI feedback is fast (`make verify` sub-second; whole job a couple of minutes). But **no branch naming convention, no review SLA/expectations are written anywhere** (checked README, CONTRIBUTING, docs/, .ai/). `make help` is a bare argparse subcommand list with no descriptions; `status`/`trace-status` (the supported way to flip ticket/trace statuses) are absent from the README table.

### Tribal knowledge I had to infer (lens 7 summary)
- A ticket's Files Allowed must include the ticket file itself + `docs/trace/traceability.json` + `.ai/requirements/` or CI rejects the PR.
- Loop start freezes verification commands and scope; mid-loop ticket edits require failure-stop + restart; one loop per checkout.
- Completion Notes / User Outcome Review must lose the word "Pending" *before* `loop stop --outcome success`.
- `TEST-NNN` IDs resolve from test-module docstrings; requirement IDs from `docs/prd/`; spec IDs from `docs/specs/`.
- `loop record-action` is the "record scoped actions" command; verify diagnostics live in `observability/events/loops.jsonl`.
- `.ai/commands/*.md` guides are one-line prose without commands; `.ai/memory/pitfalls.md` exists but covers none of the traps above.

## 3. Fixes — what · file to change · effort (ordered by stage)

| # | Stage | What | File | Effort |
| --- | --- | --- | --- | --- |
| 1 | Install | Add a 3-line "Prerequisites: Python 3.11+, make; git clone …" block to Quick start | `README.md` | 5 min |
| 2 | Orient | Add one-line descriptions to each subparser so `make help` explains itself | `scripts/ados.py` | 30 min |
| 3 | Ticket | Make `new ticket` refuse an existing ID; change the README example to an unused ID | `scripts/ados.py`, `README.md` | 30 min |
| 4 | Ticket | `new ticket` prints next steps (link real PRD/SPEC IDs → `make validate` → trace entry → `product export` → loop commands) | `scripts/ados.py` | 30 min |
| 5 | Ticket | Reword `TICKET_PRD`/`TICKET_SPEC`/`TRACE_TARGET` errors to say "unresolved ID 'X' — valid IDs defined in docs/prd/ (etc.)"; `GENERATED_DRIFT` to name the export command | `src/agentic_os/validation.py` | 45 min |
| 6 | Trace | Replace the markdown-table trace template with a real JSON record + field notes | `docs/trace/TEMPLATE.md` | 10 min |
| 7 | Loop | Fix Daily workflow: swap steps 9/10, name `loop record-action`, state that TICKET-001/002 are Complete examples and a Ready ticket is needed | `README.md` | 20 min |
| 8 | Loop | On verify failure, print each command, its return code, and tail of stderr; include current status in "must be Ready or In Progress" | `scripts/ados.py`, `src/agentic_os/governance.py` | 45 min |
| 9 | Loop | Document (or lift) the start-time snapshot and single-active-loop rules | `README.md` or `governance.py` | 15 min |
| 10 | PR | Auto-allow the ticket's own file, `docs/trace/traceability.json`, and `.ai/requirements/` in `check_scope` — or document self-listing in CONTRIBUTING | `src/agentic_os/governance.py` or `CONTRIBUTING.md` | 30 min |
| 11 | PR | Write branch naming + review expectations (who reviews, expected turnaround) into CONTRIBUTING | `CONTRIBUTING.md` | 15 min |
| 12 | PR | Scope the shipped example tickets' Files Allowed realistically so examples model the constraint | `docs/tickets/TICKET-00*.md` | 20 min |

## 4. The one-hour fix

**Make `ados.py new ticket` the onboarding script** (fixes 3 + 4, plus refuse-duplicate and a self-scoped scaffold): it should refuse existing IDs, accept `--prd/--spec` so the scaffold is born valid, pre-list the ticket's own file and `docs/trace/traceability.json` in Files Allowed, and print the exact remaining commands in the correct order (validate → trace entry → export → loop plan/start/record-action/verify → resolve completion notes → stop → PR body must contain the ticket ID). A setup script beats a setup document: this single change de-mines stumbles 2, 3, 4, 7, and 10 at the moment each dev first meets them, for every future hire, and is ~60 minutes in `scripts/ados.py`.

(Runner-up, same spirit: ship one `Ready` tutorial ticket and rewrite the Daily workflow against it so every documented command works verbatim.)

---

The tooling core is fast, deterministic, and secret-free — the friction is concentrated in five documented-path traps, all cheap to fix. **Which of the fixes above should I make?**
