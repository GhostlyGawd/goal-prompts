# Brief Forge — draft a linter-passing brief with your agent

The fastest way to author a new goal-prompts brief is to let your coding
agent draft it against the real gate. Copy the prompt below, paste it into
your agent **inside a clone of this repo**, and it will write the brief,
run the linter, and iterate until the build is green — then stop and show
you the diff. The linter (`build.py`) is the moderation story: a draft
either clears the published bar or it doesn't build.

Every rule the prompt states is the *live* rule — sourced from `build.py`'s
linter and pinned by `tests/test_build.py` (a unit test fails if this
document drifts from the real limits).

## The prompt

Copy everything in the block below.

```text
You are working inside a clone of the goal-prompts repo. Mission: author ONE
new audit brief that passes `python3 build.py` — the repo's linter and build
— on the first green run, iterating until it does.

The brief I want: <DESCRIBE THE AUDIT HERE — what it inspects, for whom, and
what a great finding looks like. One or two sentences.>

## Step 1 — Study the house style (do not skip)
Read these two exemplar briefs end to end; your draft must feel like a
sibling, not a cousin:
- prompts/quality/01-bug-hunt.md (a code-facing audit)
- prompts/venture/62-pain-demand-mining.md (a web-research audit)
Also read CONTRIBUTING.md — especially the report-format grammar the Report
Studio parses.

## Step 2 — Write prompts/<family>/<id>-<slug>.md
Front matter (all six required; the linter fails the build on any miss):
- id: "NN" — 2–3 digits, zero-padded, QUOTED, unused by any existing brief,
  and it must prefix the filename (prompts/<family>/NN-slug.md).
- title: short, concrete.
- family: an EXISTING family from FAMILY_ORDER in build.py (see the README
  Families table); question: copy the family's question verbatim from a
  sibling brief's front matter.
- output: an ALL-CAPS report filename matching [A-Z0-9-]+.md — unique across
  the whole catalog (no two briefs may write the same file), and never a
  reserved community filename (README.md, SECURITY.md, CHANGELOG.md,
  CONTRIBUTING.md, CODE_OF_CONDUCT.md, SUPPORT.md, GOVERNANCE.md, LICENSE.md).
- tagline: one card-ready line, max 170 characters, no double quotes.
- Do NOT add an `example:` field (it must point at a real file in the repo).
  `related:` is optional — only existing brief ids, never the brief's own.

Body (the linter greps for these literally):
- Total body under 4,000 characters. Aim for ~3,300 so future edits fit.
- Start with `# Goal: <title>`, then "You are working inside this repo.
  Mission: …" — one tight paragraph of scope.
- Exactly four phase headers: `## Phase 1 — Explore`, `## Phase 2 — …`,
  `## Phase 3 — Curate`, `## Phase 4 — Report` (Explore → Audit → Curate →
  Report is the house arc).
- Phase 2 audits through 4–12 numbered lenses, each shaped
  `N. **Lens Name** — what to check, concretely`. Every lens must be
  checkable against a real repo; generic advice that fits any codebase
  gets cut in review.
- Phase 4 must name the report literally, on one line, as:
  Create `<OUTPUT>.md` at repo root — the exact phrase "at repo root" is
  linted — followed by numbered bold sections (same `N. **Name** —` shape
  as the lenses). Findings should open with a **bold title** and may carry
  severity (S1/S2/S3/low), `effort S|M|L`, `impact L|M|H` — that grammar is
  what the Report Studio parses.
- Phase 4 must handle re-runs with the dated line: "Start the report with
  today's date. If `<OUTPUT>.md` already exists from a previous run, read it
  first and lead with what changed since."
- A `## Rules` section whose bullets include, verbatim:
  - "If a `reports/` directory exists at the repo root, write the report
    there instead of the root."
  - a null-report escape naming the brief's surface, e.g. "No <surface> in
    this repo? Say so in a one-paragraph null report and stop — a null
    result is a valid finding." (Only universal-subject briefs on build.py's
    NULL_REPORT_EXEMPT list may omit this — default to including it.)
  - the ask-first gate as the LAST line: "Report only — end by asking which
    fixes to make" (the literal phrase "Report only — end by asking" is
    linted; the brief must be read-only, its only write the report file).

## Step 3 — Iterate until green
1. Run `python3 build.py`. Read every FAIL/LINT line for your brief.
2. Fix the draft. Re-run. Repeat until the build exits clean.
3. Two expected non-brief failures, and their fixes:
   - the missing share card: run `python3 scripts/og.py` (needs Pillow) to
     generate og/<id>.png for the new brief;
   - the README count guard: update the "<N> mission briefs" intro line in
     README.md to the new total.
4. Finish with `scripts/check` if Node is available (prompt-only changes
   pass with Python alone).

## Step 4 — Stop and show your work
Show me the new file and the diff of everything the build regenerated.
Do NOT commit, and do not touch any other brief. I review content; the
linter only guarantees structure.
```

## Why this exists

`build.py` machine-enforces structure — the 4-phase skeleton, the ask-first
gate, the < 4,000-character cap, unique report filenames — but a blank file
plus ten house rules is a cold start. The Forge turns your agent into the
drafting half of the pipeline while the linter and human PR review stay the
gates: a wrong draft costs review time, never catalog quality. (Design:
AI-IDEAS.md, idea 1.)

Contributions land as pull requests — see
[CONTRIBUTING.md](../CONTRIBUTING.md) for the full bar, and the site's
[/quality](https://goal-prompts.vercel.app/quality) page for why the bar
exists.
