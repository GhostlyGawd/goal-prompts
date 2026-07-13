#!/usr/bin/env python3
"""One eval run: copy a fixture to scratch (never the answer key), run a
vanilla nested claude session headlessly, keep the produced report, the
JSON transcript envelope, and usage. --resume continues the SAME session
for multi-turn BDD scenarios. Deterministic wrapper; the model does the
work. Internal QA only (PRODUCT_ALIGNMENT: Internal efficacy testing)."""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

RO_TOOLS = [
    "Read", "Grep", "Glob", "LS", "TodoWrite", "Task",
    "Bash(ls:*)", "Bash(cat:*)", "Bash(grep:*)", "Bash(find:*)",
    "Bash(wc:*)", "Bash(git log:*)", "Bash(git diff:*)",
    "Bash(git status:*)", "Bash(git show:*)",
    "Bash(python3 -m unittest:*)", "Bash(python3 -m pytest:*)",
]


def act_tools(scratch):
    return RO_TOOLS + [
        f"Write({scratch}/**)", f"Edit({scratch}/**)",
        "Bash(git add:*)", "Bash(git commit:*)", "Bash(git init:*)",
    ]


def write_tools(scratch):
    return RO_TOOLS + [f"Write({scratch}/**)"]


def vanilla_env():
    return {k: v for k, v in os.environ.items()
            if not (k.startswith("CLAUDE") or k == "CLAUDECODE")} | {
                "TERM": "dumb"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", default="webshop")
    ap.add_argument("--arm", required=True,
                    help="label for results, e.g. plain | goal-v2 | s1")
    ap.add_argument("--prompt-file", help="file whose text is the prompt")
    ap.add_argument("--prompt", help="literal prompt text")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--mode", choices=["investigate", "act"],
                    default="investigate")
    ap.add_argument("--scratch", help="reuse an existing scratch checkout")
    ap.add_argument("--resume", help="session id to continue")
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()

    prompt = args.prompt or open(args.prompt_file).read()
    out_dir = os.path.join(HERE, "results", args.run_id)
    os.makedirs(out_dir, exist_ok=True)

    if args.scratch:
        scratch = args.scratch
    else:
        scratch = os.path.join(os.environ.get("TMPDIR", "/tmp"),
                               f"gp-eval-{args.run_id}")
        shutil.rmtree(scratch, ignore_errors=True)
        shutil.copytree(os.path.join(HERE, "fixtures", args.fixture), scratch)
        subprocess.run(["git", "init", "-q"], cwd=scratch, check=True)
        subprocess.run(["git", "add", "-A"], cwd=scratch, check=True)
        subprocess.run(["git", "-c", "user.email=eval@local",
                        "-c", "user.name=eval", "commit", "-qm", "fixture"],
                       cwd=scratch, check=True)

    tools = act_tools(scratch) if args.mode == "act" else write_tools(scratch)
    cmd = ["claude", "-p", prompt, "--model", args.model,
           "--output-format", "json", "--allowedTools", *tools]
    if args.resume:
        cmd += ["--resume", args.resume]
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=scratch, env=vanilla_env(),
                          capture_output=True, text=True, timeout=1500)
    wall = time.time() - t0

    envelope = None
    try:
        envelope = json.loads(proc.stdout)
    except (json.JSONDecodeError, ValueError):
        pass
    with open(os.path.join(out_dir, "envelope.json"), "w") as f:
        f.write(proc.stdout or "")
    if proc.stderr:
        with open(os.path.join(out_dir, "stderr.txt"), "w") as f:
            f.write(proc.stderr)

    report_path = None
    for cand in ("reports", "."):
        d = os.path.join(scratch, cand)
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                if fn.endswith(".md") and fn.upper() == fn and fn != "README.md":
                    report_path = os.path.join(d, fn)
                    break
        if report_path:
            break
    if report_path:
        shutil.copy(report_path, os.path.join(out_dir, os.path.basename(report_path)))

    meta = {
        "run_id": args.run_id, "arm": args.arm, "fixture": args.fixture,
        "mode": args.mode, "model": args.model, "wall_seconds": round(wall, 1),
        "exit_code": proc.returncode,
        "report": os.path.basename(report_path) if report_path else None,
        "scratch": scratch,
        "session_id": (envelope or {}).get("session_id"),
        "usage": (envelope or {}).get("usage"),
        "cost_usd": (envelope or {}).get("total_cost_usd"),
        "resumed_from": args.resume,
    }
    with open(os.path.join(out_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(json.dumps(meta))
    return 0 if proc.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
