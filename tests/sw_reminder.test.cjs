#!/usr/bin/env node
/* R34 (RETENTION R8a): the generated service worker must gate the weekly
 * Vitals notification on the IndexedDB mirror the pages write — never fire
 * blind. Loads the BUILT sw.js (run python3 build.py first; scripts/check
 * does) into a vm with a stubbed worker scope + event-shaped fake IndexedDB,
 * then exercises both the pure decision (self.gpShouldNotify) and the real
 * periodicsync handler end to end. Zero dependencies, like the other suites.
 */
"use strict";
const assert = require("assert");
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const src = fs.readFileSync(path.join(__dirname, "..", "sw.js"), "utf8");
const DAY = 86400000;

/* Build a fresh worker world around one stored mirror value. `stored` is what
 * the fake IndexedDB get("vitals") yields (undefined = no mirror written). */
function makeWorld(stored) {
  const listeners = {};
  const shown = [];
  const self = {
    addEventListener: function (type, fn) { listeners[type] = fn; },
    skipWaiting: function () {},
    location: { origin: "https://example.test" },
    registration: {
      showNotification: function (title, opts) {
        shown.push({ title: title, opts: opts });
        return Promise.resolve();
      }
    }
  };
  const indexedDB = {
    open: function () {
      const req = {};
      setImmediate(function () {
        req.result = {
          close: function () {},
          transaction: function () {
            return { objectStore: function () {
              return { get: function () {
                const g = {};
                setImmediate(function () {
                  g.result = stored;
                  if (g.onsuccess) g.onsuccess();
                });
                return g;
              } };
            } };
          }
        };
        if (req.onsuccess) req.onsuccess();
      });
      return req;
    }
  };
  const sandbox = {
    self: self, indexedDB: indexedDB, caches: {}, clients: {},
    Promise: Promise, setTimeout: setTimeout, clearTimeout: clearTimeout,
    setImmediate: setImmediate, URL: URL, console: console,
    Request: function () {}, fetch: function () { return Promise.reject(new Error("no net")); }
  };
  sandbox.globalThis = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(src, sandbox, { filename: "sw.js" });
  return { listeners: listeners, shown: shown, self: self };
}

/* Fire the periodicsync handler and wait for its waitUntil promise. */
function sync(world) {
  let p = Promise.resolve();
  world.listeners["periodicsync"]({
    tag: "vitals-weekly",
    waitUntil: function (x) { p = x; }
  });
  return p;
}

const failures = [];
function check(label, fn) {
  return Promise.resolve().then(fn).then(
    function () { console.log("  ok    " + label); },
    function (e) { console.log("  FAIL  " + label + " — " + e.message); failures.push(label); });
}

const now = Date.now();
const base = makeWorld(undefined);
const decide = base.self.gpShouldNotify;

(async function () {
  // ---- the pure decision --------------------------------------------------
  await check("no mirror at all → notify (legacy opt-in fallback)", function () {
    assert.strictEqual(decide(null, now), true);
  });
  await check("reminders mirrored off → never notify", function () {
    assert.strictEqual(decide({ remindOn: false, runs29: 0 }, now), false);
    assert.strictEqual(decide({ remindOn: false, runs29: now - 30 * DAY }, now), false);
  });
  await check("Vitals ran 1 day ago → skip", function () {
    assert.strictEqual(decide({ remindOn: true, runs29: now - 1 * DAY }, now), false);
  });
  await check("Vitals ran 6.9 days ago → still fresh, skip", function () {
    assert.strictEqual(decide({ remindOn: true, runs29: now - 6.9 * DAY }, now), false);
  });
  await check("Vitals 7+ days stale → notify", function () {
    assert.strictEqual(decide({ remindOn: true, runs29: now - 8 * DAY }, now), true);
  });
  await check("opted in but never ran Vitals (runs29 0) → notify", function () {
    assert.strictEqual(decide({ remindOn: true, runs29: 0 }, now), true);
  });

  // ---- the real handler over the fake IndexedDB ---------------------------
  await check("periodicsync + fresh mirror → no notification", async function () {
    const w = makeWorld({ remindOn: true, runs29: Date.now() - 1 * DAY });
    await sync(w);
    assert.strictEqual(w.shown.length, 0);
  });
  await check("periodicsync + reminders off → no notification", async function () {
    const w = makeWorld({ remindOn: false, runs29: Date.now() - 30 * DAY });
    await sync(w);
    assert.strictEqual(w.shown.length, 0);
  });
  await check("periodicsync + stale mirror → notifies, landing on /vitals?src=reminder", async function () {
    const w = makeWorld({ remindOn: true, runs29: Date.now() - 9 * DAY });
    await sync(w);
    assert.strictEqual(w.shown.length, 1);
    assert.strictEqual(w.shown[0].opts.data.url, "/vitals?src=reminder");
  });
  await check("periodicsync + missing mirror → notifies (never silently dead)", async function () {
    const w = makeWorld(undefined);
    await sync(w);
    assert.strictEqual(w.shown.length, 1);
  });
  await check("foreign periodicsync tag is ignored", async function () {
    const w = makeWorld(undefined);
    let waited = false;
    w.listeners["periodicsync"]({ tag: "something-else", waitUntil: function () { waited = true; } });
    assert.strictEqual(waited, false);
    assert.strictEqual(w.shown.length, 0);
  });

  if (failures.length) {
    console.error("\nsw reminder: " + failures.length + " failure(s)");
    process.exit(1);
  }
  console.log("sw reminder: all assertions passed");
})();
