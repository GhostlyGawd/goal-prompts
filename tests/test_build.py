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

    def test_playbook_detail_renders(self):
        prompts = self._prompts()
        by_id = {p["id"]: p for p in prompts}
        pb = {"key": "t", "name": "Test PB", "desc": "d",
              "ids": [prompts[0]["id"]], "conductor": "the conductor text"}
        html = build.playbook_detail(pb, by_id)
        self.assertIn("Copy the conductor", html)
        self.assertIn("the conductor text", html)     # embedded for copy


if __name__ == "__main__":
    unittest.main()
