# Social Proof & Credibility

*What evidence does this product offer a skeptical stranger that others use it,
trust it, and got value — and where does doubt win? Read-only pass over the
landing (`template.html`), README, examples (`examples/`), Studio, and the
`install` path.*

**Honesty note (this project's own rule, and this brief's):** every
recommendation below is *collect real proof* or *place existing real proof
better*. Nothing here suggests fabricating a testimonial, a logo, or a number.

**Verdict:** the product's credibility rests almost entirely on **dogfooding** —
it audits its own repo in the open, ships the real reports, and even publishes a
Venture verdict that rules *"pivot," not a reflexive "go."* That is genuinely
strong, honest proof, and it's rare. The gaps are two: (1) there is **no
evidence anyone else uses it** (no stars, installs, testimonials, or named
maintainer), and (2) the **real reassurance that already exists is placed away
from the decisions where fear peaks** — most glaringly, the checksum-verified
installer is invisible at the `curl … | sh` line.

> **Backlog reconciliation (2026-07-09).** Dispositions: **F1** (checksum
> reassurance absent at the scary `curl | sh` line) — **FIXED**: the install card
> now shows "✓ SHA-256 verified before install · read the script first," surfacing
> the installer's real, already-shipped verification. **F6** (partner band implies
> a real partnership) — **FIXED**: labeled an example. **F2** (no third-party
> proof), **F3** (unverifiable HN quotes), **F4** (proof placed far from the
> claim), **F5** (no named maintainer) — **DEFERRED**: each needs real assets or a
> personal decision; this brief's own rule is *collect real proof, never
> fabricate*, so they stay for the maintainer. See `FIXLOG.md`.

---

## 1 · Proof inventory

| Signal | Where it lives | The claim it backs | How credible |
|---|---|---|---|
| **Dogfood: real reports + FIXLOG** | Proof `template.html:556-571`; `examples/index.html` | "It works — real output, real commits" | **High** — verifiable, specific, self-hosted |
| **"Real reports, not screenshots"** | `:562` | Honesty / anti-marketing stance | **High** — and the files are inspectable |
| **Venture verdict = "pivot," not "go"** | `examples/index.html:59,73` | "The method is honest, not a hype engine" | **High** — self-disconfirming proof is the most trusted kind |
| **Read-only · ends by asking · local** | guard cards `:425-429` | "Safe for your code / no exfiltration" | **High** — matches the linter-enforced brief behavior |
| **MIT-licensed & free** | hero micro `:391`, footer `:585` | "No cost, no lock-in" | **High** — verifiable via LICENSE |
| **Open source / GitHub link** | footer `:582` | "Real, inspectable project" | **High source — but no stars/forks/activity shown** |
| **Checksum-verified installer** | `install:17-24` ("Checksum verified.") | "Safe to `curl \| sh`" | **High — but absent from the page**; lives only in the script |
| **3 developer quotes** | Problem `:406-408` | "Agents are inconsistent" (the *problem*) | **Low-Med** — anonymous ("a developer, Hacker News"), unlinkable; backs the problem, not the product |
| **"N run here" counter** | `herostat` `:776-777` | — | **Not social proof** — it counts the visitor's *own* local runs |

Pattern: strong **first-party** proof (dogfood, transparency, safety);
near-zero **third-party** proof (nobody else is shown using it); and the safety
proof that exists is not where the scared visitor is looking.

---

## 2 · Findings (lens · location · doubt left unanswered · fix · effort)

Ranked by doubt removed at the moment of decision.

### F1 — The scariest action has no reassurance in eyeshot *(lens 8: security · lens 3: proof at the decision)* — **HIGH · effort S**
- **Location:** the install card, `template.html:542` — `curl -fsSL https://goal-prompts.vercel.app/install | sh`, shown bare with only a "copy" button.
- **Doubt unanswered:** "Piping a stranger's script straight into my shell — is this safe?" The single most fear-inducing step on the site stands completely alone.
- **The irony:** the reassurance already exists. `install:17-24` fetches `checksums.txt`, verifies SHA-256, and *refuses to install on mismatch* ("Checksum verified."). The proof is real — it's just buried in the script and a SECURITY.md finding.
- **Fix:** put it at the decision. Beside the command: "✓ SHA-256 verified before install · read the script first" with links to `/install` and `/checksums.txt`. Do the same for the MCP line (`:549`) — "runs from source on GitHub, inspect it."

### F2 — No evidence anyone else uses it *(lens 2: specific over generic · lens 6: numbers that reassure)* — **MED-HIGH · effort M**
- **Location:** whole site — confirmed absence. No GitHub stars/forks, no install or download count, no "used by," no testimonials.
- **Doubt unanswered:** a skeptic's first question — "does anyone actually use this, or am I the first?" The dogfood proves it *works*; it doesn't prove it's *adopted*.
- **Fix (honest):** display *real* GitHub stars/forks (a live shields.io-style badge, or fetched at build) once the number reassures rather than deflates; surface any genuine install/MCP metric you can measure *without breaking the "nothing leaves your machine" promise*. If the numbers are still small, don't manufacture them — lean harder on the dogfood proof (F5) until real adoption exists to show. **Never invent counts or testimonials.**

### F3 — The developer quotes are unverifiable *(lens 5: credibility of source · lens 7: honesty)* — **MED · effort S**
- **Location:** `template.html:406-408` — three quotes attributed to "— a developer, Hacker News" and "— the workaround everyone rebuilds by hand."
- **Doubt unanswered:** "Are these real, or written by the site to sound like real developers?" Unlinkable quotes read as invented to a skeptic, and they only back the *problem* anyway.
- **Fix:** if the quotes are real, link each to its source HN comment so it's verifiable — a linked real quote is worth ten anonymous ones. If they're paraphrased sentiment, frame them explicitly as such ("what developers keep saying, paraphrased"). Don't present unlinkable text as literal testimony.

### F4 — The strongest proof is placed last, far from the claim it backs *(lens 1: proof beside the claim · lens 3)* — **MED · effort S**
- **Location:** the dogfood Proof section is the final content block (`:556-571`), under the soft headline "It audits its own code, too" (`:558`); the claim it backs ("senior code auditor," "evidence-backed") is made in the hero (`:383-386`), screens above.
- **Doubt unanswered:** the visitor forms a "trust me" impression at the hero and only meets the receipts at the very end — many bounce first.
- **Fix:** pull one dogfood proof line up next to the hero or the Payoff — e.g. "Don't take our word for it: here are the reports it wrote about its own code →" linking `/examples/`. Proof belongs beside the claim.

### F5 — No human behind the project *(lens 5: credibility of source)* — **LOW-MED · effort S**
- **Location:** the site is anonymous except the GitHub handle "GhostlyGawd" (footer `:582`). No name, face, role, or "built by."
- **Doubt unanswered:** "Who made this, and are they credible?" Common for OSS, but a real maintainer identity converts skeptics.
- **Fix (optional, honest):** a small "built by <name>" with a link (GitHub/X/site). Only if the maintainer wants to attach their name.

### F6 — The partner band implies a partnership that doesn't exist *(lens 2 · lens 7: no borrowed trust)* — **LOW-MED · effort S**
- **Location:** partner band `:500-515` — "Partner Tool" with a placeholder "P" logo (`:511`), "Partner Tool × Goal Prompts."
- **Doubt unanswered:** a visitor can't tell if this is a real partner or a mockup; a fabricated-looking logo *costs* trust on a page meant to build it.
- **Fix:** until a real partner exists, label it unmistakably as an example/template. Never imply an existing partnership. (Shared with SHOWCASE F6 / CRO F5.)

### What already earns trust — keep it
- **Dogfooding with real, inspectable reports and a FIXLOG** — the best proof on the site.
- **Self-disconfirming honesty** — the "pivot, not go" verdict and "Real reports, not screenshots" signal a project that won't oversell. Rare and valuable; protect it.
- **Risk-reversal guards** (`:425-429`) and **MIT/open/local** — strong, verifiable trust primitives.
- **A checksum-verified installer** — genuinely more careful than most; it just needs to be *seen*.

---

## 3 · Proof at the decision (what to place where, in order)

1. **Hero CTA (`:387-391`):** the offer line (free · no signup · local) + one dogfood proof link ("see the reports it wrote about its own code →"). *(F4)*
2. **Copy button (`:252`):** reassurance that you can *read the full prompt before copying* — the `view` toggle (`:260`) already exists; frame it as "inspect before you copy." Low fear here, but it compounds.
3. **Install `curl | sh` (`:542`):** "✓ SHA-256 verified · read the script" + links to `/install` and `/checksums.txt`. **Highest-value placement on the site.** *(F1)*
4. **MCP command (`:549`):** "runs from source on GitHub — inspect it" link. *(F1)*
5. **Partner band (`:500-515`):** a real "Partner with us →" contact CTA (CRO F5), and either a real partner or an explicit "example" label. *(F6)*

Rule applied: put the reassurance where the fear is. Today most of it sits in the
footer, the script, or the last section.

---

## 4 · Proof to earn (credibility to collect, not invent)

- **Real GitHub stars/forks** — display them live once they reassure; they're the
  most natural third-party signal for an OSS dev tool.
- **Genuine testimonials** — add a low-friction way to collect them: a "share
  what a brief found in your repo" prompt, a GitHub Discussions/Issues link, or a
  short form. Publish only real, attributed ones (link the author).
- **Verifiable versions of the HN quotes** — source links (F3).
- **A privacy-respecting usage signal** — only if measurable without violating
  "nothing leaves your machine" (e.g. anonymous, opt-in, or GitHub-side install
  counts). Don't trade the local-first promise for a vanity metric.
- **A named maintainer** and, eventually, **third-party mentions/press** — pitch
  the dogfood story; it's the hook.

---

## Report only — which fixes do you want me to make?

This was a read-only pass; nothing was changed. The highest-leverage, fully
honest, ship-now fix is **F1** — surfacing the already-real checksum verification
and "inspect the script" links at the `curl | sh` and MCP commands. **F3** (link
or reframe the quotes), **F4** (move a dogfood proof line up), and **F6** (label
the partner mockup) are also safe and cheap. **F2** and **F5** require real
assets/decisions (adoption numbers, maintainer identity) — I won't fabricate
those; tell me what's real and I'll place it well.

Tell me which fixes to implement (any subset). I'll make only the changes you pick.
