#!/usr/bin/env python3
"""css_hex_lint — forbid raw colors outside the token layer. Stdlib only.

Scans the files named in brand.json host.hex_lint.files for hex colors and
rgb()/rgba()/hsl() literals inside <style> blocks and style="" attributes.
Anything not covered by the allowlist is a violation: components must consume
var(--…) so the palette has exactly one source of truth (brand.json).

Not wired into the host gate until the surfaces are var-clean (the rebrand's
Phase 4); until then run it by hand to watch the count fall:

    python3 design-engine/tools/css_hex_lint.py [--brand path] [--list] [files...]

Allowlist entries (host.hex_lint.allow) are regexes matched against the
offending line — use sparingly, each one is a documented exception.
Exit 0 clean, 1 with one line per violation.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import enginelib as lib

HEX = re.compile(r"#[0-9A-Fa-f]{3,8}\b")
FUNC = re.compile(r"\b(?:rgba?|hsla?)\(")
STYLE_BLOCK = re.compile(r"<style[^>]*>([\s\S]*?)</style>", re.I)
STYLE_ATTR = re.compile(r'style="([^"]*)"')


def _spans(text: str):
    """Yield (offset, css_text) for every <style> block and style= attribute.
    Whole-file CSS (a .css input) is one span."""
    found = False
    for m in STYLE_BLOCK.finditer(text):
        found = True
        yield m.start(1), m.group(1)
    for m in STYLE_ATTR.finditer(text):
        found = True
        yield m.start(1), m.group(1)
    if not found and "<" not in text[:200]:
        yield 0, text


def scan_file(path: Path, allow):
    text = path.read_text(encoding="utf-8")
    line_of = lambda off: text.count("\n", 0, off) + 1
    hits = []
    for off, css in _spans(text):
        for pat in (HEX, FUNC):
            for m in pat.finditer(css):
                lineno = line_of(off + m.start())
                line = text.splitlines()[lineno - 1].strip()
                if any(re.search(a, line) for a in allow):
                    continue
                hits.append((path.name, lineno, m.group(0), line[:100]))
    return hits


def main(argv):
    brand_arg, list_only, files = None, False, []
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--brand":
            brand_arg = args.pop(0)
        elif a == "--list":
            list_only = True
        else:
            files.append(a)
    brand = lib.load_brand(brand_arg)
    cfg = brand["host"].get("hex_lint", {})
    targets = [Path(f) for f in files] or [lib.HOST_ROOT / f for f in cfg.get("files", [])]
    allow = cfg.get("allow", [])
    all_hits = []
    for t in targets:
        if not t.exists():
            print(f"FAIL  no such file: {t}", file=sys.stderr)
            return 1
        all_hits += scan_file(t, allow)
    if all_hits:
        stream = sys.stdout if list_only else sys.stderr
        print(f"{'' if list_only else 'FAIL  '}{len(all_hits)} raw color(s) outside the token layer:",
              file=stream)
        for fname, lineno, tok, line in all_hits:
            print(f"  {fname}:{lineno}  {tok}  | {line}", file=stream)
        return 0 if list_only else 1
    print(f"OK  no raw colors in {len(targets)} file(s) — everything consumes var(--…)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
