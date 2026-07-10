# Technique — presentation protocol (selection science)

How the engine presents options at gates. Learned the hard way; now law.
`tools/present.py` generates artifacts in this shape from a spec.

1. **Options are shown as the finished thing** — a palette is a full page
   wearing it; a mark is an app icon, favicon, nav lockup, real 16px browser
   tab, and one-color version; a typeface is the real headline at display
   size. Never swatch grids or name lists alone.
2. **Self-contained files** — fonts as data-URI woff2, images as data-URI
   JPEG. Sandboxed viewers load nothing external; a fallback font silently
   shown is a lie about the design.
3. **Big, few, labeled** — one option per screenful; every option carries a
   stable label (A/B/C, V1–V6, T1–T3); the gate question uses EXACTLY those
   labels.
4. **One recommendation, visible** — the page itself wears the recommended
   package; the recommendation is argued in one sentence, not asserted.
5. **Evidence in appendices** — contrast tables, methodology, collision
   research go in <details> at the end. The main flow is for looking.
6. **The artifact demonstrates the brand it proposes** — chrome, type, and
   color of the presentation ARE the current best proposal (dogfood).
7. **Failed options shown honestly** — crossed out with the number that
   killed them (a failing ratio, a fatal collision). Rigor is part of the
   show.
8. **Gates repeat until right** — "better, but iterate again" is a first-class
   outcome; never advance on a lukewarm approval.
