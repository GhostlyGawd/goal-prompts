#!/usr/bin/env python3
"""specimen — render brand.json as a reviewable specimen page. Stdlib only.

Writes design-engine/out/specimen.html: the identity, every palette role with
live contrast ratios, the categorical spectrum in every theme, the type ramp
in the real fonts, spacing/radii scales, motion tokens with hover demos, and
the mark at nav/favicon/app-icon sizes. This is the artifact every design
gate reviews — iterate on brand.json, re-run this, look.

    python3 design-engine/tools/specimen.py [--brand path] [--out file]

The page consumes the same compiled tokens as the site (tokens_build), with
font URLs rewritten relative to the output file so it works from file://.
"""
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import enginelib as lib
import tokens_build
import mark_render

esc = html.escape


def _swatches(brand, theme):
    roles = lib.theme_roles(brand, theme)
    cfg = brand["contrast"]
    surfaces = {s: lib.resolve_role(roles, s) for s in cfg["surfaces"]}
    ink = surfaces[cfg["surfaces"][0]]
    rows = []
    for group_name, group in brand["palette"]["themes"][theme].items():
        cells = []
        for name in group:
            v = lib.resolve_role(roles, name)
            r = lib.ratio(v, ink)
            cells.append(
                f'<div class="sw"><div class="chip" style="background:{v}"></div>'
                f'<code>--{name}</code><span>{v}</span>'
                f'<span class="ratio">{r:.2f}:1 on ink</span></div>')
        rows.append(f'<div class="swgroup"><h4>{esc(group_name)}</h4>{"".join(cells)}</div>')
    return "".join(rows)


def _categorical(brand, theme):
    pal = brand["palette"]
    default = pal["default_theme"]
    mix = pal.get("categorical_mix", {}).get(theme)
    cells = []
    for fam, hexv in pal["categorical"].items():
        if theme == default or not mix:
            css = hexv
        else:
            css = f"color-mix(in srgb,{hexv} {mix['percent']}%,{mix['toward']})"
        cells.append(f'<div class="cat"><div class="bar" style="background:{css}"></div>'
                     f'<span>{esc(fam)}</span></div>')
    return "".join(cells)


def build_specimen(brand) -> str:
    css = tokens_build.compile_css(brand)
    # make @font-face urls relative to design-engine/out/ so file:// works
    css = css.replace(f"url({brand['host']['fonts_url']}",
                      f"url(../../{brand['host']['fonts_dir']}/")
    ident = brand["identity"]
    mark = brand["mark"]
    motion = brand["motion"]
    themes = list(brand["palette"]["themes"])

    theme_sections = "".join(
        f'<section class="theme" data-theme="{t}"><h2>{t} theme</h2>'
        f'<div class="board">{_swatches(brand, t)}</div>'
        f'<h3>categorical — {len(brand["palette"]["categorical"])} hues</h3>'
        f'<div class="cats">{_categorical(brand, t)}</div></section>'
        for t in themes)

    dur = "".join(f'<div class="tok"><code>--dur-{k}</code><span>{v}</span>'
                  f'<div class="demo" style="transition:transform {v} '
                  f'{motion["easings"].get("standard") or motion["easings"].get("default") or next(iter(motion["easings"].values()))}"></div></div>'
                  for k, v in motion["durations"].items())
    ease = "".join(f'<div class="tok"><code>--ease-{k}</code><span>{esc(v)}</span></div>'
                   for k, v in motion["easings"].items())
    space = "".join(f'<div class="sp"><code>--{k}</code>'
                    f'<div class="bar" style="width:{v}"></div><span>{v}</span></div>'
                    for k, v in brand["space"]["scale"].items())
    radii = "".join(f'<div class="rd"><div class="box" style="border-radius:{v}"></div>'
                    f'<code>--{k}</code><span>{v}</span></div>'
                    for k, v in brand["radii"].items())
    faces = "".join(
        f'<div class="face"><h4>{esc(f["family"])} <small>({f["role"]}, {esc(f["license"])})</small></h4>'
        f'<p style="font-family:\'{f["css_name"]}\';font-size:28px">'
        f'The quick brown fox jumps over the lazy dog 0123456789</p></div>'
        for f in brand["type"]["faces"])

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(ident['product_name'])} — brand specimen v{brand['meta']['brand_version']}</title>
<style>{css}</style>
<style>
body{{margin:0;background:var(--ink);color:var(--body);font-family:var(--sans);padding:48px;max-width:1100px;margin:0 auto}}
h1{{font-family:var(--disp);color:var(--text);letter-spacing:-.02em;font-size:40px;margin:0 0 4px}}
h2{{font-family:var(--disp);color:var(--text);margin:48px 0 16px;border-top:1px solid var(--line);padding-top:32px}}
h3{{font-family:var(--mono);color:var(--dim);font-size:13px;text-transform:uppercase;letter-spacing:.12em;margin:24px 0 12px}}
h4{{font-family:var(--mono);color:var(--faint);font-size:12px;text-transform:uppercase;letter-spacing:.1em;margin:16px 0 8px}}
.tagline{{color:var(--dim);font-size:17px}}.mono{{font-family:var(--mono);font-size:13px;color:var(--faint)}}
.board{{display:flex;flex-direction:column;gap:8px}}
.swgroup{{display:flex;gap:10px;flex-wrap:wrap;align-items:flex-start}}
.swgroup h4{{width:90px;flex:none;margin:8px 0}}
.sw{{background:var(--panel);border:1px solid var(--line);border-radius:var(--r-sm);padding:10px;width:132px;font-size:12px;display:flex;flex-direction:column;gap:3px}}
.sw .chip{{height:36px;border-radius:6px;border:1px solid var(--line-2)}}
.sw code{{color:var(--text)}}.sw .ratio{{color:var(--faint)}}
.cats{{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:8px}}
.cat{{font-family:var(--mono);font-size:11px;color:var(--dim)}}
.cat .bar{{height:26px;border-radius:5px;margin-bottom:4px}}
section.theme[data-theme]{{background:var(--ink);border:1px solid var(--line);border-radius:var(--r-md);padding:24px;margin:16px 0;color-scheme:inherit}}
.marks{{display:flex;gap:32px;align-items:flex-end;flex-wrap:wrap}}
.marks figure{{margin:0;text-align:center}}.marks figcaption{{font-family:var(--mono);font-size:11px;color:var(--faint);margin-top:8px}}
.tokrow{{display:flex;gap:12px;flex-wrap:wrap}}
.tok{{background:var(--panel);border:1px solid var(--line);border-radius:var(--r-sm);padding:12px;font-size:12px;min-width:160px}}
.tok code{{color:var(--text);display:block}}.tok span{{color:var(--faint)}}
.tok .demo{{width:28px;height:28px;background:var(--amber);border-radius:6px;margin-top:8px}}
.tok:hover .demo{{transform:translateX(96px)}}
.sp,.rd{{display:flex;align-items:center;gap:12px;font-size:12px;margin:6px 0}}
.sp code,.rd code{{width:90px;color:var(--text)}}
.sp .bar{{height:14px;background:var(--fc);border-radius:3px}}
.rd .box{{width:56px;height:36px;background:var(--panel-2);border:1px solid var(--line-3)}}
.sp span,.rd span{{color:var(--faint)}}
.voice li{{margin:6px 0}}.face p{{color:var(--text);margin:4px 0 16px}}
</style></head><body>
<header style="display:flex;gap:16px;align-items:center">
{mark_render.svg(mark, size=48)}
<div><h1>{esc(ident['product_name'])}</h1>
<p class="tagline">{esc(ident['tagline'])}</p>
<p class="mono">brand.json v{brand['meta']['brand_version']} · {esc(brand['meta'].get('note', ''))}</p></div>
</header>

<h2>Mark</h2>
<div class="marks">
<figure>{mark_render.svg(mark, size=24)}<figcaption>nav · 24px</figcaption></figure>
<figure><img src="{mark_render.favicon_data_uri(mark)}" width="64" height="64" alt=""><figcaption>favicon · 64px</figcaption></figure>
<figure><img src="{mark_render.favicon_data_uri(mark)}" width="128" height="128" alt=""><figcaption>app icon · 128px</figcaption></figure>
</div>

<h2>Palette</h2>
{theme_sections}

<h2>Type</h2>
{faces}
<h3>stacks</h3>
{"".join(f'<p class="mono">--{k}: {esc(v)}</p>' for k, v in brand["type"]["stacks"].items())}

<h2>Space</h2>
{space}
<h2>Radii</h2>
{radii}

<h2>Motion <small class="mono">(hover a duration card)</small></h2>
<div class="tokrow">{dur}</div>
<h3>easings</h3>
<div class="tokrow">{ease}</div>
<p class="mono">reduced-motion policy: {esc(motion['reduced_motion'])}</p>

<h2>Voice</h2>
<p>{esc(ident['voice']['tone'])}</p>
<ul class="voice">{"".join(f"<li>{esc(p)}</li>" for p in ident['voice']['principles'])}</ul>
<p class="mono">banned: {esc(", ".join(ident['voice'].get('banned_words', [])))}</p>
<p class="mono">signatures: {esc(" · ".join(ident.get('signatures', [])))}</p>
</body></html>
"""


def main(argv):
    brand_arg, out = None, None
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--brand":
            brand_arg = args.pop(0)
        elif a == "--out":
            out = Path(args.pop(0))
        else:
            print(f"unknown arg: {a}", file=sys.stderr)
            return 2
    brand = lib.load_brand(brand_arg)
    out = out or lib.OUT_DIR / "specimen.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_specimen(brand), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
