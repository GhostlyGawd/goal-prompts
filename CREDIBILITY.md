# Credibility plan — proof for a young, honest, solo project

Status of the four "needs real assets/data/identity" items from the PROOF and
SHOWCASE audits, and the approach for each. Snapshot of the state that shapes
every call: **repo is days old, 0 stars / 0 forks, solo maintainer, Discussions
off, privacy-first ("nothing leaves your machine").**

## The through-line
At this stage credibility can't come from *social proof we don't have yet* — a
"0 stars" badge or an unlinkable "Hacker News" quote would both backfire **and**
betray the honesty that is the product's actual edge. So the strategy is:

> Show the product is real and works (a demo + a real maker), and build the proof
> **mechanisms** so social proof surfaces automatically the moment it's genuine —
> never faked, never premature.

Two items ship now; two are armed to fill with real data as it accrues. Nothing
is fabricated.

---

## 1. Product demo — SHOWCASE F1 · **held for a real recording**
With no stars or quotes yet, a short clip of a brief actually auditing a repo is
the strongest proof we can *own*. A real recording beats any CSS reconstruction,
and it's a ~15-minute task — so this is deliberately held for that asset rather
than shipped as a stand-in an agent can't visually vet.

**Recording recipe (10–15s, drop it in the Payoff or hero):**
1. Open Claude Code (or Cursor) on a small, real sample repo with a couple of
   genuine bugs.
2. Copy `01 · Bug Hunt` from the catalog and paste it into the agent.
3. Screen-record: paste → the agent audits read-only → `BUGS.md` is written with
   ranked, cited findings. Trim to the paste-through-report beat.
4. Export as **muted MP4 + WebM with a poster frame** (not a GIF — a 10s GIF is
   5–15 MB and grainy; the video is ~0.5–1 MB and crisp).
5. Send it over; it gets wired in responsively — `prefers-reduced-motion` shows
   the poster only, lazy-loaded, placed to protect first paint.

*Fallback if you'd rather not record:* an honest CSS/SVG reconstruction of the
same flow using real brief + real report text, clearly a stylized demo. Say the
word and it ships as a placeholder until the recording exists.

## 2. Maintainer identity — PROOF F5 · **shipped (handle level)**
A genuine first-person maker out-converts an anonymous catalog, and forcing a
legal name on a handle-based identity would be wrong. Shipped now: a footer line
**"Built by [@GhostlyGawd](https://github.com/GhostlyGawd), an independent
developer"** — real, public, invented nothing.

**To strengthen (your words):** a 1–2 sentence origin note (e.g. *"I got tired of
re-explaining the same audit to my agent, so I wrote the good ones down"*) and,
if you want to go un-pseudonymous, a real name + photo + link. Send them and they
get added; nothing is invented in the meantime.

## 3. Adoption metric — PROOF F2 · **armed, hidden at 0**
A live stars badge would advertise a zero **and** fire an external request on a
privacy-first site. So the mechanism is built to stay silent until it's real:

- `metrics.json` holds the true star/fork count; `build.py` bakes it into the
  static page (no runtime request) and renders the badge **only at/above
  `STAR_THRESHOLD` (25)**. Below that: nothing. Today (0 stars) it shows nothing.
- `scripts/refresh-stars.py` (stdlib) refreshes `metrics.json` from the live repo
  on demand / in a deploy hook, keeping the build itself offline + deterministic.
- The real work is *earning* the first stars (a launch / "Show HN"); the badge
  follows adoption, it can't manufacture it.

**Durable upgrade later:** publish the MCP server / installer to **npm** → an
honest, growing **downloads** count (also clears the `IMPROVEMENTS` npm item).
No "used by" logos — there are no real partners (the partner band is a labeled
mock).

**Needs you:** confirm the threshold (default 25), and a yes/no on npm publish.

## 4. Developer quotes — PROOF F3 · **honest paraphrase kept; pipeline to real**
A days-old repo has no real HN thread, so the quotes are representative, not
sourced. The only honest states are *real + linked* or *clearly paraphrased* — an
HN attribution with no link reads as fabricated. Kept as representative sentiment
(no faux attribution). To move toward real, linked quotes:

- Enable **GitHub Discussions** (currently off); the footer already carries a soft
  *"using it? tell me how ↗"* prompt (points at Issues until Discussions is on).
- Search HN / Reddit / X for genuine mentions; link any real one verbatim.
- Swap paraphrased → real + linked as they arrive.

**Needs you:** are the three quotes real (send links) or illustrative (keep
paraphrased)? And OK to enable Discussions?

---

## Decisions that unlock the rest
- The **demo recording** (recipe above) — the single biggest unlock.
- One sentence on **why you built it** (+ optional real name/photo).
- Star **threshold** + **npm publish** yes/no.
- Quotes **real-or-illustrative**, and **enable Discussions**.
