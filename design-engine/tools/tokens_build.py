#!/usr/bin/env python3
"""tokens_build — compile brand.json into the host's tokens.css.

The one implementation of manifest → CSS custom properties. build.py imports
`compile_css()` directly (python-import integration); hosts without Python in
their build run this file as a CLI, which writes host.tokens_out:

    python3 design-engine/tools/tokens_build.py [--brand path] [--check]

--check compiles and diffs against the file on disk, exiting non-zero on
drift, without writing. Stdlib only.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import enginelib as lib


def _decl(name: str, value: str) -> str:
    if value.startswith("@"):
        value = f"var(--{value[1:]})"
    return f"--{name}:{value}"


def _group_lines(brand: dict, groups: dict, indent="  ") -> list:
    """One CSS line per role group; a palette.notes entry keyed by a group's
    first role emits a comment line above it."""
    notes = brand["palette"].get("notes", {})
    lines = []
    for group in groups.values():
        first = next(iter(group))
        if first in notes:
            lines.append(f"{indent}/* {notes[first]} */")
        lines.append(indent + ";".join(_decl(k, v) for k, v in group.items()) + ";")
    return lines


def _flat_line(brand: dict, mapping: dict, indent="  ") -> str:
    notes = brand["palette"].get("notes", {})
    first = next(iter(mapping))
    prefix = f"{indent}/* {notes[first]} */\n" if first in notes else ""
    return prefix + indent + ";".join(_decl(k, v) for k, v in mapping.items()) + ";"


def _theme_block(brand: dict, theme: str, scheme: str) -> str:
    lines = [f"  color-scheme:{scheme};"]
    lines += _group_lines(brand, brand["palette"]["themes"][theme])
    return "\n".join(lines)


def _font_faces(brand: dict) -> list:
    url = brand["host"]["fonts_url"]
    faces = []
    for face in brand["type"]["faces"]:
        for f in face["files"]:
            fname = f["path"].rsplit("/", 1)[-1]
            faces.append(
                f"@font-face{{font-family:'{face['css_name']}';font-style:{f['style']};"
                f"font-weight:{f['weight']};font-display:swap;"
                f"src:url({url}{fname}) format('woff2')}}")
    return faces


def _categorical_css(brand: dict) -> str:
    pal = brand["palette"]
    prefix = pal.get("categorical_prefix", "f-")
    var = pal.get("categorical_var", "fc")
    base = "".join(f".{prefix}{k.lower()}{{--{var}:{v}}}"
                   for k, v in pal["categorical"].items())
    out = base
    # non-default themes re-tune every hue in place via color-mix; direction and
    # strength are declared per theme in palette.categorical_mix
    for theme, mix in pal.get("categorical_mix", {}).items():
        pct, toward = mix["percent"], mix["toward"]
        block = "".join(f':root[data-theme="{theme}"] .{prefix}{k.lower()}'
                        f"{{--{var}:color-mix(in srgb,{v} {pct}%,{toward})}}"
                        for k, v in pal["categorical"].items())
        block += (f"@media (prefers-color-scheme:{theme}){{"
                  + "".join(f":root:not([data-theme]) .{prefix}{k.lower()}"
                            f"{{--{var}:color-mix(in srgb,{v} {pct}%,{toward})}}"
                            for k, v in pal["categorical"].items())
                  + "}")
        out += "\n" + block
    return out


def _ease_name(k: str) -> str:
    # the key "default" emits the bare --ease; every other key suffixes it
    return "--ease" if k == "default" else f"--ease-{k}"


def _motion_lines(brand: dict) -> list:
    m = brand["motion"]
    note = m.get("note", "motion — durations + easings")
    lines = [f"  /* {note} */"]
    lines.append("  " + ";".join(f"--dur-{k}:{v}" for k, v in m["durations"].items()) + ";")
    lines.append("  " + ";".join(f"{_ease_name(k)}:{v}" for k, v in m["easings"].items()) + ";")
    return lines


def _reduced_motion(brand: dict) -> str:
    if brand["motion"].get("reduced_motion") != "collapse-to-instant":
        return ""
    zeros = ";".join(f"--dur-{k}:0ms" for k in brand["motion"]["durations"])
    return ("/* prefers-reduced-motion collapses every duration token to instant */\n"
            f"@media (prefers-reduced-motion:reduce){{:root{{{zeros}}}}}\n")


def compile_css(brand: dict) -> str:
    out = ["/* tokens.css — GENERATED; do not hand-edit. "
           "Source: design-engine/brand.json → design-engine/tools/tokens_build.py. */"]
    out += _font_faces(brand)

    root = [":root{", f"  color-scheme:{brand['palette']['default_theme']};"]
    root += _group_lines(brand, brand["palette"]["themes"][brand["palette"]["default_theme"]])
    root.append(_flat_line(brand, brand["radii"]))
    root.append(_flat_line(brand, brand["space"]["layout"]))
    root.append(_flat_line(brand, brand["space"]["scale"]))
    if brand["space"].get("sections"):
        root.append(_flat_line(brand, brand["space"]["sections"]))
    if brand.get("elevation"):
        root.append(_flat_line(brand, brand["elevation"]))
    root += _motion_lines(brand)
    for name, stack in brand["type"]["stacks"].items():
        root.append(f"  --{name}:{stack};")
    root.append("}")
    out.append("\n".join(root))

    # every non-default theme gets both an explicit [data-theme] block and an
    # OS-preference block; an explicit choice (the toggle) always wins.
    default = brand["palette"]["default_theme"]
    for theme in brand["palette"]["themes"]:
        if theme == default:
            continue
        block = _theme_block(brand, theme, theme)
        out.append(f':root[data-theme="{theme}"]{{\n{block}\n}}')
        out.append(f"/* OS-{theme} users without a stored choice get the {theme} theme by default;\n"
                   f"   an explicit data-theme (set by the toggle) always wins, both directions. */")
        out.append(f"@media (prefers-color-scheme:{theme}){{:root:not([data-theme]){{\n{block}\n}}}}")

    out += brand["host"].get("extra_css", [])
    out.append(_categorical_css(brand))
    rm = _reduced_motion(brand)
    if rm:
        out.append(rm.rstrip("\n"))
    return "\n".join(out) + "\n"


def main(argv):
    brand_arg = None
    check = False
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--brand":
            brand_arg = args.pop(0)
        elif a == "--check":
            check = True
        else:
            print(f"unknown arg: {a}", file=sys.stderr)
            return 2
    brand = lib.load_brand(brand_arg)
    css = compile_css(brand)
    out_path = lib.HOST_ROOT / brand["host"]["tokens_out"]
    if check:
        current = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
        if current != css:
            print(f"DRIFT  {out_path} does not match brand.json — "
                  "run tokens_build.py (or the host build) to regenerate", file=sys.stderr)
            return 1
        print(f"OK  {out_path} matches brand.json")
        return 0
    out_path.write_text(css, encoding="utf-8")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
