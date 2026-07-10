#!/usr/bin/env node
/* Render the site's key surfaces to PNGs so design work is done with eyes.
 *
 * This is the render-in-the-loop tool ADR-12 requires: any change that
 * touches CSS, tokens, or marketing markup must be screenshotted and LOOKED
 * AT (light + dark + mobile) before it is committed. build.py lints text and
 * scripts/check parses JS — neither ever sees a pixel, which is how
 * sub-perceptual "redesigns" used to ship.
 *
 *     python3 build.py                 # refresh index.html first
 *     node scripts/design-shot.cjs     # writes .shots/*.png (gitignored)
 *
 * Needs the global playwright (or playwright-core) package and a Chromium —
 * same toolchain as scripts/studio-shot.cjs. Point PW_CHROMIUM at a binary
 * if autodetection fails. */
"use strict";
const http = require("http");
const fs = require("fs");
const path = require("path");
let chromium;
try { ({ chromium } = require("playwright")); }
catch { ({ chromium } = require("playwright-core")); }

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, ".shots");
const MIME = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript",
  ".json": "application/json", ".md": "text/markdown", ".png": "image/png",
  ".svg": "image/svg+xml", ".woff2": "font/woff2", ".txt": "text/plain" };

function findChromium() {
  if (process.env.PW_CHROMIUM) return process.env.PW_CHROMIUM;
  const roots = [process.env.PLAYWRIGHT_BROWSERS_PATH, "/opt/pw-browsers"].filter(Boolean);
  for (const r of roots) {
    if (!fs.existsSync(r)) continue;
    for (const d of fs.readdirSync(r)) {
      for (const rel of ["chrome-linux/chrome", "chrome-linux/headless_shell"]) {
        const p = path.join(r, d, rel);
        if (fs.existsSync(p)) return p;
      }
    }
  }
  return undefined; // let playwright resolve its own
}

function serve() {
  return new Promise(resolve => {
    const srv = http.createServer((req, res) => {
      let p = decodeURIComponent(req.url.split("?")[0]);
      if (p.endsWith("/")) p += "index.html";
      const file = path.join(ROOT, p);
      if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
        res.writeHead(404); res.end(); return;
      }
      res.writeHead(200, { "content-type": MIME[path.extname(file)] || "application/octet-stream" });
      fs.createReadStream(file).pipe(res);
    });
    srv.listen(0, "127.0.0.1", () => resolve(srv));
  });
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const srv = await serve();
  const base = `http://127.0.0.1:${srv.address().port}`;
  const browser = await chromium.launch({ executablePath: findChromium() });

  const shots = [
    ["landing", "/index.html"],
    ["detail", "/b/01.html"],
    ["studio", "/studio.html"],
  ];
  for (const [name, url] of shots) {
    for (const [theme, suffix] of [["light", "light"], ["dark", "dark"]]) {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(base + url);
      await page.evaluate(t => document.documentElement.setAttribute("data-theme", t), theme);
      await page.waitForTimeout(700);
      await page.screenshot({ path: path.join(OUT, `${name}-${suffix}.png`) });
      if (name === "landing") {
        await page.screenshot({ path: path.join(OUT, `${name}-${suffix}-full.png`), fullPage: true });
      }
      await page.close();
    }
  }
  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await mobile.goto(base + "/index.html");
  await mobile.waitForTimeout(700);
  await mobile.screenshot({ path: path.join(OUT, "landing-mobile.png"), fullPage: true });
  await mobile.close();

  await browser.close();
  srv.close();
  console.log(`wrote ${fs.readdirSync(OUT).length} shots to .shots/ — now LOOK at them`);
})();
