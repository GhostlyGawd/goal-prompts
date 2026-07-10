#!/usr/bin/env python3
"""present — selection artifacts, down to a science. Stdlib only.

Generates a gate-ready presentation page from a JSON spec, enforcing
library/techniques/presentation-protocol.md structurally: options rendered
big and labeled, one recommendation, self-contained output, evidence in an
appendix, gate instructions using the exact labels.

    python3 design-engine/tools/present.py SPEC.json [--out FILE]

Spec shape:
{
  "title": "…", "kicker": "…", "lede": "…",
  "fonts": {"Family": {"weights": "300 900", "b64": "…"}},       # optional
  "palette": {"paper": "#…", "ink": "#…", "cobalt": "#…", "lamp": "#…",
              "card": "#…", "line": "#…", "dim": "#…", "faint": "#…"},
  "sections": [{
      "no": "№1", "title": "…", "how": "…", "sub": "…",
      "options": [{"label": "A", "name": "…", "recommended": true,
                   "html": "<the option rendered as the finished thing>",
                   "caption": "…"}]
  }],
  "gate": {"title": "…", "combo": "…", "body": "…"},
  "appendix": [{"summary": "…", "html": "…"}]
}
The option "html" is produced by the calling skill (mockups, gauntlets,
specimens — real assets per the protocol); present.py owns structure, chrome,
and the protocol's rules so no gate ever regresses to swatch lists.
"""
import html as html_mod
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import enginelib as lib  # noqa: E402

esc = html_mod.escape

DEFAULT_PALETTE = {"paper": "#F7F2E3", "paper2": "#EFE7D2", "card": "#FCFAF2",
                   "line": "#DCD2BA", "ink": "#1D1F28", "dim": "#4C4F5E",
                   "faint": "#6E7182", "cobalt": "#3355B4", "lamp": "#E8752C",
                   "bandtext": "#FBF8EE"}


def build(spec: dict) -> str:
    P = {**DEFAULT_PALETTE, **spec.get("palette", {})}
    fonts = "\n".join(
        f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{f['weights']};"
        f"font-display:swap;src:url(data:font/woff2;base64,{f['b64']}) format('woff2')}}"
        for fam, f in spec.get("fonts", {}).items())
    sections = []
    for sec in spec["sections"]:
        opts = []
        for o in sec["options"]:
            rec = '<span class="recb">RECOMMENDED</span>' if o.get("recommended") else ""
            opts.append(
                f'<div class="plate"><div class="platehead">'
                f'<span class="platenum">{esc(o["label"])}</span>'
                f'<span class="platename">{esc(o["name"])}</span>{rec}</div>'
                f'{o["html"]}'
                f'<p class="platecap">{o.get("caption", "")}</p></div>')
        sections.append(
            f'<section class="sec"><div class="sechead">'
            f'<span class="secno">{esc(sec.get("no", ""))}</span>'
            f'<h2>{esc(sec["title"])}</h2>'
            f'<span class="sechow">{sec.get("how", "")}</span></div>'
            f'<p class="secsub">{sec.get("sub", "")}</p>{"".join(opts)}</section>')
    gate = spec.get("gate", {})
    appendix = "".join(
        f'<details><summary>{esc(a["summary"])}</summary>{a["html"]}</details>'
        for a in spec.get("appendix", []))
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(spec["title"])}</title><style>
{fonts}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:{P["paper"]};color:{P["ink"]};font-family:'Source Serif 4',Georgia,serif;line-height:1.6;padding:0 22px 80px}}
.sheet{{max-width:980px;margin:0 auto}}
.rule2{{border-top:3px solid {P["ink"]};border-bottom:1px solid {P["ink"]};height:7px;margin:24px 0 0}}
.kicker{{font-family:'Space Mono',monospace;font-size:11px;letter-spacing:.16em;padding:12px 2px;text-transform:uppercase}}
h1{{font-family:'Fraunces',Georgia,serif;font-weight:700;font-size:clamp(34px,5.4vw,54px);line-height:1.03;margin:24px 0 12px}}
.lede{{font-size:17px;max-width:64ch;color:{P["dim"]}}}
.sec{{margin-top:88px}}
.sechead{{display:flex;align-items:baseline;gap:16px;border-top:3px solid {P["ink"]};padding-top:14px}}
.secno{{font-family:'Space Mono',monospace;font-weight:700;font-size:14px;color:{P["lamp"]}}}
h2{{font-family:'Fraunces',Georgia,serif;font-weight:700;font-size:28px}}
.sechow{{font-family:'Space Mono',monospace;font-size:10.5px;color:{P["faint"]};margin-left:auto;text-align:right}}
.secsub{{font-size:15px;color:{P["dim"]};max-width:66ch;margin:10px 0 20px}}
.plate{{margin:40px 0 0}}
.platehead{{display:flex;align-items:center;gap:13px;margin-bottom:12px}}
.platenum{{font-family:'Space Mono',monospace;font-weight:700;font-size:13px;color:{P["bandtext"]};background:{P["cobalt"]};border-radius:50%;width:32px;height:32px;display:inline-flex;align-items:center;justify-content:center;flex:none}}
.platename{{font-family:'Fraunces',Georgia,serif;font-weight:700;font-size:21px}}
.recb{{font-family:'Space Mono',monospace;font-size:10px;letter-spacing:.12em;color:{P["bandtext"]};background:{P["lamp"]};border-radius:3px;padding:3px 8px}}
.platecap{{font-size:14px;color:{P["dim"]};max-width:76ch;margin-top:10px}}
.gate{{background:{P["cobalt"]};color:{P["bandtext"]};border-radius:12px;padding:26px 30px;margin-top:80px;box-shadow:7px 7px 0 {P["line"]}}}
.gate h2{{color:{P["bandtext"]};margin-bottom:8px}}
.gate .combo{{font-family:'Space Mono',monospace;font-size:13px;color:#FFC684;margin:10px 0}}
details{{border:1.5px solid {P["line"]};border-radius:8px;padding:13px 17px;margin-top:36px;background:{P["card"]};font-size:13px;color:{P["dim"]}}}
summary{{cursor:pointer;font-family:'Space Mono',monospace;font-size:11px;letter-spacing:.05em}}
.foot{{font-family:'Space Mono',monospace;font-size:10.5px;color:{P["faint"]};margin-top:52px;letter-spacing:.04em}}
</style></head><body><div class="sheet">
<div class="rule2"></div>
<div class="kicker">{esc(spec.get("kicker", ""))}</div>
<h1>{spec["title"]}</h1>
<p class="lede">{spec.get("lede", "")}</p>
{"".join(sections)}
<div class="gate"><h2>{esc(gate.get("title", "The gate"))}</h2>
<p class="combo">{esc(gate.get("combo", ""))}</p><p>{gate.get("body", "")}</p></div>
{appendix}
<p class="foot">design engine · present.py · presentation-protocol enforced · self-contained</p>
</div></body></html>'''


def main(argv):
    args = list(argv)
    if not args:
        print(__doc__, file=sys.stderr)
        return 2
    spec = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    out = Path(args[args.index("--out") + 1]) if "--out" in args else lib.OUT_DIR / "presentation.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(spec), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
