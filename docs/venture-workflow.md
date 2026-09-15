# Venture research in a repository

Start with the [Venture conductor](../raw/family-venture.md). It guides the agent
from operator context and candidate selection through evidence gathering to a
go/pivot/kill/insufficient-evidence decision. Individual briefs 60–67 also work
alone; they keep their existing report names and root-or-`reports/` behavior.

The agent explains its research plan and uses authorization already given. You
choose the candidate and wedge unless you delegate those decisions. Research
authorization does not authorize outreach, purchases, publishing or code changes.
Missing evidence can end in a useful next experiment instead of a forced verdict.

## Find and resume a run

Open `reports/INDEX.md`. It identifies the run, selected venture, criteria,
decisions, report list and exact next step. The conductor updates it throughout
the run, including pauses. `reports/venture-run.json` provides structured state.
Both belong to the conductor; each research brief still writes just its report.

To resume, ask your agent to read the index, state, charter, current brief and
listed input reports. It must verify scope and input hashes before continuing.
When a candidate or wedge changes, increment the scope revision and mark dependent
reports stale. Revalidation needs a recorded reason; changing the hash alone does
not establish that old research applies.

Existing root reports can be reviewed and adopted. Existing reports/index/state
must be preserved in git or an agreed archive before replacement. An unrelated
index entry stays intact. Keep one active venture run per report set; concurrent
ventures need separate worktrees or repos. No automatic migration or overwriting.

## Optional local structural check

From this source checkout (Python 3.9+):

```sh
python3 workflows/venture_check.py /path/to/target-repo
python3 workflows/venture_check.py /path/to/target-repo --final
```

The build exports the same script at `/raw/venture_check.py`, and the npm package
includes it under `raw/`. Fetch scripts to a temporary location and inspect them
before execution. Do not pipe a network response into a shell. Offline agents can
check the contract manually; installing a runtime is not required.

The checker is read-only and exits nonzero on structural failures. It checks
manifest fields, safe paths, report metadata and common sections, report/input
hashes, stage order and terminal-state consistency. It does not verify source
truth, decision authority, quotation fidelity, arithmetic or commercial viability.
It does not enforce agent behavior between checks. A passing check means
**structurally consistent**, not “good venture” or “research complete.”

Schema: [venture-run.schema.json](../workflows/venture-run.schema.json). Minimal
preflight example (record real operator context and useful bars for an actual run):

```json
{
  "schema_version": 1,
  "run_id": "venture-2026-09-14-a",
  "status": "active",
  "scope": {"id": "discovery", "revision": 1},
  "operator": {"time": "5 hours/week", "capital": "$100/month"},
  "criteria": [{
    "id": "pain", "threshold": "recurring material cost for the target buyer",
    "evidence": "independent buyer accounts plus observed spending",
    "recorded_at": "2026-09-14", "exposure": "before conclusions"
  }],
  "decisions": [],
  "commit_preference": "no",
  "next_step": "Run Opportunity Scan, then select one candidate",
  "stages": [{
    "brief": "60", "output": "reports/OPPORTUNITIES.md",
    "status": "pending", "inputs": {}, "note": ""
  }]
}
```

Create `reports/INDEX.md` naming the same run ID. For a complete report, add its
SHA-256 and brief provenance; use `inputs` for earlier report paths and their
SHA-256 values. Hash the exact bytes, e.g. `shasum -a 256 reports/OPPORTUNITIES.md`.
All earlier complete/reused Venture reports in the sequence are required inputs;
adopted reports outside the sequence must also be hashed and reviewed.

Reports include a date, title, conductor provenance and exact metadata lines:

```text
Run: venture-2026-09-14-a
Scope: tutor-reminders@2
Brief: 62
Status: complete
```

Use `## Scope`, `## Findings`, `## Evidence`, `## Counterevidence`, `## Next steps`
as well as the brief's content requirements. Findings get stable bold IDs such as
`**V62-001 — Recurring collection work**`. `null` can remain a short explanation
with metadata; it describes a missing research subject, not an unsuccessful search.

States: pending/running → complete or null, or blocked/failed. Reuse becomes
`reused` only after review. Changed scope/inputs makes affected reports `stale`;
unrun stages after a stop become `skipped` with a reason. A paused run cannot have
a running stage. `--final` accepts a complete run (all stages complete/reused) or
a stopped run with every stage disposition recorded; it rejects active/paused runs.

## Implementation and evidence

- [Specification](../specs/VENTURE_WORKFLOW.md) and [task/evidence ledger](../specs/VENTURE_WORKFLOW_TASKS.md).
- [Canonical conductor source](../workflows/venture-conductor.md): the build uses it
  directly, embeds it in browser catalog logic, and puts it in catalog.json for MCP.
- [Synthetic agent trial and review](../evals/results/venture-workflow-v1/README.md):
  captured reports, recovery, review findings and revalidation receipts.
- [Regression scenarios](../tests/test_venture.py): disposable repo validation and
  full/partial/mixed sequence parity. Run through `scripts/check`.

This release adds a Venture-specific research contract. Other families retain
their current behavior. It makes no claim of measured efficacy improvement across
models or live markets without additional trials.
