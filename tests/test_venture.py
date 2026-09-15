"""Disposable-repository regression scenarios for Venture's structural contract."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import shutil
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("venture_check", ROOT / "workflows/venture_check.py")
vc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vc)


class VentureRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "reports").mkdir()
        (self.root / "reports/INDEX.md").write_text("# run-test\nNext: select a candidate\n")
        self.state = {"schema_version": 1, "run_id": "run-test", "status": "active",
            "scope": {"id": "venture-a", "revision": 1}, "operator": {"time": "5h/week"},
            "criteria": [{"id": "pain", "threshold": "recurring material cost",
                "evidence": "independent buyer evidence", "recorded_at": "2026-09-14",
                "exposure": "before conclusions"}], "decisions": [],
            "commit_preference": "no", "next_step": "select a candidate",
            "stages": [{"brief": "60", "output": "reports/OPPORTUNITIES.md",
                "status": "pending", "inputs": {}, "note": ""}]}

    def save(self):
        (self.root / "reports/venture-run.json").write_text(json.dumps(self.state))

    def errors(self, final=False):
        self.save()
        return vc.validate(self.root, final)

    def complete(self, i=0, status="complete"):
        stage = self.state["stages"][i]
        stage["status"] = status
        text = (f"2026-09-14\n# Research\nVenture · stage {i+1}/{len(self.state['stages'])} · brief {stage['brief']}\n"
                f"Run: run-test\nScope: {self.state['scope']['id']}@{self.state['scope']['revision']}\n"
                f"Brief: {stage['brief']}\nStatus: {status}\n")
        text += "\n".join("## " + h + "\nFixture content.\n" for h in
                           ("Scope", "Findings", "Evidence", "Counterevidence", "Next steps"))
        path = self.root / stage["output"]
        path.write_text(text)
        stage["report_sha256"] = vc.digest(path)
        stage["source"] = {"url": "fixture://brief/" + stage["brief"],
                           "retrieved_at": "2026-09-14", "sha256": "a" * 64}

    def test_empty_repo_preflight_and_final_gate(self):
        self.assertEqual(self.errors(), [])
        self.assertTrue(self.errors(final=True))

    def test_complete_run_and_read_only_cli(self):
        self.complete()
        self.state["status"] = "complete"
        self.assertEqual(self.errors(True), [])
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = subprocess.run(["python3", str(ROOT / "workflows/venture_check.py"), str(self.root), "--final"], capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_missing_empty_and_stale_report(self):
        self.complete()
        path = self.root / self.state["stages"][0]["output"]
        for content in ("", "unrelated old report"):
            path.write_text(content)
            self.assertTrue(self.errors())
        path.unlink()
        self.assertTrue(self.errors())

    def test_pivot_invalidates_old_scope(self):
        self.complete()
        self.state["scope"]["revision"] = 2
        self.assertTrue(any("Scope:" in e for e in self.errors()))

    def test_dependency_change_and_missing_dependency(self):
        self.state["stages"].append({"brief": "61", "output": "reports/NICHE.md", "status": "pending", "inputs": {}, "note": ""})
        self.complete(0)
        self.complete(1)
        self.assertTrue(any("missing prior" in e for e in self.errors()))
        self.state["stages"][1]["inputs"] = {"reports/OPPORTUNITIES.md": self.state["stages"][0]["report_sha256"]}
        self.assertEqual(self.errors(), [])
        with (self.root / "reports/OPPORTUNITIES.md").open("a") as f:
            f.write("new selection")
        self.assertTrue(any("stale input" in e for e in self.errors()))

    def test_stop_dispositions_and_null(self):
        self.complete(status="null")
        self.state["stages"][0]["note"] = "No operator constraints after intake"
        self.state["status"] = "stopped"
        self.assertEqual(self.errors(True), [])
        self.state["status"] = "complete"
        self.assertTrue(self.errors(True))

    def test_failed_fetch_recoverable_pause(self):
        self.state["stages"][0].update(status="failed", note="fetch and fallback unavailable")
        self.state["status"] = "paused"
        self.assertEqual(self.errors(), [])

    def test_null_and_failed_inputs_cannot_advance(self):
        self.state["stages"].append({"brief": "61", "output": "reports/NICHE.md",
            "status": "running", "inputs": {}, "note": ""})
        self.state["stages"][0].update(status="failed", note="brief unavailable")
        self.assertTrue(any("unresolved earlier" in e for e in self.errors()))

    def test_parallel_stages_and_duplicate_outputs_rejected(self):
        self.state["stages"][0]["status"] = "running"
        self.state["stages"].append(copy.deepcopy(self.state["stages"][0]))
        errors = self.errors()
        self.assertTrue(any("duplicate" in e for e in errors))
        self.assertTrue(any("sequentially" in e for e in errors))

    def test_wrong_venture_and_discovery_scope(self):
        self.state["stages"][0].update(brief="62", output="reports/DEMAND.md")
        self.state["scope"]["id"] = "discovery"
        self.complete()
        self.assertTrue(any("selection" in e for e in self.errors()))

    def test_unsafe_paths_and_symlink(self):
        for path in ("../OUTSIDE.md", "/tmp/OUTSIDE.md", "reports/../OUTSIDE.md", "reports/INDEX.md"):
            self.state["stages"][0]["output"] = path
            self.assertTrue(self.errors())
        self.state["stages"][0]["output"] = "reports/OPPORTUNITIES.md"
        (self.root / "reports/OPPORTUNITIES.md").symlink_to("/tmp/OUTSIDE.md")
        self.assertTrue(self.errors())

    def test_malformed_state_does_not_crash(self):
        original = copy.deepcopy(self.state)
        for key, value in (("stages", [None]), ("scope", []), ("criteria", [None]), ("operator", "x"), ("status", [])):
            self.state = copy.deepcopy(original)
            self.state[key] = value
            self.assertTrue(self.errors())
        for run_status in ("active", "complete", "stopped"):
            for key in ("brief", "status"):
                self.state = copy.deepcopy(original)
                self.state["status"] = run_status
                self.state["stages"][0][key] = []
                self.assertTrue(self.errors())

    def test_dirty_tree_untouched(self):
        (self.root / "app.py").write_text("user changes\n")
        self.assertEqual(self.errors(), [])
        self.assertEqual((self.root / "app.py").read_text(), "user changes\n")


class VentureDistributionTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("node"), "Node is optional")
    def test_all_entry_points_parity(self):
        import build
        catalog = json.loads((ROOT / "catalog.json").read_text())
        by_id = {p["id"]: p for p in catalog["briefs"]}
        for ids in ([str(i) for i in range(60, 68)], ["62", "67"], ["60", "47"], ["67"], ["60", "61", "65"]):
            pb = {"name": "Trial {{BASE}}", "desc": "Scope test", "ids": ids}
            expected = build.conductor(pb, by_id)
            js = "const c=require('./js/catalog-core.js'); const cat=require('./catalog.json'); process.stdout.write(c.makeConductor(process.argv[1], 'Scope test', JSON.parse(process.argv[2]), Object.fromEntries(cat.briefs.map(p=>[p.id,p])), cat.base));"
            actual = subprocess.check_output(["node", "-e", js, pb["name"], json.dumps(ids)], cwd=ROOT, text=True)
            self.assertEqual(expected, actual)
            requests = [{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "make_conductor", "arguments": {"name": pb["name"], "desc": pb["desc"], "ids": ids}}}]
            response = subprocess.run(["node", "mcp/server.cjs"], input="\n".join(json.dumps(r) for r in requests)+"\n", text=True, capture_output=True, cwd=ROOT, check=True)
            payload = json.loads(response.stdout.splitlines()[0])
            mcp_pb = dict(pb, desc=f"A custom sequence of {len(ids)} brief" + ("s" if len(ids) > 1 else "") + ", composed via the goal-prompts MCP server.")
            self.assertEqual(build.conductor(mcp_pb, by_id), payload["result"]["content"][0]["text"])
            self.assertIn("insufficient evidence", actual)

    def test_briefs_and_distributions(self):
        import build
        for path in (ROOT / "prompts/venture").glob("*.md"):
            brief = build.parse(path)
            self.assertEqual(build.lint(brief), [])
            self.assertIn("CHARTER.md", brief["body"])
            self.assertIn("counterevidence", brief["body"].lower())
            self.assertEqual((ROOT / "raw" / (brief["id"] + ".md")).read_text().strip(), brief["body"])
        self.assertEqual((ROOT / "raw/venture_check.py").read_bytes(), (ROOT / "workflows/venture_check.py").read_bytes())

    def test_contract_linter_rejects_removed_evidence_rule(self):
        import build
        brief = build.parse(next((ROOT / "prompts/venture").glob("62-*.md")))
        brief["body"] = brief["body"].replace("source links and access dates", "sources")
        self.assertTrue(any("Venture contract missing" in e for e in build.lint(brief)))


if __name__ == "__main__":
    unittest.main()
