#!/usr/bin/env node
/* motion_preview — motion & video capability. Generate-time (playwright-core).
 *
 * Loads an HTML motion prototype (any local file/URL) and produces reviewable
 * motion artifacts:
 *   - a WEBM video of the page for `--seconds N` (default 4)
 *   - a frame strip: PNG frames at even intervals (default 8) laid side by
 *     side into one strip image reviewable without a video player
 *
 *   node design-engine/tools/motion_preview.cjs FILE_OR_URL \
 *        [--seconds 4] [--frames 8] [--width 900] [--height 600] \
 *        [--out design-engine/out/motion]
 *
 * Interactions can be scripted via --click "selector" (fires after load, so
 * hover/press transitions can be captured). Videos/frames are for judging
 * motion at gates — never pixel-gated.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const cp = require("child_process");

const ENGINE = path.resolve(__dirname, "..");

function requirePlaywright() {
  const paths = [__dirname, process.cwd()];
  try {
    const g = cp.execSync("npm root -g", { encoding: "utf8" }).trim();
    paths.push(g, path.join(g, "playwright", "node_modules"));
  } catch (e) {}
  for (const name of ["playwright-core", "playwright"]) {
    try { return require(require.resolve(name, { paths })); } catch (e) {}
  }
  return null;
}

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

function opt(name, dflt) {
  const i = process.argv.indexOf(name);
  return i > -1 ? process.argv[i + 1] : dflt;
}

(async () => {
  const target = process.argv[2];
  if (!target) { console.error("usage: motion_preview.cjs FILE_OR_URL [options]"); process.exit(2); }
  const pw = requirePlaywright();
  if (!pw) { console.error("SKIP  playwright-core not resolvable"); process.exit(1); }
  const seconds = parseFloat(opt("--seconds", "4"));
  const nFrames = parseInt(opt("--frames", "8"), 10);
  const width = parseInt(opt("--width", "900"), 10);
  const height = parseInt(opt("--height", "600"), 10);
  const outDir = path.resolve(opt("--out", path.join(ENGINE, "out", "motion")));
  const click = opt("--click", null);
  fs.mkdirSync(outDir, { recursive: true });

  const url = /^https?:/.test(target) ? target : "file://" + path.resolve(target);
  const exec = findChromium();
  const browser = await pw.chromium.launch(exec ? { executablePath: exec } : {});
  const ctx = await browser.newContext({
    viewport: { width, height },
    recordVideo: { dir: outDir, size: { width, height } },
  });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: "networkidle" });
  if (click) await page.click(click).catch(e => console.error("click failed:", e.message));

  const frames = [];
  const step = (seconds * 1000) / Math.max(1, nFrames - 1);
  for (let i = 0; i < nFrames; i++) {
    const fp = path.join(outDir, `frame-${String(i).padStart(2, "0")}.png`);
    await page.screenshot({ path: fp });
    frames.push(fp);
    if (i < nFrames - 1) await page.waitForTimeout(step);
  }
  await page.close();
  const video = await ctx.pages().length; // ensure context flushes
  await ctx.close();
  await browser.close();

  // name the video deterministically
  const vids = fs.readdirSync(outDir).filter(f => f.endsWith(".webm"));
  if (vids.length) {
    const latest = vids.map(f => path.join(outDir, f))
      .sort((a, b) => fs.statSync(b).mtimeMs - fs.statSync(a).mtimeMs)[0];
    const dest = path.join(outDir, "motion.webm");
    if (latest !== dest) fs.renameSync(latest, dest);
    console.log("video", path.relative(process.cwd(), dest));
  }
  console.log(`frames ${frames.length} → ${path.relative(process.cwd(), outDir)}`);
})();
