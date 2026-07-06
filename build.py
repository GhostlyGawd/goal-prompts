#!/usr/bin/env python3
"""Build the Goal Prompts site + command archives from prompts/**/*.md.

Outputs (all committed, all deterministic):
  index.html        the catalog UI (prompts injected into template.html)
  commands.tar.gz   Claude Code slash commands, used by the /install script
  commands.zip      same content, for manual download

Each prompt file: front matter between two '---' lines, then the prompt body.
The body (what the Copy button copies) must be under 4,000 characters —
the build fails otherwise.
"""
import gzip, io, json, re, sys, tarfile, zipfile
from pathlib import Path

ROOT = Path(__file__).parent
LIMIT = 4000
FAMILY_ORDER = ["Product", "Quality", "Speed", "Trust", "Growth", "Team",
                "Clarity", "Data", "Ops", "Subtract", "Meta",
                "Agent", "Automation", "AI-UX"]
REQUIRED = ["id", "title", "family", "question", "output", "tagline"]


def parse(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3 or parts[0].strip():
        sys.exit(f"FAIL {path}: missing front matter block")
    meta = {}
    for line in parts[1].strip().splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"')
    for k in REQUIRED:
        if not meta.get(k):
            sys.exit(f"FAIL {path}: front matter missing '{k}'")
    if meta["family"] not in FAMILY_ORDER:
        sys.exit(f"FAIL {path}: unknown family '{meta['family']}'")
    if '"' in meta["tagline"]:
        sys.exit(f"FAIL {path}: tagline may not contain double quotes")
    meta["body"] = parts[2].strip()
    meta["chars"] = len(meta["body"])
    meta["slug"] = re.sub(r"^\d+-", "", path.stem)
    return meta


def write_archives(prompts: list) -> None:
    """Claude Code slash commands: .claude/commands/goal/<slug>.md
    Fixed mtimes keep both archives byte-identical across rebuilds,
    so CI can catch drift with a plain git diff."""
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


def main() -> None:
    files = sorted((ROOT / "prompts").rglob("*.md"))
    if not files:
        sys.exit("FAIL: no prompt files found under prompts/")
    prompts = [parse(f) for f in files]
    prompts.sort(key=lambda p: (FAMILY_ORDER.index(p["family"]), p["id"]))

    ids = [p["id"] for p in prompts]
    if len(ids) != len(set(ids)):
        sys.exit("FAIL: duplicate prompt ids")
    slugs = [p["slug"] for p in prompts]
    if len(slugs) != len(set(slugs)):
        sys.exit("FAIL: duplicate prompt slugs")

    over = [p for p in prompts if p["chars"] > LIMIT]
    width = max(len(p["title"]) for p in prompts)
    for p in prompts:
        flag = "  OVER 4K!" if p["chars"] > LIMIT else ""
        print(f'{p["id"]}  {p["title"]:<{width}}  {p["family"]:<8}'
              f'  {p["chars"]:>4} chars  -> /goal:{p["slug"]}{flag}')
    if over:
        sys.exit(f"\nFAIL: {len(over)} prompt body(ies) exceed {LIMIT} chars")

    payload = [{k: p[k] for k in
                ("id", "title", "family", "question", "output", "tagline",
                 "body", "chars")} for p in prompts]
    js = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    js = js.replace("</", "<\\/")

    template = (ROOT / "template.html").read_text(encoding="utf-8")
    if "__PROMPTS_JSON__" not in template:
        sys.exit("FAIL: template.html missing __PROMPTS_JSON__ placeholder")
    (ROOT / "index.html").write_text(
        template.replace("__PROMPTS_JSON__", js), encoding="utf-8")

    write_archives(prompts)

    print(f"\nOK  {len(prompts)} prompts -> index.html "
          f"({(ROOT / 'index.html').stat().st_size:,} b), "
          f"commands.tar.gz, commands.zip")


if __name__ == "__main__":
    main()
