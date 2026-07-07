#!/usr/bin/env node
/* goal-prompts MCP server — zero dependencies.
 *
 * Exposes the brief catalog to MCP clients (Claude Code, Claude Desktop, …)
 * over stdio. Data is read from the package's own catalog.json and raw/
 * directory, so it works offline and never drifts from the installed version.
 *
 * Install:  claude mcp add goal-prompts -- npx -y github:GhostlyGawd/goal-prompts
 * Tools:    list_briefs · suggest_briefs · get_brief · get_playbook · make_conductor
 */
"use strict";
const fs = require("fs");
const path = require("path");
const readline = require("readline");

const ROOT = path.join(__dirname, "..");
const VERSION = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8")).version;
const catalog = JSON.parse(fs.readFileSync(path.join(ROOT, "catalog.json"), "utf8"));
const briefs = catalog.briefs;
const byId = {};
briefs.forEach(function (b) { byId[b.id] = b; });

function readBody(id) {
  return fs.readFileSync(path.join(ROOT, "raw", id + ".md"), "utf8");
}

var bodyCache = {};
briefs.forEach(function (b) {
  try { bodyCache[b.id] = readBody(b.id).toLowerCase(); }
  catch (e) { bodyCache[b.id] = ""; }
});

function briefLine(b) {
  return b.id + " · " + b.title + "  [" + b.family + "]  -> " + b.output +
    "\n    " + b.tagline;
}

// ---- tools ----------------------------------------------------------------
const TOOLS = [
  {
    name: "list_briefs",
    description: "List every audit brief in the goal-prompts catalog: id, " +
      "title, family, the report file it writes, and a one-line tagline. " +
      "Optionally filter by family (" + catalog.families.join(", ") + ").",
    inputSchema: {
      type: "object",
      properties: {
        family: { type: "string", description: "Optional family filter" }
      }
    }
  },
  {
    name: "suggest_briefs",
    description: "Given a goal in plain words (e.g. 'my agent keeps looping' " +
      "or 'costs are exploding'), return the most relevant briefs, best " +
      "first. Stemmed, rarity-weighted keyword scoring over titles, taglines, " +
      "and bodies — " +
      "review the matches rather than trusting rank blindly.",
    inputSchema: {
      type: "object",
      properties: {
        goal: { type: "string", description: "What you want to audit or fix" },
        limit: { type: "number", description: "Max results (default 5)" }
      },
      required: ["goal"]
    }
  },
  {
    name: "get_brief",
    description: "Fetch the full text of one brief by id (e.g. '30'). The " +
      "returned prompt is self-contained: paste or execute it inside the " +
      "target repo; it audits read-only and writes exactly one report file.",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string", description: "Brief id, two digits, e.g. '06'" }
      },
      required: ["id"]
    }
  },
  {
    name: "make_conductor",
    description: "Compose a conductor — one prompt that fetches and runs a " +
      "custom sequence of briefs in order — from any list of brief ids. " +
      "Your own playbook: e.g. ids ['46','47'] for triage-then-fix, or " +
      "['33','49','34'] for a retrieval tune-up. Ids run in the order given.",
    inputSchema: {
      type: "object",
      properties: {
        ids: {
          type: "array", items: { type: "string" },
          description: "Brief ids in run order, e.g. ['00','01','06']"
        },
        name: { type: "string", description: "Optional playbook name" }
      },
      required: ["ids"]
    }
  },
  {
    name: "get_playbook",
    description: "Fetch a playbook conductor — a single prompt that runs a " +
      "curated sequence of briefs in order. Keys: " +
      catalog.playbooks.map(function (p) { return p.key; }).join(", ") + ".",
    inputSchema: {
      type: "object",
      properties: {
        key: { type: "string", description: "Playbook key, e.g. 'agentday1'" }
      },
      required: ["key"]
    }
  }
];

// Light stemming so "looping" matches "loop", "costs" matches "cost".
// Substring matching does the rest: the stem is a prefix of every inflection.
function stem(w) {
  if (w.length > 5 && w.slice(-3) === "ing") return w.slice(0, -3);
  if (w.length > 4 && w.slice(-2) === "ed") return w.slice(0, -2);
  if (w.length > 3 && w.slice(-1) === "s" && w.slice(-2) !== "ss") return w.slice(0, -1);
  return w;
}

// A word like "agent" matches half the catalog and says little; a word like
// "loop" matches a handful and says a lot. Weight = 1/sqrt(briefs matched),
// clamped so one colorful phrase in a single tagline can't hijack a query.
var dfCache = {};
function rarity(w) {
  if (dfCache[w] !== undefined) return dfCache[w];
  var df = 0;
  briefs.forEach(function (b) {
    var hay = (b.title + " " + b.family + " " + b.tagline).toLowerCase() +
      " " + bodyCache[b.id];
    if (hay.indexOf(w) !== -1) df++;
  });
  dfCache[w] = 1 / Math.sqrt(Math.max(df, 5));
  return dfCache[w];
}

function score(brief, words) {
  const title = brief.title.toLowerCase();
  const tag = brief.tagline.toLowerCase();
  const fam = (brief.family + " " + brief.question).toLowerCase();
  const body = bodyCache[brief.id];
  let s = 0;
  words.forEach(function (w) {
    var m = 0;
    if (title.indexOf(w) !== -1) m += 4;
    if (fam.indexOf(w) !== -1) m += 3;
    if (tag.indexOf(w) !== -1) m += 2;
    if (body.indexOf(w) !== -1) m += 1;
    s += m * rarity(w);
  });
  return s;
}

function conductorText(name, desc, ids) {
  var base = catalog.base;
  var stages = ids.map(function (id, i) {
    var p = byId[id];
    return (i + 1) + ". **" + id + " · " + p.title + "** — fetch " + base +
      "/raw/" + id + ".md → writes `" + p.output + "`";
  });
  var plural = ids.length > 1 ? "briefs" : "brief";
  return "# Playbook: " + name + " (conductor)\n\n" +
"You are working inside this repo. Mission: execute the **" + name + "** playbook — " +
ids.length + " audit " + plural + " in sequence, each producing one report file at this repo's root.\n\n" +
desc + "\n\n" +
"## How to run each stage, in order\n" +
"1. Fetch the brief with a read-only web request (for example: curl -s <url>).\n" +
"2. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.\n" +
"3. Confirm the report file exists at repo root before moving on.\n" +
"4. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.\n\n" +
"## Stages\n" + stages.join("\n") + "\n\n" +
"## After the final stage\n" +
"- List every report created, with a one-line takeaway each.\n" +
"- Suggest the natural next step: fetch " + base + "/raw/28.md (Roadmap Synthesis) to merge all reports at this root into one sequenced plan.\n\n" +
"## Rules\n" +
"- If a fetch fails, say so and stop — never improvise a brief from memory.\n" +
"- Honor each brief's own rules, including ending by asking before any changes.\n" +
"- If a stage's report already exists, ask whether to re-run or skip that stage.\n";
}

function callTool(name, args) {
  args = args || {};
  if (name === "list_briefs") {
    let list = briefs;
    if (args.family) {
      const f = String(args.family).toLowerCase();
      list = briefs.filter(function (b) { return b.family.toLowerCase() === f; });
      if (!list.length) return "No family '" + args.family + "'. Families: " +
        catalog.families.join(", ");
    }
    return list.map(briefLine).join("\n") +
      "\n\nUse get_brief with an id to fetch the full prompt.";
  }
  if (name === "suggest_briefs") {
    if (!args.goal) return "Provide a goal, e.g. 'my agent keeps looping'.";
    const words = String(args.goal).toLowerCase().split(/[^a-z0-9]+/)
      .filter(function (w) { return w.length > 2; })
      .map(stem)
      .filter(function (w, i, a) { return a.indexOf(w) === i; });
    const limit = Math.max(1, Math.min(10, args.limit || 5));
    const ranked = briefs
      .map(function (b) { return { b: b, s: score(b, words) }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s; })
      .slice(0, limit);
    if (!ranked.length) return "No keyword matches. Try list_briefs to browse all " +
      briefs.length + " briefs.";
    return "Best matches for: " + args.goal + "\n\n" +
      ranked.map(function (x) { return briefLine(x.b); }).join("\n") +
      "\n\nRanked by stemmed-keyword overlap with titles, families, taglines, " +
      "and bodies \u2014 review the matches rather than trusting rank blindly." +
      "\nUse get_brief with an id to fetch the full prompt.";
  }
  if (name === "get_brief") {
    const b = byId[String(args.id)];
    if (!b) return "No brief with id '" + args.id + "'. Ids run 00–" +
      briefs[briefs.length - 1].id + "; try list_briefs.";
    return readBody(b.id);
  }
  if (name === "make_conductor") {
    var raw = args.ids;
    if (typeof raw === "string") raw = raw.split(/[\s,]+/);
    if (!Array.isArray(raw) || !raw.length) {
      return "Provide ids as an array of brief ids in run order, e.g. ['46','47']. " +
        "Use list_briefs to browse.";
    }
    var ids = raw.map(function (x) {
      var s = String(x).trim();
      return s.length === 1 ? "0" + s : s;
    });
    var unknown = ids.filter(function (id) { return !byId[id]; });
    if (unknown.length) {
      return "Unknown brief id(s): " + unknown.join(", ") + ". Ids run 00–" +
        briefs[briefs.length - 1].id + "; try list_briefs.";
    }
    if (ids.length > 12) return "That's " + ids.length + " briefs — cap a conductor at 12; split the run.";
    var cname = args.name ? String(args.name) : "Custom sequence";
    var cdesc = "A custom sequence of " + ids.length + " brief" + (ids.length > 1 ? "s" : "") +
      ", composed via the goal-prompts MCP server.";
    return conductorText(cname, cdesc, ids);
  }
  if (name === "get_playbook") {
    const key = String(args.key);
    const pb = catalog.playbooks.filter(function (p) { return p.key === key; })[0];
    if (!pb) return "No playbook '" + key + "'. Keys: " +
      catalog.playbooks.map(function (p) { return p.key; }).join(", ");
    return fs.readFileSync(path.join(ROOT, "raw", "playbook-" + key + ".md"), "utf8");
  }
  throw new Error("Unknown tool: " + name);
}

// ---- JSON-RPC over stdio (newline-delimited) -------------------------------
function send(msg) { process.stdout.write(JSON.stringify(msg) + "\n"); }
function result(id, payload) { send({ jsonrpc: "2.0", id: id, result: payload }); }
function rpcError(id, code, message) {
  send({ jsonrpc: "2.0", id: id, error: { code: code, message: message } });
}

const rl = readline.createInterface({ input: process.stdin, terminal: false });
rl.on("line", function (line) {
  line = line.trim();
  if (!line) return;
  let msg;
  try { msg = JSON.parse(line); } catch (e) { return; }
  const id = msg.id;
  try {
    if (msg.method === "initialize") {
      result(id, {
        protocolVersion: (msg.params && msg.params.protocolVersion) || "2024-11-05",
        capabilities: { tools: {} },
        serverInfo: { name: "goal-prompts", version: VERSION }
      });
    } else if (msg.method === "notifications/initialized") {
      // notification: no response
    } else if (msg.method === "ping") {
      result(id, {});
    } else if (msg.method === "tools/list") {
      result(id, { tools: TOOLS });
    } else if (msg.method === "tools/call") {
      const name = msg.params && msg.params.name;
      const args = msg.params && msg.params.arguments;
      try {
        const text = callTool(name, args);
        result(id, { content: [{ type: "text", text: text }] });
      } catch (e) {
        result(id, { content: [{ type: "text", text: "Error: " + e.message }], isError: true });
      }
    } else if (id !== undefined) {
      rpcError(id, -32601, "Method not found: " + msg.method);
    }
  } catch (e) {
    if (id !== undefined) rpcError(id, -32603, "Internal error: " + e.message);
  }
});
