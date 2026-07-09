# Comprehension Audit

*Can a first-time visitor form a correct mental model — what it is, who it's for, how it works, why it beats the alternative — from the public surfaces alone?*

Read-only pass over the surfaces a stranger meets first: the landing page
(`template.html` → `index.html`), the GitHub `README.md`, the Report Studio
(`studio.html` → `/studio`), the catalog's question-led finder, and the sample
reports page (`examples/index.html`). No signup exists — this is a static,
copy-paste catalog — so "the first screen after signup" maps to the first brief
you copy.

**Verdict:** the *method* is explained unusually well (a rare strength — the
four-phase pipeline and a real sample report are both *shown*, not asserted).
The gap is one level up: the hero never names **what the thing physically is**.
A newcomer learns *what the agent does* before they learn *that they are looking
at a catalog of copy-paste text prompts*. Two core nouns — "brief" and
"conductor" — are used before they are defined, and the catalog's size is stated
four different ways, none of them the true number (129).

> **Backlog reconciliation (2026-07-09).** Dispositions: **F2** (catalog size
> stated four stale ways) — **FIXED**: `build.py` injects the live brief /
> playbook / family counts into the meta + OG descriptions, hero, and chart, and a
> build guard keeps the README count and family taxonomy in sync (the true number
> is now 135, not the 129 this audit measured — exactly the drift the injection
> ends). **F4** ("conductor" unglossed) — **FIXED**: the custom-sequence bar's
> copy button carries a one-line gloss. **F5** ("MCP" unexpanded) — **FIXED**:
> expanded to "MCP (Model Context Protocol)" on first use. **F1** (hero never
> names the artifact) & **F3** (gloss "brief") — **DEFERRED**: the hero rewrite is
> a wording decision for the maintainer (the report asks "my wording or yours?").
> See `FIXLOG.md`.

---

## 1 · Mental-model gap (intended vs honest ten-second read)

| Surface | Intended one-liner | Honest read after ~10s cold | Gap |
|---|---|---|---|
| **Landing hero** (`template.html:382-391`) | "A free catalog of copy-paste prompts that make your coding agent run a consistent, evidence-backed audit of your repo." | "Some product that turns my AI agent into a code reviewer and gives me a report. Is it an app? A CLI? A service I sign up for? What do I actually get?" | The **artifact is never named**. "Copy", "paste", "prompt", "catalog" appear nowhere in the first screenful. |
| **README** (`README.md:1-7`) | Same as hero, plus scale. | "Okay — *eighty-one* prompts, 4-phase audit, one report, MIT. Got it." | Clearer than the hero on *what it is* ("mission briefs… produces a single report file"), but the count (81) is wrong and disagrees with the site (75/129). |
| **Report Studio** (`studio.html`, `/studio`) | "Paste the reports your audits produced; findings become a checklist and one tap builds a Fixer prompt." | "This is step 2 of something — I'm supposed to already *have* reports named BUGS.md. Where did those come from?" | Assumes you've already run briefs. A visitor who lands here first (it's in the top nav) meets the middle of the story. |
| **Catalog finder** (`template.html:464`, `buildFinder()` 1166) | "Start from a goal, or pick the question you care about." | "Good — 'start with a goal', then 17 questions like *does it work? / is it safe?* I can navigate this." | Works well. A genuine strength; not truly an "empty state." |
| **Sample reports** (`examples/index.html`) | "Here's real output, run against this very repo." | "Concrete — real BUGS.md, SECURITY.md, and a FIXLOG of commits. Now I believe it." | Strong. Best proof surface on the site. |

**Takeaway:** the further down the page (or the deeper the link), the *better*
the comprehension gets. The weakest point is the very first screen — exactly
where a stranger decides whether to stay.

---

## 2 · Findings (lens · location · what a newcomer misunderstands · fix)

Ranked by cost. A wrong "what is this" loses the visitor before anything else
can help, so it leads.

### F1 — The hero never names the artifact *(lens: What is this / One-sentence test)* — **HIGH**
- **Location:** hero, `template.html:382-386` — eyebrow "An open reference for code audits", H1 "Turn your coding agent into a senior code auditor.", sub "Point it at your repo. Every brief runs the same four-phase audit and files one evidence-backed report you can act on".
- **Wrong belief:** "This is a tool / SaaS / agent I sign up for and run." The truth — *you copy a block of text and paste it into your own agent; there is nothing to install and no backend* — is never stated up top. The words that would fix it ("copy & paste", "prompt", "nothing to install") first appear far below in "Three ways in" (`template.html:534-535`).
- **Fix:** name the category in the eyebrow or sub. E.g. eyebrow → "Free, open catalog of copy-paste audit prompts"; add to sub "Copy a brief — a ready-made prompt — into Claude Code, Cursor, or any agent."

### F2 — Catalog size is stated four ways, none correct *(lens: What is this / Concrete over abstract)* — **HIGH**
- **Location & exact words:**
  - `README.md:3` — "**Eighty-one** mission briefs"
  - `template.html:7` meta description — "**75 briefs**"
  - `template.html:9` og:description — "**75 briefs**, 15 playbooks"
  - `template.html:391` static hero — "**75 briefs** · 15 playbooks"
  - `template.html:396` static chart caption — "**76 briefs total**"
  - **Actual:** 129 briefs, 32 playbooks (`catalog.json`, `playbooks.json`).
- **Nuance:** the *rendered* hero and chart self-heal at runtime — `renderStats()` (`template.html:772-778`) rewrites the hero to `DATA.length + " briefs · " + PLAYBOOKS.length + " playbooks"` and line 1161 rewrites the chart caption to `DATA.length`. So a visitor with JS sees "129 briefs · 32 playbooks." **But the meta description, the OG/Twitter card, and the README do not run JS** — and those are the *true* first impression in Google results, Slack/X unfurls, and the GitHub repo page.
- **Wrong belief:** "A small, possibly-stale catalog of ~75 prompts." Undersells the real scope by ~40%, and the internal disagreement (75 vs 76 vs 81) reads as neglect.
- **Fix:** give the static surfaces one source of truth. Have `build.py` inject the real counts into the meta/OG tags and print a count the README references, so no number is hand-typed.

### F3 — "brief" is the core noun, used before it's defined *(lens: Curse of knowledge)* — **MED-HIGH**
- **Location:** first use in the hero sub `template.html:386` "Every **brief** runs the same four-phase audit"; the word then recurs in every section. It is only *defined by demonstration* at "Three ways in → Copy & paste" (`template.html:534`) — "Tap Copy on any brief and paste it into your agent."
- **Wrong belief:** a reader may picture a legal brief, a design brief, or the *report* itself — not "a copy-paste prompt." (Classified as **explained too late**, not never.)
- **Fix:** gloss on first use — "each brief (a ready-made prompt)".

### F4 — "conductor" appears with zero explanation *(lens: Curse of knowledge)* — **MED**
- **Location:** the custom-sequence bar, `template.html:520-522` — label "conductor" and button "copy conductor". It surfaces the moment a visitor taps "+ seq" on two cards; a bar slides up reading "CONDUCTOR … copy conductor" with no gloss. (Also unglossed in `README.md:43-44`.) This is *precisely* the kind of prompt that is running this playbook — yet the landing page never says what a conductor is. (Classified as **never explained** on the page.)
- **Wrong belief:** "What is a conductor, and what will 'copy conductor' put on my clipboard?"
- **Fix:** one line of helper text in the seqbar — "one prompt that runs these briefs in order."

### F5 — "MCP" is not expanded *(lens: Curse of knowledge)* — **LOW-MED**
- **Location:** "Three ways in → Call it from an agent", `template.html:547-548` — "An **MCP** server gives any agent `list_briefs`, `suggest_briefs` & `get_brief` mid-conversation." (Classified as **explained in jargon**.)
- **Wrong belief:** a reader who doesn't already know "Model Context Protocol" skips an entire integration path as not-for-them.
- **Fix:** expand once — "An MCP (Model Context Protocol) server…".

### What already works — keep these
- **How it works is *shown*, not asserted** (`template.html:414-429`): the Explore → Audit → Curate → Report → Act pipeline plus three guard cards ("Read-only by default", "It ends by asking", "Everything stays local"). This answers the "how" lens better than most sites.
- **The mechanism has a worked example** (`template.html:446-454`): a rendered `BUGS.md` with its real section structure. Concrete over abstract, done right.
- **The audience's pain is named in their own words** (`template.html:402-410`): "AI coding agents are powerful — and maddeningly inconsistent," backed by real developer quotes. Strong "who it's for."
- **Why-this-why-now lands the alternative** (`template.html:410`): "The fix isn't a bigger model — it's **structure**." Names and beats the status quo (freehand prompting).

---

## 3 · First-screen rewrite

The hero is one edit away from passing. Keep the H1 — the "senior code auditor"
metaphor is good. Name the artifact, fix the count, and state the
no-install/no-backend fact up front (it's a real differentiator buried on line 428).

**Current** (`template.html:382-391`)
> *An open reference for code audits*
> **Turn your coding agent into a senior code auditor.**
> Point it at your repo. Every brief runs the same four-phase audit and files one evidence-backed report you can act on — no more random, throwaway results.
> *75 briefs · 15 playbooks · install in one line · MIT licensed & free*

**Proposed**
> *Free, open catalog of copy-paste audit prompts*
> **Turn your coding agent into a senior code auditor.**
> Copy a **brief** — a ready-made prompt — into Claude Code, Cursor, or any agent. It runs the same four-phase audit on your repo and files **one evidence-backed report** you can act on. No install, no backend, nothing leaves your machine.
> *129 briefs · 32 playbooks · copy-paste or install in one line · MIT-licensed & free*

Every added word answers a question a stranger is actually asking on screen one:
*what is it* (catalog of prompts), *how do I use it* (copy-paste), *what do I get*
(one report), *is it safe/free* (local, MIT).

---

## 4 · Explain-it-back script

The three sentences a newcomer should be able to repeat after one screen — and
where each is taught **today**:

1. **"It's a free, open catalog of ready-made prompts ('briefs') for AI coding agents."**
   *Today:* taught only implicitly — the site name plus "Three ways in → Copy & paste" (`template.html:534`). **Not in the hero.** → the F1/F3 fix moves it up.
2. **"I copy one into my agent; it audits my repo with a fixed four-phase method and writes one evidence-backed report file."**
   *Today:* well taught — hero sub (`:386`) + the How-it-works pipeline (`:418-424`) + the sample `BUGS.md` (`:446-454`). Keep.
3. **"It's read-only and asks before changing anything; then the Studio and the Fixer turn the report into commits."**
   *Today:* well taught — the guard cards (`:425-429`) and the Proof/Studio sections (`:556-571`) — but gated behind the unglossed nouns "Fixer" and "conductor" (F4). Gloss them and this sentence is safe.

Sentences 2 and 3 already land. **Sentence 1 is the one a stranger can't yet
say from the first screen** — and it's the one that decides whether they read on.

---

## Report only — which fixes do you want me to make?

This was a read-only pass; nothing was changed. Candidate fixes, cheapest-first:

- **F2 (counts):** wire the real brief/playbook counts into the static meta/OG
  tags and README via `build.py` — highest credibility-per-effort, and it stops
  the numbers drifting again.
- **F1 + F3 (hero + "brief"):** apply the first-screen rewrite above.
- **F4 + F5 ("conductor", "MCP"):** one-line glosses.

Tell me which of these to implement (any subset), and whether the hero rewrite
should match my proposed wording or your own. I'll make only the changes you pick.
