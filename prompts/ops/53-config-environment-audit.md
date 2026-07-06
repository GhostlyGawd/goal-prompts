---
id: "53"
title: Config & Environment Audit
family: Ops
question: does it run?
output: CONFIG.md
tagline: Env-var sprawl, prod/dev drift, magic values, and settings with no safe default — mapped so the config stops being a source of outages.
---
# Goal: Config & Environment Audit

You are working inside this repo. Mission: map how this system is configured across environments — every variable, flag, and magic value — and find where config causes drift, breakage, or 3am confusion.

Read-only pass. Your only write is the report file.

## Phase 1 — Inventory the configuration
- Find every source: env vars the code reads, config files, feature flags, hardcoded constants that behave like config, build-time vs runtime settings.
- Cross-check: which env vars does the code actually read vs which are documented (an example env file, README)? Note both directions of mismatch.
- Note how config differs across local, staging, and production, as far as the repo reveals.

## Phase 2 — Audit through 7 lenses
1. **Undocumented vars** — settings the code reads that no example file or doc mentions: landmines for a new deploy (ties to 14, 16)
2. **Missing safe defaults** — required config with no fallback, where absence crashes at runtime instead of failing loudly at startup
3. **No validation** — config read and trusted without checking presence, type, or range; a typo'd number silently changing behavior
4. **Environment drift** — behavior that differs between dev and prod because of config, in ways that cause works-locally-fails-in-prod (ties to 23)
5. **Magic values** — hardcoded URLs, timeouts, limits, and keys buried in code that should be surfaced as named config
6. **Secret hygiene** — secrets mixed into general config, committed example files carrying real-looking values, secrets read where they might get logged (ties to 06)
7. **Startup honesty** — does the system validate its config on boot and fail fast with a clear message, or discover missing config lazily when a user hits the feature

## Phase 3 — Curate
- Rank by blast radius: config that silently changes behavior outranks a missing nice-to-have
- Every finding names the fix: document, add default, validate at startup, or promote a magic value to config

## Phase 4 — Report
Create `CONFIG.md` at repo root:
1. **Config inventory** — variable/setting · read where · documented? · default? · environments it varies across
2. **Findings** — each: issue · lens · evidence · fix · risk
3. **Startup validation plan** — the config to check on boot, and what a clear failure message looks like
4. **The canonical example file** — the complete, accurate list of what a deployer must set
5. **Quick wins** — undocumented vars to document and magic values to surface today

## Rules
- Config should fail loudly at startup, never silently at runtime
- The example env file is documentation an agent and a human both trust — make it complete and true
- Report only — end by asking which fixes to make
