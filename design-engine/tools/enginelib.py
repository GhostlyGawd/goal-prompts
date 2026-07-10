"""Shared helpers for the design-engine tools. Stdlib only.

Every tool locates brand.json relative to this package (design-engine/brand.json),
so the engine keeps working when the folder is copied into another repo. The
host repo root is design-engine's parent directory. Override the manifest path
with the BRAND_JSON environment variable or a tool's --brand flag.
"""
import json
import os
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parents[1]   # .../design-engine
HOST_ROOT = ENGINE_DIR.parent                       # the repo the engine serves
OUT_DIR = ENGINE_DIR / "out"


def brand_path(cli_arg=None) -> Path:
    if cli_arg:
        return Path(cli_arg)
    env = os.environ.get("BRAND_JSON")
    if env:
        return Path(env)
    return ENGINE_DIR / "brand.json"


def load_brand(cli_arg=None) -> dict:
    return json.loads(brand_path(cli_arg).read_text(encoding="utf-8"))


# ---- color math (WCAG 2.1) -------------------------------------------------

def hex_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb) -> float:
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def ratio(a, b) -> float:
    """Contrast ratio between two colors (hex strings or rgb tuples)."""
    if isinstance(a, str):
        a = hex_rgb(a)
    if isinstance(b, str):
        b = hex_rgb(b)
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def mix_toward(hexv: str, percent: float, toward: str = "black"):
    """color-mix(in srgb, C percent%, black|white) — the exact arithmetic the
    compiled CSS uses for categorical hues on non-default themes; returns an
    rgb tuple (floats). percent is C's share, the remainder is the mix target."""
    p = percent / 100
    base = 0.0 if toward == "black" else 255.0
    return tuple(c * p + base * (1 - p) for c in hex_rgb(hexv))


def mix_toward_black(hexv: str, percent: float):
    return mix_toward(hexv, percent, "black")


# ---- theme access ----------------------------------------------------------

def theme_roles(brand: dict, theme: str) -> dict:
    """Flatten a theme's role groups into one {role: value} map (values may be
    '@alias' references)."""
    flat = {}
    for group in brand["palette"]["themes"][theme].values():
        flat.update(group)
    return flat


def resolve_role(roles: dict, name: str, _seen=None) -> str:
    """Resolve a role to a concrete hex value, following '@alias' references."""
    _seen = _seen or set()
    if name in _seen:
        raise ValueError(f"alias cycle at '{name}'")
    _seen.add(name)
    v = roles[name]
    if v.startswith("@"):
        return resolve_role(roles, v[1:], _seen)
    return v


def fmt_num(v) -> str:
    """Format a manifest number the way the SVG mark expects: 6.9 not 6.90, 11 not 11.0."""
    return f"{v:g}"
