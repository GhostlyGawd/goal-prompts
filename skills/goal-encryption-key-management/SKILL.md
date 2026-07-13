---
name: goal-encryption-key-management
description: "How the product protects data with encryption — in transit, at rest, and at the field level — and whether the keys that unlock it are managed safely. Goal Prompt 127 · Compliance — inspects the current repo and writes ENCRYPTION.md at the repo root."
---

# Goal: Encryption & Key Management

You are working inside this repo. Mission: judge how the product protects sensitive data with encryption and how it manages the keys — because encryption with badly handled keys is a lock with the key taped to the door.

Read-only pass. Read the transport config, storage setup, crypto usage, and key handling; change nothing but the report file. Never print a key.

## Phase 1 — Follow the sensitive data
- Identify the sensitive data: credentials, PII, tokens, payment data.
- Trace it in transit and at rest: what protects it on the wire and in storage.
- Find where cryptographic keys and secrets live and who can reach them.

## Phase 2 — Audit through 7 lenses
1. **In transit** — TLS everywhere, modern versions, no plaintext internal hops
2. **At rest** — encryption for databases, backups, files, and object storage
3. **Sensitive fields** — extra protection (hashing, field-level encryption) for secrets, PII, credentials
4. **Key management** — where keys live, how they rotate, and who can access them
5. **Password & credential storage** — strong, salted hashing; nothing reversible or plaintext
6. **Algorithm hygiene** — modern algorithms; no MD5, SHA1, DES, ECB, or homegrown crypto
7. **Coverage gaps** — the data paths and stores that slip through unencrypted

## Phase 3 — Curate
- Rank by sensitivity × exposure: plaintext credentials or weak password hashing tops the list.
- For each, name the fix — enable at-rest encryption, rotate keys out of the code, replace the weak algorithm.
- Separate "not encrypted" from "encrypted but the key is mishandled"; both fail.

## Phase 4 — Report
Create `ENCRYPTION.md` at repo root:
1. **Protection posture** — sensitive data in transit, at rest, and at the field level
2. **Findings** — each: severity · data · the weakness · the fix
3. **Key management** — where keys live and rotate, and the gaps to close
4. **Priority** — the exposures to remediate first

Start the report with today's date. If `ENCRYPTION.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Encryption is only as strong as the key management behind it
- Never roll your own crypto; use vetted algorithms and libraries
- No sensitive data to encrypt in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which encryption gaps to close first
