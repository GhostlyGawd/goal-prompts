#!/usr/bin/env python3
"""Tests for build.py's linter — the quality gate that had a real bug
(lens miscount from Phase 4) caught during 0.4 development."""
import importlib.util, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("build", ROOT / "build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

VALID = """# Goal: Test

Intro line.

## Phase 1 — Orient
Do the thing.

## Phase 2 — Audit through 4 lenses
1. **One** — a
2. **Two** — b
3. **Three** — c
4. **Four** — d

## Phase 3 — Curate
Rank them.

## Phase 4 — Report
Create `OUT.md`:
1. **Section** — with numbered items
2. **Another** — more items
3. **Third** — and more
4. **Fourth** — still more
5. **Fifth** — yet more

## Rules
- Report only — end by asking which to do
"""

def brief(body, **over):
    p = {"id":"99","title":"T","family":"Quality","question":"q",
         "output":"OUT.md","tagline":"fine","body":body,"chars":len(body),
         "kind":"audit","slug":"t"}
    p.update(over); return p

def run():
    fails = []
    def check(name, cond):
        print(("ok  " if cond else "FAIL ") + name)
        if not cond: fails.append(name)

    # 1. a well-formed audit brief passes clean
    check("valid brief passes", build.lint(brief(VALID)) == [])

    # 2. THE REGRESSION: Phase 4's numbered items must NOT count as lenses
    check("phase-4 items don't inflate lens count",
          not any("lens" in v for v in build.lint(brief(VALID))))

    # 3. oversized body is rejected
    big = VALID + "x"*4000
    check("oversized body fails", any("chars" in v for v in build.lint(brief(big, chars=len(big)))))

    # 4. a missing phase is caught
    check("missing phase fails", any("Phase 3" in v for v in build.lint(brief(VALID.replace("## Phase 3 — Curate","## Curate")))))

    # 5. audit brief without the ask-first ending fails
    check("audit missing ask-ending fails",
          any("ask-first" in v for v in build.lint(brief(VALID.replace("Report only — end by asking which to do","Done.")))))

    # 6. action brief uses the gate rule instead of "Report only"
    action_body = VALID.replace("- Report only — end by asking which to do",
                                "- Ask before acting. End by asking whether to open a PR.")
    check("action brief passes on gate wording",
          build.lint(brief(action_body, kind="action")) == [])

    # 7. action brief that never asks-before is rejected
    check("action without gate fails",
          any("gate" in v or "act" in v for v in build.lint(brief(VALID, kind="action"))))

    # 8. too few lenses is caught
    two_lens = VALID.replace("3. **Three** — c\n4. **Four** — d\n","")
    check("too-few-lenses fails", any("lens" in v for v in build.lint(brief(two_lens))))

    if fails:
        print(f"\n{len(fails)} test(s) failed"); sys.exit(1)
    print("\nall linter tests passed")

if __name__ == "__main__":
    run()
