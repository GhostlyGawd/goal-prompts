#!/usr/bin/env python3
"""qa_sheet — tile every screenshot in out/shots/ into ONE contact sheet.

The QA loop's review artifact: after `shots.cjs [--matrix]`, this produces
out/qa-sheet.jpg — every page x theme x viewport as labeled thumbnails in a
grid, so "review everything" is one look instead of N file opens. Pillow;
generate-time.

    python3 design-engine/tools/qa_sheet.py [--width 320] [--out FILE]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import enginelib as lib


def main(argv):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("SKIP  Pillow not installed", file=sys.stderr)
        return 1
    args = list(argv)
    tw = int(args[args.index("--width") + 1]) if "--width" in args else 320
    out = Path(args[args.index("--out") + 1]) if "--out" in args else lib.OUT_DIR / "qa-sheet.jpg"
    shots = sorted((lib.OUT_DIR / "shots").glob("*.png"))
    if not shots:
        print("FAIL  no screenshots in out/shots — run shots.cjs first", file=sys.stderr)
        return 1
    max_th = 1400  # crop very tall pages; the sheet is a scanner, not an archive
    thumbs = []
    for s in shots:
        im = Image.open(s).convert("RGB")
        im.thumbnail((tw, 100000))
        if im.height > max_th:
            im = im.crop((0, 0, im.width, max_th))
        thumbs.append((s.stem, im))
    cols = min(5, len(thumbs))
    label_h = 22
    rows = (len(thumbs) + cols - 1) // cols
    row_h = [max(t.height for _, t in thumbs[r * cols:(r + 1) * cols]) + label_h + 10
             for r in range(rows)]
    sheet = Image.new("RGB", (cols * (tw + 10) + 10, sum(row_h) + 10), "#DDD8C9")
    d = ImageDraw.Draw(sheet)
    y = 10
    for r in range(rows):
        for c, (name, t) in enumerate(thumbs[r * cols:(r + 1) * cols]):
            x = 10 + c * (tw + 10)
            d.text((x, y + 2), name.upper(), fill="#1D1F28")
            sheet.paste(t, (x, y + label_h))
        y += row_h[r]
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "JPEG", quality=80, optimize=True)
    print(f"wrote {out} ({len(thumbs)} shots)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
