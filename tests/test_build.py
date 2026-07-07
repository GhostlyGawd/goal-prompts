"""Tests for build.py's brief linter — the load-bearing quality bar.

DX.md (brief 14) flagged that the linter had no tests of its own, right after
its first version was caught counting Phase 4 report items as Phase 2 lenses.
These tests pin the house rules: run `python3 -m unittest discover -s tests`.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import build  # noqa: E402

GOOD_BODY = """# Goal: Example

You are working inside this repo. Mission: exemplify.

## Phase 1 — Explore
- Look around.

## Phase 2 — Audit through 4 lenses
1. **First** — a lens
2. **Second** — a lens
3. **Third** — a lens
4. **Fourth** — a lens

## Phase 3 — Curate
- Rank things.

## Phase 4 — Report
Create `X.md` at repo root:
1. **Sources** — a report section, numbered and bold like the lenses
2. **Backlog** — same shape as a lens on purpose
3. **Themes** — the linter must not count these
4. **Milestones** — as Phase 2 lenses
5. **Merge log** — five of them, outside the 4-12 range alone

## Rules
- Be good
- Report only — end by asking which fixes to make
"""


def brief(body=GOOD_BODY, **overrides):
    p = {"id": "99", "title": "Example", "family": "Meta", "question": "q",
         "output": "X.md", "tagline": "An example brief.",
         "body": body, "chars": len(body)}
    p.update(overrides)
    return p


class LintTests(unittest.TestCase):
    def test_clean_brief_passes(self):
        self.assertEqual(build.lint(brief()), [])

    def test_oversized_body_fails(self):
        v = build.lint(brief(chars=build.LIMIT + 1))
        self.assertTrue(any(f"max {build.LIMIT}" in x for x in v), v)

    def test_missing_phase_fails(self):
        body = GOOD_BODY.replace("## Phase 3 — Curate", "## Curate")
        v = build.lint(brief(body))
        self.assertTrue(any("Phase 3" in x for x in v), v)

    def test_missing_rules_section_fails(self):
        body = GOOD_BODY.replace("## Rules", "## Guidelines")
        v = build.lint(brief(body))
        self.assertTrue(any("Rules" in x for x in v), v)

    def test_missing_ask_first_ending_fails(self):
        body = GOOD_BODY.replace(
            "Report only — end by asking which fixes to make", "Just report.")
        v = build.lint(brief(body))
        self.assertTrue(any("ask-first" in x for x in v), v)

    def test_lens_count_scoped_to_phase_2(self):
        # The regression DX.md documented: GOOD_BODY has 4 lenses in Phase 2
        # and 5 numbered-bold items in Phase 4. Counting across phases would
        # see 9 (or 5) and misfire; scoped counting sees 4 and passes.
        self.assertEqual(
            [x for x in build.lint(brief()) if "lenses" in x], [])

    def test_too_few_lenses_fails(self):
        body = GOOD_BODY.replace(
            "3. **Third** — a lens\n4. **Fourth** — a lens\n", "")
        v = build.lint(brief(body))
        self.assertTrue(any("lenses" in x for x in v), v)

    def test_prose_phase_2_is_allowed(self):
        # Zero numbered-bold lines in Phase 2 is legal (e.g. brief 47);
        # the 4-12 rule applies only when the lens pattern is used at all.
        body = GOOD_BODY.replace(
            "1. **First** — a lens\n2. **Second** — a lens\n"
            "3. **Third** — a lens\n4. **Fourth** — a lens",
            "- Present findings as prose, then stop.")
        self.assertEqual(
            [x for x in build.lint(brief(body)) if "lenses" in x], [])

    def test_output_must_look_like_a_report_file(self):
        v = build.lint(brief(output="notes.txt"))
        self.assertTrue(any("REPORT.md" in x for x in v), v)

    def test_body_must_name_its_report(self):
        # The report grammar's anchor: Phase 4 names the file it writes,
        # so the Studio, the Fixer, and conductors can rely on it.
        body = GOOD_BODY.replace("Create `X.md` at repo root:", "Write a file:")
        v = build.lint(brief(body))
        self.assertTrue(any("at repo root" in x for x in v), v)

    def test_overlong_tagline_fails(self):
        v = build.lint(brief(tagline="x" * 171))
        self.assertTrue(any("tagline" in x for x in v), v)

    def test_example_must_be_root_relative(self):
        v = build.lint(brief(example="BUGS.md"))
        self.assertTrue(any("root-relative" in x for x in v), v)
        self.assertEqual(
            [x for x in build.lint(brief(example="/BUGS.md"))
             if "root-relative" in x], [])


class ParseTests(unittest.TestCase):
    def test_missing_front_matter_exits(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "00-bad.md"
            p.write_text("# no front matter here\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                build.parse(p)


if __name__ == "__main__":
    unittest.main()
