#!/usr/bin/env python3
"""Build the Goal Prompts site + machine-readable surfaces from prompts/**/*.md.

Outputs (all committed, all deterministic, stdlib only — this also runs on Vercel):
  index.html            the catalog UI (prompts + playbooks injected into template.html)
  raw/<id>.md           brief bodies at stable URLs, for agents to fetch
  raw/playbook-<key>.md conductor prompts that run a whole playbook
  b/<id>.html           per-brief pages with their own OG tags (unfurl + redirect)
  catalog.json          machine-readable index (consumed by the MCP server)
  commands.tar.gz/.zip  Claude Code slash commands, used by /install
  plugin/               the Claude Code plugin (manifest + commands/)

The linter enforces the house rules on every brief: front matter complete,
4-phase skeleton, a Rules section, the ask-first ending, and body < 4,000 chars.
"""
import gzip, io, json, os, re, shutil, sys, tarfile, zipfile
from pathlib import Path

ROOT = Path(__file__).parent
DEFAULT_BASE = "https://goal-prompts.vercel.app"
# Forks: set GOAL_PROMPTS_BASE to your deployment URL — every generated
# surface (site, raw/, conductors, catalog.json, brief bodies) follows it.
BASE = os.environ.get("GOAL_PROMPTS_BASE", DEFAULT_BASE).rstrip("/")
LIMIT = 4000
FAMILY_ORDER = ["Venture", "Product", "Quality", "Speed", "Trust", "Compliance",
                "Growth", "Team", "API", "Clarity", "Design", "Data", "Ops",
                "Reliability", "Subtract", "Meta", "Act", "Build", "Agent",
                "Automation", "AI-UX", "AI-Ethics"]
# family colors — the structural signature: color = family, everywhere.
# Source of truth for Python (og.py imports these); template.html's .f-* CSS
# rules must carry the same values for the JS-rendered catalog.
FAMILY_COLORS = {
    "Venture": "#C878F0", "Product": "#E8B44C", "Quality": "#E8705F",
    "Speed": "#4D9FFF", "Trust": "#52C280", "Growth": "#A98CF5",
    "Team": "#3FC1C9", "Clarity": "#9AD4E8", "Design": "#5CE8A0",
    "Data": "#F0904A", "Ops": "#B4C64A", "Subtract": "#E87FB0",
    "Meta": "#C4CBD8", "Act": "#E84C3D", "Agent": "#8B7CF8",
    "Automation": "#E8DE5A", "AI-UX": "#F06FD8", "Compliance": "#8892B0",
    "API": "#2CB5C4", "Reliability": "#5FC08A", "AI-Ethics": "#6E8AF0",
    "Build": "#8CD94C",
}
REQUIRED = ["id", "title", "family", "question", "output", "tagline"]
# Filenames that mean something else on GitHub — a brief writing one would
# shadow the repo's own community files, so the linter forbids them as outputs.
RESERVED_OUTPUTS = {"SECURITY.md", "README.md", "LICENSE.md", "CONTRIBUTING.md",
                    "CODE_OF_CONDUCT.md", "SUPPORT.md", "GOVERNANCE.md",
                    "CHANGELOG.md"}
# 47 · The Fixer is exempt from the dated re-run rule: FIXLOG.md is
# append-only history and every session entry is already dated, so a
# "lead with what changed" header would fight its own format.
DATED_REPORT_EXEMPT = {"47"}
# Briefs where a "no <surface> here" null report could never legitimately
# fire: subjects every repo has (quality, debt, pruning, the Meta/Act layers
# that operate on the repo itself) and audits whose subject's absence IS the
# primary finding (02 missing tests, 16 missing docs). 06 belongs here too:
# every repo has an attack surface — its own supply chain, secrets in git,
# config — so a "no attack surface" escape could never truthfully fire.
NULL_REPORT_EXEMPT = {"00", "01", "02", "06", "13", "16", "26", "27", "28",
                      "29", "46", "47"}


def sort_key(p: dict) -> tuple:
    """Catalog order: family (curated), then id — numerically, so 45 < 106."""
    return (FAMILY_ORDER.index(p["family"]), int(p["id"]))


def fail(msg: str) -> None:
    sys.exit("FAIL " + msg)


def parse(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3 or parts[0].strip():
        fail(f"{path}: missing front matter block")
    meta = {}
    for line in parts[1].strip().splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"')
    for k in REQUIRED:
        if not meta.get(k):
            fail(f"{path}: front matter missing '{k}'")
    if not re.fullmatch(r"\d{2,3}", meta["id"]):
        fail(f'{path}: id "{meta["id"]}" must be 2–3 digits, zero-padded and '
             f'quoted (like id: "07") — it orders the catalog numerically')
    if meta["family"] not in FAMILY_ORDER:
        fail(f"{path}: unknown family '{meta['family']}'")
    if '"' in meta["tagline"]:
        fail(f"{path}: tagline may not contain double quotes")
    if meta.get("related"):
        meta["related"] = [t for t in re.split(r"[,\s]+", meta["related"]) if t]
    meta["body"] = parts[2].strip()
    if BASE != DEFAULT_BASE:
        meta["body"] = meta["body"].replace(DEFAULT_BASE, BASE)
    meta["chars"] = len(meta["body"])
    meta["slug"] = re.sub(r"^\d+-", "", path.stem)
    meta["_path"] = str(path.relative_to(ROOT))
    return meta


def lint(p: dict) -> list:
    """The house rules, enforced. Returns a list of violations."""
    v, body = [], p["body"]
    for n in (1, 2, 3, 4):
        if f"## Phase {n}" not in body:
            v.append(f"missing '## Phase {n}' header")
    if "## Rules" not in body:
        v.append("missing '## Rules' section")
    if "Report only — end by asking" not in body:
        v.append("missing the ask-first ending ('Report only — end by asking …')")
    if not re.fullmatch(r"[A-Z0-9-]+\.md", p["output"]):
        v.append(f"output '{p['output']}' must look like REPORT.md")
    if f"`{p['output']}` at repo root" not in body:
        v.append(f"body must name its report ('… `{p['output']}` at repo root')")
    if len(p["tagline"]) > 170:
        v.append(f"tagline is {len(p['tagline'])} chars (max 170)")
    phase2 = re.search(r"## Phase 2.*?(?=## Phase 3|\Z)", body, re.S)
    lenses = re.findall(r"(?m)^\d+\. \*\*", phase2.group(0)) if phase2 else []
    if lenses and not 4 <= len(lenses) <= 12:
        v.append(f"{len(lenses)} lenses (want 4–12)")
    phase4 = re.search(r"## Phase 4.*?(?=\n## |\Z)", body, re.S)
    if (p["id"] not in DATED_REPORT_EXEMPT
            and "already exists" not in (phase4.group(0) if phase4 else "")):
        v.append("Phase 4 must date the report and handle re-runs "
                 "('… already exists from a previous run …')")
    rules = re.search(r"## Rules.*?(?=\n## |\Z)", body, re.S)
    rules_txt = rules.group(0) if rules else ""
    if "reports/` directory" not in rules_txt:
        v.append("Rules must offer the reports/ directory option "
                 "('If a `reports/` directory exists at the repo root …')")
    if p["id"] not in NULL_REPORT_EXEMPT and "null report" not in rules_txt:
        v.append("Rules must carry the null-report escape ('… null report …') "
                 "or the id joins NULL_REPORT_EXEMPT in build.py")
    if p["chars"] > LIMIT:
        v.append(f"body is {p['chars']} chars (max {LIMIT})")
    if p["output"] in RESERVED_OUTPUTS:
        v.append(f"output '{p['output']}' is a reserved GitHub/community "
                 f"filename — pick one that can't shadow it")
    if p.get("_path"):
        fname = Path(p["_path"]).name
        if not fname.startswith(p["id"] + "-"):
            v.append(f"filename '{fname}' must be prefixed with id '{p['id']}'")
    if p.get("example") and not p["example"].startswith("/"):
        v.append(f"example '{p['example']}' must be a root-relative path like /BUGS.md")
    elif p.get("example") and not (ROOT / p["example"].lstrip("/")).exists():
        v.append(f"example '{p['example']}' does not exist in the repo")
    return v


def lint_catalog(prompts: list) -> list:
    """Cross-brief rules: every report filename must be unique — two briefs
    writing the same file would silently clobber each other's reports — and
    every `related:` reference must point at a real, different brief (the
    "pairs well with" cards on b/ pages render straight from it)."""
    v, seen = [], {}
    ids = {p["id"] for p in prompts}
    for p in prompts:
        if p["output"] in seen:
            v.append(f"briefs {seen[p['output']]} and {p['id']} both write "
                     f"'{p['output']}' — outputs must be unique")
        else:
            seen[p["output"]] = p["id"]
        for r in p.get("related", []):
            if r == p["id"]:
                v.append(f"brief {p['id']} lists itself as related")
            elif r not in ids:
                v.append(f"brief {p['id']}: related id '{r}' does not exist "
                         f"in the catalog")
    return v


def lint_family_icons(template: str) -> list:
    """Every family in FAMILY_ORDER must have a FAM_ICON entry in template.html
    AND a matching <symbol> — otherwise the hero chart and finder silently fall
    back to the Meta icon (the 17-of-21 drift this guards against)."""
    m = re.search(r"const FAM_ICON = \{(.*?)\};", template, re.S)
    icons = dict(re.findall(r'"?([\w-]+)"?\s*:\s*"([\w-]+)"', m.group(1))) if m else {}
    symbols = set(re.findall(r'<symbol id="([\w-]+)"', template))
    v = []
    for fam in FAMILY_ORDER:
        sym = icons.get(fam)
        if not sym:
            v.append(f"family '{fam}' has no FAM_ICON entry in template.html")
        elif sym not in symbols:
            v.append(f"family '{fam}' maps to '{sym}' but template.html has "
                     f"no <symbol id=\"{sym}\">")
    return v


def conductor(pb: dict, by_id: dict) -> str:
    """A meta-prompt that runs every brief in a playbook, in order.

    The instruction text has siblings in mcp/server.cjs (conductorText) and
    template.html (makeConductor); scripts/mcp-smoke.cjs asserts the canonical
    sentences match across all three, so edit them together. The 16-stage cap
    is the same policy make_conductor enforces — a family growing past 16
    briefs must fail here loudly, not drift past what the server will compose.
    """
    if len(pb["ids"]) > 16:
        sys.exit(f"FAIL conductor '{pb['name']}' has {len(pb['ids'])} stages — "
                 f"the cap is 16 (mcp/server.cjs make_conductor enforces the "
                 f"same); split it into two conductors")
    stages = []
    for n, pid in enumerate(pb["ids"], 1):
        p = by_id[pid]
        stages.append(f"{n}. **{pid} · {p['title']}** — fetch {BASE}/raw/{pid}.md"
                      f" → writes `{p['output']}`")
    plural = "briefs" if len(pb["ids"]) > 1 else "brief"
    return f"""# Playbook: {pb['name']} (conductor)

You are working inside this repo. Mission: execute the **{pb['name']}** playbook — {len(pb['ids'])} audit {plural} in sequence, each producing one report file at the repo root (or in `reports/`, if the repo has that directory).

{pb['desc']}

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. If your harness can run subagents or fresh sessions, run each stage in one — a stage needs only the earlier report files at the repo root and in `reports/`, never this conversation.
3. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
4. Confirm the report file exists (at the repo root or in `reports/`) before moving on.
5. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
{chr(10).join(stages)}

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch {BASE}/raw/28.md (Roadmap Synthesis) to merge the reports at the repo root and in `reports/` into one sequenced plan.

## Rules
- If a fetch fails, retry once; if it still fails, use the locally installed /goal:<slug> (or /goal-<slug>) command or the goal-prompts MCP get_brief tool for that stage; if neither exists, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists (at the repo root or in `reports/`), ask whether to re-run or skip that stage.
- A conductor caps at 16 stages — for a longer campaign, split it into two conductors and run them back-to-back.
"""


SERVICE_WORKER = """/* goal-prompts service worker — generated by build.py; do not hand-edit.
 * Precaches the app shell + self-hosted fonts so the catalog, Studio, and
 * Vitals Viewer work offline. HTML is network-first (fresh when online,
 * cached when not); static assets are cache-first. Version is a content
 * hash, so a deploy makes a new cache and the old one is purged. */
"use strict";
var CACHE = "goal-prompts-__VERSION__";
var PRECACHE = __PRECACHE__;
self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) {
    return Promise.all(PRECACHE.map(function (u) {
      return c.add(new Request(u, { cache: "reload" })).catch(function () {});
    }));
  }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.map(function (k) { if (k !== CACHE) return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;
  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return;   // never touch cross-origin (GitHub, analytics)
  if (url.pathname.indexOf("/raw/") === 0) return;   // raw briefs stay network-only — their fetch counts are the usage metric (docs/usage-metrics.md)
  var isHTML = req.mode === "navigate" ||
    (req.headers.get("accept") || "").indexOf("text/html") !== -1;
  if (isHTML) {
    e.respondWith(fetch(req).then(function (res) {
      var copy = res.clone();
      caches.open(CACHE).then(function (c) { c.put(req, copy); });
      return res;
    }).catch(function () {
      return caches.match(req).then(function (m) { return m || caches.match("/"); });
    }));
    return;
  }
  e.respondWith(caches.match(req).then(function (m) {
    return m || fetch(req).then(function (res) {
      if (res && res.status === 200 && res.type === "basic") {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
      }
      return res;
    }).catch(function () { return m; });
  }));
});
/* Opt-in weekly Vitals reminder (see the landing's reminder toggle). Fires only
 * when the user explicitly enabled it and the browser supports periodicSync
 * (Chromium, installed PWA) — nothing is auto-enabled and nothing leaves the
 * device. */
self.addEventListener("periodicsync", function (e) {
  if (e.tag !== "vitals-weekly") return;
  e.waitUntil(self.registration.showNotification("Weekly Vitals is due", {
    body: "Ten minutes for fresh trend arrows on your repo.",
    icon: "/icons/icon-192.png", badge: "/icons/icon-192.png",
    tag: "vitals-weekly", data: { url: "/#29" }
  }));
});
self.addEventListener("notificationclick", function (e) {
  e.notification.close();
  var url = (e.notification.data && e.notification.data.url) || "/";
  e.waitUntil(clients.matchAll({ type: "window" }).then(function (cs) {
    for (var i = 0; i < cs.length; i++) {
      if (cs[i].url.indexOf(url) !== -1 && "focus" in cs[i]) return cs[i].focus();
    }
    if (clients.openWindow) return clients.openWindow(url);
  }));
});
"""


# =====================================================================
# Detail pages — every brief and every playbook gets a full, crawlable,
# conversion-shaped page (not a redirect stub). The catalog stays the shop
# floor; these are the product pages. All markup is generated here from the
# same brief bodies the linter guards, so the pages can never drift from the
# prompts they describe.
# =====================================================================

def esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def attr(s: str) -> str:
    return esc(s).replace('"', "&quot;")


def md_inline(s: str) -> str:
    """The tiny slice of Markdown the briefs use inline: **bold** and `code`."""
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def md_block(text: str) -> str:
    """Render a chunk of a brief body: paragraphs, and -/1. lists."""
    out, para, items = [], [], []

    def flush_p():
        if para:
            out.append("<p>" + md_inline(" ".join(para).strip()) + "</p>")
            para.clear()

    def flush_l():
        if items:
            out.append("<ul>" + "".join("<li>" + md_inline(x) + "</li>"
                                        for x in items) + "</ul>")
            items.clear()

    for line in text.splitlines():
        st = line.strip()
        if not st:
            flush_p(); flush_l(); continue
        m = re.match(r"^(?:[-*]|\d+\.)\s+(.*)$", st)
        if m:
            flush_p(); items.append(m.group(1))
        else:
            flush_l(); para.append(st)
    flush_p(); flush_l()
    return "\n".join(out)


def _numbered_bold(chunk: str) -> list:
    """`N. **Name** — description` rows (Phase-2 lenses, Phase-4 sections)."""
    rows = []
    for m in re.finditer(r"(?m)^\d+\.\s+\*\*(.+?)\*\*\s*[—–-]?\s*(.*)$", chunk):
        rows.append((m.group(1).strip(), m.group(2).strip()))
    return rows


def _gist(chunk: str) -> str:
    """One-line essence of a phase, in editorial voice: its first descriptive
    sentence, cleaned — no dangling colons, no pasted operator-gate lines."""
    for line in chunk.splitlines():
        st = line.strip()
        if not st:
            continue
        if "end by asking" in st.lower():
            continue  # the ask-first gate is a rule, not a description
        st = re.sub(r"^(?:[-*]|\d+\.)\s+", "", st)
        st = re.sub(r"\*\*(.+?)\*\*", r"\1", st)
        st = st.replace("`", "")
        st = re.split(r"(?<=[a-z0-9])[.;:]\s", st)[0]
        st = st.rstrip(" ,;:—–-")
        if not st:
            continue
        if len(st) > 118:
            return st[:118].rstrip(" ,") + "…"
        st = st[0].upper() + st[1:]
        return st + ("" if st.endswith((".", "!", "?", "…")) else ".")
    return ""


def brief_parts(body: str) -> dict:
    """Structured pieces of a brief, leaning on the house structure the linter
    enforces: a `# Goal:` header, four `## Phase N` sections, and `## Rules`."""
    pre, sections = "", []
    cur_h, cur = None, []
    for line in body.splitlines():
        m = re.match(r"^##\s+(.*)$", line)
        if m:
            if cur_h is not None:
                sections.append((cur_h, "\n".join(cur).strip()))
            cur_h, cur = m.group(1).strip(), []
        elif cur_h is None:
            pre += line + "\n"
        else:
            cur.append(line)
    if cur_h is not None:
        sections.append((cur_h, "\n".join(cur).strip()))

    intro = re.sub(r"^#\s+.*\n?", "", pre, count=1).strip()

    phases, lenses, report, rules = [], [], [], []
    for head, chunk in sections:
        pm = re.match(r"Phase\s+(\d)\s*[—–-]?\s*(.*)$", head)
        if pm:
            n = int(pm.group(1))
            phases.append({"n": n, "name": pm.group(2).strip(), "gist": _gist(chunk)})
            if n == 2:
                lenses = _numbered_bold(chunk)
                if not lenses:
                    lenses = []  # prose Phase 2 (e.g. 47 · The Fixer)
                    # descriptive area only — the operator gate stays in the
                    # full verbatim brief, not the "how the pass runs" summary
                    prose_src = "\n".join(
                        l for l in chunk.splitlines()
                        if "end by asking" not in l.lower())
                    phases[-1]["prose"] = md_block(prose_src)
            if n == 4:
                report = _numbered_bold(chunk)
        elif head.lower().startswith("rules"):
            rules = [re.sub(r"^[-*]\s+", "", l.strip())
                     for l in chunk.splitlines() if l.strip().startswith(("-", "*"))]
    phases.sort(key=lambda p: p["n"])
    return {"intro": intro, "phases": phases, "lenses": lenses,
            "report": report, "rules": rules}


# ---- shared shell: tokens, components, nav, footer -------------------

BRAND_MARK = (
    '<svg class="mark" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true">'
    '<rect x="1" y="7" width="3.4" height="11" rx="1.7" fill="#E8B44C"/>'
    '<rect x="6.9" y="3" width="3.4" height="18" rx="1.7" fill="#52C280"/>'
    '<rect x="12.8" y="6" width="3.4" height="13" rx="1.7" fill="#4D9FFF"/>'
    '<rect x="18.7" y="9" width="3.4" height="8" rx="1.7" fill="#C878F0"/></svg>')

# Favicon = the bar mark (same geometry as BRAND_MARK), so the browser tab
# echoes the header logo instead of an unrelated "GP" monogram (B1).
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
           "viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='13' "
           "fill='%23131417'/%3E%3Cg transform='translate(10 9.2) scale(1.9)'%3E"
           "%3Crect x='1' y='7' width='3.4' height='11' rx='1.7' fill='%23E8B44C'/%3E"
           "%3Crect x='6.9' y='3' width='3.4' height='18' rx='1.7' fill='%2352C280'/%3E"
           "%3Crect x='12.8' y='6' width='3.4' height='13' rx='1.7' fill='%234D9FFF'/%3E"
           "%3Crect x='18.7' y='9' width='3.4' height='8' rx='1.7' fill='%23C878F0'/%3E"
           "%3C/g%3E%3C/svg%3E")

FAMILY_CSS = "".join(f".f-{k.lower()}{{--fc:{v}}}" for k, v in FAMILY_COLORS.items())

# Light theme darkens every family accent in place: the raw hues sit at
# 1.3–1.9:1 on the light panels (unreadable as text). 62% toward black keeps
# every hue recognizable and puts the worst (#E8DE5A Automation) at ≥3:1 on
# the lightest and darkest light surfaces — TokensTests pins the arithmetic.
FAMILY_MIX_LIGHT = 62
FAMILY_CSS_LIGHT = (
    "".join(f':root[data-theme="light"] .f-{k.lower()}'
            f"{{--fc:color-mix(in srgb,{v} {FAMILY_MIX_LIGHT}%,black)}}"
            for k, v in FAMILY_COLORS.items())
    + "@media (prefers-color-scheme:light){"
    + "".join(f":root:not([data-theme]) .f-{k.lower()}"
              f"{{--fc:color-mix(in srgb,{v} {FAMILY_MIX_LIGHT}%,black)}}"
              for k, v in FAMILY_COLORS.items())
    + "}")

# tokens.css — the single source of truth for design tokens on EVERY surface.
# build.py writes it to /tokens.css and every page links it (index, the b//p/
# detail pages, studio.html, vitals.html), so the token set can never drift
# between stylesheets again. Fonts live here too, so shipping/dropping a weight
# is a one-line change. Edit here, not in the HTML files.
TOKENS_CSS = """/* tokens.css — GENERATED by build.py; do not hand-edit. Edit TOKENS_CSS in build.py. */
@font-face{font-family:'Schib';font-style:normal;font-weight:400 800;font-display:swap;src:url(/fonts/schibstedgrotesk-latin-var.woff2) format('woff2')}
@font-face{font-family:'PSans';font-style:normal;font-weight:400;font-display:swap;src:url(/fonts/plexsans-latin-400.woff2) format('woff2')}
@font-face{font-family:'PSans';font-style:normal;font-weight:600;font-display:swap;src:url(/fonts/plexsans-latin-600.woff2) format('woff2')}
@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:400;font-display:swap;src:url(/fonts/plexmono-latin-400.woff2) format('woff2')}
@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:600;font-display:swap;src:url(/fonts/plexmono-latin-600.woff2) format('woff2')}
:root{
  color-scheme:dark;
  --ink:#131417;--ink-2:#0E0F11;--panel:#1B1C20;--panel-2:#212329;
  --line:#26272C;--line-2:#33353B;--line-3:#45474E;
  --text:#F1F1F3;--dim:#B7B8BE;--faint:#8B8D95;--body:#C7C8CE;
  --btn:#F1F1F3;--btn-fg:#141518;--sev:#F0806A;
  --amber:#E8B44C;--amber-2:#F2CE7C;--fc:#8B7CF8;
  --success:#2FAF73;--warning:#F59E2C;--danger:#E23B4B;
  /* Primary-action colour convention (HIERARCHY F6): amber / the family --fc is
     the *browse/navigate* primary; --act (a distinct crimson) is the *commit /
     act-adjacent* primary — the Studio Fixer button, the Act family. Deliberate,
     not drift; kept distinct from every family hue (COLOR C2–C5). */
  --good:var(--success);--act:var(--danger);--up:var(--success);--down:var(--danger);--meta:#C4CBD8;
  --r-sm:8px;--r-md:12px;--r-pill:999px;--radius:8px;
  /* container + rhythm scale (LAYOUT L1/T4 — one source; @media can't take var() so breakpoints stay literal) */
  --w-page:1120px;--w-doc:960px;--w-read:760px;--gutter:24px;--lh-body:1.6;
  /* spacing scale — 4pt base (LAYOUT L2/L4/L6); map off-grid values (9,7,22…) onto it */
  --s1:4px;--s2:8px;--s3:12px;--s4:16px;--s5:24px;--s6:32px;--s7:40px;--s8:48px;--s9:64px;
  --section:64px;--section-tight:48px;
  --disp:'Schib','PSans',system-ui,-apple-system,sans-serif;
  --sans:'PSans',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
  --mono:'IBM Plex Mono',ui-monospace,'SF Mono',Menlo,Consolas,monospace;
}
:root[data-theme="light"]{__LIGHT__}
/* OS-light users without a stored choice get the light theme by default;
   an explicit data-theme (set by the toggle) always wins, both directions. */
@media (prefers-color-scheme:light){:root:not([data-theme]){__LIGHT__}}
button:active{transform:scale(.97)}
button:disabled,[aria-disabled="true"]{opacity:.5;cursor:not-allowed}
__FAMILY_CSS__
""".replace("__LIGHT__", """
  color-scheme:light;
  --ink:#F4F3EF;--ink-2:#EBEAE2;--panel:#FCFBF9;--panel-2:#EFEEE7;
  --line:#E5E4DE;--line-2:#D5D4CD;--line-3:#BEBDB4;
  --text:#191A1C;--dim:#4C4E53;--faint:#6A6C73;--body:#33353A;
  --btn:#191A1C;--btn-fg:#F5F4F0;--sev:#C4402E;--amber:#9C6E2A;--amber-2:#B8863B;--fc:#7C5CE0;
  --success:#1E9A5A;--warning:#B87A12;--danger:#C42E3E;--good:var(--success);--act:var(--danger);--up:var(--success);--down:var(--danger);--meta:#6B6E74;
""").replace("__FAMILY_CSS__", FAMILY_CSS + "\n" + FAMILY_CSS_LIGHT)

SITE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--dim);font-family:var(--sans);font-size:16px;line-height:var(--lh-body);-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.wrap{max-width:var(--w-doc);margin:0 auto;padding:0 var(--gutter)}
.mono{font-family:var(--mono)}
svg.ic{display:block;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
:focus-visible{outline:2px solid var(--fc);outline-offset:2px;border-radius:4px}
code{font-family:var(--mono);font-size:.88em;background:var(--panel-2);border:1px solid var(--line);border-radius:5px;padding:.06em .34em;color:var(--text)}

/* nav */
.nav{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--ink) 84%,transparent);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.nav-in{display:flex;align-items:center;gap:16px;height:60px}
.brand{display:flex;align-items:center;gap:8px;font-family:var(--disp);font-weight:700;letter-spacing:-.02em;font-size:16px;color:var(--text)}
.brand .mark{flex:none}
.nav-links{display:flex;gap:20px;margin-left:8px;font-size:14px;color:var(--faint)}
.nav-links a:hover{color:var(--text)}
.nav-right{margin-left:auto;display:flex;align-items:center;gap:10px}
.themetog{width:34px;height:34px;border-radius:8px;border:1px solid var(--line-2);background:var(--panel);color:var(--dim);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:border-color .15s,color .15s}
.themetog:hover{color:var(--text);border-color:var(--line-3)}
.themetog .ic{width:17px;height:17px}
.themetog .moon{display:none}.themetog .sun{display:block}
:root[data-theme="light"] .themetog .moon{display:block}:root[data-theme="light"] .themetog .sun{display:none}
@media (prefers-color-scheme:light){:root:not([data-theme]) .themetog .moon{display:block}:root:not([data-theme]) .themetog .sun{display:none}}
.nav-cta{background:var(--btn);color:var(--btn-fg);font-weight:600;font-size:13px;padding:9px 15px;border-radius:8px;font-family:var(--sans)}
.nav-cta:hover{filter:brightness(1.12)}
/* under 720px keep Playbooks + Studio reachable — same treatment as the landing page */
@media(max-width:720px){.nav-links{gap:14px}.nav-links .mh{display:none}}

/* buttons */
.btn{display:inline-flex;align-items:center;gap:8px;font-family:var(--sans);font-size:14px;font-weight:600;border-radius:8px;padding:12px 18px;cursor:pointer;border:1px solid transparent;transition:transform .1s,filter .15s,background .15s,border-color .15s;-webkit-tap-highlight-color:transparent}
.btn:active{transform:translateY(1px)}
.btn-primary{background:var(--btn);color:var(--btn-fg);border-color:var(--btn)}
.btn-primary:hover{filter:brightness(1.12)}
.btn-ghost{background:transparent;color:var(--text);border-color:var(--line-3)}
.btn-ghost:hover{border-color:var(--text)}
.btn.done{background:var(--good);color:#0c1510;border-color:var(--good)}

/* breadcrumb + eyebrow */
.crumb{display:flex;gap:8px;align-items:center;font-family:var(--mono);font-size:12px;color:var(--faint);padding:24px 0 0;flex-wrap:wrap}
.crumb a:hover{color:var(--dim)}
.crumb .sep{opacity:.5}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--faint)}

/* chips + badges */
.chip{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:12px;color:var(--dim);background:var(--panel);border:1px solid var(--line-2);border-radius:999px;padding:6px 12px}
.chip .dot{width:8px;height:8px;border-radius:2px;background:var(--fc);flex:none}
.badge{display:inline-flex;align-items:center;gap:6px;font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--btn-fg);background:var(--fc);border-radius:999px;padding:4px 10px}
.badge.soft{background:color-mix(in srgb,var(--fc) 16%,var(--panel));color:var(--fc);border:1px solid color-mix(in srgb,var(--fc) 40%,transparent)}
.out{font-family:var(--mono);font-size:12px;color:var(--dim);background:var(--panel-2);border:1px solid var(--line);border-radius:6px;padding:3px 9px}
.out::before{content:"→ ";color:var(--fc)}

/* hero */
.dhero{position:relative;padding:30px 0 34px;border-bottom:1px solid var(--line);overflow:hidden}
.dhero>*{position:relative}
.dhero .id{font-family:var(--mono);font-weight:600;font-size:15px;color:var(--fc);display:inline-flex;align-items:center;gap:8px}
.dhero .id .ic{width:19px;height:19px}
.dhero h1{font-family:var(--disp);font-size:clamp(30px,5.6vw,50px);font-weight:680;letter-spacing:-.03em;line-height:1.05;margin:12px 0 14px;color:var(--text)}
.dhero .lede{font-size:clamp(16px,2.4vw,20px);color:var(--text);max-width:60ch;line-height:1.5}
.dhero .meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
.dhero .cta{display:flex;flex-wrap:wrap;gap:11px;margin-top:24px}

/* section scaffolding */
section.blk{padding:var(--s7) 0;border-bottom:1px solid var(--line)}
.kicker{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);font-weight:600}
.h2{font-family:var(--disp);font-size:clamp(22px,3.4vw,30px);font-weight:680;letter-spacing:-.02em;margin:9px 0 6px;color:var(--text)}
.lead{color:var(--dim);max-width:64ch;font-size:16px}
.prose{color:var(--text);font-size:16px;max-width:68ch}
.prose p{margin:0 0 12px}
.prose ul{margin:0 0 12px;padding-left:20px}.prose li{margin:4px 0}
.prose strong{color:var(--text);font-weight:600}

/* method / phases */
.method{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:var(--s5)}
.phase{background:var(--panel);border:1px solid var(--line);border-top:2px solid var(--fc);border-radius:var(--radius);padding:16px 15px;position:relative}
.phase .pn{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.phase h3{font-family:var(--disp);font-size:16px;font-weight:660;margin:5px 0 8px;letter-spacing:-.01em;color:var(--text)}
.phase p{font-size:13px;color:var(--dim);line-height:1.5}
.phase .step{position:absolute;top:-11px;right:13px;width:22px;height:22px;border-radius:6px;background:var(--fc);color:var(--btn-fg);font-family:var(--mono);font-weight:600;font-size:12px;display:flex;align-items:center;justify-content:center}
@media(max-width:820px){.method{grid-template-columns:repeat(2,1fr)}}
@media(max-width:460px){.method{grid-template-columns:1fr}}

/* lenses */
.lenses{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:var(--s5)}
.lens{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:15px 16px;display:flex;gap:13px;transition:border-color .15s,transform .15s}
.lens:hover{border-color:var(--line-2);transform:translateY(-2px)}
.lens .i{font-family:var(--mono);font-weight:600;font-size:13px;color:var(--fc);flex:none;width:26px;height:26px;border-radius:7px;background:color-mix(in srgb,var(--fc) 14%,var(--panel-2));display:flex;align-items:center;justify-content:center}
.lens h4{font-family:var(--disp);font-size:15px;font-weight:660;margin-bottom:3px;letter-spacing:-.01em;color:var(--text)}
.lens p{font-size:13px;color:var(--dim);line-height:1.5}
@media(max-width:640px){.lenses{grid-template-columns:1fr}}

/* the report doc */
.report{margin-top:var(--s5);background:var(--panel);border:1px solid var(--line-2);border-radius:12px;overflow:hidden}
.report .bar{display:flex;align-items:center;gap:8px;padding:12px 16px;border-bottom:1px solid var(--line);background:var(--panel-2)}
.report .fname{font-family:var(--mono);font-size:13px;color:var(--text);font-weight:600}
.report .fname::before{content:"▸ ";color:var(--faint)}
.report .doc{padding:6px 10px 14px}
.report .row{display:flex;gap:13px;padding:12px 8px;border-radius:9px}
.report .row+.row{border-top:1px solid var(--line)}
.report .rn{font-family:var(--mono);font-size:12px;color:var(--fc);flex:none;width:22px;text-align:right;font-weight:600}
.report .rt{font-family:var(--disp);font-weight:640;font-size:14px;color:var(--text)}
.report .rd{font-size:13px;color:var(--dim);margin-top:2px;line-height:1.45}
.report .foot{padding:12px 16px;border-top:1px solid var(--line);font-family:var(--mono);font-size:12px;color:var(--faint);display:flex;gap:12px;flex-wrap:wrap;align-items:center}

/* use / commands */
.ways{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:var(--s5)}
.way{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:16px;min-width:0}
.way h4{font-family:var(--disp);font-size:14px;font-weight:660;margin-bottom:4px;color:var(--text)}
.way .num{font-family:var(--mono);font-size:11px;color:var(--fc);letter-spacing:.1em}
.way p{font-size:13px;color:var(--dim);margin:2px 0 12px;line-height:1.5}
.cmd{display:flex;align-items:center;gap:8px;font-family:var(--mono);font-size:12px;color:var(--text);background:var(--ink-2);border:1px solid var(--line);border-radius:9px;padding:10px 11px;overflow-x:auto;min-width:0}
.cmd code{flex:1;white-space:nowrap;min-width:0;background:none;border:0;padding:0;color:var(--text)}
.cmd .cp{flex:none;font-family:var(--mono);font-size:11px;color:var(--dim);background:var(--panel-2);border:1px solid var(--line-2);border-radius:6px;padding:5px 8px;cursor:pointer}
.cmd .cp:hover{color:var(--text);border-color:var(--line-3)}
.cmd .cp.done{color:var(--good);border-color:var(--good)}
@media(max-width:760px){.ways{grid-template-columns:1fr}}

/* full brief + rules */
.full{margin-top:20px;border:1px solid var(--line);border-radius:var(--radius);background:var(--panel);overflow:hidden}
.full summary{cursor:pointer;list-style:none;padding:14px 16px;font-family:var(--mono);font-size:13px;color:var(--dim);display:flex;align-items:center;gap:8px}
.full summary::-webkit-details-marker{display:none}
.full summary .chev{transition:transform .2s}.full[open] summary .chev{transform:rotate(90deg)}
.full pre{font-family:var(--mono);font-size:12px;line-height:1.6;color:var(--text);background:var(--ink-2);border-top:1px solid var(--line);padding:16px;overflow-x:auto;white-space:pre-wrap;word-break:break-word}
.rules{margin-top:var(--s5);background:color-mix(in srgb,var(--fc) 7%,var(--panel));border:1px solid var(--line);border-left:2px solid var(--fc);border-radius:var(--radius);padding:16px 18px}
.rules h4{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--fc);margin-bottom:9px}
.rules ul{list-style:none;display:grid;gap:8px}
.rules li{font-size:14px;color:var(--text);padding-left:20px;position:relative}
.rules li::before{content:"→";position:absolute;left:0;color:var(--fc)}

/* related + cards */
.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:20px}
.pcard{display:block;background:var(--panel);border:1px solid var(--line);border-left:2px solid var(--fc);border-radius:var(--radius);padding:15px 16px;transition:transform .15s,border-color .15s}
.pcard:hover{transform:translateY(-2px);border-color:var(--line-2)}
.pcard .pid{font-family:var(--mono);font-size:12px;color:var(--fc)}
.pcard h4{font-family:var(--disp);font-size:16px;font-weight:660;margin:3px 0 5px;letter-spacing:-.01em;color:var(--text)}
.pcard p{font-size:13px;color:var(--dim);line-height:1.45}
@media(max-width:640px){.cards{grid-template-columns:1fr}}
.pblinks{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.pblink{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:12px;color:var(--dim);background:var(--panel);border:1px dashed var(--line-2);border-radius:999px;padding:8px 13px}
.pblink:hover{color:var(--text);border-color:var(--fc)}
.pblink .len{color:var(--faint)}

/* playbook sequence map */
.seq{display:flex;flex-direction:column;gap:0;margin-top:var(--s5)}
.seqstep{display:flex;gap:14px;align-items:stretch}
.seqstep .rail{display:flex;flex-direction:column;align-items:center;flex:none;width:30px}
.seqstep .node{width:30px;height:30px;border-radius:9px;background:var(--panel);border:2px solid var(--fc);color:var(--fc);font-family:var(--mono);font-weight:600;font-size:12px;display:flex;align-items:center;justify-content:center}
.seqstep .wire{flex:1;width:2px;background:var(--line-2);min-height:14px;margin:2px 0}
.seqstep:last-child .wire{display:none}
.seqcard{flex:1;background:var(--panel);border:1px solid var(--line);border-left:2px solid var(--fc);border-radius:11px;padding:13px 15px;margin-bottom:14px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;transition:transform .15s,border-color .15s}
.seqcard:hover{transform:translateX(3px);border-color:var(--line-2)}
.seqcard .sid{font-family:var(--mono);font-size:12px;color:var(--fc);flex:none}
.seqcard .st{font-family:var(--disp);font-weight:640;font-size:15px;flex:1;min-width:120px;letter-spacing:-.01em;color:var(--text)}
.seqcard .sq{font-size:12px;color:var(--faint);font-family:var(--mono)}

/* partner / monetization */
.partner{margin-top:24px;background:var(--panel);border:1px solid var(--line-2);border-radius:12px;padding:20px 22px}
.partner .co{display:flex;align-items:center;gap:12px;font-family:var(--mono);font-size:14px;color:var(--text);flex-wrap:wrap}
.partner .co .x{color:var(--faint)}
.partner .logo{width:34px;height:34px;border-radius:9px;background:var(--fc);color:var(--btn-fg);font-weight:800;display:flex;align-items:center;justify-content:center;font-family:var(--disp)}
.partner p{font-size:14px;color:var(--dim);margin:12px 0 14px;max-width:64ch;line-height:1.5}
.note{margin-top:18px;font-family:var(--mono);font-size:12px;color:var(--faint);background:var(--panel);border:1px dashed var(--line-2);border-radius:10px;padding:11px 14px}

/* per-step copy on playbook sequence maps */
.seqstep .stepcopy{flex:none;align-self:center;margin-bottom:14px;font-family:var(--mono);font-size:11px;color:var(--dim);background:var(--panel-2);border:1px solid var(--line-2);border-radius:6px;padding:6px 9px;cursor:pointer;text-decoration:none}
.seqstep .stepcopy:hover{color:var(--text);border-color:var(--line-3)}
.seqstep .stepcopy.done{color:var(--good);border-color:var(--good)}

/* post-copy hint (gp-detail.js) — same shape as the landing page's toast */
.gp-hint{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);z-index:40;display:flex;align-items:center;gap:12px;max-width:min(92vw,470px);background:var(--panel-2);border:1px solid var(--line-2);border-radius:10px;padding:11px 14px;font-size:13px;line-height:1.45;color:var(--text);box-shadow:0 12px 40px -14px rgba(0,0,0,.55)}
.gp-hint[hidden]{display:none}
.gp-hint code{font-family:var(--mono);color:var(--fc)}
.gp-hint b{color:var(--text)}
.gp-hint .markrun{flex:none;background:var(--good);color:#0C1510;border:0;border-radius:6px;font-family:var(--sans);font-size:12px;font-weight:600;padding:4px 9px;cursor:pointer;white-space:nowrap}
.gp-hint .markrun:disabled{opacity:.6;cursor:default}
.gp-hint .x{flex:none;background:none;border:0;color:var(--faint);cursor:pointer;font-size:16px;line-height:1;padding:2px}
.gp-hint .x:hover{color:var(--text)}

/* footer */
footer.foot{padding:var(--s7) 0 var(--s9);color:var(--dim)}
.foot .cta-band{background:var(--panel);border:1px solid var(--line-2);border-radius:16px;padding:28px 26px;text-align:center;margin-bottom:34px}
.foot .cta-band h3{font-family:var(--disp);font-size:clamp(20px,3vw,26px);font-weight:700;letter-spacing:-.02em;color:var(--text);margin-bottom:8px}
.foot .cta-band p{font-size:15px;max-width:52ch;margin:0 auto 18px}
.foot .links{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:12px}
.foot .links a:hover{color:var(--text)}
.foot .fine{margin-top:16px;font-family:var(--mono);font-size:12px;color:var(--faint)}

@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}html{scroll-behavior:auto}}
"""

NAV_HTML = ('<header class="nav"><div class="nav-in wrap">'
            f'<a class="brand" href="/">{BRAND_MARK}Goal Prompts</a>'
            '<nav class="nav-links">'
            '<a href="/#how" class="mh">How it works</a>'
            '<a href="/#catalog" class="mh">Catalog</a>'
            '<a href="/#playbooks">Playbooks</a>'
            '<a href="/studio">Studio</a></nav>'
            '<div class="nav-right">'
            '<button class="themetog" id="themetog" type="button" aria-label="Toggle light or dark theme"><svg class="ic sun"><use href="#i-sun"></use></svg><svg class="ic moon"><use href="#i-moon"></use></svg></button>'
            '<a class="nav-cta" href="/#start">Get started</a></div>'
            '</div></header>')



SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<symbol id="i-product" viewBox="0 0 24 24"><path d="M12 3 L13.7 10.3 L21 12 L13.7 13.7 L12 21 L10.3 13.7 L3 12 L10.3 10.3 Z"/></symbol>
<symbol id="i-quality" viewBox="0 0 24 24"><ellipse cx="12" cy="13.5" rx="4" ry="5.3"/><circle cx="12" cy="7.5" r="2.1"/><path d="M8 12 L4.2 10 M8 14.5 L4 14.5 M8.2 17.5 L4.8 19.6 M16 12 L19.8 10 M16 14.5 L20 14.5 M15.8 17.5 L19.2 19.6 M10.6 6.2 L9.4 3.8 M13.4 6.2 L14.6 3.8"/></symbol>
<symbol id="i-speed" viewBox="0 0 24 24"><path d="M4 17 A8 8 0 0 1 20 17"/><path d="M12 17 L16.5 11.5"/><circle cx="12" cy="17" r="1.3"/></symbol>
<symbol id="i-trust" viewBox="0 0 24 24"><path d="M12 3 L20 6 V11 C20 16 16.5 19.5 12 21 C7.5 19.5 4 16 4 11 V6 Z"/><path d="M8.8 12 L11 14.2 L15.4 9.4"/></symbol>
<symbol id="i-growth" viewBox="0 0 24 24"><path d="M4 18 L10 12 L13.5 15 L20 7"/><path d="M15 7 L20 7 L20 12"/></symbol>
<symbol id="i-clarity" viewBox="0 0 24 24"><path d="M2.5 12 C5 7.2 8.8 5.2 12 5.2 C15.2 5.2 19 7.2 21.5 12 C19 16.8 15.2 18.8 12 18.8 C8.8 18.8 5 16.8 2.5 12 Z"/><circle cx="12" cy="12" r="2.7"/></symbol>
<symbol id="i-design" viewBox="0 0 24 24"><path d="M12 4 L7.5 20 M12 4 L16.5 20 M9.4 13.4 L14.6 13.4"/><circle cx="12" cy="4.4" r="1.5"/></symbol>
<symbol id="i-data" viewBox="0 0 24 24"><ellipse cx="12" cy="6" rx="7" ry="2.9"/><path d="M5 6 V18 C5 19.7 8.1 21 12 21 C15.9 21 19 19.7 19 18 V6"/><path d="M5 12 C5 13.7 8.1 15 12 15 C15.9 15 19 13.7 19 12"/></symbol>
<symbol id="i-ops" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3.2"/><path d="M12 2.6 V5.2 M12 18.8 V21.4 M2.6 12 H5.2 M18.8 12 H21.4 M5.4 5.4 L7.2 7.2 M16.8 16.8 L18.6 18.6 M18.6 5.4 L16.8 7.2 M7.2 16.8 L5.4 18.6"/></symbol>
<symbol id="i-team" viewBox="0 0 24 24"><circle cx="9" cy="9" r="2.5"/><circle cx="16" cy="10" r="2"/><path d="M3.5 19 C3.5 15.4 5.8 13.8 9 13.8 C11 13.8 12.6 14.5 13.4 16 M13.6 19 C13.9 16 15.2 15 17 15 C19.2 15 20.5 16.6 20.5 19"/></symbol>
<symbol id="i-subtract" viewBox="0 0 24 24"><circle cx="6.5" cy="7" r="2"/><circle cx="6.5" cy="17" r="2"/><path d="M8.2 8.2 L20 18 M8.2 15.8 L20 6 M8.4 12 L12.5 9"/></symbol>
<symbol id="i-meta" viewBox="0 0 24 24"><path d="M12 4 L21 9 L12 14 L3 9 Z"/><path d="M3.5 13 L12 17.6 L20.5 13"/></symbol>
<symbol id="i-act" viewBox="0 0 24 24"><path d="M13 3 L5.5 13 H11 L10 21 L18.5 10.5 H12.5 Z"/></symbol>
<symbol id="i-agent" viewBox="0 0 24 24"><path d="M12 3 L20 7.5 V16.5 L12 21 L4 16.5 V7.5 Z"/><circle cx="12" cy="12" r="2.5"/><path d="M12 5.2 V7.4"/></symbol>
<symbol id="i-automation" viewBox="0 0 24 24"><path d="M6.5 9.5 A6 6 0 0 1 18 8.2"/><path d="M17.5 14.5 A6 6 0 0 1 6 15.8"/><path d="M18.4 4.6 L18.4 8.6 L14.4 8.4 M5.6 19.4 L5.6 15.4 L9.6 15.6"/></symbol>
<symbol id="i-aiux" viewBox="0 0 24 24"><path d="M12 20 C6.2 15.6 4 12.2 4 9 C4 6.5 6 4.9 8.3 4.9 C9.9 4.9 11.3 5.9 12 7.1 C12.7 5.9 14.1 4.9 15.7 4.9 C18 4.9 20 6.5 20 9 C20 12.2 17.8 15.6 12 20 Z"/></symbol>
<symbol id="i-venture" viewBox="0 0 24 24"><path d="M12 2.6 C15.2 5 16.8 9.2 16.8 13 L14 16 H10 L7.2 13 C7.2 9.2 8.8 5 12 2.6 Z"/><circle cx="12" cy="10" r="1.7"/><path d="M10 16 L7.8 20.4 M14 16 L16.2 20.4 M12 16.4 V20.6"/></symbol>
<symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2.5V5 M12 19V21.5 M2.5 12H5 M19 12H21.5 M5.2 5.2l1.8 1.8 M17 17l1.8 1.8 M18.8 5.2 17 7 M7 17l-1.8 1.8"/></symbol>
<symbol id="i-moon" viewBox="0 0 24 24"><path d="M20 14.5 A8 8 0 0 1 9.5 4 A7 7 0 1 0 20 14.5 Z"/></symbol>
</defs></svg>'''
THEME_INLINE = '<script>try{var _t=localStorage.getItem("gp-theme");if(_t==="light"||_t==="dark")document.documentElement.setAttribute("data-theme",_t);}catch(e){}</script>\n'
THEME_JS = '''(function(){var KEY="gp-theme",root=document.documentElement,btn=document.getElementById("themetog");function isLight(){var t=root.getAttribute("data-theme");if(t==="light"||t==="dark")return t==="light";try{return window.matchMedia("(prefers-color-scheme: light)").matches;}catch(e){return false;}}function paint(){var m=document.querySelector('meta[name=\"theme-color\"]');if(m)m.setAttribute("content",isLight()?"#F4F3EF":"#131417");}paint();if(btn)btn.onclick=function(){var next=isLight()?"dark":"light";root.setAttribute("data-theme",next);try{localStorage.setItem(KEY,next);}catch(e){}paint();};})();'''


def page(title, desc, canon, body_html, og_image, og_type="website",
         body_class="") -> str:
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
            '<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f"<title>{esc(title)}</title>\n"
            f'<meta name="description" content="{attr(desc)}">\n'
            f'<meta property="og:title" content="{attr(title)}">\n'
            f'<meta property="og:description" content="{attr(desc)}">\n'
            f'<meta property="og:image" content="{og_image}">\n'
            f'<meta property="og:url" content="{canon}">\n'
            f'<meta property="og:type" content="{og_type}">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:image" content="{og_image}">\n'
            '<meta name="theme-color" content="#131417">\n'
            '<link rel="manifest" href="/manifest.json">\n'
            f'<link rel="canonical" href="{canon}">\n'
            f'<link rel="icon" href="{FAVICON}">\n'
            '<link rel="preload" href="/fonts/schibstedgrotesk-latin-var.woff2" as="font" type="font/woff2" crossorigin>\n'
            '<link rel="preload" href="/fonts/plexsans-latin-400.woff2" as="font" type="font/woff2" crossorigin>\n'
            '<link rel="preload" href="/fonts/plexmono-latin-400.woff2" as="font" type="font/woff2" crossorigin>\n'
            '<link rel="stylesheet" href="/tokens.css">\n'
            f"<style>{SITE_CSS}</style>\n" + THEME_INLINE + "</head>\n"
            f'<body class="{body_class}">\n' + SPRITE + f'\n{NAV_HTML}\n{body_html}\n'
            '<script src="/js/gp-detail.js"></script>\n'
            f"<script>{THEME_JS}</script>\n</body>\n</html>\n")


def foot(head, sub, buttons_html) -> str:
    return ('<footer class="foot"><div class="wrap">'
            f'<div class="cta-band"><h3>{esc(head)}</h3><p>{esc(sub)}</p>'
            f'<div class="row">{buttons_html}</div></div>'
            '<div class="links">'
            '<a href="/">Home</a><a href="/#catalog">Catalog</a>'
            '<a href="/#playbooks">Playbooks</a><a href="/studio">Report Studio</a>'
            '<a href="/examples/">Sample reports</a>'
            '<a href="https://github.com/GhostlyGawd/goal-prompts">GitHub</a></div>'
            '<p class="fine">Free &amp; open source · MIT licensed · every brief under 4,000 characters · '
            'works with Claude Code, Cursor, Copilot &amp; any coding agent</p>'
            '</div></footer>')


def cmd_html(text: str) -> str:
    import hashlib
    cid = "c" + hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
    return (f'<div class="cmd"><code>{esc(text)}</code>'
            f'<button class="cp" data-copy="#{cid}">copy</button>'
            f'<textarea id="{cid}" hidden>{esc(text)}</textarea></div>')


def brief_detail(p, siblings, in_playbooks, related=()) -> str:
    parts = brief_parts(p["body"])
    fc = "f-" + p["family"].lower()
    slug = p["slug"]
    lens_word = "lens" if len(parts["lenses"]) == 1 else "lenses"
    copy_attrs = (f'data-copy="#rawbody" data-ctx="1" data-brief="{p["id"]}" '
                  f'data-output="{attr(p["output"])}"')

    # hero
    meta = [f'<span class="out">{esc(p["output"])}</span>',
            f'<span class="chip">{len(parts["phases"])} phases</span>']
    if parts["lenses"]:
        meta.append(f'<span class="chip">{len(parts["lenses"])} audit {lens_word}</span>')
    meta.append(f'<span class="chip">~{p["chars"]/1000:.1f}k chars</span>')

    cta = [f'<button class="btn btn-primary" {copy_attrs}>Copy this prompt</button>',
           f'<a class="btn btn-ghost" href="#use">How to run it</a>']
    if p.get("example"):
        ex = p["example"] if p["example"].startswith("/") else p["example"]
        cta.append(f'<a class="btn btn-ghost" href="{ex}">See a real report ↗</a>')

    hero = (f'<section class="dhero"><div class="wrap">'
            f'<div class="crumb"><a href="/">Home</a><span class="sep">/</span>'
            f'<a href="/#catalog">Catalog</a><span class="sep">/</span>'
            f'<span>{esc(p["family"])}</span></div>'
            f'<div style="margin-top:14px"><span class="chip"><span class="dot"></span>'
            f'{esc(p["family"])} — <span class="mono" style="color:var(--faint)">{esc(p["question"])}</span></span></div>'
            f'<div class="id" style="margin-top:14px">Brief {esc(p["id"])}</div>'
            f'<h1>{esc(p["title"])}</h1>'
            f'<p class="lede">{esc(p["tagline"])}</p>'
            f'<div class="meta">{"".join(meta)}</div>'
            f'<div class="cta">{"".join(cta)}</div>'
            f'</div></section>')

    # what it does
    whatis = (f'<section class="blk"><div class="wrap">'
              f'<div class="kicker">What it does</div>'
              f'<div class="prose" style="margin-top:12px">{md_block(parts["intro"])}</div>'
              f'</div></section>')

    # method
    pcards = []
    for ph in parts["phases"]:
        pcards.append(f'<div class="phase"><span class="step">{ph["n"]}</span>'
                      f'<div class="pn">Phase {ph["n"]}</div>'
                      f'<h3>{esc(ph["name"])}</h3><p>{esc(ph["gist"])}</p></div>')
    method = (f'<section class="blk"><div class="wrap">'
              f'<div class="kicker">How it works</div>'
              f'<h2 class="h2">The four-phase method</h2>'
              f'<p class="lead">Every brief follows the same arc, so results are consistent '
              f'and repeatable — no matter which audit you run.</p>'
              f'<div class="method">{"".join(pcards)}</div>'
              f'</div></section>')

    # lenses (or prose phase 2)
    if parts["lenses"]:
        lcards = []
        for i, (name, d) in enumerate(parts["lenses"], 1):
            lcards.append(f'<div class="lens"><div class="i">{i}</div><div>'
                          f'<h4>{esc(name)}</h4><p>{md_inline(d)}</p></div></div>')
        lenses = (f'<section class="blk"><div class="wrap">'
                  f'<div class="kicker">The audit</div>'
                  f'<h2 class="h2">{len(parts["lenses"])} {lens_word} it looks through</h2>'
                  f'<p class="lead">Phase 2 sweeps the codebase through every one of these, '
                  f'citing file and line for each finding.</p>'
                  f'<div class="lenses">{"".join(lcards)}</div></div></section>')
    else:
        pr = next((ph.get("prose", "") for ph in parts["phases"] if ph["n"] == 2), "")
        lenses = (f'<section class="blk"><div class="wrap">'
                  f'<div class="kicker">The audit</div>'
                  f'<h2 class="h2">How the pass runs</h2>'
                  f'<div class="prose" style="margin-top:14px">{pr}</div></div></section>')

    # the report
    rrows = "".join(
        f'<div class="row"><div class="rn">{i}</div><div>'
        f'<div class="rt">{esc(name)}</div><div class="rd">{md_inline(d)}</div></div></div>'
        for i, (name, d) in enumerate(parts["report"], 1))
    rfoot = ['One file. Evidence-backed. It ends by asking before touching anything.']
    if p.get("example"):
        rfoot.append(f'<a href="{p["example"]}" style="color:var(--fc)">see a real {esc(p["output"])} ↗</a>')
    report = (f'<section class="blk"><div class="wrap">'
              f'<div class="kicker">The deliverable</div>'
              f'<h2 class="h2">What lands in your repo</h2>'
              f'<p class="lead">One structured report at the repo root — or in <code>reports/</code>, '
              f'if you keep one — the same shape every time, '
              f'ready for the Report Studio or a teammate to act on.</p>'
              f'<div class="report"><div class="bar"><div class="dots"><i></i><i></i><i></i></div>'
              f'<span class="fname">{esc(p["output"])}</span></div>'
              f'<div class="doc">{rrows}</div>'
              f'<div class="foot">{" · ".join(rfoot)}</div></div></div></section>')

    # use it
    ways = (f'<section class="blk" id="use"><div class="wrap">'
            f'<div class="kicker">Get started</div>'
            f'<h2 class="h2">Three ways to run this brief</h2>'
            f'<div class="ways">'
            f'<div class="way"><div class="num">01 · COPY</div><h4>Paste it in</h4>'
            f'<p>Copy the prompt and paste it into your agent inside the repo you want audited.</p>'
            f'<button class="btn btn-primary" style="width:100%;justify-content:center" {copy_attrs}>Copy this prompt</button></div>'
            f'<div class="way"><div class="num">02 · INSTALL</div><h4>As a slash command</h4>'
            f'<p>Install the <b>goal</b> plugin once, then just type <code>/goal:{esc(slug)}</code> '
            f'— or use the curl installer for the same brief as <code>/goal-{esc(slug)}</code>.</p>'
            f'{cmd_html("/plugin marketplace add GhostlyGawd/goal-prompts")}</div>'
            f'<div class="way"><div class="num">03 · AGENT</div><h4>From an agent (MCP)</h4>'
            f'<p>Let an agent fetch it mid-conversation, or pull the raw brief by URL.</p>'
            f'{cmd_html(BASE + "/raw/" + p["id"] + ".md")}</div>'
            f'</div></div></section>')

    # full brief + rules
    rules = ""
    if parts["rules"]:
        rules = ('<div class="rules"><h4>House rules for this brief</h4><ul>'
                 + "".join(f"<li>{md_inline(r)}</li>" for r in parts["rules"])
                 + "</ul></div>")
    full = (f'<section class="blk"><div class="wrap">'
            f'<div class="kicker">Transparency</div>'
            f'<h2 class="h2">The exact prompt</h2>'
            f'<p class="lead">Nothing hidden — this is the whole brief, verbatim. '
            f'Read it in a minute, edit it, or copy it as-is.</p>'
            f'<details class="full"><summary><span class="chev">▸</span> Read the full brief '
            f'({p["chars"]:,} characters)</summary>'
            f'<pre id="rawbody">{esc(p["body"])}</pre></details>'
            f'{rules}</div></section>')

    # related
    def _pcard(s):
        return (f'<a class="pcard {"f-"+s["family"].lower()}" href="/b/{s["id"]}">'
                f'<div class="pid">{esc(s["id"])} · {esc(s["family"])}</div>'
                f'<h4>{esc(s["title"])}</h4><p>{esc(s["tagline"])}</p></a>')
    rel = ""
    rel_cards = "".join(_pcard(r) for r in related)
    if p["id"] == "47":
        # the Fixer's natural neighbor isn't a brief — it's the Studio, where
        # checked findings become this brief's targeted form
        rel_cards += ('<a class="pcard" href="/studio">'
                      '<div class="pid">Studio · Act</div>'
                      '<h4>Report Studio</h4>'
                      '<p>Drop the reports your audits produced — findings become a '
                      'checklist, and checked findings become a targeted Fixer run.</p></a>')
    sib_cards = "".join(_pcard(s) for s in siblings[:4])
    pb_links = "".join(
        f'<a class="pblink" href="/p/{pb["key"]}">{esc(pb["name"])} '
        f'<span class="len">{len(pb["ids"])}</span></a>' for pb in in_playbooks)
    if rel_cards or sib_cards or pb_links:
        rel = '<section class="blk"><div class="wrap"><div class="kicker">Keep exploring</div>'
        if rel_cards:
            rel += (f'<h2 class="h2">Pairs well with</h2>'
                    f'<p class="lead">Curated neighbors — briefs that answer the adjacent '
                    f'question, worth running in the same session.</p>'
                    f'<div class="cards">{rel_cards}</div>')
        if sib_cards:
            gap = ' style="margin-top:30px"' if rel_cards else ""
            rel += (f'<h2 class="h2"{gap}>'
                    f'More {esc(p["family"])} briefs</h2>'
                    f'<div class="cards">{sib_cards}</div>')
        if pb_links:
            rel += ('<p class="lead" style="margin-top:26px">Runs inside these playbooks — '
                    'curated sequences you can launch with one paste:</p>'
                    f'<div class="pblinks">{pb_links}</div>')
        rel += '</div></section>'

    ftr = foot("Point your agent at your repo",
               "Browse the full catalog of audits, or install every brief as a "
               "slash command in one line.",
               '<a class="btn btn-primary" href="/#catalog">Browse the catalog</a>'
               '<a class="btn btn-ghost" href="/#start">Install everything</a>')

    body = hero + whatis + lenses + report + method + ways + full + rel + ftr
    title = f'{p["id"]} · {p["title"]} — Goal Prompts'
    return page(title, p["tagline"], f"{BASE}/b/{p['id']}", body,
                f"{BASE}/og/{p['id']}.png", "article", fc)


def playbook_detail(pb, by_id) -> str:
    accent = pb.get("accent")
    fam_of_first = by_id[pb["ids"][0]]["family"]
    body_class = "" if accent else "f-" + fam_of_first.lower()
    style = f'style="--fc:{accent}"' if accent else ""
    n = len(pb["ids"])
    kind = pb.get("type", "standard")
    partner = pb.get("partner")

    badge = ""
    if pb.get("badge"):
        badge = f'<span class="badge">{esc(pb["badge"])}</span> '
    win = f'<span class="chip">{esc(pb["window"])}</span>' if pb.get("window") else ""

    hero = (f'<section class="dhero" {style}><div class="wrap">'
            f'<div class="crumb"><a href="/">Home</a><span class="sep">/</span>'
            f'<a href="/#playbooks">Playbooks</a><span class="sep">/</span>'
            f'<span>{esc(pb["name"])}</span></div>'
            f'<div style="margin-top:14px">{badge}'
            f'<span class="chip">Playbook · {n} brief{"s" if n>1 else ""}</span> {win}</div>'
            f'<h1 style="margin-top:14px">{esc(pb["name"])}</h1>'
            f'<p class="lede">{esc(pb.get("tagline") or pb["desc"])}</p>'
            f'<div class="cta">'
            f'<button class="btn btn-primary" data-copy="#rawcond">Copy the conductor</button>'
            f'<a class="btn btn-ghost" href="#seq">See the sequence</a></div>'
            f'</div></section>')

    # preview / partner note
    banner = ""
    if pb.get("preview"):
        banner = ('<div class="wrap"><div class="note">Preview — this is a worked '
                  'template showing how a co-branded partner playbook appears. '
                  'The sequence is real and runnable; the partner is a placeholder.</div></div>')

    # narrative
    why = (f'<section class="blk"><div class="wrap">'
           f'<div class="kicker">Why this sequence</div>'
           f'<div class="prose" style="margin-top:12px"><p>{esc(pb["desc"])}</p></div>'
           f'</div></section>')

    # sequence map
    steps = []
    for i, pid in enumerate(pb["ids"], 1):
        b = by_id[pid]
        fc = "f-" + b["family"].lower()
        steps.append(
            f'<div class="seqstep"><div class="rail"><div class="node">{i}</div>'
            f'<div class="wire"></div></div>'
            f'<a class="seqcard {fc}" href="/b/{pid}">'
            f'<span class="sid">{esc(pid)}</span>'
            f'<span class="st">{esc(b["title"])}</span>'
            f'<span class="out">{esc(b["output"])}</span>'
            f'<span class="sq">{esc(b["family"])}</span></a>'
            f'<button class="stepcopy" type="button" data-fetch="/raw/{pid}.md" '
            f'data-raw="{BASE}/raw/{pid}.md" data-brief="{pid}" '
            f'data-output="{attr(b["output"])}" '
            f'aria-label="Copy brief {pid} · {attr(b["title"])}">copy</button></div>')
    outputs = ", ".join(by_id[i]["output"] for i in pb["ids"])
    seq = (f'<section class="blk" id="seq" {style}><div class="wrap">'
           f'<div class="kicker">The map</div>'
           f'<h2 class="h2">Run it in order</h2>'
           f'<p class="lead">The conductor fetches each brief in turn and writes its report before '
           f'moving on — later briefs can build on earlier findings. Or copy any single '
           f'stage to run it alone.</p>'
           f'<div class="seq">{"".join(steps)}</div>'
           f'<div class="report" style="margin-top:26px"><div class="bar">'
           f'<div class="dots"><i></i><i></i><i></i></div>'
           f'<span class="fname mono" style="color:var(--dim)">what you\'ll have at the end</span></div>'
           f'<div class="doc" style="padding:16px"><div class="prose">'
           f'<p><strong>{n} report{"s" if n>1 else ""}</strong> at the repo root (or in <code>reports/</code>): '
           f'<span class="mono" style="font-size:13px;color:var(--dim)">{esc(outputs)}</span>. '
           f'Feed them to <a href="/studio" style="color:var(--fc)">Report Studio</a> to turn findings '
           f'into commits, or run <a href="/b/28" style="color:var(--fc)">28 · Roadmap Synthesis</a> '
           f'to merge them into one plan.</p></div></div></div>'
           f'</div></section>')

    # how to run
    run = (f'<section class="blk" {style}><div class="wrap">'
           f'<div class="kicker">Get started</div>'
           f'<h2 class="h2">One paste runs the whole thing</h2>'
           f'<p class="lead">Copy the conductor into your agent inside the repo you want audited. '
           f'It runs each brief in sequence, honoring every brief\'s ask-first rule.</p>'
           f'<div class="cta" style="margin-top:18px">'
           f'<button class="btn btn-primary" data-copy="#rawcond">Copy the conductor</button>'
           f'<a class="btn btn-ghost" href="{BASE}/raw/playbook-{pb["key"]}.md">View raw ↗</a></div>'
           f'</div></section>')

    # partner block
    pblock = ""
    if partner:
        logo = esc(partner["name"][:1].upper())
        pblock = (f'<section class="blk" {style}><div class="wrap">'
                  f'<div class="kicker">Partner playbook</div>'
                  f'<div class="partner"><div class="co">'
                  f'<span class="logo">{logo}</span>'
                  f'<strong>{esc(partner["name"])}</strong> <span class="x">×</span> '
                  f'<span class="brand" style="font-size:15px">Goal Prompts</span></div>'
                  f'<p>{esc(partner["blurb"])}</p>'
                  f'<a class="btn btn-primary" href="https://github.com/GhostlyGawd/goal-prompts/discussions/new?category=ideas&title=Partner%20playbook">'
                  f'{esc(partner.get("cta", "Partner with us"))}</a>'
                  f'</div></div></section>')

    # briefs as cards
    cards = "".join(
        f'<a class="pcard {"f-"+by_id[i]["family"].lower()}" href="/b/{i}">'
        f'<div class="pid">{esc(i)} · {esc(by_id[i]["family"])}</div>'
        f'<h4>{esc(by_id[i]["title"])}</h4>'
        f'<p>{esc(by_id[i]["tagline"])}</p></a>' for i in pb["ids"])
    briefs = (f'<section class="blk"><div class="wrap">'
              f'<div class="kicker">In this playbook</div>'
              f'<h2 class="h2">The {n} brief{"s" if n>1 else ""}</h2>'
              f'<div class="cards">{cards}</div></div></section>')

    rawcond = f'<textarea id="rawcond" hidden>{esc(pb["conductor"])}</textarea>'

    ftr = foot("Curated so you don't have to choose",
               "Every playbook is a battle-tested sequence. Browse them all, "
               "or explore the full catalog of audits.",
               '<a class="btn btn-primary" href="/#playbooks">All playbooks</a>'
               '<a class="btn btn-ghost" href="/#catalog">Full catalog</a>')

    body = hero + banner + why + seq + run + pblock + briefs + rawcond + ftr
    title = f'{pb["name"]} — Goal Prompts playbook'
    return page(title, pb.get("tagline") or pb["desc"], f"{BASE}/p/{pb['key']}",
                body, f"{BASE}/og.png", "website", body_class)


def command_md(p: dict) -> str:
    """One brief as a Claude Code command file — the same content ships in the
    tar/zip archives (curl installer) and the plugin's commands/ directory."""
    return f'---\ndescription: "{p["tagline"]}"\n---\n\n{p["body"]}\n'


def write_plugin(prompts: list) -> None:
    """The Claude Code plugin (plugin/), listed by .claude-plugin/marketplace.json.

    /plugin marketplace add GhostlyGawd/goal-prompts, install "goal", and every
    brief is a real namespaced /goal:<slug> command. The whole directory is a
    build output: commands/ regenerates from the briefs and plugin.json's
    version tracks package.json, so neither can drift (tests/test_build.py
    PluginTests pins both; CI diffs the committed copy)."""
    version = json.loads(
        (ROOT / "package.json").read_text(encoding="utf-8"))["version"]
    shutil.rmtree(ROOT / "plugin", ignore_errors=True)
    (ROOT / "plugin" / ".claude-plugin").mkdir(parents=True)
    (ROOT / "plugin" / "commands").mkdir()
    for p in prompts:
        (ROOT / "plugin" / "commands" / f'{p["slug"]}.md').write_text(
            command_md(p), encoding="utf-8")
    manifest = {
        "name": "goal",
        "displayName": "Goal Prompts",
        "version": version,
        "description": "The goal-prompts audit catalog as native /goal:<slug> "
                       "commands — each brief points your agent at the repo "
                       "and writes one evidence-backed report.",
        "author": {"name": "GhostlyGawd"},
        "homepage": BASE,
        "repository": "https://github.com/GhostlyGawd/goal-prompts",
        "license": "MIT",
        "keywords": ["audit", "code-audit", "claude-code", "prompts"],
    }
    (ROOT / "plugin" / ".claude-plugin" / "plugin.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")


def write_archives(prompts: list) -> None:
    # Entries live under goal/ (one rm -rf uninstalls) but carry the goal-
    # prefix in the filename, because a commands subdirectory does not
    # namespace: the installed commands really are /goal-<slug>. The plugin
    # (write_plugin) is where the /goal:<slug> namespace comes from.
    version = json.loads(
        (ROOT / "package.json").read_text(encoding="utf-8"))["version"]
    entries = [("goal/.version", version.encode("utf-8"))]
    for p in prompts:
        content = command_md(p).encode("utf-8")
        entries.append((f'goal/goal-{p["slug"]}.md', content))
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.GNU_FORMAT) as tf:
        for name, data in entries:
            ti = tarfile.TarInfo(name)
            ti.size, ti.mtime, ti.mode = len(data), 0, 0o644
            tf.addfile(ti, io.BytesIO(data))
    with open(ROOT / "commands.tar.gz", "wb") as f:
        with gzip.GzipFile(fileobj=f, mode="wb", mtime=0) as gz:
            gz.write(raw.getvalue())
    with zipfile.ZipFile(ROOT / "commands.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in entries:
            zi = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            zi.external_attr = 0o644 << 16
            zf.writestr(zi, data)
    import hashlib
    lines = []
    for fname in ("commands.tar.gz", "commands.zip"):
        digest = hashlib.sha256((ROOT / fname).read_bytes()).hexdigest()
        lines.append(f"{digest}  {fname}")
    (ROOT / "checksums.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    files = sorted((ROOT / "prompts").rglob("*.md"))
    if not files:
        fail("no prompt files found under prompts/")
    prompts = [parse(f) for f in files]
    prompts.sort(key=sort_key)
    by_id = {p["id"]: p for p in prompts}

    ids = [p["id"] for p in prompts]
    if len(ids) != len(set(ids)):
        fail("duplicate prompt ids")
    if len({p["slug"] for p in prompts}) != len(prompts):
        fail("duplicate prompt slugs")
    cross = lint_catalog(prompts)
    if cross:
        fail("; ".join(cross))

    playbooks = json.loads((ROOT / "playbooks.json").read_text(encoding="utf-8"))
    for pb in playbooks:
        missing = [i for i in pb["ids"] if i not in by_id]
        if missing:
            fail(f"playbook '{pb['key']}' references unknown ids {missing}")
        pb["conductor"] = conductor(pb, by_id)

    # ---- lint ----
    violations = 0
    width = max(len(p["title"]) for p in prompts)
    for p in prompts:
        v = lint(p)
        mark = "  LINT: " + "; ".join(v) if v else ""
        violations += len(v)
        print(f'{p["id"]}  {p["title"]:<{width}}  {p["family"]:<10}'
              f'  {p["chars"]:>4} chars  -> /goal:{p["slug"]}{mark}')
    if violations:
        sys.exit(f"\nFAIL: {violations} lint violation(s)")

    missing_og = [p["id"] for p in prompts
                  if not (ROOT / "og" / f"{p['id']}.png").exists()]
    if missing_og:
        fail(f"briefs missing share cards: og/{{{','.join(missing_og)}}}.png"
             " — generate with scripts/og.py (needs Pillow)")

    # ---- README drift guard: its intro count and family taxonomy are
    # source-derived, so make silent drift a loud build failure ----
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    m = re.search(r"(\d+) mission briefs", readme)
    if not m:
        fail("README.md: missing the '<N> mission briefs' intro count")
    if int(m.group(1)) != len(prompts):
        fail(f"README.md says {m.group(1)} mission briefs but the catalog has "
             f"{len(prompts)} — update the intro line")
    missing_fams = [f for f in FAMILY_ORDER
                    if any(p["family"] == f for p in prompts)
                    and f"| {f} |" not in readme]
    if missing_fams:
        fail("README.md Families table is missing: " + ", ".join(missing_fams))

    # ---- og.png drift guard: the home share card bakes "N briefs" in as pixels,
    # so scripts/og.py embeds the count as PNG metadata and the build (stdlib
    # only — no Pillow) reads it back and compares to the live catalog ----
    def _png_text(path, key):
        b = path.read_bytes()
        if b[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        i = 8
        while i + 8 <= len(b):
            ln = int.from_bytes(b[i:i + 4], "big")
            if b[i + 4:i + 8] == b"tEXt":
                k, _, v = b[i + 8:i + 8 + ln].partition(b"\x00")
                if k.decode("latin1") == key:
                    return v.decode("latin1")
            i += 12 + ln
        return None
    og_n = _png_text(ROOT / "og.png", "gp-briefs")
    if og_n is None:
        fail("og.png has no gp-briefs metadata — regenerate with "
             "scripts/og.py --home")
    if int(og_n) != len(prompts):
        fail(f"og.png's baked-in count is {og_n} briefs but the catalog has "
             f"{len(prompts)} — regenerate with scripts/og.py --home (needs Pillow)")

    # ---- shared design tokens (single source of truth, linked by every page) ----
    (ROOT / "tokens.css").write_text(TOKENS_CSS, encoding="utf-8")

    # ---- injected site ----
    prompt_payload = [{**{k: p[k] for k in
                          ("id", "title", "family", "question", "output",
                           "tagline", "body", "chars")},
                       **({"example": BASE + p["example"]} if p.get("example") else {})}
                      for p in prompts]
    pb_opt = ("type", "badge", "featured", "window", "accent", "partner",
              "preview", "tagline")
    # no "conductor" in the injected payload: the client composes it with
    # makeConductor() (js/catalog-core.js); machines get raw/playbook-<key>.md
    pb_payload = [{**{k: pb[k] for k in ("key", "name", "desc", "ids")},
                   **{k: pb[k] for k in pb_opt if k in pb}}
                  for pb in playbooks]
    fam_payload = [[fam, next(p["question"] for p in prompts if p["family"] == fam)]
                   for fam in FAMILY_ORDER
                   if any(p["family"] == fam for p in prompts)]
    template = (ROOT / "template.html").read_text(encoding="utf-8")
    if BASE != DEFAULT_BASE:
        template = template.replace(DEFAULT_BASE, BASE)
    for token in ("__PROMPTS_JSON__", "__PLAYBOOKS_JSON__", "__FAMILIES_JSON__",
                  "__N_BRIEFS__", "__N_PLAYBOOKS__", "__N_FAMILIES__", "__GH_STARS__"):
        if token not in template:
            fail(f"template.html missing {token} placeholder")
    icon_gaps = lint_family_icons(template)
    if icon_gaps:
        fail("; ".join(icon_gaps))
    esc = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
    # Armed-but-hidden GitHub adoption badge. The real star count lives in
    # metrics.json (refreshed out-of-band by scripts/refresh-stars.py) so the
    # build stays offline + deterministic. Shown only at/above the threshold, so
    # a small or zero count never deflates — it turns itself on once adoption is
    # real (PROOF F2, fit to a young project with 0 stars today).
    STAR_THRESHOLD = 25
    try:
        stars = int(json.loads((ROOT / "metrics.json").read_text()).get("stars", 0))
    except Exception:
        stars = 0
    gh_stars = (f' \u00b7 <a href="https://github.com/GhostlyGawd/goal-prompts/stargazers">'
                f'{stars:,} stars on GitHub</a>') if stars >= STAR_THRESHOLD else ""
    # counts injected from source-of-truth so the static meta/OG tags and the
    # no-JS hero/chart fallbacks can never drift from the catalog again
    (ROOT / "index.html").write_text(
        template.replace("__PROMPTS_JSON__", esc(prompt_payload))
                .replace("__PLAYBOOKS_JSON__", esc(pb_payload))
                .replace("__FAMILIES_JSON__", esc(fam_payload))
                .replace("__N_BRIEFS__", str(len(prompts)))
                .replace("__N_PLAYBOOKS__", str(len(playbooks)))
                .replace("__N_FAMILIES__", str(len(fam_payload)))
                .replace("__GH_STARS__", gh_stars),
        encoding="utf-8")

    # ---- raw endpoints + full detail pages (brief + playbook) ----
    for d in ("raw", "b", "p"):
        shutil.rmtree(ROOT / d, ignore_errors=True)
        (ROOT / d).mkdir()
    for p in prompts:
        (ROOT / "raw" / f'{p["id"]}.md').write_text(p["body"] + "\n", encoding="utf-8")
        siblings = [s for s in prompts
                    if s["family"] == p["family"] and s["id"] != p["id"]]
        in_pb = [pb for pb in playbooks
                 if p["id"] in pb["ids"] and not pb.get("preview")]
        related = [by_id[r] for r in p.get("related", [])]
        (ROOT / "b" / f'{p["id"]}.html').write_text(
            brief_detail(p, siblings, in_pb, related), encoding="utf-8")
    for pb in playbooks:
        (ROOT / "raw" / f'playbook-{pb["key"]}.md').write_text(
            pb["conductor"], encoding="utf-8")
        (ROOT / "p" / f'{pb["key"]}.html').write_text(
            playbook_detail(pb, by_id), encoding="utf-8")

    # ---- per-family conductors ("run all Trust briefs") ----
    fam_conductors = {}
    for fam in FAMILY_ORDER:
        ids = [p["id"] for p in prompts if p["family"] == fam]
        if len(ids) < 2:
            continue
        slug = fam.lower()
        fam_pb = {"name": f"All {fam} briefs",
                  "desc": f"Every {fam} brief in the catalog, in order — {ids[0]} through {ids[-1]}, one report each.",
                  "ids": ids}
        (ROOT / "raw" / f"family-{slug}.md").write_text(
            conductor(fam_pb, by_id), encoding="utf-8")
        fam_conductors[fam] = f"{BASE}/raw/family-{slug}.md"

    # ---- machine-readable catalog ----
    catalog = {
        "name": "goal-prompts",
        "base": BASE,
        "families": FAMILY_ORDER,
        "playbooks": [{**{k: pb[k] for k in ("key", "name", "desc", "ids")},
                       "page": f"{BASE}/p/{pb['key']}",
                       "conductor": f"{BASE}/raw/playbook-{pb['key']}.md",
                       **{k: pb[k] for k in
                          ("type", "badge", "featured", "window", "tagline", "preview")
                          if k in pb}}
                      for pb in playbooks],
        "family_conductors": fam_conductors,
        "briefs": [{**{k: p[k] for k in ("id", "title", "family", "question",
                                         "output", "tagline", "chars", "slug")},
                    **({"example": BASE + p["example"]} if p.get("example") else {}),
                    "raw": f"{BASE}/raw/{p['id']}.md"} for p in prompts],
    }
    (ROOT / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
        encoding="utf-8")

    # ---- service worker (offline shell; version stamped from content) ----
    import hashlib as _hl
    ver_src = b"".join((ROOT / f).read_bytes() for f in
                       ("index.html", "studio.html", "vitals.html", "tokens.css",
                        "js/catalog-core.js", "js/report-parser.js", "js/gp-detail.js",
                        "icons/icon-192.png", "icons/icon-512.png"))
    sw_ver = _hl.sha256(ver_src).hexdigest()[:12]
    precache = ["/", "/studio", "/vitals", "/examples/", "/manifest.json",
                "/tokens.css", "/js/catalog-core.js", "/js/report-parser.js", "/js/gp-detail.js",
                "/fonts/schibstedgrotesk-latin-var.woff2", "/fonts/plexsans-latin-400.woff2", "/fonts/plexsans-latin-600.woff2", "/fonts/plexmono-latin-400.woff2",
                "/fonts/plexmono-latin-600.woff2",
                "/icons/icon-192.png", "/icons/icon-512.png"]
    (ROOT / "sw.js").write_text(SERVICE_WORKER
                                .replace("__VERSION__", sw_ver)
                                .replace("__PRECACHE__", json.dumps(precache)),
                                encoding="utf-8")

    # ---- sitemap + robots (crawlers can't guess 68 share pages) ----
    urls = [f"{BASE}/", f"{BASE}/studio", f"{BASE}/vitals", f"{BASE}/examples/"]
    urls += [f"{BASE}/p/{pb['key']}" for pb in playbooks]
    urls += [f"{BASE}/b/{p['id']}" for p in prompts]
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
               + "</urlset>\n")
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")

    write_archives(prompts)
    write_plugin(prompts)
    print(f"\nOK  {len(prompts)} briefs, {len(playbooks)} playbooks -> "
          f"index.html ({(ROOT / 'index.html').stat().st_size:,} b), "
          f"raw/, b/, catalog.json, sitemap.xml, robots.txt, "
          f"commands.tar.gz, commands.zip, plugin/")


if __name__ == "__main__":
    main()
