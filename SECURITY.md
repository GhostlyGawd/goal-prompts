# SECURITY.md
*Produced by brief 06 · Security & Privacy Audit, run against this repo (goal-prompts, v0.4). Part of the sample-report gallery.*

## Posture summary
Static site with no backend, no accounts, no stored user data beyond device-local preferences — the attack surface is client-side JavaScript, the supply chain, and the curl-pipe-to-shell installer pattern. Trust boundaries: the search box (only user input reaching the DOM) and everything downloaded by the installer.

## Findings

**1. Self-XSS at the search/empty-state boundary — was High-adjacent · FIXED in 0.4**
Location: `template.html` empty-state rendering. Risk: user-typed query flowed into `innerHTML`; self-only today, reflected the day anyone adds a `?q=` parameter. Fix shipped: `textContent` construction. Adopted default: user input never meets `innerHTML` anywhere in this codebase.

**2. Installer had no integrity check — Medium · FIXED in 0.4**
Location: `install`. Risk: curl-pipe-sh delivers whatever the CDN serves; users had no way to detect tampering or corruption. Fix shipped: `build.py` publishes `checksums.txt` (sha256 of both archives); the installer downloads to a temp file and verifies before extracting when `sha256sum` exists, hard-failing on mismatch.

**3. No security headers — Medium · FIXED in 0.5**
Location: `vercel.json` (absent `headers` block). Risk: no `X-Content-Type-Options`, `Referrer-Policy`, or frame-ancestors control; a strict CSP is complicated by the inline script and Google Fonts but a baseline is free. Fix: add nosniff, `Referrer-Policy: strict-origin-when-cross-origin`, and `frame-ancestors 'self'` via a headers block. Fix shipped: `vercel.json` now sends `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, and `Content-Security-Policy: frame-ancestors 'self'` on every route.

**4. Runtime third-party dependency: Google Fonts — Low · FIXED in 0.8**
Location: `template.html` head. Risk: availability and a request leak to a third party on every visit. Fix shipped: both families vendored as woff2 under `fonts/` (OFL); no `fonts.googleapis`/`gstatic` requests remain in the built site (`224243d`). This also cleared the last blocker for the offline PWA.

**5. MCP server trust scope — informational**
`mcp/server.cjs` reads only its own package files, takes no network or filesystem input beyond tool arguments, and executes nothing. The meaningful trust decision is `npx github:` itself — users execute this repo's code; the linter and CI keep the diff surface reviewable.

## Fix-this-week
Finding 3 shipped in 0.5 (the headers block below). Finding 4 (self-hosting fonts) shipped in 0.8 — no open findings remain.

## Defaults to adopt
User input renders via `textContent` only; anything piped to a shell ships a published checksum; new runtime third-party dependencies require a reason in the PR.

*Report only — which fixes should be made?*
