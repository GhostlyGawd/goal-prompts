#!/usr/bin/env python3
"""Read-only structural checks for a venture run. No dependencies or agent runtime."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

OUTPUTS = dict(zip(map(str, range(60, 68)), (
    "OPPORTUNITIES.md", "NICHE.md", "DEMAND.md", "COMPETITORS.md",
    "MARKET.md", "POSITIONING.md", "MOAT.md", "VERDICT.md")))
STATES = {"pending", "running", "complete", "reused", "null", "blocked",
          "failed", "stale", "skipped"}
FINISHED = {"complete", "reused", "null"}
EVIDENCE = {"complete", "reused"}
HASH = re.compile(r"^[a-f0-9]{64}$")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(root, final=False):
    root = Path(root).resolve()
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)
        return condition

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def safe_path(value):
        if not isinstance(value, str):
            return None
        path = Path(value)
        if path.is_absolute() or ".." in path.parts or "\\" in value:
            return None
        if not re.fullmatch(r"(?:reports/)?[A-Z][A-Z0-9-]*\.md", value):
            return None
        resolved = (root / path).resolve()
        if not resolved.is_relative_to(root):
            return None
        return resolved

    try:
        state_path = root / "reports/venture-run.json"
        if not state_path.resolve().is_relative_to(root):
            return ["run state resolves outside the repo"]
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"cannot read run state: {exc}"]
    if not isinstance(state, dict):
        return ["run state must be an object"]
    check(state.get("schema_version") == 1, "schema_version must be 1")
    check(text(state.get("run_id")), "run_id is required")
    status = state.get("status")
    if not check(status in ("active", "paused", "stopped", "complete"), "invalid run status"):
        return errors
    check(state.get("commit_preference") in ("yes", "no"), "commit_preference must be yes/no")
    check(text(state.get("next_step")), "next_step is required, including terminal handoff")
    check(isinstance(state.get("operator"), dict) and bool(state["operator"]), "operator context is required")
    criteria = state.get("criteria")
    check(isinstance(criteria, list) and bool(criteria), "nonempty criteria array is required")
    if isinstance(criteria, list):
        for criterion in criteria:
            check(isinstance(criterion, dict) and all(text(criterion.get(k)) for k in
                  ("id", "threshold", "evidence", "recorded_at", "exposure")),
                  "each criterion needs id, threshold, evidence, recorded_at, exposure")
    check(isinstance(state.get("decisions"), list), "decisions must be an array")
    scope = state.get("scope", {})
    if not isinstance(scope, dict):
        scope = {}
    check(text(scope.get("id")), "scope.id is required")
    check(type(scope.get("revision")) is int and scope["revision"] >= 1, "scope.revision must be a positive integer")
    index = root / "reports/INDEX.md"
    try:
        check(index.resolve().is_relative_to(root), "index resolves outside repo")
        index_text = index.read_text(encoding="utf-8") if index.resolve().is_relative_to(root) else ""
        check(text(index_text) and str(state.get("run_id")) in index_text, "INDEX.md must identify this run")
    except OSError:
        errors.append("INDEX.md is missing")
    stages = state.get("stages")
    if not isinstance(stages, list) or not 1 <= len(stages) <= 16:
        return errors + ["stages must contain 1–16 entries"]
    seen, earlier, running = set(), {}, 0
    for number, stage in enumerate(stages, 1):
        prefix = f"stage {number}: "
        if not isinstance(stage, dict):
            errors.append(prefix + "must be an object")
            continue
        brief, output, ss = stage.get("brief"), stage.get("output"), stage.get("status")
        if not isinstance(ss, str) or ss not in STATES:
            errors.append(prefix + "invalid status")
            continue
        check(isinstance(brief, str) and bool(re.fullmatch(r"\d{2,3}", brief)), prefix + "invalid brief ID")
        if not isinstance(brief, str):
            brief = ""
        path = safe_path(output)
        check(path is not None, prefix + "output must be a safe root/reports Markdown path")
        if path is None:
            continue
        check(path.name not in {"INDEX.md", "CHARTER.md", "README.md"}, prefix + "reserved output")
        check(output not in seen, prefix + "duplicate output")
        seen.add(output)
        if brief in OUTPUTS:
            check(path.name == OUTPUTS[brief], prefix + "wrong Venture output")
        check(isinstance(stage.get("note"), str), prefix + "note is required")
        if ss in {"null", "blocked", "failed", "stale", "skipped"}:
            check(text(stage.get("note")), prefix + "non-completion requires a reason")
        inputs = stage.get("inputs")
        if not isinstance(inputs, dict):
            errors.append(prefix + "inputs must be a path/hash map")
            inputs = {}
        if ss in EVIDENCE or ss == "running":
            check(all(s["status"] in EVIDENCE | {"skipped"} for s in earlier.values()),
                  prefix + "unresolved earlier stage")
            if brief in OUTPUTS and brief != "60":
                check(scope.get("id") != "discovery", prefix + "venture selection is required")
                for dependency, prev in earlier.items():
                    if prev.get("brief") in OUTPUTS and prev["status"] in EVIDENCE:
                        check(dependency in inputs, prefix + "missing prior Venture input " + dependency)
        for dependency, sha in inputs.items():
            dep_path = safe_path(dependency)
            if not check(dep_path is not None and dep_path.is_file(), prefix + "missing/unsafe input " + dependency):
                continue
            check(dependency != output, prefix + "report cannot depend on itself")
            if dependency in earlier:
                check(earlier[dependency]["status"] in EVIDENCE, prefix + "input is not usable evidence")
            elif any(isinstance(s, dict) and s.get("output") == dependency for s in stages[number:]):
                errors.append(prefix + "input is a future stage")
            check(isinstance(sha, str) and bool(HASH.fullmatch(sha)), prefix + "invalid input hash")
            try:
                check(digest(dep_path) == sha, prefix + "stale input " + dependency)
            except OSError as exc:
                errors.append(prefix + str(exc))
        if ss == "running":
            running += 1
        if ss in FINISHED:
            source = stage.get("source", {})
            check(isinstance(source, dict) and all(text(source.get(k)) for k in
                  ("url", "retrieved_at", "sha256")), prefix + "source provenance is required")
            if isinstance(source, dict):
                check(isinstance(source.get("sha256"), str) and bool(HASH.fullmatch(source["sha256"])), prefix + "invalid brief hash")
            try:
                report = path.read_text(encoding="utf-8")
                check(bool(report.strip()), prefix + "empty report")
                check(digest(path) == stage.get("report_sha256"), prefix + "report hash mismatch")
                for line in (f"Run: {state.get('run_id')}",
                             f"Scope: {scope.get('id')}@{scope.get('revision')}",
                             f"Brief: {brief}", f"Status: {ss}"):
                    check(line in report.splitlines(), prefix + "missing metadata " + line)
                check(bool(re.search(r"\d{4}-\d{2}-\d{2}", report[:250])), prefix + "report date is required")
                check(f"stage {number}/{len(stages)} · brief {brief}" in report, prefix + "missing provenance")
                if ss in EVIDENCE:
                    for heading in ("Scope", "Findings", "Evidence", "Counterevidence", "Next steps"):
                        check("## " + heading in report.splitlines(), prefix + "missing section " + heading)
            except (OSError, UnicodeError) as exc:
                errors.append(prefix + f"cannot read report: {exc}")
        earlier[output] = stage
    check(running <= 1, "stages must execute sequentially")
    if status in {"paused", "stopped", "complete"}:
        check(running == 0, "non-active run cannot contain a running stage")
    if status == "complete":
        check(all(isinstance(s, dict) and s.get("status") in EVIDENCE for s in stages),
              "complete run requires every scheduled stage complete/reused")
    if status == "stopped":
        check(all(isinstance(s, dict) and s.get("status") not in {"pending", "running"} for s in stages),
              "stopped run needs a disposition for every stage")
    if final:
        check(status in {"complete", "stopped"}, "--final requires complete or stopped run")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    errors = validate(args.repo, args.final)
    if errors:
        print("\n".join("FAIL " + error for error in errors))
        return 1
    print("PASS structural readiness only; evidence quality and decision authority require review")
    return 0


if __name__ == "__main__":
    sys.exit(main())
