#!/usr/bin/env python3
"""Generate og/<id>.png share cards for briefs — the style of the 0.4 set.

Usage:
    python3 scripts/og.py            # generate cards missing from og/
    python3 scripts/og.py --all      # regenerate every card
    python3 scripts/og.py 46 47      # specific ids

Needs Pillow (`pip install Pillow`) and the DejaVu fonts most Linux images
ship. build.py fails when a brief has no og/<id>.png, so run this after
adding a brief. Cards are 1200x630: family-colored bar and id, title,
wrapped tagline, and a family -> OUTPUT.md footer.
"""
import sys
from pathlib import Path

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

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


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

    f_num = font("DejaVuSansMono.ttf", 100)
    f_tag = font("DejaVuSans.ttf", 30)
    f_foot_b = font("DejaVuSansMono-Bold.ttf", 22)
    f_foot = font("DejaVuSansMono.ttf", 22)

    d.text((LEFT, 62), brief["id"], font=f_num, fill=accent)

    title = brief["title"]
    tf = font("DejaVuSans-Bold.ttf", 58)
    while d.textlength(title, font=tf) > W - LEFT - 60 and tf.size > 40:
        tf = font("DejaVuSans-Bold.ttf", tf.size - 4)
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
    out = "-> " + brief["output"]
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
