# Security policy

Goal Prompts is a static site plus three small local surfaces: the briefs
themselves (markdown your agent runs), a zero-dependency MCP server
(`mcp/server.cjs`), and a shell installer (`install`). There is no backend,
no account system, and no data path: briefs run in *your* agent on *your*
machine, and the Report Studio parses reports entirely in the browser tab.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting on this repository
(**Security → Report a vulnerability**), or open an issue if the problem
isn't sensitive. Reports get a reply as fast as a solo maintainer can
manage — typically within a few days.

In scope, roughly in order of how seriously it would be taken:

- Anything that makes a brief, conductor, or installed command do more than
  its stated contract (audit briefs are read-only and end by asking; the
  Fixer-pattern briefs gate edits behind an explicit selection).
- The installer (`install`) and its checksum verification.
- The MCP server (`mcp/server.cjs`).
- XSS or content injection on any generated page (the Studio and Vitals
  parse user-supplied report files — findings there are very welcome).
- A dependency or supply-chain path we claim not to have.

## What to expect from the artifacts

Every brief is plain markdown you can read in five minutes — do that before
running anything, here or anywhere. The build enforces the house rules
(read-only phases, the ask-first gate, size caps) as failing exit codes, and
`reports/SECURITY-AUDIT.md` is this repo's own security audit, run with the
catalog's security brief and committed unedited.
