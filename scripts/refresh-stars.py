#!/usr/bin/env python3
"""Refresh metrics.json (GitHub stars / forks) so build.py can render the adoption
badge without a network call — the build itself stays offline + deterministic
(stdlib-only, no fetch). Run this on demand or from a deploy hook, then rebuild.

The badge is threshold-gated in build.py (STAR_THRESHOLD), so a small or zero
count renders nothing — it turns itself on once adoption is real. Today: 0 stars,
so nothing shows. Usage:

    python3 scripts/refresh-stars.py     # updates metrics.json from the live repo
"""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "GhostlyGawd/goal-prompts"


def main():
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "goal-prompts-build"},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.load(r)
    m = {"stars": int(d.get("stargazers_count", 0)), "forks": int(d.get("forks_count", 0))}
    (ROOT / "metrics.json").write_text(json.dumps(m, indent=2) + "\n")
    print(f"metrics.json <- {m}")


if __name__ == "__main__":
    main()
