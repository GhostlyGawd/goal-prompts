# DECISIONS — append-only ADR log

One entry per load-bearing choice. Never rewrite an old entry; supersede it
with a new one. Format: `## ADR-N — title`, then Date / Status / Context /
Decision / Consequences.

## ADR-0001 — Instantiated from the goal-prompts golden-path template

Date: (scaffold date)
Status: accepted
Context: (product name and the go verdict that authorized it — cite
VERDICT.md if the Founder Funnel produced one.)
Decision: This repo uses the goal-prompts golden-path harness unchanged:
Python 3 stdlib + unittest, zero dependencies, `scripts/check` as the single
gate, the harness layer operator-owned. Deviations, if any, are listed here.
Consequences: Every dependency ever added needs its own ADR naming the
package (the spec lint greps this file for it). The harness layer changes
only by operator hand.
