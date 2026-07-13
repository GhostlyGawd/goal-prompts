# ALIGNMENT_BUILD — roadmap, traceability ledger, and build state

Source of truth for delivering `PRODUCT_ALIGNMENT.md` (root). Every requirement
in that document has a row here. **The build is complete only when every row is
`done` or explicitly ruled out by the operator.** Update statuses in the same
commit as the work; append session notes to the State log. A fresh session
resumes from this file.

Gate rule (from the source doc): implementation beyond Gate A is blocked until
the operator ratifies the items in **Ratification block** below. Each gate ends
with an operator review stop.

Verification legend: **lint** = failing exit code in build.py (rule written
before migration, TDD); **test** = tests/test_build.py or JS suites (written
before the change); **bdd** = scenario walked end-to-end and transcript kept;
**harness** = the efficacy harness itself; **op** = operator judgment at a gate.

## Traceability ledger

| ID | Requirement (PRODUCT_ALIGNMENT section) | Gate | Verify | Status |
|---|---|---|---|---|
| R01 | Doc updated in same commit as any product-meaning change (How this doc stays current #1) | A | process + CLAUDE.md rule | done |
| R02 | CHARTER/DECISIONS/specs/prompts/site must not contradict doc; contradiction blocks release (#2) | C | lint (contradiction checklist in release gate) + op | todo |
| R03 | Ratified decisions superseded only via dated Decision history (#3) | A | process rule in CLAUDE.md | done |
| R04 | Open questions labeled open; no silent ratification (#4) | A | process | done |
| R05 | Every checkpoint ends reconciling doc vs built reality (#5) | A–E | State log entry per gate | ongoing |
| R06 | Positioning: selling quality+repeatability of the designed instruction (Strategic truth) | D | copy review vs doc + test on hero copy | todo |
| R07 | Public category = coding agents, not Claude-only, not general chatbots (Who it is for) | D | test: site copy asserts category | todo |
| R08 | Core prompts portable: no proprietary host commands in bodies (Portable by default) | C | lint: ban host-command tokens in bodies | todo |
| R09 | Claude Code = first-class integration, not dependency (Who it is for) | C/D | lint R08 + copy test | todo |
| R10 | Every one of 152 prompts names + writes exactly one MD result (Current contract) | C | lint (exists today; keep green) | done (preserve) |
| R11 | Shared 6-step baseline in every prompt (inspect→lenses→evidence→save→continue→verify) (Current contract) | C | lint: new contract grammar | todo |
| R12 | Read-only default; action-capable exceptions keep approval gates (Current contract) | C | lint (exists; extend to contract classes) | todo |
| R13 | No invented code churn; artifact-only endings are legitimate (Current contract) | B/C | contract wording + bdd | todo |
| R14 | Actionable findings continue in SAME conversation; no second session; no required "Fixer" knowledge (Current contract + Fixer) | B/C | bdd on 4 goal classes + lint on ending grammar | B-validated (S1–S4); lint at C |
| R15 | "Not every goal produces a report" proposal is rejected — report stays universal (Current contract) | A | recorded; enforced by R10 | done |
| R16 | The 7-step user-visible loop (Choose→Copy→Paste→Run→Understand→Choose scope→Act+check) | B/C/D | bdd transcript + site copy match | todo |
| R17 | Explicit change request = authorization; no redundant approval ritual (User-visible loop) | B/C | lint: authorization-aware gate grammar + bdd | B-validated (S1); lint at C |
| R18 | Exploratory/audit request ≠ permission for unrequested edits (User-visible loop) | B/C | same gate grammar + bdd | B-validated (S2/S3); lint at C |
| R19 | Publish/deploy/send/merge external actions need own authority (User-visible loop) | C | contract clause + lint token check | todo |
| R20 | Same visible conversation; subagents internal only, no new approval surfaces (User-visible loop) | B/C | contract clause + bdd | todo |
| R21 | Browse/choose/copy/paste = primary path, explicit invocation (How people start) | D | site copy test | todo |
| R22 | No generic /goal entry, no automatic router at launch (How people start) | A | recorded; nothing to build | done |
| R23 | Optional integrations expose same catalog (plugin, other hosts, MCP) (How people start) | C | existing surfaces kept green in scripts/check | todo |
| R24 | Plugin namespace → `goal-prompts` (ratified, ADR-15) | C | test pins plugin.json name | todo |
| R25 | Prompts describe capabilities, not host commands; native adapters need portable fallback (Portable) | C | lint R08 + adapter doc | todo |
| R26 | Compatibility smoke: 1 primary agent + ≥1 non-Claude before claiming support (Portable) | B/E | bdd checklist per host, kept in repo | todo |
| R27 | Library front door = 6 concrete situations; not stacked taxonomies (Goal Library) | D | test: static HTML has situation entries | todo |
| R28 | Search, families, browse-all preserved beneath guided start (Goal Library) | D | existing tests keep passing | todo |
| R29 | Two-axis (outcome × project-type) navigation rejected (Goal Library) | A | recorded | done |
| R30 | Detail pages state: when/when-not, inspects, result name, strong result, can-continue, how-checked, real example (Goal Library) | C/D | front-matter fields + lint + page test | todo |
| R31 | Internal write-policy taxonomy stays internal, not public vocabulary (Goal Library) | D | copy review + test bans class labels in public copy | todo |
| R32 | Custom sequences made more discoverable (Playbooks) | D | test: sequence UI discoverability element | todo |
| R33 | Studio = post-run optional batch triage; never the normal hinge (Studio) | C/D | copy tests + nav position | todo |
| R34 | Normal findings→action path works without Studio (Studio) | B/C | bdd | todo |
| R35 | Studio value validated in beta; demote/remove if unused (Studio) | E | beta signal + op | todo |
| R36 | Fixer behaviors kept; experienced as same-conversation continuation; name not required vocabulary (Fixer) | C/D | lint ending grammar + copy test | todo |
| R37 | One reasoned recommended scope, not a menu; ordinary-language corrections (Recommendations) | B/C | contract grammar + bdd | B-validated w/ open ruling: quick-wins bundle counts as one scope? |
| R38 | Recommendation explains: evidence, causal impact, confidence, what changes, effort, what's left alone, how checked (Recommendations) | C | lint: recommendation section fields | todo |
| R39 | Result file = durable memory + inspectable evidence (Saved results) | C | contract copy; existing behavior | todo |
| R40 | Repeat runs read previous result; lead with delta: fixed / still present / new / regressed (Saved results) | C | lint: re-run clause present + bdd repeat run | B-validated (S6); lint at C |
| R41 | Compounding loop: charter constrains; no rediscovery-as-new; fixes traceable; deltas (Saved results) | B/C | bdd + contract | todo |
| R42 | Saved-result location: root-or-`reports/` ratified (ADR-15); wording pinned by lint | C | lint | todo |
| R43 | Stickiness framings are hypotheses; no browser-reminder positioning; learn triggers from real use (Saved results) | D/E | copy test bans claims; beta notes | todo |
| R44 | Internal efficacy test harness: frozen snapshot, plain-request vs Goal Prompt, scored, repeated (Efficacy) | B | harness built + first results committed | done (evals/, GATE_B_RESULTS.md) |
| R45 | Efficacy is internal QA — never a user-facing step (Efficacy) | D | copy review | todo |
| R46 | Prototype contract privately on representative types before catalog-wide rewrite (Efficacy) | B | bdd fixtures | done for investigate+act (S1–S6); decide/verify prototypes written, matrix-run pending |
| R47 | Migrate all 152 or version/deprecate/remove before presenting as coherent (Efficacy + Gate C) | C | lint over full catalog + count check | todo |
| R48 | Marketing: concrete object+motion before internal nouns (Marketing) | D | hero-copy test: banned lead words | todo |
| R49 | Marketing shows the 6 concrete things (copy from site→paste→inspects your files→named result→continuation→informed next run) (Marketing) | D | copy test + demo content | todo |
| R50 | Homepage must not LEAD with: ship, pre-ship, Claude Code review, memory, workflow, session, Fixer, Studio, command, report (Marketing) | D | test: first-viewport copy scan | todo |
| R51 | Rejected framings list never used (before-you-ship trigger, /goal entry, "remembers your repo", unexplained labels, auto-invocation promise, abstract axes, unobserved stickiness/portability claims) (Marketing) | D | copy test: banned phrases | todo |
| R52 | Demo = guided replay of a REAL sanitized run: actual prompt, evidence, result, scope decision, actual diff, actual checks (Marketing) | D | build from Gate B transcript; test asserts assets exist | todo |
| R53 | Full run record available for inspection (Marketing) | D | link test | todo |
| R54 | No public ratings/reviews during beta (Beta) | E | absence test | todo |
| R55 | Contextual opt-in feedback: Yes/Partly/No + optional text + minimal consented context (Beta) | E | feature + privacy test | todo |
| R56 | Never silently collect repo/report/code contents (Beta) | E | privacy boundary doc + code review | todo |
| R57 | Moderated tests, interviews, shared sanitized runs supplement metrics (Beta) | E | op | todo |
| R58 | Gate process followed; stop at each gate for operator review (Delivery plan) | A–E | State log | ongoing |
| R59 | 12 ratified-alignment bullets hold (Ratified alignment) — mapped to R06,R08,R14,R20,R25,R37,R38,R40,R47,R52,R55,R43 | — | via mapped rows | tracked |

## Gate A deliverables (this session)

1. `PRODUCT_ALIGNMENT.md` committed at repo root — **done**.
2. This roadmap/ledger — **done**.
3. `specs/GOAL_CONTRACT.md` — **ratified v1 (ADR-15)**.
4. Reconciliation (below) — **done**.
5. Namespace + saved-result decision memos (below) — **prepared, awaiting
   operator choice**.
6. DECISIONS.md ADR-14 recording adoption — **done**.
7. Operator review stop — **this is where we are**.

## Gate A reconciliation findings

1. **Ask-first vs authorization-aware.** CHARTER invariant says "ask-first gate
   on every brief"; PRODUCT_ALIGNMENT says an explicit original change request
   is already authorization and redundant approval rituals are forbidden.
   Resolution proposed in GOAL_CONTRACT §4: the gate becomes
   *authorization-aware* — ask only when scope was not already granted.
   CHARTER's invariant wording will need a ratified amendment at Gate C.
2. **Terminology: "brief" vs "Goal Prompt."** The alignment doc names the unit
   **Goal Prompt** and the catalog **Goal Library** throughout. The site,
   README, CHARTER, linter and tests say **brief** (chosen in the 0.14
   re-badge). Per doc rule #2 this contradiction blocks release. Needs an
   explicit ruling — see Ratification item 8. Migration cost if renaming:
   site/README/CLAUDE.md/CONTRIBUTING copy + tests; ids, slugs, file layout,
   commands can stay.
3. **Studio centering.** README section "Act on the reports — Report Studio"
   and landing Proof cards still position Studio as the hinge; CHARTER Now #6
   and the doc demote it to optional triage. Gate D work (R33–R35).
4. **Charter-as-input already shipped for conductors** (0.19.0 contractor
   voice: reads CHARTER.md, narrates stages, ranked ending with Fixer offer).
   The remaining continuation work is per-prompt endings (R14, R17, R37) —
   Gate B prototype + Gate C migration.
5. **No contradiction** found between the doc and DECISIONS ADR-1..13 except
   ADR-9's metric focus, already reconciled inside CHARTER ("Contradictions
   found" #1).

## Decision memo 1 — Claude Code plugin namespace (Ratification item 7a)

Current: marketplace `goal-prompts`, plugin `goal`, commands `/goal:bug-hunt`.
Doc: generic `/goal` rejected; leading direction = full product namespace.
**Recommendation: rename plugin to `goal-prompts`** → commands become
`/goal-prompts:bug-hunt`. No collision with any host-owned `/goal`. Cost:
marketplace.json, plugin generator, README/site install copy, tests
(PluginTests), CHANGELOG note + uninstall/reinstall line for existing users.
Curl-installer un-namespaced files stay `goal-<slug>` (no conflict with a bare
`/goal`).

## Decision memo 2 — saved-result location (Ratification item 7b)

Current contract: repo root, or `reports/` when that directory exists.
Options: (a) keep as-is; (b) default `reports/` always. (b) breaks the
"no unexplained clutter" rule in reverse (creates a directory uninvited) and
touches every collector. **Recommendation: (a) ratify the status quo** and
write it into GOAL_CONTRACT verbatim; revisit only on real-user evidence.

## Ratification block — operator input required to open Gate B

Reply "ratify all with recommendations" or list exceptions by number.

1. Shared contract: every Goal Prompt writes one MD result; action continues
   in-conversation after any needed authorization.
2. Browse/choose/copy/paste primary; no auto-routing at launch; integrations
   optional.
3. Public scope: coding agents broadly; portable core; Claude Code first-class
   integration, not dependency.
4. Studio: post-run optional batch triage; custom sequences are the pre-run
   batching tool.
5. Efficacy test + cross-host smoke = internal QA, not user workflow.
6. Situation-first front door replaces two-axis navigation.
7. (a) Plugin namespace → `goal-prompts` (recommended) or name another.
   (b) Saved-result location → keep root-or-`reports/` (recommended) or
   name another.
8. Terminology: keep **brief** everywhere (update PRODUCT_ALIGNMENT wording to
   "briefs, formally Goal Prompts"), or migrate public vocabulary to
   **Goal Prompt / Goal Library** (Gate D copy work). Operator's call — no
   recommendation strong enough to presume.

## State log

- **2026-07-12 · session 1 (Gate A).** Branch reset on main @ 3ec00b1. Doc
  committed; ledger created; GOAL_CONTRACT drafted; reconciliation complete;
  ADR-14 appended; CLAUDE.md breadcrumbs added. Stopped at Gate A review with
  ratification block pending. Next session: on ratification, open Gate B —
  build efficacy harness + continuation prototypes on 4 goal classes
  (investigation: 01; artifact: 142 or 149; action: 47; verification: 144),
  fixtures under a private scratch area, transcripts kept for the Gate D demo.

- **2026-07-13 · session 2 (Gate B opens).** Operator: "Aligned on all" —
  ADR-15 records it (item 8 read as Goal Prompt/Goal Library vocabulary,
  veto offered). Gate B in progress: evals/ harness (fixture webshop with
  8 seeded, answer-keyed defects + 1 pre-existing failing test), scorer
  with unit tests (TDD), 4 contract-prototype prompt bodies
  (01/149/47/144 classes), BDD scenarios S1–S7, first efficacy runs
  plain-vs-goal. Results land in evals/results/ + GATE_B_RESULTS.md, then
  operator review stop.

- **2026-07-13 · session 2 (Gate B complete — review stop).** Matrix run:
  plain vs goal-v2 N=3 (7 valid seeds; D5 excluded after a plain run
  proved it commutative), scenarios S1–S6 all pass (S2 adjudicated; S7
  observational pass). Headline: finding-count edge modest (5.67 vs 5.0),
  structural edge total (saved-file 3/3 vs 0/3; deltas, gates, receipts),
  cost 2.7×. Harness bugs found+fixed (write-allowlist, report detector);
  denied runs kept as evidence. Open: cross-host smoke (R26), decide/verify
  matrix runs, R37 bundle ruling, contract amendments (a)/(b) proposed in
  evals/GATE_B_RESULTS.md. Awaiting operator review to open Gate C.

- **2026-07-13 · session 3 (value-axes ruling; Gate B stop holds).**
  Operator confirmed ALL FOUR value axes as the product's true value:
  (1) knowing what to run — the catalog/curation itself; (2) encoded
  judgment — what to inspect, what counts as evidence, what a good result
  looks like (doc line 31 phrasing); (3) a process you can trust — the
  axis Gate B proved 100% vs 0% (saved result, scope safety, honest
  verification, re-run deltas); (4) skip the prompt-writing — instant
  well-formed request. **Register rule (operator, explicit):** never frame
  the product around "senior engineer" or any engineers-only persona, and
  never as an overly-technical code thing — the audience is the doc's
  §Who-it-is-for (solo builders/maintainers, any digital product in
  files). That phrase appears nowhere in the doc or product surfaces
  (grepped) — it was assistant framing; banned from all future copy,
  specs, and prompts. Gate D consequence: add engineer-persona phrases to
  the banned-copy test list (with R48/R50/R51). Efficacy consequence:
  future harness rounds should exercise all four axes, not bug-count
  alone; each public claim still needs observed evidence. Three Gate B
  rulings (bundle-as-one-scope, delta-open lint, decide/verify runs)
  still pending; Gate C remains closed.

- **2026-07-13 · session 3 (operator override — migration parked, marketing
  direct).** Operator, twice and emphatically: the goal is fixing product
  positioning + marketing and making the product match its goal — NOT
  rewriting prompts. Reality check supports it: current prompt bodies
  already carry the trust behaviors (named dated report, re-run delta
  lead, evidence rule, null escape, reports/ option, ask-first gate);
  the contract migration is refinement, not a prerequisite for honest
  copy. **Ruling recorded: prompt bodies are FROZEN; the 152-prompt
  migration (doc §10, Gate C) is parked and must not start without an
  explicit operator request. Site/positioning work proceeds now against
  observed current behavior.** PRODUCT_ALIGNMENT §Delivery order and §10
  conflict with this ruling and need an operator-approved amendment;
  until then the ruling governs. Gate C rows in the ledger inherit
  status "parked". The three Gate B rulings are moot while migration is
  parked. Next: situation-first front door + plain-words hero + honest
  claims (Gate D scope), preview link to operator.
