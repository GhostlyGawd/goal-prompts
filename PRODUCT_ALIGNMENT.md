# Goal Prompts — Product Alignment

**Status:** Working agreement, partially ratified  
**Last reconciled with the operator:** 2026-07-12  
**Scope:** Product, interaction, catalog, distribution, marketing, validation, and launch

This is the master document for the current Goal Prompts direction. It exists so the
product does not drift back toward whatever wording, interface, or implementation is
most convenient in a later coding session.

## How this document stays current

1. A change that alters what Goal Prompts is, who it is for, how someone starts it,
   what it writes, when it changes files, or what the site promises must update this
   document in the same commit.
2. `CHARTER.md`, `DECISIONS.md`, product specs, prompts, generated integrations, and
   site copy must not contradict this document. A contradiction blocks release.
3. Ratified decisions are not silently rewritten. Supersede them with a dated entry
   in **Decision history** and update the affected section.
4. Open questions must be labeled as open. An implementation preference is not a
   product decision until the operator ratifies it.
5. Every implementation checkpoint ends by reconciling this document against what
   was actually built.

## The strategic truth

> Goal Prompts is selling the quality and repeatability of the second instruction
> without requiring the user to design it themselves.

A Goal Prompt is a pre-authored, goal-specific instruction for a coding agent. It
tells the agent what to inspect, how to reason about it, what counts as evidence, how
to filter weak conclusions, and what result to save. The user gets a more deliberate,
repeatable run without having to design that instruction from scratch.

Goal Prompts is the curated system around those instructions: the Goal Library,
playbooks that combine them, portable copy-and-paste delivery, optional native
integrations, a shared quality contract, examples, and the path from findings to
approved and verified action.

The coding agent still does the work. Goal Prompts supplies the better instruction and
the repeatable operating contract.

## Who it is for

The first user is the burned solo builder or open-source maintainer using a coding
agent on a website, application, developer tool, AI feature, documentation site, or
other digital product stored in files the agent can inspect.

The public category is **coding agents**, not Claude Code alone and not every general
chatbot or tool-using AI. The portable prompt must work without proprietary commands
in any capable coding agent that can inspect the supplied files and run the tools the
task requires.

Claude Code is a first-class integration, not a dependency in the core prompts.

## The current product contract that must be preserved

The existing catalog has 152 Goal Prompts. The build currently enforces that every
one names and writes exactly one Markdown result. This is core functionality, not an
optional side effect.

The shared baseline is:

1. The agent inspects the relevant files and available context.
2. It evaluates the work through the Goal Prompt's defined lenses.
3. It keeps conclusions it can support with evidence and records uncertainty honestly.
4. It saves one named Markdown result so the work survives the temporary conversation,
   can be checked by the user, and can inform a later run.
5. If there is appropriate work to carry out, the same user-facing conversation
   presents a reasoned recommendation and continues after the user authorizes the
   scope.
6. The agent verifies any changes using checks appropriate to the work and records
   what passed, failed, was skipped, or remained inconclusive.

Not every individual Goal Prompt changes code. Most of the current catalog is
deliberately read-only apart from its result file. `47 · The Fixer`, `141 · Scaffold
the Rails`, and `143 · Implement to Spec` are current action-capable exceptions with
approval gates. A spec, charter, decision, or investigation may itself be the useful
artifact; invented code churn is not a successful ending.

The end-to-end product loop, however, must not strand an actionable result in a
report. When findings can become useful file or code changes, the agent should offer
that continuation in the same conversation, explain the proposed scope, wait for any
needed authorization, carry it out, verify it, and append the receipt. The user must
not need a second session or understand an internal component called “The Fixer.”

The earlier proposal that “not every goal produces a Markdown report” is rejected. It
contradicts both the current product and the aligned value of durable, compounding
results.

## The user-visible loop

1. **Choose.** The user browses the site, opens a specific Goal Prompt or playbook, or
   assembles a custom sequence from the catalog.
2. **Copy.** The user copies it. No installation is required for this path.
3. **Paste.** The user pastes it into the coding agent already working with the files
   they want help with.
4. **Run.** The agent inspects the work, follows the structured instruction, and
   writes the named Markdown result.
5. **Understand.** In the same conversation, the agent explains the most important
   conclusions, their evidence, causal impact, uncertainty, effort, and tradeoffs.
6. **Choose scope.** If action is appropriate, the agent recommends a defensible
   scope. The user can accept it, expand it, reduce it, ask for an explanation, give
   different constraints, or stop in ordinary language.
7. **Act and check.** Within the authorized scope, the agent makes changes, runs the
   stated checks, distinguishes existing failures from introduced failures, and
   records the result.

An explicit original request to change or fix something is already authorization for
that stated scope. The agent must not add a redundant approval ritual. An exploratory
or audit request is not permission for unrequested edits. Publishing, deploying,
sending, merging, or other external actions require their own authority.

“The same conversation” means the same visible conversation and coordinating agent
from the user's perspective. The coordinator may use subagents internally when that
improves the work. Subagents must not change the user-facing contract, lose scope, or
create additional approval surfaces.

## How people start Goal Prompts

The primary, model-portable path remains the one the product already offers:

- Browse the Goal Library or a playbook on the website.
- Optionally add several Goal Prompts to a custom sequence while browsing.
- Copy the chosen prompt or sequence.
- Paste it into the coding agent working with the relevant files.

This is an explicit invocation. Goal Prompts does not silently attach itself to every
agent request and does not need to infer that every ordinary sentence should trigger
a Goal Prompt.

Optional integrations exist for repeat users:

- A Claude Code plugin can expose the same catalog through a non-conflicting,
  product-namespaced command.
- Other hosts can package the same portable prompts in their native skill, command,
  or plugin format.
- The MCP surface can help a capable agent search the catalog, retrieve a Goal
  Prompt, or assemble a sequence.

The proposed generic `/goal` entry point and automatic router are rejected for the
launch plan. Claude Code already owns `/goal`, and a router would replace the clear
browse/choose/copy promise with inference the product has not proven. The exact new
Claude Code plugin namespace remains an implementation decision; the current leading
direction is the full product namespace rather than `/goal:*`.

## Portable by default; native when available

Core Goal Prompts must describe capabilities, not proprietary host commands. They may
ask the host agent to inspect files, search, run checks, edit within scope, use version
control when available, and delegate when useful. A host adapter may use native
features to do those jobs, but every native path needs a portable fallback.

The promise is not that every model will return identical work. The promise is that
the Goal Prompt does not require Claude-only syntax to make sense and that each
advertised integration can complete the documented loop.

Compatibility should therefore be checked in one primary coding agent and at least
one non-Claude integration before claiming broad support. This is a small delivery
smoke test—can it inspect, write the result, ask before unrequested edits, continue,
and verify—not a claim that two different models have equal judgment.

## The Goal Library, playbooks, Studio, and Fixer

### Goal Library

The Goal Library is the complete catalog of Goal Prompts. Search remains useful, but
search cannot be the only way in because a new visitor may not know what exists or
what words to use.

The default front door should begin with recognizable situations, not stacked abstract
taxonomies. The current candidate situations are:

- “I don't know what to check first.”
- “Something is broken or unreliable.”
- “Users aren't understanding, signing up, or coming back.”
- “The product feels messy and I need priorities.”
- “I'm making a risky change.”
- “I need to prove a specific thing works.”

Each situation leads to a small number of relevant individual Goal Prompts and
playbooks. Full search, families, and browse-all remain available beneath that guided
start. The earlier two-axis navigation—abstract outcomes crossed with types of
projects—is rejected as blurry.

Every Goal Prompt detail page should state in concrete language:

- when to use it and when not to;
- what material the agent will inspect;
- the named Markdown result it will leave;
- what a strong result contains;
- whether the same run can continue into changes;
- how any changes will be checked;
- a real example when one exists.

The internal write policy may distinguish read-only, artifact-writing, action-capable,
and verification prompts for safety and linting. That internal taxonomy is not the
public definition of Goal Prompts and should not become another concept the user has
to learn.

### Playbooks and custom sequences

A playbook is a curated sequence of Goal Prompts for a recognizable situation. The
site also already supports a custom sequence: while browsing, the user can add Goal
Prompts and copy one combined conductor prompt. That is the product's native
pre-run batching experience and should be made more discoverable.

### Studio

Studio is not the pre-run prompt selector. It is a separate post-run tool: it loads
one or more Markdown reports, turns their findings into a checklist, and copies a
targeted Fixer or Roadmap prompt from the selected findings.

That distinction is currently not clear enough. The conversation should handle the
normal path from findings to approved action without requiring Studio. Studio remains
an optional batch-triage surface for someone with many reports or a need to compare
and hand-select findings visually. Its value must be validated in beta; it should be
further demoted or removed if that use is not real.

### Fixer

The Fixer is currently a separate Goal Prompt that reads reports, asks the operator to
choose scope, changes code, runs checks, creates commits, and appends `FIXLOG.md`.
Those behaviors remain useful. The user should experience them as the same
conversation continuing into approved action, not as a second product they must find,
understand, and paste manually. “Fixer” may remain an internal/catalog name without
being required vocabulary in the main experience.

## Recommendations and choices

The agent should not present a large arbitrary menu. It should present one reasoned
recommended scope and make clear that ordinary-language corrections are welcome.

A recommendation must explain:

- what evidence supports the finding;
- the causal path from the underlying issue to user or product impact;
- why the agent is confident or uncertain;
- what files or behavior would change;
- why the effort estimate is reasonable;
- what is deliberately left alone and the tradeoff of doing so;
- how the proposed work will be checked.

The user can then say “proceed,” “include all of them,” “do none of this,” “explain
the second one,” or give a different constraint. Those are examples of natural
responses, not buttons or a required menu.

## Saved results and compounding value

The Markdown result is durable working memory for the user, the current agent, a
future agent session, or a collaborator. It is also inspectable evidence: the user can
challenge a claim instead of trusting vanished chat text.

Repeated runs should use the previous result when it exists and lead with meaningful
change: fixed, still present, new, or regressed. The intended compounding loop is:

- the repo's intent constrains later recommendations;
- previous findings are not rediscovered and narrated as if new;
- fixes and verification remain traceable to the finding that caused them;
- a repeat run can report deltas instead of starting from zero.

The exact default directory and migration path for saved results still need a
compatibility decision. The current contract is the repository root, or `reports/`
when that directory already exists. Whatever replaces or preserves it must stay easy
for agents and humans to find, must not create unexplained clutter, and must keep old
collectors and reports working.

Stickiness is not “browser reminders.” The product hypothesis is that a user returns
because the same high-quality goals recur and the saved history makes the next run
more useful. The natural repeat-use trigger must be learned from real use; “before
shipping” and “Claude changed enough code that I feel uncertain” are hypotheses, not
approved positioning.

## Internal efficacy testing

The product's central claim is that its designed instruction produces a better and
more repeatable result than the user's likely first request. That claim needs an
internal test; this is not a step users perform and does not appear in their workflow.

For a representative goal:

1. Freeze one repository snapshot and one concrete task.
2. Run a fresh agent conversation with the short request a user would naturally type.
3. Run a separate fresh conversation on the same snapshot with the relevant Goal
   Prompt, using the same model and comparable settings.
4. Compare both results against known behavior, reproducible issues, or a task-specific
   answer key.
5. Score real findings, false alarms, evidence quality, causal explanation, scope
   control, actionable recommendations, verification quality, completion, time, and
   token cost.
6. Repeat enough times to avoid mistaking one lucky model run for a product effect.

The point is not to prove that longer prompts always win. It is to find where the
Goal Prompt materially improves the work, where it adds cost without value, and where
its structure makes the agent worse. A Goal Prompt that cannot beat or meaningfully
stabilize the plain request should be rewritten, narrowed, combined, or removed.

Prototype this contract privately across representative goal types before applying a
mechanical rewrite to the whole catalog. Once the contract is ratified, migrate all
152 public Goal Prompts—or explicitly version, deprecate, or remove incompatible
ones—before presenting the new behavior as one coherent product.

## Marketing and demonstration rules

Marketing must explain the concrete object and motion before introducing internal
nouns.

It should show:

- a Goal Prompt is a carefully designed instruction copied from the site;
- it is pasted into the coding agent the user already has;
- the agent inspects the user's own files;
- one named, evidence-backed Markdown result is saved;
- actionable findings can continue into authorized, checked changes in the same
  conversation;
- the report and verification record make a later run more informed.

The homepage should not lead with “ship,” “pre-ship,” “Claude Code review,” “memory,”
“workflow,” “session,” “Fixer,” “Studio,” “command,” or “report” before showing what
the thing is and why the saved file helps. These words can appear after the concrete
motion is visible.

Rejected or unvalidated framing includes:

- “before you ship” as the main trigger;
- a generic `/goal` command as the main entry;
- “A Claude Code check that remembers your repo”;
- “review your codebase” without saying what is inspected and why;
- public confidence, severity, or effort labels without supporting reasons;
- a public promise of automatic invocation;
- abstract navigation built from “understand / find / improve” and “website / app /
  API” dimensions;
- claims of stickiness or model portability that have not been observed or tested.

The main demonstration should be a guided visual replay built from a real sanitized
run: the actual Goal Prompt, actual repository evidence, actual saved result, the
scope decision, actual diff, and actual checks. A full run record can remain available
for people who want to inspect the proof. Animation is presentation; reality is the
source material.

## Beta learning

Do not add a public star-rating or review marketplace during the beta. Sparse ratings,
version drift, model differences, and project differences would create misleading
social proof and invite noise before the product has enough use.

Use contextual, opt-in feedback after a run instead:

- Did this help? **Yes / Partly / No**.
- Optional: what was missing, wrong, or unnecessarily difficult?
- With consent, record only minimal context needed to interpret the answer, such as
  the Goal Prompt id, version, host integration, whether action was completed, and
  whether checks passed.

Never collect repository contents, report contents, or code silently. Supplement the
small quantitative signal with moderated tests, interviews, and user-shared sanitized
run records.

## Delivery plan and approval gates

No implementation begins from this document until the operator ratifies the pending
corrections below.

### Gate A — Product contract

- Reconcile this document, `CHARTER.md`, `DECISIONS.md`, and `CLAUDE.md`.
- Define the shared Goal Prompt safety and result schema.
- Resolve the exact plugin namespace and saved-result location/migration.
- Stop for operator review.

### Gate B — Private working prototype

- Prototype the in-conversation continuation on representative investigation,
  decision/artifact, action, and verification goals.
- Test scope corrections, direct authorization, subagent coordination, failed checks,
  null results, and repeat runs.
- Run the internal efficacy comparison on the same fixtures.
- Stop for operator review.

### Gate C — Coherent catalog

- Migrate all 152 Goal Prompts to the approved contract or explicitly version,
  deprecate, or remove exceptions.
- Update playbooks, conductors, Fixer behavior, integrations, collectors, examples,
  schemas, linters, and compatibility paths together.
- Run the full build and quality gates.
- Stop for operator review.

### Gate D — Library and site

- Reorganize the front door around concrete user situations while preserving full
  search, family browsing, playbooks, and custom sequences.
- Rewrite the homepage only after the behavior it describes exists.
- Build the guided real-run demonstration and supporting detail pages.
- Reposition Studio as optional batch triage.
- Stop at a local preview for operator review.

### Gate E — Beta and launch

- Add contextual opt-in feedback and documented privacy boundaries.
- Test the complete path with real external repositories and real target users.
- Publish only claims supported by the observed runs.
- Launch after the operator approves the beta evidence and final site.

## Ratified alignment carried from the conversation

- The product is the quality and repeatability of the designed instruction, not a
  claim that the underlying agent lacks tools.
- Goal Prompts complements skills, plugins, and built-in agent capabilities; those are
  delivery or execution primitives, not the product distinction.
- Core prompts stay model- and host-portable; adapters may use native features with
  fallbacks.
- The same visible conversation continues from findings into approved action.
- Subagents may work behind the coordinator without becoming a user-facing burden.
- Recommendations explain evidence, causal impact, uncertainty, effort, tradeoffs,
  and verification rather than presenting unexplained labels.
- Verification must distinguish pre-existing failures, introduced failures, and
  inconclusive checks; it must never claim success on a broken or untested result.
- The full catalog cannot publicly mix incompatible old and new contracts.
- The demonstration is a guided presentation of a real run, not a fabricated mockup.
- Beta feedback is contextual and opt-in, not a public ratings marketplace.
- Natural repeat-use triggers and stickiness remain hypotheses until observed.

## Pending operator confirmation from the latest review

1. Confirm the corrected shared contract: every Goal Prompt writes one Markdown
   result; not every individual Goal Prompt changes code, but actionable work can
   continue in the same conversation after any needed authorization.
2. Confirm that browse/choose/copy/paste is the primary entry and automatic routing is
   out of launch scope; optional installed integrations expose the same catalog.
3. Confirm the public scope: coding agents broadly, portable by default, with Claude
   Code as a first-class integration rather than a dependency.
4. Confirm Studio's role: post-run visual batch triage, optional and never the normal
   hinge; the catalog's existing custom sequence is the pre-run batching tool.
5. Confirm the internal efficacy test and the small cross-host compatibility smoke
   test as product QA, not user-facing workflow.
6. Confirm replacing the blurry two-axis library organization with the concrete
   situation-first front door described above.
7. Choose or authorize testing of the final non-conflicting Claude Code plugin
   namespace and the long-term saved-result location before Gate A is closed.

## Decision history

- **2026-07-12 — Initial consolidation.** Captured the operator-approved direction
  from the product-alignment conversation and recorded the latest challenged items as
  pending confirmation. The proposed corrections preserve reports as a universal
  contract, website copy/paste and custom sequences as the primary path, explicit
  rather than automatic invocation, coding agents as the public category, the same
  visible conversation for continuation, Studio as a report-findings selector,
  efficacy comparisons as internal product QA, and a situation-first catalog entry
  instead of the proposed abstract axes.
