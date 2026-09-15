# Venture workflow v1 — synthetic agent trial

**Simulation only: no real market claims.** Start with [trial-results.md](trial-results.md)
and [reports/INDEX.md](reports/INDEX.md). The source packet and captured instructions
are in sources/. The complete original transition/check/action logs, recovery script,
and the report-quality repair trail are preserved in trial-audit.tar.gz.

Copied from the original disposable trial; report and source bytes are unchanged.
Absolute file URLs record where sources were accessed during the trial. The same
source bytes are retained under sources/; the original /tmp path need not survive.
For a relocated recovery check, resolve source URLs by basename against sources/
and verify their hashes, rather than silently treating old absolute paths as live.
Report dependencies remain relative and can be checked directly:

```sh
python3 workflows/venture_check.py evals/results/venture-workflow-v1 --final
```

The checker checks structural state, not the source packet's truth. A Niche-report
content omission passed structural checks and was caught by report review; the
archived repair preserves originals and revalidates all affected downstream reports.
A small conductor instruction was added after the captured trial to forbid deferring
required content to later reports. Captured instructions remain immutable evidence.
