# Launch — positioning one-pager + runbook

The strategy work is done and ruled on (reports/POSITIONING.md, VERDICT.md,
ROADMAP.md). This file is the operational end of it: the positioning
distilled to one page, the launch-day checklist, and ready-to-post drafts.
Nothing here invents new strategy — where it states a position, it cites the
report that chose it.

## The positioning, on one page

**One-liner** (POSITIONING.md Option A, stress-tested against live rival
copy): *Point your coding agent at your repo and get back a filed,
evidence-backed report you can diff, re-run, and act on — the same four
phases every time.*

**Onlyness:** the only audit catalog that carries a finding through to a fix
log — brief → report → Studio → Fixer → FIXLOG. Every rival stops at
"here's a prompt" or "here's a comment"; nobody else owns *after the run*.

**Who it's for first:** the burned solo dev / OSS maintainer who already
hand-rolls prompts and no longer trusts one-off agent output. The DevEx
lead (the eventual buyer) arrives later, via /teams.

**Against:** the habit of doing nothing well — the private prompt doc and
"just rerun it." *Not* against CodeRabbit/Greptile; framing this as cheaper
AI code review is the camouflage trap (POSITIONING.md §3, option B verdict).

**Register:** audit · brief · report · evidence. Never lead with "prompts"
or counts (NICHE.md §3: the tribe is abandoning "prompt"; COMPETITIVE §7:
the audit register is unclaimed).

**Tone rules for every asset below:** claims must be checkable (link the
report, the commit, the linter); the bear case is stated, not hidden; no
number we can't source. The catalog's own evidence rules apply to its
marketing.

## Launch checklist

Shipped in the launch PR (verify on the preview deploy, then forget):

- [x] Loop-first hero, meta, and OG copy (COMPETITIVE §10 bet 1)
- [x] Mobile nav keeps every link — scrolls, never amputates (BLINDSPOTS P0-1)
- [x] Reports render as readable /r/ pages; raw .md one click away (BLINDSPOTS P0-2)
- [x] Storefront curated to 6 featured playbooks; sponsored/collab previews
      off the landing page until real partners exist (ADR-9, BLINDSPOTS F6)
- [x] SECURITY.md policy; report-reading guidance on /examples/ (BLINDSPOTS §5)
- [x] README opens with the loop and a 60-second first report

Maintainer-only, before announcing (each blocks reading or riding the launch):

- [ ] **Turn on raw-fetch counting** (FUNNEL §4 — "don't launch into an
      unreadable funnel"). Zero-code path: Vercel dashboard → Observability →
      filter `pathname:/raw/` — confirm you can see per-path counts. Better:
      a Log Drain (docs/usage-metrics.md, Option 1). The middleware+KV path
      (Option 2) can wait.
- [ ] **npm publish + MCP registry** (CREDIBILITY 3): create an npm
      automation token, add it as the `NPM_TOKEN` repo secret, copy
      `.github/publish.example.yml` to `.github/workflows/publish.yml`, then
      publish a GitHub Release tagged `v<package.json version>` — the
      workflow gates on `scripts/check` and publishes. Makes
      `npx -y goal-prompts` real and lists the server where MCP clients look.
- [ ] **Record the 10–15s run clip** (SHOWCASE F1 — "the single biggest
      unlock"): screen-record `/goal:bug-hunt` running in Claude Code on a
      real repo → BUGS.md appearing → one finding scrolled. No narration, no
      edit. Embed on the landing page proof section and in the HN comment.
- [ ] **Dogfood on a repo that isn't this one** (VERDICT act 3): run Day-1
      against a well-known OSS repo you have standing in, file the reports
      publicly (with the maintainer's blessing), link them from /examples/.
      Self-dogfood proves honesty; external dogfood proves transfer.
- [ ] Decide star-badge stance (threshold is armed at 25 — build.py; nothing
      to do, just don't fake it), and turn on GitHub Discussions so the
      "tell me how you use it" link has a home (CREDIBILITY 2/4).
- [ ] Optional: custom domain. The .vercel.app URL is honest but a domain
      survives a platform move. Don't block launch on it.

Launch day (order matters — proof surfaces first, announcement last):

1. Final `scripts/check` + deploy; click the preview on a phone.
2. Submit the plugin to `anthropics/claude-plugins-official` (MOAT kill #1:
   turns the absorption threat into co-option, or tells you the rail is
   closed — either answer is useful before HN asks "won't Anthropic ship
   this?").
3. Open the awesome-claude-code inclusion PR (draft below) — the
   border-control channel where the beachhead actually browses (NICHE.md §2).
4. Post Show HN (draft below), morning US time, Tue–Thu. Stay at the
   keyboard for the first 3 hours and answer everything; the maker
   in-thread IS the launch.
5. Same day, smaller channels: r/ClaudeAI (draft below), X thread (draft
   below). Don't cross-post to more than you can attend.
6. Watch raw/ fetch counts and `copy_prompt` events; note which briefs get
   run first — that's the wedge the audience picked, feed it back into
   featured ordering.

The week after (the WTP test, VERDICT act 1 — do not skip):

- [ ] Point attention at /teams in every reply where a team asks "can we
      standardize on this?" Count inbound intent explicitly.
- [ ] Ask the flat-fee question ("would your team pay a flat $1–3k/yr for a
      private catalog + standing CI audits + support — never per-seat?") to
      every team-shaped conversation the launch produces, and to the named
      sufferers collected in DEMAND.md. Log answers in reports/ — the
      pivot ruling (VERDICT: economics bar FAIL at 1–3% conversion) flips
      only on real yeses, not on stars.

## Drafts

### Show HN

**Title** (pick one, don't decorate):

> Show HN: Audit briefs for coding agents — same four phases, one filed
> report, then commits

> Show HN: I made my coding agent file evidence-backed audit reports
> instead of vibes

**Body:**

> "Review my repo" gets a different answer every time. Point an agent at
> your own code and you get a wall of opinions one run, a shrug the next —
> and nothing you can diff, hand to a teammate, or act on next week.
>
> Goal Prompts is a free, open catalog of 149 audit briefs. Each one walks
> the agent through the same four phases — explore, audit, curate, report —
> and files one evidence-backed report at your repo root (BUGS.md, PERF.md,
> SECURITY-AUDIT.md…). Every finding cites file and line, carries severity
> + confidence, and ends with a fix sketch. Briefs are read-only and end by
> asking; a second paste (the Fixer) turns the findings you pick into
> one-commit-per-finding fixes.
>
> The part I care most about: the loop is dogfooded in the open. The
> catalog's own briefs run against the catalog's own repo, the reports are
> committed unedited (goal-prompts.vercel.app/examples), and a FIXLOG
> traces each shipped fix back to the finding that surfaced it. The bug in
> the hero of the landing page is a real self-XSS one of the briefs found
> in the site's own search.
>
> Works as copy-paste, as a Claude Code plugin (/goal:bug-hunt), as Cursor
> project commands, or over MCP. MIT, no signup, no backend — briefs run in
> your agent, so nothing leaves your machine.
>
> Honest limits: the briefs are linter-gated for shape (4-phase, read-only,
> ask-first, size caps) but I don't yet have efficacy evals proving each
> brief beats an unstructured "review my repo" — that's next, and part of
> why I'm posting. I'd love to know what a brief misses on *your* repo.

(If the run clip exists, add it as the first comment, not in the body.)

### awesome-claude-code inclusion PR

> **Goal Prompts** — 149 linter-gated audit briefs (4-phase, read-only,
> ask-first) that file evidence-backed reports at the repo root, plus a
> browser Studio that turns reports into targeted fix prompts. Every brief
> is dogfooded against its own repo with the reports committed unedited.
> MIT. https://goal-prompts.vercel.app

### r/ClaudeAI

> I got tired of "review my repo" giving me different vibes every run, so I
> built a catalog of audit briefs for Claude Code: each one runs the same
> four phases (explore → audit → curate → report) and files one
> evidence-backed report at the repo root — findings cite file:line with
> severity + confidence, and a Fixer prompt turns the ones you pick into
> commits. Install as a plugin (`/plugin marketplace add
> GhostlyGawd/goal-prompts`) and every brief is a `/goal:` command. Free,
> MIT, runs entirely in your agent. The catalog's own audit reports (run
> against its own repo, committed unedited) are the sample gallery:
> https://goal-prompts.vercel.app/examples — curious what it catches (or
> misses) on your repos.

### X thread

> 1/ Your coding agent gives you a different code review every time you
> ask. The fix isn't a bigger model — it's structure.
>
> 2/ A brief tells the agent exactly what to look for, how to weigh it, and
> what to leave behind: explore → audit → curate → report. Out the other
> end: one file, every finding citing file:line with severity + confidence.
>
> 3/ Then the part nobody owns — after the run. Drop reports in the Studio,
> tick the findings that matter, and a Fixer prompt implements them one
> verified commit at a time. brief → report → commits.
>
> 4/ It's dogfooded in the open: the catalog's briefs run against the
> catalog's repo, reports committed unedited, a FIXLOG tracing every fix
> back to its finding. The landing page's hero bug is a real one it caught
> in itself.
>
> 5/ 149 briefs, free, MIT, no signup, nothing leaves your machine. Plugin,
> Cursor commands, or MCP: goal-prompts.vercel.app

### Product Hunt (if used at all — HN is the beachhead's channel)

Tagline options, ≤60 chars:
- "Audit briefs that make your coding agent file evidence"
- "Evidence, not vibes: audit briefs for coding agents"
- "Your coding agent, on the record"

## Post-launch follow-ups already identified (don't do before)

- Prune the playbook shelf from 36 toward ~15 once fetch counts say which
  ones nobody runs (BLINDSPOTS F6 wants it; fetch data should pick the
  survivors). Candidates the reports already doubt: near-duplicates of
  featured sequences and the seasonal themes out of window.
- Efficacy evals behind /quality (BLINDSPOTS F4): a small harness scoring a
  brief's report against an unstructured baseline on seeded-bug repos.
  The quality-bar claim is live; this is what makes it unbluffable.
- Version-stamp copied prompts (BLINDSPOTS §5): a `— goal-prompts vX.Y ·
  /raw/<id>.md` footer line appended at copy time, so a report can name the
  brief version that produced it. Touches the copy path in template.html +
  js/gp-detail.js + MCP server together (parity!).
- Publish the honest token cost of the heaviest brief (MOAT kill #4).
