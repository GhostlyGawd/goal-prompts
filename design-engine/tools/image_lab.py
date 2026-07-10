#!/usr/bin/env python3
"""image_lab — the engine's image workhorse. Pillow; generate-time.

Turns reference/board/generated imagery into brand assets. This is the tool
that closes the "stick figures vs Mona Lisas" gap: instead of hand-drawing
primitives, take the board's own pixels (or any supplied illustration) and
re-ink them into the brand system.

    python3 design-engine/tools/image_lab.py CMD IN [options] --out OUT

Commands
  sample IN [--k 8]                     k-means palette from an image → hex list
  map IN --palette "#hex,#hex,…" [--levels N] [--boost B]
                                        re-ink every pixel onto the palette
                                        (posterize first with --levels; B>1
                                        saturates before mapping)
  duotone IN --dark "#hex" --light "#hex" [--mid "#hex"]
                                        luminance → 2–3 color ramp
  halftone IN --color "#hex" --bg "#hex" [--cell 6]
                                        classic print dot screen
  grain IN [--amount 12]                film/paper grain overlay
  outline IN [--color "#hex"] [--threshold 90]
                                        ink edge pass (composite over map/duotone
                                        output for the printed-illustration look)
  crop IN --box X,Y,W,H                 crop
  resize IN --width W                   proportional resize
  composite BASE --over TOP --at X,Y [--scale S]
                                        paste one image over another (build new
                                        compositions from board pieces)

No host facts in code: palettes always come from arguments (callers read them
from brand.json or a board.json). Deterministic given inputs.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import enginelib as lib  # noqa: E402


def _pil():
    try:
        from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
        return Image, ImageDraw, ImageEnhance, ImageFilter
    except ImportError:
        print("SKIP  Pillow not installed — image_lab is generate-time "
              "(pip install pillow)", file=sys.stderr)
        raise SystemExit(1)


def _hexes(s):
    return [h.strip() for h in s.split(",") if h.strip()]


# ---- palette sampling (pure-python k-means on a thumbnail) -------------------

def sample(img, k=8, iterations=12, seed=4):
    """Dominant colors as hex, by cluster size. Deterministic (fixed seed)."""
    Image = _pil()[0]
    im = img.convert("RGB")
    im.thumbnail((96, 96))
    px = list(im.getdata())
    import random
    rng = random.Random(seed)
    centers = [px[rng.randrange(len(px))] for _ in range(k)]
    for _ in range(iterations):
        buckets = [[] for _ in range(k)]
        for p in px:
            best = min(range(k), key=lambda i: _d2(p, centers[i]))
            buckets[best].append(p)
        for i, b in enumerate(buckets):
            if b:
                centers[i] = tuple(sum(c[j] for c in b) // len(b) for j in range(3))
    sized = sorted(((len(b), c) for b, c in zip(buckets, centers)), reverse=True)
    return ["#%02X%02X%02X" % c for n, c in sized if n]


def _d2(a, b):
    # perceptual-ish weighted RGB distance
    dr, dg, db = a[0] - b[0], a[1] - b[1], a[2] - b[2]
    return 3 * dr * dr + 4 * dg * dg + 2 * db * db


# ---- re-inking ---------------------------------------------------------------

def palette_map(img, palette, levels=0, boost=1.0):
    """Replace every pixel with its nearest palette color — the screen-print
    re-ink. Posterizing first (levels) flattens gradients into printable shapes."""
    Image, _, ImageEnhance, _ = _pil()
    im = img.convert("RGB")
    if boost != 1.0:
        im = ImageEnhance.Color(im).enhance(boost)
    if levels:
        from PIL import ImageOps
        im = ImageOps.posterize(im, max(1, min(8, levels)))
    pal = [lib.hex_rgb(h) for h in palette]
    # Pillow's quantize with a fixed palette does the nearest-color mapping in C
    palim = Image.new("P", (1, 1))
    flat = []
    for c in pal:
        flat += list(c)
    flat += pal[0] and list(pal[0]) * (256 - len(pal))
    palim.putpalette(flat[:768])
    return im.quantize(palette=palim, dither=Image.Dither.NONE).convert("RGB")


def duotone(img, dark, light, mid=None):
    Image = _pil()[0]
    g = img.convert("L")
    d, l = lib.hex_rgb(dark), lib.hex_rgb(light)
    stops = [(0, d), (255, l)] if not mid else [(0, d), (128, lib.hex_rgb(mid)), (255, l)]
    lut = []
    for ch in range(3):
        for v in range(256):
            for (x0, c0), (x1, c1) in zip(stops, stops[1:]):
                if v <= x1:
                    t = (v - x0) / (x1 - x0)
                    lut.append(round(c0[ch] + t * (c1[ch] - c0[ch])))
                    break
            else:
                lut.append(stops[-1][1][ch])
    return Image.merge("RGB", [g.point(lut[i * 256:(i + 1) * 256]) for i in range(3)])


def halftone(img, color, bg, cell=6):
    Image, ImageDraw, _, _ = _pil()
    g = img.convert("L")
    w, h = g.size
    out = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(out)
    fg = lib.hex_rgb(color)
    for y in range(0, h, cell):
        for x in range(0, w, cell):
            box = g.crop((x, y, min(x + cell, w), min(y + cell, h)))
            lum = sum(box.getdata()) / max(1, box.width * box.height)
            r = (1 - lum / 255) * cell * 0.62
            if r > 0.4:
                cx, cy = x + cell / 2, y + cell / 2
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fg)
    return out


def grain(img, amount=12, seed=7):
    Image = _pil()[0]
    import random
    rng = random.Random(seed)
    im = img.convert("RGB")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            n = rng.randint(-amount, amount)
            r, g, b = px[x, y]
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)),
                        max(0, min(255, b + n)))
    return im


def outline(img, color="#1D1F28", threshold=90):
    """Ink-line pass: edges as a transparent overlay (composite over a re-inked
    base for the printed-illustration look)."""
    Image, _, _, ImageFilter = _pil()
    edges = img.convert("L").filter(ImageFilter.FIND_EDGES).point(
        lambda v: 255 if v > threshold else 0)
    ink = Image.new("RGBA", img.size, (*lib.hex_rgb(color), 255))
    ink.putalpha(edges.filter(ImageFilter.MaxFilter(3)).point(lambda v: v * 200 // 255))
    return ink


def main(argv):
    Image = _pil()[0]
    args = list(argv)
    if len(args) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    cmd, inp = args[0], Path(args[1])
    rest = args[2:]

    def opt(name, default=None):
        if name in rest:
            i = rest.index(name)
            return rest[i + 1]
        return default

    img = Image.open(inp)
    out = opt("--out")

    if cmd == "sample":
        for h in sample(img, k=int(opt("--k", 8))):
            print(h)
        return 0
    if cmd == "map":
        res = palette_map(img, _hexes(opt("--palette")),
                          levels=int(opt("--levels", 0)), boost=float(opt("--boost", 1.0)))
    elif cmd == "duotone":
        res = duotone(img, opt("--dark"), opt("--light"), opt("--mid"))
    elif cmd == "halftone":
        res = halftone(img, opt("--color"), opt("--bg"), cell=int(opt("--cell", 6)))
    elif cmd == "grain":
        res = grain(img, amount=int(opt("--amount", 12)))
    elif cmd == "outline":
        base = img.convert("RGBA")
        base.alpha_composite(outline(img, opt("--color", "#1D1F28"),
                                     int(opt("--threshold", 90))))
        res = base.convert("RGB")
    elif cmd == "crop":
        x, y, w, h = (int(v) for v in opt("--box").split(","))
        res = img.crop((x, y, x + w, y + h))
    elif cmd == "resize":
        w = int(opt("--width"))
        res = img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)
    elif cmd == "composite":
        top = Image.open(opt("--over")).convert("RGBA")
        s = float(opt("--scale", 1.0))
        if s != 1.0:
            top = top.resize((round(top.width * s), round(top.height * s)), Image.LANCZOS)
        x, y = (int(v) for v in opt("--at").split(","))
        res = img.convert("RGBA")
        res.alpha_composite(top, (x, y))
        res = res.convert("RGB")
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        return 2
    if not out:
        print("--out required", file=sys.stderr)
        return 2
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    res.save(out)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
