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

/* mtext is the fence-masked twin of text: signals (severity, status, chips)
 * are read from it so fenced sample lines can't grade or resolve a finding,
 * while text — and therefore the localStorage key — keeps the original bytes. */
function mkFinding(report, section, rawTitle, text, mtext) {
  if (mtext == null) mtext = text;
  var title = firstWords(rawTitle.replace(/^\d+\.\s*/, ""));
  var em = mtext.match(/effort\s*[:·—-]?\s*([SML])\b/i);
  var im = mtext.match(/impact\s*[:·—-]?\s*([LMH])\b/i);
  var tag = (rawTitle.match(/^(NEW|FIX|IMPROVE)\b/) || [])[1] || null;
  var key = "f" + hash(report + "|" + title + "|" + text.slice(0, 120));
  return { key: key, report: report, section: section, title: title, text: text,
           sev: sevOf(mtext), fixed: isFixed(mtext), effort: em ? em[1].toUpperCase() : null,
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
  /* code-fence pre-pass: every line inside a ``` fence is masked to one inert
   * glyph in a parallel copy. All STRUCTURE (sections, block splits, finding
   * shapes) and all SIGNALS (severity, status) read the masked lines, so a
   * fenced "### heading" can't mint a finding and a fenced "Severity: S1"
   * can't grade one — while bodies keep the original fence text verbatim.
   * Masking blank fence lines too keeps a whole fence inside one block. */
  var masked = lines.slice();
  var inFence = false;
  for (var fi = 0; fi < lines.length; fi++) {
    if (/^\s*```/.test(lines[fi])) inFence = !inFence;
    else if (inFence) masked[fi] = "░";
  }
  var sections = [];
  var cur = { title: "", o: [], m: [] };
  for (var li = 0; li < lines.length; li++) {
    var mh = masked[li].match(/^##\s+(.+)/);
    if (mh && !/^###/.test(masked[li])) { sections.push(cur); cur = { title: mh[1].trim(), o: [], m: [] }; }
    else { cur.o.push(lines[li]); cur.m.push(masked[li]); }
  }
  sections.push(cur);
  for (var si = 0; si < sections.length; si++) {
    var s = sections[si];
    /* block-split on the masked lines; each block keeps its original lines so
     * bodies (and the localStorage key hashes) stay byte-identical */
    var blocks = [];
    var bo = [], bm = [];
    for (var gi = 0; gi <= s.m.length; gi++) {
      if (gi === s.m.length || !s.m[gi].trim()) {
        if (bm.length) blocks.push({ o: bo.join("\n").trim(), m: bm.join("\n").trim(), ol: bo });
        bo = []; bm = [];
      } else { bo.push(s.o[gi]); bm.push(s.m[gi]); }
    }
    for (var bi = 0; bi < blocks.length; bi++) {
      var b = blocks[bi];
      var hm = b.m.match(/^#{3,}\s+(\S[^\n]*)([\s\S]*)$/);
      if (hm) {
        /* a ###/#### finding: the heading titles it; heading-free blocks that
         * follow (evidence paragraphs, small bullets) fold into its body */
        var chunk = [b.o], mchunk = [b.m];
        while (bi + 1 < blocks.length && !/^#/.test(blocks[bi + 1].m) &&
               !findingShaped(blocks[bi + 1].m)) {
          bi++;
          chunk.push(blocks[bi].o); mchunk.push(blocks[bi].m);
        }
        var body = chunk.join("\n\n");
        if (body.length >= 30) out.push(mkFinding(name, s.title, hm[1].trim(), body, mchunk.join("\n\n")));
        else skipped++;              // a titled stub is still content — keep "M unrecognized" honest
        continue;
      }
      if (/^#/.test(b.m)) continue;                     // stray/degenerate headings
      var bold = b.m.match(/^\*\*(.+?)\*\*/);
      if (bold) { out.push(mkFinding(name, s.title, bold[1], b.o, b.m)); continue; }
      if (/^(\d+\.|[-*])\s/.test(b.m)) {
        var mItems = b.m.split(/\n(?=(?:\d+\.|[-*])\s)/);
        var plain = b.o === b.m;                        // no fence in this block
        var pos = 0;
        for (var ii = 0; ii < mItems.length; ii++) {
          var mIt = mItems[ii].trim();
          var n = mItems[ii].split("\n").length;
          var it = plain ? mIt : b.ol.slice(pos, pos + n).join("\n").trim();
          pos += n;
          var t = mIt.replace(/^(\d+\.|[-*])\s*/, "");
          if (t.length < 30 && !t.includes("**")) continue;   // nav / trivia lines
          var bm2 = t.match(/^\*\*(.+?)\*\*/);
          out.push(mkFinding(name, s.title, bm2 ? bm2[1] : t, it, mIt));
        }
        continue;
      }
      /* plain prose blocks (summaries, sign-offs) are context, not findings —
       * but count the substantive ones so the Studio can say "M unrecognized" */
      if (b.o.length >= 40) skipped++;
    }
  }
  return { findings: out, skipped: skipped };
}

/* inferReportName — the Studio's paste box uses this so an unnamed paste
 * lands under the report's own name instead of the shared "pasted.md"
 * default (FORMS FV1: two unnamed pastes silently overwrote each other).
 * Reads, in order: an ALL-CAPS *.md token in the first `#` heading, the
 * heading text slugified, or an ALL-CAPS *.md token in the first lines.
 * Returns null when nothing name-shaped is found — callers keep their own
 * fallback (and any uniqueness suffixing). */
var CAPS_MD = /\b([A-Z][A-Z0-9_-]*\.md)\b/;
function inferReportName(text) {
  var lines = String(text || "").replace(/\r\n?/g, "\n").split("\n");
  var top = lines.slice(0, 40);
  for (var i = 0; i < top.length; i++) {
    var h = top[i].match(/^#\s+(.+)/);
    if (!h) continue;
    var tok = h[1].match(CAPS_MD);
    if (tok) return tok[1];
    /* slugify the heading; an em/en-dash subtitle ("— 2026-07-09") drops */
    var slug = h[1].split(/[—–:·|]/)[0].replace(/[*_`~#>\[\]()]/g, "")
      .trim().toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
    return slug ? slug.slice(0, 48).replace(/-+$/, "") + ".md" : null;
  }
  for (var j = 0; j < top.length; j++) {
    var t2 = top[j].match(CAPS_MD);
    if (t2) return t2[1];
  }
  return null;
}

var GPReportParser = {
  hash: hash,
  firstWords: firstWords,
  mkFinding: mkFinding,
  parseReport: parseReport,
  inferReportName: inferReportName
};
if (typeof module !== "undefined" && module.exports) module.exports = GPReportParser;
global.GPReportParser = GPReportParser;
})(typeof window !== "undefined" ? window : globalThis);
