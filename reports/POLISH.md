# POLISH.md — Fit & Finish Audit

2026-07-26 · brief 152 · second run (same day as the first)

What changed since the last run: everything. The first run's eight
findings were worked through in order, and every fix below was re-verified
in a real browser the same way the original findings were reproduced. One
new seam was found *during* the fixing — restoring a search query at page
load exposed a constant declared below the boot render (the ranked view had
simply never run that early before) — caught, fixed, and folded into the
search-state item. Nothing in this run's re-walk of the original flows
turned up a new work-loss path.

The re-walk covered the same ground: catalog search and filtering, the
quick-view and deep-link path, the copy buttons, the custom conductor
sequence, and the full Report Studio loop — refreshed mid-task, Escape
pressed everywhere, every × and clear button exercised and undone.

## Loses user work

- **FIXED S2 · Removing one report in Studio destroys its checklist progress with a single click** — shipped in the previous release: the × now snapshots the report and its checked keys and offers a transient "removed X — undo" chip; undo restores both at the old position. Re-verified this run.

- **FIXED S3 · A half-written paste dies with the tab** — the paste box now mirrors its name and text into sessionStorage on input, restores them (box reopened) on reload, and clears the draft the moment "add" lands. Verified: reload mid-draft returns the draft; a successful add leaves no residue. Honest scope: sessionStorage survives reload and restore-tab, not a deliberate tab close — reload was the loss path users actually hit.

- **FIXED S3 · Search and filter state vanish on reload** — the query and family chip now mirror into `?q=…&f=…` via `replaceState` (no history spam) and restore before first paint; a filtered view is a shareable link for free. The fix surfaced a latent boot-order bug — the ranked view's family chips read `FAM_ICON` before its declaration when rendered at load — now declared beside `FAMILIES`, above the boot render. Verified: `?q=error` boot-renders 8 ranked cards, `?f=Craft` boot-renders the family with its chip pressed, and the URL cleans itself when filters reset. Scope note: the playbook filter deliberately stays out of the URL — playbooks already have their own `/p/<key>` pages as the shareable form.

## Breaks flow

- **FIXED S3 · Escape closes disclosures on the landing page but not in Studio** — fixed by the systemic cure rather than a patch: both Studio boxes now go through one `disclosure()` helper (below). Escape inside either box closes it and hands focus back to the button that opened it. Verified on both boxes.

- **FIXED S3 · Deep links flash the card but never hand it focus** — `openFromHash` now calls `el.focus({preventScroll:true})` after the scroll; cards were already j/k focus targets. Verified: landing on `/#152` puts `document.activeElement` on the card itself, so Tab and j/k resume from where the eye landed.

## Reads unfinished

- **FIXED S3 · The only unbranded screen in the product was the error screen** — `build.py` now emits a `404.html` in the site shell ("Not in the ledger."), with the catalog and gallery one tap away and the full footer link row for orientation; noindexed and absent from the sitemap. Vercel serves a root `404.html` automatically for static deploys. Rendered and reviewed.

## Systemic gaps

- **FIXED · There is no undo primitive anywhere** — Studio's one-off undo was extracted into `undoChip(label, aria, restore)` — snapshot → chip → restore, single-level, self-expiring, never expiring under keyboard focus — and now covers all three Studio destructive acts: single-report ×, "remove all reports", and "clear selection". On the landing page, clearing a conductor sequence now posts its toast with a live undo button (the toast already took DOM nodes; it brings its own 9-second expiry). Arm-confirm still guards every bulk click; undo now forgives it. All four paths verified round-trip: destroy → undo → state and storage identical.

- **FIXED · Each disclosure box hand-rolls its own open/close** — Studio's paste and GitHub boxes now share one ten-line `disclosure(btn, box, firstField)` helper: toggle, focus the first field on open, Escape closes and returns focus. Any future box gets the same behavior by construction — which is the point.

## The feel delta

The first run named three changes that would most move the product toward
feeling finished — the undo toast, search state in the URL, the branded 404.
All three are shipped, along with the rest of the list. What this run leaves
behind is a standard, not a backlog: destructive acts offer undo, drafts
survive reloads, view state survives refreshes, Escape means one thing, and
the lost visitor sees the same ledger as everyone else.

Report only — the previous run's findings are all closed; re-run this brief
after the next stretch of UI work to see what new seams have crept in. Which
surface should the next craft pass walk first?
