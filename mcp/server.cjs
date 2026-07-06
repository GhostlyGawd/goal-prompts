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

function score(brief, words) {
  const title = brief.title.toLowerCase();
  const tag = brief.tagline.toLowerCase();
  const fam = (brief.family + " " + brief.question).toLowerCase();
  let body = "";
  try { body = readBody(brief.id).toLowerCase(); } catch (e) { body = ""; }
  let s = 0;
  words.forEach(function (w) {
    if (title.indexOf(w) !== -1) s += 4;
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
    const words = String(args.goal).toLowerCase().split(/[^a-z0-9]+/)
      .filter(function (w) { return w.length > 2; });
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
      "\n\nUse get_brief with an id to fetch the full prompt.";
  }
  if (name === "get_brief") {
    const b = byId[String(args.id)];
    if (!b) return "No brief with id '" + args.id + "'. Ids run 00–" +
      briefs[briefs.length - 1].id + "; try list_briefs.";
    return readBody(b.id);
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
        serverInfo: { name: "goal-prompts", version: "0.4.0" }
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
