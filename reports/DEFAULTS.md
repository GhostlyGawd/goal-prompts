# DEFAULTS.md — Smart Defaults & Anticipation Audit

All Craft Goal Prompts · stage 2/5 · brief 153

2026-07-26 · brief 153 · first run (no prior DEFAULTS.md found)

Method: read every input, setting, and persistence path in the source pages
(template.html, studio.html, vitals.html, the build.py detail-page builders,
js/gp-detail.js, js/catalog-core.js, install, mcp/server.cjs), then ran the
first-run and return paths in a real Chromium against the built site — a
fresh profile, and a seeded return profile (6 run marks, saved Operator
context, Vitals 9 days stale).

The headline is honest and unusual: **the first run is already excellent.**
A fresh visit renders one visible form field (the search box), the hero
quickstart copies brief 01 in one click with zero setup, Studio's demo
button carries primary weight when empty, and a passive visit writes nothing
but the anonymous analytics ids (`gp-aid`/`gp-fsw`) — all verified in the
browser. The gaps are in the *return* loop: the product accumulates real
memory (run marks, Operator context, Studio checklists) and then declines to
use it at exactly the moments the weekly ritual needs it. Every top finding
below is a question the product re-asks a user it already knows.

## 1 · Question findings (ranked by frequency × friction)

**Q1 · S1 — Studio's GitHub loader can't see `reports/`, the product's own
default output location.** Lens: never ask what you know / resume. Every
brief writes to `reports/` when that directory exists
(prompts/quality/01-bug-hunt.md:51 — the linter-enforced rule), and every
conductor *creates* `reports/` before stage 1 (js/catalog-core.js:171,
mcp/server.cjs:209). But Studio's "load from a github repo" fetches only the
root listing (studio.html:738 — `/contents`, no `reports/` pass), its
rate-limit fallback probes only root paths (studio.html:723–728), and the
helper text promises exactly that: "fetches the ALL-CAPS .md reports at the
repo root" (studio.html:261). So the repo that followed the product's own
default — ran a playbook once — gets "No report-shaped .md files at that
repo's root" and is bounced back to manual drag-and-drop. The irony: the
demo button fetches this site's own reports *from `/reports/`*
(studio.html:803). **Default to ship:** one extra listing call to
`/contents/reports` (and `reports/<name>` in the raw-URL probe), merged with
the root pass. No new question; the wrong answer costs one 404.

**Q2 · S2 — The repo reference is asked for twice and remembered zero
times.** Lens: never ask what you know / choices remembered. The landing
page's "recommend for my repo" input (template.html:799) and Studio's
`ghref` (studio.html:259) both start blank on every visit; a successful
analyze or load saves nothing (`addReport` stores only `{name, text}` —
studio.html:308, 607 — verified in the browser: reports survive reload, the
ref doesn't). The weekly loop makes this a treadmill: the Fixer hint says
"Reload the reports here afterwards to see ✓ fixed" (studio.html:917) —
and "reload" means retyping owner/repo. **Default to ship:** persist the
last successful ref as `gp-repo` (it already qualifies for the export/import
backup's `gp-` sweep, template.html:1946), prefill both inputs from it, and
turn the post-Fixer hint into a one-tap "reload from ⟨owner/repo⟩".
Override: it's a prefilled text field — edit or clear it.

**Q3 · S2 — A one-time milestone permanently outranks the weekly ritual in
the nudge ladder.** Lens: the likely next step. Both nudge stacks put the
roadmap milestone first in an else-if: `n >= 5 && !runs["28"]` wins over
stale Vitals (template.html:1661–1669; same order in gp-detail.js:237–251).
Verified: with Vitals 9 days stale and 6 runs marked, the landing and detail
pages both showed only "compose them into one plan: #28". A user who never
runs 28 — a legitimate choice — never sees the stale-Vitals nudge again,
anywhere, and the retention ritual the SW reminder machinery was built for
(R33–R35) silently loses its on-page half. **Default to ship:** recurring,
time-keyed staleness outranks the one-shot milestone; or the milestone shows
a bounded number of times (one `gp-` dismissal key, the backer nudge's
existing pattern at template.html:1633).

**Q4 · S2 — Detail pages hide run state the product already stores.** Lens:
resume, don't restart. With `runs["01"]` nine days old, /b/01 renders no
trace of it — the run mark appears only inside the post-copy hint
(gp-detail.js:126). /p/day1 shows steps 1–8 with copy buttons and no ✓ marks
even when four of its stages are marked run (verified; build.py:1435–1450
emits no run-state hook, though gp-detail.js:69 already has `hasRun` and
loads on every detail page). A returning user planning "what's next?" from a
playbook page is re-deriving progress the product knows. **Default to
ship:** a "✓ run · 9d ago" chip beside the brief CTA and per-step marks on
the sequence map — display only, from data already on the device; overrule
is the existing run toggle.

**Q5 · S3 — The browse gate re-asks an answered question on every return.**
Lens: choices remembered. `browsing` is a plain JS variable
(template.html:1010), so the returning user with 6 run marks still lands on
"Pick a question above, search, or browse all 157 Goal Prompts" with zero
cards (verified — the intent gate at template.html:1712–1719 renders
identically for a stranger and a regular). The gate is right for first
contact (BLINDSPOTS F6); it's a re-asked question for someone whose
localStorage proves they've picked before. **Default to ship:** persist the
last mode (or treat any run mark as standing intent and boot into the
catalog); the gate's own controls remain the override. The ?q=&f= URL
mirror (POLISH S3) already covers reloads — this covers fresh navigations.

**Q6 · S3 — Conductor copies silently drop the Operator context that "rides
every copy".** Lens: never ask what you know / cheap to overrule. The
context box promises "applied to every copy" (template.html:805) and "
appended to every Goal Prompt you copy" (template.html:811), and per-step
playbook copies honor it (gp-detail.js:207, 214). But every conductor path
skips it: storefront (template.html:1391), playbook bar (1768), family
"run all" (1793), custom sequence (2073), and the playbook page's CTA
(build.py:1414 emits no `data-ctx`; makeConductor at js/catalog-core.js:159
never sees `gp-ctx`). The flagship one-paste path is the one place the
user's saved tuning vanishes — invisibly, so it fails lens 7 too. **Default
to ship:** append the same `## Operator context` block to conductor text
with one line telling the agent to weigh it in every stage.

**Q7 · S3 — Studio's fallback probe guesses 11 hardcoded filenames while
the catalog knows all ~157.** Lens: never ask what you know. `GH_COMMON`
(studio.html:706) is a fixed list; the product also knows, per user, which
briefs were marked run (`gp-runs`) and each one's `output` filename
(catalog.json). When the listing API 403s, the probe misses most real
reports. **Default to ship:** probe the run-marked briefs' outputs first,
then GH_COMMON. Pairs with Q1's `reports/` paths.

**Q8 · S3 — The "product" and "stage" context fields stay blank after a
call that could fill them.** Lens: never ask what you know. Repo-recommend
already prefills `ctx.stack` from its GitHub call and says so visibly
(template.html:2208–2213 — the right pattern: only when empty, announced,
editable). The same API surface carries the repo `description`, which is the
"product" line the form asks for (template.html:808); today the user
composes it from memory or runs the copy-a-prompt-to-your-agent detour
(template.html:813). **Default to ship:** prefill `product` from the repo
description when empty, with the same "✓ saved" line and the same override.

**Q9 · S3 — The touch heuristic assumes every coarse pointer is the wrong
machine, with no way to overrule.** Lens: cheap to overrule. On any coarse-
pointer device the post-copy hint *replaces* the paste guidance with "On
your phone? Copy this URL instead" (template.html:1207–1215). An iPad or a
touch-screen laptop sitting next to (or running) the agent gets the detour
and never the actual next step. A wrong guess here should cost a click —
instead it removes the correct path entirely. **Default to ship:** show
both — paste guidance plus the raw-URL bridge — instead of branching.

**Q10 · S3 — Vitals, the weekly page, is the only surface with no fetch
path.** Lens: works before configured / resume. Its inputs are drop, paste,
sample (vitals.html:132–136, browser-verified) — so the weekly ritual means
re-dropping the same HEALTH.md every Monday, while sibling Studio can fetch
from a repo. Dedupe already protects re-drops (vitals.html:367). **Default
to ship:** with Q2's remembered `gp-repo`, a one-tap "refresh HEALTH.md
from ⟨repo⟩" (root + `reports/`).

**Correctly asked — leave these alone.** The weekly reminder is opt-in
behind a real OS notification permission (template.html:2012–2038): a wrong
guess there is a nagging notification, worse than asking. Every destructive
clear is arm-confirm + undo (POLISH's systemic fix) — asking is the point.
The conductor's stage-1 go-ahead and per-stage "re-run or skip" when a
report exists (js/catalog-core.js:174, 192) guard hours of agent time and
file overwrites — the ask-first gate is the product's charter invariant,
not indecision. And repo-recommend refusing to overwrite an existing
`ctx.stack` (template.html:2212) is the right restraint.

## 2 · The memory map

Persists per user today (all localStorage unless noted):
`gp-theme` (theme override; OS preference is the default — right)
· `gp-runs` (run marks + timestamps) · `gp-seq`/`gp-seqused` (custom
conductor) · `gp-ctx` (Operator context) · `gp-remind` (reminder opt-in)
· `gp-studio-reports`/`gp-studio-checks` (Studio state — survives reload,
verified) · `gp-studio-draft` (sessionStorage paste draft)
· `gp-vitals-texts` (Vitals sources) · `gp-backer-done`, `gp-wb-hide`
(nudge dismissals) · `gp-aid`/`gp-fsw` (anonymous cohort ids) · the
IndexedDB `gp-sw` mirror for the SW · `?q=`/`?f=` and `#sel=` in URLs.
The export/import backup sweeps every `gp-` key (template.html:1946), so
new keys inherit portability for free.

Resets to factory every visit, though the product knows the answer:
the repo reference (Q2) · the browse-gate answer (Q5) · run state on
detail pages (Q4 — stored but not shown) · which reports came from where
in Studio (Q1/Q2 — `{name, text}` only).

## 3 · First-run delta

Today, install → first value is already two actions and zero fields: land →
quickstart copy (brief 01, visible without scrolling) → paste into the
agent. The installer asks nothing (`curl | sh`, checksum-verified, sensible
`BRIEF`/`BASE` env overrides); the MCP server works with zero config and
zero-pads ids so `'6'` just works (mcp/server.cjs:31). These defaults don't
shorten a path that's already near-minimal.

The delta lives in run 2..N. Today's return: retype owner/repo in Studio
(Q2), get told the repo has no reports because they're in `reports/` (Q1),
re-drop HEALTH.md by hand (Q10), re-answer the browse gate (Q5), re-derive
playbook progress by memory (Q4). After these defaults: land → catalog
already open on your state → Studio one-tap "reload from ⟨repo⟩" finds the
`reports/` directory → Vitals refreshes itself → zero retyped fields in the
whole weekly loop.

## 4 · Retired settings

This product has admirably few toggles — the indecision shows up as
unpersisted questions (above), not settings. Two small retirements stand:
the Studio paste-name field is already effectively retired by
`inferReportName` (studio.html:664) — keep it as the override it now is;
and the coarse-pointer branch (Q9) is a setting the product invented for
the user without asking — retire the either/or, show both paths. Everything
else that looks like a setting (reminder toggle, reset, export/import) is
a consent or portability control the no-backend charter requires.
