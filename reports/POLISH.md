# POLISH.md — Fit & Finish Audit

2026-07-26 · brief 152 · first run

The flows walked, deliberately roughly: catalog search and filtering on the
landing page, the quick-view and deep-link path, the copy buttons, the custom
conductor sequence, and the whole Report Studio loop — paste, load from
GitHub, check findings off, remove reports — refreshing mid-task, pressing
Escape, and clicking × along the way. Every finding below was reproduced in a
real browser against the built site, not inferred from code.

The baseline is high. Copy buttons only claim "Copied ✓" when the clipboard
write actually lands and degrade to a raw-file link when it doesn't; bulk
destructive buttons arm ("click again") instead of throwing dialogs; unnamed
pastes get names inferred from their own markdown and suffix instead of
overwriting; the repo box accepts a full GitHub URL, `owner/repo`, or a
`.git` suffix without complaint; run chips say "1d ago", not a raw
timestamp; the search box is `type="search"`, so Escape clears it natively;
`/`, Cmd+K, and j/k give the whole catalog a hands-on-keyboard path. The
findings are the seams left after all that.

## Loses user work

- **FIX S2 · Removing one report in Studio destroys its checklist progress with a single click** — effort S · impact H. The per-report × (`studio.html:484`) filters the report out and re-renders; the re-render immediately prunes every saved checkbox that no longer matches a loaded finding (`studio.html:471-474`, `gp-studio-checks`). Reproduced: check a finding, click the chip's ×, re-add the identical file — the findings return, the check state is gone. The × has no armed confirm (its own sibling "remove all reports" arms at `studio.html:790-799`) and no undo. An operator mid-triage who slips on the 12px × loses an afternoon of decisions silently. Fix, in order of craft: keep an in-memory copy of the removed report + its checks and show a one-line undo ("removed BUGS.md — undo") for ~8s before pruning; or at minimum give × the same armConfirm its bulk sibling has and defer pruning until a different report overwrites the key.

- **FIX S3 · A half-written paste dies with the tab** — effort S · impact M. The Studio paste box (`studio.html:623-649`) keeps the typed name and pasted markdown only in the live DOM; reload mid-edit and both are empty (reproduced). Reports themselves persist to localStorage the moment "add" is clicked — the draft *before* add is the only unprotected input on the page. Fix: mirror `#pastetext`/`#pastename` into sessionStorage on input, restore on load, clear on successful add. No unload dialog needed once the draft survives.

- **FIX S3 · Search and filter state vanish on reload** — effort S · impact M. `query`, the active family chip, and the active playbook filter live only in JS variables (`template.html:1820-1825`); reload and the filtered view resets to zero (reproduced: "error" → 8 cards → reload → all cards, empty box). The page already rewrites its URL with `history.replaceState` to strip tracking params (`template.html:1140`) and already owns `#NN` deep links, so the machinery exists. Fix: mirror `?q=…&f=…` into the URL via replaceState on input, restore them before first render. A filtered catalog view also becomes shareable for free, which the hash deep-links already proved people use.

## Breaks flow

- **FIX S3 · Escape closes disclosures on the landing page but not in Studio** — effort S · impact M. The landing page's "⋯" more-rows close on Escape like any disclosure (`template.html:1613`); Studio's paste box and GitHub box don't — Escape inside `#pastetext` leaves the box open (reproduced; `studio.html:618-622`, `729-733` toggle only from their buttons). Same product, same key, different answer. Fix: one Studio keydown handler — Escape hides whichever box is open and returns focus to the button that opened it.

- **FIX S3 · Deep links flash the card but never hand it focus** — effort S · impact M. `openFromHash` (`template.html:1803-1817`) scrolls to the card, flashes it for two seconds, and sets the expander's aria state — but never calls `focus()`. The eye lands; the keyboard doesn't. j/k then starts from the top of the list, not from the card the link named, and Tab resumes from the document top. Cards are already focusable (j/k focuses them at `template.html:1842`), so the fix is one line: `el.focus({preventScroll:true})` after the scroll.

## Reads unfinished

- **NEW S3 · The only unbranded screen in the product is the error screen** — effort S · impact M. There is no `404.html` in the repo, `build.py` doesn't generate one, and `vercel.json` doesn't configure one — a mistyped `/b/999` or a stale link lands on Vercel's stock 404, the one screen with no ledger type, no mark, and no way back. For a site whose whole pitch is craft, the lost visitor gets the least-crafted moment. Fix: emit a `404.html` from `build.py` (mark, one line of copy, a search link and "browse all briefs") — Vercel serves a root `404.html` automatically for static deploys.

## Systemic gaps

- **IMPROVE · There is no undo primitive anywhere** — effort M · impact H. The codebase's only answer to destructive acts is armConfirm ("click again"), which is good, and used on the bulk paths — but nothing in the product can *reverse* anything. One tiny shared helper (snapshot state → toast with "undo" → restore on click, expire after ~8s) would fix the S2 above, cover the sequence-clear and selection-clear paths, and set the pattern brief 152 preaches: undo over confirm.

- **IMPROVE · Each disclosure box hand-rolls its own open/close** — effort S · impact M. The paste box, GitHub box, more-rows, and context box each wire their own toggle, hidden flag, and (sometimes) Escape/focus behavior — which is exactly how the Escape inconsistency crept in. A ten-line shared `disclosure(btn, box)` helper would give every current and future box Escape-to-close and focus-return for free.

## The feel delta

The three changes that would most move this product toward feeling finished:
1. The undo toast in Studio (kills the only real work-loss path and plants the undo primitive).
2. Search/filter state in the URL (nothing lost on reload, filtered views become links).
3. The branded 404 (the last unbranded pixel in the product).

Report only — which rough edge should be smoothed first?
