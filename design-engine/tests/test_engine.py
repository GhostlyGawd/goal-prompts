"""Design-engine tool tests. Run: python3 -m unittest discover -s design-engine/tests

Stdlib only. The suite pins (1) the tools' own logic against fixtures and
known WCAG values, and (2) the live brand.json against the host's committed
tokens.css — the drift guard that makes the manifest the single source of
truth in practice, not just in prose.
"""
import copy
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import enginelib as lib
import tokens_build
import mark_render
import contrast
import brand_lint
import css_hex_lint

BRAND = lib.load_brand()
SCHEMA = json.loads((lib.ENGINE_DIR / "brand.schema.json").read_text(encoding="utf-8"))


def flatparse(css):
    """{(media_context, selector, prop): value} — one level of @media nesting,
    comments stripped. Small on purpose: tokens.css is a flat, generated file."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = {}

    def parse_block(text, ctx):
        i, selbuf = 0, ""
        while i < len(text):
            ch = text[i]
            if ch == "{":
                depth, j = 1, i + 1
                while j < len(text) and depth:
                    if text[j] == "{":
                        depth += 1
                    elif text[j] == "}":
                        depth -= 1
                    j += 1
                body, sel = text[i + 1:j - 1], selbuf.strip()
                selbuf = ""
                if sel.startswith("@media"):
                    parse_block(body, sel)
                else:
                    for part in body.split(";"):
                        if ":" in part:
                            k, v = part.split(":", 1)
                            out[(ctx, sel, k.strip())] = v.strip()
                i = j
            else:
                selbuf += ch
                i += 1

    parse_block(css, "")
    return out


class ColorMathTests(unittest.TestCase):
    def test_known_wcag_ratios(self):
        self.assertAlmostEqual(lib.ratio("#FFFFFF", "#000000"), 21.0, places=2)
        self.assertAlmostEqual(lib.ratio("#000000", "#FFFFFF"), 21.0, places=2)
        self.assertAlmostEqual(lib.ratio("#777777", "#FFFFFF"), 4.48, places=2)

    def test_mix_matches_legacy_tokens_test_arithmetic(self):
        # identical math to tests/test_build.py TokensTests: c * p toward black
        self.assertEqual(lib.mix_toward_black("#E8DE5A", 62),
                         tuple(c * 0.62 for c in (0xE8, 0xDE, 0x5A)))

    def test_alias_resolution_and_cycle(self):
        roles = {"a": "@b", "b": "#112233", "x": "@y", "y": "@x"}
        self.assertEqual(lib.resolve_role(roles, "a"), "#112233")
        with self.assertRaises(ValueError):
            lib.resolve_role(roles, "x")


class TokensBuildTests(unittest.TestCase):
    def test_compiled_tokens_match_the_committed_file(self):
        # THE single-source guard: tokens.css on disk must be exactly what
        # brand.json compiles to. Regenerate via build.py (or tokens_build
        # --check) whenever the manifest changes.
        committed = (lib.HOST_ROOT / BRAND["host"]["tokens_out"]).read_text(encoding="utf-8")
        self.assertEqual(flatparse(tokens_build.compile_css(BRAND)), flatparse(committed))

    def test_aliases_emit_var_references(self):
        css = tokens_build.compile_css(BRAND)
        self.assertIn("--good:var(--success)", css)
        self.assertIn("--act:var(--danger)", css)

    def test_every_categorical_family_gets_base_and_mix_rules(self):
        css = tokens_build.compile_css(BRAND)
        for fam, hexv in BRAND["palette"]["categorical"].items():
            rule = f".f-{fam.lower()}{{--fc:{hexv}}}"
            self.assertIn(rule, css, fam)
            for theme, mix in BRAND["palette"].get("categorical_mix", {}).items():
                mixed = (f'.f-{fam.lower()}{{--fc:color-mix(in srgb,{hexv} '
                         f'{mix["percent"]}%,{mix["toward"]})}}')
                self.assertIn(f':root[data-theme="{theme}"] {mixed}', css, fam)
                self.assertIn(f":root:not([data-theme]) {mixed}", css, fam)

    def test_motion_tokens_and_reduced_motion_collapse(self):
        flat = flatparse(tokens_build.compile_css(BRAND))
        collapse = BRAND["motion"].get("reduced_motion") == "collapse-to-instant"
        for k, v in BRAND["motion"]["durations"].items():
            self.assertEqual(flat[("", ":root", f"--dur-{k}")], v)
            rm_key = ("@media (prefers-reduced-motion:reduce)", ":root", f"--dur-{k}")
            if collapse:
                self.assertEqual(flat[rm_key], "0ms")
            else:
                self.assertNotIn(rm_key, flat)
        for k in BRAND["motion"]["easings"]:
            name = "--ease" if k == "default" else f"--ease-{k}"
            self.assertIn(("", ":root", name), flat)

    def test_non_default_theme_gets_explicit_and_os_preference_blocks(self):
        flat = flatparse(tokens_build.compile_css(BRAND))
        default = BRAND["palette"]["default_theme"]
        for theme in BRAND["palette"]["themes"]:
            if theme == default:
                continue
            self.assertIn(("", f':root[data-theme="{theme}"]', "--ink"), flat)
            self.assertIn((f"@media (prefers-color-scheme:{theme})",
                           ":root:not([data-theme])", "--ink"), flat)

    def test_fontface_lines_cover_every_declared_file(self):
        css = tokens_build.compile_css(BRAND)
        for face in BRAND["type"]["faces"]:
            for f in face["files"]:
                fname = f["path"].rsplit("/", 1)[-1]
                self.assertIn(f"src:url({BRAND['host']['fonts_url']}{fname})", css)


class MarkRenderTests(unittest.TestCase):
    def test_svg_structure_follows_manifest(self):
        svg = mark_render.svg(BRAND["mark"])
        mark = BRAND["mark"]
        if "bars" in mark:
            self.assertEqual(svg.count("<rect"), len(mark["bars"]))
            for b in mark["bars"]:
                self.assertIn(f'fill="{b["color"]}"', svg)
        else:
            arches = [e for e in mark["elements"] if e["type"] == "arch"]
            self.assertEqual(svg.count("<path"), len(arches))
            default = mark.get("default_theme", "light")
            for e in arches:
                c = e.get("stroke", e.get("fill"))
                if isinstance(c, dict):
                    c = c[default]
                self.assertIn(c, svg)
        self.assertIn(f'viewBox="0 0 {mark["viewbox"]:g} '
                      f'{mark["viewbox"]:g}"', svg)

    def test_number_formatting_has_no_trailing_zeros(self):
        # 11 not 11.0, 6.9 not 6.90 — pins parity with the hand-authored SVG
        svg = mark_render.svg(BRAND["mark"])
        self.assertNotRegex(svg, r'"\d+\.0"')

    def test_favicon_is_a_urlencoded_svg_on_the_bg_tile(self):
        uri = mark_render.favicon_data_uri(BRAND["mark"])
        self.assertTrue(uri.startswith("data:image/svg+xml,%3Csvg"))
        bg = BRAND["mark"]["favicon"]["bg"].replace("#", "%23")
        self.assertIn(f"fill='{bg}'", uri)
        self.assertNotIn("<", uri.split(",", 1)[1])

    def test_png_renders_at_requested_size(self):
        try:
            import PIL  # noqa: F401
        except ImportError:
            self.skipTest("Pillow not installed (generate-time dep)")
        im = mark_render.png(BRAND["mark"], 64)
        self.assertEqual(im.size, (64, 64))

    ELEMENTS_MARK = {
        "viewbox": 24, "class": "mark", "size": 24, "default_theme": "light",
        "elements": [
            {"type": "arch", "x0": 3.4, "x1": 20.6, "top": 3.2,
             "stroke": {"light": "#3355B4", "dark": "#7F9FEC"}, "width": 2.3},
            {"type": "arch", "x0": 10.6, "x1": 13.4, "top": 14.8, "fill": "#E8752C"},
            {"type": "line", "x1": 4, "y1": 22, "x2": 20, "y2": 22,
             "stroke": "#1D1F28", "width": 2},
            {"type": "circle", "cx": 12, "cy": 19, "r": 1.5, "fill": "#E8752C"},
        ],
        "favicon": {"viewbox": 64, "bg": "#F7F2E3", "bg_radius": 13,
                    "tx": 10, "ty": 9.2, "scale": 1.9},
    }

    def test_element_mark_renders_arch_stroke_fill_and_theme_colors(self):
        svg_light = mark_render.svg(self.ELEMENTS_MARK)
        self.assertIn('stroke="#3355B4"', svg_light)          # theme map, light
        self.assertIn('A8.6 8.6 0 0 1', svg_light)            # stroked arch radius
        self.assertIn('fill="#E8752C"', svg_light)            # filled arch + circle
        self.assertIn("Z", svg_light)                         # filled arch closes
        svg_dark = mark_render.svg(self.ELEMENTS_MARK, theme="dark")
        self.assertIn('stroke="#7F9FEC"', svg_dark)
        self.assertNotIn("#3355B4", svg_dark)

    def test_element_mark_favicon_and_png(self):
        uri = mark_render.favicon_data_uri(self.ELEMENTS_MARK)
        self.assertTrue(uri.startswith("data:image/svg+xml,%3Csvg"))
        self.assertIn("fill='%23F7F2E3'", uri)
        try:
            import PIL  # noqa: F401
        except ImportError:
            self.skipTest("Pillow not installed (generate-time dep)")
        im = mark_render.png(self.ELEMENTS_MARK, 64)
        self.assertEqual(im.size, (64, 64))


class ContrastTests(unittest.TestCase):
    def test_current_brand_passes(self):
        violations, _ = contrast.check(BRAND)
        self.assertEqual(violations, [])

    def test_unreadable_text_role_is_caught(self):
        doctored = copy.deepcopy(BRAND)
        doctored["palette"]["themes"]["dark"]["text"]["faint"] = "#26272C"  # ~ the line color
        violations, _ = contrast.check(doctored)
        self.assertTrue(any("faint" in v for v in violations), violations)

    def test_categorical_below_minimum_is_caught_in_mixed_theme(self):
        doctored = copy.deepcopy(BRAND)
        mix_theme = next(iter(doctored["palette"]["categorical_mix"]))
        mix = doctored["palette"]["categorical_mix"][mix_theme]
        # push a hue to nearly the mixed theme's own ground color so it fails
        doctored["palette"]["categorical"]["Automation"] = (
            "#F8F0A0" if mix["toward"] == "black" else "#EDE6D4")
        mix["percent"] = 96
        violations, _ = contrast.check(doctored)
        self.assertTrue(any("Automation" in v for v in violations), violations)


class BrandLintTests(unittest.TestCase):
    def _lint(self, brand):
        return brand_lint.lint(brand, SCHEMA, lib.HOST_ROOT)

    def test_current_brand_is_clean(self):
        self.assertEqual(self._lint(BRAND), [])

    def test_theme_role_parity_is_enforced(self):
        doctored = copy.deepcopy(BRAND)
        # delete a role from a NON-default theme; parity is judged vs the default
        other = next(t for t in doctored["palette"]["themes"]
                     if t != doctored["palette"]["default_theme"])
        del doctored["palette"]["themes"][other]["accents"]["amber-2"]
        errs = self._lint(doctored)
        self.assertTrue(any(other in e and "amber-2" in e for e in errs), errs)

    def test_bad_hex_is_a_schema_error(self):
        doctored = copy.deepcopy(BRAND)
        doctored["palette"]["themes"]["dark"]["surfaces"]["ink"] = "midnight"
        errs = self._lint(doctored)
        self.assertTrue(any("ink" in e for e in errs), errs)

    def test_missing_font_file_is_caught(self):
        doctored = copy.deepcopy(BRAND)
        doctored["type"]["faces"][0]["files"][0]["path"] = "fonts/nope.woff2"
        errs = self._lint(doctored)
        self.assertTrue(any("nope.woff2" in e for e in errs), errs)

    def test_dangling_alias_is_caught(self):
        doctored = copy.deepcopy(BRAND)
        doctored["palette"]["themes"]["dark"]["aliases"]["good"] = "@nonexistent"
        errs = self._lint(doctored)
        self.assertTrue(any("does not resolve" in e for e in errs), errs)


class CssHexLintTests(unittest.TestCase):
    def _scan(self, content, allow=()):
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
            f.write(content)
            p = Path(f.name)
        try:
            return css_hex_lint.scan_file(p, list(allow))
        finally:
            p.unlink()

    def test_raw_hex_in_style_block_is_flagged(self):
        hits = self._scan("<style>.a{color:#FF0000}</style>")
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0][2], "#FF0000")

    def test_var_consumption_is_clean(self):
        self.assertEqual(self._scan("<style>.a{color:var(--text)}</style>"), [])

    def test_hex_outside_style_is_ignored(self):
        self.assertEqual(self._scan("<p>use #FF0000 for errors</p>"), [])

    def test_allowlist_suppresses_a_documented_exception(self):
        hits = self._scan('<div style="background:#131417"></div>',
                          allow=[r"background:#131417"])
        self.assertEqual(hits, [])

    def test_rgba_is_flagged(self):
        hits = self._scan("<style>.a{box-shadow:0 0 4px rgba(0,0,0,.5)}</style>")
        self.assertEqual(len(hits), 1)


class SpecimenTests(unittest.TestCase):
    def test_specimen_builds_and_carries_the_system(self):
        import specimen
        html = specimen.build_specimen(BRAND)
        self.assertIn(BRAND["identity"]["product_name"], html)
        for fam in BRAND["palette"]["categorical"]:
            self.assertIn(fam, html)
        first_dur = next(iter(BRAND["motion"]["durations"]))
        self.assertIn(f"--dur-{first_dur}", html)
        self.assertIn("<svg", html)


if __name__ == "__main__":
    unittest.main()
