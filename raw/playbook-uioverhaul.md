# Playbook: Total UI Overhaul (conductor)

You are working inside this repo. Mission: execute the **Total UI Overhaul** playbook — 6 audit briefs in sequence, each producing one report file in the repo's `reports/` directory.

The interaction-and-UI sweep: navigation, menus, every interactive state, the empty screens, and the icon language — then the Fixer turns the findings into verified commits.

## Before stage 1
- If `CHARTER.md` exists at the repo root or in `reports/`, read it first — its goals, non-goals, and invariants bound every recommendation in every stage. No charter? Proceed, and suggest 149 · The Charter afterwards.
- If there is no `reports/` directory at the repo root, create it now — every brief writes its report there once the directory exists, so the whole run lands in one folder instead of scattering generic filenames across the root.
- Before fetching stage 1, tell the operator in plain words what this playbook will do — one line per stage — and ask for the go-ahead.
- In a git repo, plan to commit as you go — one commit per report plus a final one for the index; make committing part of the go-ahead question, and skip it only if the operator says no.

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. If your harness can run subagents or fresh sessions, run each stage in one — a stage needs only the earlier report files at the repo root and in `reports/`, never this conversation.
3. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
4. Confirm the report file exists (at the repo root or in `reports/`) before moving on, and stamp one provenance line under its title — `<playbook> · stage <N>/<M> · brief <id>` — so the file itself names the run that wrote it.
5. If committing, commit the report now, message `reports: <FILE> — <stage title> (<playbook> <N>/<M>)` — that per-stage trail is what lets any later session recover the whole run with one git log --grep.
6. After each stage, tell the operator in two or three plain sentences what it found — the single biggest finding and why it matters for this repo — and what comes next; never advance in silence.
7. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
1. **129 · Navigation & Wayfinding Audit** — fetch https://goal-prompts.vercel.app/raw/129.md → writes `NAVIGATION.md`
2. **130 · Menu & Command Surface Audit** — fetch https://goal-prompts.vercel.app/raw/130.md → writes `MENUS.md`
3. **58 · Interaction States & Motion Audit** — fetch https://goal-prompts.vercel.app/raw/58.md → writes `STATES.md`
4. **133 · Empty & Zero-Data States Audit** — fetch https://goal-prompts.vercel.app/raw/133.md → writes `EMPTYSTATES.md`
5. **134 · Iconography & Visual Language Audit** — fetch https://goal-prompts.vercel.app/raw/134.md → writes `ICONOGRAPHY.md`
6. **47 · The Fixer** — fetch https://goal-prompts.vercel.app/raw/47.md → writes `FIXLOG.md`

## After the final stage
- Write the run's index — `INDEX.md`, in the same directory as the reports (commit it last, if committing): the run date, the playbook name, each stage with its brief URL, and one line per report — file name, finding count (mark a null report as such), and its top two or three next steps. A session with no memory of this run must be able to start from that one file.
- Present the strongest findings across every report as one ranked list, in plain words — each with why it matters for this repo; the operator should not need to open a report file to act.
- Then ask which findings to fix. Unless 47 · The Fixer already ran as a stage of this playbook, offer to fetch https://goal-prompts.vercel.app/raw/47.md and implement exactly the operator's picks — one verified commit per finding. The report files stay on disk as the paper trail.
- Prefer a merged plan instead? Fetch https://goal-prompts.vercel.app/raw/28.md (Roadmap Synthesis) to fold the reports at the repo root and in `reports/` into one sequenced plan.
- Close with the handoff: if the run sits on an unmerged branch, offer to open a pull request titled `reports: <playbook> run <date> (<M> stages)` whose body is the index — the PR list is the first place a later session or teammate looks; either way, print a paste-ready handoff block naming the branch, the report directory, the file list, and `INDEX.md` as the place to start.

## Rules
- If a fetch fails, retry once; if it still fails, use the locally installed /goal:<slug> (or /goal-<slug>) command or the goal-prompts MCP get_brief tool for that stage; if neither exists, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists (at the repo root or in `reports/`), ask whether to re-run or skip that stage.
- A conductor caps at 16 stages — for a longer campaign, split it into two conductors and run them back-to-back.
