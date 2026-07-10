#!/usr/bin/env python3
"""font_subset — source a typeface into the host, license-checked. Generate-time.

Takes a TTF/OTF, verifies its license is a free/open one from the name table
(OFL / Apache / UFL markers), subsets it to the latin range, and writes a
woff2 into the host's fonts dir. The license check is a gate: an unverifiable
license exits non-zero unless --allow-unverified is passed *and* the operator
records why in DECISIONS.md.

    python3 design-engine/tools/font_subset.py IN.ttf [--name out-name] \\
        [--unicodes RANGES] [--allow-unverified] [--brand path]

Needs fontTools + brotli (already blessed generate-time deps, ADR-10 / ADR-13).
Latin default range matches the site's existing subsets.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import enginelib as lib

LATIN = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,"
         "U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,"
         "U+2212,U+2215,U+FEFF,U+FFFD,U+2190,U+2192,U+25B8,U+2713,U+00D7,U+2197")
# name-table strings AND license URLs count — some faces (e.g. Space Mono)
# carry only the OFL URL in nameID 14
FREE_MARKERS = ("SIL Open Font License", "OFL", "Apache License", "Ubuntu Font Licence",
                "openfontlicense.org", "scripts.sil.org/OFL")


def license_strings(font):
    out = []
    for rec in font["name"].names:
        if rec.nameID in (13, 14):  # license description, license URL
            out.append(rec.toUnicode())
    return out


def main(argv):
    try:
        from fontTools.ttLib import TTFont
        from fontTools.subset import Subsetter, Options
    except ImportError:
        print("SKIP  fontTools not installed — font_subset is a generate-time tool "
              "(pip install fonttools brotli)", file=sys.stderr)
        return 1

    src, name, unicodes, allow_unverified, brand_arg = None, None, LATIN, False, None
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--name":
            name = args.pop(0)
        elif a == "--unicodes":
            unicodes = args.pop(0)
        elif a == "--allow-unverified":
            allow_unverified = True
        elif a == "--brand":
            brand_arg = args.pop(0)
        else:
            src = Path(a)
    if not src or not src.exists():
        print("usage: font_subset.py IN.ttf [--name out] [--unicodes R] "
              "[--allow-unverified]", file=sys.stderr)
        return 2

    brand = lib.load_brand(brand_arg)
    font = TTFont(str(src))
    lic = license_strings(font)
    verified = any(m in s for s in lic for m in FREE_MARKERS)
    if not verified:
        head = (lic[0][:120] + "…") if lic else "(no license record in name table)"
        if not allow_unverified:
            print(f"FAIL  cannot verify a free license for {src.name}: {head}\n"
                  "      pass --allow-unverified only with an ADR recording the "
                  "actual license", file=sys.stderr)
            return 1
        print(f"WARN  license unverified for {src.name}: {head}")
    else:
        print(f"OK  license verified free: "
              f"{next(m for s in lic for m in FREE_MARKERS if m in s)}")

    opts = Options(flavor="woff2", layout_features="*", hinting=True)
    ss = Subsetter(options=opts)
    ss.populate(unicodes=[u.strip() for u in unicodes.split(",")])
    ss.subset(font)
    out_name = name or src.stem.lower().replace(" ", "") + "-latin.woff2"
    out = lib.HOST_ROOT / brand["host"]["fonts_dir"] / out_name
    out.parent.mkdir(parents=True, exist_ok=True)
    font.save(str(out))
    before, after = src.stat().st_size, out.stat().st_size
    print(f"wrote {out.relative_to(lib.HOST_ROOT)}  "
          f"{before / 1024:.0f}K → {after / 1024:.0f}K "
          f"({100 * after / before:.0f}%)")
    print("next: add the file to brand.json type.faces (path, weight, style) — "
          "brand_lint verifies it exists")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
