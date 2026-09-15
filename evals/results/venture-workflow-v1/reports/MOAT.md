# 2026-09-14 — Moat (SIMULATION ONLY)
All Venture · stage 7/8 · brief 66
Run: simulation-tutorfollowup-20260914
Scope: tutorfollowup-us@1
Brief: 66
Status: complete

## Scope
US independent tutors; missed-payment follow-up; automated reminders. Synthetic offline behavioral QA, not real venture evidence. Charter absent; fixed selected candidate and provisional bars unchanged.

## Findings
1. **V66-001 — A subscription is plausible but operating costs are unmeasured**. This matters because access and complaints alone do not establish a viable paid service. Resolve the specified unknowns before any build or external test.

## Models
Provisional $10/tutor/month subscription matches recurring-reminder hypothesis. Manual service could test value but time may dominate; usage billing lacks a measured value unit. No model has sourced buyer acceptance.
## Economics
Assumptions only, USD/month: price 10, variable cash cost 2/tutor, contribution = 10−2 = 8/tutor before labor/acquisition. Assumed fixed cash cost 20 gives cash break-even ceil(20/8)=3 users. At 12 users: revenue 120, variable 24, fixed 20, surplus 76 before labor. Monthly spend 44 fits 100 on these assumptions only.
Sensitivity: variable cost 8 gives contribution 2 and break-even 10; costs >=10 erase positive contribution. Model is not observed economics. Illustrative 1h/customer/month × 12 = 12h/month support + 8h/month sales/build = 20h/month, approximately the 5h/week capacity; spikes could exceed it. Labor value/CAC/payback unknown. No verified acquisition rate.
## Defenses/response
No evidenced moat. Reminder behavior could be copied; no documented timing. Data ownership, integration lock-in, supplier fees and permission design unknown; do not assume protective effects.
## Risk tests
1. Payment intent: 10 conversations, 3h/$0 proposed; pass 2 commitments, stop expansion at zero.
2. Workload/cost: dummy-data walkthrough, 1h/$0 proposed; pass conservative <=5h/week and <=$100/month, stop pilot if exceeded.
3. Permission/delivery: map minimal data and consent, 1h/$0 proposed; pass documented allowed flow and working dummy delivery, stop on unresolved blocker.
Tests are proposed only; external outreach or implementation needs authority.

## Evidence
[Single synthetic packet](../sources/packet.md), S1–S5; created/accessed 2026-09-14; event dates unavailable. Fixture descriptions only; no authentic quotes or external citations. Primary sources, trends and independent verification absent. Repeated citations are not corroboration.
Input report versions:
- [OPPORTUNITIES.md](OPPORTUNITIES.md): `62cc4fba4384b94077ccb393b763fa5d3b48f61c73ee0398bf0242bbe0fee0a7`
- [NICHE.md](NICHE.md): `6918bad9d89c53748a1125563caf39d3ce195b625c8d6e20a4228c7f4e9328c1`
- [DEMAND.md](DEMAND.md): `7d85f09a46b4b69531754c79548c02ba530a400dcefc1868772c33540f2e491c`
- [COMPETITORS.md](COMPETITORS.md): `62f8613d86fce0412a78b6793c1b1a14225941d37a532f7bdf9a70006c0a16fd`
- [MARKET.md](MARKET.md): `62c8be8f4d47aacdae7f84ef9d2fe3c3261b63c16182c06220dac8ce116ff19d`
- [POSITIONING.md](POSITIONING.md): `614382bb421f5bf6bfc71153fdec3b4372e8e0606844fd4b811b7a449435fe55`

## Counterevidence
Two fixture tutors successfully use calendars; no verified willingness to pay. Price and reach are proxies, not proof of purchases. Unknown severity/cost/timing could reverse the hypothesis. No live search was attempted under the explicit offline simulation scope.

## Next steps
Which risks next? Recommend price intent first; no outward tests authorized.
No outreach, purchases, code changes, commits or publishing performed. See stage-specific tests above; delegated continuation applies where recorded.

## Review revalidation — 2026-09-14
Added tests do not measure willingness to pay, variable costs, labor or consent; economics assumptions and ranked risk tests remain provisional. No synthetic source facts changed; this report retains its substantive conclusion after explicit input review.

## Fresh-session review revalidation
Reviewed refined upstream tests: no measured costs, adoption or defense; economics/fit uncertainty and model assumptions remain unchanged. The added test rules are prospective hypotheses, not simulated observations.
