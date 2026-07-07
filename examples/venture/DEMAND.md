# DEMAND.md
*Produced by brief 62 · Pain & Demand Mining, run as a Gut Check dogfood on the niche **flaky-test detection & management for CI**. Sample report — a Venture-family run against a candidate that does not exist yet. All sources accessed 2026-07-07.*

## The pain hypothesis
Engineering teams with meaningful CI suites hit tests that fail nondeterministically — pass on rerun, no code change. The pain: wasted debugging hours, blocked merges, and eroded trust in the suite ("just hit rerun"). Who hurts: platform/DevEx and QA engineers at teams past ~10 engineers where CI is a shared dependency. Trigger: per-PR and per-merge — a recurring, not occasional, tax.

## The evidence wall

**Vendors lead with the emotion, not the feature — a tell that the pain is felt, not abstract.**
- Trunk's flaky-tests landing headline is verbatim *"Engineers Hate Flaky Tests. We can help."* — `https://trunk.io/flaky-tests` (2026-07-07). Leading with the feeling is a positioning bet that the audience self-identifies with the frustration.
- BuildPulse's product headline is verbatim *"Find every flaky test. Then fix it."* — `https://buildpulse.io/products/flaky-tests` (2026-07-07).

**Named practitioners describe the pain in their own words** (vendor testimonials — treat as favorable but real, attributed people):
- Ziv Gutman, Automation & QA Engineer @ Growthspace: *"I primarily focused on the flaky tests tab and found all the information I sought. The app provided an excellent summary of our E2E pain points."* — `https://trunk.io/flaky-tests` (2026-07-07).
- Joshua Inoa, Engineering Manager, Release Infrastructure @ Brex: *"We would have never known how many flaky tests we had exactly, or to what level each of them was flaky."* — same source.

**Even Google, with the deepest test infra on earth, admits it cannot fully quantify the cost** — a severity marker in itself:
- Google Testing Blog: *"We do not currently keep accurate count of the number of times that flaky tests are really masking bugs in the code."* — `https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html` (2026-07-07).
- Same post: *"We are currently working to better analyze the cost to the developer workflows caused by test flakiness — we do not yet have anything publishable out of that effort."* If Google is still measuring it a decade on, the pain outruns the tooling.

## Spend and workaround table
| Solution | Price signal | Adoption signal | Source (2026-07-07) |
|---|---|---|---|
| Trunk Flaky Tests | Free for OSS; paid tiers not on the page | Logos claimed: Faire, Brex, Gusto, Zillow, Cockroach Labs, Google, Retool | `https://trunk.io/flaky-tests` |
| BuildPulse | "Start for free" free tier; per-repo paid (per category coverage) | Atlassian Marketplace listing; iOS/Android CI writeups | `https://buildpulse.io/products/flaky-tests` |
| Datadog Test Optimization | Usage-based; enterprise reported to exceed ~$100K/yr | Embedded in a large observability platform | search synthesis, secondary — flagged below |
| Retry plugins (pytest-rerunfailures, Jest retry, CI "re-run failed jobs") | Free / built-in | The default status-quo workaround everywhere | ecosystem-common |

**The workaround census confirms latent demand:** the near-universal duct tape is *rerun-until-green* — retry plugins and CI "re-run failed jobs" buttons. That is a purchase order waiting for a product: teams already spend engineering time papering over flakiness with no visibility into it.

## Trunk's own impact calculator (vendor arithmetic, shown for transparency)
For 10 engineers / 1,000 commits / CI 5–90 min / 0.1–1% flaky rate, Trunk's on-page calculator estimates **~56 engineering hours and ~48 CI hours wasted monthly** — `https://trunk.io/flaky-tests` (2026-07-07). Vendor-favorable inputs, but even discounted heavily it clears "annoying enough to pay for."

## The honest counter-read
The disconfirming interpretation gets equal weight: **this pain may be real but not independently monetizable.** Flaky-test detection is increasingly a *feature*, not a *product* — CI platforms (CircleCI, Buildkite, GitHub) and observability suites (Datadog) are absorbing it. The emotional vendor headlines could signal a crowded category shouting to be heard, not a green field. The status-quo workaround (free retry plugins) is *good enough* for most teams, which caps willingness to pay. And the OSS-free pricing across specialists suggests the paid wedge is narrow.

## The verdict (graded, arithmetic visible)
- Severity: **High** — trust erosion + per-merge blockage; vendors lead with the emotion.
- Frequency: **High** — per-PR/per-merge recurring trigger.
- Evidence density: **Medium** — strong vendor + Google primary quotes; thin on independent, dated practitioner complaints in this pass (a gap, see silence test).
- Spend proof: **Medium** — real paid products exist, but heavy OSS-free tiers and platform-bundling cloud the standalone willingness-to-pay.
- Rough grade = High × High × Medium × Medium → **promising pain, contested monetization.** Proceed to competitor teardown before any further conviction.

## The silence test
Where evidence should be denser but wasn't in this compact pass: **independent, dated, verbatim developer complaints** (Reddit/HN threads with URLs) — the general-web search returned synthesized summaries rather than quotable, linkable posts, so this report leans on vendor and Google primaries. That thinness is itself data: the loudest voices here are *sellers*, not *sufferers*, which the counter-read weighs against the idea.

## The ten people
Where to find ten sufferers to talk to this week: platform/DevEx engineers in the Trunk and BuildPulse customer orgs' public talks; the `#ci` and `#testing` channels of large OSS Slacks/Discords; authors of pytest-rerunfailures / Jest-retry issues; QA leads posting in r/QualityAssurance and r/ExperiencedDevs; and DevEx ICs at the named logo companies (Gusto, Retool, Zillow).

*Report only — proceed to competitor teardown, pivot the pain (e.g. toward CI-cost rather than flakiness), or drop it?*
