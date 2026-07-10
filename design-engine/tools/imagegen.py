#!/usr/bin/env python3
"""imagegen — new raster imagery for the engine. Generate-time; needs an API key.

Procedural vectors have a hard quality ceiling ("stick figures"); board-grade
NEW imagery comes from a real image model. This tool is the pluggable front
door: same interface regardless of provider, board style language composed
into every prompt, and output that can flow straight through the re-ink
pipeline so it lands exactly on the brand palette.

    python3 design-engine/tools/imagegen.py "a reading room of blue arches" \
        --out design-engine/out/gen/arches.png \
        [--style midcentury-editorial] [--size 1536x1024] \
        [--provider openai|replicate] [--reink] [--n 1]

Providers (stdlib urllib only — no SDK deps):
  gemini     needs GEMINI_API_KEY        (model gemini-2.5-flash-image;
                                          supports --ref style-reference images
                                          — pass the board's images so new
                                          scenes are born in its exact style)
  openai     needs OPENAI_API_KEY        (model gpt-image-1)
  replicate  needs REPLICATE_API_TOKEN   (model black-forest-labs/flux-1.1-pro;
                                          text-only conditioning)
Select with --provider or IMAGEGEN_PROVIDER; with neither set, the tool exits
loudly explaining exactly which env var to add — set it in this environment's
settings (never commit keys).

--ref path[,path…] attaches reference images (gemini). Combine with --style:
the words carry the rules, the references carry the pixels.

--style NAME loads library/boards/NAME/board.json and prefixes the prompt
with the board's technique + palette language, so every generation is born
in the brand's world. --reink then maps the result onto the brand inks via
image_lab (palette from brand.json themes + lines + lamp) and adds grain —
the guarantee that generated art IS brand art.
"""
import base64
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import enginelib as lib  # noqa: E402


def compose_style(board_name: str) -> str:
    bp = lib.ENGINE_DIR / "library" / "boards" / board_name / "board.json"
    board = json.loads(bp.read_text(encoding="utf-8"))
    s = board["system"]
    parts = [
        f"Mid-century editorial illustration, {s['technique']}.",
        f"Grounds: {s['grounds']}. {s['brand_color']}.",
        f"Accent: {s['accent']}. Supporting colors: {', '.join(s['supporting'])}.",
        f"Composition: {s['composition']}.",
        "Never: " + "; ".join(s["donts"]) + ".",
    ]
    return " ".join(parts)


def brand_inks(brand: dict) -> list:
    """The re-ink palette: all theme role values + lamp + lines (deduped)."""
    inks = []
    for theme in brand["palette"]["themes"].values():
        for group in theme.values():
            for v in group.values():
                if isinstance(v, str) and v.startswith("#") and v not in inks:
                    inks.append(v)
    return inks


# ---- providers ---------------------------------------------------------------

def _post_json(url, payload, headers):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:600]
        raise SystemExit(f"FAIL  {e.code} from {url.split('/')[2]}: {body}")


def gen_openai(prompt, size, n):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit("FAIL  provider openai selected but OPENAI_API_KEY is not set "
                         "— add it to this environment's variables")
    out = _post_json("https://api.openai.com/v1/images/generations",
                     {"model": "gpt-image-1", "prompt": prompt, "size": size, "n": n},
                     {"Authorization": f"Bearer {key}"})
    return [base64.b64decode(d["b64_json"]) for d in out["data"]]


def gen_replicate(prompt, size, n):
    key = os.environ.get("REPLICATE_API_TOKEN")
    if not key:
        raise SystemExit("FAIL  provider replicate selected but REPLICATE_API_TOKEN is "
                         "not set — add it to this environment's variables")
    w, h = size.split("x")
    results = []
    for _ in range(n):
        pred = _post_json(
            "https://api.replicate.com/v1/models/black-forest-labs/flux-1.1-pro/predictions",
            {"input": {"prompt": prompt, "width": int(w), "height": int(h),
                       "output_format": "png"}},
            {"Authorization": f"Bearer {key}", "Prefer": "wait=60"})
        while pred["status"] in ("starting", "processing"):
            time.sleep(2)
            req = urllib.request.Request(pred["urls"]["get"],
                                         headers={"Authorization": f"Bearer {key}"})
            with urllib.request.urlopen(req, timeout=60) as r:
                pred = json.loads(r.read())
        if pred["status"] != "succeeded":
            raise SystemExit(f"FAIL  replicate prediction {pred['status']}: "
                             f"{pred.get('error')}")
        url = pred["output"] if isinstance(pred["output"], str) else pred["output"][0]
        with urllib.request.urlopen(url, timeout=120) as r:
            results.append(r.read())
    return results


def gen_gemini(prompt, size, n, refs=()):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("FAIL  provider gemini selected but GEMINI_API_KEY is not set "
                         "— get one at aistudio.google.com/apikey and add it to this "
                         "environment's variables")
    parts = []
    for ref in refs:
        rp = Path(ref)
        mime = "image/png" if rp.suffix.lower() == ".png" else "image/jpeg"
        parts.append({"inline_data": {"mime_type": mime,
                                      "data": base64.b64encode(rp.read_bytes()).decode()}})
    parts.append({"text": prompt})
    results = []
    for _ in range(n):
        out = _post_json(
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-2.5-flash-image:generateContent",
            {"contents": [{"parts": parts}],
             "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}},
            {"x-goog-api-key": key})
        blobs = [pt["inlineData"]["data"]
                 for cand in out.get("candidates", [])
                 for pt in cand.get("content", {}).get("parts", [])
                 if "inlineData" in pt]
        if not blobs:
            raise SystemExit(f"FAIL  gemini returned no image: "
                             f"{json.dumps(out)[:400]}")
        results.append(base64.b64decode(blobs[0]))
    return results


PROVIDERS = {"openai": gen_openai, "replicate": gen_replicate, "gemini": gen_gemini}


def main(argv):
    args = list(argv)
    if not args or args[0].startswith("--"):
        print(__doc__, file=sys.stderr)
        return 2
    prompt = args.pop(0)

    def opt(name, default=None):
        if name in args:
            return args[args.index(name) + 1]
        return default

    style = opt("--style")
    size = opt("--size", "1536x1024")
    n = int(opt("--n", 1))
    out = opt("--out")
    reink = "--reink" in args
    provider = opt("--provider", os.environ.get("IMAGEGEN_PROVIDER"))

    refs = [r for r in (opt("--ref", "") or "").split(",") if r]
    if not provider:
        print("FAIL  no image-generation provider configured.\n"
              "      Set IMAGEGEN_PROVIDER=gemini (+ GEMINI_API_KEY,\n"
              "        aistudio.google.com/apikey — recommended: takes the\n"
              "        board's images as style references) or\n"
              "      IMAGEGEN_PROVIDER=openai (+ OPENAI_API_KEY) or\n"
              "      IMAGEGEN_PROVIDER=replicate (+ REPLICATE_API_TOKEN)\n"
              "      in this environment's variables. Until then, the re-ink\n"
              "      pipeline over library/boards/ imagery is the hero-art path.",
              file=sys.stderr)
        return 1
    if provider not in PROVIDERS:
        print(f"FAIL  unknown provider '{provider}' (gemini|openai|replicate)",
              file=sys.stderr)
        return 1
    if refs and provider != "gemini":
        print(f"WARN  --ref is only wired for gemini; ignoring for {provider}",
              file=sys.stderr)
    if not out:
        print("--out required", file=sys.stderr)
        return 2

    full_prompt = (compose_style(style) + " " + prompt) if style else prompt
    print(f"provider={provider} size={size} n={n} reink={reink}")
    print(f"prompt: {full_prompt[:200]}{'…' if len(full_prompt) > 200 else ''}")
    if provider == "gemini":
        images = gen_gemini(full_prompt, size, n, refs=refs)
    else:
        images = PROVIDERS[provider](full_prompt, size, n)

    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    written = []
    for i, blob in enumerate(images):
        p = out_path if n == 1 else out_path.with_stem(f"{out_path.stem}-{i + 1}")
        p.write_bytes(blob)
        written.append(p)
        print(f"wrote {p}")

    if reink:
        import image_lab
        from PIL import Image
        brand = lib.load_brand()
        inks = brand_inks(brand)
        for p in written:
            im = Image.open(p)
            im = image_lab.palette_map(im, inks, levels=5, boost=1.05)
            im = image_lab.grain(im, amount=6)
            rp = p.with_stem(p.stem + "-inked")
            im.save(rp)
            print(f"wrote {rp}  (re-inked onto {len(inks)} brand inks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
