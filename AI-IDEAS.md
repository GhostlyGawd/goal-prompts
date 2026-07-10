# AI-IDEAS.md — AI Opportunity Scan

**Date:** 2026-07-09
**Auditor:** ai-opportunity brief, read-only pass
**Prior run:** none — no previous `AI-IDEAS.md` existed; this is the first AI scan.
**Companion evidence:** `FUNNEL.md` (instrumentation & flows), `COMPETITIVE.md` (moat & do-not-copy), `REVENUE.md` (Teams/sponsorship rails) — all written today; cited rather than re-derived.

---

## 0 · The framing that governs everything below

This product has a hard architectural stance: **static site, no backend, no accounts, "nothing leaves your machine"** (`template.html:502`, `vercel.json` — no functions, no storage). Any AI feature that requires a runtime model call *from the product* needs either a backend or a user-supplied API key — both violate the stance that `COMPETITIVE.md` §9 identifies as the differentiation.

But the product is not AI-poor — it is AI-shaped in an unusual way: **its runtime LLM is the user's own coding agent.** Three AI features already ship in this form and prove the pattern:

- **Brief 46 · Audit Triage** (`prompts/act/46-audit-triage.md`) — natural-language "which audit do I need?" answered by the agent, with repo access, where the question is actually decidable.
- **The Fixer composer** (`studio.html:307`, `buildFixer`) — checked findings compiled into a targeted prompt; the model work happens in the agent.
- **Conductors** (`makeConductor` in `js/catalog-core.js:94`, `make_conductor` in `mcp/server.cjs`) — multi-brief orchestration as a composed prompt.

So the viable AI surfaces here are exactly three shapes, and every idea below fits one:
**(A) composed prompts delegated to the user's agent** (zero cost, zero latency, zero privacy risk to the product), **(B) offline/build-time AI producing committed static artifacts** (maintainer's key, runs never per-visitor), and **(C) CI-time AI** (maintainer's key, runs per-PR). Runtime in-browser AI is on the gimmick list wholesale.

---

## 1 · Raw material summary

**Data the product holds:**

| Data | Where it accumulates | Notes |
|---|---|---|
| 141 brief bodies, heavily structured (4-phase skeleton, front matter, <4k chars) | `prompts/<family>/*.md`, mirrored to `raw/`, `catalog.json` | The corpus. Machine-linted (`build.py:102` `lint()`, `lint_catalog`) — the moat per `COMPETITIVE.md` §6.1 |
| Curated sequences + merchandising fields | `playbooks.json` | 35 playbooks |
| Sample outputs (real Day-1 run) + FIXLOG | `examples/`, `FIXLOG.md` | Proof corpus, currently underused |
| Per-user state — Operator context, run marks, custom sequence, Studio checks | browser localStorage only (`gp-ctx`, `gp-runs`, `gp-seq`, `gp-studio-checks`) | Device-bound, thin, and `gp-runs` is currently falsified by copy-time auto-marking (`FUNNEL.md` §2) |
| User audit reports (transient) | dropped into Report Studio, parsed client-side (`js/report-parser.js`) | May contain private code — must never leave the browser |
| Analytics events incl. `search_zero{q}` (`template.html:1264`) | Vercel Web Analytics, landing + Studio only | The one signal of unmet search intent; `/raw/*` fetch counting designed but not live (`docs/usage-metrics.md`) |

**Tedious multi-step tasks, traced:**

1. **Authoring a brief** (maintainer, contributor, future Teams customer): idea → front matter with unique id/family/output/tagline → 4-phase skeleton → ask-first gate → <4k chars → `related:` ids → `scripts/check`. Many linter rules to satisfy by hand; 141 exemplars exist to imitate.
2. **Choosing among 141 briefs**: six parallel choosers (`FUNNEL.md` §1 Choose row) — the site-side answer is rules; the good answer already exists as brief 46.
3. **Filling the Operator-context box** (`template.html:600–608`): four free-text fields the user types from memory about their own repo, while an agent that knows the repo sits one window away.
4. **Post-Studio next step**: after ticking findings the only output is a Fixer prompt; merging *multiple reports into a plan* means leaving the Studio to find brief 28.
5. **Keeping search good**: `search_zero` queries have no closing loop — nobody turns misses into synonyms.
6. **Semantic quality review of briefs** (maintainer): the linter checks structure; house rules like "read-only posture stated", "tagline matches body", "doesn't duplicate an existing brief" are reviewed by eye.

**Judgment calls the product could draft:** which brief next (46 covers it), severity/priority of findings (deterministic parser covers it — deliberately), what a new brief should say (nothing covers it — the biggest gap).

---

## 2 · Ideas (survivors)

### Idea 1 — Brief Forge: an authoring copilot that drafts linter-passing briefs
- **User moment:** a contributor reads `CONTRIBUTING.md` / "Add a prompt" (`README.md:198`) and faces a blank file with ~10 house rules; a Teams customer needs org-specific briefs (`REVENUE.md` §2 — "custom briefs passing the linter" is the paid deliverable). Today both start from zero.
- **Data needed:** have it all — 141 exemplar briefs, the linter's rules (`build.py:102–171`), the family list, the 4-phase skeleton. Nothing to collect.
- **Failure mode:** a drafted brief is subtly wrong (too vague, overlaps an existing brief, unsafe posture). Fallback is already built: `scripts/check` is a hard gate for structure, and a human PR review is the gate for content — the copilot's output is a *draft PR*, never a published brief. Wrong answers cost review time, not catalog quality.
- **Cost & latency:** one agent run per new brief (rare event, maintainer/contributor-initiated); zero cost to the product — shape A, the user's own agent does the work.
- **Build shape:** prompt-only + tool use — a meta-brief ("author a new goal-prompts brief") that embeds the skeleton, the linter rules, and two exemplars, instructs the agent to write `prompts/<family>/NN-slug.md`, run `python3 build.py`, and iterate until green. Ships as a doc page + a copyable prompt; optionally as a repo `.claude/commands/` file.
- **Beats the boring alternative?** Yes — the boring alternative is a markdown template, which already implicitly exists (any brief file) and still leaves all the judgment (phases, lenses, tagline, related ids) to the human. Drafting is exactly what a model is for; the linter makes wrongness cheap.
- **Value: High** (unlocks contributions — `COMPETITIVE.md` §3.5 table stake — and is the production line for the Teams offer). **Feasibility: High** (one markdown file; no site code).

### Idea 2 — Semantic linter tier: an LLM review pass in CI for changed briefs
- **User moment:** maintainer reviewing a brief PR (their own or, post-Idea-1, a contributor's). `build.py` catches structure; the human alone catches "this brief isn't actually read-only in spirit", "tagline oversells", "this duplicates brief 27".
- **Data needed:** have it — the diffed brief, the full catalog for overlap checks, the house rules (currently implicit in `CLAUDE.md` + `CONTRIBUTING.md`; writing them down is half the work).
- **Failure mode:** false positives annoy; false negatives are status quo. Fallback: the pass is **advisory only** — a PR comment, never a blocking check. The deterministic linter remains the only gate; CI cost of wrongness is one ignorable comment.
- **Cost & latency:** one model call per brief-touching PR (rare; repo is one-maintainer today). Maintainer's `ANTHROPIC_API_KEY` in Actions — the repo already models exactly this pattern in `.github/run-brief.example.yml`. Cents per PR, latency irrelevant (async CI).
- **Build shape:** prompt-only in a GitHub Action (shape C). No site code, no runtime surface.
- **Beats the boring alternative?** Yes — the boring alternative *is already built* (the regex linter) and provably can't read semantics; this deepens the one moat rivals lack (`COMPETITIVE.md` §6.1) and makes "every brief passes a published linter + a semantic review" a true marketing sentence.
- **Value: Medium-High** (moat maintenance; scales the moment contributions arrive). **Feasibility: High.**

### Idea 3 — Studio "Copy Synthesis prompt": roadmap composition over loaded reports
- **User moment:** Report Studio with several reports loaded and findings ticked (`studio.html`). Today the selection bar offers exactly one exit: "Copy Fixer prompt" (implement now). The other legitimate exit — "merge these into a sequenced plan" — requires knowing brief 28 exists and leaving the Studio.
- **Data needed:** have it — the parsed findings (titles, severities, sections, report names) already in memory client-side; brief 28's method as the template.
- **Failure mode:** the *composition* can't be wrong (it's deterministic templating, same as `buildFixer`); the model work happens later in the user's agent under brief 28's own rules, which end by asking. Fallback if the user's agent produces a poor roadmap: the reports are untouched — read-only by construction.
- **Cost & latency:** zero to the product (shape A); one agent run on the user's side, which is the product's normal unit of work.
- **Build shape:** prompt composition — a `buildSynthesis(findings)` sibling of `buildFixer` plus one button in the selbar. This is "AI feature" in the product's native sense: the AI is delegated, the product contributes the targeting.
- **Beats the boring alternative?** The boring alternative is a static link to `/b/28` — worth having, but it loses the *targeting* (severity counts, which reports, which findings the user prioritized), which is the same value-add the Fixer button already proved.
- **Value: Medium** (completes the act loop the product uniquely owns — `COMPETITIVE.md` §6.2). **Feasibility: High** (mirrors an existing, tested pattern).

### Idea 4 — "Have your agent aim the briefs": Operator-context generated by the user's agent
- **User moment:** the "aim the briefs at your repo" box (`template.html:600`) — four blank inputs (stack / product / stage / watch-out-for) the user must compose from memory. This context rides on *every* subsequent copy (`withContext`, `gp-detail.js:17`), so its quality compounds; today most users plausibly skip it.
- **Data needed:** must collect — but the collector is the user's agent, which has the repo. A copyable mini-prompt ("inspect this repo; answer in exactly four lines: Stack:…, Product:…, Stage:…, Watch out for:…") produces paste-back-able output; the box gains a small "have your agent fill this in" copy link.
- **Failure mode:** the agent's four lines are off — the user sees them before pasting and edits; the box stays free-text. No silent path for wrongness.
- **Cost & latency:** zero to the product (shape A); ~30 seconds of agent time once per repo.
- **Failure of the boring alternative:** repo-recommend's rule table (`catalog-core.js:157–193`) already infers *stack* from `package.json` — but it's JS-centric (Go/Python/Rust match no briefs, lines 181–183) and can never infer *product*, *stage*, or *fragility notes* from a file listing. Those three fields genuinely need judgment over the repo's contents.
- **Value: Medium** (better context → better audits → better first-run aha). **Feasibility: High** (one static prompt string + one link; no parsing needed if output is paste-into-fields).

### Idea 5 — Search alias table, generated offline, tuned by `search_zero`
- **User moment:** catalog search (`template.html:615`). The scorer (`closestScored`) is stemmed-keyword only: "auth" finds nothing labeled "authentication-adjacent trust briefs", "memory leak" doesn't reach 04. The `search_zero{q}` event (`template.html:1264`) already logs exactly these misses.
- **Data needed:** have the corpus; must *accumulate* the miss log (it's live on the landing page today, just unread). V1 can ship from the corpus alone: an LLM pass over all 141 briefs emitting `{alias: [brief-relevant terms]}`.
- **Failure mode:** a bad alias surfaces an irrelevant brief. Fallback by construction: aliases score strictly below direct matches (add as a low-weight haystack field), and the table is a *committed, human-reviewable JSON file* — a wrong entry is a one-line revert, and search without the table is exactly today's search.
- **Cost & latency:** zero at runtime — shape B. Generated by a standalone script run manually with the maintainer's key, committed like `og/` assets; **not** in `build.py` (which must stay stdlib-only per `CLAUDE.md`), so the Vercel build is untouched.
- **Build shape:** offline generation → static artifact consumed by `catalog-core.js` and `mcp/server.cjs` (keeping the parity guard in `scripts/mcp-smoke.cjs` in mind).
- **Beats the boring alternative?** Partially — a hand-written synonym list is the boring alternative and would work for the top 20 aliases. The model earns its place only at corpus scale (141 briefs × their vocabulary) and on the long tail the miss log will reveal. Honest rating: worthwhile, but last among survivors.
- **Value: Medium-Low today** (search volume unmeasured; `FUNNEL.md` says instrumentation first). **Feasibility: High.**

---

## 3 · Value × feasibility ranking

| # | Idea | Value | Feasibility | Shape | Why this order |
|---|---|---|---|---|---|
| 1 | Brief Forge authoring copilot | High | High | A (user's agent) | Serves contributors (table stake), the Teams offer (revenue), and the maintainer; pure content, zero site risk |
| 2 | Semantic linter tier in CI | Med-High | High | C (CI, maintainer key) | Deepens the stated moat; pattern already modeled by `run-brief.example.yml` |
| 3 | Studio "Copy Synthesis prompt" | Medium | High | A | Completes the uniquely-owned act loop; clones a proven code path |
| 4 | Agent-filled Operator context | Medium | High | A | Compounds into every future copy; smallest build of all |
| 5 | Offline search alias table | Med-Low | High | B (offline artifact) | Real but should wait for `search_zero` data to size the problem |

---

## 4 · Gimmick list (rejected — this list protects the roadmap)

1. **Client-side semantic search / embeddings / "chat with the catalog."** 141 items with strong metadata; the keyword scorer, finder, picker, and brief 46 already cover intent-routing. An in-browser embedding model is megabytes of WASM for marginal gain; a hosted one needs a backend or key — both break "nothing leaves your machine." The rule beats the model at this corpus size.
2. **LLM-powered Studio report parser or severity grader.** Would ship users' *private audit findings* to an API (privacy stance violation), add latency to a currently-instant parse, and break the pinned content-hash localStorage keys (`report-parser.js` header comment: "must never change"). The boring alternative is structural: the briefs *author* the report format — tighten the house style at the source, and the deterministic parser stays right.
3. **An LLM inside the MCP server.** `suggest_briefs` is consumed *by* an LLM client that does the semantic reasoning itself; the server's job is fast, deterministic retrieval. Adding a model adds a key requirement, latency, and nondeterminism to a zero-dep server whose whole virtue is having none.
4. **AI-generated brief inflation** (bulk-generating briefs to grow the count). Directly poisons the moat — `COMPETITIVE.md` §9 already rules against the item arms race; the linter's value is that a human + gate stands behind every entry. Idea 1 is the opposite of this: AI drafts, gates decide.
5. **"Your week in audits" AI summary.** The only data is `gp-runs` — thin (id + timestamp), device-bound, and currently *falsified* by copy-time auto-marking (`FUNNEL.md` §2). A template sentence ("5 runs across 3 families") needs no model; any model version launders fake data into confident prose. Revisit never — or only after mark-run is un-faked, as a template.
6. **In-browser LLM repo analyzer** to replace `repoRecommend`'s rules. The browser sees only a file listing and `package.json` via the GitHub API; the agent sees the whole repo. Brief 46 already is this feature, running where the data lives. Extending the rule table (Go/Python/Rust brief mappings) is the correct boring fix.
7. **AI-personalized landing page / copy.** No accounts, no cohorts, no data to personalize on — and a static page that ships identical bytes to everyone is the performance and trust story.

---

## 5 · Prototype-this-week pick

**Idea 1 — Brief Forge**, scoped to one day:

1. Write `docs/author-a-brief.md` (or a `/b/`-style page later): a single copyable meta-prompt embedding (a) the 4-phase skeleton and ask-first gate, (b) the linter's rules restated in prose (id format, family list, tagline constraints, <4k body, `related:` validity — from `build.py:66–171`), (c) two contrasting exemplar briefs (one code-facing like 01, one web-research like 62), and (d) the loop: *write `prompts/<family>/NN-slug.md` → run `python3 build.py` → fix → repeat until green → stop and show the diff*.
2. Test it once: run the prompt in an agent against this repo with a deliberately mundane idea ("audit a repo's error messages"), confirm it converges to a linter-passing draft, then discard the draft (the prototype proves the prompt, not the brief).
3. Link it from `CONTRIBUTING.md` and the README's "Add a prompt" section.

Day-sized because it is pure markdown — no site code, no build change — and it is the one idea that simultaneously advances distribution (contributions), revenue (the Teams production line), and the moat (drafts that arrive pre-shaped for the gate).

---

*Read-only audit — no code, content, or config was changed.* Which idea should I prototype: the Brief Forge authoring copilot, the CI semantic-linter pass, the Studio Synthesis button, the agent-filled Operator context, the offline search alias table — or a specific combination?
