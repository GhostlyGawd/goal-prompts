# Product Improvement Discovery — Agentic Development Operating System

Date: 2026-07-12
(First run — no previous `IMPROVEMENTS.md` existed.)

## 1. Product snapshot

Agentic Development OS is a repository-native, zero-dependency (Python 3.11+ stdlib) governance system for teams shipping software with AI agents: it chains product intent (outcome → opportunity → bet → PRD → spec → ticket) to bounded agent execution loops, and proves the chain with append-only JSONL events, 15 delivery metrics, threshold alerts, and a static HTML dashboard. Its users are AI-native product/platform teams (PRD-001 `docs/prd/PRD-001-agentic-development-os.md:21`) — and, critically, their agents, which are expected to operate the CLI (`scripts/ados.py`, 16 subcommands) inside "Ralph loops" with file-scope and risk-tier enforcement. The intended journey is: clone → `make verify` + `make demo` (README quick start) → adapt one ticket in shadow mode → graduate to autonomous R0/R1 execution once metrics stabilize (`docs/specs/SPEC-002-adoption.md`) → publish case studies per the growth playbook (`docs/growth/`). The repo is one day old (git log: 2026-07-11..12, 5 commits), fully green on its own 100-obligation compliance gate, and all 30 tests pass (verified this run). Its core promise is "evidence over memory" (README:104) — which makes the verified findings below sting: verification evidence can be forged with a flag, the demo command deletes the real event history, and CI's metrics step emits false alerts on every fresh checkout. There is also notable half-built infrastructure: a 10-tool agent catalog with no executable surface (`tools/catalog.json`), a dashboard definition file the renderer never reads (`observability/dashboards/default.json`), five catalogued event types nothing can emit, and timestamps on every event that no report ever aggregates into a trend.

## 2. Opportunity map (impact × effort)

| | Effort S (≤1 day) | Effort M (days) | Effort L (week+) |
| --- | --- | --- | --- |
| **Impact H** | #1 dry-run forgery, #2 demo wipes history, #3 false/duplicate alerts, #8 loop status + help | #10 real trace impact analysis, #12 metric history & trends | #13 upstream scaffolding, #14 tool catalog → agent server |
| **Impact M** | #4 input hardening, #5 stale audit dead in CI, #9 show verification output | #6 product-gate filter, #7 corrupt-event recovery, #11 dashboard uses its definition, #15 emit-able lifecycle events | — |

Generated ~30 raw ideas; curated to 15. Cut in curation: wiring the configured-but-never-run ruff/pyright (`pyproject.toml:8-12` vs `Makefile:18-20`; the unused `import shutil` at `scripts/ados.py:8` shows the gap), README badges from `metrics.json`, Windows `make` support, glob support in scope rules — real but low-impact or generic.

## 3. Top 5 quick wins & Top 3 big bets

**Quick wins (~a day each):** #1 close the `--dry-run` verification hole · #2 make `demo` non-destructive · #3 no-data alert guard + alert dedupe · #4 CLI input hardening · #8 `loop status` + named-ticket errors + subcommand help.

**Big bets:** #13 scaffolding for the entire upstream chain (`new bet|outcome|…` + `trace add`) · #14 turn `tools/catalog.json` into a working agent tool server · #12 metric history and trends (unlocks the product's own graduation gates).

## 4. Full list

### #1 Verification evidence can be forged with `--dry-run` — FIX · Fixes & felt debt
- **Evidence:** `scripts/ados.py:89` passes `not args.dry_run` into `LoopManager.verify`; `src/agentic_os/governance.py:154-160` then records `returncode: 0` for every command *without executing anything* and sets `run["verified"]=True`; `governance.py:173-174` lets `stop --outcome success` through on that flag. Reproduced in a sandbox copy: `loop start` → `loop verify --dry-run` → `loop stop --outcome success` succeeds, and `loops.jsonl` contains `verification.completed outcome: passed, checks: [{make verify, rc 0}, {make demo, rc 0}]` — indistinguishable from a real run.
- **Proposal:** Record `executed: false` in the event and loop state; make `stop --outcome success` reject non-executed verification (tests that use `execute=False` should assert the rejection instead).
- **Why it matters:** The product's single value proposition is trustworthy execution evidence; today the audit trail is forgeable by one flag.
- **Effort:** S · **Impact:** H · **Risks:** Breaks `tests/test_end_to_end.py:19` and `tests/test_governance.py:27` which stop successfully after `execute=False` — update them deliberately.

### #2 `make demo` destroys real event history — FIX · Retention
- **Evidence:** `scripts/ados.py:161` — `event_path.unlink(missing_ok=True)` deletes `observability/events/loops.jsonl` before emitting demo events. README:24-26 tells every new user to run `make demo`. Reproduced: 6 real events → `demo` → 5 synthetic events. (`make clean`, Makefile:37, also deletes all event streams.)
- **Proposal:** Point demo output at a separate stream (`observability/events/demo.jsonl` or a temp dir), render to preview paths, and never unlink the canonical stream.
- **Why it matters:** An append-only evidence system whose own quick-start command erases the evidence violates "evidence over memory" (README:104) and punishes exactly the users who reached the habit stage.
- **Effort:** S · **Impact:** H · **Risks:** Demo determinism — solved by the separate stream.

### #3 Metrics falsely alarm on empty streams and duplicate alerts forever — FIX · Feedback & state
- **Evidence:** `src/agentic_os/metrics.py:44-53` breaches thresholds on zero-run rates: with no events, `first_pass_success_rate` 0.0 < 0.80 and `event_completeness_rate` 0.0 < 0.95 (`ado.config.json:10-11`). Reproduced: fresh tree → `ados.py metrics` → 2 alerts. Since `loops.jsonl` is gitignored (`.gitignore:8`), CI's `make metrics` step (`.github/workflows/governance.yml:28-29`) uploads false alerts as "governance evidence" on every PR. Additionally `scripts/ados.py:103` re-appends `alert.triggered` on every run — reproduced: 3 runs → 6 duplicate alert events in the canonical stream.
- **Proposal:** Report "no data" (and skip run-denominated thresholds) when `runs_started == 0`; emit `alert.triggered` only on state transition by diffing against `observability/alerts/latest.json`.
- **Why it matters:** Alert fatigue on day one teaches users to ignore the alerting system; duplicate alert events pollute the metrics' own input.
- **Effort:** S · **Impact:** H · **Risks:** None significant; keep the "no data" state explicit so it can't mask real gaps.

### #4 CLI inputs crash or corrupt state instead of failing helpfully — FIX · Friendliness
- **Evidence (all reproduced):** (a) `approve --expires-at 2030-01-01` is accepted, then `loop start` dies with a raw `TypeError: can't compare offset-naive and offset-aware datetimes` at `governance.py:74`; (b) `new ticket --title "Fix A/B flow"` dies with `FileNotFoundError` from the unsanitized slug at `scripts/ados.py:34`; (c) `status ticket --status Bananas` is accepted (`scripts/ados.py:57-65`) even though gates only recognize Ready/In Progress (`governance.py:102`) and Complete/Cancelled (`ado.config.json:5`); (d) loop durations diff a persisted `time.monotonic_ns()` across processes (`governance.py:118,179`) — after a reboot the negative value makes `telemetry.py:58-60` raise, so the loop can never stop.
- **Proposal:** Normalize/require timezone at approve time; slugify titles to `[a-z0-9-]`; validate status against the real vocabulary; use wall-clock epoch (or clamp ≥0) for durations.
- **Why it matters:** These are the first commands a new team runs; tracebacks and silently corrupted status fields erode trust in a trust product.
- **Effort:** S · **Impact:** M · **Risks:** Status vocabulary must match existing docs' statuses (Accepted, Draft…) — derive per artifact kind.

### #5 The weekly stale-artifact audit can never fire in CI — FIX · Fixes & felt debt
- **Evidence:** `src/agentic_os/validation.py:107-112` uses `st_mtime`; the scheduled audit job does a fresh checkout (`.github/workflows/governance.yml:42-49`), where every file's mtime is checkout time, so `stale_artifacts` is always empty. The feature only "works" in long-lived local clones.
- **Proposal:** Derive age from `git log -1 --format=%ct -- <path>` (subprocess git is already a pattern: `governance.py:82-84`).
- **Why it matters:** A maintenance control that structurally cannot trigger is false confidence — one of PRD-001's own named risks (`docs/prd/PRD-001-agentic-development-os.md:58`).
- **Effort:** S · **Impact:** M · **Risks:** Slightly slower audit; batch with one `git log --name-only` pass if needed.

### #6 The PRD product gate filters issues by substring luck — FIX · Fixes & felt debt
- **Evidence:** `scripts/ados.py:152` — `relevant=[issue for issue in issues if args.prd in issue or "bet" in issue or "outcome" in issue or "opportunity" in issue]`. Any repo-wide validation issue mentioning "bet"/"outcome" blocks an unrelated PRD; a PRD-specific issue phrased without those words passes the gate.
- **Proposal:** Have `validate_product` return structured issues (artifact ref + code), and gate on the named PRD's actual ancestry.
- **Why it matters:** The gate is the enforcement point of the whole "no PRD from an unvalidated bet" rule (MASTER.md:33); it should be precise, not lexical.
- **Effort:** M · **Impact:** M · **Risks:** Touches `validate_product`'s return type — keep a string view for existing callers/tests.

### #7 One corrupt event line bricks metrics and validate — IMPROVE · Feedback & state
- **Evidence:** `src/agentic_os/telemetry.py:76-85` raises on the first bad line. Reproduced: appending one truncated line makes both `ados.py metrics` and `ados.py validate` fail (`ERROR EVENT_INVALID: invalid event at line 7…`). A killed process mid-append produces exactly this, and the only fix is hand-editing the evidence file the docs say never to hand-edit.
- **Proposal:** `ados.py events repair` that quarantines bad lines to a sidecar and records the repair as an event; or a `--skip-invalid` read mode that reports a completeness warning.
- **Why it matters:** Graceful failure for the system's single most load-bearing file; currently availability of all reporting hinges on perfect JSONL hygiene.
- **Effort:** M · **Impact:** M · **Risks:** Silent evidence loss — mitigated by quarantine + explicit repair event.

### #8 The CLI cannot tell you where you are — IMPROVE · UX & flows / Onboarding
- **Evidence:** No `loop status` action exists (`scripts/ados.py:172` choices are plan/start/record-action/retry/verify/stop). The single-loop guard error says only "only one loop may be active in this checkout" (`governance.py:115-116`, reproduced) — not which ticket, run, or how to resolve it. `ados.py --help` lists 16 subcommands with zero descriptions (no `help=` anywhere in `parser()`, `scripts/ados.py:167-185`), and `make help` (Makefile:5-6) surfaces that same bare list as the primary onboarding aid.
- **Proposal:** Add `loop status` (active ticket, run id, retries, verified flag, elapsed); include the active ticket in the guard error; add one-line `help=` per subcommand and a workflow epilog mirroring README's daily workflow.
- **Why it matters:** This is the daily driver for both humans and agents; discoverability currently lives only in the README.
- **Effort:** S · **Impact:** H · **Risks:** None.

### #9 Verification failures hide their output — IMPROVE · Helpfulness
- **Evidence:** `governance.py:158-160` captures stdout/stderr but stores only `returncode`; a failing `loop verify` prints just "failed" (`scripts/ados.py:89`), forcing a manual rerun to learn why.
- **Proposal:** Print the failing command plus a redacted, size-capped output tail; store the same tail in `verification.completed` metadata (through `_sanitize`).
- **Why it matters:** Retry depth is a first-class metric (`docs/metrics/catalog.md` METRIC-004); giving the agent the failure reason is the cheapest way to reduce it.
- **Effort:** S · **Impact:** M · **Risks:** Event bloat / secret leakage — cap length, reuse the redaction pass.

### #10 `trace-query` undersells the trace graph it owns — IMPROVE · Helpfulness / Synergies
- **Evidence:** `scripts/ados.py:51-54` does exact value matching only. Reproduced: `trace-query --id PRD-001` → `[]`, exit 1, no hint — despite 18 related records in `docs/trace/traceability.json`. README:66 sells it as "forward/backward impact analysis". The 17-field records plus `ci/impact-map.json` already encode the full chain.
- **Proposal:** Support prefix/partial IDs; render the chain (outcome → opportunity → bet → PRD → spec → ticket → test → metric → review) for any matched ID; append impacted tests via the impact map; print a "did you mean" hint on zero matches.
- **Why it matters:** This is the payoff moment of all the traceability discipline — the "what breaks if I touch this?" answer — and today it returns an empty array.
- **Effort:** M · **Impact:** H · **Risks:** Keep `--json` exact-match behavior for scripts; add the rich view alongside.

### #11 The dashboard ignores its own definition file — IMPROVE · UI & beauty / Synergies
- **Evidence:** `render_dashboard` (`src/agentic_os/metrics.py:79-86`) hardcodes cards and formats every value as a bare 2-decimal float — the committed `observability/reports/dashboard.html` shows "Task Completion Rate 1.00" and "Lead Time Ms 1200.00". `observability/dashboards/default.json` (titles + thresholds per metric) is only existence-checked (`validation.py:38`) and never consumed; `ado.config.json` thresholds aren't used for display either; alerts render as `metric: value` without the breached rule; dark-only palette; no generated-at timestamp.
- **Proposal:** Drive cards from `default.json` + config thresholds (green/amber/red status per card), format rates as %, cost as $, durations as s, show the rule in alerts, stamp generation time, add a `prefers-color-scheme: light` variant.
- **Why it matters:** The dashboard is the shareable proof artifact in the growth loop ("dashboards… must be copyable and shareable", `docs/growth/operating-system.md:13`); right now it reads as a debug page.
- **Effort:** M · **Impact:** M · **Risks:** None — data already exists.

### #12 History exists, trends don't — NEW · Retention / Engagement
- **Evidence:** Every event carries an ISO timestamp (`telemetry.py:36-44`), yet `summarize` (`metrics.py:10-41`) collapses all time into one snapshot; `docs/metrics/latest.md` is overwritten each run; `scripts/metrics/aggregate.py` just re-runs the snapshot. The adoption spec's own graduation gate — "First-pass success is stable for four weeks" (`docs/specs/SPEC-002-adoption.md:21`) — is unmeasurable with current reporting.
- **Proposal:** Bucket events by ISO week into an append-only `observability/reports/history.json`; add a trend column (and dashboard sparklines) for the key rates; alert on deterioration, not just absolute thresholds.
- **Why it matters:** Trends are the reason to *return* to the dashboard, and the product's own rollout model depends on them.
- **Effort:** M · **Impact:** H · **Risks:** Week-boundary edge cases; keep raw events canonical and history derived.

### #13 The upstream chain has no scaffolding — NEW · Onboarding / UX & flows
- **Evidence:** `ados.py new` supports only prd/spec/ticket (`scripts/ados.py:33`), but the enforced chain demands outcome/opportunity/experiment/bet/milestone/CR/review files with exact section contracts validated in `src/agentic_os/product.py:59-131` — and no TEMPLATE.md exists anywhere under `.ai/` (full file inventory: templates exist only under `docs/`). The daily workflow also requires hand-editing a 17-field JSON record (README:47, `docs/trace/traceability.json`).
- **Proposal:** `ados.py new outcome|opportunity|experiment|bet|milestone|change-request|review` generating section-complete stubs *from the same contracts dict the validator uses*, plus `ados.py trace add` that composes a record interactively with defaults from sibling records and validates before writing.
- **Why it matters:** Time-to-first-value for a real team is dominated by "copy a file you don't have and guess eight required headings until `product validate` stops erroring." This converts the validator from a wall into a guide.
- **Effort:** L · **Impact:** H · **Risks:** Stub/validator drift — eliminated by generating both from one contract table.

### #14 The agent tool catalog is a spec without a server — NEW · Synergies / Reach
- **Evidence:** `tools/catalog.json` defines 10 governed tools (validate_repository, create_ticket, start_loop, record_event, update_trace, archive_ticket, validate_product_chain, export_product_views, evaluate_product_gate, record_product_review) with descriptions, parameters, and server-side validation notes; `src/agentic_os/tooling.py` lint-enforces the naming standard — but nothing executes any of them, and `record_product_review` has no CLI equivalent at all. The declared primary users are AI-native teams (`docs/prd/PRD-001-agentic-development-os.md:21`) whose agents consume tools, not READMEs.
- **Proposal:** A stdlib-only stdio JSON-RPC/MCP server (`scripts/ados_server.py`) mapping catalog entries 1:1 onto the existing `agentic_os` functions, with a parity test (every catalog tool has a handler and vice versa). Risk-tier gating and digest approvals already exist to protect the write paths.
- **Why it matters:** This is the cheapest route from "framework you read about" to "thing your agent actually operates," and it directly serves the GitHub-channel growth motion (clone → agent connects → first governed loop).
- **Effort:** L · **Impact:** H · **Risks:** New security surface — reuse `check_scope`/`approval_valid`, keep R2/R3 tools human-gated.

### #15 Catalogued lifecycle events nothing can emit — NEW · Synergies
- **Evidence:** `approval.revoked`, `finding.recorded`, `human.intervened`, `product_review.completed`, `reversal.completed` are all in `EVENT_NAMES` (`telemetry.py:15-22`) and the JSON schema, but no command produces them (only the generic low-level `emit`). `reversal.completed` is even consumed by the regression metric (`metrics.py:23`). Approvals are written with `status: "active"` (`governance.py:60`) and there is no revoke path; `docs/findings/README.md` asks for FINDING-NNN markdown files but no command creates or instruments them.
- **Proposal:** `ados.py approve --revoke`, `ados.py finding record` (scaffolds the markdown + emits `finding.recorded`), `ados.py review record` (writes the review log + emits `product_review.completed` / `milestone.reviewed`).
- **Why it matters:** The measurement layer promises a fully instrumented lifecycle (MASTER.md:19); today several instruments exist only as enum entries, so the metrics that depend on them silently read zero.
- **Effort:** M · **Impact:** M · **Risks:** None significant; reuse existing event validation.

## 5. Sequence — if only 3 ship first

1. **#1 Close the dry-run verification hole.** Everything this product sells — approvals, metrics, case studies — rests on `verification.completed` meaning verification happened. A one-flag forgery, provable in three commands, is an existential credibility bug for a governance tool.
2. **#2 + #3 Make the evidence stream trustworthy (demo no longer wipes it; alerts only fire on real breaches, once).** These two share a theme and a day: after them, the canonical JSONL and the alert channel are safe to rely on from first clone through CI, which is the precondition for every retention and growth artifact built on top.
3. **#8 `loop status` + named errors + subcommand help.** The cheapest first-touch UX repair: the funnel in `docs/growth/strategy.md` is README → `make demo` → first ticket, and today the first stumble ("only one loop may be active…" — which one?) has no in-tool answer. Ship the trust fixes, then make the daily driver explain itself; the big bets (#13, #14) then have a foundation worth building on.

---
Report only — no code was modified. **Which of these items should I build?**
