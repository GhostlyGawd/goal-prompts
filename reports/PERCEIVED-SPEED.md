# PERCEIVED-SPEED.md — Perceived Speed Audit

All Craft Goal Prompts · stage 3/5 · brief 154

2026-07-26 · brief 154 · first run (no prior PERCEIVED-SPEED.md found)

Method: read every loading, fetch, and transition path in the source pages
(template.html, studio.html, vitals.html, js/gp-detail.js, build.py's
SERVICE_WORKER and detail-page builders, install, mcp/server.cjs), then ran
the built site in a real Chromium and *felt* the waits — CDP network
throttling for page loads, per-route delays for bodies.json / raw briefs /
GitHub, and two purpose-built slow origins (40 KB/s streaming; 3 s
time-to-first-byte with must-revalidate headers) because CDP emulation does
not reach service-worker fetches. Local numbers are shape-accurate, not
production-exact (no gzip locally; index.html is 260 KB raw / 78 KB gz,
bodies.json 466 KB raw / 142 KB gz).

The honest headline first: most of this product is genuinely fast and
honestly presented. A `/b/01` copy acknowledges in 94 ms (body inlined in
the page), search keystrokes cost 0.4–9 ms with no jank (measured across a
14-char query), Vitals renders its sample in 85 ms, Studio boots
synchronously from localStorage, layout shift on a throttled cold load is
CLS 0.002, fonts are preloaded with `font-display:swap`, and the 10–20 min
agent run — the real wait this product sells — is narrated stage-by-stage
by the conductor ("never advance in silence", build.py:239). The findings
below are the seams where a slow network turns that polish into frozen
silence.

## 1 · Wait findings (ranked by exposure)

**W1 · S2 · unacknowledged · lens 1 — The hero quickstart (and every card
Copy) freezes for the length of the bodies.json download.** Interaction:
first-visit click on "New here? Copy your first brief" — the product's
front door. Observed: with bodies.json delayed 6 s (a slow first visit,
before the idle prefetch lands), the click produced **zero visible change
for 6.1 s** — same label, no busy state, no cursor change — then "Copied ✓"
popped. Where: `copyBrief` (template.html:1311–1348) deliberately starts a
gesture-synchronous `ClipboardItem` write whose text resolves when
bodies.json lands — correct for WebKit's clipboard rules — but nothing
paints a pending state; `feedback()` only fires on resolution. The frozen
window is real on slow networks for roughly the whole first ~10–20 s of a
visit (prefetch starts at `load` + idle, template.html:2108–2112; the blob
is 142 KB gz). A dead-feeling click on the single most important button
invites a re-click and reads as broken. **Treatment: acknowledge, then
resolve** — set the button to "copying…" (+`aria-busy`) synchronously in
the click, keep the existing write exactly as is; `feedback()` already
restores labels. Failure story already exists: the raw-link swap
(template.html:1301–1306).

**W2 · S2 · cold reload of something just seen · lens 5 — The service
worker fetches HTML network-first with no timeout, so a warm cache buys
returning visitors nothing while online.** Interaction: every return visit
and every in-site page hop (catalog → /studio → /vitals — the weekly
loop's actual navigation). Observed on a 3 s-TTFB, must-revalidate origin
with the precache fully warm: first visit DCL 6153 ms, **return visit DCL
6038 ms** — the cache changed nothing; offline, the identical page renders
in 79–113 ms, which is what the cache *could* deliver. Where:
build.py:286–296 — `fetch(req)` first, cache only on rejection; the
precache already holds `/`, `/studio`, `/vitals` (build.py:2441). Worst
case is lie-fi: a network that answers slowly never rejects, so the
cached app never appears. **Treatment:** stale-while-revalidate for
same-origin HTML (serve cache, refresh behind) — the deploy story already
tolerates it because the cache version is a content hash and a deploy
self-invalidates (build.py:2440); or keep network-first but race it
against a ~2.5 s timeout that falls back to cache. Either turns the weekly
return into a ~100 ms open.

**W3 · S2 · unshaped + dishonest · lenses 4/3 — Studio's GitHub load is
one flat "loading…" over a multi-phase operation, and its rate-limit
failure lies about what happened.** Interaction: "load its reports" in
Studio. Observed with the listing API returning 403 and raw probes
delayed: the button reads "loading…" with no other signal while the code
silently runs a **22-request** filename probe (11 names × 2 branches,
studio.html:719–731), then the note says "No report-shaped .md files
(ALL-CAPS names) at that repo's root" (studio.html:766) — but the truth
was "GitHub rate-limited the listing; a fallback guessed 11 common
filenames and missed." The user gets a confident wrong diagnosis after an
unnarrated wait — they'll conclude their reports are invisible, not that
GitHub throttled them. (DEFAULTS Q1/Q7 cover *what* the loader should
fetch; this is about what the wait says while it fetches.) **Treatment:
honest progress** — advance the label per phase ("listing repo…" →
"rate-limited — trying 11 common filenames…"), and split the two failure
messages so the 403 path says the rate limit was the problem, like the
landing page's repo-analyze already does (template.html:2178).

**W4 · S3 · half-acknowledged · lens 1 — Playbook per-step copy stays
clickable mid-fetch and double-fetches; on WebKit the slow path loses the
copy entirely.** Interaction: a step's "copy" on any `/p/<key>` page —
the first copy fetches `/raw/<id>.md` at click time. Observed with a 3 s
raw delay: the button shows "…" (good), but a second impatient click fired
a **duplicate fetch** (2 requests observed); and the copy runs *after* the
await (gp-detail.js:207–215) — the exact pattern template.html:1318–1324
documents as failing on WebKit and on expired transient activation, so on
Safari over a slow link the step copy degrades to "open raw ↗" instead of
copying. **Treatment:** disable during fetch, and reuse `copyBrief`'s
gesture-synchronous ClipboardItem pattern. Failure story: the existing
`rawFail` link (gp-detail.js:100–106).

**W5 · S3 · warm next steps · lens 5 — Playbook pages never warm the
bodies they know they'll need — and the cold path they use pollutes the
usage metric.** The page carries every step's URL at build time
(build.py:1447 emits `data-fetch="/raw/<id>.md"`), yet the first copy of
each step pays a full round trip inside the click (the W4 wait), while
the landing page idle-prefetches bodies.json for exactly this reason
(template.html:2106–2112). Sharper: these are *browser* copies hitting
`/raw/`, the endpoint whose fetch counts are supposed to stay an honest
agent-usage metric (template.html:989–993, docs/usage-metrics.md) — the
slow path and the metric leak are the same line of code. **Treatment:**
source step copies from bodies.json (SW-precached, idle-warmable) and
leave `/raw/` to agents — faster when warm, and the metric stays clean.

**W6 · S3 · late-arriving hot path · lens 7 — On a slow first load, the
newcomer's primary CTA is the last thing to appear.** Observed on the
40 KB/s origin: hero headline and static CTAs paint at ~1.3 s (the HTML
streams well), but the quickstart pill stays `hidden` until the full
260 KB document parses and JS runs — it appeared at **6.2 s** (quickstart
unhidden at template.html:2230). No layout shift (CLS 0.002), but the
door the hero exists for arrives ~5 s after the room. **Treatment:** the
label is static in practice (brief 01) — ship the pill visible in the
built HTML as a plain link to `/b/01` and let JS upgrade it in place to
the copy button.

**W7 · S4 · unframed wait · lens 4 — The majority copy path starts a
10–20 minute wait without ever saying so.** The conductor hint says
"(~15 min each)" (template.html:1254) and #how says "go get coffee"
(template.html:612), but the single-brief post-copy toast — the majority
path — names the artifact and never the duration (showCopyHint,
template.html:1217–1235; same in gp-detail.js showHint:122). The first
real wait of the product begins with no ceiling. **Treatment:** the same
two words in both toasts: "…it writes `BUGS.md` at the root (~15 min)."

**W8 · S4 · unshaped · lens 3 — Quick view says "loading…" then pops.**
Observed under a 4 s bodies delay: the panel holds bare "loading…" text
(template.html:1594), then the full ~3 KB brief lands at once and the
card expands to full height in one jump. Acknowledged and honest, and
usually instant (prefetch + SW) — lowest priority. **Treatment if ever
touched:** reserve a few lines of min-height on `.body` so the expansion
is one motion, not two.

**W9 · S4 · serialized wait · lens 6 — The Studio demo fetches its four
sample reports one at a time.** studio.html:802–806 awaits each
`/reports/<name>` in sequence, so the first-touch demo pays 4 round trips
where 1 would do on high-latency links (code-cited; local runs are too
fast to feel it, and SW interception hid per-request delays from the
probe). The per-file `addReport` → render is already progressive — keep
that. **Treatment:** fetch all four in parallel, add in order.

## 2 · The hot path

The one action this product exists for: **copy → paste → a report lands.**
Step by step today: (1) land — hero readable at ~1.3 s even at 40 KB/s,
though the quickstart door arrives at 6.2 s there (W6); (2) click copy —
instant when warm (94 ms on `/b/01`), frozen-silent when cold on a slow
network (W1); (3) paste into the agent — the toast names the artifact but
not the ~15 min (W7); (4) the run itself — narrated per stage by the
conductor with an explicit no-silence rule and a closing ranked list
(build.py:230, 239, 247): this, the longest wait in the product, is its
*best*-handled wait; (5) return next week — pays full network for a page
sitting byte-identical in cache (W2). Target: every copy acknowledges
within 100 ms in all cache states, every return opens in ~100 ms from
cache, and the paste moment states its price once.

## 3 · Optimism candidates

Architecturally short list — the no-backend charter means nearly every
write is local and already instantaneous-with-undo (run marks, Studio
checks, sequence edits; POLISH's undo primitive covers the failure
story). Two waits must stay pessimistic and one candidate remains:
- **Copy buttons may never claim success early** — "Copied ✓" before the
  clipboard write resolves would repeat the AN2 bug the product already
  fixed (template.html:1276–1278). W1's fix is acknowledgment, not optimism.
- **Candidate: Studio re-add of a known report** (the post-Fixer "reload
  the reports" ritual, studio.html:917): with DEFAULTS Q2's remembered
  repo ref, the reload could render the cached copy instantly, refresh
  from GitHub behind, and reconcile — failure story: a note that the
  refresh failed and the view shows the previous version.

## 4 · Honesty fixes

- **W3** — "loading…" concealing a 22-request probe, and a 403 reported
  as "no files found" (studio.html:766). The one place the product tells
  the user something false about their own repo.
- **W7** — the unstated ~15 min on the majority copy path; the conductor
  path already tells the truth (template.html:1254).
- **W2's lie-fi corner** — network-first with no timeout means a hanging
  network shows a blank tab forever while a complete offline copy sits
  ready; a timeout-to-cache makes the wait's ceiling real.
- Everything else checked out honest: `mark_run` fires only on confirmed
  action, copy success only on a confirmed clipboard write, Studio's
  parser names what it skipped (studio.html:516–524), and no progress
  indicator anywhere fakes a percentage.
