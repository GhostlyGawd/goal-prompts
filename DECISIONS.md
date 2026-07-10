# DECISIONS — the harness ADR log

2026-07-09 · Append-only. One entry per load-bearing choice in converting
goal-prompts into the decision layer of the build harness. Entries marked
**inherited** confirm a prior strategy decision against repo evidence;
entries marked **deviation** overturn one, with the rationale the deviation
rule demands. Supersede entries with new ones; never rewrite.

## ADR-1 — Enforcement hierarchy: exit codes > scripts > prose (inherited)

Status: accepted
Context: The prior strategy ranked deterministic enforcement above executable
artifacts above written instructions. The repo already lives this: every
house rule that matters is a lint in `build.py` (`lint()` at build.py:102,
`lint_catalog()` at build.py:151), the whole contribution surface is one
gate (`scripts/check`), and CI fails on any drift between sources and
generated files (.github/workflows/ci.yml, the `git status --porcelain`
step). During this session the gate itself caught three omissions (README
count, families table, OG cards) that prose review would have missed.
Decision: Confirmed. Every new harness rule ships as a failing exit code
first; briefs only narrate what the gates enforce.
Consequences: Opus is trusted to *read* rules but never *relied on* to
follow them; anything relied on must exit non-zero when violated.

## ADR-2 — Goal-prompts stays the decision layer; extension is append-only (inherited)

Status: accepted
Context: The repo documents its own extension points: new briefs in
`prompts/<family>/`, new families via `FAMILY_ORDER` + `FAMILY_COLORS`
(CLAUDE.md · Conventions), new playbooks in `playbooks.json`. No existing
brief was edited in this session.
Decision: Confirmed, with one correction to the prior model: adding a family
also requires a `FAM_ICON` entry and an SVG `<symbol>` in `template.html` —
`lint_family_icons()` (build.py:175) fails the build without them. CLAUDE.md's
"nothing else needs editing" sentence undersold this; both were added.
Consequences: Future family additions touch exactly four places: two dicts
in build.py, two lines in template.html.

## ADR-3 — Build family (141–144), gated on the Fixer pattern (inherited, refined)

Status: accepted
Context: The prior decision said "add a Build family: spec → scaffold →
implement → verify." Two frictions with house rules: (1) briefs are
read-only except `47 · The Fixer`, whose ask-first gate sits at the end of
Phase 2 before any edit (CLAUDE.md · Conventions); (2) every brief writes
exactly one report file with a unique name (build.py:112, build.py:159).
Decision: Four briefs — `141 · Scaffold the Rails` (SCAFFOLD.md),
`142 · Spec the Product` (SPEC.md), `143 · Implement to Spec` (BUILDLOG.md),
`144 · Ship Gate` (SHIP-GATE.md), family question "will it ship?". The two
code-writing briefs (141, 143) adopt the Fixer pattern: the operator picks
the scope at a Phase 2 gate before anything is written. 142's only write
*is* its report file (the spec), and 144 is read-only, so both fit the
classic contract. Refinements to the prior decision:
- **Execution order is scaffold → spec**, not spec → scaffold. Writing
  SPEC.md inside the scaffold means `scripts/spec_lint.py` gates the spec
  the moment it is written; a spec authored outside the rails is checked by
  nobody. Ids were assigned in execution order so the auto-generated family
  conductor (`raw/family-build.md`, built by build.py:1338) is itself the
  build pipeline, for free.
- Briefs reference the in-repo SPEC.md and template rather than embedding
  them, keeping all four bodies at 2.9–3.7k chars under the 4,000 gate.
Consequences: CLAUDE.md's "one exception is 47" sentence is now "the
exceptions follow the Fixer pattern" — updated in this session. The Build
briefs run inside *product* repos; run against goal-prompts itself they
null-report (no `scripts/spec_lint.py` here).

## ADR-4 — Golden-path template: Python 3 stdlib + unittest, zero dependencies (inherited, made concrete)

Status: accepted
Context: The template needed one concrete stack. The parent repo proves
stdlib-only Python + zero-dep Node works for a real shipped product, and
every dependency is a fresh way for an unsupervised Opus session to break a
build or rationalize an upgrade.
Decision: `template/` ships Python 3 stdlib + `unittest`, no requirements
file. Deviation is legal but expensive by design: rewrite the harness layer
preserving the four enforcement moments (post-edit, pre-commit, CI, ship
gate) and record an ADR. Dependencies added later must be named in an ADR —
`spec_lint.py` greps DECISIONS.md for the package name and fails otherwise.
Consequences: A whole class of failure (dependency drift, broken installs,
supply-chain surprises) is structurally absent from v1 products. Products
that genuinely need a framework surface that need as a recorded decision,
not a silent `pip install`.

## ADR-5 — Master conductor: two chained conductors + brief gates, not one artifact (deviation)

Status: accepted
Context: The prior decision called for "one artifact spanning no-product to
operated product." Repo evidence against it: (1) conductor text is
*generated* by `conductor()` (build.py:191) with canonical sentences
parity-checked across three implementations by `scripts/mcp-smoke.cjs` —
a hand-shaped conditional conductor would either fork that grammar or
falsify it; (2) the journey crosses a repo boundary (venture research
workspace → product repo) which a single "you are working inside this
repo" conductor cannot honestly span; (3) the go/no-go after `67 · Venture
Verdict` is already an ask-first gate — briefs' own gates ARE the branch
points, and prose conditionals on top would be weaker than what exists.
Decision: The master path is two stock conductors joined by the operator at
the two human decision points: `raw/playbook-founderfunnel.md` (61→67, in
the research workspace), then on a go, `raw/playbook-buildloop.md`
(141→144, in the product repo 141 creates), then the standing loop
(29 weekly; 46→47 on findings). specs/CONDUCTOR_SPEC.md carries the
one-page operator runbook that chains them.
Consequences: Arithmetic: 7 + 4 = 11 stages across two conductors, both
under the 16-stage cap (build.py:200). No new conductor grammar to keep in
parity. The "one artifact" ideal is met by the runbook, which is prose for
the *operator* — the two machine-facing artifacts stay generated and linted.

## ADR-6 — Verifiability constraint enforced as spec grammar (inherited)

Status: accepted
Context: "Only build products whose quality is mechanically verifiable" was
a prose constraint. Prose is advisory (ADR-1).
Decision: It is now a parse error: `spec_lint.py`'s AC grammar makes an
acceptance criterion without a runnable `check:` command unwritable, and
`141`'s Phase 2 lens 2 refuses instantiation for pure-taste products before
a repo even exists.
Consequences: The constraint binds at the two cheapest moments — before
scaffold and at spec write — rather than after implementation.

## ADR-7 — No custom orchestrator (inherited)

Status: accepted
Context: Everything here runs on Claude Code (interactive or headless) +
GitHub Actions + `sh`. The template's CI is a 13-line workflow.
Decision: Confirmed. No API orchestrator, no runner service, no dashboard.
Consequences: The system's availability story is GitHub's and Anthropic's,
not ours; the operator's laptop is never load-bearing.

## ADR-8 — PreToolUse blocks harness edits; the named residual risk is product-test weakening

Status: accepted
Context: "Opus never authors the verification layer" needed teeth. Hooks can
deterministically block tool calls (exit 2).
Decision: `template/scripts/hook-protect` blocks any Edit/Write into
`scripts/`, `.githooks/`, `.github/`, `.claude/`, `tests/harness/`;
CODEOWNERS routes any harness diff that arrives another way to the operator;
`144 · Ship Gate` diffs the harness layer against the template. Considered
and rejected: a checksum lockfile (harness.lock) — Opus could regenerate it,
so it adds friction without adding enforcement beyond what CODEOWNERS + the
144 diff already give.
Consequences: The one gap hooks cannot close: Opus *owns* product tests
(test-first requires it) and could weaken one to get green. Mitigations:
144's sabotage lens (break the behavior, expect red), CLAUDE.md's explicit
prohibition, and operator review of test diffs. Named, not hidden.

## ADR-9 — The catalog is distribution; the products are the revenue

Status: accepted
Context: "What is the product?" metrics.json records 0 stars, 0 forks; the
monetization surfaces in playbooks.json (`sponsored-example`,
`codereview-collab`) are `preview: true` placeholders. Catalog revenue today
is zero and its path (sponsorships, partners) needs an audience first.
Decision: Both answers are true but only one gets investment: goal-prompts
is the decision layer and the distribution surface (briefs, conductors, MCP,
plugin); the revenue-generating artifacts are the product repos the Build
family creates. Catalog monetization stays on the shelf until adoption
exists (the star-threshold badge at build.py:1298 is the same bet).
Consequences: No further work on sponsored/collab plumbing now. Weekly
Vitals on shipped products, not catalog traffic, is the number that matters.

## ADR-10 — Session scope notes

Status: accepted
Context: Mission rules: no existing brief edited, no build-gate logic
edited, no dependencies added.
Decision: Honored as follows — existing briefs untouched; build.py changes
are two data-dict additions at the documented extension point (FAMILY_ORDER,
FAMILY_COLORS), zero lint-logic changes; README.md count/table edits were
*demanded by the gate itself* (build.py:1232 fails on a stale count);
CLAUDE.md edits document the new family and template. `Pillow/fonttools/
brotli` were installed to run the pre-existing `scripts/og.py` (its
docstring already requires them) — a dev-time tool dependency that predates
this session, not a new runtime dependency.
Consequences: `scripts/check` passes end to end; CI's drift gate passes with
all regenerated surfaces committed.

## ADR-11 — No research workspace: the harness runs in the user's actual repo (operator correction; supersedes ADR-5's split)

Status: accepted
Context: The first cut of the conductor design (ADR-5) routed the Founder
Funnel through a separate "research workspace" repo, inheriting the framing
from the Venture briefs' own language ("this repo — the research workspace
for this venture", prompts/venture/67). The operator corrected the premise:
this whole system is meant to be used by people on their actual repos.
Decision: One repo end to end. The Venture briefs run in the actual repo
(their reports already land at the repo root or reports/ under the standing
convention — no brief changes needed). 141 · Scaffold the Rails was
rewritten to install the harness into the current repo in one of two modes:
greenfield (empty repo — copy the whole template) or graft (existing code —
install the harness layer plus the SPEC.md/DECISIONS.md skeletons,
overwriting nothing, with the repo's existing test/lint commands wired into
scripts/check as one-line steps the operator ratifies at the Phase 2 gate).
With the repo boundary gone, ADR-5's strongest argument dissolves, so the
prior "one artifact" master-conductor decision is restored: the
`zerotoship` playbook (61→67, 141→144 — 11 stages, under the 16 cap) is the
master conductor, generated by the standard grammar. `founderfunnel` and
`buildloop` remain as subset entry points. ADR-5's other two arguments
survive unchanged inside this shape: the grammar stays generated and
parity-tested, and the briefs' ask-first gates remain the branch logic.
Consequences: specs/CONDUCTOR_SPEC.md, HARNESS_PLAN.md, template/README.md,
and specs/BUILD_FAMILY_SPEC.md were re-cut to the one-repo model. The
operate loop (29, 46→47, re-run 144) stays out of the conductor — it is a
cadence, not a sequence. Residual note: in graft mode spec_lint's
dependency rule still only reads requirements.txt; extending it to
package.json and kin is queue work (FABLE_BUILD_QUEUE item 3 territory).

## ADR-12 — Design direction is pinned as decisions, not adjectives (new)

Status: accepted
Context: Ten visual passes (see git log through 0.13) converged on the same
generic landing page, and hours-long "redesign" sessions produced changes
users could not perceive. Two causes, both structural. First: with no pinned
direction, an agent asked to "redesign" samples the maximum-likelihood
landing page — soft neutrals, rounded cards, kicker + two buttons — so every
regeneration lands in the same basin. Second: the repo's own audit briefs
reward *verifiable* findings (a radius token drift, a 22px/24px logo split),
so agent effort flowed into sub-perceptual consistency fixes; consistency
audits can maintain an identity but cannot originate one. Nothing in the
loop ever rendered the page — build.py lints text, scripts/check parses JS —
so design edits shipped on plausibility alone.
Decision: The identity is a written contract: specs/DESIGN_DIRECTION.md
("the ledger" — the page typeset like the audit report the product sells:
warm ink/paper, ruled numbered sections, mono metadata, ONE vermilion
accent, family hues demoted to metadata, real report content as the hero
artifact, 4-bar mark with the tallest bar flagged). Restyling against it
requires a superseding ADR here first. Palette lives only in TOKENS_CSS
(build.py) so one edit re-keys every surface. UI work must render
screenshots (scripts/design-shot.cjs) and eyeball them before commit.
Consequences: "Redesign it again" is no longer a valid prompt against this
repo; the valid prompts are "execute the direction better" or "supersede
ADR-8 with a new direction". Visual changes below a stranger's
just-noticeable-difference are maintenance and must be labeled as such.

## ADR-13 — The design engine: brand.json is the single source of brand truth; design-engine/ is a portable, second plugin

Status: accepted (amends ADR-12's storage clause; the pinned direction stands)
Context: The ledger identity (ADR-12) lived in four hand-synced places —
TOKENS_CSS + BRAND_MARK + FAVICON + FAMILY_COLORS literals in build.py, a
duplicated BARS geometry in scripts/icons.py, echoed constants in
scripts/og.py — with the contrast maths pinned only where individual tests
thought to look. Separately, the operator commissioned a portable branding &
design engine (clonable into other repos); a full rebrand attempted through
it was rejected at the live preview and rolled back (the engine's
library/references/retros.md records the lessons), leaving the engine itself
as the contribution.
Decision: design-engine/ is a self-contained folder: brand.json (palette
themes incl. the severity ramp, categorical family hues, type faces, space,
radii, motion vocabulary, mark geometry, host config) + stdlib tools
(tokens_build, brand_lint, contrast, mark_render, specimen, css_hex_lint;
font_subset, image_lab, scene, imagegen, present, shots.cjs, qa_sheet,
motion_preview as generate-time tools) + six design skills + a mind library
(boards, references incl. anti-slop and the program retro, technique
recipes). build.py imports the engine's tools (host → engine, never the
reverse, so the folder stays copy-portable) and derives FAMILY_COLORS,
FAMILY_MIX_LIGHT, BRAND_MARK, FAVICON, and TOKENS_CSS from brand.json;
scripts/icons.py draws from mark_render (byte-identical PNGs). The compiled
tokens.css is declaration-identical to the hand-authored ledger file — the
mark and favicon strings are byte-identical — so this changes no pixels.
scripts/check grew a design-gates step (brand_lint + contrast, both exit
non-zero, ADR-1) and discovers design-engine/tests. The engine ships as a
second marketplace entry with its own hand-maintained version.
This AMENDS one clause of ADR-12: "Palette lives only in TOKENS_CSS
(build.py)" becomes "palette lives only in design-engine/brand.json" — the
one-edit-re-keys-every-surface property that clause protected is preserved
and now machine-gated (contrast matrix + manifest↔tokens parity test).
Everything else in ADR-12 stands unchanged: the ledger direction is still
the identity, restyling still requires a superseding ADR, UI work still
renders screenshots before commit (scripts/design-shot.cjs, now joined by
the engine's shots.cjs matrix asserts + qa_sheet contact sheets). Amends
ADR-2's new-family recipe: the color now goes in brand.json
palette.categorical (plus FAMILY_ORDER, FAM_ICON, and the template.html
symbol as before). Contrast thresholds are seeded at the ledger's shipped
floors (all accents clear 3.0 on every surface; categorical is checked on
the three TokensTests surfaces) with the standing rule that thresholds only
ever tighten.
Consequences: One brand definition feeds site CSS, header mark, favicon,
and PWA icons, and the folder can be copied into any repo to port the
system. Superseded brands are preserved as manifests under
design-engine/library/proposals/ (brand v1, the rejected Auditorium).
og.py still carries local color constants — re-pointing it at brand.json
is queued. css_hex_lint joins scripts/check only once the three
inline-<style> surfaces are var-clean.
