# Contributing

The fastest way to contribute is a new brief or a sharper version of an
existing one.

1. Create `prompts/<family>/NN-slug.md` — front matter + body (see README).
2. Keep the 4-phase skeleton: Explore → Audit → Curate → Report.
3. Keep the body under 4,000 characters. `python3 build.py` enforces this.
4. Run `python3 build.py` and commit the regenerated files — CI fails on drift.

Brief-writing bar: every lens must be checkable against a real repo, every
report section must have a defined shape, and the brief must end by asking
before changing anything. Generic advice that fits any codebase gets cut.
