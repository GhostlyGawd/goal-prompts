#!/usr/bin/env node
/* Capture img/studio.png — a real screenshot of the Report Studio mid-use, for
 * the landing "Act on what you find" proof card (SHOWCASE F2).
 *
 * This is a generate-time tool (like scripts/og.py), NOT part of the stdlib
 * build or scripts/check: a screenshot can't be pixel-gated across browser
 * versions. Re-run it when the Studio UI changes so the committed asset does
 * not drift:
 *
 *     npm i -g playwright-core           # or run where playwright-core resolves
 *     node scripts/studio-shot.cjs       # writes img/studio.png
 *
 * It boots a tiny static server over the repo, loads /studio.html, clicks the
 * "try it on this repo's own reports" demo (which loads the real root reports),
 * checks the first few findings, and shoots the checklist + the Fixer bar.
 * Point PW_CHROMIUM at a Chromium/headless-shell binary if autodetection fails. */
"use strict";
const http = require("http");
const fs = require("fs");
const path = require("path");
function requirePlaywright() {
  const paths = [__dirname, process.cwd()];
  try {
    const g = require("child_process").execSync("npm root -g", { encoding: "utf8" }).trim();
    paths.push(g, require("path").join(g, "playwright", "node_modules"));
  } catch (e) {}
  for (const name of ["playwright-core", "playwright"]) {
    try { return require(require.resolve(name, { paths })); } catch (e) {}
  }
  console.error("SKIP  playwright-core not resolvable — npm i -g playwright-core");
  process.exit(0);
}
const { chromium } = requirePlaywright();

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "img", "studio.png");
const MIME = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript",
  ".json": "application/json", ".md": "text/markdown", ".png": "image/png",
  ".svg": "image/svg+xml", ".woff2": "font/woff2", ".txt": "text/plain" };

function findChromium() {
  if (process.env.PW_CHROMIUM) return process.env.PW_CHROMIUM;
  const base = process.env.PLAYWRIGHT_BROWSERS_PATH || "/opt/pw-browsers";
  const dirs = fs.existsSync(base) ? fs.readdirSync(base) : [];
  // Prefer the headless shell everywhere first (the modern chrome binary has
  // dropped the old headless mode playwright-core reaches for), then chrome.
  for (const rel of ["chrome-linux/headless_shell", "chrome-linux/chrome"]) {
    for (const d of dirs) {
      const p = path.join(base, d, rel);
      if (fs.existsSync(p)) return p;
    }
  }
  return null; // let playwright try its own default
}

const server = http.createServer((req, res) => {
  let f = decodeURIComponent(req.url.split("?")[0]);
  if (f === "/") f = "/index.html";
  const fp = path.join(ROOT, path.normalize(f));
  if (!fp.startsWith(ROOT) || !fs.existsSync(fp) || fs.statSync(fp).isDirectory()) {
    res.writeHead(404); res.end("not found"); return;
  }
  res.writeHead(200, { "content-type": MIME[path.extname(fp)] || "application/octet-stream" });
  fs.createReadStream(fp).pipe(res);
});

(async () => {
  await new Promise(r => server.listen(0, "127.0.0.1", r));
  const port = server.address().port;
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  const exec = findChromium();
  const browser = await chromium.launch(exec ? { executablePath: exec } : {});
  // colorScheme pinned: tokens.css now follows the OS, and the landing's proof
  // card expects the house dark ink, not whatever the headless default is
  const page = await browser.newPage({ viewport: { width: 1280, height: 1000 },
                                       deviceScaleFactor: 2, colorScheme: "dark" });
  await page.goto(`http://127.0.0.1:${port}/studio.html`, { waitUntil: "networkidle" });
  await page.click("#demobtn");
  // the hidden "view raw" rows share .find — wait for and tick visible rows only
  await page.waitForSelector(".find:visible", { timeout: 15000 });
  const cbs = page.locator(".find:visible input[type=checkbox]");
  const n = await cbs.count();
  for (let i = 0; i < Math.min(3, n); i++) await cbs.nth(i).check();
  // shoot from the top: h1 + loader + report chips + checklist + the Fixer bar
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(400);
  await page.screenshot({ path: OUT });
  await browser.close();
  server.close();
  console.log(`wrote ${path.relative(ROOT, OUT)} (${n} findings from the demo reports)`);
})().catch(e => { console.error("studio-shot failed:", e.message); server.close(); process.exit(1); });
