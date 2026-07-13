#!/usr/bin/env python3
"""Mechanical scorer: one report vs one answer key. Deterministic on
purpose — no model in the loop. A defect counts as FOUND only when the
report names its file AND uses at least one of its match phrases (both
case-insensitive); naming the symptom without locating it earns nothing,
which is the product's own evidence bar. Judgment-shaped dimensions
(causal quality, recommendation quality) are left to the operator's
transcript review at the gate, not faked with heuristics."""
import json
import re
import sys


def _findings_count(text: str) -> int:
    """Count finding-shaped units: '### n.' headings or bold-led list rows."""
    heads = re.findall(r"(?m)^###\s+\d+[\.·]", text)
    if heads:
        return len(heads)
    return len(re.findall(r"(?m)^[-*]?\s*\*\*[^*\n]{4,}\*\*", text))


def score(report: str, key: dict) -> dict:
    low = report.lower()
    found, missed = [], []
    evidenced = 0
    for d in key["defects"]:
        file_hit = d["file"].lower() in low
        kw_hit = any(m.lower() in low for m in d["match"])
        if file_hit and kw_hit:
            found.append(d["id"])
            evidenced += 1  # file citation is the evidence bar
        else:
            missed.append(d["id"])
    n_findings = _findings_count(report)
    false_alarms = max(0, n_findings - len(found))
    pre = key.get("pre_existing_failing_tests", [])
    pre_named = any(t.lower() in low for t in pre)
    pre_flagged = pre_named and ("pre-existing" in low or "preexisting" in low
                                 or "already failing" in low
                                 or "not introduced" in low)
    verification_vocab = bool(
        re.search(r"\b(passed|pass)\b", low)
        and re.search(r"\b(failed|fail)\b", low)) or pre_flagged
    return {
        "found": found,
        "missed": missed,
        "false_alarms": false_alarms,
        "findings_counted": n_findings,
        "evidence_rate": (evidenced / len(found)) if found else 0.0,
        "preexisting_flagged": pre_flagged,
        "verification_vocab": verification_vocab,
    }


if __name__ == "__main__":
    report_path, key_path = sys.argv[1], sys.argv[2]
    with open(report_path) as f:
        report = f.read()
    with open(key_path) as f:
        key = json.load(f)
    print(json.dumps(score(report, key), indent=2))
