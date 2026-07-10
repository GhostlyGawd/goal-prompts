#!/usr/bin/env python3
"""mark_render — the one implementation of the brand mark's geometry.

brand.json's `mark` block is the single definition; this renders it as:
  svg(mark)               inline SVG for page headers (build.BRAND_MARK)
  favicon_data_uri(mark)  the data: URI favicon (build.FAVICON)
  png(mark, size)         a rasterized app icon (scripts/icons.py; needs Pillow)

CLI:  python3 design-engine/tools/mark_render.py [--brand path] [--png SIZE OUT]
With no args it prints the SVG and favicon URI (eyeball check). Stdlib except
png(), which imports Pillow lazily — generate-time only.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import enginelib as lib

n = lib.fmt_num


def _color(v, theme):
    """Element colors are a CSS color string (hex, currentColor, var(--x,...))
    or a {theme: color} map (theme-aware marks)."""
    if isinstance(v, dict):
        return v.get(theme) or next(iter(v.values()))
    return v


def _paint(e, key, theme, solid):
    """An element's paint for a context: inline SVG uses `key` (fill/stroke,
    which may be a CSS keyword or var()); standalone contexts — the favicon
    and rasterized icons, where no page CSS exists — prefer the element's
    `solid` hex when one is declared."""
    if solid and "solid" in e:
        return _color(e["solid"], theme)
    return _color(e[key], theme)


def _arch_d(e, closed):
    """Round-top arch path: legs at x0/x1 down to bot, semicircular top at `top`."""
    x0, x1, top = e["x0"], e["x1"], e["top"]
    bot = e.get("bot", 22)
    r = (x1 - x0) / 2
    d = (f"M{n(x0)} {n(bot)} V{n(top + r)} "
         f"A{n(r)} {n(r)} 0 0 1 {n(x1)} {n(top + r)} V{n(bot)}")
    return d + " Z" if closed else d


def _element_svg(e, theme, quote='"', solid=False):
    q = quote
    t = e["type"]
    if t == "rect":
        return (f"<rect x={q}{n(e['x'])}{q} y={q}{n(e['y'])}{q} width={q}{n(e['w'])}{q} "
                f"height={q}{n(e['h'])}{q} rx={q}{n(e.get('rx', 0))}{q} "
                f"fill={q}{_paint(e, 'fill', theme, solid)}{q}/>")
    if t == "circle":
        return (f"<circle cx={q}{n(e['cx'])}{q} cy={q}{n(e['cy'])}{q} r={q}{n(e['r'])}{q} "
                f"fill={q}{_paint(e, 'fill', theme, solid)}{q}/>")
    if t == "line":
        return (f"<line x1={q}{n(e['x1'])}{q} y1={q}{n(e['y1'])}{q} x2={q}{n(e['x2'])}{q} "
                f"y2={q}{n(e['y2'])}{q} stroke={q}{_paint(e, 'stroke', theme, solid)}{q} "
                f"stroke-width={q}{n(e['width'])}{q}/>")
    if t == "arch":
        if "fill" in e:
            return f"<path d={q}{_arch_d(e, True)}{q} fill={q}{_paint(e, 'fill', theme, solid)}{q}/>"
        return (f"<path d={q}{_arch_d(e, False)}{q} fill={q}none{q} "
                f"stroke={q}{_paint(e, 'stroke', theme, solid)}{q} stroke-width={q}{n(e['width'])}{q}/>")
    raise ValueError(f"unknown mark element type: {t}")


def _body_svg(mark: dict, theme: str, quote='"', solid=False) -> str:
    if "elements" in mark:
        return "".join(_element_svg(e, theme, quote, solid) for e in mark["elements"])
    # legacy bar geometry (brand v1) — byte-stable with the original renderer
    if quote == '"':
        return "".join(
            f'<rect x="{n(b["x"])}" y="{n(b["y"])}" width="{n(b["w"])}" '
            f'height="{n(b["h"])}" rx="{n(mark["rx"])}" fill="{b["color"]}"/>'
            for b in mark["bars"])
    return "".join(
        f"<rect x='{n(b['x'])}' y='{n(b['y'])}' width='{n(b['w'])}' "
        f"height='{n(b['h'])}' rx='{n(mark['rx'])}' fill='{b['color']}'/>"
        for b in mark["bars"])


def svg(mark: dict, cls=None, size=None, theme=None) -> str:
    cls = mark.get("class", "mark") if cls is None else cls
    size = mark.get("size", mark["viewbox"]) if size is None else size
    theme = theme or mark.get("default_theme", "light")
    vb = n(mark["viewbox"])
    cls_attr = f' class="{cls}"' if cls else ""
    return (f'<svg{cls_attr} width="{n(size)}" height="{n(size)}" '
            f'viewBox="0 0 {vb} {vb}" aria-hidden="true">{_body_svg(mark, theme)}</svg>')


def favicon_svg(mark: dict, theme=None) -> str:
    f = mark["favicon"]
    theme = theme or mark.get("default_theme", "light")
    vb = n(f["viewbox"])
    body = _body_svg(mark, theme, quote="'", solid=True)
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {vb} {vb}'>"
            f"<rect width='{vb}' height='{vb}' rx='{n(f['bg_radius'])}' fill='{f['bg']}'/>"
            f"<g transform='translate({n(f['tx'])} {n(f['ty'])}) scale({n(f['scale'])})'>"
            f"{body}</g></svg>")


def favicon_data_uri(mark: dict) -> str:
    body = favicon_svg(mark).replace("#", "%23").replace("<", "%3C").replace(">", "%3E")
    return "data:image/svg+xml," + body


def png(mark: dict, size: int, supersample: int = 4):
    """Rasterize the favicon composition at `size`×`size` (Pillow, lazy import)."""
    from PIL import Image, ImageDraw
    f = mark["favicon"]
    theme = mark.get("default_theme", "light")
    s = size * supersample
    k = s / f["viewbox"]
    tx, ty, sc = f["tx"], f["ty"], f["scale"]

    def pt(x, y):
        return ((x * sc + tx) * k, (y * sc + ty) * k)

    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=f["bg_radius"] * k, fill=f["bg"])

    if "elements" not in mark:
        for b in mark["bars"]:
            x0, y0 = pt(b["x"], b["y"])
            x1, y1 = pt(b["x"] + b["w"], b["y"] + b["h"])
            d.rounded_rectangle([x0, y0, x1, y1], radius=mark["rx"] * sc * k, fill=b["color"])
        return im.resize((size, size), Image.LANCZOS)

    for e in mark["elements"]:
        t = e["type"]
        if t == "rect":
            x0, y0 = pt(e["x"], e["y"])
            x1, y1 = pt(e["x"] + e["w"], e["y"] + e["h"])
            d.rounded_rectangle([x0, y0, x1, y1], radius=e.get("rx", 0) * sc * k,
                                fill=_paint(e, "fill", theme, True))
        elif t == "circle":
            cx, cy = pt(e["cx"], e["cy"])
            r = e["r"] * sc * k
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=_paint(e, "fill", theme, True))
        elif t == "line":
            d.line([pt(e["x1"], e["y1"]), pt(e["x2"], e["y2"])],
                   fill=_paint(e, "stroke", theme, True), width=round(e["width"] * sc * k))
        elif t == "arch":
            x0, x1, top, bot = e["x0"], e["x1"], e["top"], e.get("bot", 22)
            r = (x1 - x0) / 2
            (ax0, ay0), (ax1, ay1) = pt(x0, top), pt(x1, top + 2 * r)
            if "fill" in e:
                fill = _paint(e, "fill", theme, True)
                d.pieslice([ax0, ay0, ax1, ay1], 180, 360, fill=fill)
                lx0, ly0 = pt(x0, top + r)
                lx1, ly1 = pt(x1, bot)
                d.rectangle([lx0, ly0, lx1, ly1], fill=fill)
            else:
                stroke = _paint(e, "stroke", theme, True)
                w = e["width"] * sc * k
                d.arc([ax0, ay0, ax1, ay1], 180, 360, fill=stroke, width=round(w))
                for lx in (x0, x1):
                    cx0, cy0 = pt(lx, top + r)
                    _, cy1 = pt(lx, bot)
                    d.rectangle([cx0 - w / 2, cy0, cx0 + w / 2, cy1], fill=stroke)
        else:
            raise ValueError(f"unknown mark element type: {t}")
    return im.resize((size, size), Image.LANCZOS)


def main(argv):
    brand_arg = None
    png_args = None
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--brand":
            brand_arg = args.pop(0)
        elif a == "--png":
            png_args = (int(args.pop(0)), args.pop(0))
        else:
            print(f"unknown arg: {a}", file=sys.stderr)
            return 2
    mark = lib.load_brand(brand_arg)["mark"]
    if png_args:
        size, out = png_args
        png(mark, size).save(out, optimize=True)
        print(f"wrote {out}")
        return 0
    print(svg(mark))
    print(favicon_data_uri(mark))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
