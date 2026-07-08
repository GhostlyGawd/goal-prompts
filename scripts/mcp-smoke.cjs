#!/usr/bin/env node
/* MCP smoke test — spawns the real server over stdio and asserts behavior.
 *
 * This is the check that originally caught the "looping" ranking bug
 * (IMPROVEMENTS.md, quick win 1), promoted from a manual ritual to a gate.
 * Run directly (node scripts/mcp-smoke.cjs) or via scripts/check.
 */
"use strict";
const { spawn } = require("child_process");
const path = require("path");

const server = spawn("node", [path.join(__dirname, "..", "mcp", "server.cjs")],
  { stdio: ["pipe", "pipe", "inherit"] });

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
];
requests.forEach(function (m) { server.stdin.write(JSON.stringify(m) + "\n"); });

const failures = [];
function check(label, ok) {
  console.log((ok ? "  ok  " : "  FAIL") + "  " + label);
  if (!ok) failures.push(label);
}
function text(msg) { return msg.result.content[0].text; }

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
    }
    if (msg.id === 2) {
      const names = msg.result.tools.map(function (t) { return t.name; });
      check("tools/list exposes 5 tools (" + names.join(", ") + ")",
        names.length === 5 && names.indexOf("make_conductor") !== -1);
    }
    if (msg.id === 3) {
      // The historic regression: raw substring matching ranked 41 above 32
      // for "looping". Stemming + rarity weighting must surface 32 near the
      // top. Strict-first is no longer pinned: as the catalog grew, more
      // briefs (94 Inner-Loop, 96 Feedback-Loop) legitimately carry "loop",
      // so rarity down-weights the now-common term and a same-family title
      // match (50 Multi-Agent) can tie out ahead. What stays guaranteed: the
      // looping -> loop stemming ranks 32 in the top 3, not buried.
      const _sl = text(msg).split("\n");
      const top = [_sl[2], _sl[4], _sl[6]].join("\n");
      check("suggest('looping') ranks 32 · Loop & Termination in the top 3",
        top.indexOf("32 \u00b7") !== -1);
      check("suggest output states its scoring method",
        text(msg).indexOf("Ranked by") !== -1);
    }
    if (msg.id === 4) {
      // Fuzzy phrasing: position may vary, but the cost briefs must surface.
      check("suggest('costs exploding') surfaces 24 · Cost Audit in results",
        text(msg).indexOf("24 \u00b7 Cost Audit") !== -1);
    }
    if (msg.id === 5) {
      const t = text(msg);
      check("make_conductor(['46','47']) builds a two-stage conductor",
        t.indexOf("# Playbook: Smoke run (conductor)") === 0 &&
        t.indexOf("46 \u00b7 Audit Triage") !== -1 &&
        t.indexOf("47 \u00b7 The Fixer") !== -1 &&
        t.indexOf("/raw/47.md") !== -1);
    }
    if (msg.id === 6) {
      check("get_brief('47') returns the ask-first gate",
        text(msg).indexOf("Report only \u2014 end by asking") !== -1);
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
