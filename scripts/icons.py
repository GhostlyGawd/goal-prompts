#!/usr/bin/env python3
"""Generate the PWA icons (icons/icon-192.png, icon-512.png) from the bar mark.

The 4-bar equalizer logo — same geometry as build.BRAND_MARK and the favicon —
drawn on the dark rounded square, so the installed-app / home-screen icon stays
in step with the header logo and the browser tab.

Usage:  python3 scripts/icons.py     # writes both sizes
Needs Pillow.
"""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
INK = "#15120D"
# bars: (x, y, w, h) in the logo's 24-unit viewBox; shared corner radius RX
# Ledger identity: three paper bars + the tallest flagged in vermilion
# (specs/design-direction.md) — keep in step with build.BRAND_MARK/FAVICON.
BARS = [
    (1.0, 9.0, 3.4, 9.0, "#F0EADC"),
    (6.9, 3.0, 3.4, 15.0, "#FF6B47"),
    (12.8, 7.0, 3.4, 11.0, "#F0EADC"),
    (18.7, 12.0, 3.4, 6.0, "#F0EADC"),
]
RX = 0.8
# favicon composition: translate(10, 9.2) scale(1.9) inside a 64-unit square
TX, TY, SC, VB = 10.0, 9.2, 1.9, 64.0
BG_RADIUS = 6.0  # in 64-space, matches the favicon's rounded square


def render(size):
    ss = 4  # supersample, then downscale for smooth edges
    s = size * ss
    k = s / VB
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=BG_RADIUS * k, fill=INK)
    for x, y, w, h, color in BARS:
        x0, y0 = (x * SC + TX) * k, (y * SC + TY) * k
        x1, y1 = ((x + w) * SC + TX) * k, ((y + h) * SC + TY) * k
        d.rounded_rectangle([x0, y0, x1, y1], radius=RX * SC * k, fill=color)
    return im.resize((size, size), Image.LANCZOS)


def main():
    for size in (192, 512):
        out = ROOT / "icons" / f"icon-{size}.png"
        render(size).save(out, optimize=True)
        print(f"icons/icon-{size}.png")


if __name__ == "__main__":
    main()
