# Contributing

The fastest way to contribute is a new brief or a sharper version of an
existing one. (Working on the repo's own tooling instead? The agent entry
point is `CLAUDE.md` — commands, layout taxonomy, conventions.)

1. Create `prompts/<family>/NN-slug.md` — front matter + body (see README).
2. Keep the 4-phase skeleton: Explore → Audit → Curate → Report.
3. Keep the body under 4,000 characters. `python3 build.py` enforces this.
4. A new brief needs a share card and the README count bump — both are hard
   build gates: `python3 scripts/og.py <id>` writes `og/<id>.png` (needs
   `pip3 install Pillow fonttools brotli` — the only step the stdlib-only
   build outsources), and README's "<N> mission briefs" line must match the
   new catalog size.
5. Run `scripts/check` and commit the regenerated files — CI fails on drift.

Don't want to start from a blank file? Use the **Brief Forge**
([docs/brief-forge.md](docs/brief-forge.md)) — a copyable meta-prompt that
has your agent draft the brief and iterate against the real linter until
the build is green.

## One command

`scripts/check` is the whole gate: it builds (linting every brief),
runs the linter's own tests, syntax-checks the MCP server and the site
scripts, and runs the MCP smoke test. If it passes locally, the Vercel
deploy and CI will pass too. Node is needed only for the `mcp/` and
site-script steps — a prompt-only change passes with Python alone, and
`scripts/check` skips the Node steps loudly when Node is absent.

Brief-writing bar: every lens must be checkable against a real repo, every
report section must have a defined shape, and the brief must end by asking
before changing anything. Generic advice that fits any codebase gets cut.

## The brief contract (linted)

`build.py` fails the build unless every brief carries these, so write them
in from the start:

- **id format**: front-matter `id` is 2–3 digits (`"07"`, `"140"`) and must
  match the filename prefix (`prompts/<family>/07-….md`).
- **unique, non-reserved output**: no two briefs may write the same report
  file, and `output:` may not shadow a community file (`README.md`,
  `SECURITY.md`, `CHANGELOG.md`, …).
- **dated re-run line**: Phase 4 tells the agent to date the report and, if
  it *already exists* from a previous run, to read it first and lead with
  what changed.
- **reports/ bullet**: Rules include "If a `reports/` directory exists at
  the repo root, write the report there instead of the root."
- **null report**: unless the brief's subject is universal (the exemption
  list lives in `build.py`), Rules name its surface and allow a
  one-paragraph null report when the repo simply doesn't have one.

## Optional `related:` front matter

A brief may list ids that pair well with it (`related: 46 28`); they
render as cross-links on its `/b/<id>` page. Every id must exist and differ
from the brief's own — linted.

## Report format

The reports briefs produce are consumed by machines as well as humans —
the [Report Studio](https://goal-prompts.vercel.app/studio) parses them
into a checklist and `47 · The Fixer` implements them. Keep a new brief's
Phase 4 inside this grammar:

- Phase 4 names its file: `` … `REPORT.md` at repo root `` (linted).
- One finding = one paragraph or list item that opens with a
  `**bold title**`. Prose without a bold lead-in is context, not a finding.
- Signals the parsers recognize inside a finding, case-insensitively:
  severity (`S1`/`critical`, `S2`/`high`, `S3`/`medium`, `low`),
  `effort S|M|L`, `impact L|M|H`, a leading `FIX`/`IMPROVE`/`NEW` tag in
  the title, and `FIXED`/`shipped` on resolved items.
- `## headings` group findings into sections.
