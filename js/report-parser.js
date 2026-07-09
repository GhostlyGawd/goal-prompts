/* report-parser.js — the Report Studio's markdown-report parser, factored out
 * of studio.html so Node can test it (tests/report_parser.test.cjs). Loaded by
 * studio.html via <script src="/js/report-parser.js">; pure functions only, no
 * DOM. Finding keys are content hashes persisted in localStorage
 * (gp-studio-checks) — the key scheme for bold-led and list-item findings is
 * pinned by the tests and must never change. ###/#### findings are new keys
 * (those blocks used to be dropped entirely), so nobody's saved checks move. */
(function (global) {
"use strict";

function hash(s) { var h = 5381; for (var i = 0; i < s.length; i++) { h = ((h << 5) + h + s.charCodeAt(i)) >>> 0; } return h.toString(36); }
function firstWords(t) {
  var clean = t.replace(/[*_`>#]/g, "").replace(/\s+/g, " ").trim();
  return clean.length > 88 ? clean.slice(0, 85).trimEnd() + "…" : clean;
}

/* severity words count only where they are labels, never as prose: the
 * finding's first (title) line, or an explicit "Severity: …" line. The (?!-)
 * guard keeps "high-traffic" / "low-hanging" from reading as grades. */
function gradeSev(s) {
  if (/\bS1\b/i.test(s) || /\bcritical\b(?!-)/i.test(s)) return "S1";
  if (/\bS2\b/i.test(s) || /\bhigh\b(?!-)/i.test(s))     return "S2";
  if (/\bS3\b/i.test(s) || /\bmedium\b(?!-)/i.test(s))   return "S3";
  if (/\blow\b(?!-)/i.test(s))                           return "Low";
  return null;
}
function sevOf(text) {
  var label = text.match(/(?:^|\n)[\s>*-]*(?:\*\*)?severity(?:\*\*)?\s*[:·—-]\s*([^\n]*)/i);
  if (label) return gradeSev(label[1]);
  return gradeSev(text.split("\n", 1)[0]);
}

/* "fixed"/"shipped" mark done only from a status position: an uppercase
 * FIXED/SHIPPED shout in the title line (the BUGS.md house style), a checked
 * checkbox, a "Status: …" line, or a line that opens with the word — never
 * from a mid-sentence prose mention. */
function isFixed(text) {
  var lines = text.split("\n");
  if (/\b(FIXED|SHIPPED|RESOLVED)\b/.test(lines[0] || "")) return true;
  for (var i = 0; i < lines.length; i++) {
    var ln = lines[i];
    if (/^\s*(?:[-*]\s+)?\[[xX]\]/.test(ln)) return true;
    if (/^\s*(?:[->*]\s+)?(?:\*\*)?(?:status|state)(?:\*\*)?\s*[:·—-]/i.test(ln) &&
        /\b(?:fixed|shipped|done|resolved|closed)\b/i.test(ln)) return true;
    if (/^\s*(?:[->*]\s+)?(?:\*\*)?(?:fixed|shipped)\b/i.test(ln)) return true;
  }
  return false;
}

function mkFinding(report, section, rawTitle, text) {
  var title = firstWords(rawTitle.replace(/^\d+\.\s*/, ""));
  var em = text.match(/effort\s*[:·—-]?\s*([SML])\b/i);
  var im = text.match(/impact\s*[:·—-]?\s*([LMH])\b/i);
  var tag = (rawTitle.match(/^(NEW|FIX|IMPROVE)\b/) || [])[1] || null;
  var key = "f" + hash(report + "|" + title + "|" + text.slice(0, 120));
  return { key: key, report: report, section: section, title: title, text: text,
           sev: sevOf(text), fixed: isFixed(text), effort: em ? em[1].toUpperCase() : null,
           impact: im ? im[1].toUpperCase() : null, tag: tag };
}

/* Would this block have parsed as finding(s) on its own? Used to stop a
 * ###-finding's body from swallowing a sibling bold-led or list finding —
 * every shape that parsed before ### support still parses identically. */
function findingShaped(b) {
  if (/^\*\*(.+?)\*\*/.test(b)) return true;
  if (/^(\d+\.|[-*])\s/.test(b)) {
    var items = b.split(/\n(?=(?:\d+\.|[-*])\s)/);
    for (var i = 0; i < items.length; i++) {
      var t = items[i].trim().replace(/^(\d+\.|[-*])\s*/, "");
      if (t.length >= 30 || t.includes("**")) return true;
    }
  }
  return false;
}

function parseReport(name, text) {
  var out = [];
  var skipped = 0;
  var lines = String(text).replace(/\r\n?/g, "\n").split("\n");
  var sections = [];
  var cur = { title: "", lines: [] };
  for (var li = 0; li < lines.length; li++) {
    var ln = lines[li];
    var m = ln.match(/^##\s+(.+)/);
    if (m && !/^###/.test(ln)) { sections.push(cur); cur = { title: m[1].trim(), lines: [] }; }
    else cur.lines.push(ln);
  }
  sections.push(cur);
  for (var si = 0; si < sections.length; si++) {
    var s = sections[si];
    var blocks = s.lines.join("\n").split(/\n\s*\n/).map(function (b) { return b.trim(); }).filter(Boolean);
    for (var bi = 0; bi < blocks.length; bi++) {
      var b = blocks[bi];
      var hm = b.match(/^#{3,}\s+(\S[^\n]*)([\s\S]*)$/);
      if (hm) {
        /* a ###/#### finding: the heading titles it; heading-free blocks that
         * follow (evidence paragraphs, small bullets) fold into its body */
        var chunk = [b];
        while (bi + 1 < blocks.length && !/^#/.test(blocks[bi + 1]) &&
               !findingShaped(blocks[bi + 1])) {
          chunk.push(blocks[++bi]);
        }
        var body = chunk.join("\n\n");
        if (body.length >= 30) out.push(mkFinding(name, s.title, hm[1].trim(), body));
        continue;
      }
      if (/^#/.test(b)) continue;                       // stray/degenerate headings
      var bold = b.match(/^\*\*(.+?)\*\*/);
      if (bold) { out.push(mkFinding(name, s.title, bold[1], b)); continue; }
      if (/^(\d+\.|[-*])\s/.test(b)) {
        var items = b.split(/\n(?=(?:\d+\.|[-*])\s)/);
        for (var ii = 0; ii < items.length; ii++) {
          var it = items[ii].trim();
          var t = it.replace(/^(\d+\.|[-*])\s*/, "");
          if (t.length < 30 && !t.includes("**")) continue;   // nav / trivia lines
          var bm = t.match(/^\*\*(.+?)\*\*/);
          out.push(mkFinding(name, s.title, bm ? bm[1] : t, it));
        }
        continue;
      }
      /* plain prose blocks (summaries, sign-offs) are context, not findings —
       * but count the substantive ones so the Studio can say "M unrecognized" */
      if (b.length >= 40) skipped++;
    }
  }
  return { findings: out, skipped: skipped };
}

var GPReportParser = {
  hash: hash,
  firstWords: firstWords,
  mkFinding: mkFinding,
  parseReport: parseReport
};
if (typeof module !== "undefined" && module.exports) module.exports = GPReportParser;
global.GPReportParser = GPReportParser;
})(typeof window !== "undefined" ? window : globalThis);
