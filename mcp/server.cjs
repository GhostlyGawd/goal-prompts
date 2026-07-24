#!/usr/bin/env node
/* goal-prompts MCP server — zero dependencies.
 *
 * Exposes the brief catalog to MCP clients (Claude Code, Claude Desktop, …)
 * over stdio. Data is read from the package's own catalog.json and raw/
 * directory, so it works offline and never drifts from the installed version.
 *
 * Install:  claude mcp add goal-prompts -- npx -y github:GhostlyGawd/goal-prompts
 * Tools:    list_briefs · suggest_briefs · get_brief · list_playbooks ·
 *           get_playbook · make_conductor
 * Prompts:  every brief is also exposed as an MCP prompt (goal-<slug>).
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
const bySlug = {};
briefs.forEach(function (b) { byId[b.id] = b; bySlug[b.slug] = b; });
const MAX_ID = briefs.reduce(function (m, b) {
  return Math.max(m, parseInt(b.id, 10));
}, 0);
const ID_RANGE = "Ids run 00–" + MAX_ID;

function normalizeId(x) {
  var s = String(x).trim().replace(/^0+(?=\d)/, "");
  return s.length === 1 ? "0" + s : s;
}

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

// R36 (RETENTION R10): this server reads its own pinned catalog by design, so
// the list footers say which version that is and where "what's new" lives —
// an installed surface stops going silently stale.
const VERSION_NOTE = "goal-prompts v" + VERSION +
  " — this install pins its catalog; newer briefs may exist: " +
  catalog.base + "/changelog";

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
    description: "Fetch the full text of one brief by id (e.g. '30' or '6' — " +
      "single digits are zero-padded). The returned prompt is self-contained: " +
      "paste or execute it inside the target repo; it audits read-only and " +
      "writes exactly one report file.",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string", description: "Brief id, e.g. '06' or '6'" }
      },
      required: ["id"]
    }
  },
  {
    name: "make_conductor",
    description: "Compose a conductor — one prompt that fetches and runs a " +
      "custom sequence of briefs in order — from any list of brief ids. " +
      "Your own playbook: e.g. ids ['46','47'] for triage-then-fix, or " +
      "['33','49','34'] for a retrieval tune-up. Ids run in the order given. " +
      "Caps at 16 stages; split a longer campaign into two conductors.",
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
    name: "list_playbooks",
    description: "List every curated playbook: key, name, tagline, and the " +
      "brief ids it runs in order. Use get_playbook with a key to fetch its " +
      "conductor prompt.",
    inputSchema: { type: "object", properties: {} }
  },
  {
    name: "get_playbook",
    description: "Fetch a playbook conductor — a single prompt that runs a " +
      "curated sequence of briefs in order. Use list_playbooks to browse " +
      "the available keys.",
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
// Prefix matching at a word boundary does the rest: the stem starts every
// inflection. Words ending in "eed"/"eeds" keep their "ed" ("speed" must not
// become "spe"); "ies" folds to "y" so "queries" reaches "query".
function stem(w) {
  if (w.length > 5 && w.slice(-3) === "ing") return w.slice(0, -3);
  if (w.length > 4 && w.slice(-3) === "ies") return w.slice(0, -3) + "y";
  if (w.length > 4 && w.slice(-2) === "ed" && w.slice(-3) !== "eed") return w.slice(0, -2);
  if (w.length > 3 && w.slice(-1) === "s" && w.slice(-2) !== "ss") return w.slice(0, -1);
  return w;
}

// Match a stem only at the start of a word: "loop" hits "loops" and
// "looping" but not "blooper". Stems arrive as [a-z0-9]+ so no escaping.
var wordRe = {};
function matchWord(hay, w) {
  var re = wordRe[w] || (wordRe[w] = new RegExp("\\b" + w));
  return re.test(hay);
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
    if (matchWord(hay, w)) df++;
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
    if (matchWord(title, w)) m += 4;
    if (matchWord(fam, w)) m += 3;
    if (matchWord(tag, w)) m += 2;
    if (matchWord(body, w)) m += 1;
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
ids.length + " audit " + plural + " in sequence, each producing one report file in the repo's `reports/` directory.\n\n" +
desc + "\n\n" +
"## Before stage 1\n" +
"- If `CHARTER.md` exists at the repo root or in `reports/`, read it first — its goals, non-goals, and invariants bound every recommendation in every stage. No charter? Proceed, and suggest 149 · The Charter afterwards.\n" +
"- If there is no `reports/` directory at the repo root, create it now — every brief writes its report there once the directory exists, so the whole run lands in one folder instead of scattering generic filenames across the root.\n" +
"- Before fetching stage 1, tell the operator in plain words what this playbook will do — one line per stage — and ask for the go-ahead.\n" +
"- In a git repo, plan to commit as you go — one commit per report plus a final one for the index; make committing part of the go-ahead question, and skip it only if the operator says no.\n\n" +
"## How to run each stage, in order\n" +
"1. Fetch the brief with a read-only web request (for example: curl -s <url>).\n" +
"2. If your harness can run subagents or fresh sessions, run each stage in one — a stage needs only the earlier report files at the repo root and in `reports/`, never this conversation.\n" +
"3. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.\n" +
"4. Confirm the report file exists (at the repo root or in `reports/`) before moving on, and stamp one provenance line under its title — `<playbook> · stage <N>/<M> · brief <id>` — so the file itself names the run that wrote it.\n" +
"5. If committing, commit the report now, message `reports: <FILE> — <stage title> (<playbook> <N>/<M>)` — that per-stage trail is what lets any later session recover the whole run with one git log --grep.\n" +
"6. After each stage, tell the operator in two or three plain sentences what it found — the single biggest finding and why it matters for this repo — and what comes next; never advance in silence.\n" +
"7. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.\n\n" +
"## Stages\n" + stages.join("\n") + "\n\n" +
"## After the final stage\n" +
"- Write the run's index — `INDEX.md`, in the same directory as the reports (commit it last, if committing): the run date, the playbook name, each stage with its brief URL, and one line per report — file name, finding count (mark a null report as such), and its top two or three next steps. A session with no memory of this run must be able to start from that one file.\n" +
"- Present the strongest findings across every report as one ranked list, in plain words — each with why it matters for this repo; the operator should not need to open a report file to act.\n" +
"- Then ask which findings to fix. Unless 47 · The Fixer already ran as a stage of this playbook, offer to fetch " + base + "/raw/47.md and implement exactly the operator's picks — one verified commit per finding. The report files stay on disk as the paper trail.\n" +
"- Prefer a merged plan instead? Fetch " + base + "/raw/28.md (Roadmap Synthesis) to fold the reports at the repo root and in `reports/` into one sequenced plan.\n" +
"- Close with the handoff: if the run sits on an unmerged branch, offer to open a pull request titled `reports: <playbook> run <date> (<M> stages)` whose body is the index — the PR list is the first place a later session or teammate looks; either way, print a paste-ready handoff block naming the branch, the report directory, the file list, and `INDEX.md` as the place to start.\n\n" +
"## Rules\n" +
"- If a fetch fails, retry once; if it still fails, use the locally installed /goal:<slug> (or /goal-<slug>) command or the goal-prompts MCP get_brief tool for that stage; if neither exists, say so and stop — never improvise a brief from memory.\n" +
"- Honor each brief's own rules, including ending by asking before any changes.\n" +
"- If a stage's report already exists (at the repo root or in `reports/`), ask whether to re-run or skip that stage.\n" +
"- A conductor caps at 16 stages — for a longer campaign, split it into two conductors and run them back-to-back.\n";
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
      "\n\nUse get_brief with an id to fetch the full prompt.\n" + VERSION_NOTE;
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
    const b = byId[normalizeId(args.id)];
    if (!b) return "No brief with id '" + args.id + "'. " + ID_RANGE +
      "; try list_briefs.";
    return readBody(b.id);
  }
  if (name === "make_conductor") {
    var raw = args.ids;
    if (typeof raw === "string") raw = raw.split(/[\s,]+/).filter(Boolean);
    if (!Array.isArray(raw) || !raw.length) {
      return "Provide ids as an array of brief ids in run order, e.g. ['46','47']. " +
        "Use list_briefs to browse.";
    }
    var ids = raw.map(normalizeId);
    var unknown = ids.filter(function (id) { return !byId[id]; });
    if (unknown.length) {
      return "Unknown brief id(s): " + unknown.join(", ") + ". " + ID_RANGE +
        "; try list_briefs.";
    }
    if (ids.length > 16) return "That's " + ids.length +
      " briefs — a conductor caps at 16 stages; split it into two conductors and run them back-to-back.";
    var cname = args.name ? String(args.name) : "Custom sequence";
    var cdesc = "A custom sequence of " + ids.length + " brief" + (ids.length > 1 ? "s" : "") +
      ", composed via the goal-prompts MCP server.";
    return conductorText(cname, cdesc, ids);
  }
  if (name === "list_playbooks") {
    return catalog.playbooks.map(function (p) {
      return p.key + " · " + p.name + "  [" + p.ids.join(" → ") + "]" +
        "\n    " + (p.tagline || p.desc) +
        (p.tagline && p.desc ? "\n    " + p.desc : "");
    }).join("\n") +
      "\n\nUse get_playbook with a key to fetch the conductor prompt.\n" +
      VERSION_NOTE;
  }
  if (name === "get_playbook") {
    const key = String(args.key);
    const pb = catalog.playbooks.filter(function (p) { return p.key === key; })[0];
    if (!pb) return "No playbook '" + key + "'. Use list_playbooks to browse the " +
      catalog.playbooks.length + " available keys.";
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
        capabilities: { tools: {}, prompts: {} },
        serverInfo: { name: "goal-prompts", version: VERSION }
      });
    } else if (msg.method === "notifications/initialized") {
      // notification: no response
    } else if (msg.method === "ping") {
      result(id, {});
    } else if (msg.method === "prompts/list") {
      result(id, {
        prompts: briefs.map(function (b) {
          return { name: "goal-" + b.slug, description: b.tagline };
        })
      });
    } else if (msg.method === "prompts/get") {
      const pname = String((msg.params && msg.params.name) || "");
      const pb = bySlug[pname.replace(/^goal-/, "")];
      if (!pb || pname.indexOf("goal-") !== 0) {
        rpcError(id, -32602, "Unknown prompt: " + pname +
          ". Names are goal-<slug>; see prompts/list.");
      } else {
        result(id, {
          description: pb.tagline,
          messages: [{ role: "user",
            content: { type: "text", text: readBody(pb.id) } }]
        });
      }
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
