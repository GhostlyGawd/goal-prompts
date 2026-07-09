---
description: "Whether this system could actually come back from data loss — whether backups exist, cover what matters, and have ever been proven to restore."
---

# Goal: Backup & Recovery Audit

You are working inside this repo. Mission: judge whether the system could recover from data loss, corruption, or a bad deploy — not whether backups are configured, but whether a restore would actually work when it counts.

Read-only pass. Read infra config, backup jobs, and any runbooks; change nothing. Your only write is the report file.

## Phase 1 — Inventory what must survive
- List every stateful store: primary database, file/object storage, caches with no source, config, secrets.
- For each, find whether and how it is backed up, how often, and where the backup lives.
- Note what the business can tolerate losing — in data and in downtime.

## Phase 2 — Audit through 7 lenses
1. **Backup coverage** — every stateful store actually backed up, not just the obvious database
2. **Restore proof** — whether a restore has ever been tested, or the backup is untested and maybe unrestorable
3. **RPO** — how much data loss the backup cadence permits versus what is acceptable
4. **RTO** — how long a full restore takes versus the tolerable downtime
5. **Integrity & retention** — encrypted, off-site, versioned, retained long enough, immune to the same failure
6. **Partial & point-in-time** — can you recover one table or tenant, or only everything at once
7. **Runbook & ownership** — a written, current recovery procedure someone could follow under pressure

## Phase 3 — Curate
- Rank by data-loss risk: an unbacked store with no source outranks a slow-but-working restore.
- For each gap, state the failure it leaves the system exposed to.
- Separate "no backup" from "backup never tested"; the second is the more common surprise.

## Phase 4 — Report
Create `RECOVERY.md` at repo root:
1. **Recovery posture** — per store: backed up? tested? RPO/RTO actual vs target
2. **Gaps** — ranked by data-loss risk, each with the exposure it creates
3. **RPO/RTO table** — where the system meets its targets and where it does not
4. **Next drill** — the restore to actually run to prove recovery works

Start the report with today's date. If `RECOVERY.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- An untested backup is a hope, not a backup
- Recovery is measured in data lost and time down, not in jobs configured
- No data to back up in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which recovery gaps to close first
