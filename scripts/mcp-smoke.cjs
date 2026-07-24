#!/usr/bin/env node
/* MCP smoke test — spawns the real server over stdio and asserts behavior.
 *
 * This is the check that originally caught the "looping" ranking bug
 * (IMPROVEMENTS.md, quick win 1), promoted from a manual ritual to a gate.
 * Run directly (node scripts/mcp-smoke.cjs) or via scripts/check.
 */
"use strict";
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const catalog = JSON.parse(fs.readFileSync(path.join(ROOT, "catalog.json"), "utf8"));
const VER = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8")).version;

const failures = [];
function check(label, ok) {
  console.log((ok ? "  ok  " : "  FAIL") + "  " + label);
  if (!ok) failures.push(label);
}
function text(msg) { return msg.result.content[0].text; }
function top3(msg) {
  const l = text(msg).split("\n");
  return [l[2], l[4], l[6]].join("\n");
}

// ---- conductor parity guard -------------------------------------------------
// The conductor text lives in three places: build.py's template (raw/ +
// catalog.json), server.cjs's make_conductor, and js/catalog-core.js's
// client-side makeConductor(). These canonical sentences must appear verbatim
// in all three, so the copies can't drift silently. Each must stay on one
// source line.
const CANONICAL = [
  "If your harness can run subagents or fresh sessions, run each stage in one — a stage needs only the earlier report files at the repo root and in `reports/`, never this conversation.",
  "If a fetch fails, retry once; if it still fails, use the locally installed /goal:<slug> (or /goal-<slug>) command or the goal-prompts MCP get_brief tool for that stage; if neither exists, say so and stop — never improvise a brief from memory.",
  "If a stage's report already exists (at the repo root or in `reports/`), ask whether to re-run or skip that stage.",
  "A conductor caps at 16 stages — for a longer campaign, split it into two conductors and run them back-to-back.",
  // contractor-voice pins (CHARTER.md operator findings F1/F2 + ratified
  // charter-as-input): read the charter, introduce the run, narrate every
  // stage, end with a ranked plain-words list — no report-reading to act.
  "If `CHARTER.md` exists at the repo root or in `reports/`, read it first — its goals, non-goals, and invariants bound every recommendation in every stage. No charter? Proceed, and suggest 149 · The Charter afterwards.",
  "Before fetching stage 1, tell the operator in plain words what this playbook will do — one line per stage — and ask for the go-ahead.",
  "After each stage, tell the operator in two or three plain sentences what it found — the single biggest finding and why it matters for this repo — and what comes next; never advance in silence.",
  "Present the strongest findings across every report as one ranked list, in plain words — each with why it matters for this repo; the operator should not need to open a report file to act.",
  // cross-session handoff pins (operator bug report 2026-07-23: a follow-up
  // session couldn't find a finished playbook run — loose root files on an
  // unadvertised branch). The run must land in reports/, stamp and commit
  // each report, index itself, and end with a paste-ready handoff.
  "If there is no `reports/` directory at the repo root, create it now — every brief writes its report there once the directory exists, so the whole run lands in one folder instead of scattering generic filenames across the root.",
  "In a git repo, plan to commit as you go — one commit per report plus a final one for the index; make committing part of the go-ahead question, and skip it only if the operator says no.",
  "Confirm the report file exists (at the repo root or in `reports/`) before moving on, and stamp one provenance line under its title — `<playbook> · stage <N>/<M> · brief <id>` — so the file itself names the run that wrote it.",
  "If committing, commit the report now, message `reports: <FILE> — <stage title> (<playbook> <N>/<M>)` — that per-stage trail is what lets any later session recover the whole run with one git log --grep.",
  "Write the run's index — `INDEX.md`, in the same directory as the reports (commit it last, if committing): the run date, the playbook name, each stage with its brief URL, and one line per report — file name, finding count (mark a null report as such), and its top two or three next steps. A session with no memory of this run must be able to start from that one file.",
  "Close with the handoff: if the run sits on an unmerged branch, offer to open a pull request titled `reports: <playbook> run <date> (<M> stages)` whose body is the index — the PR list is the first place a later session or teammate looks; either way, print a paste-ready handoff block naming the branch, the report directory, the file list, and `INDEX.md` as the place to start.",
];
["build.py", "mcp/server.cjs", "js/catalog-core.js"].forEach(function (f) {
  const src = fs.readFileSync(path.join(ROOT, f), "utf8");
  CANONICAL.forEach(function (s, i) {
    check("conductor parity: sentence " + (i + 1) + " in " + f, src.indexOf(s) !== -1);
  });
});

// ---- live server ------------------------------------------------------------
const server = spawn("node", [path.join(ROOT, "mcp", "server.cjs")],
  { stdio: ["pipe", "pipe", "inherit"] });

const thirteen = ["00", "01", "02", "04", "06", "07", "08", "09", "13", "14", "21", "22", "23"];
const seventeen = thirteen.concat(["24", "26", "27", "28"]);

const requests = [
  { jsonrpc: "2.0", id: 1, method: "initialize",
    params: { protocolVersion: "2024-11-05" } },
  { jsonrpc: "2.0", id: 2, method: "tools/list" },
  { jsonrpc: "2.0", id: 3, method: "tools/call",
    params: { name: "suggest_briefs",
              arguments: { goal: "my agent keeps looping" } } },
  { jsonrpc: "2.0", id: 4, method: "tools/call",
    params: { name: "suggest_briefs",
              arguments: { goal: "costs are exploding" } } },
  { jsonrpc: "2.0", id: 5, method: "tools/call",
    params: { name: "make_conductor",
              arguments: { ids: ["46", "47"], name: "Smoke run" } } },
  { jsonrpc: "2.0", id: 6, method: "tools/call",
    params: { name: "get_brief", arguments: { id: "47" } } },
  { jsonrpc: "2.0", id: 7, method: "tools/call",
    params: { name: "get_brief", arguments: { id: "6" } } },
  { jsonrpc: "2.0", id: 8, method: "tools/call",
    params: { name: "get_brief", arguments: { id: " 47 " } } },
  { jsonrpc: "2.0", id: 9, method: "tools/call",
    params: { name: "get_brief", arguments: { id: "999" } } },
  { jsonrpc: "2.0", id: 10, method: "tools/call",
    params: { name: "list_playbooks", arguments: {} } },
  { jsonrpc: "2.0", id: 11, method: "prompts/list" },
  { jsonrpc: "2.0", id: 12, method: "prompts/get",
    params: { name: "goal-bug-hunt" } },
  { jsonrpc: "2.0", id: 13, method: "tools/call",
    params: { name: "make_conductor", arguments: { ids: thirteen } } },
  { jsonrpc: "2.0", id: 14, method: "tools/call",
    params: { name: "make_conductor", arguments: { ids: seventeen } } },
  // Pinned queries, one per marquee family — the guard for stemming
  // (eed/eeds exemption) and word-boundary matching in suggest_briefs.
  { jsonrpc: "2.0", id: 15, method: "tools/call",
    params: { name: "suggest_briefs", arguments: { goal: "bug" } } },
  { jsonrpc: "2.0", id: 16, method: "tools/call",
    params: { name: "suggest_briefs", arguments: { goal: "slow queries" } } },
  { jsonrpc: "2.0", id: 17, method: "tools/call",
    params: { name: "suggest_briefs", arguments: { goal: "prompt injection" } } },
  { jsonrpc: "2.0", id: 18, method: "tools/call",
    params: { name: "suggest_briefs", arguments: { goal: "checkout drop-off" } } },
  { jsonrpc: "2.0", id: 19, method: "tools/call",
    params: { name: "suggest_briefs", arguments: { goal: "dependency licenses" } } },
  { jsonrpc: "2.0", id: 20, method: "tools/call",
    params: { name: "get_brief", arguments: { id: "007" } } },
  { jsonrpc: "2.0", id: 21, method: "tools/call",
    params: { name: "make_conductor", arguments: { ids: " 46, 47" } } },
  { jsonrpc: "2.0", id: 22, method: "tools/call",
    params: { name: "list_briefs", arguments: {} } },
];
requests.forEach(function (m) { server.stdin.write(JSON.stringify(m) + "\n"); });

let buf = "";
let seen = 0;
server.stdout.on("data", function (d) {
  buf += d;
  let i;
  while ((i = buf.indexOf("\n")) !== -1) {
    const line = buf.slice(0, i); buf = buf.slice(i + 1);
    if (!line.trim()) continue;
    let msg;
    try { msg = JSON.parse(line); } catch (e) { continue; }
    seen++;
    if (msg.id === 1) {
      check("initialize returns serverInfo",
        !!(msg.result && msg.result.serverInfo &&
           msg.result.serverInfo.name === "goal-prompts"));
      check("initialize declares the prompts capability",
        !!(msg.result && msg.result.capabilities && msg.result.capabilities.prompts));
    }
    if (msg.id === 2) {
      const tools = msg.result.tools;
      const names = tools.map(function (t) { return t.name; });
      check("tools/list exposes 6 tools (" + names.join(", ") + ")",
        names.length === 6 && names.indexOf("make_conductor") !== -1 &&
        names.indexOf("list_playbooks") !== -1);
      const gp = tools.filter(function (t) { return t.name === "get_playbook"; })[0];
      check("get_playbook points at list_playbooks instead of enumerating keys",
        gp.description.indexOf("list_playbooks") !== -1 &&
        gp.description.indexOf("day1") === -1);
      const mc = tools.filter(function (t) { return t.name === "make_conductor"; })[0];
      check("make_conductor documents the 16-stage cap",
        mc.description.indexOf("16") !== -1);
    }
    if (msg.id === 3) {
      // The historic regression: raw substring matching ranked 41 above 32
      // for "looping". Stemming + rarity weighting must surface 32 near the
      // top. Strict-first is no longer pinned: as the catalog grew, more
      // briefs (94 Inner-Loop, 96 Feedback-Loop) legitimately carry "loop",
      // so rarity down-weights the now-common term and a same-family title
      // match (50 Multi-Agent) can tie out ahead. What stays guaranteed: the
      // looping -> loop stemming ranks 32 in the top 3, not buried.
      check("suggest('looping') ranks 32 · Loop & Termination in the top 3",
        top3(msg).indexOf("32 ·") !== -1);
      check("suggest output states its scoring method",
        text(msg).indexOf("Ranked by") !== -1);
    }
    if (msg.id === 4) {
      // Fuzzy phrasing: position may vary, but the cost briefs must surface.
      check("suggest('costs exploding') surfaces 24 · Cost Audit in results",
        text(msg).indexOf("24 · Cost Audit") !== -1);
    }
    if (msg.id === 5) {
      const t = text(msg);
      check("make_conductor(['46','47']) builds a two-stage conductor",
        t.indexOf("# Playbook: Smoke run (conductor)") === 0 &&
        t.indexOf("46 · Audit Triage") !== -1 &&
        t.indexOf("47 · The Fixer") !== -1 &&
        t.indexOf("/raw/47.md") !== -1);
      check("conductor text carries every canonical instruction sentence",
        CANONICAL.every(function (s) { return t.indexOf(s) !== -1; }));
    }
    if (msg.id === 6) {
      check("get_brief('47') returns the ask-first gate",
        text(msg).indexOf("Report only — end by asking") !== -1);
    }
    if (msg.id === 7) {
      check("get_brief('6') normalizes to 06",
        text(msg).indexOf("# Goal:") === 0 && !msg.result.isError &&
        text(msg).indexOf("No brief") === -1);
    }
    if (msg.id === 8) {
      check("get_brief(' 47 ') trims whitespace",
        text(msg).indexOf("Report only — end by asking") !== -1);
    }
    if (msg.id === 9) {
      const maxId = Math.max.apply(null, catalog.briefs.map(function (b) {
        return parseInt(b.id, 10);
      }));
      check("get_brief('999') error names the real id range (00–" + maxId + ")",
        text(msg).indexOf("00–" + maxId) !== -1);
    }
    if (msg.id === 10) {
      const t = text(msg);
      const allKeys = catalog.playbooks.every(function (p) {
        return t.indexOf(p.key) !== -1;
      });
      check("list_playbooks names all " + catalog.playbooks.length + " playbooks",
        allKeys);
      check("list_playbooks includes ids and taglines",
        t.indexOf("day1") !== -1 && t.indexOf("00 → 01 → 06 → 14") !== -1 &&
        t.indexOf("The four questions to ask any repo you just cloned.") !== -1);
      // R36 (RETENTION R10): the pinned-catalog footer names the installed
      // version and where "what's new" lives
      check("list_playbooks footer pins v" + VER + " + /changelog",
        t.indexOf("v" + VER) !== -1 && t.indexOf("/changelog") !== -1);
    }
    if (msg.id === 22) {
      check("list_briefs footer pins v" + VER + " + /changelog",
        text(msg).indexOf("v" + VER) !== -1 &&
        text(msg).indexOf("/changelog") !== -1);
    }
    if (msg.id === 11) {
      const prompts = (msg.result && msg.result.prompts) || [];
      check("prompts/list returns all " + catalog.briefs.length + " briefs",
        prompts.length === catalog.briefs.length);
      const bh = prompts.filter(function (p) { return p.name === "goal-bug-hunt"; })[0];
      check("prompts/list names goal-<slug> with tagline as description",
        !!bh && bh.description.indexOf("bug") !== -1);
    }
    if (msg.id === 12) {
      const m = msg.result && msg.result.messages && msg.result.messages[0];
      check("prompts/get('goal-bug-hunt') returns the brief body as a user message",
        !!m && m.role === "user" &&
        m.content.text.indexOf("Report only — end by asking") !== -1);
    }
    if (msg.id === 13) {
      check("make_conductor accepts 13 stages under the new 16 cap",
        text(msg).indexOf("# Playbook:") === 0);
    }
    if (msg.id === 14) {
      check("make_conductor refuses 17 stages, naming the 16 cap",
        text(msg).indexOf("# Playbook:") === -1 && text(msg).indexOf("16") !== -1);
    }
    if (msg.id === 15) {
      check("suggest('bug') ranks 01 · Bug Hunt in the top 3",
        top3(msg).indexOf("01 · Bug Hunt") !== -1);
    }
    if (msg.id === 16) {
      check("suggest('slow queries') ranks 87 · Query Performance in the top 3",
        top3(msg).indexOf("87 ·") !== -1);
    }
    if (msg.id === 17) {
      check("suggest('prompt injection') ranks 118 · Prompt-Injection Red-Team in the top 3",
        top3(msg).indexOf("118 ·") !== -1);
    }
    if (msg.id === 18) {
      check("suggest('checkout drop-off') ranks 110 · Checkout & Payment in the top 3",
        top3(msg).indexOf("110 ·") !== -1);
    }
    if (msg.id === 19) {
      check("suggest('dependency licenses') ranks 69 · License & Compliance in the top 3",
        top3(msg).indexOf("69 ·") !== -1);
    }
    if (msg.id === 20) {
      check("get_brief('007') strips leading zeros before padding",
        text(msg).indexOf("# Goal:") === 0 && text(msg).indexOf("No brief") === -1);
    }
    if (msg.id === 21) {
      check("make_conductor(' 46, 47') drops empty tokens from a string id list",
        text(msg).indexOf("# Playbook:") === 0 &&
        text(msg).indexOf("46 · Audit Triage") !== -1 &&
        text(msg).indexOf("47 · The Fixer") !== -1 &&
        text(msg).indexOf("Unknown brief id") === -1);
    }
    if (seen === requests.length) finish();
  }
});

function finish() {
  server.kill();
  if (failures.length) {
    console.error("\nMCP smoke: " + failures.length + " failure(s)");
    process.exit(1);
  }
  console.log("MCP smoke: all assertions passed");
  process.exit(0);
}
setTimeout(function () {
  console.error("MCP smoke: timed out waiting for server responses");
  server.kill();
  process.exit(1);
}, 8000);
