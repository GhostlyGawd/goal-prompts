"""Tests for build.py's brief linter — the load-bearing quality bar.

DX.md (brief 14) flagged that the linter had no tests of its own, right after
its first version was caught counting Phase 4 report items as Phase 2 lenses.
These tests pin the house rules: run `python3 -m unittest discover -s tests`.
"""
import json
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

Start the report with today's date. If `X.md` already exists from a previous run, read it first and lead with what changed since.

## Rules
- Be good
- No example surface in this repo? Say so in a one-paragraph null report and stop — a null result is a valid finding.
- If a `reports/` directory exists at the repo root, write the report there instead of the root.
- Report only — end by asking which fixes to make
"""

DATED_LINE = ("Start the report with today's date. If `X.md` already exists "
              "from a previous run, read it first and lead with what changed since.\n\n")
REPORTS_DIR_LINE = ("- If a `reports/` directory exists at the repo root, "
                    "write the report there instead of the root.\n")
NULL_REPORT_LINE = ("- No example surface in this repo? Say so in a one-paragraph "
                    "null report and stop — a null result is a valid finding.\n")


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

    def test_reserved_output_filename_fails(self):
        # SECURITY.md, README.md & co. mean something else on GitHub — a
        # brief that writes one would shadow the repo's community files.
        for name in ("SECURITY.md", "README.md", "CHANGELOG.md"):
            v = build.lint(brief(
                body=GOOD_BODY.replace("`X.md`", f"`{name}`"), output=name))
            self.assertTrue(any("reserved" in x for x in v), (name, v))
        self.assertEqual(
            [x for x in build.lint(brief(
                body=GOOD_BODY.replace("`X.md`", "`SECURITY-AUDIT.md`"),
                output="SECURITY-AUDIT.md")) if "reserved" in x], [])

    def test_filename_prefix_must_match_id(self):
        v = build.lint(brief(_path="prompts/meta/98-example.md"))
        self.assertTrue(any("filename" in x for x in v), v)
        self.assertEqual(
            [x for x in build.lint(brief(_path="prompts/meta/99-example.md"))
             if "filename" in x], [])

    def test_phase_4_must_be_rerun_aware(self):
        # Every report opens with today's date and diffs against a prior run.
        body = GOOD_BODY.replace(DATED_LINE, "")
        v = build.lint(brief(body))
        self.assertTrue(any("already exists" in x for x in v), v)

    def test_fixer_is_exempt_from_the_rerun_rule(self):
        # 47's FIXLOG.md is append-only and each session entry is dated
        # already, so the dated re-run header would be redundant there.
        body = GOOD_BODY.replace(DATED_LINE, "")
        self.assertIn("47", build.DATED_REPORT_EXEMPT)
        self.assertEqual(
            [x for x in build.lint(brief(body, id="47"))
             if "already exists" in x], [])

    def test_rules_must_offer_the_reports_directory(self):
        # Root-pollution fix: a repo with a reports/ directory keeps its
        # root clean, so every brief must offer to write there.
        body = GOOD_BODY.replace(REPORTS_DIR_LINE, "")
        v = build.lint(brief(body))
        self.assertTrue(any("reports/" in x for x in v), v)

    def test_rules_must_include_the_null_report_escape(self):
        # A brief whose subject is absent must say so and stop, not invent
        # findings — the escape hatch is mandatory unless the subject is
        # universal (see NULL_REPORT_EXEMPT).
        body = GOOD_BODY.replace(NULL_REPORT_LINE, "")
        v = build.lint(brief(body))
        self.assertTrue(any("null report" in x for x in v), v)

    def test_universal_subjects_are_exempt_from_null_report(self):
        body = GOOD_BODY.replace(NULL_REPORT_LINE, "")
        for pid in sorted(build.NULL_REPORT_EXEMPT):
            self.assertEqual(
                [x for x in build.lint(brief(body, id=pid))
                 if "null report" in x], [], pid)

    def test_example_target_must_exist(self):
        v = build.lint(brief(example="/NO-SUCH-REPORT-EVER.md"))
        self.assertTrue(any("does not exist" in x for x in v), v)
        self.assertEqual(
            [x for x in build.lint(brief(example="/BUGS.md"))
             if "does not exist" in x], [])


class WindowChipTests(unittest.TestCase):
    # CRO NF4 (R22): merchandising `window` chips are date-gated. A plain
    # string stays an evergreen chip; a {"label", "months"} object is emitted
    # hidden with its months in a data attribute, and gp-detail.js unhides it
    # only while the viewer's month is inside the window — so a static build
    # can never show "January drop" in July, and the build itself stays
    # deterministic (no build-time clock in the output).
    def test_string_window_renders_an_evergreen_chip(self):
        html = build.window_chip("Featured drop")
        self.assertIn(">Featured drop<", html)
        self.assertNotIn("hidden", html)
        self.assertNotIn("data-window-months", html)

    def test_dated_window_renders_hidden_with_its_months(self):
        html = build.window_chip({"label": "January drop", "months": [12, 1]})
        self.assertIn(">January drop<", html)
        self.assertIn("hidden", html)
        self.assertIn('data-window-months="12,1"', html)

    def test_label_is_escaped(self):
        html = build.window_chip({"label": "<b>x</b>", "months": [1]})
        self.assertNotIn("<b>", html)

    def test_month_out_of_range_fails_the_build(self):
        with self.assertRaises(SystemExit):
            build.window_chip({"label": "Bad", "months": [0]})
        with self.assertRaises(SystemExit):
            build.window_chip({"label": "Bad", "months": [13]})

    def test_empty_months_fail_the_build(self):
        with self.assertRaises(SystemExit):
            build.window_chip({"label": "Bad", "months": []})

    def test_boolean_months_fail_the_build(self):
        # bool is an int subclass — [True] would serialize as
        # data-window-months="True", a silently dead chip. Fail loudly.
        with self.assertRaises(SystemExit):
            build.window_chip({"label": "Bad", "months": [True]})

    def test_missing_label_fails_the_build(self):
        with self.assertRaises(SystemExit):
            build.window_chip({"months": [1]})


class SortKeyTests(unittest.TestCase):
    def test_ids_sort_numerically_within_a_family(self):
        # String ids sort "106" < "45"; the catalog must order numerically.
        a, b = brief(id="45"), brief(id="106")
        self.assertEqual([p["id"] for p in sorted([b, a], key=build.sort_key)],
                         ["45", "106"])

    def test_family_order_still_wins(self):
        v = brief(id="106", family="Venture")   # first family in FAMILY_ORDER
        m = brief(id="45", family="Meta")
        self.assertEqual([p["id"] for p in sorted([m, v], key=build.sort_key)],
                         ["106", "45"])


class CatalogLintTests(unittest.TestCase):
    def test_two_briefs_sharing_an_output_fail(self):
        v = build.lint_catalog([brief(id="14"), brief(id="94")])  # both X.md
        self.assertTrue(any("X.md" in x and "14" in x and "94" in x
                            for x in v), v)

    def test_unique_outputs_pass(self):
        self.assertEqual(build.lint_catalog(
            [brief(id="14"), brief(id="94", output="Y.md")]), [])


class RelatedTests(unittest.TestCase):
    # `related:` front matter drives the cross-family "pairs well with" cards
    # on b/ pages; a dead id there would render a broken card, so the catalog
    # linter validates every reference.
    def test_related_ids_must_exist(self):
        v = build.lint_catalog([brief(id="07", related=["999"])])
        self.assertTrue(any("related" in x and "999" in x for x in v), v)

    def test_valid_related_ids_pass(self):
        v = build.lint_catalog([brief(id="07", related=["85"]),
                                brief(id="85", output="Y.md")])
        self.assertEqual([x for x in v if "related" in x], [])

    def test_self_reference_fails(self):
        v = build.lint_catalog([brief(id="07", related=["07"])])
        self.assertTrue(any("related" in x and "itself" in x for x in v), v)

    def test_parse_splits_the_related_list(self):
        import tempfile
        with tempfile.TemporaryDirectory(dir=build.ROOT) as d:
            p = Path(d) / "07-x.md"
            p.write_text('---\nid: "07"\ntitle: T\nfamily: Meta\nquestion: q\n'
                         'output: X.md\ntagline: t\nrelated: 85, 123\n---\nbody\n',
                         encoding="utf-8")
            self.assertEqual(build.parse(p)["related"], ["85", "123"])


class TaglineQuoteTests(unittest.TestCase):
    # command_md writes `description: "{tagline}"` into the plugin/installer
    # command front matter — a double quote in a tagline would break that
    # YAML, so parse() must reject it at the source.
    def test_tagline_with_double_quote_fails_at_parse(self):
        import tempfile
        with tempfile.TemporaryDirectory(dir=build.ROOT) as d:
            p = Path(d) / "07-x.md"
            p.write_text('---\nid: "07"\ntitle: T\nfamily: Meta\nquestion: q\n'
                         'output: X.md\ntagline: says "quoted" things\n---\nbody\n',
                         encoding="utf-8")
            with self.assertRaises(SystemExit) as cm:
                build.parse(p)
            self.assertIn("tagline", str(cm.exception))

    def test_command_md_yaml_stays_intact(self):
        cmd = build.command_md(brief())
        self.assertIn('description: "An example brief."', cmd)


class ConductorTests(unittest.TestCase):
    # The 16-stage cap is one policy in three places (build.py, mcp/server.cjs,
    # template.html — scripts/mcp-smoke.cjs guards the text parity). Here we
    # pin that build.py itself refuses to emit a conductor over the cap, so a
    # family growing past 16 briefs fails the build loudly instead of drifting
    # past what make_conductor will compose.
    def _pb(self, n):
        ids = [f"{i:02d}" for i in range(n)]
        by_id = {i: brief(id=i) for i in ids}
        return {"name": "Big", "desc": "d", "ids": ids}, by_id

    def test_sixteen_stages_pass(self):
        pb, by_id = self._pb(16)
        self.assertIn("# Playbook: Big (conductor)", build.conductor(pb, by_id))

    def test_seventeen_stages_fail_the_build(self):
        pb, by_id = self._pb(17)
        with self.assertRaises(SystemExit) as cm:
            build.conductor(pb, by_id)
        self.assertIn("16", str(cm.exception))

    def test_conductor_text_documents_the_cap_and_fallbacks(self):
        pb, by_id = self._pb(2)
        text = build.conductor(pb, by_id)
        self.assertIn("A conductor caps at 16 stages", text)
        self.assertIn("retry once", text)
        self.assertIn("subagents or fresh sessions", text)
        self.assertIn("at the repo root or in `reports/`", text)
        # the local-command fallback names both real install shapes: the
        # plugin's /goal:<slug> and the curl installer's /goal-<slug>
        self.assertIn("/goal:<slug> (or /goal-<slug>) command", text)


class FamilyIconTests(unittest.TestCase):
    # Root fix for the family icon/chart drift: every family in FAMILY_ORDER
    # must have a FAM_ICON entry AND a matching <symbol> in template.html,
    # enforced at build time so a new family can't ship iconless again.
    def setUp(self):
        self.tpl = (build.ROOT / "template.html").read_text(encoding="utf-8")

    def test_live_template_covers_every_family(self):
        self.assertEqual(build.lint_family_icons(self.tpl), [])

    def test_missing_fam_icon_entry_is_reported(self):
        broken = self.tpl.replace('Trust:"i-trust",', "")
        v = build.lint_family_icons(broken)
        self.assertTrue(any("Trust" in x and "FAM_ICON" in x for x in v), v)

    def test_missing_symbol_is_reported(self):
        broken = self.tpl.replace('<symbol id="i-trust"', '<symbol id="i-trustx"')
        v = build.lint_family_icons(broken)
        self.assertTrue(any("i-trust" in x and "symbol" in x for x in v), v)


class TokensTests(unittest.TestCase):
    # Light theme must darken every family accent: the raw hues sit at
    # 1.3-1.9:1 on the light panels. These pin (a) that TOKENS_CSS carries a
    # light-scoped color-mix override for every family, in both the
    # data-theme and the prefers-color-scheme form, and (b) the arithmetic:
    # the mix leaves every family at >= 3:1 against the lightest and darkest
    # light-theme surfaces, so nobody can nudge the percentage below AA-large.
    LIGHT_SURFACES = ("FCFBF9", "F4F3EF", "EFEEE7")  # --panel, --ink, --panel-2

    @staticmethod
    def _lum(rgb):
        def lin(c):
            c /= 255
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        r, g, b = rgb
        return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

    @classmethod
    def _ratio(cls, a, b):
        la, lb = cls._lum(a), cls._lum(b)
        return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

    def test_every_family_has_light_theme_overrides(self):
        for fam in build.FAMILY_ORDER:
            rule = (f".f-{fam.lower()}{{--fc:color-mix(in srgb,"
                    f"{build.FAMILY_COLORS[fam]} {build.FAMILY_MIX_LIGHT}%,black)}}")
            self.assertIn(f':root[data-theme="light"] {rule}', build.TOKENS_CSS, fam)
            self.assertIn(f":root:not([data-theme]) {rule}", build.TOKENS_CSS, fam)

    def test_light_mix_meets_3_to_1_on_every_light_surface(self):
        p = build.FAMILY_MIX_LIGHT / 100
        for fam, hexv in build.FAMILY_COLORS.items():
            raw = tuple(int(hexv[i:i + 2], 16) for i in (1, 3, 5))
            mixed = tuple(c * p for c in raw)  # color-mix(in srgb, C p%, black)
            for surface in self.LIGHT_SURFACES:
                bg = tuple(int(surface[i:i + 2], 16) for i in (0, 2, 4))
                r = self._ratio(mixed, bg)
                self.assertGreaterEqual(
                    r, 3.0, f"{fam} at {build.FAMILY_MIX_LIGHT}% on #{surface}: {r:.2f}")


class ParseTests(unittest.TestCase):
    def test_missing_front_matter_exits(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "00-bad.md"
            p.write_text("# no front matter here\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                build.parse(p)

    def _front_matter(self, pid):
        return (f'---\nid: "{pid}"\ntitle: T\nfamily: Meta\nquestion: q\n'
                f'output: X.md\ntagline: t\n---\nbody\n')

    def test_malformed_id_fails_at_parse_time_with_a_friendly_message(self):
        # A typoed id used to surface as a ValueError traceback from
        # sort_key (the sort runs before the linter); parse must catch it.
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            for bad in ("4a", "7", "1024", "07 "):
                p = Path(d) / "07-bad.md"
                p.write_text(self._front_matter(bad), encoding="utf-8")
                with self.assertRaises(SystemExit) as cm:
                    build.parse(p)
                self.assertIn("id", str(cm.exception), bad)
                self.assertIn(bad.strip(), str(cm.exception), bad)

    def test_well_formed_ids_parse(self):
        import tempfile
        # under ROOT: parse() records the path relative to the repo root
        with tempfile.TemporaryDirectory(dir=build.ROOT) as d:
            for good in ("07", "99", "135"):
                p = Path(d) / f"{good}-good.md"
                p.write_text(self._front_matter(good), encoding="utf-8")
                self.assertEqual(build.parse(p)["id"], good)


# The detail pages (b/<id>, p/<key>) are generated from the same brief bodies
# the linter guards, so their structure can never drift from the prompts. These
# pin the parser that feeds them.
BODY = """# Goal: Demo

Intro one, the mission.

Intro two, the constraint.

## Phase 1 — Explore
- look around

## Phase 2 — Audit through 3 lenses
1. **Alpha** — the first lens
2. **Beta** — the second lens
3. **Gamma** — the third lens

## Phase 3 — Curate
- rank things

## Phase 4 — Report
Create `X.md` at repo root:
1. **Summary** — a report section
2. **Findings** — another one

## Rules
- Evidence or it doesn't exist
- Report only — end by asking which fixes to make
"""


class BriefPartsTests(unittest.TestCase):
    def setUp(self):
        self.parts = build.brief_parts(BODY)

    def test_intro_drops_goal_header(self):
        self.assertIn("Intro one", self.parts["intro"])
        self.assertIn("Intro two", self.parts["intro"])
        self.assertNotIn("# Goal", self.parts["intro"])

    def test_four_phases_in_order_with_names(self):
        self.assertEqual([p["n"] for p in self.parts["phases"]], [1, 2, 3, 4])
        self.assertEqual(self.parts["phases"][0]["name"], "Explore")
        self.assertTrue(self.parts["phases"][0]["gist"])

    def test_phase_2_lenses_extracted(self):
        self.assertEqual([n for n, _ in self.parts["lenses"]],
                         ["Alpha", "Beta", "Gamma"])
        self.assertEqual(self.parts["lenses"][0][1], "the first lens")

    def test_phase_4_report_sections_extracted(self):
        self.assertEqual([n for n, _ in self.parts["report"]],
                         ["Summary", "Findings"])

    def test_rules_extracted(self):
        self.assertTrue(any("Report only" in r for r in self.parts["rules"]))

    def test_prose_phase_2_yields_no_lenses(self):
        prose = BODY.replace(
            "1. **Alpha** — the first lens\n2. **Beta** — the second lens\n"
            "3. **Gamma** — the third lens",
            "- Present findings as prose, then stop.")
        self.assertEqual(build.brief_parts(prose)["lenses"], [])

    def test_gist_is_a_clean_sentence(self):
        # editorial voice: no dangling colon, capitalized, ends like a sentence
        self.assertEqual(build._gist("Create `X.md` at repo root:"),
                         "Create X.md at repo root.")
        self.assertEqual(build._gist("- look around"), "Look around.")

    def test_gist_skips_the_operator_gate_line(self):
        gist = build._gist("Report only — end by asking which to fix.\n"
                           "Show the findings menu.")
        self.assertEqual(gist, "Show the findings menu.")

    def test_prose_phase_2_drops_the_operator_gate_line(self):
        prose = BODY.replace(
            "1. **Alpha** — the first lens\n2. **Beta** — the second lens\n"
            "3. **Gamma** — the third lens",
            "Present findings as prose.\n\n"
            "Report only — end by asking which selection to build.")
        parts = build.brief_parts(prose)
        p2 = next(ph for ph in parts["phases"] if ph["n"] == 2)
        self.assertIn("Present findings as prose.", p2["prose"])
        self.assertNotIn("end by asking", p2["prose"])


class RenderHelperTests(unittest.TestCase):
    def test_esc(self):
        self.assertEqual(build.esc("a<b>&c"), "a&lt;b&gt;&amp;c")

    def test_md_inline_bold_and_code(self):
        self.assertEqual(build.md_inline("a **b** `c`"),
                         "a <strong>b</strong> <code>c</code>")

    def test_md_block_paragraphs_and_lists(self):
        html = build.md_block("A para.\n\n- one\n- two")
        self.assertIn("<p>A para.</p>", html)
        self.assertIn("<li>one</li>", html)
        self.assertIn("<ul>", html)

    def test_cmd_html_id_is_deterministic(self):
        # the copy-source id must be stable across runs (deterministic build)
        self.assertEqual(build.cmd_html("npm test"), build.cmd_html("npm test"))


class WorkflowFileTests(unittest.TestCase):
    # The stdlib has no YAML parser, so this is a smoke check, not validation:
    # the CI workflow must exist and run the real gate, and every workflow
    # file (live or .example) must be non-empty with the skeleton keys.
    def _files(self):
        gh = build.ROOT / ".github"
        return sorted(list(gh.glob("*.yml")) +
                      list((gh / "workflows").glob("*.yml")))

    def test_ci_workflow_is_active_and_runs_the_gate(self):
        ci = build.ROOT / ".github" / "workflows" / "ci.yml"
        self.assertTrue(ci.exists(), "CI must live at .github/workflows/ci.yml")
        self.assertIn("scripts/check", ci.read_text(encoding="utf-8"))

    def test_ci_drift_check_is_airtight(self):
        # The drift step must catch ANY modified tracked file (full git diff,
        # not a file subset) AND any untracked new output (porcelain check) —
        # a new brief's raw/NNN.md was invisible to the old subset diff.
        text = (build.ROOT / ".github" / "workflows" /
                "ci.yml").read_text(encoding="utf-8")
        self.assertIn("git diff --exit-code", text)
        self.assertIn('test -z "$(git status --porcelain)"', text)
        self.assertNotIn("git diff --exit-code index.html", text,
                         "file-subset drift diff is back; keep it full")

    def test_workflow_files_carry_the_skeleton(self):
        files = self._files()
        self.assertTrue(files, "no workflow files found under .github/")
        for f in files:
            text = f.read_text(encoding="utf-8")
            self.assertTrue(text.strip(), f.name)
            for key in ("on:", "jobs:", "steps:"):
                self.assertIn(key, text, f.name)


class PluginTests(unittest.TestCase):
    # The Claude Code plugin (plugin/, listed by .claude-plugin/marketplace.json)
    # is a build output: commands/ is generated from the same briefs as the
    # command archives, and plugin.json's version tracks package.json — these
    # pin that none of it can drift from the catalog.
    def test_plugin_commands_cover_every_brief(self):
        briefs = list((build.ROOT / "prompts").rglob("*.md"))
        cmds = list((build.ROOT / "plugin" / "commands").glob("*.md"))
        self.assertEqual(len(cmds), len(briefs))

    def test_plugin_command_carries_the_raw_brief_body(self):
        cmd = (build.ROOT / "plugin" / "commands" / "bug-hunt.md").read_text(
            encoding="utf-8")
        fm, body = cmd.split("---", 2)[1:]
        self.assertIn("description:", fm)
        raw = (build.ROOT / "raw" / "01.md").read_text(encoding="utf-8")
        self.assertEqual(body.strip(), raw.strip())

    def test_plugin_manifest_tracks_package_version(self):
        manifest = json.loads((build.ROOT / "plugin" / ".claude-plugin" /
                               "plugin.json").read_text(encoding="utf-8"))
        pkg = json.loads((build.ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "goal")
        self.assertEqual(manifest["version"], pkg["version"])

    def test_marketplace_lists_the_goal_plugin(self):
        market = json.loads((build.ROOT / ".claude-plugin" /
                             "marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(market["name"], "goal-prompts")
        self.assertEqual(market["owner"]["name"], "GhostlyGawd")
        entry = [pl for pl in market["plugins"] if pl["name"] == "goal"][0]
        self.assertEqual(entry["source"], "./plugin")

    def test_plugin_descriptions_name_a_first_command(self):
        # ACTIVATION AN5 (R15): the install/browse surfaces name a concrete
        # first command instead of dropping the user into 141 equal choices.
        manifest = json.loads((build.ROOT / "plugin" / ".claude-plugin" /
                               "plugin.json").read_text(encoding="utf-8"))
        self.assertIn("/goal:audit-triage", manifest["description"])
        market = json.loads((build.ROOT / ".claude-plugin" /
                             "marketplace.json").read_text(encoding="utf-8"))
        entry = [pl for pl in market["plugins"] if pl["name"] == "goal"][0]
        self.assertIn("/goal:audit-triage", entry["description"])


class DetailPageAnalyticsTests(unittest.TestCase):
    # R02 (FUNNEL §4.1 / RETENTION R7): the 176 side-door pages carry the same
    # insights script + va shim as the landing page, so detail-page entries,
    # copies, and returns stop being invisible.
    def _brief_html(self):
        p = build.parse(next(iter(sorted((build.ROOT / "prompts").rglob("*.md")))))
        return build.brief_detail(p, [], [])

    def test_detail_head_carries_the_insights_script(self):
        html = self._brief_html()
        self.assertIn("/_vercel/insights/script.js", html)
        self.assertIn("window.va=window.va||", html)   # the queue shim

    def test_detail_head_carries_unfurl_metadata(self):
        # SEO-9 (R30): og:site_name + image dimensions/alt + twitter tags
        html = self._brief_html()
        self.assertIn('property="og:site_name" content="Goal Prompts"', html)
        self.assertIn('property="og:image:width" content="1200"', html)
        self.assertIn('property="og:image:height" content="630"', html)
        self.assertIn('property="og:image:alt"', html)
        self.assertIn('name="twitter:title"', html)
        self.assertIn('name="twitter:description"', html)

    def test_install_step_copy_buttons_are_distinguishable(self):
        # B2 review carry-over: the .cp buttons all said just "copy" to a
        # screen reader — each carries a distinguishing aria-label now.
        html = self._brief_html()
        self.assertIn('aria-label="copy step 1"', html)
        self.assertIn('aria-label="copy step 2"', html)
        self.assertIn('aria-label="copy raw brief URL"', html)

    def test_conductor_copy_buttons_carry_key_and_raw_fallback(self):
        # gp-detail.js needs the playbook key (copy_conductor event) and the
        # raw conductor URL (clipboard-failure link fallback) on the button.
        prompts = [build.parse(f)
                   for f in sorted((build.ROOT / "prompts").rglob("*.md"))]
        by_id = {p["id"]: p for p in prompts}
        pb = {"key": "t", "name": "Test PB", "desc": "d",
              "ids": [prompts[0]["id"]], "conductor": "c"}
        html = build.playbook_detail(pb, by_id)
        self.assertIn('data-pb="t"', html)
        self.assertIn('data-raw="' + build.BASE + '/raw/playbook-t.md"', html)


class SitemapLastmodTests(unittest.TestCase):
    # SEO-7 (R30): <lastmod> must come from stable inputs, never the build
    # clock — CI rebuilds and diffs, so an unchanged rebuild must be
    # byte-identical.
    def test_dates_persist_while_content_is_unchanged(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            state = Path(d) / "state.json"
            first = build.sitemap_lastmod({"/x": b"one"}, state)
            again = build.sitemap_lastmod({"/x": b"one"}, state)
            self.assertEqual(first, again)

    def test_changed_content_moves_the_date(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            state = Path(d) / "state.json"
            state.write_text(json.dumps(
                {"/x": {"h": "stale-hash", "d": "2001-01-01"}}), encoding="utf-8")
            out = build.sitemap_lastmod({"/x": b"two"}, state)
            self.assertNotEqual(out["/x"], "2001-01-01")

    def test_unchanged_hash_keeps_the_recorded_date(self):
        import tempfile, hashlib
        with tempfile.TemporaryDirectory() as d:
            state = Path(d) / "state.json"
            h = hashlib.sha1(b"one").hexdigest()[:16]
            state.write_text(json.dumps(
                {"/x": {"h": h, "d": "2001-01-01"}}), encoding="utf-8")
            out = build.sitemap_lastmod({"/x": b"one"}, state)
            self.assertEqual(out["/x"], "2001-01-01")

    def test_generated_sitemap_carries_a_lastmod_per_url(self):
        import re as _re
        xml = (build.ROOT / "sitemap.xml").read_text(encoding="utf-8")
        locs = xml.count("<loc>")
        mods = _re.findall(r"<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>", xml)
        self.assertGreater(locs, 0)
        self.assertEqual(locs, len(mods))


class StaticHeadTests(unittest.TestCase):
    # R30: SEO-4 (og/canonical on /examples/), SEO-5 (canonicals on
    # studio/vitals — the clean URLs, per vercel.json cleanUrls), SEO-9
    # (site_name + image dims + twitter tags on the hand-authored heads).
    def _head(self, name):
        text = (build.ROOT / name).read_text(encoding="utf-8")
        return text.split("</head>")[0]

    def test_examples_page_has_og_twitter_and_canonical(self):
        head = self._head("examples/index.html")
        self.assertIn('property="og:title"', head)
        self.assertIn('property="og:image"', head)
        self.assertIn('name="twitter:card"', head)
        self.assertIn('rel="canonical" href="https://goal-prompts.vercel.app/examples/"',
                      head)

    def test_studio_and_vitals_have_clean_url_canonicals(self):
        self.assertIn('rel="canonical" href="https://goal-prompts.vercel.app/studio"',
                      self._head("studio.html"))
        self.assertIn('rel="canonical" href="https://goal-prompts.vercel.app/vitals"',
                      self._head("vitals.html"))

    def test_hand_authored_heads_carry_the_seo9_tags(self):
        for name in ("template.html", "studio.html", "vitals.html",
                     "examples/index.html"):
            head = self._head(name)
            self.assertIn('property="og:site_name" content="Goal Prompts"', head,
                          name)
            self.assertIn('property="og:image:width" content="1200"', head, name)
            self.assertIn('property="og:image:height" content="630"', head, name)
            self.assertIn('name="twitter:title"', head, name)
            self.assertIn('name="twitter:description"', head, name)

    def test_landing_install_copy_buttons_are_distinguishable(self):
        html = (build.ROOT / "template.html").read_text(encoding="utf-8")
        self.assertIn('id="copyinstall" aria-label="copy step 1"', html)
        self.assertIn('id="copyinstall2" aria-label="copy step 2"', html)


class DetailPageTests(unittest.TestCase):
    def _prompts(self):
        return [build.parse(f)
                for f in sorted((build.ROOT / "prompts").rglob("*.md"))]

    def test_brief_detail_renders(self):
        p = self._prompts()[0]
        html = build.brief_detail(p, [], [])
        self.assertIn("<title>", html)
        self.assertIn(p["title"], html)
        self.assertIn(f'/b/{p["id"]}', html)          # canonical
        self.assertIn("rawbody", html)                # the copy source
        self.assertIn("js/gp-detail.js", html)        # shared detail behavior
        self.assertIn('data-ctx="1"', html)           # Operator context rides along

    def test_brief_detail_renders_related_cards(self):
        prompts = self._prompts()
        p, r = prompts[0], prompts[1]
        html = build.brief_detail(p, [], [], related=[r])
        self.assertIn("Pairs well with", html)
        self.assertIn(f'/b/{r["id"]}', html)
        self.assertNotIn("Pairs well with", build.brief_detail(p, [], []))

    def test_playbook_detail_has_per_step_copy(self):
        prompts = self._prompts()
        by_id = {p["id"]: p for p in prompts}
        pb = {"key": "t", "name": "Test PB", "desc": "d",
              "ids": [prompts[0]["id"]], "conductor": "c"}
        html = build.playbook_detail(pb, by_id)
        self.assertIn(f'data-fetch="/raw/{prompts[0]["id"]}.md"', html)
        self.assertIn("stepcopy", html)

    def test_playbook_detail_renders(self):
        prompts = self._prompts()
        by_id = {p["id"]: p for p in prompts}
        pb = {"key": "t", "name": "Test PB", "desc": "d",
              "ids": [prompts[0]["id"]], "conductor": "the conductor text"}
        html = build.playbook_detail(pb, by_id)
        self.assertIn("Copy the conductor", html)
        self.assertIn("the conductor text", html)     # embedded for copy


class ChangelogTests(unittest.TestCase):
    """R36 (RETENTION R10): CHANGELOG.md publishes as /changelog — the one URL
    that says what's new to surfaces that pin their catalog at install time."""

    MD = ("# Changelog\n"
          "\n"
          "## 0.2.0 — 2026-01-02\n"
          "- added a **bold** thing with `code`\n"
          "- second item\n"
          "\n"
          "## 0.1.0 — 2026-01-01\n"
          "First release.\n")

    def test_changelog_page_emits_every_release(self):
        html = build.changelog_page(self.MD)
        self.assertIn("0.2.0", html)
        self.assertIn("0.1.0", html)
        self.assertIn("<li>added a <strong>bold</strong> thing with "
                      "<code>code</code></li>", html)
        self.assertIn(f'<link rel="canonical" href="{build.BASE}/changelog">',
                      html)

    def test_newest_release_leads_the_page(self):
        html = build.changelog_page(self.MD)
        self.assertLess(html.index("0.2.0"), html.index("0.1.0"))

    def test_changelog_content_is_escaped(self):
        html = build.changelog_page(
            "# Changelog\n\n## 0.1.0\n- evil <script>alert(1)</script> & co\n")
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt; &amp; co", html)
        self.assertNotIn("<script>alert(1)</script>", html)

    def test_changelog_without_releases_fails_the_build(self):
        with self.assertRaises(SystemExit):
            build.changelog_page("# Changelog\n\nnothing released yet\n")

    def test_live_sitemap_lists_changelog(self):
        # scripts/check builds before testing, so the committed sitemap is live
        sitemap = (Path(build.__file__).resolve().parent
                   / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn(f"<loc>{build.BASE}/changelog</loc>", sitemap)


if __name__ == "__main__":
    unittest.main()
