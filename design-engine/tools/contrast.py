#!/usr/bin/env python3
"""contrast — the WCAG 2.1 contrast gate for brand.json. Stdlib only.

Checks, per theme, against the thresholds the manifest itself declares
(brand.json `contrast`):
  1. every text role × every surface  >= text_min[role]
  2. every accent role × every surface >= accents_min
  3. every categorical hue >= categorical_min — raw on the default (dark)
     theme's surfaces; color-mix()ed toward black (categorical_mix_light) on
     every other theme's surfaces, mirroring the compiled CSS exactly.

Exit 0 with a PASS summary, or 1 with one line per violation (ADR-1: the
gate is an exit code, not prose).

    python3 design-engine/tools/contrast.py [--brand path] [--report [file]]

--report writes the full ratio matrix to design-engine/out/contrast-report.txt
(or the given path) — the evidence artifact for design reviews.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import enginelib as lib


def check(brand: dict):
    """Return (violations, matrix_lines). Empty violations == gate passes."""
    cfg = brand["contrast"]
    pal = brand["palette"]
    default = pal["default_theme"]
    violations, matrix = [], []

    for theme in pal["themes"]:
        roles = lib.theme_roles(brand, theme)
        surfaces = {s: lib.resolve_role(roles, s) for s in cfg["surfaces"]}
        matrix.append(f"[{theme}]")

        for role, minimum in cfg["text_min"].items():
            fg = lib.resolve_role(roles, role)
            for sname, sval in surfaces.items():
                r = lib.ratio(fg, sval)
                matrix.append(f"  {role:>8} on {sname:<8} {r:6.2f}  (min {minimum})")
                if r < minimum:
                    violations.append(
                        f"{theme}: --{role} {fg} on --{sname} {sval} = {r:.2f} < {minimum}")

        for role in cfg.get("accents", []):
            fg = lib.resolve_role(roles, role)
            minimum = cfg.get("accents_min", 3.0)
            for sname, sval in surfaces.items():
                r = lib.ratio(fg, sval)
                matrix.append(f"  {role:>8} on {sname:<8} {r:6.2f}  (min {minimum})")
                if r < minimum:
                    violations.append(
                        f"{theme}: accent --{role} {fg} on --{sname} {sval} = {r:.2f} < {minimum}")

        cat_min = cfg["categorical_min"]
        mix = pal.get("categorical_mix", {}).get(theme)
        cat_surfaces = {s: surfaces[s] for s in cfg.get("categorical_surfaces", cfg["surfaces"])}
        for fam, hexv in pal["categorical"].items():
            if theme == default or not mix:
                fg, how = lib.hex_rgb(hexv), "raw"
            else:
                fg = lib.mix_toward(hexv, mix["percent"], mix["toward"])
                how = f"mix {mix['percent']}% {mix['toward']}"
            for sname, sval in cat_surfaces.items():
                r = lib.ratio(fg, sval)
                matrix.append(f"  {fam:>12} ({how}) on {sname:<8} {r:6.2f}  (min {cat_min})")
                if r < cat_min:
                    violations.append(
                        f"{theme}: categorical {fam} {hexv} ({how}) on --{sname} {sval} "
                        f"= {r:.2f} < {cat_min}")
    return violations, matrix


def main(argv):
    brand_arg, report = None, None
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--brand":
            brand_arg = args.pop(0)
        elif a == "--report":
            report = args.pop(0) if args and not args[0].startswith("--") else str(
                lib.OUT_DIR / "contrast-report.txt")
        else:
            print(f"unknown arg: {a}", file=sys.stderr)
            return 2
    brand = lib.load_brand(brand_arg)
    violations, matrix = check(brand)
    if report:
        p = Path(report)
        p.parent.mkdir(parents=True, exist_ok=True)
        head = "PASS" if not violations else "FAIL:\n" + "\n".join(violations)
        p.write_text(head + "\n\n" + "\n".join(matrix) + "\n", encoding="utf-8")
        print(f"wrote {p}")
    if violations:
        print(f"FAIL  {len(violations)} contrast violation(s):", file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        return 1
    n_pairs = len(matrix) - len(brand["palette"]["themes"])
    print(f"OK  contrast: {n_pairs} pairs checked across "
          f"{len(brand['palette']['themes'])} themes, all above declared minimums")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
