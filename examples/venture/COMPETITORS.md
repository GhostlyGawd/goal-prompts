# COMPETITORS.md
*Produced by brief 63 · Competitor Teardown, run as a Gut Check dogfood on **flaky-test detection & management for CI**. Sample report. All sources accessed 2026-07-07; claims from general-web search synthesis (rather than a directly fetched primary page) are marked **[secondary]**.*

## The matrix
| Vendor | Positioning (their words / their page) | Price signal | Traction proxy | Source (2026-07-07) |
|---|---|---|---|---|
| **Trunk Flaky Tests** | *"Engineers Hate Flaky Tests. We can help."* — detect, quarantine, eliminate across any language, test runner, CI | Free for OSS; paid tiers not shown on page | Logos: Faire, Brex, Gusto, Zillow, Cockroach Labs, Google, Retool | `https://trunk.io/flaky-tests` |
| **BuildPulse** | *"Find every flaky test. Then fix it."* — specialist, fast setup, per-repo | "Start for free"; per-repo paid **[secondary]** | Atlassian Marketplace app; mobile-CI writeups | `https://buildpulse.io/products/flaky-tests` |
| **Datadog Test Optimization** | Flaky management embedded in CI Visibility / observability | Usage-based; enterprise reported >~$100K/yr **[secondary]** | Bundled into a large platform footprint | `https://www.datadoghq.com/pricing/` **[secondary]** |
| **Status quo** (retry plugins, CI "re-run failed") | "Just rerun it" | Free / built-in | Ubiquitous default | ecosystem-common |

## Positioning claims — the cluster
Two of the specialists lead with **emotion + eliminate language** ("hate," "find every… then fix"). Datadog leads with **integration/visibility** ("part of your CI observability"). The words *everyone* uses — *detect, quarantine, fix* — are free differentiation for whoever stops using them and instead promises *prevent* or *root-cause-once*. The generic-marketing whitespace is "why the test is flaky," not "which tests are flaky."

## Complaint synthesis (market truths vs per-vendor ceilings)
- **Market truth (shared gripe):** the category converges on *detect → quarantine → dashboard*; buyers increasingly ask "and then what?" — quarantine hides the flake, it doesn't fix it. The unmet job is **durable root-causing and prevention**, which even Google frames as unsolved (see DEMAND.md's Google primary quotes).
- **Per-vendor ceiling — specialists (Trunk, BuildPulse):** standalone tools must justify a *new* line item against CI platforms that bundle detection for free. Their ceiling is procurement, not capability.
- **Per-vendor ceiling — Datadog:** power is gated behind platform adoption and cost; reported enterprise spend >~$100K/yr **[secondary]** prices out exactly the small/mid teams who feel flakiness most acutely.
*(Independent dated review quotes were not linkable in this compact pass — flagged as an evidence gap, consistent with DEMAND.md's silence test.)*

## Traction proxies
Trunk publicly claims recognizable logos (Brex, Gusto, Zillow, Cockroach Labs, Retool, Google) on the flaky-tests page — the strongest single traction signal in the set (`https://trunk.io/flaky-tests`, 2026-07-07). The existence of "best flaky-test tools in 2026" roundups (e.g. Mergify's *"How to Get Rid of Flaky Tests: 5 Tools to Know"* `https://articles.mergify.com/how-to-get-rid-of-flaky-tests-lethal-tools/`; TestDino's *"9 Best Flaky Test Detection Tools… 2026"* `https://testdino.com/blog/flaky-test-detection-tools`, both 2026-07-07) is itself a traction proxy: enough vendors exist to fill a listicle — a crowding signal, not a green field.

## Release pulse
Not independently verified in this compact pass (changelogs not fetched). The presence of 2026-dated third-party roundups suggests the category is actively marketed rather than in maintenance decay. **Flagged as unverified.**

## Moat inspection
- **Trunk / BuildPulse:** moat = breadth of CI/test-runner integrations + accumulated per-repo flakiness history (a mild data network effect). Replicable head start, not a deep moat.
- **Datadog:** moat = platform lock-in and existing contracts — the strongest and least assailable, but also the reason it can't chase the low end.
- **Status quo:** the real competitor. "Rerun until green" is free, zero-integration, and *culturally entrenched*. Any entrant's hardest opponent is inertia, not another vendor.

## Gap analysis
| Gap | Evidence it's real | Why it's open | Graveyard check |
|---|---|---|---|
| **Root-cause once, prevent recurrence** (not just quarantine) | Google's own "unsolved cost" quotes; buyer "and then what?" | Genuinely hard — needs code/trace analysis, not just pass/fail history | Academic (Google's *DeFlake* research `https://research.google/pubs/...`, 2026-07-07) but few durable commercial products — *open because hard* |
| **Sub-Datadog price for small/mid teams** | Enterprise pricing prices out the loudest sufferers **[secondary]** | Specialists chase OSS-free + mid-market; true SMB monetization is thin | Free retry plugins occupy this floor — *partly open-for-a-reason* |
| **Non-JS / polyglot depth** | JS-heavy tooling (Cypress/Playwright ecosystems) | Effort to support JVM/Go/Python matrices | Develocity owns JVM; open elsewhere but fragmented |

## The wedge shortlist
1. **Root-cause & prevention, not quarantine** — the one gap open because it's *hard*, not worthless; aligns with the unmet "and then what?" job.
2. **Opinionated SMB tier** — dead-simple, priced for teams Datadog ignores; risk: colliding with free retry plugins.
3. **Polyglot-first** — depth where the JS-centric field is thin; risk: breadth burns runway.

*Report only — which gap to build positioning around before the verdict?*
