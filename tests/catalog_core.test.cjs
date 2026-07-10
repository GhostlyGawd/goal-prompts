#!/usr/bin/env node
/* Unit tests for js/catalog-core.js — the landing page's pure catalog logic.
 * Zero dependencies; run directly (node tests/catalog_core.test.cjs) or via
 * scripts/check. Ranking cases run against the real built catalog (catalog.json
 * + raw/), so a scoring regression that reorders marquee results fails here. */
"use strict";
const assert = require("assert");
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const CC = require(path.join(ROOT, "js", "catalog-core.js"));
const catalog = JSON.parse(fs.readFileSync(path.join(ROOT, "catalog.json"), "utf8"));
const DATA = catalog.briefs.map(b => ({
  ...b, body: fs.readFileSync(path.join(ROOT, "raw", b.id + ".md"), "utf8"),
}));
const PLAYBOOKS = JSON.parse(fs.readFileSync(path.join(ROOT, "playbooks.json"), "utf8"));
const BY_ID = {};
DATA.forEach(p => { BY_ID[p.id] = p; });
const BASE = "https://goal-prompts.vercel.app";

const failures = [];
function t(name, fn) {
  try { fn(); console.log("  ok    " + name); }
  catch (e) { console.log("  FAIL  " + name + " — " + e.message); failures.push(name); }
}

// ---- closest() ranking ------------------------------------------------------
t("closest: 'speed' puts 04 · Performance Audit in the top 3", () => {
  const top = CC.closest(DATA, "speed", 3).map(p => p.id);
  assert(top.includes("04"), "top 3 was " + top.join(","));
});
t("closest: 'bug' ranks 01 · Bug Hunt first", () => {
  assert.strictEqual(CC.closest(DATA, "bug", 3)[0].id, "01");
});
t("closest: 'checkout drop-off' surfaces 110 first", () => {
  assert.strictEqual(CC.closest(DATA, "checkout drop-off", 3)[0].id, "110");
});
t("closest: 'prompt injection' ranks 118 · Prompt-Injection Red-Team first", () => {
  assert.strictEqual(CC.closest(DATA, "prompt injection", 3)[0].id, "118");
});
t("closest: stemmer leaves 'needs' family words intact (eed exemption)", () => {
  assert.strictEqual(CC.stemWord("needs"), "need");
  assert.strictEqual(CC.stemWord("indeed"), "indeed");
  assert.strictEqual(CC.stemWord("loading"), "load");
});
t("closest: empty and sub-3-char queries return nothing", () => {
  assert.deepStrictEqual(CC.closest(DATA, "", 5), []);
  assert.deepStrictEqual(CC.closest(DATA, "a b", 5), []);
});

// ---- fuzzy zero-state fallback (FORMS FV11 / R41) ---------------------------
t("fuzzy: typo 'preformance' (transposition) still finds 04 · Performance Audit", () => {
  const top = CC.closest(DATA, "preformance", 3).map(p => p.id);
  assert(top.length > 0, "no fallback results");
  assert.strictEqual(top[0], "04", "top was " + top.join(","));
});
t("fuzzy: typo 'secruity' (transposition) surfaces a security brief", () => {
  const top = CC.closest(DATA, "secruity", 3);
  assert(top.length > 0, "no fallback results");
  assert(top.some(p => (p.title + " " + p.family).toLowerCase().includes("secur")),
    "top was " + top.map(p => p.id + " " + p.title).join(", "));
});
t("fuzzy: typo 'cachng' (dropped letter) finds cache briefs", () => {
  const top = CC.closest(DATA, "cachng", 5);
  assert(top.length > 0, "no fallback results");
  assert(top.some(p => p.id === "140"), "top was " + top.map(p => p.id).join(","));
});
t("fuzzy: gibberish 'zzqxzz' still returns nothing", () => {
  assert.deepStrictEqual(CC.closest(DATA, "zzqxzz", 5), []);
});
t("fuzzy: never fires when the exact query already matches", () => {
  // 'bug' matches directly; fallback must not reorder the exact ranking
  assert.strictEqual(CC.closest(DATA, "bug", 3)[0].id, "01");
});

// ---- matches() composition ---------------------------------------------------
t("matches: family filter + query compose (AND, within the family)", () => {
  const state = { family: "Speed", query: "cache" };
  const hits = DATA.filter(p => CC.matches(p, state, PLAYBOOKS));
  assert(hits.length > 0, "no hits");
  assert(hits.every(p => p.family === "Speed"));
  assert(hits.some(p => p.id === "140"));
  assert(!hits.some(p => p.family !== "Speed"));
});
t("matches: playbook filter restricts to the playbook's ids", () => {
  const day1 = PLAYBOOKS.find(pb => pb.key === "day1");
  const hits = DATA.filter(p => CC.matches(p, { playbook: "day1" }, PLAYBOOKS));
  assert.deepStrictEqual(hits.map(p => p.id).sort(), day1.ids.slice().sort());
});
t("matches: no state matches everything", () => {
  assert.strictEqual(DATA.filter(p => CC.matches(p, {}, PLAYBOOKS)).length, DATA.length);
});

// ---- makeConductor() ----------------------------------------------------------
t("conductor: text contains every stage id and output", () => {
  const pb = PLAYBOOKS.find(p => p.key === "day1");
  const text = CC.makeConductor(pb.name, pb.desc, pb.ids, BY_ID, BASE);
  for (const id of pb.ids) {
    assert(text.includes(id + " · " + BY_ID[id].title), "missing stage " + id);
    assert(text.includes("`" + BY_ID[id].output + "`"), "missing output for " + id);
  }
  assert(text.includes("A conductor caps at 16 stages"));
});
t("conductor: matches build.py's committed raw/playbook-*.md byte for byte, all " + PLAYBOOKS.length + " playbooks", () => {
  for (const pb of PLAYBOOKS) {
    const built = fs.readFileSync(path.join(ROOT, "raw", "playbook-" + pb.key + ".md"), "utf8");
    assert.strictEqual(CC.makeConductor(pb.name, pb.desc, pb.ids, BY_ID, BASE), built,
      "conductor drift for playbook " + pb.key);
  }
});
t("conductor: SEQ_CAP is the documented 16", () => {
  assert.strictEqual(CC.SEQ_CAP, 16);
});

// ---- pickerPlan() --------------------------------------------------------------
t("picker: situation=new repo → the day1 playbook", () => {
  assert.deepStrictEqual(CC.pickerPlan({ situation: "new" }, DATA, PLAYBOOKS),
    { kind: "playbook", key: "day1", alt: "46" });
});
t("picker: hurt=breaks + time=brief → 01 · Bug Hunt", () => {
  const plan = CC.pickerPlan({ situation: "new", hurt: "breaks", time: "brief" }, DATA, PLAYBOOKS);
  assert.deepStrictEqual(plan, { kind: "brief", id: "01", alt: "46" });
});
t("picker: an explicit 'not sure' answer → the 46 · Audit Triage escape, never day1", () => {
  assert.deepStrictEqual(CC.pickerPlan({ hurt: "unsure" }, DATA, PLAYBOOKS),
    { kind: "brief", id: "46", alt: "46" });
  assert.deepStrictEqual(CC.pickerPlan({ hurt: "unsure", time: "playbook" }, DATA, PLAYBOOKS),
    { kind: "brief", id: "46", alt: "46" });
});
t("picker: 'not sure' defers to a real situation answer", () => {
  assert.deepStrictEqual(CC.pickerPlan({ situation: "new", hurt: "unsure" }, DATA, PLAYBOOKS),
    { kind: "playbook", key: "day1", alt: "46" });
});
t("picker: nothing answered → 46 · Audit Triage as the fallback", () => {
  const plan = CC.pickerPlan({ time: "brief" }, DATA, PLAYBOOKS);
  assert.deepStrictEqual(plan, { kind: "brief", id: "46", alt: "46" });
});
t("picker: every mapped playbook key and brief id exists in the catalog", () => {
  const keys = new Set(PLAYBOOKS.map(pb => pb.key));
  const sits = ["new", "inherited", "prelaunch", "slow", "ai", "idea"];
  const hurts = ["breaks", "slow", "security", "conversion", "design", "data", "agent"];
  for (const s of sits) {
    const p = CC.pickerPlan({ situation: s }, DATA, PLAYBOOKS);
    assert(p.kind !== "playbook" || keys.has(p.key), s + " → dead playbook " + p.key);
    const b = CC.pickerPlan({ situation: s, time: "brief" }, DATA, PLAYBOOKS);
    assert(BY_ID[b.id], s + " → dead brief " + b.id);
  }
  for (const h of hurts) {
    const p = CC.pickerPlan({ hurt: h, time: "playbook" }, DATA, PLAYBOOKS);
    assert(p.kind !== "playbook" || keys.has(p.key), h + " → dead playbook " + p.key);
    const b = CC.pickerPlan({ hurt: h }, DATA, PLAYBOOKS);
    assert(BY_ID[b.id], h + " → dead brief " + b.id);
  }
});

// ---- repoRecommend() ------------------------------------------------------------
t("repoRecommend: React + Stripe + Docker repo → relevant briefs + stack", () => {
  const rec = CC.repoRecommend(
    ["package.json", "Dockerfile", "tsconfig.json", "src"],
    { dependencies: { react: "^18", stripe: "^14" } }, DATA);
  assert(rec.ids.includes("88"), "no bundle audit");
  assert(rec.ids.includes("110"), "no checkout audit");
  assert(rec.ids.includes("137"), "no infra audit");
  assert(rec.stack.includes("React") && rec.stack.includes("Stripe"));
  assert(rec.ids.length >= 3 && rec.ids.length <= 5, "got " + rec.ids.length);
});
t("repoRecommend: bare repo still recommends 3 universal briefs", () => {
  const rec = CC.repoRecommend(["README.md", "src"], null, DATA);
  assert(rec.ids.length >= 3 && rec.ids.length <= 5);
  rec.ids.forEach(id => assert(BY_ID[id], "dead id " + id));
});
t("repoRecommend: every recommendable id exists in the catalog", () => {
  const rec = CC.repoRecommend(
    ["package.json", "Dockerfile", "go.mod", "prisma", "prompts", "main.tf", "schema.prisma"],
    { bin: { x: "x" }, dependencies: { next: "1", express: "1", stripe: "1",
      "@anthropic-ai/sdk": "1", typescript: "1" } }, DATA);
  rec.ids.forEach(id => assert(BY_ID[id], "dead id " + id));
  assert(rec.ids.length <= 5);
});

// ---- property: seeded random queries never break closest() ----------------------
t("property: 200 seeded random queries — no throw, bounded, finite scores", () => {
  let seed = 0x9e3779b9;
  function rnd() { // mulberry32
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let z = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    z = (z + Math.imul(z ^ (z >>> 7), 61 | z)) ^ z;
    return ((z ^ (z >>> 14)) >>> 0) / 4294967296;
  }
  const chars = "abcdefghijklmnopqrstuvwxyz0123456789 -_/.!?\"'()<>&;éπ漢";
  const words = ["speed", "bug", "auth", "flaky", "index", "drop", "prompt",
                 "s", "ss", "needs", "looping", "cached", ""];
  for (let i = 0; i < 200; i++) {
    let q = "";
    if (rnd() < 0.5) {
      const len = Math.floor(rnd() * 40);
      for (let j = 0; j < len; j++) q += chars[Math.floor(rnd() * chars.length)];
    } else {
      const n = 1 + Math.floor(rnd() * 5);
      for (let j = 0; j < n; j++) q += words[Math.floor(rnd() * words.length)] + " ";
    }
    const n = 1 + Math.floor(rnd() * 25);
    const scored = CC.closestScored(DATA, q, n);
    assert(scored.length <= n, "over cap for " + JSON.stringify(q));
    scored.forEach(x => {
      assert(Number.isFinite(x.s) && x.s > 0, "bad score for " + JSON.stringify(q));
      assert(BY_ID[x.p.id], "bad brief for " + JSON.stringify(q));
    });
  }
});

// ---- body-less DATA (R29 / SEO-2): the landing page's payload has no body --
t("metadata-only: matches() works without a body field", () => {
  const p = { id: "01", title: "Bug Hunt", tagline: "find bugs", family: "Quality",
              question: "Where is it broken?", output: "BUGS.md" };
  assert(CC.matches(p, { family: "All", query: "bug" }, PLAYBOOKS));
  assert(CC.matches(p, { family: "Quality", query: "" }, PLAYBOOKS));
  assert(!CC.matches(p, { family: "All", query: "zebra" }, PLAYBOOKS));
});
t("withBodies: body-only terms rank again after the zero-state upgrade", () => {
  const LITE = catalog.briefs.map(b => ({ ...b }));
  assert.deepStrictEqual(CC.closest(LITE, "backpressure", 5), [], "should miss without bodies");
  const bodies = {};
  catalog.briefs.forEach(b => { bodies[b.id] = fs.readFileSync(path.join(ROOT, "raw", b.id + ".md"), "utf8"); });
  const full = CC.withBodies(LITE, bodies);
  assert.strictEqual(CC.closest(full, "backpressure", 5)[0].id, "39");
  assert.strictEqual(CC.closest(full, "cardinality", 5)[0].id, "73");
  assert.deepStrictEqual(CC.closest(full, "zzqxzz", 5), [], "absent terms stay an honest zero");
  // the source array is untouched (no cache-poisoning of the lite index)
  assert.strictEqual(LITE[0].body, undefined);
});
t("withBodies: missing map entries become empty bodies, not crashes", () => {
  const full = CC.withBodies([{ id: "01", title: "Bug Hunt", tagline: "t", family: "Quality",
                                question: "q", output: "BUGS.md" }], null);
  assert.strictEqual(full[0].body, "");
  assert(CC.matches(full[0], { family: "All", query: "bug" }, PLAYBOOKS));
});
t("metadata-only: closest() still ranks on title/family/tagline", () => {
  const LITE = catalog.briefs.map(b => ({ ...b }));   // no body key at all
  const top = CC.closest(LITE, "bug", 3).map(p => p.id);
  assert.strictEqual(top[0], "01", "top was " + top.join(","));
  const perf = CC.closest(LITE, "speed", 5).map(p => p.id);
  assert(perf.includes("04"), "speed top 5 was " + perf.join(","));
});

if (failures.length) {
  console.error("\n" + failures.length + " catalog-core test(s) failed");
  process.exit(1);
}
console.log("\nOK  catalog-core: all tests passed");
