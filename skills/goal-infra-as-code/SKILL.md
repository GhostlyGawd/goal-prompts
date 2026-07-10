---
name: goal-infra-as-code
description: "Read the Terraform, K8s, and Dockerfiles the way the machine will — :latest tags, plaintext secrets, copy-pasted stanzas — and map the blast radius of one bad apply. Audit brief 137 · Ops — runs a four-phase audit of the current repo and writes INFRA.md at the repo root."
---

# Goal: Infra-as-Code Audit

You are working inside this repo. Mission: audit the infrastructure definitions — Terraform, Kubernetes manifests, Dockerfiles, compose files, CI deploy steps — the way the machine reads them, and map what one careless apply could take down.

Read-only pass. Parse the definitions; run read-only validators (`terraform validate`, `docker build --check`, dry-run renders) if available; change nothing. Your only write is the report file.

## Phase 1 — Inventory the definitions
- Find every infra definition in the repo and what each one actually provisions or deploys; note the ones nothing references anymore.
- Identify how changes reach reality: who or what runs apply, from where, gated by what.
- Locate state: remote backends, lockfiles, kubeconfig assumptions.

## Phase 2 — Audit through 7 lenses
Every finding cites a resource and file:line.
1. **Secrets in the open** — plaintext credentials in tfvars, manifests, Dockerfiles, compose env blocks; secrets that land in Terraform state or image layers
2. **Unpinned reality** — `:latest` and mutable tags, unpinned providers and modules, base images by name only; each one a deploy that can differ from the last
3. **Blast radius of one apply** — what a single bad apply can destroy: missing `prevent_destroy`, no deletion protection on data stores, resources whose recreation loses state
4. **Sizing by copy-paste** — requests, limits, and instance types: chosen for this workload or inherited from a tutorial; the missing limits that let one pod starve a node
5. **Stanza drift** — the same block duplicated across environments and already diverging; diffs between dev and prod that are accidents, not decisions
6. **Boot honesty** — health checks, readiness probes, and restart policies that reflect real dependencies, or containers that report ready while their world is down
7. **The apply path** — state locking, plan review before apply, who can run it from a laptop; the gap between "in git" and "what's live"

## Phase 3 — Curate
- Rank by irreversibility: a destroyable database outranks an oversized instance.
- Separate "one-line hardening" (a pin, a protect flag, a limit) from "restructure" (module extraction, environment layering).
- For drift findings, name the intended single source and the diff to reconcile.

## Phase 4 — Report
Create `INFRA.md` at repo root:
1. **The blast map** — what one bad apply or deploy can destroy, worst first, with the guard each lacks
2. **Findings** — each: lens · resource (file:line) · risk · the fix · one-liner or restructure
3. **Drift census** — duplicated stanzas and environment diffs: intentional (documented where?) or accidental
4. **Hardening order** — the pins, protections, and limits to add this week, sequenced

Start the report with today's date. If `INFRA.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Judge what the files do, not what their comments intend; the machine reads only one of those
- Irreversible beats inefficient in every ranking
- No infrastructure definitions in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which hardening steps to take first
