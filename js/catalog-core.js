/* catalog-core.js — the landing page's pure catalog logic, factored out so
 * Node can test it (tests/catalog_core.test.cjs). Loaded by index.html via
 * <script src="/js/catalog-core.js"> before the inline script; every function
 * takes the injected DATA/PLAYBOOKS as parameters, so it never touches the
 * DOM or globals. The conductor's canonical sentences are parity-guarded by
 * scripts/mcp-smoke.cjs against build.py and mcp/server.cjs — keep each on
 * one source line and edit all three copies together. */
(function (global) {
"use strict";

/* ---- scored matching — same scoring as the MCP server's suggest_briefs ---- */
function stemWord(w) {
  if (w.length > 5 && w.slice(-3) === "ing") return w.slice(0, -3);
  if (w.length > 4 && w.slice(-2) === "ed" && w.slice(-3) !== "eed") return w.slice(0, -2);
  if (w.length > 3 && w.slice(-1) === "s" && w.slice(-2) !== "ss") return w.slice(0, -1);
  return w;
}

var _idx = typeof WeakMap !== "undefined" ? new WeakMap() : null;
function index(data) {
  var got = _idx && _idx.get(data);
  if (got) return got;
  var hay = {};
  data.forEach(function (p) {
    hay[p.id] = {
      title: p.title.toLowerCase(),
      fam: (p.family + " " + p.question).toLowerCase(),
      tag: p.tagline.toLowerCase(),
      body: p.body.toLowerCase()
    };
  });
  var made = { hay: hay, df: {} };
  if (_idx) _idx.set(data, made);
  return made;
}

function rarity(data, ix, w) {
  if (ix.df[w] !== undefined) return ix.df[w];
  var df = 0;
  for (var i = 0; i < data.length; i++) {
    var h = ix.hay[data[i].id];
    if (h.title.indexOf(w) !== -1 || h.fam.indexOf(w) !== -1 ||
        h.tag.indexOf(w) !== -1 || h.body.indexOf(w) !== -1) df++;
  }
  return (ix.df[w] = 1 / Math.sqrt(Math.max(df, 5)));
}

function closestScored(data, q, n) {
  var ix = index(data);
  var words = String(q || "").toLowerCase().split(/[^a-z0-9]+/)
    .filter(function (w) { return w.length > 2; }).map(stemWord)
    .filter(function (w, i, a) { return a.indexOf(w) === i; });
  if (!words.length) return [];
  return data.map(function (p) {
    var h = ix.hay[p.id], s = 0;
    for (var i = 0; i < words.length; i++) {
      var w = words[i], m = 0;
      if (h.title.indexOf(w) !== -1) m += 4;
      if (h.fam.indexOf(w) !== -1) m += 3;
      if (h.tag.indexOf(w) !== -1) m += 2;
      if (h.body.indexOf(w) !== -1) m += 1;
      s += m * rarity(data, ix, w);
    }
    return { p: p, s: s };
  }).filter(function (x) { return x.s > 0; })
    .sort(function (a, b) { return b.s - a.s; })
    .slice(0, n);
}

function closest(data, q, n) {
  return closestScored(data, q, n).map(function (x) { return x.p; });
}

/* ---- filter — family chip + playbook chip + AND-substring query ---- */
function matches(p, state, playbooks) {
  state = state || {};
  if (state.playbook) {
    var pb = null;
    for (var i = 0; i < (playbooks || []).length; i++) {
      if (playbooks[i].key === state.playbook) { pb = playbooks[i]; break; }
    }
    if (!pb || pb.ids.indexOf(p.id) === -1) return false;
  }
  if (state.family && state.family !== "All" && p.family !== state.family) return false;
  var q = String(state.query || "").trim().toLowerCase();
  if (!q) return true;
  var h = (p.id + " " + p.title + " " + p.tagline + " " + p.family + " " +
           p.output + " " + p.body).toLowerCase();
  return q.split(/\s+/).every(function (t) { return h.indexOf(t) !== -1; });
}

/* ---- conductor — one prompt that runs several briefs in order ---- */
var SEQ_CAP = 16;
function makeConductor(name, desc, ids, byId, base) {
  var stages = ids.map(function (id, i) {
    var p = byId[id];
    return (i + 1) + ". **" + id + " · " + p.title + "** — fetch " + base + "/raw/" + id + ".md" +
           " → writes `" + p.output + "`";
  });
  var plural = ids.length > 1 ? "briefs" : "brief";
  return "# Playbook: " + name + " (conductor)\n\n" +
"You are working inside this repo. Mission: execute the **" + name + "** playbook — " + ids.length + " audit " + plural + " in sequence, each producing one report file at the repo root (or in `reports/`, if the repo has that directory).\n\n" +
desc + "\n\n" +
"## How to run each stage, in order\n" +
"1. Fetch the brief with a read-only web request (for example: curl -s <url>).\n" +
"2. If your harness can run subagents or fresh sessions, run each stage in one — a stage needs only the earlier report files at the repo root and in `reports/`, never this conversation.\n" +
"3. Execute it exactly as written. Every brief is read-only toward the codebase; its only write is its own report file.\n" +
"4. Confirm the report file exists (at the repo root or in `reports/`) before moving on.\n" +
"5. Proceed to the next stage. Do not parallelize — later briefs may draw on earlier reports.\n\n" +
"## Stages\n" + stages.join("\n") + "\n\n" +
"## After the final stage\n" +
"- List every report created, with a one-line takeaway each.\n" +
"- Suggest the natural next step: fetch " + base + "/raw/28.md (Roadmap Synthesis) to merge the reports at the repo root and in `reports/` into one sequenced plan.\n\n" +
"## Rules\n" +
"- If a fetch fails, retry once; if it still fails, use the locally installed /goal:<slug> (or /goal-<slug>) command or the goal-prompts MCP get_brief tool for that stage; if neither exists, say so and stop — never improvise a brief from memory.\n" +
"- Honor each brief's own rules, including ending by asking before any changes.\n" +
"- If a stage's report already exists (at the repo root or in `reports/`), ask whether to re-run or skip that stage.\n" +
"- A conductor caps at 16 stages — for a longer campaign, split it into two conductors and run them back-to-back.\n";
}

/* ---- 3-question picker — situation × pain × time → one brief or playbook ---- */
var SIT_PB = { "new": "day1", inherited: "inherit", prelaunch: "shipit",
               slow: "makefast", ai: "agentday1", idea: "gutcheck" };
var SIT_BRIEF = { "new": "00", inherited: "13", prelaunch: "01",
                  slow: "04", ai: "30", idea: "60" };
var HURT = {
  breaks:     { brief: "01", pb: "testconfidence" },
  slow:       { brief: "04", pb: "makefast" },
  security:   { brief: "06", pb: "harden" },
  conversion: { brief: "09", pb: "founderfunnel" },
  design:     { brief: "54", pb: "facelift" },
  data:       { brief: "19", pb: "datalayer" },
  agent:      { brief: "30", pb: "agentday1" }
};
function pickerPlan(a, data, playbooks) {
  a = a || {};
  var byId = {};
  (data || []).forEach(function (p) { byId[p.id] = p; });
  var pbs = {};
  (playbooks || []).forEach(function (pb) { pbs[pb.key] = pb; });
  var hurt = HURT[a.hurt] || null;
  var time = a.time || (hurt && !SIT_PB[a.situation] ? "brief" : "playbook");
  if (time === "playbook") {
    var key = SIT_PB[a.situation] || (hurt && hurt.pb) || "day1";
    if (pbs[key]) return { kind: "playbook", key: key, alt: "46" };
  }
  var id = (hurt && hurt.brief) || SIT_BRIEF[a.situation] || "46";
  if (!byId[id]) id = "46";
  return { kind: "brief", id: id, alt: "46" };
}

/* ---- per-repo recommendation — root listing + package.json → briefs ---- */
function repoRecommend(names, pkg, data) {
  names = names || [];
  var has = {};
  names.forEach(function (n) { has[String(n).toLowerCase()] = true; });
  var any = function (re) { return names.some(function (n) { return re.test(String(n)); }); };
  var deps = {};
  if (pkg) {
    ["dependencies", "devDependencies", "peerDependencies"].forEach(function (k) {
      var d = pkg[k];
      if (d && typeof d === "object") Object.keys(d).forEach(function (n) { deps[n] = true; });
    });
  }
  var stack = [], ids = [];
  var add = function (id) { if (ids.indexOf(id) === -1) ids.push(id); };
  if (deps.next) { stack.push("Next.js"); add("88"); }
  else if (deps.react) { stack.push("React"); add("88"); }
  if (deps.vue || deps.nuxt) { stack.push("Vue"); add("88"); }
  if (deps.svelte) { stack.push("Svelte"); add("88"); }
  if (deps.express || deps.fastify || deps.koa || deps.hono) { stack.push("Node API"); add("18"); }
  if (deps["@anthropic-ai/sdk"] || deps.openai || deps.langchain || deps.ai ||
      any(/^(prompts?|evals?)$/i)) { stack.push("LLM/agent code"); add("30"); add("35"); }
  if (deps.stripe) { stack.push("Stripe"); add("110"); }
  if (has["tsconfig.json"] || deps.typescript) { stack.push("TypeScript"); add("99"); }
  if (has["go.mod"]) { stack.push("Go"); }
  if (has["requirements.txt"] || has["pyproject.toml"]) { stack.push("Python"); }
  if (has["cargo.toml"]) { stack.push("Rust"); }
  if (has["dockerfile"] || has["docker-compose.yml"] || has["docker-compose.yaml"] ||
      any(/\.tf$/i) || has.terraform || has.helm || has.k8s) { stack.push("Docker/IaC"); add("137"); }
  if (any(/^(migrations|prisma|db)$/i) || has["schema.prisma"]) { stack.push("SQL database"); add("19"); }
  if (pkg && pkg.bin) { stack.push("a CLI"); add("135"); }
  else if (pkg && pkg.private !== true && (pkg.main || pkg.exports || pkg.module)) { add("136"); }
  ["01", "02", "16"].forEach(function (id) { if (ids.length < 3) add(id); });
  ids = ids.slice(0, 5).filter(function (id) {
    return (data || []).some(function (p) { return p.id === id; });
  });
  return { stack: stack, ids: ids };
}

var GPCatalogCore = {
  stemWord: stemWord,
  closest: closest,
  closestScored: closestScored,
  matches: matches,
  makeConductor: makeConductor,
  pickerPlan: pickerPlan,
  repoRecommend: repoRecommend,
  SEQ_CAP: SEQ_CAP
};
if (typeof module !== "undefined" && module.exports) module.exports = GPCatalogCore;
global.GPCatalogCore = GPCatalogCore;
})(typeof window !== "undefined" ? window : globalThis);
