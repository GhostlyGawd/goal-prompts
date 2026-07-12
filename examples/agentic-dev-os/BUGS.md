# Bug Hunt — agentic-dev-os

**Date:** 2026-07-12
**Run:** initial (no prior `BUGS.md` found at repo root or in `reports/`)

Scope note: this repo has no frontend/runtime app to click through — it's a Python CLI (`scripts/ados.py` + `src/agentic_os/`) that governs *itself* (tickets, approvals, traceability, metrics, telemetry). "Money/auth/irreversible" here maps to: the append-only event log, approval records, the traceability/compliance ledger, and the CI gates that block merges. I read every module in `src/agentic_os/`, `scripts/ados.py`, all of `ci/`, the test suite, the governance docs (`agent/policies/*`, `agent/harness/*`), and cross-checked claims with `git log`, `grep`, and a full manual trace of `validate_repository(ROOT)` against the live artifacts (Python execution was blocked in this sandbox, so everything below is argued from static reading, not a test run).

One honest data point up front: I manually traced all ten sub-checks inside `validate_repository(ROOT)` (structure, tickets, trace, compliance, owners, product chain, generated-view drift, architecture, tool catalog, event log) against the actual committed artifacts, and the repo **does** currently satisfy its own validator — this is not a "tests are already red" situation. The bugs below are latent/dormant traps and silent gaps, not currently-failing gates.

## Summary

- **10 findings** — **S1: 2** · **S2: 6** · **S3: 2**
- **Scariest finding (#1):** `python scripts/ados.py demo` unconditionally deletes the real, gitignored (unrecoverable) event log before seeding fake data — and `make demo` is not just a README suggestion, it is literally listed as a **Verification** step on both real tickets in this repo (`TICKET-001`, `TICKET-002`). Running ticket verification for real (the documented, default CLI behavior) wipes the project's entire operational history.

## Findings

### 1. `ados.py demo` destroys the real event log — and it's wired into ticket verification itself
**Severity:** S1 (irreversible data loss) · **Confidence:** certain

**Location:** `scripts/ados.py:160-164` (`demo()`), `docs/tickets/TICKET-001-bootstrap.md:86-88`, `docs/tickets/TICKET-002-product-strategy-integration.md:72-76`, `README.md:19-24`, `src/agentic_os/governance.py:146-162` (`LoopManager.verify`), `scripts/ados.py:89,172` (CLI wiring, `execute` defaults `True`)

```python
def demo(_):
    event_path=ROOT/load_config(ROOT)["event_file"]; event_path.unlink(missing_ok=True)
    run="demo-"+uuid.uuid4().hex[:10]
    for event,fields in [...]: append_event(event_path,build_event(event,run,"TICKET-001","demo",**fields))
    metrics(argparse.Namespace()); print("End-to-end demo completed."); return 0
```

**Trigger:** Any of these, independently:
- A new team follows `README.md`'s own "Quick start" (`make verify` then `make demo`) on a checkout that already has real accumulated `loop.*`/`agent.action` history.
- An agent or developer runs the *documented, canonical* command from the README's "Daily workflow" step 8 — `python scripts/ados.py loop verify --ticket TICKET-001` — with no `--dry-run` flag (the default). `LoopManager.verify()` (governance.py:154-159) shells out via `subprocess.run(command, shell=True, ...)` for every string in the ticket's own `## Verification` section. Both real tickets in this repo list `` `make demo` `` there. So the *standard, documented way* to verify TICKET-001 or TICKET-002 for real executes `make demo` mid-verification, deleting `observability/events/loops.jsonl` — including the `verification.started` event `verify()` had just appended one line earlier (governance.py:151) — and replaces it with 5 fabricated demo events, then overwrites `docs/metrics/latest.md` and `observability/reports/dashboard.html` with numbers derived from the fake run.

**Expected vs actual:** Expected: verifying a ticket or running the quick-start demo proves the tooling works without touching unrelated project history. Actual: it unconditionally `unlink()`s the one place all loop/audit history lives, with no confirmation, no backup, and (per `.gitignore:8`) no git history to recover from.

**Root-cause hypothesis:** `demo()` was written assuming it only ever runs against an empty/throwaway checkout, and nobody threaded that assumption through to "this is also a listed Verification command on real tickets."

**Fix sketch:** Make `demo()` refuse to run (or write to a separate `observability/events/demo.jsonl`) when the real event file already contains non-demo events; alternatively require `--force` to wipe. Remove `make demo` from any ticket's real `## Verification` list — it's a showcase command, not a per-ticket check.

**Effort:** S

---

### 2. Sensitive free-text fields bypass redaction entirely — even the one path that redacts only checks key names
**Severity:** S1 (security / policy violation) · **Confidence:** likely

**Location:** `src/agentic_os/telemetry.py:25-33` (`_sanitize`), `src/agentic_os/governance.py:56-62` (`grant_approval`, writes `reason` raw), `scripts/ados.py:68-74` (`trace_status`, writes `completion_note` raw), `scripts/ados.py:77-80` (`approve` CLI exposes free-text `--reason`), `agent/policies/data-handling.md:3,5`, `CONTRIBUTING.md:16`, `agent/harness/run_loop.md:20`, `.github/workflows/governance.yml:33-41` (uploads `observability/events/loops.jsonl` as a CI artifact on every run)

```python
def _sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: "[REDACTED]" if SENSITIVE.search(key) else _sanitize(item) for key, item in value.items()}
    ...
    return value  # <- a plain string value is NEVER scanned for its content
```

This project's own policy is explicit: *"Never place secrets, credentials, tokens, personal data, or production payloads in prompts, events, fixtures, or findings"* and *"Redact sensitive tool output before persistence"* (`agent/policies/data-handling.md:3,5`); `CONTRIBUTING.md:16` repeats it. The implementation only half-delivers:
- `_sanitize` redacts a dict value **only if its key name** matches `token|secret|password|credential|authorization` (telemetry.py:25,30). A free-text string value — e.g. `metadata={"reason": "used prod token sk-live-... to repro"}` — is returned unchanged (line 33): the key `"reason"` doesn't match, so the content is never scanned.
- Worse, two real write paths never call `_sanitize`/`validate_event` at all: `grant_approval()` writes the human-supplied `reason` straight into `agent/approvals/<ticket>.json` via `write_json` (governance.py:59,61), and `trace_status()` writes the human-supplied `--completion-note` straight into the tracked, committed `docs/trace/traceability.json` (ados.py:72-73). Neither is gitignored, so anything pasted there is permanent, committed, plaintext.

**Trigger:** `python scripts/ados.py approve --ticket TICKET-005 --approver alice --reason "confirmed against prod using secret_key=sk-XXXX" ...` — commits the secret straight into `agent/approvals/TICKET-005.json`. Or: `python scripts/ados.py trace-status --requirement PRD-003-R02 --status Done --completion-note "fixed by rotating AWS_SECRET_ACCESS_KEY=..." ` — commits it into `docs/trace/traceability.json`. Both are exactly the kind of "explain what happened" free-text field a rushed human or agent fills in.

**Expected vs actual:** Expected (per the project's own stated policy): sensitive content is redacted before persistence. Actual: redaction is key-name-only and only wired into one of three persistence paths.

**Root-cause hypothesis:** `_sanitize` was built to satisfy `test_sensitive_metadata_is_redacted` (telemetry.py's own test, which only exercises the key-based case), and was never applied to the `governance.py`/`ados.py` write paths that bypass the event system entirely.

**Fix sketch:** Extend `_sanitize` to regex-scan string values for the `SENSITIVE` pattern (or an obvious secret shape like `sk-`, `ghp_`, etc.) and redact matches, then route `reason`/`completion_note`/free-text CLI fields through it before any `write_json` call.

**Effort:** M

---

### 3. Staleness audit is silently defeated by every fresh CI checkout — the weekly job has likely never worked
**Severity:** S2 · **Confidence:** certain

**Location:** `src/agentic_os/validation.py:107-112` (`stale_artifacts`), `.github/workflows/governance.yml:42-49` (`maintenance-audit` job, `actions/checkout@v4` + `make audit`), `Makefile:33-34`, `tests/test_governance.py:29-32`

```python
def stale_artifacts(root:Path,days:int|None=None)->list[str]:
    days=days or load_config(root)["stale_after_days"]; now=datetime.now(timezone.utc).timestamp(); stale=[]
    for pattern in ("docs/prd/PRD-*.md","docs/specs/SPEC-*.md","docs/tickets/TICKET-*.md"):
        for path in root.glob(pattern):
            if (now-path.stat().st_mtime)/86400>days: stale.append(...)
```

**Trigger:** The `maintenance-audit` job runs weekly (`cron: "17 6 * * 1"`) and does a fresh `actions/checkout@v4` every time, then `make audit` → `ados.py audit-stale` → this function. Git does not preserve original authorship/commit mtimes on checkout — every file's `st_mtime` becomes "now" (checkout time). So `(now - path.stat().st_mtime)` is always ~0 seconds, never `> 90 days`, no matter how old the PRD/spec/ticket actually is by `git log`. The test suite's own `test_archive_and_stale_audit` (test_governance.py:32) has to manually call `os.utime(prd,(1,1))` to force an old mtime to exercise the "stale" branch at all — which is the tell: nothing in the *real* deployment path (a fresh git checkout) can ever naturally produce an old mtime.

**Expected vs actual:** Expected: a weekly job that flags PRDs/specs/tickets nobody has touched in 90+ days. Actual: it can never fire — `make audit` will print "No stale active artifacts" on every scheduled run forever, regardless of true staleness.

**Root-cause hypothesis:** Filesystem mtime was used as a proxy for "last touched," which is only valid for local, uncloned working copies — it silently breaks the moment the check runs in CI, which is the only place it's actually scheduled to run.

**Fix sketch:** Use `git log -1 --format=%ct -- <path>` (last commit time) instead of `st_mtime`, falling back to mtime only for uncommitted files.

**Effort:** M

---

### 4. `approval_valid` crashes on a plain expiry date — blocks the R2/R3 CI gate with a raw traceback
**Severity:** S2 · **Confidence:** certain

**Location:** `src/agentic_os/governance.py:65-74` (`approval_valid`, esp. line 74), `scripts/ados.py:171` (`--expires-at`, plain string, no format validation or example), `ci/validate_pr_scope.py:20` (CI calls `approval_valid` for R2/R3)

```python
expires = record.get("expires_at")
return not expires or datetime.fromisoformat(expires) > datetime.now(timezone.utc)
```

**Trigger:** `python scripts/ados.py approve --ticket TICKET-009 --approver alice --reason "ok" --expires-at 2026-08-01` (or any ISO string without a UTC offset, e.g. `2026-08-01T00:00:00`). `--expires-at` is undocumented beyond its flag name — nothing hints that an offset is required — so a plain date is the natural thing to type. `datetime.fromisoformat("2026-08-01")` returns a **naive** datetime; comparing it to `datetime.now(timezone.utc)` (aware) raises `TypeError: can't compare offset-naive and offset-aware datetimes`. This isn't caught anywhere, so it propagates out of `approval_valid` → `LoopManager.start()` and, separately, out of `ci/validate_pr_scope.py`, which calls `approval_valid` directly at PR time for any R2/R3-risk ticket.

**Expected vs actual:** Expected: an approval past its expiry is reported "invalid" cleanly; one that's still valid says so. Actual: the *entire governance CI gate crashes* with an unhandled exception for any R2/R3 PR whose approval used an offset-less expiry — blocking merge until someone figures out the undocumented format requirement.

**Root-cause hypothesis:** No validation or normalization of `expires_at` at grant time; `approval_valid` assumes every stored value round-trips into an aware datetime.

**Fix sketch:** In `grant_approval`, parse and normalize `expires_at` to a UTC-aware ISO string at write time (reject or coerce naive input with a clear `ValueError`); in `approval_valid`, guard the comparison (`datetime.fromisoformat(expires).astimezone(timezone.utc)`).

**Effort:** S

---

### 5. Master-compliance ledger accepts orphaned, never-executed files as proof of "Complete"
**Severity:** S2 · **Confidence:** certain

**Location:** `src/agentic_os/validation.py:88-99` (`validate_compliance`, esp. lines 96-97), `docs/trace/master-compliance.json:19` (MASTER-016), `:23` (MASTER-020)

```python
for ref in record.get("implementation_refs",[]):
    if not (root/ref).exists(): issues.append(Issue("MASTER_REF",f"missing {ref}",...))
```

**Trigger:** none needed — this is already true today, not a future risk. `MASTER-016` ("Loop blast radius is limited") cites `ci/check_changed_scope.py` as evidence, and `MASTER-020` ("Named harness files and CI guard manifest exist") cites `ci/agent-guards.yml`. I grepped both filenames across the whole repo: `ci/check_changed_scope.py` is referenced **nowhere** except this JSON record — not the Makefile, not `.github/workflows/governance.yml`, not any script. It's a second, independently-written reimplementation of `governance.check_scope`/`ci/validate_pr_scope.py` that nothing ever calls. `ci/agent-guards.yml` is likewise referenced only by this same JSON record — it's a static list of gate names, never parsed by any code. `validate_compliance` only checks that the *file exists on disk*, never that anything actually imports, runs, or parses it.

**Expected vs actual:** Expected: "Complete" in the compliance ledger means the cited implementation actually does the job. Actual: it can mean "a file with a plausible name sits in the repo," which is true for at least two of the ledger's ~100 records right now.

**Root-cause hypothesis:** The compliance check was built to catch typos/missing-file drift, not to verify reachability — an easy trap in any ledger built from `implementation_refs` path strings.

**Fix sketch:** Either wire `ci/check_changed_scope.py` and `ci/agent-guards.yml` into real enforcement (or delete them and repoint the records at what's actually running: `ci/validate_pr_scope.py` + `governance.py`), and/or extend `validate_compliance` to flag `implementation_refs` that are never imported/invoked by anything (at minimum, exclude `ci/*.py` files that no workflow/Makefile target names).

**Effort:** M

---

### 6. "Validated bet" status leaks across documents via full-text ID scanning
**Severity:** S2 · **Confidence:** likely

**Location:** `src/agentic_os/product.py:98-101` (builds `validated`), `:105` (gates on it), `tests/test_product.py:27-30` (only tests the single-bet-status-flip case, not cross-contamination)

```python
validated=set()
for path in (root/".ai/bets").glob("BET-*.md"):
    text=_text(path); identifiers=_ids(BET,text)          # <- every BET-XXX anywhere in the file
    if section(text,"Status")=="Validated": validated.update(identifiers)
...
if not _ids(BET,section(text,"Parent Bet"))<=validated: issues.append(f"{path...} must link a validated bet")
```

**Trigger:** `validated` is built by scanning a bet document's **entire text** for any `BET-\d{3,}` match, not just its own declared ID. The moment a *second* bet exists and its prose naturally references the first — e.g. `BET-001`'s notes say "supersedes BET-002" or "see also BET-002" (completely ordinary cross-referencing language) — and `BET-001` is `Status: Validated`, then `BET-002` gets added to `validated` too, even if `BET-002` itself is still `Proposed` or was killed. Any PRD whose `## Parent Bet` section then names `BET-002` sails through the "must link a validated bet" gate (product.py:105) that's supposed to be this system's core safety property (per `BET-001`'s own hypothesis: *"delivery work cannot start without evidenced upstream links"*). Only one bet file exists today, so this hasn't fired yet — but it will the moment anyone writes a second bet document the way people naturally write them.

**Expected vs actual:** Expected: a bet is "validated" only by its own Status field. Actual: any validated bet's free-text prose can vouch for an unrelated, unvalidated bet ID.

**Root-cause hypothesis:** `_ids(BET, text)` (a generic "find all matching IDs in this text" helper used correctly elsewhere for corpus-wide inventories) was reused here where the scope needed to be "this document's own ID," not "everything this document happens to mention."

**Fix sketch:** Scope `identifiers` to the bet's own declared ID (parse it from the filename or the `# BET-NNN:` H1) instead of scanning the whole body.

**Effort:** S

---

### 7. NaN/Infinity `--cost-usd` permanently corrupts the cumulative cost metric and can never alert
**Severity:** S2 · **Confidence:** certain

**Location:** `src/agentic_os/telemetry.py:58-60` (non-negative check), `scripts/ados.py:172` (`--cost-usd`, `type=float`), `src/agentic_os/metrics.py:20,33` (`total_cost`, `cost_per_successful_task`)

```python
for key in ("duration_ms", "retry_count", "cost_usd", ...):
    if key in event and (not isinstance(event[key], (int, float)) or event[key] < 0):
        raise ValueError(f"{key} must be non-negative")
```

**Trigger:** `python scripts/ados.py loop stop --ticket TICKET-005 --actor a --outcome success --cost-usd nan` (or `inf`). Argparse's `type=float` happily parses both (`float("nan")`, `float("inf")` are valid Python floats). Neither fails the check above: `nan < 0` and `inf < 0` are both `False` in IEEE-754, so both are accepted as "non-negative" and appended to the permanent event log. `metrics.summarize()` then does `total_cost = sum(float(e.get("cost_usd", 0)) for e in stopped_events)` (metrics.py:20) over **every** stopped run ever recorded — one `nan` poisons the sum for all time (`nan` propagates through addition), and `cost_per_successful_task` (metrics.py:33) reports `nan` forever after. An `inf` value similarly makes every future report show `inf`. Since NaN/Inf comparisons are always `False`, a poisoned metric can also never breach a `metric_thresholds` alert again (`evaluate_alerts`, metrics.py:44-53).

**Expected vs actual:** Expected: cost tracking rejects garbage input. Actual: one bad flag value (a typo, a buggy cost-calculator upstream that divides by zero and passes through `inf`) permanently corrupts an aggregate metric derived from an append-only log, with no repair mechanism.

**Root-cause hypothesis:** The non-negative check assumes "not negative" implies "valid number," which is false for NaN/Infinity.

**Fix sketch:** In `validate_event`, additionally require `math.isfinite(event[key])` for these numeric fields.

**Effort:** S

---

### 8. `LoopManager`'s active-run state has no locking — concurrent invocations race
**Severity:** S2 · **Confidence:** likely (defect is certain; real-world hit-rate depends on how often loops run concurrently)

**Location:** `src/agentic_os/governance.py:94-98` (`_state`/`_save`), `:114-120` (`start()`'s "only one loop active" check), `src/agentic_os/config.py:16-18` (`write_json`, plain truncating write, no lock)

```python
def _state(self) -> dict[str, Any]:
    return load_json(self.state_path) if self.state_path.exists() else {}
def _save(self, state: dict[str, Any]) -> None:
    write_json(self.state_path, state)
...
state = self._state()
if state:
    raise ValueError("only one loop may be active in this checkout")
...
self._save(state)
```

**Trigger:** Two `ados.py loop ...` invocations running close together against the same checkout (two agent processes, or a human and an agent, or two CI jobs sharing a workspace) — e.g. both call `loop start` within the same read-modify-write window. Both read `active-runs.json` before either writes; both see `{}`; both pass the "only one loop may be active" guard; both write, and whichever writes last silently clobbers the other's state. The same race applies to `action()`/`retry()`/`stop()` on an already-active loop: two concurrent `retry()` calls can both read `retries: 2`, both compute `3`, both write `3` — one increment is lost with no error raised anywhere.

**Expected vs actual:** Expected: "only one loop may be active in this checkout" is a hard invariant. Actual: it's enforced with a non-atomic read-then-write and no file lock, so it can be violated under real concurrency, and other state mutations (retry counts, verification results) can silently lose updates the same way.

**Root-cause hypothesis:** State is a single JSON file updated via unconditional overwrite; the code was written for a single sequential CLI user, but the system is explicitly designed for multi-agent use.

**Fix sketch:** Wrap the read-modify-write in an OS file lock (`fcntl.flock` on a sidecar lockfile) or use an atomic write-temp-then-`os.replace` combined with an exclusive-create lock.

**Effort:** M

---

### 9. Architecture/dependency-boundary checker is blind to relative imports
**Severity:** S3 (dormant today; would silently defeat the check after a natural refactor) · **Confidence:** certain (defect), worth-verifying (real-world impact, since it's dormant)

**Location:** `src/agentic_os/architecture.py:49-56`, esp. line 50

```python
names += [node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
```

**Trigger:** This only inspects `ast.ImportFrom.module` and discards `.level` (the leading-dot count). For a relative import like `from .governance import section` (used throughout `src/agentic_os/*.py`, e.g. `product.py:11`, `validation.py:9-14`), `node.module` is `"governance"` — with no package qualifier. Matching against `local_import_roots` (`architecture.json:20-23`, prefixes `"agentic_os"`/`"scripts"`) never succeeds for a bare `"governance"`, so **every relative import in this codebase is invisible to the checker**. It's harmless today only because `src/agentic_os` is registered as one undivided module — same-module imports wouldn't violate the graph even if seen. The moment this package is split into declared sub-modules (a natural next step for a system whose own README advertises "multiple bounded features, modules, and loops"), a relative import crossing that new boundary would pass `validate_architecture` with zero detection, even though the exact same import written in absolute form (`from agentic_os.other_module import x`) would be correctly caught.

**Expected vs actual:** Expected: "Circular dependencies are rejected" / "Cross-layer imports are rejected" (MASTER-023/024) for any import style. Actual: only absolute imports are checked; relative imports (the idiomatic Python style, and the only style this package currently uses internally) are never inspected.

**Root-cause hypothesis:** The AST walk was written and tested against absolute imports only; relative-import resolution (reconstructing the fully-qualified target from `level` + the importing file's own package path) was never implemented.

**Fix sketch:** When `node.level > 0`, resolve the target module by walking up `level` package segments from the importing file's own module path before matching against `local_import_roots`.

**Effort:** M

---

### 10. `ados.py new <kind> --title "..."` crashes on titles containing "/"
**Severity:** S3 · **Confidence:** certain

**Location:** `scripts/ados.py:32-37` (`new_artifact`), esp. line 34 (no sanitization) and line 37 (`write_text`, no parent `mkdir`)

```python
template,directory=mapping[args.kind]; target=ROOT/directory/f"{args.id}-{args.title.lower().replace(' ','-')}.md"
if target.exists(): raise ValueError("artifact already exists")
text=(ROOT/template).read_text(...)...
target.write_text(text,encoding="utf-8")
```

**Trigger:** `python scripts/ados.py new ticket --id TICKET-030 --title "Fix API/CLI parity bug"` — an entirely ordinary title. `args.title` is interpolated directly into a path string with no check for `/` (or `..`). `Path`'s `/` operator treats the embedded slash as a real path separator, so the target becomes `docs/tickets/TICKET-030-fix-api/cli-parity-bug.md` — a file inside a subdirectory `TICKET-030-fix-api/` that doesn't exist. `write_text()` doesn't create parent directories, so this raises an unhandled `FileNotFoundError`. (If such a subdirectory happened to already exist for unrelated reasons, the artifact would instead be silently written somewhere `docs/tickets/TICKET-*.md`-style globs never look, making it invisible to every validator in this repo.)

**Expected vs actual:** Expected: any reasonable human-typed title produces a valid ticket/PRD/spec file. Actual: any title containing a slash crashes the command.

**Root-cause hypothesis:** No path-safety validation on user-supplied `--title` before using it to build a filesystem path.

**Fix sketch:** Reject or replace path separators (and leading dots) in `args.title` before building `target`, and assert the resolved path's parent equals `directory`.

**Effort:** S

## Verification plan

Fastest way to confirm each item (all doable in a scratch clone; none require touching this session's sandbox):

1. **demo() wipe:** `make demo`, inspect `observability/events/loops.jsonl`, run `make demo` again after manually appending a fake real event — watch it disappear.
2. **Secrets bypass:** `python scripts/ados.py approve --ticket TICKET-001 --approver x --reason "token=sk-test-123" ...` then `cat agent/approvals/TICKET-001.json` — the string is there verbatim.
3. **Stale-audit defeat:** fresh `git clone` into a new directory, immediately `python scripts/ados.py audit-stale` — compare against `git log -1 --format=%ci -- docs/prd/PRD-001-agentic-development-os.md` to see the real (irrelevant-to-mtime) age.
4. **approval_valid crash:** in a scratch copy, `grant_approval(root, "TICKET-001", "me", "test", "2026-08-01")` then `approval_valid(root, "TICKET-001")` — observe the `TypeError`.
5. **Dead implementation_refs:** `grep -rn "check_changed_scope\|agent-guards.yml" Makefile .github/ ci/*.py scripts/` — zero hits outside the JSON ledger.
6. **Validated-bet leak:** add a minimal `BET-002.md` (`Status: Proposed`), add a line to `BET-001.md` mentioning "BET-002", run `validate_product(root)` — no issue is raised for a PRD claiming `Parent Bet: BET-002`.
7. **NaN cost:** in a scratch copy with an active loop, `loop stop --cost-usd nan`, then `python scripts/ados.py metrics` and grep `docs/metrics/latest.md` for `nan`.
8. **LoopManager race:** launch two `loop start` calls back-to-back with a tiny injected delay between read and write (or just hammer it in a loop from two shells) and check whether `active-runs.json` ever ends up missing an expected key.
9. **Relative-import blind spot:** temporarily add `local_import_roots` entries that split `src/agentic_os` into two fake modules with a disallowed relative import between them — `validate_architecture` reports no issue.
10. **Title crash:** `python scripts/ados.py new ticket --id TICKET-099 --title "A/B test"` — unhandled `FileNotFoundError`.

## Top 3 to fix first

1. **#1 — `demo()` wipes the event log.** Certain, S1, zero-effort trigger (it's the documented verification step on real tickets), unrecoverable. Fix is small (guard + separate demo path).
2. **#2 — Redaction only covers key names, and two write paths skip it entirely.** S1, directly contradicts this project's own written data-handling policy, and the affected files (`agent/approvals/*.json`, `docs/trace/traceability.json`) are committed to git, not gitignored — leaked secrets there are permanent.
3. **#3 — Staleness audit is dead on arrival in its only real execution context.** It's a scheduled, "green forever" job that gives false confidence about artifact hygiene from week one; nobody will notice it's broken because it never has anything to say.

Close runner-up: **#4** (`approval_valid` crash) — it's certain, cheap to fix, and actively blocks merges on exactly the high-risk (R2/R3) work this system's approval gate exists to protect.
