# SIGNATURE.md — Signature Moments Audit

All Craft Goal Prompts · stage 5/5 · brief 156

2026-07-26 · brief 156 · first run (no prior SIGNATURE.md found)

Method: mapped the three core journeys to their emotional beats, then ran
them in a real Chromium against the built site — a fresh profile for the
newcomer path, seeded profiles for the repeat visits (5 runs with saved
Operator context; 60 runs; a Studio report re-added in its post-Fixer
"FIXED" form), plus the Studio demo, the Vitals sample, the `/b/47` and
`/p/day1` detail pages, the `/r/` report pages, the gallery, and the OG
cards. Every "observed" below is a screenshot or a computed style from
that run. Sibling findings from today's run stay with their owners
(PERCEIVED-SPEED W1 owns the frozen first copy, DEFAULTS Q1 the Studio
`reports/` blind spot, COMPOUNDING C-series the accrual gaps); this
report's angle is peaks, endings, and what a user would show someone.

Where the journeys peak, honestly: (a) the newcomer's real first win —
the report file appearing in their repo — happens **in the agent
conversation**, off this site; the site's share of it is the post-copy
hint and the brief's own ending. (b) The triage loop peaks twice: copying
the Fixer prompt, and — the true peak — reloading the reports and seeing
findings turn `✓ fixed`. (c) The weekly ritual peaks at the trend arrows.
The product's restraint is genuinely excellent — no confetti, no streaks,
no self-congratulating toasts anywhere in the codebase — but two of those
three peaks currently land broken or silent, and the crafted ending that
does exist (the conductor's debrief) is specified in text nobody ever
sees staged.

## 1 · Moment findings (ranked by retelling odds)

**M1 · unstaged peak · journey b (report → Fixer → reload) —
studio.html:601–618, 131–135; js/report-parser.js:59.** The loop's proof
moment is silent. Observed: pasted a BUGS.md with 3 open findings,
re-added it in its post-Fixer form (2 marked FIXED) — the two `✓ fixed`
chips render and nothing else happens. No line says "2 findings closed
since the last load." The fixed rows keep the same red action border as
open ones (`.find{border-left:3px solid var(--act)}`, studio.html:132 —
there is no fixed-row variant), keep full visual weight and position, and
the title renders "FIXED S1 · Crash on empty input" with a duplicate
`✓ fixed` chip beneath it. The selbar reads "0 of 3 findings selected" —
the ledger never says "2 closed." This is the one moment the product can
show *your repo actually got better* in pixels, and it is
indistinguishable from a first load. The mechanism is even in reach:
`addReport` (studio.html:601) holds both the old and new versions at
replace time, so the closed-count is computable from state Studio already
has. **Crafted version:** on a same-name re-add, diff the fixed flags and
post one line in the existing note/undo-chip register — "BUGS.md: 2
findings closed since the last load · 1 still open" — and let fixed rows
sink: `--sev-fixed` left border, dimmed, sorted after open findings, the
redundant FIXED title prefix stripped when the chip is present. Decay
rule: the line is data, not praise — it renders only when the closed
count is > 0, so it self-decays to nothing on ordinary reloads.

**M2 · squandered peak · journey c (weekly Vitals) — vitals.html:340–349;
tokens.css:30/67 (`--up:var(--success); --down:var(--danger)`).** The
trend arrows color direction, not meaning — the ritual's payoff paints
wins as regressions. Observed on the page's own sample history (an
improving repo by every vital): "Build (s) 35 **▼ -1**" and "TODOs 46
**▼ -3**" render in danger red `rgb(176,46,18)`; "LOC 8410 **▲ +105**"
renders success green. A build getting faster and a TODO count falling
are the good weeks this ritual exists to produce, and the viewer flags
them like failures. Brief 29 pins the same vitals every run by rule
(prompts/meta/29-health-check.md:20–26, 45: "Same vitals every run"), so
the canonical set is knowable. **Crafted version:** a small
lower-is-better map for brief 29's own vitals (fail counts, build
seconds, vulns, outdated, lint/type errors, TODOs) flips the good/bad
coloring for those; any metric the map doesn't know — including LOC —
gets the neutral `--faint` delta it can honestly claim. No decay rule
needed; this is semantics, not flourish.

**M3 · peak surface, least craft · journey c — vitals.html:75 (`.pastebox
{display:grid}`), 72 (`.iconbtn{display:inline-flex}`), no `[hidden]`
pin.** The Vitals page ships permanently half-open. Observed on a fresh
load with nothing loaded: `#pastebox` (`hidden` attribute set) and the
"clear" button (`#clearall`, also `hidden`) are both fully visible —
their author `display` beats the UA's `[hidden]` rule. Studio pinned
exactly this with `[hidden]{display:none!important}` and a comment naming
the hazard (studio.html:36); vitals.html never got the line. So the
weekly ritual's landing view greets the user with an open paste form and
a "clear" button for nothing — on the surface whose screenshot *is* the
shareable trend view. **Crafted version:** copy Studio's one-line pin.

**M4 · squandered ending · journey a (single-brief run, the majority
path) — prompts/quality/01-bug-hunt.md:52 vs js/catalog-core.js:185.**
Every audit brief ends "Report only — end by asking which bugs to fix,"
which correctly stops the agent — but nothing requires the agent to
*present* the findings first. The conductor's ending has the crafted
line: "Present the strongest findings across every report as one ranked
list, in plain words — the operator should not need to open a report
file to act" (catalog-core.js:185). Single briefs — the way most users
run this product — leave that to the agent's mood, and CHARTER.md F1 is
verbatim about what happens when legibility is left to chance ("I have no
idea what [the Fixer] even does"). The journey's ending is a file path
and a question; whether the win is *felt* is unspecified. **Crafted
version:** one shared sentence added to the ask-first gate grammar
(CONTRIBUTING + linter, so it lands mechanically across briefs): present
the top findings as a short ranked list in plain words before asking. The
ending becomes the debrief in miniature — same shape at every scale.

**M5 · first win diluted · journey a — template.html:1217–1235.**
Observed: the first hero copy pops a hint carrying four onward paths —
"drop it in the Report Studio", "what happens next →", "then run the rest
of Day-1 →", "✓ mark it run" — inside one 13px toast. The product's very
first acknowledgment offers a menu, against its own one-thing-at-a-time
voice (CLAUDE.md), and two of the four (Studio first among them — the
surface CHARTER.md F2 says the ICP skips) point away from the only step
that matters now: go paste it. **Crafted version:** the first-copy hint
carries paste + "what happens next →" only; "✓ mark it run" and the
Day-1 tee arrive on the *return* (the mark-run moment already exists as
the proven-intent hook — template.html:2043). Decay rule: see R1 — after
the first confirmed run, the whole explainer collapses to one line.

**M6 · quiet accrual, unacknowledged · journey a repeat —
template.html:1416–1423, 1654–1680.** Observed: at 60 runs the page is
pixel-identical to 6 runs except the mono fine-print "157 Goal Prompts ·
60 run here"; once brief 28 has run, no milestone surface exists at all.
The one milestone that does fire (5 runs) opens with the user's number
but spends its sentence asking for more work ("Ready to compose them into
one plan: #28 →") — and it has no dismiss, so it re-renders every
default view until obeyed (template.html:1670–1679 builds only links).
The near-total quiet is *mostly right* — this report is not asking for
confetti — but the only voice at the milestone being an undismissable ask
reads as the product honoring its funnel, not the user's work. **Crafted
version:** keep the register; give the nudge a permanent dismiss × (the
backer nudge already has one — template.html:1643–1648), and let the
first clause stand as the acknowledgment it almost is. Decay rule:
dismissed = gone forever, like the backer nudge's `gp-backer-done`.

## 2 · The signature candidate

**The conductor's closing debrief** — one paste runs the playbook,
narrates every stage in two plain sentences ("never advance in silence",
js/catalog-core.js:180), then ends with a ranked plain-words list of the
strongest findings across every report, the question "which do I fix?",
the Fixer offer, and a paste-ready handoff block
(js/catalog-core.js:183–188). This is the moment someone retells: "I
pasted one prompt; it audited my repo for an hour, told me the five
things that matter, asked me, then fixed them with one verified commit
each and left the receipts." It is the charter's own definition of the
product (Now #6: paste once → audits → "which do I fix?" → commits +
FIXLOG, zero browser), it needs no browser surface, and every finding
above feeds it: M4 gives the same ending to single briefs, M1 gives the
loop its visible receipt, M2/M3 make the weekly echo of it trustworthy.

The gap: it is **specified but never staged**. No surface shows what the
debrief looks like — the gallery (examples/index.html, observed) shows
every *report* but never the conversation moment; the playbook pages'
"what you'll have at the end" box (observed on /p/day1) lists files, not
the ranked-list-and-ask that is the actual ending; and its shape lives
only as prompt text, unpinned by any test, so it can drift silently.
Over-invest here: pin the debrief's shape (ranked list · ask · handoff
block) in the conductor-parity smoke test, put one real transcript
excerpt — the debrief of an actual run, not a mockup — in the gallery
and on the playbook pages' ending box, and let the site's "how it works"
end on that moment instead of on the report files.

## 3 · Output audit (each shareable artifact)

- **The user's report files** (BUGS.md, HEALTH.md, …) — current: strong
  ambassadors; summary-first, severity-ranked, evidence-cited, and they
  render cleanly on GitHub (the format grammar did its job). Gap: a
  single-brief report says nothing about what produced it — conductors
  stamp a provenance line (catalog-core.js:178) but solo runs carry only
  a date, so the artifact a teammate reads names no origin. Show-worthy:
  the conductor's exact one-line pattern, extended to solo runs via the
  shared grammar — one mono line, no badge, no link-spam.
- **INDEX.md + the PR handoff** (catalog-core.js:184–188) — current: the
  best-composed ending artifact in the product ("the PR list is the first
  place a later session or teammate looks"). Gap: unproven in public —
  no published external before/after exists (CHARTER Now #1), so the
  shareable ending has never been shown ending anything real.
- **The `/r/` report pages** — current: genuinely show-worthy (observed
  /r/fixlog, /r/bugs: composed hero, "Run this audit on your repo" CTA).
  Scope is honest — dogfood reports only; no change wanted.
- **OG share cards** (og/, scripts/og.py) — current: crafted; the bar
  language, family colors, and "N REPORTS" line carry the brand (observed
  p-day1.png). No change.
- **Studio's share-selection link** (studio.html:928–933) — current:
  honest but weak — it only reconstitutes for someone who loads the same
  reports, and its own boot note says so (studio.html:936–940). Fine
  as-is; the Fixer prompt, not the link, is the real export.
- **The Vitals trend view** — current: the screenshot *is* the share
  format, and today it ships with mis-colored wins (M2) and a permanently
  open paste form (M3). Fixing those two is the entire show-worthiness
  gap; no export feature wanted.

## 4 · Restraint list

The codebase contains no confetti, no streaks, no milestone animations,
no self-congratulation — `grep` for celebration vocabulary comes back
empty, and the loudest success state anywhere is a 1.6-second "Copied ✓"
(template.html:1119–1126). That bar is correct; hold it. What remains is
tutorial-repetition, the quieter cousin of confetti:

- **R1 · The post-copy explainer never decays** (template.html:1204–1236,
  js/gp-detail.js:110–161). Every copy — the 1st and the 200th — replays
  the full "Paste into Claude Code, Cursor, or any agent inside your
  repo…" toast. Decay: once `runCount() > 0`, collapse to the short form
  ("Copied ✓ — writes `BUGS.md`"); the full explainer is for people the
  product hasn't met yet.
- **R2 · The roadmap / stale-Vitals nudges have no dismiss** and re-render
  every default view until obeyed (template.html:1654–1680). Decay: a ×
  that sets a `gp-*-done` key, exactly like the backer nudge
  (template.html:1643–1648). The stale-Vitals nudge may return on a new
  staleness, but a dismissal within the same stale period sticks.
- **R3 · The Day-1 tee rides the first copy** (template.html:1224–1228).
  Move it behind the first mark-run (M5); the first-win toast carries one
  next step. Decay: it appears once — a marked run means the tee's job is
  done.
- Everything else — arm-confirm, undo chips, the herostat counter, the
  welcome-back strips with their 14-day dismissal (gp-detail.js:235) —
  is already right-sized and already decays. Nothing to remove.

## Next steps, ranked

1. **Stage the loop's receipt (M1)** — the closed-count line + fixed-row
   demotion in Studio; it converts the product's proof moment from
   silence into the thing users screenshot.
2. **Fix the Vitals peak (M2 + M3)** — the direction map and the one-line
   `[hidden]` pin; the weekly ritual's payoff must never paint a win red
   or greet its user with a broken form.
3. **Give every brief the debrief ending (M4), then stage the debrief
   itself (§2)** — one grammar sentence now, one real transcript in the
   gallery when the next real run produces it.
