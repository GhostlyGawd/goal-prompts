#!/usr/bin/env node
/* Tests for js/report-parser.js — the Report Studio's markdown-report parser,
 * extracted from studio.html so Node can test it. Zero dependencies; run
 * directly (node tests/report_parser.test.cjs) or via scripts/check.
 *
 * The stakes: the parser feeds the Studio checklist and the Fixer prompt.
 * Finding keys are content hashes stored in localStorage (gp-studio-checks),
 * so the key scheme for already-parsing shapes (bold-led blocks, list items)
 * must never change — the key-stability test pins it. */
"use strict";
const assert = require("assert");
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const RP = require(path.join(ROOT, "js", "report-parser.js"));

const failures = [];
function t(name, fn) {
  try { fn(); console.log("  ok    " + name); }
  catch (e) { console.log("  FAIL  " + name + " — " + e.message); failures.push(name); }
}
function findings(text, name) { return RP.parseReport(name || "R.md", text).findings; }

// ---- ###/#### findings (the silent-drop bug) --------------------------------
t("### numbered heading + body paragraphs become one finding", () => {
  const f = findings([
    "## Findings", "",
    "### 1. Copy button races on double tap", "",
    "Location: template.html. The second call captures the wrong label.", "",
    "Repro: tap twice within 1.6 seconds and watch it stick.",
  ].join("\n"));
  assert.strictEqual(f.length, 1, "got " + f.length + " findings");
  assert.strictEqual(f[0].title, "Copy button races on double tap");
  assert(f[0].text.includes("Location: template.html"), "body paragraph 1 missing");
  assert(f[0].text.includes("Repro: tap twice"), "body paragraph 2 missing");
  assert.strictEqual(f[0].section, "Findings");
});
t("#### headings become findings too", () => {
  const f = findings([
    "## Audit", "",
    "#### Slow query on the dashboard",
    "The dashboard endpoint scans the whole table on every load.",
    "",
    "#### Missing index on the user column",
    "Every lookup does a sequential scan over four million rows.",
  ].join("\n"));
  assert.strictEqual(f.length, 2);
  assert.strictEqual(f[0].title, "Slow query on the dashboard");
  assert.strictEqual(f[1].title, "Missing index on the user column");
});
t("### finding body may span several heading-free blocks", () => {
  const f = findings([
    "## Findings", "",
    "### 2. Stale cache never invalidates", "",
    "First paragraph of evidence, long enough to matter.", "",
    "- a supporting bullet",
    "- another supporting bullet", "",
    "### 3. Second finding here",
    "Its own body, also long enough to count as real.",
  ].join("\n"));
  assert.strictEqual(f.length, 2, "got " + f.map(x => x.title).join(" | "));
  assert(f[0].text.includes("supporting bullet"), "bullets folded into the ### finding");
  assert.strictEqual(f[1].title, "Second finding here");
});

// ---- shapes that already worked must keep working ----------------------------
t("bold-led block still parses, and its key scheme is byte-stable", () => {
  const text = "**Login times out under load — S2**\nThe pool is capped at 4 connections and requests queue forever.";
  const f = findings("## Findings\n\n" + text, "BUGS.md");
  assert.strictEqual(f.length, 1);
  assert.strictEqual(f[0].title, "Login times out under load — S2");
  // gp-studio-checks stores these keys in localStorage — the scheme must not move
  const expected = "f" + RP.hash("BUGS.md" + "|" + f[0].title + "|" + f[0].text.slice(0, 120));
  assert.strictEqual(f[0].key, expected);
});
t("numbered and dashed list items still parse; short nav lines still skipped", () => {
  const f = findings([
    "## Quick wins", "",
    "1. **Add a loading state** — the empty flash reads as broken on slow networks",
    "2. **Debounce the search box** — every keystroke refetches the whole catalog",
    "- see also",
    "- Rename the misleading `utils` module so newcomers stop importing the wrong one",
  ].join("\n"));
  assert.strictEqual(f.length, 3, f.map(x => x.title).join(" | "));
  assert.strictEqual(f[0].title, "Add a loading state");
  assert(f[2].title.includes("Rename the misleading"));
});
t("effort/impact/tag chips still extract", () => {
  const f = findings("## L\n\n**Thing one** — effort: M, impact: H\nNEW body text long enough to hold both markers in place.");
  assert.strictEqual(f[0].effort, "M");
  assert.strictEqual(f[0].impact, "H");
});
t("plain prose blocks are context, not findings", () => {
  const r = RP.parseReport("R.md", [
    "## Summary", "",
    "Five findings overall; the scariest is the cache one. This paragraph is a summary, not a finding.",
  ].join("\n"));
  assert.strictEqual(r.findings.length, 0);
  assert(r.skipped >= 1, "prose block should be counted as unrecognized");
});

// ---- severity: first line or an explicit Severity: label only ----------------
t("severity read from the finding's first line", () => {
  const f = findings("## F\n\n**Broken checkout — S1 · certain**\nBody prose here, long enough.");
  assert.strictEqual(f[0].sev, "S1");
});
t("explicit 'Severity: high' label anywhere in the body counts", () => {
  const f = findings("## F\n\n**Broken thing**\nEvidence line one.\nSeverity: high\nMore prose.");
  assert.strictEqual(f[0].sev, "S2");
});
t("'high-traffic' in prose must NOT set a severity", () => {
  const f = findings("## F\n\n**Slow endpoint**\nThis is a high-traffic route and the queue backs up during peaks.");
  assert.strictEqual(f[0].sev, null, "got " + f[0].sev);
});
t("'critical' inside a fix description must NOT mark S1", () => {
  const f = findings("## F\n\n**Flaky test in CI**\nThe fix is critical to land before the release branch cut.");
  assert.strictEqual(f[0].sev, null, "got " + f[0].sev);
});
t("'low-hanging' in the first line must not read as severity Low", () => {
  const f = findings("## F\n\n**Some low-hanging cleanup in the utils module**\nLonger body prose so the block parses.");
  assert.strictEqual(f[0].sev, null, "got " + f[0].sev);
});
t("### finding title carries severity like a bold title does", () => {
  const f = findings("## F\n\n### 4. Sessions never expire — S3 · likely\nCookies live forever; body long enough to parse.");
  assert.strictEqual(f[0].sev, "S3");
});

// ---- fixed/shipped: status positions only -------------------------------------
t("FIXED in the title line marks done (the BUGS.md house style)", () => {
  const f = findings("## F\n\n**Copy-button label race — S2 · certain · FIXED in 0.4**\nRoot cause prose, long enough to parse fine.");
  assert.strictEqual(f[0].fixed, true);
});
t("'Status: shipped' line marks done", () => {
  const f = findings("## F\n\n**Slow dashboard**\nEvidence prose first.\nStatus: shipped in 0.9");
  assert.strictEqual(f[0].fixed, true);
});
t("a line starting with 'Fixed …' marks done", () => {
  const f = findings("## F\n\n**Broken redirect**\nEvidence prose first.\nFixed in commit abc123.");
  assert.strictEqual(f[0].fixed, true);
});
t("a checked checkbox marks done", () => {
  const f = findings("## F\n\n- [x] **Rotate the leaked token** — it is still live in CI and that is scary");
  assert.strictEqual(f.length, 1);
  assert.strictEqual(f[0].fixed, true);
});
t("'shipped'/'fixed' in mid-sentence prose must NOT mark done", () => {
  const f = findings("## F\n\n**Onboarding drop-off**\nThe welcome email we shipped last spring never links back, so users who fixed their profile still bounce.");
  assert.strictEqual(f[0].fixed, false, "prose mention marked it done");
});

// ---- code fences are inert structure --------------------------------------------
t("a fenced ### heading does not mint a finding", () => {
  const r = RP.parseReport("R.md", [
    "## Findings", "",
    "```",
    "### not a finding, just a config sample",
    "with a body line inside the fence",
    "```",
  ].join("\n"));
  assert.strictEqual(r.findings.length, 0,
    "fenced ### minted: " + r.findings.map(f => f.title).join(" | "));
});
t("a fence containing blank lines and a ### stays one inert region", () => {
  const r = RP.parseReport("R.md", [
    "## Findings", "",
    "```",
    "some output first", "",
    "### 9. looks exactly like a finding heading", "",
    "Severity: S1",
    "```",
  ].join("\n"));
  assert.strictEqual(r.findings.length, 0,
    "got " + r.findings.map(f => f.title).join(" | "));
});
t("a fenced 'Severity: S1' line does not grade the finding", () => {
  const f = findings([
    "## F", "",
    "**Log format confuses the triage script** — the sample below trips it.",
    "```",
    "Severity: S1",
    "```",
    "The script greps for that literal string and misfires.",
  ].join("\n"));
  assert.strictEqual(f.length, 1);
  assert.strictEqual(f[0].sev, null, "graded from inside a fence: " + f[0].sev);
  assert(f[0].text.includes("Severity: S1"), "fence content must stay in the body");
});
t("### finding keeps its fenced example verbatim in the body", () => {
  const f = findings([
    "## F", "",
    "### 1. Loader rejects its own documented sample", "",
    "The config loader errors on the exact sample the docs ship:", "",
    "```",
    "### section header in the config format", "",
    "retry = critical",
    "```",
  ].join("\n"));
  assert.strictEqual(f.length, 1, "got " + f.map(x => x.title).join(" | "));
  assert.strictEqual(f[0].title, "Loader rejects its own documented sample");
  assert(f[0].text.includes("### section header in the config format"), "fenced heading lost");
  assert(f[0].text.includes("retry = critical"), "fenced body line lost");
  assert.strictEqual(f[0].sev, null, "graded from fenced 'critical': " + f[0].sev);
});
t("fenced 'Status: fixed' does not mark a finding done", () => {
  const f = findings([
    "## F", "",
    "**Deploy log is misleading** — it prints a done line before the rollout.",
    "```",
    "Status: fixed",
    "```",
    "Operators read that and walk away mid-deploy.",
  ].join("\n"));
  assert.strictEqual(f[0].fixed, false, "fence content marked it done");
});

// ---- unrecognized-block accounting ---------------------------------------------
t("parseReport reports skipped blocks so the Studio can say so", () => {
  const r = RP.parseReport("R.md", [
    "## Findings", "",
    "**A real finding** — with enough body to parse as one.", "",
    "A stray analysis paragraph that matches no finding shape but is clearly substantive content.",
  ].join("\n"));
  assert.strictEqual(r.findings.length, 1);
  assert.strictEqual(r.skipped, 1);
});
t("a fully recognized report has zero skipped blocks", () => {
  const r = RP.parseReport("R.md", "## F\n\n**Only finding** — body long enough to parse without residue.");
  assert.strictEqual(r.skipped, 0);
});
t("a dropped short ###-block counts as unrecognized", () => {
  const r = RP.parseReport("R.md", "## F\n\n### Stub\ntiny");
  assert.strictEqual(r.findings.length, 0);
  assert.strictEqual(r.skipped, 1, "short ### block not counted, skipped=" + r.skipped);
});

// ---- the repo's own dogfood reports (real-world regression) ---------------------
t("BUGS.md in reports/ parses to its 5 findings, all severity-tagged and fixed", () => {
  const text = fs.readFileSync(path.join(ROOT, "reports", "BUGS.md"), "utf8");
  const f = findings(text, "BUGS.md");
  assert.strictEqual(f.length, 5, "got " + f.length);
  f.forEach(x => {
    assert(x.sev === "S2" || x.sev === "S3", x.title + " → " + x.sev);
    assert.strictEqual(x.fixed, true, x.title + " not marked fixed");
  });
});
t("IMPROVEMENTS.md parses to a non-trivial finding list", () => {
  const text = fs.readFileSync(path.join(ROOT, "reports", "IMPROVEMENTS.md"), "utf8");
  assert(findings(text, "IMPROVEMENTS.md").length >= 8);
});

// ---- property: seeded random markdown never breaks the parser --------------------
t("property: 300 seeded random reports — no throw, no empty titles, ### blocks ≥30 chars captured", () => {
  let seed = 0xdecafbad;
  function rnd() { // mulberry32
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let z = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    z = (z + Math.imul(z ^ (z >>> 7), 61 | z)) ^ z;
    return ((z ^ (z >>> 14)) >>> 0) / 4294967296;
  }
  const words = ["cache", "query", "flaky", "token", "index", "retry", "queue",
                 "shipped", "fixed", "critical", "high-traffic", "S1", "low"];
  function phrase(n) {
    let out = [];
    for (let i = 0; i < n; i++) out.push(words[Math.floor(rnd() * words.length)]);
    return out.join(" ");
  }
  for (let i = 0; i < 300; i++) {
    const parts = [];
    const heads = [];
    const nb = 2 + Math.floor(rnd() * 10);
    for (let j = 0; j < nb; j++) {
      const roll = rnd();
      if (roll < 0.15) parts.push("## " + phrase(2));
      else if (roll < 0.3) {
        const title = "Finding " + i + "x" + j + " " + phrase(2);
        const body = phrase(1 + Math.floor(rnd() * 12));
        parts.push("### " + title + (rnd() < 0.5 ? "\n" : "\n\n") + body);
        heads.push({ title: title, size: ("### " + title + "\n" + body).length });
      }
      else if (roll < 0.4) parts.push("###" + (rnd() < 0.3 ? "" : " "));  // degenerate heading
      else if (roll < 0.55) parts.push("**" + phrase(3) + "** — " + phrase(6));
      else if (roll < 0.7) parts.push("- " + phrase(2 + Math.floor(rnd() * 8)));
      else if (roll < 0.8) parts.push((1 + j) + ". **" + phrase(2) + "** — " + phrase(5));
      else parts.push(phrase(3 + Math.floor(rnd() * 10)));
    }
    const text = parts.join("\n\n");
    let r;
    try { r = RP.parseReport("rand" + i + ".md", text); }
    catch (e) { throw new Error("parser threw on seed report " + i + ": " + e.message); }
    assert(Array.isArray(r.findings) && typeof r.skipped === "number", "bad shape on " + i);
    r.findings.forEach(f => {
      assert(f.title && f.title.trim().length > 0, "empty title in report " + i);
      assert(typeof f.key === "string" && f.key[0] === "f", "bad key in report " + i);
    });
    for (const h of heads) {
      if (h.size < 30) continue;
      const want = RP.firstWords(h.title.replace(/^\d+\.\s*/, ""));
      assert(r.findings.some(f => f.title === want),
        "### block dropped in report " + i + ": " + h.title);
    }
  }
});

// ---- inferReportName — Studio paste name inference (FORMS FV1 / R38) --------
t("inferReportName: ALL-CAPS .md token in the first heading wins", () => {
  assert.strictEqual(
    RP.inferReportName("# FORMS.md — Forms & Validation Audit\n\ntext"),
    "FORMS.md");
  assert.strictEqual(
    RP.inferReportName("intro line\n\n# SECURITY-AUDIT.md\n\n## Findings"),
    "SECURITY-AUDIT.md");
});
t("inferReportName: heading without a token slugifies to a .md name", () => {
  assert.strictEqual(
    RP.inferReportName("# Bug Hunt report\n\n**Finding** — text"),
    "bug-hunt-report.md");
  // trailing dash-separated dates/subtitles after an em dash are dropped
  assert.strictEqual(
    RP.inferReportName("# Performance Audit — 2026-07-09\n\nbody"),
    "performance-audit.md");
});
t("inferReportName: ALL-CAPS token in early lines works without a heading", () => {
  assert.strictEqual(
    RP.inferReportName("Findings from BUGS.md, week 3\n\n- **One** — a thing"),
    "BUGS.md");
});
t("inferReportName: lowercase .md tokens and plain prose infer nothing", () => {
  assert.strictEqual(RP.inferReportName("see readme.md for details\n\nplain text"), null);
  assert.strictEqual(RP.inferReportName("just a paragraph of prose"), null);
  assert.strictEqual(RP.inferReportName(""), null);
});

if (failures.length) {
  console.error("\n" + failures.length + " report-parser test(s) failed");
  process.exit(1);
}
console.log("\nOK  report-parser: all tests passed");
