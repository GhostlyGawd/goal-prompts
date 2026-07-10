#!/usr/bin/env node
/* shots — screenshot + page-health harness for the design engine.
 *
 * Boots a static server over the host repo and visits every page in
 * brand.json host.pages_to_shoot × host.themes_to_shoot.
 *
 *   node design-engine/tools/shots.cjs            # screenshots → out/shots/
 *   node design-engine/tools/shots.cjs --assert   # health mode, no pixels:
 *       page loads, zero console errors / page errors, var(--ink) resolves,
 *       document.fonts reports loaded faces, no horizontal overflow.
 *       Exit 1 on any failure — gate-grade; pixels never are.
 *   --matrix   widens either mode to {390, 768, 1280} viewports — the QA
 *       loop's full sweep (see library/techniques/qa-loop.md + qa_sheet.py).
 *
 * Needs playwright-core + a Chromium (PW_CHROMIUM or /opt/pw-browsers);
 * generate-time tool, same tier as scripts/og.py.
 */
"use strict";
const http = require("http");
const fs = require("fs");
const path = require("path");

const ENGINE = path.resolve(__dirname, "..");
const ROOT = path.dirname(ENGINE);
const OUTDIR = path.join(ENGINE, "out", "shots");
const MIME = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript",
  ".json": "application/json", ".md": "text/markdown", ".png": "image/png",
  ".svg": "image/svg+xml", ".woff2": "font/woff2", ".txt": "text/plain" };

function findChromium() {
  if (process.env.PW_CHROMIUM) return process.env.PW_CHROMIUM;
  const base = process.env.PLAYWRIGHT_BROWSERS_PATH || "/opt/pw-browsers";
  const dirs = fs.existsSync(base) ? fs.readdirSync(base) : [];
  for (const rel of ["chrome-linux/headless_shell", "chrome-linux/chrome"]) {
    for (const d of dirs) {
      const p = path.join(base, d, rel);
      if (fs.existsSync(p)) return p;
    }
  }
  return null;
}

function serve() {
  const server = http.createServer((req, res) => {
    let f = decodeURIComponent(req.url.split("?")[0]);
    if (f.startsWith("/_vercel/")) {
      // platform-injected assets (analytics) exist only on Vercel's edge;
      // stub them so the health assert judges the pages, not the host
      res.writeHead(200, { "content-type": "text/javascript" });
      res.end("/* stubbed by shots.cjs */");
      return;
    }
    if (f === "/") f = "/index.html";
    let fp = path.join(ROOT, path.normalize(f));
    if (!path.extname(fp) && fs.existsSync(fp + ".html")) fp += ".html"; // cleanUrls
    if (!fp.startsWith(ROOT) || !fs.existsSync(fp) || fs.statSync(fp).isDirectory()) {
      res.writeHead(404); res.end("not found"); return;
    }
    res.writeHead(200, { "content-type": MIME[path.extname(fp)] || "application/octet-stream" });
    fs.createReadStream(fp).pipe(res);
  });
  return new Promise(r => server.listen(0, "127.0.0.1", () => r(server)));
}

function requirePlaywright() {
  // local resolution first; then the npm global root (covers playwright-core
  // installed globally, or nested inside a global `playwright`)
  const paths = [__dirname, process.cwd()];
  try {
    const g = require("child_process").execSync("npm root -g", { encoding: "utf8" }).trim();
    paths.push(g, path.join(g, "playwright", "node_modules"));
  } catch (e) {}
  for (const name of ["playwright-core", "playwright"]) {
    try { return require(require.resolve(name, { paths })); } catch (e) {}
  }
  return null;
}

(async () => {
  const assertMode = process.argv.includes("--assert");
  const pw = requirePlaywright();
  if (!pw) {
    console.error("SKIP  playwright-core not resolvable — npm i -g playwright-core");
    process.exit(assertMode ? 1 : 0);
  }
  const { chromium } = pw;
  const brand = JSON.parse(fs.readFileSync(path.join(ENGINE, "brand.json"), "utf8"));
  const pages = brand.host.pages_to_shoot || ["/"];
  const themes = brand.host.themes_to_shoot || ["dark"];
  const key = brand.host.theme_storage_key || "theme";
  const matrix = process.argv.includes("--matrix");
  const widths = matrix ? [390, 768, 1280] : [1280];

  const server = await serve();
  const port = server.address().port;
  if (!assertMode) fs.mkdirSync(OUTDIR, { recursive: true });
  const exec = findChromium();
  const browser = await chromium.launch(exec ? { executablePath: exec } : {});
  let failures = 0;

  for (const theme of themes) {
    for (const vw of widths) {
    const ctx = await browser.newContext({
      viewport: { width: vw, height: 900 },
      deviceScaleFactor: assertMode ? 1 : 2,
      colorScheme: theme === "light" ? "light" : "dark",
    });
    await ctx.addInitScript(([k, t]) => { try { localStorage.setItem(k, t); } catch (e) {} }, [key, theme]);
    for (const p of pages) {
      const page = await ctx.newPage();
      const errors = [];
      page.on("console", m => { if (m.type() === "error") errors.push(m.text()); });
      page.on("pageerror", e => errors.push(String(e)));
      page.on("response", r => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
      const name = (p === "/" ? "home" : p.replace(/^\//, "").replace(/\.html$/, "").replace(/\//g, "-"))
        + (matrix ? `-w${vw}` : "");
      try {
        const resp = await page.goto(`http://127.0.0.1:${port}${p}`, { waitUntil: "networkidle", timeout: 30000 });
        if (!resp || !resp.ok()) throw new Error(`HTTP ${resp && resp.status()}`);
        const health = await page.evaluate(async () => {
          await document.fonts.ready;
          const ink = getComputedStyle(document.documentElement).getPropertyValue("--ink").trim();
          const loaded = [...document.fonts].filter(f => f.status === "loaded").length;
          const overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
          return { ink, loaded, overflow };
        });
        if (!health.ink) throw new Error("var(--ink) did not resolve — tokens.css missing?");
        if (health.overflow > 1) throw new Error(`horizontal overflow: content ${health.overflow}px wider than the viewport`);
        if (errors.length) throw new Error(`console errors: ${errors.join(" | ")}`);
        if (assertMode) {
          console.log(`OK  ${name} [${theme}]  --ink=${health.ink}  fonts=${health.loaded}`);
        } else {
          const out = path.join(OUTDIR, `${name}-${theme}.png`);
          await page.screenshot({ path: out, fullPage: true });
          console.log(`shot ${path.relative(ROOT, out)}`);
        }
      } catch (e) {
        failures++;
        console.error(`FAIL  ${name} [${theme}]  ${e.message}`);
      }
      await page.close();
    }
    await ctx.close();
    }
  }
  await browser.close();
  server.close();
  if (failures) { console.error(`\n${failures} page(s) failed`); process.exit(1); }
  console.log(assertMode ? "\nALL PAGES HEALTHY" : "\nall shots written");
})();
