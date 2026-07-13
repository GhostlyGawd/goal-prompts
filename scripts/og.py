#!/usr/bin/env python3
"""Generate og/<id>.png share cards for briefs — the style of the 0.4 set.

Usage:
    python3 scripts/og.py             # generate cards missing from og/
    python3 scripts/og.py --all       # regenerate every card + home + playbooks
    python3 scripts/og.py --home      # just the home card (og.png)
    python3 scripts/og.py --playbooks # the per-playbook cards (og/p-<key>.png)
    python3 scripts/og.py 46 47       # specific ids

Needs Pillow and fontTools (`pip install Pillow fonttools brotli`). The cards
render in the site's own brand fonts — Schibsted Grotesk (variable), IBM Plex Sans, Plex Mono —
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
INK = "#15120D"
TEXT = "#F0EADC"
DIM = "#B9B09B"
ACCENT = "#FF6B47"  # the ledger vermilion (specs/design-direction.md)
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
    if weight is not None:  # Schibsted Grotesk is variable — pin the wght axis
        try:
            fnt.set_variation_by_axes([weight])
        except Exception:
            pass
    return fnt

DISPLAY = "schibstedgrotesk-latin-var.woff2"
SANS = "plexsans-latin-400.woff2"
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
    f_tag = font(SANS, 30)
    f_foot_b = font(MONO_SB, 22)
    f_foot = font(MONO, 22)

    d.text((LEFT, 62), brief["id"], font=f_num, fill=accent)

    title = brief["title"]
    tf = font(DISPLAY, 58, 800)
    while d.textlength(title, font=tf) > W - LEFT - 60 and tf.size > 40:
        tf = font(DISPLAY, tf.size - 4, 800)
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


def render_home(briefs):
    """The catalog's own share card: the bar mark, wordmark, tagline — the
    ledger identity (three paper bars, tallest flagged vermilion), not the
    retired 22-family spectrum."""
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)
    span = W - LEFT - 60
    # the brand bars, scaled up from the 24-unit viewBox (build.BRAND_MARK)
    mk, my = 5.4, 88  # scale + top of the mark
    for x, y, w, h, c in ((1, 9, 3.4, 9, TEXT), (6.9, 3, 3.4, 15, ACCENT),
                          (12.8, 7, 3.4, 11, TEXT), (18.7, 12, 3.4, 6, TEXT)):
        d.rounded_rectangle([LEFT + x * mk, my + y * mk,
                             LEFT + (x + w) * mk, my + (y + h) * mk],
                            radius=0.8 * mk, fill=c)
    d.text((LEFT + 156, 96), "Goal Prompts", font=font(DISPLAY, 92, 800), fill=TEXT)
    d.rectangle([LEFT, 290, LEFT + span, 293], fill=ACCENT)
    sf = font(DISPLAY, 48, 640)
    y = 340
    for line in wrap(d, "Know what to ask your coding agent.", sf, span)[:2]:
        d.text((LEFT, y), line, font=sf, fill=TEXT)
        y += 60
    fams = build.FAMILY_ORDER
    foot = f"{len(briefs)} briefs / {len(fams)} families / {DOMAIN}"
    d.text((LEFT, 548), foot, font=font(MONO, 24), fill=DIM)
    return im


def render_playbook(pb, by_id):
    """A playbook's share card (SEO-3, R31): same visual language as the
    brief cards — ink ground, mono eyebrow, display-weight title — with the
    sequence itself as the color: the left edge stacks one equalizer segment
    per stage in its brief's family color, and a dot row repeats the order
    horizontally (the storefront's seqDots)."""
    ids = pb["ids"]
    fams = [by_id[i]["family"] for i in ids]
    # ledger: one voice color — the eyebrow/lead speak vermilion; the family
    # hues stay where they are metadata (the stacked edge + the dot row).
    accent = ACCENT
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)

    # left edge: one segment per stage, gapped like the BRAND_MARK bars
    seg = H / len(ids)
    gap = 3 if len(ids) > 1 else 0
    for i, fam in enumerate(fams):
        y0 = i * seg
        y1 = (i + 1) * seg - (gap if i < len(ids) - 1 else 0)
        d.rectangle([0, y0, BAR_W - 1, y1], fill=FAMILY_COLORS[fam])

    f_eyebrow = font(MONO_SB, 26)
    n = len(ids)
    d.text((LEFT, 84), "PLAYBOOK", font=f_eyebrow, fill=accent)
    x = LEFT + d.textlength("PLAYBOOK", font=f_eyebrow) + 30
    d.text((x, 84), f"{n} BRIEF{'S' if n > 1 else ''} / ONE PASTE",
           font=font(MONO, 26), fill=DIM)

    title = pb["name"]
    tf = font(DISPLAY, 76, 800)
    while d.textlength(title, font=tf) > W - LEFT - 60 and tf.size > 42:
        tf = font(DISPLAY, tf.size - 4, 800)
    d.text((LEFT, 150), title, font=tf, fill=TEXT)

    f_tag = font(SANS, 30)
    y = 275
    for line in wrap(d, pb.get("tagline") or pb["desc"], f_tag, 1000)[:4]:
        d.text((LEFT, y), line, font=f_tag, fill=DIM)
        y += 38

    # the sequence, in order — the storefront's seqDots at share-card scale
    dy, dsz, dgap = 452, 30, 12
    for i, fam in enumerate(fams[:16]):
        x0 = LEFT + i * (dsz + dgap)
        d.rounded_rectangle([x0, dy, x0 + dsz, dy + dsz], radius=3,
                            fill=FAMILY_COLORS[fam])

    fy = 549
    x = LEFT
    lead = f"{n} REPORTS" if n > 1 else "1 REPORT"
    d.text((x, fy), lead, font=font(MONO_SB, 22), fill=accent)
    x += d.textlength(lead, font=font(MONO_SB, 22)) + 42
    d.text((x, fy), DOMAIN, font=font(MONO, 22), fill=DIM)
    return im


def write_playbook_cards(by_id):
    import json
    from PIL.PngImagePlugin import PngInfo
    playbooks = json.loads((ROOT / "playbooks.json").read_text(encoding="utf-8"))
    for pb in playbooks:
        # build.py's drift guard compares this baked-in stage count to the
        # live playbook, like og.png's gp-briefs count
        meta = PngInfo()
        meta.add_text("gp-briefs", str(len(pb["ids"])))
        out = ROOT / "og" / f'p-{pb["key"]}.png'
        render_playbook(pb, by_id).save(str(out), optimize=True, pnginfo=meta)
        print(f'og/p-{pb["key"]}.png  {pb["name"]}')
    print(f"OK  {len(playbooks)} playbook card(s) written")


def main():
    briefs = [build.parse(f) for f in sorted((ROOT / "prompts").rglob("*.md"))]
    by_id = {b["id"]: b for b in briefs}
    if "--home" in sys.argv or "--all" in sys.argv:
        # Embed the brief count as PNG metadata so the (stdlib-only) build can
        # guard this raster's baked-in "N briefs" against the live catalog.
        from PIL.PngImagePlugin import PngInfo
        meta = PngInfo()
        meta.add_text("gp-briefs", str(len(briefs)))
        render_home(briefs).save(str(ROOT / "og.png"), optimize=True, pnginfo=meta)
        print("og.png  home card")
        if "--home" in sys.argv:
            return
    if "--playbooks" in sys.argv or "--all" in sys.argv:
        write_playbook_cards(by_id)
        if "--playbooks" in sys.argv:
            return
    args = [a for a in sys.argv[1:] if a not in ("--all", "--home", "--playbooks")]
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
