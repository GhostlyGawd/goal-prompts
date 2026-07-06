#!/usr/bin/env node
/* goal-prompts MCP server — zero dependencies.
 *
 * Exposes the brief catalog to MCP clients (Claude Code, Claude Desktop, …)
 * over stdio. Data is read from the package's own catalog.json and raw/
 * directory, so it works offline and never drifts from the installed version.
 *
 * Install:  claude mcp add goal-prompts -- npx -y github:GhostlyGawd/goal-prompts
 * Tools:    list_briefs · suggest_briefs · get_brief · get_playbook
 */
"use strict";
const fs = require("fs");
const path = require("path");
const readline = require("readline");

const ROOT = path.join(__dirname, "..");
const catalog = JSON.parse(fs.readFileSync(path.join(ROOT, "catalog.json"), "utf8"));
const briefs = catalog.briefs;
const byId = {};
briefs.forEach(function (b) { byId[b.id] = b; });

// terms appearing in a large fraction of briefs are noise for ranking
var STOP = (function () {
  var df = {}, N = briefs.length;
  briefs.forEach(function (b) {
    var seen = {};
    (b.title + " " + b.tagline + " " + b.family + " " + b.question)
      .toLowerCase().split(/[^a-z0-9]+/).forEach(function (w) {
        if (w.length > 2 && !seen[w]) { seen[w] = 1; df[w] = (df[w] || 0) + 1; }
      });
  });
  var stop = { the: 1, and: 1, for: 1, your: 1, that: 1, with: 1, this: 1 };
  Object.keys(df).forEach(function (w) { if (df[w] / N > 0.25) stop[w] = 1; });
  return stop;
})();

function readBody(id) {
  return fs.readFileSync(path.join(ROOT, "raw", id + ".md"), "utf8");
}

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
      "first. Simple keyword scoring over titles, taglines, and bodies — " +
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
    description: "Compose a custom conductor prompt from an ordered list of " +
      "brief ids. Returns a single prompt that runs exactly those briefs in " +
      "sequence, each writing its report — use it to build a bespoke audit " +
      "run tailored to what you found (e.g. after suggest_briefs).",
    inputSchema: {
      type: "object",
      properties: {
        ids: {
          type: "array", items: { type: "string" },
          description: "Brief ids in run order, e.g. ['33','49','34']"
        }
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

// crude stemmer: fold common suffixes so "looping" matches "loop", "queries"
// matches "query", etc. Applied to both the goal words and the haystacks.
function stem(w) {
  if (w.length > 5 && w.slice(-3) === "ing") w = w.slice(0, -3);
  else if (w.length > 4 && w.slice(-2) === "ed") w = w.slice(0, -2);
  else if (w.length > 4 && w.slice(-3) === "ies") w = w.slice(0, -3) + "y";
  else if (w.length > 3 && w.slice(-1) === "s" && w.slice(-2) !== "ss") w = w.slice(0, -1);
  return w;
}
function stemAll(text) {
  return text.toLowerCase().split(/[^a-z0-9]+/).map(stem).join(" ");
}
function score(brief, stems) {
  const title = stemAll(brief.title);
  const fam = stemAll(brief.family + " " + brief.question);
  const tag = stemAll(brief.tagline);
  let body = "";
  try { body = stemAll(readBody(brief.id)); } catch (e) { body = ""; }
  var s = 0;
  stems.forEach(function (w) {
    var inTitle = title.split(" ").indexOf(w) !== -1; // whole-word in title
    if (inTitle) s += 8;
    else if (title.indexOf(w) !== -1) s += 4;         // substring in title
    if (fam.indexOf(w) !== -1) s += 3;
    if (tag.indexOf(w) !== -1) s += 2;
    if (body.indexOf(w) !== -1) s += 1;
  });
  return s;
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
    var stems = String(args.goal).toLowerCase().split(/[^a-z0-9]+/)
      .filter(function (w) { return w.length > 2 && !STOP[w]; }).map(stem);
    if (!stems.length) {  // goal was all stopwords — fall back to raw words
      stems = String(args.goal).toLowerCase().split(/[^a-z0-9]+/)
        .filter(function (w) { return w.length > 2; }).map(stem);
    }
    const limit = Math.max(1, Math.min(10, args.limit || 5));
    const ranked = briefs
      .map(function (b) { return { b: b, s: score(b, stems) }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s; })
      .slice(0, limit);
    if (!ranked.length) return "No keyword matches. Try list_briefs to browse all " +
      briefs.length + " briefs.";
    return "Best matches for: " + args.goal + "\n\n" +
      ranked.map(function (x) { return briefLine(x.b); }).join("\n") +
      "\n\nUse get_brief with an id to fetch the full prompt.";
  }
  if (name === "get_brief") {
    const b = byId[String(args.id)];
    if (!b) return "No brief with id '" + args.id + "'. Ids run 00–" +
      briefs[briefs.length - 1].id + "; try list_briefs.";
    return readBody(b.id);
  }
  if (name === "make_conductor") {
    const ids = Array.isArray(args.ids) ? args.ids.map(String) : [];
    if (!ids.length) return "Provide ids, e.g. { ids: ['33','49','34'] }.";
    const bad = ids.filter(function (i) { return !byId[i]; });
    if (bad.length) return "Unknown ids: " + bad.join(", ") + ". Use list_briefs.";
    var out = "# Playbook: custom sequence (conductor)\n\n";
    out += "You are working inside this repo. Mission: execute the following " +
      "audit briefs in order, each producing one report file at this repo's root.\n\n";
    out += "## How to run each stage, in order\n";
    out += "1. Fetch the brief with a read-only web request (e.g. curl -s <url>).\n";
    out += "2. Execute it exactly as written. Each brief is read-only toward the " +
      "codebase unless it says otherwise; its only write is its own report file.\n";
    out += "3. Confirm the report exists at repo root before moving on. Do not parallelize.\n\n";
    out += "## Stages\n";
    ids.forEach(function (id, i) {
      var b = byId[id];
      out += (i + 1) + ". **" + id + " \u00b7 " + b.title + "** \u2014 fetch " +
        catalog.base + "/raw/" + id + ".md \u2192 writes `" + b.output + "`\n";
    });
    out += "\n## After the final stage\n- List every report created, one-line " +
      "takeaway each.\n- Suggest fetching " + catalog.base + "/raw/28.md " +
      "(Roadmap Synthesis) to merge all reports into one plan.\n\n";
    out += "## Rules\n- If a fetch fails, say so and stop \u2014 never improvise " +
      "a brief from memory.\n- Honor each brief's own rules, including any that " +
      "ask before acting.\n";
    return out;
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
        serverInfo: { name: "goal-prompts", version: "0.5.0" }
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
