# Technique — editorial layout (the composition system)

How to compose pages that read as printed editorial design instead of a
component stack. Companion to references/anti-slop.md (the defects this
prevents). Calibration: 1950s Fortune spreads, CBS/Olivetti/IBM annual
reports — Beall, Rand, Brodovitch.

## 1 · The page is a magazine, not a stack
- **Masthead**: double rule (3px + 1px), mono kicker row (publication ·
  issue · date-ish), the wordmark as a masthead.
- **Numbered sections**: "№ 01 · THE PROBLEM" in letterspaced mono over a
  rule — the table-of-contents grammar.
- **Folios/colophon**: a real colophon in the footer ("Set in Fraunces,
  Source Serif 4 & Space Mono · printed on #F7F2E3") — the page signs its
  work.
- **Figure captions** under every image/artifact, mono, small, letterspaced.

## 2 · Scale violence
Every screenful needs a size extreme: display numerals or initials at
72–140px against 9–11px captions. Concrete ratios: display:body ≥ 4:1,
display:caption ≥ 10:1. Drop caps on lead paragraphs
(`::first-letter{font-size:3.2em;float:left}`). Big numbers are the
cheapest editorial move there is — use the content's own numbers (145
briefs, 4 phases, 22 families).

## 3 · Asymmetry & grid breaks (at least one per section, varied)
- Split ratios from {2/3+1/3, 5/8+3/8, 3/4+1/4} — never 50/50 twice in a row.
- Pull-quotes set display-size as the section's LEFT column, body text right.
- Bleeds: a figure that crosses the section rule or exits the container.
- Rotation: stamps (-6°..-3°), a filed document (±1°), never more than two
  rotated objects per page.
- Marginalia: tiny mono notes hanging in the outer margin.
- Multi-column body text (`columns:2`) for editorial passages on wide screens.

## 4 · Content as artifact
Typeset the product's real output as the physical thing it is: a report is
a paper document (ruled, mono-headed, red margin marks, a rotated
"FILED · EVIDENCE ATTACHED" stamp); an install command is a ticket stub
(dashed rule, "ADMIT ONE"); a playbook is a programme entry. The artifact
IS the section's illustration — never describe what you can show.

## 5 · Inhabit the page
Spot illustrations (imagegen/image_lab, isolated on the paper ground) woven
through sections — a lamp in a margin, the report stack beside the proof,
the desk at the colophon. One hero-grade image per page; two to four spots;
zero text deserts (see anti-slop #6). Frame art with the ink border +
figcaption, or let spots sit borderless on the paper.

## 6 · The motif carries the layout
This brand's arcade: arch-topped featured cards
(`border-radius: 999px 999px 10px 10px` on a tall card reads as an arch),
arched section dividers, the lamp glow (--glow-lamp) on exactly one
"most popular" object. A motif used structurally twice per page beats one
used decoratively ten times.

## 7 · Process
Compose section-by-section against the content (what IS this section's one
job?), pick its device (pull-quote spread / artifact / programme table /
ticket row), then run the anti-slop checklist over the full-page
screenshot at arm's length. Two adjacent sections sharing a skeleton =
recompose one.
