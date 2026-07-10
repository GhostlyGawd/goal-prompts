#!/bin/sh
# Hermetic test for the `install` script — run by scripts/check.
#
# Serves the repo's real commands.tar.gz + checksums.txt from a local
# python3 http.server on an ephemeral port, installs into a scratch dir via
# the installer's BASE override, and asserts the contract:
#   1. every brief lands as goal-<slug>.md, plus the goal/.version stamp
#   2. re-running removes stale files left by a previous install
#   3. a corrupted tarball aborts before touching the existing install
# Needs python3 + sh + curl; finishes in a couple of seconds.
set -e
cd "$(dirname "$0")/.."
REPO="$PWD"

TMPD=$(mktemp -d)
SRV_PID=""
cleanup() { [ -n "$SRV_PID" ] && kill "$SRV_PID" 2>/dev/null; rm -rf "$TMPD"; }
trap cleanup EXIT

# one server, two origins: /good serves the real artifacts, /bad a corrupted
# tarball beside the real checksums (so verification must fail).
# catalog.json rides along: the BRIEF flag resolves ids to slugs through it.
mkdir -p "$TMPD/www/good" "$TMPD/www/bad"
cp commands.tar.gz checksums.txt catalog.json "$TMPD/www/good/"
cp checksums.txt "$TMPD/www/bad/"
{ cat commands.tar.gz; printf 'corrupt'; } > "$TMPD/www/bad/commands.tar.gz"

python3 - "$TMPD/www" "$TMPD/port" <<'EOF' &
import http.server, socketserver, sys, os
os.chdir(sys.argv[1])
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", 0), Quiet) as srv:
    with open(sys.argv[2], "w") as f:
        f.write(str(srv.server_address[1]))
    srv.serve_forever()
EOF
SRV_PID=$!
i=0
while [ ! -s "$TMPD/port" ]; do
  i=$((i + 1)); [ "$i" -gt 50 ] && { echo "FAIL  server did not start"; exit 1; }
  sleep 0.1
done
PORT=$(cat "$TMPD/port")

fail() { echo "FAIL  $1"; exit 1; }

WORK="$TMPD/work"; mkdir -p "$WORK"; cd "$WORK"
BASE="http://127.0.0.1:$PORT/good" sh "$REPO/install" > out1.txt

grep -q 'Checksum verified' out1.txt || fail "checksum was not verified"
[ -f .claude/commands/goal/goal-bug-hunt.md ] || fail "goal-bug-hunt.md missing"
[ -f .claude/commands/goal/.version ] || fail "goal/.version missing"
VER=$(python3 -c "import json; print(json.load(open('$REPO/package.json'))['version'])")
[ "$(cat .claude/commands/goal/.version)" = "$VER" ] || fail ".version != package.json version"
grep -q "v$VER" out1.txt || fail "installer did not print the version"
N=$(ls .claude/commands/goal/*.md | wc -l | tr -d ' ')
WANT=$(find "$REPO/prompts" -name '*.md' | wc -l | tr -d ' ')
[ "$N" = "$WANT" ] || fail "installed $N commands, catalog has $WANT"

# re-run removes stale files from an earlier version
touch .claude/commands/goal/goal-stale-brief.md
BASE="http://127.0.0.1:$PORT/good" sh "$REPO/install" > out2.txt
[ ! -e .claude/commands/goal/goal-stale-brief.md ] || fail "stale file survived a re-run"

# corrupted tarball aborts, leaving the good install untouched
if BASE="http://127.0.0.1:$PORT/bad" sh "$REPO/install" > out3.txt 2>&1; then
  fail "corrupted tarball did not abort"
fi
grep -q 'checksum mismatch' out3.txt || fail "abort did not name the checksum mismatch"
[ -f .claude/commands/goal/goal-bug-hunt.md ] || fail "existing install damaged by the aborted run"

# --- R43 (COMPETITIVE §3.3): per-brief install via the BRIEF flag ---
# BRIEF=<id> in a fresh dir installs exactly that brief (still verified)
ONE="$TMPD/one"; mkdir -p "$ONE"; cd "$ONE"
BASE="http://127.0.0.1:$PORT/good" BRIEF=01 sh "$REPO/install" > out4.txt
grep -q 'Checksum verified' out4.txt || fail "BRIEF install skipped verification"
[ -f .claude/commands/goal/goal-bug-hunt.md ] || fail "BRIEF=01 did not install goal-bug-hunt.md"
N1=$(ls .claude/commands/goal/*.md | wc -l | tr -d ' ')
[ "$N1" = "1" ] || fail "BRIEF=01 installed $N1 commands, wanted exactly 1"

# a slug works directly, and adding a second brief leaves the first alone
BASE="http://127.0.0.1:$PORT/good" BRIEF=roadmap-synthesis sh "$REPO/install" > out5.txt
[ -f .claude/commands/goal/goal-roadmap-synthesis.md ] || fail "BRIEF=<slug> did not install"
[ -f .claude/commands/goal/goal-bug-hunt.md ] || fail "second BRIEF install removed the first brief"

# an unknown brief aborts without touching the install
if BASE="http://127.0.0.1:$PORT/good" BRIEF=999 sh "$REPO/install" > out6.txt 2>&1; then
  fail "unknown BRIEF did not abort"
fi
grep -q 'unknown brief' out6.txt || fail "abort did not name the unknown brief"
[ -f .claude/commands/goal/goal-bug-hunt.md ] || fail "failed BRIEF install damaged existing files"

echo "OK  install: $N commands, v$VER, stale-file removal, corrupt-tarball abort, BRIEF flag"
