#!/usr/bin/env python3
"""Generate the PWA icons (icons/icon-192.png, icon-512.png) from the bar mark.

The mark's geometry lives in design-engine/brand.json (`mark`) — the same
single source build.BRAND_MARK and the favicon render from — and
design-engine/tools/mark_render.py does the drawing, so the installed-app /
home-screen icon can never drift from the header logo or the browser tab.

Usage:  python3 scripts/icons.py     # writes both sizes
Needs Pillow (generate-time tool, like scripts/og.py).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "design-engine" / "tools"))
import enginelib as lib  # noqa: E402
import mark_render  # noqa: E402


def main():
    mark = lib.load_brand()["mark"]
    for size in (192, 512):
        out = ROOT / "icons" / f"icon-{size}.png"
        mark_render.png(mark, size).save(out, optimize=True)
        print(f"icons/icon-{size}.png")


if __name__ == "__main__":
    main()
