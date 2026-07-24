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
      /* body is optional since R29 (SEO-2): the landing page's DATA carries
         metadata only — search there runs on title/family/question/tagline.
         Callers that do have bodies (tests, MCP-parity checks) still get the
         body-weighted scoring. */
      body: (p.body || "").toLowerCase()
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

function scoreAll(data, ix, words, n) {
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

/* true when a and b are exactly one edit apart — substitution, insertion,
 * deletion, or an adjacent transposition ("preformance" → "performance"),
 * i.e. optimal-string-alignment distance 1 */
function edit1(a, b) {
  var d = a.length - b.length;
  if (d < -1 || d > 1) return false;
  if (d !== 0) {                                   // one insertion/deletion
    if (d < 0) { var t = a; a = b; b = t; }        // make a the longer one
    var i = 0;
    while (i < b.length && a[i] === b[i]) i++;
    return a.slice(i + 1) === b.slice(i);
  }
  if (a === b) return false;
  var j = 0;
  while (a[j] === b[j]) j++;
  if (a.slice(j + 1) === b.slice(j + 1)) return true;      // one substitution
  return a[j] === b[j + 1] && a[j + 1] === b[j] &&         // one transposition
         a.slice(j + 2) === b.slice(j + 2);
}

/* FV11: when the scored pass finds nothing, try correcting each query word to
 * a catalog word one edit away (same-first-letter candidates preferred). The
 * corrected list re-scores through the normal path; null = nothing to fix. */
function fuzzyWords(data, ix, words) {
  if (!ix.vocab) {
    var seen = {}, vocab = [];
    for (var di = 0; di < data.length; di++) {
      var h = ix.hay[data[di].id];
      var ws = (h.title + " " + h.fam + " " + h.tag + " " + h.body).split(/[^a-z0-9]+/);
      for (var wi = 0; wi < ws.length; wi++) {
        var vw = ws[wi];
        if (vw.length >= 4 && !seen[vw]) { seen[vw] = true; vocab.push(vw); }
      }
    }
    ix.vocab = vocab;
  }
  var out = [], changed = false;
  for (var qi = 0; qi < words.length; qi++) {
    var w = words[qi], fix = null;
    if (w.length >= 4) {
      for (var vi = 0; vi < ix.vocab.length; vi++) {
        var c = ix.vocab[vi];
        if (!edit1(w, c)) continue;
        if (c[0] === w[0]) { fix = c; break; }
        if (!fix) fix = c;
      }
    }
    if (fix) { out.push(fix); changed = true; } else out.push(w);
  }
  return changed ? out : null;
}

function closestScored(data, q, n) {
  var ix = index(data);
  var words = String(q || "").toLowerCase().split(/[^a-z0-9]+/)
    .filter(function (w) { return w.length > 2; }).map(stemWord)
    .filter(function (w, i, a) { return a.indexOf(w) === i; });
  if (!words.length) return [];
  var hits = scoreAll(data, ix, words, n);
  if (hits.length) return hits;
  /* zero hits — a typo shouldn't strand the user (FORMS FV11): one cheap
   * edit-distance-1 pass over the catalog vocabulary, then re-score */
  var fixed = fuzzyWords(data, ix, words);
  return fixed ? scoreAll(data, ix, fixed, n) : [];
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
           p.output + " " + (p.body || "")).toLowerCase();
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
"You are working inside this repo. Mission: execute the **" + name + "** playbook — " + ids.length + " audit " + plural + " in sequence, each producing one report file in the repo's `reports/` directory.\n\n" +
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
  /* an explicit "not sure" is an answer, not an omission — without a situation
     to route on, hand off to 46 · Audit Triage instead of defaulting to day1 */
  if (a.hurt === "unsure" && !SIT_PB[a.situation] && !SIT_BRIEF[a.situation]) {
    return { kind: "brief", id: byId["46"] ? "46" : (data && data[0] && data[0].id), alt: "46" };
  }
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

/* R29 (SEO-2): merge fetched bodies into a metadata-only catalog. Returns a
 * NEW array of copies — index()'s WeakMap cache keys on array identity, so
 * the merged corpus gets its own body-weighted index and the lite one stays
 * untouched. The landing page uses this to upgrade a zero-result search once
 * bodies.json arrives. */
function withBodies(data, bodies) {
  return (data || []).map(function (p) {
    return Object.assign({}, p, { body: (bodies && bodies[p.id]) || "" });
  });
}

var GPCatalogCore = {
  stemWord: stemWord,
  closest: closest,
  closestScored: closestScored,
  matches: matches,
  withBodies: withBodies,
  makeConductor: makeConductor,
  pickerPlan: pickerPlan,
  repoRecommend: repoRecommend,
  SEQ_CAP: SEQ_CAP
};
if (typeof module !== "undefined" && module.exports) module.exports = GPCatalogCore;
global.GPCatalogCore = GPCatalogCore;
})(typeof window !== "undefined" ? window : globalThis);
