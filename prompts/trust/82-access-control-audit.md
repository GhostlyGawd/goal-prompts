---
id: "82"
title: Access-Control & Authorization Audit
family: Trust
question: is it safe?
output: ACCESS.md
tagline: Who can do what — whether every sensitive action and record checks the caller's permission, not just that they are logged in.
---
# Goal: Access-Control & Authorization Audit

You are working inside this repo. Mission: judge whether the app enforces authorization — that every sensitive action and record verifies both who the caller is and whether they are allowed, on the server, by default.

Read-only pass. Trace routes, middleware, and data access; run read-only checks; change nothing. Your only write is the report file.

## Phase 1 — Map the access model
- List the roles/permissions the system recognizes and where they are checked.
- Enumerate sensitive resources and actions: records, admin functions, money movement, data export.
- Trace one request end to end: where is identity established, and where is permission decided.

## Phase 2 — Audit through 7 lenses
Cite the route, handler, or query for every finding.
1. **Authn ≠ authz** — logged-in treated as allowed; endpoints behind auth with no permission check
2. **Object-level access (IDOR)** — an id taken from the request and trusted without an ownership check
3. **Function-level access** — admin or privileged actions reachable by ordinary roles
4. **Tenant isolation** — one customer's data reachable from another's session in a multi-tenant app
5. **Server-side enforcement** — checks done only in the UI, bypassable by calling the API directly
6. **Default posture** — new routes and resources default to open rather than deny-by-default
7. **Escalation paths** — role changes, impersonation, or token scopes that let a user climb

## Phase 3 — Curate
- Rank by what a finding unlocks: cross-tenant data or admin access outranks a self-scoped leak.
- For each gap, name the exact check missing and where it belongs in the request path.
- Prefer one enforced choke point over a check sprinkled per handler.

## Phase 4 — Report
Create `ACCESS.md` at repo root:
1. **Access map** — role × resource × action, with where each is enforced
2. **Findings** — each: severity S1–S3 · location · who can reach what · the missing check · fix
3. **Deny-by-default gaps** — resources that should be closed until explicitly opened
4. **Proof cases** — the request each fix should now reject, ready to turn into a test

## Rules
- Identity is not permission; every sensitive path needs both
- Enforce on the server; the client is a convenience, not a control
- Report only — end by asking which authorization gaps to close first
