---
description: Recompile brand.json into the host's tokens.css (or verify it hasn't drifted with --check).
---

Run `python3 design-engine/tools/tokens_build.py $ARGUMENTS` from the repo
root. If the host integrates via python-import (see brand.json host.integration),
prefer running the host's own build so every generated surface stays in step;
use this command directly for file-integration hosts or a quick --check.
Report what changed.
