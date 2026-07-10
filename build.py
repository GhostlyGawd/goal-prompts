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
import datetime, gzip, io, json, os, re, shutil, sys, tarfile, zipfile
from pathlib import Path

ROOT = Path(__file__).parent
DEFAULT_BASE = "https://goal-prompts.vercel.app"
# Forks: set GOAL_PROMPTS_BASE to your deployment URL — every generated
# surface (site, raw/, conductors, catalog.json, brief bodies) follows it.
BASE = os.environ.get("GOAL_PROMPTS_BASE", DEFAULT_BASE).rstrip("/")
LIMIT = 4000
FAMILY_ORDER = ["Venture", "Product", "Quality", "Speed", "Trust", "Compliance",
                "Growth", "Team", "API", "Clarity", "Design", "Data", "Ops",
                "Reliability", "Subtract", "Meta", "Act", "Agent", "Automation",
                "AI-UX", "AI-Ethics"]
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
 * device.
 * R34 (RETENTION R8a): a worker can't read localStorage, so the pages mirror
 * the two fields this check needs — runs["29"] + remind.on — into IndexedDB
 * (db "gp-sw", store "kv", key "vitals"; writers: template.html's
 * mirrorVitalsState and js/gp-detail.js — keep all three in step). The
 * notification is skipped when reminders are off or Vitals ran under 7 days
 * ago; a missing mirror (an opt-in that predates it) falls back to notifying,
 * matching the old behavior rather than going silently dead. */
var VITALS_STALE_MS = 7 * 86400000;
function readVitalsState() {
  return new Promise(function (resolve) {
    var t = setTimeout(function () { resolve(null); }, 3000);
    function done(v) { clearTimeout(t); resolve(v); }
    try {
      var req = indexedDB.open("gp-sw", 1);
      req.onupgradeneeded = function () { try { req.result.createObjectStore("kv"); } catch (e) {} };
      req.onerror = function () { done(null); };
      req.onsuccess = function () {
        try {
          var db = req.result;
          var get = db.transaction("kv").objectStore("kv").get("vitals");
          get.onsuccess = function () { db.close(); done(get.result || null); };
          get.onerror = function () { db.close(); done(null); };
        } catch (e) { done(null); }
      };
    } catch (e) { done(null); }
  });
}
/* the notify decision, pure — exposed as self.gpShouldNotify so
 * tests/sw_reminder.test.cjs can exercise it without a browser */
function gpShouldNotify(state, now) {
  if (state && state.remindOn === false) return false;
  var last = (state && typeof state.runs29 === "number" && state.runs29 > 0) ? state.runs29 : 0;
  return !last || now - last >= VITALS_STALE_MS;
}
self.gpShouldNotify = gpShouldNotify;
self.addEventListener("periodicsync", function (e) {
  if (e.tag !== "vitals-weekly") return;
  e.waitUntil(readVitalsState().then(function (state) {
    if (!gpShouldNotify(state, Date.now())) return;
    /* R33 (RETENTION R6): land on the Vitals Viewer — the page that shows the
     * history this ritual accrues — instead of a cold catalog anchor. */
    return self.registration.showNotification("Weekly Vitals is due", {
      body: "Ten minutes for fresh trend arrows on your repo.",
      icon: "/icons/icon-192.png", badge: "/icons/icon-192.png",
      tag: "vitals-weekly", data: { url: "/vitals?src=reminder" }
    });
  }));
});
self.addEventListener("notificationclick", function (e) {
  e.notification.close();
  var url = (e.notification.data && e.notification.data.url) || "/";
  var bare = url.replace("?src=reminder", "");  // match open windows without the attribution query
  e.waitUntil(clients.matchAll({ type: "window" }).then(function (cs) {
    for (var i = 0; i < cs.length; i++) {
      if (cs[i].url.indexOf(bare) !== -1 && "focus" in cs[i]) {
        /* navigate the existing window so ?src=reminder rides along and the
         * page can fire reminder_return — a focus alone would hide the return.
         * If navigate() rejects, still surface the window rather than no-op. */
        if ("navigate" in cs[i]) {
          var win = cs[i];
          return win.navigate(url)
            .then(function (c) { return c ? c.focus() : win.focus(); })
            .catch(function () { return win.focus(); });
        }
        return cs[i].focus();
      }
    }
    if (clients.openWindow) return clients.openWindow(url);
  }));
});
"""


# R37 (RETENTION R11 · COMPETITIVE §6.4): the standing-audit GitHub Action,
# linked at the moments of proven intent (post-Vitals mark, b/29, p/vitals).
# template.html and js/gp-detail.js carry the same URL as a literal.
WORKFLOW_URL = ("https://github.com/GhostlyGawd/goal-prompts/blob/main/"
                ".github/run-brief.example.yml")

# R52 (CRO NF5 · REVENUE §4.1–2): the one partner contact. Both CTAs (the
# landing Partnerships band — kept as a literal in template.html, guarded by
# tests — and every /p/ partner block) point here; the old /p/ target was
# GitHub Discussions, which isn't enabled on the repo. The private email
# channel REVENUE §4.2 wants is external (no address exists yet — never
# invent one); the issue template offers a "prefer to talk privately?" out.
PARTNER_CTA_URL = ("https://github.com/GhostlyGawd/goal-prompts/issues/new"
                   "?template=partnership.md&title=Partnership+inquiry")

# R56 (REVENUE §3.3), dormant until R53: the post-activation backer nudge is
# gated on this URL the same way the star badge gates on metrics.json — empty
# means the logic ships dark with zero user-visible change. Set it to a real
# Sponsors/backers URL once one exists; nothing else needs editing.
BACKER_URL = ""


# =====================================================================
# Detail pages — every brief and every playbook gets a full, crawlable,
# conversion-shaped page (not a redirect stub). The catalog stays the shop
# floor; these are the product pages. All markup is generated here from the
# same brief bodies the linter guards, so the pages can never drift from the
# prompts they describe.
# =====================================================================

def esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def jsonld(obj) -> str:
    """One <script type="application/ld+json"> block (SEO-6, R32).
    json.dumps owns the quote escaping; "</" is additionally escaped so a
    hostile title/tagline can never close the script element early."""
    return ('<script type="application/ld+json">'
            + json.dumps(obj, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).replace("</", "<\\/")
            + "</script>\n")


def png_text(path, key):
    """Read a tEXt chunk from a PNG, stdlib-only — the OG drift guards use it
    to compare a card's baked-in-pixels count against the live catalog."""
    b = Path(path).read_bytes()
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


def playbook_og_violations(playbooks, og_dir) -> list:
    """R31 (SEO-3): every playbook page references its own og/p-<key>.png.
    Like og.png, each card bakes its brief count in as pixels, so scripts/og.py
    embeds the count as PNG metadata and the (stdlib-only) build compares it
    to the live playbook here."""
    v = []
    for pb in playbooks:
        f = Path(og_dir) / f'p-{pb["key"]}.png'
        if not f.exists():
            v.append(f'playbook "{pb["key"]}" has no share card og/{f.name}'
                     f' — generate with scripts/og.py --playbooks')
            continue
        n = png_text(f, "gp-briefs")
        if n is None or int(n) != len(pb["ids"]):
            v.append(f'og/{f.name} is stale (baked-in count {n}, catalog has '
                     f'{len(pb["ids"])} briefs) — regenerate with '
                     f'scripts/og.py --playbooks')
    return v


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
  --rainbow:linear-gradient(90deg,#E8B44C,#E8705F,#4D9FFF,#52C280,#A98CF5,#9AD4E8,#5CE8A0,#F0904A,#B4C64A,#3FC1C9,#E87FB0,#C4CBD8,#E84C3D,#8B7CF8,#E8DE5A,#F06FD8,#C878F0);
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
.dhero .offer{margin-top:14px;font-family:var(--mono);font-size:12px;color:var(--faint);line-height:1.6}

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
.lens h3{font-family:var(--disp);font-size:15px;font-weight:660;margin-bottom:3px;letter-spacing:-.01em;color:var(--text)}
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
.way h3{font-family:var(--disp);font-size:14px;font-weight:660;margin-bottom:4px;color:var(--text)}
.way .num{font-family:var(--mono);font-size:11px;color:var(--fc);letter-spacing:.1em}
.way p{font-size:13px;color:var(--dim);margin:2px 0 12px;line-height:1.5}
.cmd{display:flex;align-items:center;gap:8px;font-family:var(--mono);font-size:12px;color:var(--text);background:var(--ink-2);border:1px solid var(--line);border-radius:9px;padding:10px 11px;overflow-x:auto;min-width:0}
.cmd+.cmd{margin-top:8px}
.cmd .cmdstep{flex:none;font-family:var(--mono);font-size:11px;font-weight:600;color:var(--fc)}
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
.rules h3{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--fc);margin-bottom:9px}
.rules ul{list-style:none;display:grid;gap:8px}
.rules li{font-size:14px;color:var(--text);padding-left:20px;position:relative}
.rules li::before{content:"→";position:absolute;left:0;color:var(--fc)}

/* related + cards */
.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:20px}
.pcard{display:block;background:var(--panel);border:1px solid var(--line);border-left:2px solid var(--fc);border-radius:var(--radius);padding:15px 16px;transition:transform .15s,border-color .15s}
.pcard:hover{transform:translateY(-2px);border-color:var(--line-2)}
.pcard .pid{font-family:var(--mono);font-size:12px;color:var(--fc)}
.pcard h3{font-family:var(--disp);font-size:16px;font-weight:660;margin:3px 0 5px;letter-spacing:-.01em;color:var(--text)}
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
.gp-hint a{color:var(--fc);text-decoration:underline}
.gp-hint b{color:var(--text)}
.gp-hint .markrun{flex:none;background:var(--good);color:#0C1510;border:0;border-radius:6px;font-family:var(--sans);font-size:12px;font-weight:600;padding:4px 9px;cursor:pointer;white-space:nowrap}
.gp-hint .markrun:disabled{opacity:.6;cursor:default}
.gp-hint .x{flex:none;background:none;border:0;color:var(--faint);cursor:pointer;font-size:16px;line-height:1;padding:2px}
.gp-hint .x:hover{color:var(--text)}

/* RETENTION R7 (R02): slim welcome-back strip for returning visitors —
   built by gp-detail.js only when gp-runs has data, dismissible */
.gp-wb{border-bottom:1px solid var(--line);background:var(--panel);font-size:13px;color:var(--dim)}
.gp-wb .wrap{display:flex;align-items:center;gap:8px;padding-top:9px;padding-bottom:9px;flex-wrap:wrap}
.gp-wb b{color:var(--text);font-weight:600}
.gp-wb a{color:var(--fc,#C4CBD8);font-family:var(--mono);text-decoration:none;white-space:nowrap}
.gp-wb a:hover{text-decoration:underline}
.gp-wb .x{margin-left:auto;background:none;border:0;color:var(--faint);cursor:pointer;font-size:16px;line-height:1;padding:2px 4px}
.gp-wb .x:hover{color:var(--text)}

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


def static_catalog(prompts) -> str:
    """R28 (SEO-1): the crawlable homepage catalog. A plain, family-grouped
    link list of every brief — emitted into #list from the same parsed
    prompts as the JS payload (so it can never drift), then replaced by the
    interactive catalog when the inline script boots. Links + taglines only:
    the page stays light (bodies live in bodies.json, R29)."""
    out = []
    for fam in FAMILY_ORDER:
        members = [p for p in prompts if p["family"] == fam]
        if not members:
            continue
        items = "".join(
            f'<li><a href="/b/{p["id"]}">{esc(p["id"])} · {esc(p["title"])}</a>'
            f'<span class="st"> — {esc(p["tagline"])}</span></li>'
            for p in members)
        out.append(
            f'<section class="sfam f-{fam.lower()}">'
            f'<h3 class="famhead"><span class="name">{esc(fam)}</span>'
            f'<span class="q">{esc(members[0]["question"])}</span>'
            f'<span class="rule"></span></h3>'
            f'<ul class="sbriefs">{items}</ul></section>')
    return "".join(out)


def static_playbooks(playbooks, by_id) -> tuple:
    """R28 (SEO-1): the crawlable storefront — a static card per featured
    playbook and a pill per remaining one, mirroring renderFeatured()'s
    6-card split so the JS swap-in changes nothing visible."""
    feat = [pb for pb in playbooks if pb.get("featured")]
    rest = feat[6:] + [pb for pb in playbooks if not pb.get("featured")]
    cards = []
    for pb in feat[:6]:
        first = by_id[pb["ids"][0]]
        style = f' style="--fc:{attr(pb["accent"])}"' if pb.get("accent") else ""
        cls = "" if pb.get("accent") else " f-" + first["family"].lower()
        n = len(pb["ids"])
        cards.append(
            f'<a class="storecard{cls}" href="/p/{pb["key"]}"{style}>'
            f'<h3>{esc(pb["name"])}</h3>'
            f'<p class="tl">{esc(pb.get("tagline") or pb["desc"])}</p>'
            f'<span class="seqdots"><span class="cnt">{n} brief'
            f'{"s" if n > 1 else ""}</span></span>'
            f'<span class="go">Explore playbook →</span></a>')
    pills = ['<span class="morelab">more sequences</span>'] if rest else []
    for pb in rest:
        first = by_id[pb["ids"][0]]
        style = f' style="--fc:{attr(pb["accent"])}"' if pb.get("accent") else ""
        pills.append(
            f'<a class="pb-pill f-{first["family"].lower()}" '
            f'href="/p/{pb["key"]}"{style}>'
            f'<b>{esc(pb["name"])}</b> '
            f'<span class="len">{len(pb["ids"])}</span></a>')
    return "".join(cards), "".join(pills)


def page(title, desc, canon, body_html, og_image, og_type="website",
         body_class="", head_extra="") -> str:
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
            # SEO-9 (R30): site_name + image dims/alt + explicit twitter
            # title/description — scrapers stop guessing, unfurlers get alt text
            '<meta property="og:site_name" content="Goal Prompts">\n'
            '<meta property="og:image:width" content="1200">\n'
            '<meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="{attr(title)}">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:image" content="{og_image}">\n'
            f'<meta name="twitter:title" content="{attr(title)}">\n'
            f'<meta name="twitter:description" content="{attr(desc)}">\n'
            '<meta name="theme-color" content="#131417">\n'
            '<link rel="manifest" href="/manifest.json">\n'
            f'<link rel="canonical" href="{canon}">\n'
            + head_extra +
            f'<link rel="icon" href="{FAVICON}">\n'
            '<link rel="preload" href="/fonts/schibstedgrotesk-latin-var.woff2" as="font" type="font/woff2" crossorigin>\n'
            '<link rel="preload" href="/fonts/plexsans-latin-400.woff2" as="font" type="font/woff2" crossorigin>\n'
            '<link rel="preload" href="/fonts/plexmono-latin-400.woff2" as="font" type="font/woff2" crossorigin>\n'
            # R02 (FUNNEL §4.1 / RETENTION R7): the side doors carry the same
            # anonymous insights script + va queue shim as the landing page —
            # entry mix, copies, and returns on /b/ and /p/ become visible.
            '<script defer src="/_vercel/insights/script.js"></script>\n'
            '<script>window.va=window.va||function(){(window.vaq=window.vaq||[]).push(arguments)};</script>\n'
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
            '<a href="/vitals">Vitals Viewer</a>'
            '<a href="/examples/">Sample reports</a>'
            '<a href="/quality">Why briefs don\'t rot</a>'
            '<a href="/changelog">Changelog</a>'
            '<a href="/teams">For teams</a>'
            '<a href="/partners">Partners</a>'
            '<a href="https://github.com/GhostlyGawd/goal-prompts">GitHub</a></div>'
            '<p class="fine">Free &amp; open source · MIT licensed · every brief under 4,000 characters · '
            'works with Claude Code, Cursor, Copilot &amp; any coding agent</p>'
            '</div></footer>')


def cmd_html(text: str, step: int = 0, label: str = "") -> str:
    import hashlib
    cid = "c" + hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
    # CRO NF3 (R07): multi-command installs render as numbered copyable steps
    lab = f'<span class="cmdstep">{step}</span>' if step else ""
    # B2 review carry-over (R02 batch): every .cp button said just "copy" to a
    # screen reader — give each a distinguishing accessible name
    aria = label or (f"copy step {step}" if step else "copy command")
    return (f'<div class="cmd">{lab}<code>{esc(text)}</code>'
            f'<button class="cp" data-copy="#{cid}" aria-label="{attr(aria)}">copy</button>'
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
    else:
        # PROOF NF6 (R19): the 121 briefs without their own sample still get
        # evidence in eyeshot of the copy button — the generic gallery.
        cta.append('<a class="btn btn-ghost" href="/examples/">See real sample reports ↗</a>')
    # CRO NF2 (R19): the landing page's offer + risk-reversal, restated at the
    # side-door CTA. Brief 47 is the catalog's one code-modifying brief — its
    # line must not claim read-only (CLAUDE.md's Fixer exception).
    offer = ('Free &amp; open · no signup · it asks before touching anything — '
             'you pick what it fixes · nothing leaves your machine'
             if p["id"] == "47" else
             'Free &amp; open · no signup · read-only — it ends by asking · '
             'nothing leaves your machine')

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
            f'<p class="offer">{offer}</p>'
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
                          f'<h3>{esc(name)}</h3><p>{md_inline(d)}</p></div></div>')
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
    if p["id"] == "29":
        # R33 (RETENTION R6): the deliverable accrues — say where the history
        # becomes visible, right where the deliverable is described.
        rfoot.append('<a href="/vitals" style="color:var(--fc)">paste it into '
                     'the Vitals Viewer — your trend history →</a>')
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
    per_brief_cmd = f'curl -fsSL {BASE}/install | BRIEF={p["id"]} sh'
    per_brief_label = f'copy the install command for just brief {p["id"]}'
    ways = (f'<section class="blk" id="use"><div class="wrap">'
            f'<div class="kicker">Get started</div>'
            f'<h2 class="h2">Three ways to run this brief</h2>'
            f'<div class="ways">'
            f'<div class="way"><div class="num">01 · COPY</div><h3>Paste it in</h3>'
            f'<p>Copy the prompt and paste it into your agent inside the repo you want audited.</p>'
            f'<button class="btn btn-primary" style="width:100%;justify-content:center" {copy_attrs}>Copy this prompt</button></div>'
            f'<div class="way"><div class="num">02 · INSTALL</div><h3>As a slash command</h3>'
            f'<p>Install the <b>goal</b> plugin once — two commands — then just type <code>/goal:{esc(slug)}</code>.</p>'
            f'{cmd_html("/plugin marketplace add GhostlyGawd/goal-prompts", step=1)}'
            f'{cmd_html("/plugin install goal@goal-prompts", step=2)}'
            # R43 (COMPETITIVE §3.3): install just this brief — no all-or-nothing
            f'<p style="margin:12px 0 8px">Or install only this brief as <code>/goal-{esc(slug)}</code>:</p>'
            f'{cmd_html(per_brief_cmd, label=per_brief_label)}</div>'
            f'<div class="way"><div class="num">03 · AGENT</div><h3>From an agent (MCP)</h3>'
            f'<p>Let an agent fetch it mid-conversation, or pull the raw brief by URL.</p>'
            f'{cmd_html(BASE + "/raw/" + p["id"] + ".md", label="copy raw brief URL")}</div>'
            f'</div></div></section>')

    # R33/R37 (RETENTION R6/R11): brief 29 is a weekly ritual — its page names
    # both halves of what keeps it weekly: the Vitals Viewer (where the pasted
    # history accrues into trends) and the standing-audit GitHub Action
    # (which runs without human memory).
    ritual = ""
    if p["id"] == "29":
        ritual = (
            f'<section class="blk"><div class="wrap">'
            f'<div class="kicker">Keep the ritual</div>'
            f'<h2 class="h2">Make it a standing appointment</h2>'
            f'<p class="lead">Each run appends one dated row to <code>{esc(p["output"])}</code> — '
            f'drop the file on the <a href="/vitals" style="color:var(--fc)">Vitals Viewer</a> and '
            f'every vital becomes a sparkline with run-over-run deltas. And a ready-made GitHub '
            f'Action runs this brief every Monday and files the report as an issue, so the ritual '
            f'survives without your memory: '
            f'<a href="{WORKFLOW_URL}" style="color:var(--fc)">copy the workflow ↗</a></p>'
            f'</div></section>')

    # full brief + rules
    rules = ""
    if parts["rules"]:
        rules = ('<div class="rules"><h3>House rules for this brief</h3><ul>'
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
                f'<h3>{esc(s["title"])}</h3><p>{esc(s["tagline"])}</p></a>')
    rel = ""
    rel_cards = "".join(_pcard(r) for r in related)
    if p["id"] == "47":
        # the Fixer's natural neighbor isn't a brief — it's the Studio, where
        # checked findings become this brief's targeted form
        rel_cards += ('<a class="pcard" href="/studio">'
                      '<div class="pid">Studio · Act</div>'
                      '<h3>Report Studio</h3>'
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

    body = hero + whatis + lenses + report + method + ways + ritual + full + rel + ftr
    title = f'{p["id"]} · {p["title"]} — Goal Prompts'
    # SEO-6 (R32): BreadcrumbList mirrors the visible crumb; the 4-phase
    # method maps to HowTo steps — all from data already in hand at build time
    ld = jsonld({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Catalog",
             "item": BASE + "/#catalog"},
            {"@type": "ListItem", "position": 3,
             "name": f'{p["id"]} · {p["title"]}',
             "item": f'{BASE}/b/{p["id"]}'}]})
    ld += jsonld({
        "@context": "https://schema.org", "@type": "HowTo",
        "name": p["title"], "description": p["tagline"],
        "isAccessibleForFree": True,
        "step": [{"@type": "HowToStep", "position": ph["n"],
                  "name": f'Phase {ph["n"]} — {ph["name"]}',
                  "text": ph["gist"] or ph["name"]}
                 for ph in parts["phases"]]})
    return page(title, p["tagline"], f"{BASE}/b/{p['id']}", body,
                f"{BASE}/og/{p['id']}.png", "article", fc, head_extra=ld)


def window_chip(win) -> str:
    """Merchandising `window` → chip HTML, date-gated (CRO NF4, R22).

    A plain string renders as an evergreen chip. A {"label", "months"} object
    renders *hidden* with its months in a data attribute; gp-detail.js unhides
    it only while the viewer's month is inside the window. Gating on the
    viewer's clock (not the build's) keeps the build deterministic and means a
    stale deploy can never show "January drop" in July — without JS the chip
    simply stays hidden, which is the safe direction."""
    if isinstance(win, str):
        return f'<span class="chip">{esc(win)}</span>'
    label = win.get("label")
    months = win.get("months")
    if not label or not isinstance(label, str):
        fail(f"playbook window {win!r} needs a non-empty 'label'")
    if (not months or not isinstance(months, list)
            # type() not isinstance(): bool is an int subclass, and [True]
            # would serialize as a silently dead data-window-months="True"
            or any(type(m) is not int or not 1 <= m <= 12 for m in months)):
        fail(f"playbook window '{label}' needs 'months' as a list of ints 1-12")
    ms = ",".join(str(m) for m in months)
    return f'<span class="chip" data-window-months="{ms}" hidden>{esc(label)}</span>'


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
    win = window_chip(pb["window"]) if pb.get("window") else ""

    # CRO NF2 (R19): offer + risk-reversal at the conductor CTA. Sequences
    # that end in 47 · The Fixer aren't read-only — say so honestly.
    offer = ('Free &amp; open · no signup · audits are read-only — the Fixer '
             'asks before any edit · nothing leaves your machine'
             if "47" in pb["ids"] else
             'Free &amp; open · no signup · read-only — every stage ends by '
             'asking · nothing leaves your machine')

    hero = (f'<section class="dhero" {style}><div class="wrap">'
            f'<div class="crumb"><a href="/">Home</a><span class="sep">/</span>'
            f'<a href="/#playbooks">Playbooks</a><span class="sep">/</span>'
            f'<span>{esc(pb["name"])}</span></div>'
            f'<div style="margin-top:14px">{badge}'
            f'<span class="chip">Playbook · {n} brief{"s" if n>1 else ""}</span> {win}</div>'
            f'<h1 style="margin-top:14px">{esc(pb["name"])}</h1>'
            f'<p class="lede">{esc(pb.get("tagline") or pb["desc"])}</p>'
            f'<div class="cta">'
            # data-pb + data-raw: gp-detail.js fires copy_conductor with the
            # key and degrades to the raw conductor link on clipboard failure
            f'<button class="btn btn-primary" data-copy="#rawcond" data-pb="{pb["key"]}" '
            f'data-raw="{BASE}/raw/playbook-{pb["key"]}.md">Copy the conductor</button>'
            f'<a class="btn btn-ghost" href="#seq">See the sequence</a>'
            f'<a class="btn btn-ghost" href="/examples/">See real sample reports ↗</a></div>'
            f'<p class="offer">{offer}</p>'
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
    # R33 (RETENTION R6): sequences that run 29 accrue a history — say where
    # it becomes visible (the Vitals Viewer), right where the outputs land.
    vitals_line = ""
    if "29" in pb["ids"]:
        vitals_line = (' Drop each week\'s <code>HEALTH.md</code> on the '
                       '<a href="/vitals" style="color:var(--fc)">Vitals Viewer</a> '
                       'to watch your trend history grow.')
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
           f'to merge them into one plan.{vitals_line}</p></div></div></div>'
           f'</div></section>')

    # how to run
    run = (f'<section class="blk" {style}><div class="wrap">'
           f'<div class="kicker">Get started</div>'
           f'<h2 class="h2">One paste runs the whole thing</h2>'
           f'<p class="lead">Copy the conductor into your agent inside the repo you want audited. '
           f'It runs each brief in sequence, honoring every brief\'s ask-first rule.</p>'
           f'<div class="cta" style="margin-top:18px">'
           f'<button class="btn btn-primary" data-copy="#rawcond" data-pb="{pb["key"]}" '
           f'data-raw="{BASE}/raw/playbook-{pb["key"]}.md">Copy the conductor</button>'
           f'<a class="btn btn-ghost" href="{BASE}/raw/playbook-{pb["key"]}.md">View raw ↗</a></div>'
           # R37 (RETENTION R11): playbooks meant to repeat get the
           # standing-appointment path at the point of intent
           + (f'<div class="note">Make it a standing appointment — a ready-made GitHub Action '
              f'runs a brief on a Monday cron and files the report as an issue. '
              f'<a href="{WORKFLOW_URL}" style="color:var(--fc)">Copy '
              f'<code>.github/run-brief.example.yml</code> into your repo ↗</a></div>'
              if "29" in pb["ids"] else "")
           + f'</div></section>')

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
                  # R52: the unified partner contact — same destination as the
                  # landing band, and a working one (Discussions isn't enabled)
                  f'<a class="btn btn-primary" href="{PARTNER_CTA_URL}">'
                  f'{esc(partner.get("cta", "Partner with us"))}</a>'
                  f'<p class="note">Formats &amp; specs: <a href="/partners" '
                  f'style="color:var(--fc)">/partners</a> · Want this set up '
                  f'for your org, with your own briefs? <a href="/teams" '
                  f'style="color:var(--fc)">Goal Prompts for Teams →</a></p>'
                  f'</div></div></section>')

    # briefs as cards
    cards = "".join(
        f'<a class="pcard {"f-"+by_id[i]["family"].lower()}" href="/b/{i}">'
        f'<div class="pid">{esc(i)} · {esc(by_id[i]["family"])}</div>'
        f'<h3>{esc(by_id[i]["title"])}</h3>'
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
    # SEO-6 (R32): breadcrumbs + the member briefs as a machine-readable list
    n_name = pb["name"]
    ld = jsonld({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Playbooks",
             "item": BASE + "/#playbooks"},
            {"@type": "ListItem", "position": 3, "name": n_name,
             "item": f'{BASE}/p/{pb["key"]}'}]})
    ld += jsonld({
        "@context": "https://schema.org", "@type": "ItemList",
        "name": n_name, "description": pb.get("tagline") or pb["desc"],
        "numberOfItems": n,
        "itemListElement": [
            {"@type": "ListItem", "position": i,
             "name": f'{pid} · {by_id[pid]["title"]}',
             "url": f"{BASE}/b/{pid}"}
            for i, pid in enumerate(pb["ids"], 1)]})
    # SEO-3 (R31): each playbook unfurls with its own card, not the site-wide one
    return page(title, pb.get("tagline") or pb["desc"], f"{BASE}/p/{pb['key']}",
                body, f"{BASE}/og/p-{pb['key']}.png", "website", body_class,
                head_extra=ld)


def changelog_page(md: str) -> str:
    """CHANGELOG.md → the /changelog page (R36, RETENTION R10).

    Installed surfaces (plugin, curl commands, MCP server) pin the catalog
    they shipped with; this page is the one URL that always says what's new —
    the MCP tool footers and the installer's outro point here. Rendering
    reuses the briefs' own tiny markdown subset (md_block/md_inline): `## `
    headings split releases, everything else is escaped paragraph/list text."""
    releases, cur_head, cur = [], None, []
    for line in md.splitlines():
        m = re.match(r"^##\s+(.*)$", line)
        if m:
            if cur_head is not None:
                releases.append((cur_head, "\n".join(cur)))
            cur_head, cur = m.group(1).strip(), []
        elif cur_head is not None:
            cur.append(line)
    if cur_head is not None:
        releases.append((cur_head, "\n".join(cur)))
    if not releases:
        fail("CHANGELOG.md has no '## <version>' releases to render")

    secs = "".join(
        f'<section class="blk"><div class="wrap">'
        f'<div class="kicker mono">release</div>'
        f'<h2 class="h2">{esc(head)}</h2>'
        f'<div class="prose" style="margin-top:12px">{md_block(chunk)}</div>'
        f'</div></section>'
        for head, chunk in releases)

    latest = releases[0][0]
    hero = (f'<section class="dhero"><div class="wrap">'
            f'<div class="crumb"><a href="/">Home</a><span class="sep">/</span>'
            f'<span>Changelog</span></div>'
            f'<h1 style="margin-top:14px">Changelog</h1>'
            f'<p class="lede">What changed, release by release — latest: '
            f'<span class="mono">{esc(latest)}</span>. Installed the plugin, the slash '
            f'commands, or the MCP server? They pin the catalog they shipped with; '
            f'update any time to pick up new briefs.</p>'
            f'<div class="cta">'
            f'<a class="btn btn-primary" href="/#start">Install / update</a>'
            f'<a class="btn btn-ghost" href="https://github.com/GhostlyGawd/goal-prompts/blob/main/CHANGELOG.md">Raw CHANGELOG.md ↗</a>'
            f'</div></div></section>')

    ftr = foot("Pick up what's new",
               "Re-run the installer or update the plugin — the whole catalog "
               "stays free and open.",
               '<a class="btn btn-primary" href="/#catalog">Browse the catalog</a>'
               '<a class="btn btn-ghost" href="/#start">Install everything</a>')

    return page("Changelog — Goal Prompts",
                f"Every goal-prompts release — new briefs, playbooks, and fixes. "
                f"Latest: {latest}.",
                f"{BASE}/changelog", hero + secs + ftr, f"{BASE}/og.png")


def quality_page(prompts: list) -> str:
    """R50 (COMPETITIVE §10 bet 2, §6.1): /quality — why these briefs don't
    rot. The category's complaint record is flaky, stale, unmanageable
    prompts; this catalog's answer is a machine-enforced floor that no rival
    has. Everything on the page is checkable: each claim links the linter
    source, the CI workflow, or the dogfooding artifacts."""
    gh = "https://github.com/GhostlyGawd/goal-prompts/blob/main/"
    n = len(prompts)

    def rules_block(title, items):
        return ('<div class="rules" style="margin-top:18px"><h3>'
                + esc(title) + '</h3><ul>'
                + "".join(f"<li>{item}</li>" for item in items)
                + "</ul></div>")

    hero = (f'<section class="dhero"><div class="wrap">'
            f'<div class="crumb"><a href="/">Home</a><span class="sep">/</span>'
            f'<span>Quality</span></div>'
            f'<h1 style="margin-top:14px">Why these briefs don’t rot</h1>'
            f'<p class="lede">Prompt catalogs age badly: rules go stale, quality varies '
            f'by entry, and nothing enforces a floor. Every one of the {n} briefs here '
            f'passes a published linter and a CI gate before it ships — this page is '
            f'the bar, with links to the code that enforces it.</p>'
            f'<div class="cta">'
            f'<a class="btn btn-primary" href="/#catalog">Browse the catalog</a>'
            f'<a class="btn btn-ghost" href="{gh}build.py">Read the linter source ↗</a>'
            f'</div></div></section>')

    linter = (
        f'<section class="blk"><div class="wrap">'
        f'<div class="kicker">The linter</div>'
        f'<h2 class="h2">Every brief passes the same published linter.</h2>'
        f'<p class="lead">Not a style guide — a build step. <code>python3 build.py</code> '
        f'refuses to build the site (and the deploy) unless every brief in the catalog '
        f'clears every rule below. The rules live in '
        f'<a href="{gh}build.py" style="color:var(--fc)">build.py</a>, in the open, and the '
        f'linter has <a href="{gh}tests/test_build.py" style="color:var(--fc)">its own test '
        f'suite</a> so the bar itself can’t silently loosen.</p>'
        + rules_block("Structure — enforced on all " + str(n) + " briefs", [
            'The four-phase skeleton: <code>## Phase 1–4</code> — Explore → '
            'Audit → Curate → Report — plus a <code>## Rules</code> section.',
            f'Body under {LIMIT:,} characters — short enough to read before you run it.',
            'Phase 2 audits through 4–12 named lenses; each report section has a defined shape.',
            'The brief names its one report file (<code>REPORT.md</code>-shaped, ALL-CAPS), '
            'and no two briefs may write the same file.',
            'Re-runs are first-class: the report is dated, and a report that already exists '
            'is read first so the new one leads with what changed.',
        ])
        + rules_block("Safety — the ask-first gate", [
            'Every brief ends with the literal gate: “Report only — end by asking …” '
            '— the linter greps for it and fails the build without it.',
            'Audit briefs are read-only toward your code; the only write is the report itself '
            '(honest exception: <a href="/b/47" style="color:var(--fc)">47 · The Fixer</a> '
            'modifies code, and gates on your explicit selection first).',
            'A brief whose subject a repo simply doesn’t have must say so in a one-paragraph '
            'null report and stop — no invented findings.',
        ])
        + '</div></section>')

    ci = (f'<section class="blk"><div class="wrap">'
          f'<div class="kicker">The gate</div>'
          f'<h2 class="h2">CI runs the whole bar on every change.</h2>'
          f'<p class="lead">Every push and pull request runs '
          f'<a href="{gh}.github/workflows/ci.yml" style="color:var(--fc)">.github/workflows/ci.yml</a>: '
          f'the build (which lints all {n} briefs), the linter’s own tests, a hermetic '
          f'installer test, and the MCP smoke test — then fails on any drift between '
          f'sources and generated files. The Vercel deploy runs the same build as a hard '
          f'gate, so an oversized or rule-breaking brief can’t reach production. '
          f'Contributions clear the identical bar — the linter is the moderation story '
          f'(<a href="{gh}CONTRIBUTING.md" style="color:var(--fc)">CONTRIBUTING.md</a>).</p>'
          f'</div></section>')

    dogfood = (
        f'<section class="blk"><div class="wrap">'
        f'<div class="kicker">The receipts</div>'
        f'<h2 class="h2">It’s run against its own code, in the open.</h2>'
        f'<p class="lead">The briefs audit this site’s own repo: the reports they wrote are '
        f'<a href="/examples/" style="color:var(--fc)">published as live samples</a>, and the '
        f'<a href="/FIXLOG.md" style="color:var(--fc)">FIXLOG</a> traces shipped fixes back to '
        f'the report and finding that surfaced each one. Nothing here is a mock-up — the '
        f'loop (brief → report → <a href="/studio" style="color:var(--fc)">Studio</a> '
        f'→ Fixer → FIXLOG) is how this catalog maintains itself. When a brief '
        f'under-delivers on this repo, it gets sharpened before it stays in the catalog.</p>'
        f'</div></section>')

    ftr = foot("Hold your repo to the same bar",
               "Every audit is one paste away — and every brief you paste "
               "cleared everything on this page.",
               '<a class="btn btn-primary" href="/#catalog">Browse the catalog</a>'
               '<a class="btn btn-ghost" href="/examples/">See real reports</a>')

    return page("Why these briefs don't rot — Goal Prompts",
                f"The quality bar behind all {n} audit briefs: a published "
                f"linter, a CI gate, a {LIMIT:,}-character cap, the ask-first "
                f"safety rule, and reports dogfooded on the catalog's own repo.",
                f"{BASE}/quality", hero + linter + ci + dogfood + ftr,
                f"{BASE}/og.png")


def teams_page(prompts: list) -> str:
    """R55 (REVENUE §5/§3.2 · COMPETITIVE §10 bet 3): /teams — the offer page
    that productizes what already ships free: the private-catalog build
    (GOAL_PROMPTS_BASE), the installer/plugin/MCP/skills distribution, and
    the standing-audit GitHub Action. Honesty rules: pricing is the
    maintainer's call and doesn't exist yet, so the page says "on request";
    the only dollar figures are the cited competitor range and $0; the DIY
    path is documented right on the page."""
    gh = "https://github.com/GhostlyGawd/goal-prompts/blob/main/"
    n = len(prompts)

    hero = (f'<section class="dhero"><div class="wrap">'
            f'<div class="crumb"><a href="/">Home</a><span class="sep">/</span>'
            f'<span>For teams</span></div>'
            f'<h1 style="margin-top:14px">Goal Prompts for Teams</h1>'
            f'<p class="lede">Run the whole catalog — plus your own private, '
            f'linted briefs — inside your org: your own deployment, your own '
            f'slash commands, standing audits on a cron. Everything below '
            f'already exists in the open repo; the offer is having it set up, '
            f'extended with your briefs, and supported for you.</p>'
            f'<div class="cta">'
            f'<a class="btn btn-primary" href="{PARTNER_CTA_URL}">Ask about a team setup →</a>'
            f'<a class="btn btn-ghost" href="{gh}README.md#run-your-private-team-catalog">Read the DIY docs ↗</a>'
            f'</div></div></section>')

    what = (f'<section class="blk"><div class="wrap">'
            f'<div class="kicker">The pipeline</div>'
            f'<h2 class="h2">A private audit pipeline, built from shipping parts.</h2>'
            f'<p class="lead">Nothing here is vaporware — each piece is live in the '
            f'public repo today and MIT-licensed. A Teams engagement assembles them '
            f'around your org.</p>'
            f'<div class="rules" style="margin-top:18px"><h3>What a setup includes</h3><ul>'
            f'<li><b>A private catalog.</b> A fork built with '
            f'<code>GOAL_PROMPTS_BASE=https://audits.your-co.internal python3 build.py</code> '
            f'— the site, raw endpoints, conductors, and <code>catalog.json</code> all '
            f'point at your internal deployment. Nothing your briefs touch leaves your infra.</li>'
            f'<li><b>Your own briefs.</b> Org-specific audits — your stack, your compliance '
            f'bar, your review checklist — written to the same '
            f'<a href="/quality" style="color:var(--fc)">published linter and CI gate</a> '
            f'that keeps the public {n} from rotting.</li>'
            f'<li><b>Distribution to every seat.</b> The slash-command installer '
            f'(<code>BASE=… sh install</code>), the Claude Code plugin, the MCP server, '
            f'and the skills tree — the same one-paste flow, pointed at your catalog.</li>'
            f'<li><b>Standing audits.</b> '
            f'<a href="{gh}.github/run-brief.example.yml" style="color:var(--fc)">'
            f'<code>run-brief.example.yml</code> ↗</a> wired into your repos: a scheduled '
            f'brief runs on a cron and files its report as an issue — audits as an '
            f'appointment, not a memory.</li>'
            f'</ul></div></div></section>')

    price = (f'<section class="blk"><div class="wrap">'
             f'<div class="kicker">Pricing</div>'
             f'<h2 class="h2">Flat fee, on request. No per-seat metering.</h2>'
             f'<p class="lead">A setup engagement plus an optional support retainer — '
             f'scoped per org, priced flat, nothing metered. <b>Pricing is on '
             f'request</b> via the partnership contact; the project is young and '
             f'every engagement is scoped individually.</p>'
             f'<p class="lead" style="margin-top:12px">For scale: adjacent automated-review '
             f'products price per seat — CodeRabbit’s paid tiers run about $24–$48 '
             f'per user per month on their published plans. The GitHub Action above already '
             f'delivers a standing audit at $0; what an engagement buys is the '
             f'implementation and your own private content, once.</p>'
             f'<div class="note">Do-it-yourself first: all of this is open source and '
             f'documented — the <a href="{gh}README.md#run-your-private-team-catalog" '
             f'style="color:var(--fc)">README covers the private-catalog build ↗</a>. '
             f'If your team can spare the setup time, you don’t need to pay anyone.</div>'
             f'</div></section>')

    ftr = foot("Bring the audit loop in-house",
               "One contact starts the conversation — public issue, and say "
               "the word if you'd rather talk privately.",
               f'<a class="btn btn-primary" href="{PARTNER_CTA_URL}">Ask about a team setup →</a>'
               '<a class="btn btn-ghost" href="/#catalog">Browse the catalog</a>')

    return page("Goal Prompts for Teams — private audit catalogs",
                f"A private audit pipeline from shipping parts: your own catalog "
                f"of linted briefs, slash-command distribution, and standing CI "
                f"audits. Flat-fee setup, pricing on request.",
                f"{BASE}/teams", hero + what + price + ftr,
                f"{BASE}/og.png")


def partners_page(playbooks: list) -> str:
    """R55 (REVENUE §4.3/§5): /partners — the rate-card structure. Formats
    and specs are real (the merchandising fields ship in playbooks.json and
    render today); the numbers are not, so audience metrics and pricing are
    "on request" — never invented. Same single contact as R52."""
    # the worked-example links come from the data, so they track playbooks.json
    ex = {pb["type"]: pb for pb in playbooks if pb.get("partner")}
    collab_key = ex["collab"]["key"]
    sponsored_key = ex["sponsored"]["key"]

    hero = (f'<section class="dhero"><div class="wrap">'
            f'<div class="crumb"><a href="/">Home</a><span class="sep">/</span>'
            f'<span>Partners</span></div>'
            f'<h1 style="margin-top:14px">Partner &amp; sponsored playbooks</h1>'
            f'<p class="lede">Playbooks are how this catalog is built to sustain itself: a '
            f'partner’s brand wraps a real, linted, useful sequence — always '
            f'disclosed, never ahead of the organic catalog. This page is the '
            f'rate-card structure; the numbers are on request while the project '
            f'is early.</p>'
            f'<div class="cta">'
            f'<a class="btn btn-primary" href="{PARTNER_CTA_URL}">Start a partnership →</a>'
            f'<a class="btn btn-ghost" href="/p/{collab_key}">See the collab template</a>'
            f'</div></div></section>')

    formats = (f'<section class="blk"><div class="wrap">'
               f'<div class="kicker">Formats</div>'
               f'<h2 class="h2">Three placement formats, all already rendered.</h2>'
               f'<p class="lead">Each format is live in the build today as a worked '
               f'example — what you see on the example pages is exactly what ships.</p>'
               f'<div class="rules" style="margin-top:18px"><h3>The inventory</h3><ul>'
               f'<li><b>Sponsored playbook.</b> A curated sequence your brand wraps — '
               f'logo, name, blurb, CTA — with the placement paid. Worked example: '
               f'<a href="/p/{sponsored_key}" style="color:var(--fc)">'
               f'{esc(ex["sponsored"]["name"])}</a>.</li>'
               f'<li><b>Collab playbook.</b> Co-branded with a tool or creator: the '
               f'content is shared and so is the revenue. Worked example: '
               f'<a href="/p/{collab_key}" style="color:var(--fc)">'
               f'{esc(ex["collab"]["name"])}</a>.</li>'
               f'<li><b>Themed drop.</b> A limited-run seasonal slot with a visible '
               f'window label (the catalog already runs its own — Ship-It Week, the '
               f'January reset). Calendar inventory, one partner per window.</li>'
               f'</ul></div></div></section>')

    specs = (f'<section class="blk"><div class="wrap">'
             f'<div class="kicker">Specs</div>'
             f'<h2 class="h2">What a placement includes.</h2>'
             f'<p class="lead">Every placement is a first-class playbook, not a banner: '
             f'its own detail page with your name, mark, blurb, and CTA; a storefront '
             f'card on the landing page; a one-paste conductor and raw endpoint; and an '
             f'OG share card. The merchandising fields are already live in '
             f'<code>playbooks.json</code> — <code>type</code>, <code>badge</code>, '
             f'<code>window</code>, <code>accent</code>, <code>partner</code>, '
             f'<code>tagline</code>, <code>featured</code> — so a real partner slots in '
             f'without new code.</p>'
             f'<div class="rules" style="margin-top:18px"><h3>Disclosure rules — non-negotiable</h3><ul>'
             f'<li>Every paid placement carries a visible <b>Sponsored</b> or '
             f'<b>Collab</b> badge, on the card and on its page.</li>'
             f'<li>Sponsored cards never displace organic playbooks in the featured '
             f'storefront grid.</li>'
             f'<li>No sponsor messaging in the copy-and-run flow — the surface users '
             f'trust stays clean.</li>'
             f'<li>The briefs themselves are never sponsored. Placement wraps a '
             f'sequence; every brief in it clears the same '
             f'<a href="/quality" style="color:var(--fc)">published linter</a> as the '
             f'rest of the catalog.</li>'
             f'</ul></div></div></section>')

    numbers = (f'<section class="blk"><div class="wrap">'
               f'<div class="kicker">Numbers</div>'
               f'<h2 class="h2">Audience and pricing: on request.</h2>'
               f'<p class="lead">The catalog is early and the numbers stay honest: '
               f'distribution metrics are shared on request as they come online, and '
               f'pricing is quoted per placement. No inflated reach claims — if a '
               f'number isn’t real, it isn’t on this page.</p>'
               f'<div class="note">Prefer to talk privately? Open the contact issue '
               f'and say so — it can stay a one-liner, and the maintainer will follow '
               f'up with you directly.</div>'
               f'</div></section>')

    ftr = foot("Wrap a sequence worth running",
               "The example placements show the whole shape, end to end — "
               "swap in a real partner to ship one.",
               f'<a class="btn btn-primary" href="{PARTNER_CTA_URL}">Start a partnership →</a>'
               '<a class="btn btn-ghost" href="/#playbooks">See the playbooks</a>')

    return page("Partner & sponsored playbooks — Goal Prompts",
                "Placement formats and specs for sponsored, collab, and themed "
                "playbooks: what each includes, the disclosure rules, and how "
                "to start — audience numbers and pricing on request.",
                f"{BASE}/partners", hero + formats + specs + numbers + ftr,
                f"{BASE}/og.png")


def command_md(p: dict) -> str:
    """One brief as a Claude Code command file — the same content ships in the
    tar/zip archives (curl installer) and the plugin's commands/ directory."""
    return f'---\ndescription: "{p["tagline"]}"\n---\n\n{p["body"]}\n'


def skill_md(p: dict) -> str:
    """One brief in the ecosystem's recommended SKILL.md packaging (R42,
    COMPETITIVE §3.2): YAML frontmatter (name + description) over the same
    body the plugin commands carry. The description names the deliverable so
    an agent picking skills by description knows what the run leaves behind.
    Taglines are linted double-quote-free, so the quoted YAML scalar is safe."""
    return (f'---\n'
            f'name: goal-{p["slug"]}\n'
            f'description: "{p["tagline"]} Audit brief {p["id"]} · '
            f'{p["family"]} — runs a four-phase audit of the current repo '
            f'and writes {p["output"]} at the repo root."\n'
            f'---\n\n{p["body"]}\n')


def write_skills(prompts: list) -> None:
    """The skills/ output tree (R42): one skills/goal-<slug>/SKILL.md per
    brief — same goal-<slug> naming as the plugin and archives. Copy any
    skill directory into .claude/skills/ (or a plugin's skills/) to use it.
    Fully regenerated like plugin/; CI's drift gate diffs the committed copy."""
    shutil.rmtree(ROOT / "skills", ignore_errors=True)
    for p in prompts:
        d = ROOT / "skills" / f'goal-{p["slug"]}'
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(skill_md(p), encoding="utf-8")


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
        # ACTIVATION AN5 (R15): name a concrete first command, so the install
        # moment doesn't land in 141 equal choices (mirrors install's outro).
        "description": "The goal-prompts audit catalog as native /goal:<slug> "
                       "commands — each brief points your agent at the repo "
                       "and writes one evidence-backed report. Start with "
                       "/goal:audit-triage (it names the audits your repo "
                       "needs) or /goal:bug-hunt.",
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
    # R44 (COMPETITIVE §3.4/§9): one extra native target, not five — Cursor's
    # project-commands format. Unzip at a repo root and every brief is a
    # /goal-<slug> command in Cursor (.cursor/commands/<name>.md, plain
    # markdown: the name comes from the filename, so no frontmatter).
    with zipfile.ZipFile(ROOT / "cursor-commands.zip", "w",
                         zipfile.ZIP_DEFLATED) as zf:
        for p in prompts:
            zi = zipfile.ZipInfo(f'.cursor/commands/goal-{p["slug"]}.md',
                                 date_time=(2026, 1, 1, 0, 0, 0))
            zi.external_attr = 0o644 << 16
            zf.writestr(zi, p["body"] + "\n")
    import hashlib
    lines = []
    for fname in ("commands.tar.gz", "commands.zip", "cursor-commands.zip"):
        digest = hashlib.sha256((ROOT / fname).read_bytes()).hexdigest()
        lines.append(f"{digest}  {fname}")
    (ROOT / "checksums.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def sitemap_lastmod(inputs: dict, state_path: Path = None) -> dict:
    """Deterministic sitemap <lastmod> dates (SEO-7, R30): path -> ISO date.

    The build clock can't be used (CI rebuilds and diffs — any timestamp would
    drift) and git file dates disagree between full and shallow clones (CI and
    Vercel check out depth-1), so dates persist in sitemap-lastmod.json keyed
    by a hash of each URL's content sources. A date moves to "today" only when
    that page's content actually changed; an unchanged rebuild is
    byte-identical. The state file is build-maintained — commit it with the
    other outputs, never hand-edit it."""
    import hashlib
    state_path = state_path or (ROOT / "sitemap-lastmod.json")
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    today = datetime.date.today().isoformat()
    dates, new_state = {}, {}
    for path, blob in inputs.items():
        h = hashlib.sha1(blob).hexdigest()[:16]
        prev = state.get(path)
        d = prev["d"] if isinstance(prev, dict) and prev.get("h") == h else today
        dates[path] = d
        new_state[path] = {"h": h, "d": d}
    if new_state != state:
        state_path.write_text(
            json.dumps(new_state, sort_keys=True, indent=1) + "\n",
            encoding="utf-8")
    return dates


def main() -> None:
    files = sorted((ROOT / "prompts").rglob("*.md"))
    if not files:
        fail("no prompt files found under prompts/")
    prompts = [parse(f) for f in files]
    # source path per brief — feeds the sitemap's content-keyed <lastmod>
    src_of = {p["id"]: f for p, f in zip(prompts, files)}
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

    # ---- OG drift guards: the home card bakes "N briefs" in as pixels and
    # each playbook card bakes its stage count, so scripts/og.py embeds the
    # counts as PNG metadata and the build (stdlib only — no Pillow) reads
    # them back and compares to the live catalog ----
    og_n = png_text(ROOT / "og.png", "gp-briefs")
    if og_n is None:
        fail("og.png has no gp-briefs metadata — regenerate with "
             "scripts/og.py --home")
    if int(og_n) != len(prompts):
        fail(f"og.png's baked-in count is {og_n} briefs but the catalog has "
             f"{len(prompts)} — regenerate with scripts/og.py --home (needs Pillow)")
    pb_og = playbook_og_violations(playbooks, ROOT / "og")
    if pb_og:
        fail("; ".join(pb_og))

    # ---- shared design tokens (single source of truth, linked by every page) ----
    (ROOT / "tokens.css").write_text(TOKENS_CSS, encoding="utf-8")

    # ---- injected site ----
    # R29 (SEO-2): metadata only — no bodies. The catalog UI fetches
    # /bodies.json at copy/quick-view time (SW-precached, so offline
    # copies survive); the lens count the card meta line used to derive
    # from the body ships precomputed instead.
    prompt_payload = [{**{k: p[k] for k in
                          ("id", "title", "family", "question", "output",
                           "tagline", "chars")},
                       "lenses": len(brief_parts(p["body"])["lenses"]),
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
                  "__N_BRIEFS__", "__N_PLAYBOOKS__", "__N_FAMILIES__",
                  "__GH_STARS__", "__GH_STARS_HERO__", "__STATIC_CATALOG__",
                  "__STATIC_PB_FEATURED__", "__STATIC_PB_MORE__",
                  "__BACKER_URL__"):
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
    # One badge, two placements: the footer buildnote and \u2014 PROOF NF7 (R25) \u2014
    # the hero micro-line next to "free & open". Same threshold, same
    # dark-below-it discipline; never a fake or deflating number.
    gh_stars = (f' \u00b7 <a href="https://github.com/GhostlyGawd/goal-prompts/stargazers">'
                f'{stars:,} stars on GitHub</a>') if stars >= STAR_THRESHOLD else ""
    # counts injected from source-of-truth so the static meta/OG tags and the
    # no-JS hero/chart fallbacks can never drift from the catalog again
    # R28 (SEO-1): the static, crawlable catalog + storefront — same source
    # of truth as the JSON payloads; the inline script replaces them on boot
    pb_feat_html, pb_more_html = static_playbooks(playbooks, by_id)
    index_html = (template.replace("__PROMPTS_JSON__", esc(prompt_payload))
                          .replace("__PLAYBOOKS_JSON__", esc(pb_payload))
                          .replace("__FAMILIES_JSON__", esc(fam_payload))
                          .replace("__STATIC_CATALOG__", static_catalog(prompts))
                          .replace("__STATIC_PB_FEATURED__", pb_feat_html)
                          .replace("__STATIC_PB_MORE__", pb_more_html)
                          .replace("__N_BRIEFS__", str(len(prompts)))
                          .replace("__N_PLAYBOOKS__", str(len(playbooks)))
                          .replace("__N_FAMILIES__", str(len(fam_payload)))
                          .replace("__GH_STARS_HERO__", gh_stars)
                          .replace("__GH_STARS__", gh_stars)
                          # R56: dormant backer nudge — empty BACKER_URL
                          # (R53 is external) keeps the whole feature inert
                          .replace("__BACKER_URL__", BACKER_URL))
    (ROOT / "index.html").write_text(index_html, encoding="utf-8")

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

    # ---- /changelog (R36, RETENTION R10): the freshness pull for installed
    # surfaces — MCP footers and the installer's outro point here ----
    changelog_md = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    (ROOT / "changelog.html").write_text(changelog_page(changelog_md),
                                         encoding="utf-8")

    # ---- /quality (R50): the published quality bar — "why these briefs
    # don't rot", linked from the loop copy and every footer ----
    quality_html = quality_page(prompts)
    (ROOT / "quality.html").write_text(quality_html, encoding="utf-8")

    # ---- /teams + /partners (R55): the revenue rails — the offer page and
    # the rate-card structure; pricing/audience numbers stay "on request" ----
    teams_html = teams_page(prompts)
    (ROOT / "teams.html").write_text(teams_html, encoding="utf-8")
    partners_html = partners_page(playbooks)
    (ROOT / "partners.html").write_text(partners_html, encoding="utf-8")

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

    # ---- bodies.json (R29, SEO-2): every brief body in one fetchable blob.
    # The landing page loads it lazily at copy/quick-view time instead of
    # inlining 141 bodies into index.html; the service worker precaches it so
    # offline copies keep working. raw/<id>.md stays the agents' network-only
    # endpoint (its fetch counts are the usage metric — docs/usage-metrics.md),
    # so browser copies never pollute that signal. ----
    (ROOT / "bodies.json").write_text(
        json.dumps({p["id"]: p["body"] for p in prompts},
                   ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8")

    # ---- service worker (offline shell; version stamped from content) ----
    import hashlib as _hl
    # bodies.json rides the version hash: index.html no longer changes when a
    # brief body does, so without it a body edit would never bust the cache
    ver_src = b"".join((ROOT / f).read_bytes() for f in
                       ("index.html", "studio.html", "vitals.html", "tokens.css",
                        "bodies.json",
                        "js/catalog-core.js", "js/report-parser.js", "js/gp-detail.js",
                        "icons/icon-192.png", "icons/icon-512.png"))
    sw_ver = _hl.sha256(ver_src).hexdigest()[:12]
    precache = ["/", "/studio", "/vitals", "/examples/", "/manifest.json",
                "/tokens.css", "/bodies.json",
                "/js/catalog-core.js", "/js/report-parser.js", "/js/gp-detail.js",
                "/fonts/schibstedgrotesk-latin-var.woff2", "/fonts/plexsans-latin-400.woff2", "/fonts/plexsans-latin-600.woff2", "/fonts/plexmono-latin-400.woff2",
                "/fonts/plexmono-latin-600.woff2",
                "/icons/icon-192.png", "/icons/icon-512.png"]
    (ROOT / "sw.js").write_text(SERVICE_WORKER
                                .replace("__VERSION__", sw_ver)
                                .replace("__PRECACHE__", json.dumps(precache)),
                                encoding="utf-8")

    # ---- sitemap + robots (crawlers can't guess 68 share pages) ----
    # SEO-7 (R30): each URL's <lastmod> is keyed to its content sources via
    # sitemap-lastmod.json (see sitemap_lastmod) — a freshness signal that
    # moves only when the page's content does, and stays build-deterministic.
    blobs = {"/": index_html.encode("utf-8"),
             "/studio": (ROOT / "studio.html").read_bytes(),
             "/vitals": (ROOT / "vitals.html").read_bytes(),
             "/examples/": (ROOT / "examples" / "index.html").read_bytes(),
             "/changelog": changelog_md.encode("utf-8"),
             "/quality": quality_html.encode("utf-8"),
             "/teams": teams_html.encode("utf-8"),
             "/partners": partners_html.encode("utf-8")}
    for pb in playbooks:
        # the page renders the entry (incl. conductor) + its members' card copy
        members = [{k: by_id[i][k] for k in
                    ("id", "title", "tagline", "output", "family")}
                   for i in pb["ids"]]
        blobs[f"/p/{pb['key']}"] = json.dumps(
            [pb, members], sort_keys=True, ensure_ascii=False).encode("utf-8")
    for p in prompts:
        blobs[f"/b/{p['id']}"] = src_of[p["id"]].read_bytes()
    lastmod = sitemap_lastmod(blobs)
    paths = ["/", "/studio", "/vitals", "/examples/", "/changelog", "/quality",
             "/teams", "/partners"]
    paths += [f"/p/{pb['key']}" for pb in playbooks]
    paths += [f"/b/{p['id']}" for p in prompts]
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "".join(f"  <url><loc>{BASE}{u}</loc>"
                         f"<lastmod>{lastmod[u]}</lastmod></url>\n"
                         for u in paths)
               + "</urlset>\n")
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")

    write_archives(prompts)
    write_plugin(prompts)
    write_skills(prompts)
    print(f"\nOK  {len(prompts)} briefs, {len(playbooks)} playbooks -> "
          f"index.html ({(ROOT / 'index.html').stat().st_size:,} b), "
          f"raw/, b/, catalog.json, bodies.json, sitemap.xml, robots.txt, "
          f"commands.tar.gz, commands.zip, cursor-commands.zip, plugin/, "
          f"skills/")


if __name__ == "__main__":
    main()
