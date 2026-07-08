#!/usr/bin/env python3
"""Generate og/<id>.png share cards for briefs — the style of the 0.4 set.

Usage:
    python3 scripts/og.py            # generate cards missing from og/
    python3 scripts/og.py --all      # regenerate every card
    python3 scripts/og.py 46 47      # specific ids

Needs Pillow and fontTools (`pip install Pillow fonttools brotli`). The cards
render in the site's own brand fonts — Archivo (variable) and IBM Plex Mono —
decompressed from the shipped woff2 at runtime, so the share image matches the
live site instead of a DejaVu stand-in. build.py fails when a brief has no
og/<id>.png, so run this after adding a brief. Cards are 1200x630:
family-colored bar and id, title, wrapped tagline, and a family → OUTPUT.md
footer.
"""
import sys
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402  (reuses the brief parser + family colors; stdlib-only)

# family colors live in build.FAMILY_COLORS (one source of truth for Python);
# template.html's .f-* CSS rules must carry the same values for the JS catalog.
FAMILY_COLORS = build.FAMILY_COLORS

W, H = 1200, 630
INK = "#14181E"
TEXT = "#E2E6EC"
DIM = "#8B96A5"
BAR_W = 17
LEFT = 78
DOMAIN = "goal-prompts.vercel.app"

FONTS = ROOT / "fonts"
_TTF_CACHE = {}


def _ttf(woff2_name):
    """Decompress a shipped woff2 to a temp ttf once; Pillow can't read woff2."""
    if woff2_name not in _TTF_CACHE:
        f = TTFont(str(FONTS / woff2_name))  # brotli-decompresses the woff2
        f.flavor = None
        out = Path(tempfile.gettempdir()) / (Path(woff2_name).stem + ".ttf")
        f.save(str(out))
        _TTF_CACHE[woff2_name] = out
    return _TTF_CACHE[woff2_name]


def font(woff2_name, size, weight=None):
    fnt = ImageFont.truetype(str(_ttf(woff2_name)), size)
    if weight is not None:  # Archivo is variable — pin the wght axis
        try:
            fnt.set_variation_by_axes([weight])
        except Exception:
            pass
    return fnt

ARCHIVO = "archivo-latin-var.woff2"
MONO = "plexmono-latin-400.woff2"
MONO_SB = "plexmono-latin-600.woff2"


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def render(brief):
    accent = FAMILY_COLORS[brief["family"]]
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, BAR_W - 1, H], fill=accent)

    f_num = font(MONO_SB, 100)
    f_tag = font(ARCHIVO, 30, 400)
    f_foot_b = font(MONO_SB, 22)
    f_foot = font(MONO, 22)

    d.text((LEFT, 62), brief["id"], font=f_num, fill=accent)

    title = brief["title"]
    tf = font(ARCHIVO, 58, 800)
    while d.textlength(title, font=tf) > W - LEFT - 60 and tf.size > 40:
        tf = font(ARCHIVO, tf.size - 4, 800)
    d.text((LEFT, 198), title, font=tf, fill=TEXT)

    y = 285
    for line in wrap(d, brief["tagline"], f_tag, 880)[:5]:
        d.text((LEFT, y), line, font=f_tag, fill=DIM)
        y += 38

    fy = 549
    x = LEFT
    fam = brief["family"].upper()
    d.text((x, fy), fam, font=f_foot_b, fill=accent)
    x += d.textlength(fam, font=f_foot_b) + 32
    out = "-> " + brief["output"]  # ASCII: the latin-subset mono woff2 has no U+2192 glyph
    d.text((x, fy), out, font=f_foot, fill=DIM)
    x += d.textlength(out, font=f_foot) + 42
    d.text((x, fy), DOMAIN, font=f_foot, fill=DIM)
    return im


def main():
    briefs = [build.parse(f) for f in sorted((ROOT / "prompts").rglob("*.md"))]
    by_id = {b["id"]: b for b in briefs}
    args = [a for a in sys.argv[1:] if a != "--all"]
    if args:
        ids = [a.zfill(2) for a in args]
        unknown = [i for i in ids if i not in by_id]
        if unknown:
            sys.exit("FAIL unknown brief id(s): " + ", ".join(unknown))
    elif "--all" in sys.argv:
        ids = list(by_id)
    else:
        ids = [i for i in by_id if not (ROOT / "og" / f"{i}.png").exists()]
    if not ids:
        print("OK  every brief has an og card; use --all to regenerate")
        return
    for i in sorted(ids):
        out = ROOT / "og" / f"{i}.png"
        render(by_id[i]).save(out, optimize=True)
        print(f"og/{i}.png  {by_id[i]['title']}")
    print(f"\nOK  {len(ids)} card(s) written")


if __name__ == "__main__":
    main()
