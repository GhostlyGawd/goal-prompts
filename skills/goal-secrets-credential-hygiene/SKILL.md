---
name: goal-secrets-credential-hygiene
description: "Every hardcoded key, token, and password the repo carries — in source, config, and git history — plus how they rotate and who can read them. Audit brief 81 · Trust — runs a four-phase audit of the current repo and writes SECRETS.md at the repo root."
---

# Goal: Secrets & Credential Hygiene

You are working inside this repo. Mission: find every credential the codebase holds or handles — API keys, tokens, passwords, connection strings, private keys — wherever they hide, and judge how they are stored, injected, and rotated.

Read-only pass. Grep the tree and the git history, read config and CI, but change nothing; your only write is the report file. Never print a full live secret — mask all but the last four characters.

## Phase 1 — Map where secrets live
- Inventory every place a secret could enter: env files, config, CI/CD variables, Dockerfiles, k8s manifests, client bundles, test fixtures, seed scripts.
- Note how secrets reach runtime: env vars, a vault, a secrets manager, or hardcoded literals.
- Identify the blast radius: which secrets unlock production data, payments, or third-party spend.

## Phase 2 — Audit through 7 lenses
Cite file and line for every finding; mask the value.
1. **Hardcoded in source** — keys, tokens, passwords, or private keys committed as literals
2. **Buried in git history** — secrets gone from HEAD but still reachable in old commits or tags
3. **Leaked to the client** — anything secret shipped in a frontend bundle, mobile app, or public asset
4. **Weak storage** — plaintext `.env` in the image, world-readable config, secrets in logs or traces
5. **No rotation path** — credentials with no way to rotate and no expiry
6. **Over-broad scope** — one god-key where a scoped, least-privilege credential would do
7. **Unsafe handling** — secrets on the command line, interpolated into URLs, or cached where they persist

## Phase 3 — Curate
- Rank by blast radius × exposure: a production payments key in the client bundle outranks a dev token in a test.
- For each live exposure, state whether it must rotate now — assume anything ever committed is compromised.
- Separate "exposed today" from "fragile process"; both matter, but only one is on fire.

## Phase 4 — Report
Create `SECRETS.md` at repo root:
1. **Exposure summary** — count by severity, and the must-rotate-now list up top
2. **Findings** — each: severity S1–S3 · location (file:line or commit) · masked value · blast radius · fix
3. **Rotation & storage plan** — where these secrets should live instead, and how they should reach runtime
4. **Prevention** — the pre-commit hook, scanner, or ignore rule that stops the next leak

Start the report with today's date. If `SECRETS.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Mask every value; a report that leaks a secret is the vulnerability
- Assume anything ever committed is compromised and must rotate
- No credentials, keys, or secrets in play in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which exposures to rotate and remediate first
