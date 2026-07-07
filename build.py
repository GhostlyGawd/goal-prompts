#!/usr/bin/env python3
"""Build the Goal Prompts site + machine-readable surfaces from prompts/**/*.md.

Outputs (all committed, all deterministic, stdlib only — this also runs on Vercel):
  index.html            the catalog UI (prompts + playbooks injected into template.html)
  raw/<id>.md           brief bodies at stable URLs, for agents to fetch
  raw/playbook-<key>.md conductor prompts that run a whole playbook
  b/<id>.html           per-brief pages with their own OG tags (unfurl + redirect)
  catalog.json          machine-readable index (consumed by the MCP server)
  commands.tar.gz/.zip  Claude Code slash commands, used by /install

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
FAMILY_ORDER = ["Venture", "Product", "Quality", "Speed", "Trust", "Growth", "Team",
                "Clarity", "Design", "Data", "Ops", "Subtract", "Meta", "Act",
                "Agent", "Automation", "AI-UX"]
REQUIRED = ["id", "title", "family", "question", "output", "tagline"]


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
    if meta["family"] not in FAMILY_ORDER:
        fail(f"{path}: unknown family '{meta['family']}'")
    if '"' in meta["tagline"]:
        fail(f"{path}: tagline may not contain double quotes")
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
    if p["chars"] > LIMIT:
        v.append(f"body is {p['chars']} chars (max {LIMIT})")
    if p.get("example") and not p["example"].startswith("/"):
        v.append(f"example '{p['example']}' must be a root-relative path like /BUGS.md")
    return v


def conductor(pb: dict, by_id: dict) -> str:
    """A meta-prompt that runs every brief in a playbook, in order."""
    stages = []
    for n, pid in enumerate(pb["ids"], 1):
        p = by_id[pid]
        stages.append(f"{n}. **{pid} · {p['title']}** — fetch {BASE}/raw/{pid}.md"
                      f" → writes `{p['output']}`")
    plural = "briefs" if len(pb["ids"]) > 1 else "brief"
    return f"""# Playbook: {pb['name']} (conductor)

You are working inside this repo. Mission: execute the **{pb['name']}** playbook — {len(pb['ids'])} audit {plural} in sequence, each producing one report file at this repo's root.

{pb['desc']}

## How to run each stage, in order
1. Fetch the brief with a read-only web request (for example: curl -s <url>).
2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.
3. Confirm the report file exists at repo root before moving on.
4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.

## Stages
{chr(10).join(stages)}

## After the final stage
- List every report created, with a one-line takeaway each.
- Suggest the natural next step: fetch {BASE}/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.

## Rules
- If a fetch fails, say so and stop — never improvise a brief from memory.
- Honor each brief's own rules, including ending by asking before any changes.
- If a stage's report already exists, ask whether to re-run or skip that stage.
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
"""


BRIEF_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>__ID__ · __TITLE__ — Goal Prompts</title>
<meta name="description" content="__TAGLINE__">
<meta property="og:title" content="__ID__ · __TITLE__ — Goal Prompts">
<meta property="og:description" content="__TAGLINE__">
<meta property="og:image" content="__BASE__/og/__ID__.png">
<meta property="og:url" content="__BASE__/b/__ID__">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="__BASE__/og/__ID__.png">
<meta http-equiv="refresh" content="0;url=/#__ID__">
<link rel="canonical" href="__BASE__/#__ID__">
</head>
<body style="background:#14181E;color:#8B96A5;font-family:monospace;padding:40px">
<p>__ID__ · __TITLE__ — <a style="color:#E8B44C" href="/#__ID__">open in the catalog →</a></p>
</body>
</html>
"""


def brief_page(p: dict) -> str:
    out = BRIEF_PAGE
    for k, v in (("__ID__", p["id"]), ("__TITLE__", p["title"]),
                 ("__TAGLINE__", p["tagline"].replace('"', "'")),
                 ("__BASE__", BASE)):
        out = out.replace(k, v)
    return out


def write_archives(prompts: list) -> None:
    entries = []
    for p in prompts:
        content = (f'---\ndescription: "{p["tagline"]}"\n---\n\n'
                   f'{p["body"]}\n').encode("utf-8")
        entries.append((f'goal/{p["slug"]}.md', content))
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
    prompts.sort(key=lambda p: (FAMILY_ORDER.index(p["family"]), p["id"]))
    by_id = {p["id"]: p for p in prompts}

    ids = [p["id"] for p in prompts]
    if len(ids) != len(set(ids)):
        fail("duplicate prompt ids")
    if len({p["slug"] for p in prompts}) != len(prompts):
        fail("duplicate prompt slugs")

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

    # ---- injected site ----
    prompt_payload = [{**{k: p[k] for k in
                          ("id", "title", "family", "question", "output",
                           "tagline", "body", "chars")},
                       **({"example": BASE + p["example"]} if p.get("example") else {})}
                      for p in prompts]
    pb_payload = [{k: pb[k] for k in ("key", "name", "desc", "ids", "conductor")}
                  for pb in playbooks]
    fam_payload = [[fam, next(p["question"] for p in prompts if p["family"] == fam)]
                   for fam in FAMILY_ORDER
                   if any(p["family"] == fam for p in prompts)]
    template = (ROOT / "template.html").read_text(encoding="utf-8")
    if BASE != DEFAULT_BASE:
        template = template.replace(DEFAULT_BASE, BASE)
    for token in ("__PROMPTS_JSON__", "__PLAYBOOKS_JSON__", "__FAMILIES_JSON__"):
        if token not in template:
            fail(f"template.html missing {token} placeholder")
    esc = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
    (ROOT / "index.html").write_text(
        template.replace("__PROMPTS_JSON__", esc(prompt_payload))
                .replace("__PLAYBOOKS_JSON__", esc(pb_payload))
                .replace("__FAMILIES_JSON__", esc(fam_payload)),
        encoding="utf-8")

    # ---- raw endpoints + brief pages ----
    for d in ("raw", "b"):
        shutil.rmtree(ROOT / d, ignore_errors=True)
        (ROOT / d).mkdir()
    for p in prompts:
        (ROOT / "raw" / f'{p["id"]}.md').write_text(p["body"] + "\n", encoding="utf-8")
        (ROOT / "b" / f'{p["id"]}.html').write_text(brief_page(p), encoding="utf-8")
    for pb in playbooks:
        (ROOT / "raw" / f'playbook-{pb["key"]}.md').write_text(
            pb["conductor"], encoding="utf-8")

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
        "playbooks": [{k: pb[k] for k in ("key", "name", "desc", "ids")}
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
                       ("index.html", "studio.html", "vitals.html"))
    sw_ver = _hl.sha256(ver_src).hexdigest()[:12]
    precache = ["/", "/studio", "/vitals", "/examples/", "/manifest.json",
                "/fonts/archivo-latin-var.woff2", "/fonts/plexmono-latin-400.woff2",
                "/fonts/plexmono-latin-500.woff2", "/fonts/plexmono-latin-600.woff2",
                "/icons/icon-192.png", "/icons/icon-512.png"]
    (ROOT / "sw.js").write_text(SERVICE_WORKER
                                .replace("__VERSION__", sw_ver)
                                .replace("__PRECACHE__", json.dumps(precache)),
                                encoding="utf-8")

    # ---- sitemap + robots (crawlers can't guess 68 share pages) ----
    urls = [f"{BASE}/", f"{BASE}/studio", f"{BASE}/vitals", f"{BASE}/examples/"]
    urls += [f"{BASE}/b/{p['id']}" for p in prompts]
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
               + "</urlset>\n")
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")

    write_archives(prompts)
    print(f"\nOK  {len(prompts)} briefs, {len(playbooks)} playbooks -> "
          f"index.html ({(ROOT / 'index.html').stat().st_size:,} b), "
          f"raw/, b/, catalog.json, sitemap.xml, robots.txt, "
          f"commands.tar.gz, commands.zip")


if __name__ == "__main__":
    main()
