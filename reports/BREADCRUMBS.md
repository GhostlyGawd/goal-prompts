# BREADCRUMBS.md
**2026-07-10** · *Produced by brief 145 · Breadcrumb Audit, run against this repo (goal-prompts, v0.14). Part of the sample-report gallery.*

First run — no previous report to diff against. This run landed immediately after the 0.14.0 breadcrumb pass (CLAUDE.md ↔ README cross-links, the `reports/` taxonomy class, the stated two-hop rule), so the headline gaps that motivated the brief are already closed; what follows is the residue.

## Reachability map
Entry files found: `CLAUDE.md` (agent), `README.md` (human), `CONTRIBUTING.md` (contributor) — all three exist and CLAUDE.md now names the other two; README links back. From CLAUDE.md, hop 1 names every command, every source file, the design layer (`HARNESS_PLAN.md`, `DECISIONS.md`, `FABLE_BUILD_QUEUE.md`, `specs/`, `template/`), the js/ modules with their test suites, and the generated-output list; hop 2 (via `template/README.md`, `HARNESS_PLAN.md`, `README.md`) covers the individual specs, the template harness internals, `docs/usage-metrics.md`, and `.claude-plugin/marketplace.json`. Roughly 95% of the repo's docs, scripts, and tooling are reachable in two hops. The far side — reachable only by directory listing or buried code comment — is six files, itemized below.

## Broken and missing links
- **`vercel.json` is named by no entry doc.** Deployment behavior (buildCommand, cleanUrls, the redirect that keeps old report URLs alive, cache headers) is discoverable only by spotting the file. README documents CI (`.github/workflows/ci.yml`) but not the deploy config beside it.
- **CONTRIBUTING's add-a-brief steps omit two hard build gates.** `build.py` fails without an `og/<id>.png` share card for every brief and fails when README's "<N> mission briefs" count drifts — but CONTRIBUTING step 1 says only "front matter + body (see README)." A contributor learns both rules from build failures, and the failure for the og card doesn't say the fix is `python3 scripts/og.py <id>` (needs Pillow, which the stdlib-only pitch says you don't need). Enforced-but-unwritten, the exact inverse of the house style.
- **CONTRIBUTING doesn't link back to CLAUDE.md** — a contributor who lands there never learns the agent entry point exists. One line closes the loop (CLAUDE.md already points forward).

## Orphans and unclassified files
- **`manifest.json`** — the hand-authored PWA manifest (committed in 0.4, hand-edited since), but it appears in neither of CLAUDE.md's classes. An agent can't tell from the taxonomy whether editing it is safe or futile — the exact ambiguity the two lists exist to remove. Verdict: **classify** (add to "Edit these").
- **`vitals.html`** — a source page like `studio.html`, but absent from "Edit these"; its only CLAUDE.md mention is inside the design-tokens parenthetical. Verdict: **classify**.
- **`examples/index.html`** — the hand-authored report gallery; nothing in CLAUDE.md's taxonomy covers `examples/`, and it points into `reports/` so it must move in step when reports do (this pass proved it). Verdict: **classify**.
- **`metrics.json` + `scripts/refresh-stars.py`** — an out-of-band-refreshed asset and the script that writes it; their only breadcrumb is a comment at `build.py:1294`. Same species as `img/studio.png` (ungated asset with a refresh command), which *does* get a CLAUDE.md note. Verdict: **classify** alongside it.
- **`vercel.json`** — see above. Verdict: **link** from README's develop/CI section.
- **`fonts/`** — self-hosted font assets, unmentioned anywhere; referenced only by generated CSS and the vercel cache header. Deliberately internal rather than lost. Verdict: **flag only**, no action.

## Fixes
1. **Add the four unclassified source surfaces to CLAUDE.md's Layout** — `vitals.html`, `examples/` (gallery, points into `reports/`), `manifest.json`, and a `metrics.json`/`refresh-stars.py` note. Four lines, closes every taxonomy hole. Effort S.
2. **State the two unwritten build gates in CONTRIBUTING's add-a-brief steps** — new brief ⇒ `python3 scripts/og.py <id>` (Pillow needed) and bump README's brief count. Effort S.
3. **One line in README naming `vercel.json`** as the deploy config, beside the existing CI sentence. Effort S.
4. **One backlink line in CONTRIBUTING** to CLAUDE.md. Effort S.

*Report only — which breadcrumbs should be laid first?*
