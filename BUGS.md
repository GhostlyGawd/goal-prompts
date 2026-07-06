# BUGS.md
*Produced by brief 01 · Bug Hunt, run against this repo (goal-prompts, v0.4). Part of the sample-report gallery.*

## Summary
5 findings: 0 × S1, 3 × S2 (two fixed in 0.4 during this audit cycle), 2 × S3. Scariest: the empty-state XSS, because it was the only place user input met `innerHTML`.

## Findings

**1. Copy-button label race — S2 · certain · FIXED in 0.4**
Location: `template.html`, `feedback()`. Trigger: tap Copy twice within 1.6s; the second call captured "Copied ✓" as the restore label, so the button stuck on "Copied ✓" forever. Expected: label always restores. Root cause: restore text read from live `textContent` instead of a stored original. Fix shipped: original cached in `dataset.label`, timer cleared on re-entry.

**2. Self-XSS in the empty state — S2 · certain · FIXED in 0.4**
Location: `template.html`, `render()` empty branch. Trigger: type `<img src=x onerror=…>` into search with zero matches. Expected: query rendered as text. Root cause: `query` interpolated into `innerHTML`. Impact was self-only (no URL parameter feeds search), but it was one refactor away from reflected. Fix shipped: built with `textContent`.

**3. Deep-link target hides under the sticky toolbar — S3 · likely · open**
Location: `template.html`, `.card{scroll-margin-top:120px}` vs the sticky `.toolbar`. Trigger: open `/#30` on a narrow screen where search + family chips + playbook chips wrap to ~180px tall. Expected: card top visible. Fix sketch: raise scroll-margin to ~190px or set it from measured toolbar height. Effort S.

**4. Hash router caps at two-digit ids — S3 · certain · open**
Location: `openFromHash()`, regex `^\d\d$`. Trigger: none today (ids run 00–45); becomes real at id 100. Fix sketch: `^\d{2,3}$` plus the existing `byId` guard. Effort S. Filed as forward-compat.

**5. Installer silently overwrites local command edits — S3 · likely · FIXED in 0.4**
Location: `install`. Trigger: user customizes a file under `.claude/commands/goal/`, re-runs the installer, edits vanish. Fix shipped: explicit warning line when `goal/` already exists.

## Verification plan
Finding 3: load `/#30` in a 390px viewport, check card top offset against toolbar height.

## Top 3 to fix first
1 and 2 shipped with this release; 3 is next (one CSS value, real mobile impact).

*Report only — which remaining bugs should be fixed?*
