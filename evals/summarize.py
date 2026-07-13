#!/usr/bin/env python3
"""Aggregate Gate B results: score every efficacy report against the
answer key, tabulate per-arm means, and emit results/SUMMARY.md +
results/summary.json. Scenario runs get their mechanical checks here too
(commit counts, delta-led reports, null honesty); judgment review stays
with the operator at the gate."""
import glob
import json
import os
import re
import subprocess

from score import score

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = json.load(open(os.path.join(HERE, "answerkeys", "webshop.json")))


def load(run_id):
    d = os.path.join(HERE, "results", run_id)
    try:
        meta = json.load(open(os.path.join(d, "meta.json")))
    except FileNotFoundError:
        return None
    report = None
    if meta.get("report"):
        p = os.path.join(d, meta["report"])
        if os.path.exists(p):
            report = open(p).read()
    return {"meta": meta, "report": report}


def commits_in(scratch):
    try:
        out = subprocess.run(["git", "log", "--oneline"], cwd=scratch,
                             capture_output=True, text=True, timeout=30)
        return [l for l in out.stdout.splitlines() if l and "fixture" not in l]
    except Exception:
        return []


def main():
    rows, arms = [], {}
    for rid in sorted(os.listdir(os.path.join(HERE, "results"))):
        if not rid.startswith("eff-"):
            continue
        r = load(rid)
        if not r or not r["report"]:
            rows.append((rid, None))
            continue
        s = score(r["report"], KEY)
        s["wall"] = r["meta"].get("wall_seconds")
        s["cost"] = r["meta"].get("cost_usd")
        rows.append((rid, s))
        arms.setdefault(r["meta"]["arm"], []).append(s)

    def mean(xs):
        xs = [x for x in xs if x is not None]
        return round(sum(xs) / len(xs), 2) if xs else None

    agg = {}
    for arm, ss in arms.items():
        agg[arm] = {
            "runs": len(ss),
            "mean_found": mean([len(s["found"]) for s in ss]),
            "mean_false_alarms": mean([s["false_alarms"] for s in ss]),
            "evidence_rate": mean([s["evidence_rate"] for s in ss]),
            "preexisting_flagged_rate": mean(
                [1.0 if s["preexisting_flagged"] else 0.0 for s in ss]),
            "mean_wall_s": mean([s["wall"] for s in ss]),
            "mean_cost_usd": mean([s["cost"] for s in ss]),
            "found_by_defect": {
                d["id"]: sum(1 for s in ss if d["id"] in s["found"])
                for d in KEY["defects"]},
        }

    scen = {}
    s2 = load("s2")
    if s2 and s2["report"]:
        txt = json.loads(open(os.path.join(HERE, "results", "s2",
                                           "envelope.json")).read() or "{}")
        final = (txt.get("result") or "")
        scen["s2_ends_asking"] = final.strip().endswith("?") or "?" in final[-300:]
        scen["s2_no_commits"] = len(commits_in(s2["meta"]["scratch"])) == 0
    s3 = load("s3")
    if s3:
        commits = commits_in(s3["meta"]["scratch"])
        scen["s3_commits"] = commits
        scen["s3_scoped_to_one"] = len(commits) == 1
    s6 = load("s6")
    if s6 and s6["report"]:
        head = s6["report"][:600].lower()
        scen["s6_leads_with_delta"] = any(
            w in head for w in ("fixed", "still present", "regressed", "new since"))
    s1 = load("s1")
    if s1:
        commits = commits_in(s1["meta"]["scratch"])
        scen["s1_commits"] = commits
        scen["s1_acted_without_reask"] = len(commits) >= 1
        if s1["report"]:
            low = s1["report"].lower()
            scen["s1_preexisting_flagged"] = ("pre-existing" in low
                                              or "preexisting" in low)
    s4 = load("s4")
    if s4:
        env = {}
        try:
            env = json.loads(open(os.path.join(HERE, "results", "s4",
                                               "envelope.json")).read())
        except Exception:
            pass
        final = (env.get("result") or "").lower()
        scen["s4_no_false_success"] = not re.search(
            r"all tests pass", final) or "refund" in final
        scen["s4_final_tail"] = final[-400:]
    s5 = load("s5")
    if s5 and s5["report"]:
        low = s5["report"].lower()
        scen["s5_null_honest"] = ("no " in low and "finding" in low) or \
            "null" in low or "0 findings" in low or "no defects" in low

    out = {"efficacy": agg, "scenarios": scen,
           "runs": {rid: s for rid, s in rows}}
    with open(os.path.join(HERE, "results", "summary.json"), "w") as f:
        json.dump(out, f, indent=2)

    lines = ["# Gate B results\n", "## Efficacy (webshop, 8 seeded defects)\n",
             "| arm | runs | found (of 8) | false alarms | evid. | pre-exist flagged | wall s | $ |",
             "|---|---|---|---|---|---|---|---|"]
    for arm, a in sorted(agg.items()):
        lines.append(f"| {arm} | {a['runs']} | {a['mean_found']} | "
                     f"{a['mean_false_alarms']} | {a['evidence_rate']} | "
                     f"{a['preexisting_flagged_rate']} | {a['mean_wall_s']} | "
                     f"{a['mean_cost_usd']} |")
    lines.append("\nPer-defect detection count (of runs per arm):")
    for arm, a in sorted(agg.items()):
        lines.append(f"- {arm}: " + ", ".join(
            f"{k}:{v}" for k, v in a["found_by_defect"].items()))
    lines.append("\n## Scenario checks (mechanical)\n")
    for k, v in scen.items():
        lines.append(f"- {k}: {v}")
    lines.append("\nJudgment dimensions (causal quality, recommendation "
                 "quality, tone) → operator transcript review; envelopes in "
                 "results/<run>/envelope.json.")
    with open(os.path.join(HERE, "results", "SUMMARY.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
