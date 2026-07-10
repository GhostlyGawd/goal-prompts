"""Tests for the media/craft layer: image_lab, scene, present.
Pillow-dependent tests skip loudly when it's absent (generate-time dep)."""
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import scene  # noqa: E402
import present  # noqa: E402

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False


@unittest.skipUnless(HAVE_PIL, "Pillow not installed (generate-time dep)")
class ImageLabTests(unittest.TestCase):
    def _img(self):
        im = Image.new("RGB", (60, 60), "#3355B4")
        for x in range(30):
            for y in range(30):
                im.putpixel((x, y), (232, 117, 44))  # orange quadrant
        return im

    def test_sample_finds_the_dominant_colors(self):
        import image_lab
        pal = image_lab.sample(self._img(), k=4)
        self.assertTrue(any(h.upper().startswith("#33") or "55B4" in h.upper() for h in pal), pal)
        self.assertTrue(any("E8" in h.upper() or "75" in h.upper() for h in pal), pal)

    def test_palette_map_only_emits_palette_colors(self):
        import image_lab
        out = image_lab.palette_map(self._img(), ["#F7F2E3", "#131C33"])
        colors = {c for _, c in out.getcolors(maxcolors=10)}
        self.assertTrue(colors.issubset({(0xF7, 0xF2, 0xE3), (0x13, 0x1C, 0x33)}), colors)

    def test_duotone_maps_black_and_white_to_the_ramp_ends(self):
        import image_lab
        im = Image.new("RGB", (2, 1))
        im.putpixel((0, 0), (0, 0, 0))
        im.putpixel((1, 0), (255, 255, 255))
        out = image_lab.duotone(im, "#131C33", "#F7F2E3")
        self.assertEqual(out.getpixel((0, 0)), (0x13, 0x1C, 0x33))
        self.assertEqual(out.getpixel((1, 0)), (0xF7, 0xF2, 0xE3))

    def test_grain_is_deterministic(self):
        import image_lab
        a = image_lab.grain(self._img(), amount=10)
        b = image_lab.grain(self._img(), amount=10)
        self.assertEqual(list(a.getdata()), list(b.getdata()))


class SceneTests(unittest.TestCase):
    def test_wobble_is_deterministic_and_wobbles(self):
        pts = [(0, 0), (100, 0)]
        a = scene.wobble_path(pts, seed=5)
        b = scene.wobble_path(pts, seed=5)
        c = scene.wobble_path(pts, seed=6)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertGreater(a.count("L"), 3)  # subdivided, not one straight line

    def test_doc_shelf_is_dense(self):
        svg = scene.doc_shelf(0, 0, 300, 60)
        self.assertGreater(svg.count("<rect"), 15)   # many documents
        self.assertGreater(svg.count("<line"), 60)   # many rule lines

    def test_checker_floor_perspective_shrinks_far_rows(self):
        svg = scene.checker_floor(0, 0, 100, 100, cols=2, rows=2, perspective=0.5)
        import re
        heights = sorted({float(m) for m in re.findall(r'height="([\d.]+)"', svg)})
        self.assertGreater(heights[-1], heights[0])

    def test_filters_and_lamp_render(self):
        self.assertIn("feTurbulence", scene.grain_filter())
        self.assertIn("feDisplacementMap", scene.rough_filter())
        lamp = scene.bubble_lamp(50, 0, 40, 20, 24)
        self.assertIn("<ellipse", lamp)
        self.assertIn("opacity=\"0.10\"", lamp)  # the glow


class PresentTests(unittest.TestCase):
    SPEC = {
        "title": "T", "kicker": "K", "lede": "L",
        "sections": [{"no": "№1", "title": "S", "options": [
            {"label": "A", "name": "Opt A", "recommended": True,
             "html": "<div>ART</div>", "caption": "cap"}]}],
        "gate": {"title": "G", "combo": "A", "body": "B"},
        "appendix": [{"summary": "ev", "html": "<table></table>"}],
    }

    def test_structure_enforces_the_protocol(self):
        html = present.build(self.SPEC)
        self.assertIn("RECOMMENDED", html)          # visible recommendation
        self.assertIn('class="platenum">A<', html)  # stable labels
        self.assertIn("<details>", html)            # evidence in appendix
        self.assertIn("ART", html)                  # option rendered as given
        self.assertIn("№1", html)


if __name__ == "__main__":
    unittest.main()


class ImagegenTests(unittest.TestCase):
    def test_style_composition_carries_the_board_language(self):
        import imagegen
        s = imagegen.compose_style("midcentury-editorial")
        for must in ("gouache", "cream", "orange", "Never:"):
            self.assertIn(must, s, must)

    def test_brand_inks_dedupes_and_covers_both_themes(self):
        import enginelib, imagegen
        inks = imagegen.brand_inks(enginelib.load_brand())
        self.assertEqual(len(inks), len(set(inks)))
        self.assertGreater(len(inks), 15)
        self.assertTrue(all(i.startswith("#") for i in inks))

    def test_no_provider_exits_loudly_with_setup_instructions(self):
        import io, os, contextlib, imagegen
        env = {k: os.environ.pop(k, None) for k in
               ("IMAGEGEN_PROVIDER", "OPENAI_API_KEY", "REPLICATE_API_TOKEN")}
        try:
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                rc = imagegen.main(["a lamp", "--out", "/tmp/x.png"])
            self.assertEqual(rc, 1)
            self.assertIn("IMAGEGEN_PROVIDER", err.getvalue())
        finally:
            for k, v in env.items():
                if v is not None:
                    os.environ[k] = v
