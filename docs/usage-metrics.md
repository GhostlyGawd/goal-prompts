# Usage metrics — counting brief fetches without a backend

The catalog's one honest usage signal is already in the traffic: every brief
lives at a stable URL (`/raw/<id>.md`), and every consumer — the copy button
(indirectly, via page loads), conductors, the MCP server's cold path, the
curl installer, CI workflows — ultimately fetches those files. Counting
`raw/*.md` requests per path per day answers "which briefs get run" without
cookies, scripts, or user tracking.

Nothing in this document is live. (The site itself does ship analytics now —
the anonymous Vercel Web Analytics beacon plus custom events like
`copy_prompt` and `mark_run` — but those only see browser visits; the
raw-fetch counting designed here, which covers conductors, the MCP server,
the curl installer, and CI, is still off.)

## Option 1 — Vercel logs (zero code)

Vercel records every request. Two ways to read them:

- **Runtime Logs / Observability** in the dashboard: filter on
  `pathname:/raw/` and group by path. Good for a spot check, capped
  retention on the free tier.
- **Log Drains** (Pro): stream request logs to any HTTPS endpoint or a
  provider (Axiom, Datadog, …) and aggregate `GET /raw/<id>.md` counts
  there. No change to this repo at all.

This is the recommended starting point: the deploy stays static, nothing can
break, and the numbers cover every consumer including `curl`.

## Option 2 — Edge Middleware + KV (per-path counters in-house)

A tiny middleware increments a counter per brief per day and passes the
request through untouched. See `middleware.js.example` at the repo root —
it is inert on purpose (Vercel only executes a file named exactly
`middleware.js`).

To activate:

1. Create a KV/Redis store in the Vercel dashboard (Storage → Upstash for
   Redis or equivalent) and link it to the project — that injects
   `KV_REST_API_URL` / `KV_REST_API_TOKEN` env vars.
2. Rename `middleware.js.example` → `middleware.js` and deploy.
3. Read the counters with any Redis client, or add a tiny `/api/metrics`
   endpoint later.

Why it isn't shipped live: the project has no KV store configured, and a
middleware that references missing env vars turns a working static deploy
into a broken one. The example fails open (counting is fire-and-forget;
errors never block the response), but it stays `.example` until the store
exists.

## What to count (and what not to)

- Count: `GET /raw/<id>.md` per id per UTC day; optionally the conductor
  files (`playbook-*.md`, `family-*.md`) and `commands.tar.gz` (installs).
- Don't count: HTML page views (that's marketing, not usage), anything
  per-user or per-IP (no identifiers, no fingerprinting — a count per path
  per day is the whole schema).
- The `sw.js` service worker serves cached HTML offline but never caches
  `raw/*.md`, so fetch counts stay honest.

## Reading the numbers

A brief with rising fetches is earning its place; a family nobody fetches is
a candidate for `26 · Prune` treatment. Fold the monthly counts into
`metrics.json` (the same out-of-band pattern as the star count in
`scripts/refresh-stars.py`) if the site should ever show them.
