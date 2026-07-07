# Contributing

The fastest way to contribute is a new brief or a sharper version of an
existing one.

1. Create `prompts/<family>/NN-slug.md` — front matter + body (see README).
2. Keep the 4-phase skeleton: Explore → Audit → Curate → Report.
3. Keep the body under 4,000 characters. `python3 build.py` enforces this.
4. Run `scripts/check` and commit the regenerated files — CI fails on drift.

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
