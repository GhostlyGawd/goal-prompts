---
id: "83"
title: Input & Injection Audit
family: Trust
question: is it safe?
output: INJECTION.md
tagline: Trace untrusted input to dangerous sinks — where attacker-controlled data becomes a query, a command, markup, a request, or a file path.
---
# Goal: Input & Injection Audit

You are working inside this repo. Mission: follow untrusted input from where it enters to where it does something dangerous, and find the places it reaches a sink without being parameterized, escaped, or validated.

Read-only pass. Trace data flow through the code; change nothing. Your only write is the report file.

## Phase 1 — Map sources and sinks
- List untrusted sources: request params, bodies, headers, webhooks, uploads, queue messages, third-party responses.
- List dangerous sinks: the database, the shell, HTML/DOM, outbound requests, the filesystem, template engines.
- Sketch which sources can reach which sinks; those paths are the audit.

## Phase 2 — Audit through 7 lenses
Give the source → sink path and file:line for every finding.
1. **SQL / NoSQL injection** — string-built queries; unparameterized input reaching the database
2. **Command & code injection** — shell-outs, `eval`, and deserialization of untrusted data
3. **Cross-site scripting** — unescaped input rendered to HTML/DOM; unsafe `innerHTML`/`dangerouslySetInnerHTML`
4. **Server-side request forgery** — user-supplied URLs fetched by the server
5. **Path & file handling** — traversal, unrestricted upload type/size, unsafe filenames
6. **Template & expression injection** — user input into template engines or expression evaluators
7. **Validation boundary** — where validation should sit (server) versus where it actually sits (client)

## Phase 3 — Curate
- Rank by reachability × impact: a path an anonymous caller can trigger outranks an admin-only one.
- For each finding, state the fix in the right layer — parameterize, escape at output, allow-list, or sandbox.
- Note systemic causes: one unsafe helper reused everywhere beats fixing call sites one by one.

## Phase 4 — Report
Create `INJECTION.md` at repo root:
1. **Reachability summary** — findings by severity and who can trigger them
2. **Findings** — each: severity S1–S3 · source → sink path · proof of reach · the layer-correct fix
3. **Systemic fixes** — the shared helpers or patterns that would close whole classes at once
4. **Validation strategy** — where trust boundaries should be drawn going forward

## Rules
- Follow the data; a sink is only a bug if untrusted input reaches it
- Fix at the right layer — escaping output beats sanitizing input beats hoping
- Report only — end by asking which injection paths to close first
