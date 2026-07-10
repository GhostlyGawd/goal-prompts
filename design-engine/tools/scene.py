#!/usr/bin/env python3
"""scene — procedural illustration with craft density. Stdlib only.

The anti-stick-figure library: helpers that make hand-coded SVG read like
printed illustration instead of clean vectors. Used by artifact builders and
(in application phases) by hero/asset generators. Everything is deterministic
given a seed — no Date.now/random drift between builds.

Ingredients (see library/techniques/svg-gouache.md for the method):
  wobble_path(points, seed)      hand-drawn line: subtle per-segment jitter
  hatch(x,y,w,h, ...)            hatching fill for shaded areas
  grain_filter(id, amount)       paper-grain <filter> (feTurbulence)
  rough_filter(id, scale)        edge roughening (displacement) for gouache edges
  misregister(svg_body, dx, dy, color, opacity)
                                 offset color pass — screen-print misregistration
  arch_band(...) / checker_floor(...) / doc_shelf(...) / bubble_lamp(...)
                                 the board's motifs, drawn dense
"""
import math
import random


def _rng(seed):
    return random.Random(seed)


def wobble_path(points, seed=1, amp=0.8, step=14, close=False):
    """Polyline through `points` with hand-drawn jitter. Subdivides long
    segments every `step` units and displaces midpoints by ±amp."""
    r = _rng(seed)
    out = []
    for i, (x, y) in enumerate(points):
        if i == 0:
            out.append(f"M{x:.1f} {y:.1f}")
            continue
        px, py = points[i - 1]
        dist = math.hypot(x - px, y - py)
        n = max(1, int(dist / step))
        for j in range(1, n + 1):
            t = j / n
            mx = px + (x - px) * t + (r.random() - 0.5) * 2 * amp * (0 if j == n else 1)
            my = py + (y - py) * t + (r.random() - 0.5) * 2 * amp * (0 if j == n else 1)
            out.append(f"L{mx:.1f} {my:.1f}")
    if close:
        out.append("Z")
    return " ".join(out)


def hatch(x, y, w, h, spacing=5, angle=45, color="#1D1F28", width=0.9,
          opacity=0.5, seed=3):
    """Hand-hatching inside a rect (clip it yourself if the shape isn't a rect)."""
    r = _rng(seed)
    lines = []
    rad = math.radians(angle)
    dx, dy = math.cos(rad), math.sin(rad)
    diag = math.hypot(w, h)
    n = int(diag / spacing) + 2
    for i in range(-n, n):
        cx, cy = x + w / 2 + i * spacing * -dy, y + h / 2 + i * spacing * dx
        j = (r.random() - 0.5) * spacing * 0.4
        lines.append(
            f'<line x1="{cx - dx * diag / 2 + j:.1f}" y1="{cy - dy * diag / 2:.1f}" '
            f'x2="{cx + dx * diag / 2 + j:.1f}" y2="{cy + dy * diag / 2:.1f}" '
            f'stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>')
    clip_id = f"hcl{abs(hash((x, y, w, h, seed))) % 99999}"
    return (f'<clipPath id="{clip_id}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'
            f'<g clip-path="url(#{clip_id})">{"".join(lines)}</g>')


def grain_filter(fid="grain", amount=0.06, freq=0.9):
    return (f'<filter id="{fid}"><feTurbulence type="fractalNoise" baseFrequency="{freq}" '
            f'numOctaves="2" result="n"/><feColorMatrix in="n" type="matrix" '
            f'values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.6 0.6 0.6 0 0" result="a"/>'
            f'<feComposite operator="in" in="a" in2="SourceGraphic" result="g"/>'
            f'<feBlend in="SourceGraphic" in2="g" mode="multiply"/></filter>')


def rough_filter(fid="rough", scale=1.6, freq=0.06, seed=2):
    """Displacement roughening — gives flat shapes gouache-brush edges."""
    return (f'<filter id="{fid}" x="-5%" y="-5%" width="110%" height="110%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="3" '
            f'seed="{seed}" result="n"/>'
            f'<feDisplacementMap in="SourceGraphic" in2="n" scale="{scale}"/></filter>')


def misregister(body, dx=1.4, dy=-1.1, color="#E8752C", opacity=0.35):
    """A second, offset, recolored pass of a shape group — the screen-print
    misregistration that makes flat color read as printed. `body` must use
    fill="currentColor" for the parts to offset."""
    return (f'<g transform="translate({dx} {dy})" color="{color}" opacity="{opacity}" '
            f'aria-hidden="true">{body}</g>'
            f'<g color="inherit">{body}</g>')


def checker_floor(x, y, w, h, cols, rows, a="#FFFFFF", b="#F1EBDA",
                  line="#1D1F28", perspective=0.0, seed=5):
    """Tiled floor; perspective>0 shrinks far rows. Slight per-tile tint jitter."""
    r = _rng(seed)
    tiles = []
    row_heights = []
    total = 0.0
    for i in range(rows):
        rh = 1.0 - perspective * (rows - 1 - i) / max(1, rows - 1)
        row_heights.append(rh)
        total += rh
    ty = y
    for i, rh in enumerate(row_heights):
        th = h * rh / total
        tw = w / cols
        for c in range(cols):
            fill = a if (c + i) % 2 == 0 else b
            if r.random() < 0.18:
                fill = fill + "F0" if len(fill) == 7 else fill
            tiles.append(f'<rect x="{x + c * tw:.1f}" y="{ty:.1f}" width="{tw:.2f}" '
                         f'height="{th:.2f}" fill="{fill}"/>')
        ty += th
    tiles.append(f'<line x1="{x}" y1="{y}" x2="{x + w}" y2="{y}" stroke="{line}" stroke-width="1.6"/>')
    return "".join(tiles)


def arch_band(cx, base_y, half_w, top_y, color, width=14, seed=7, wobble=0.7):
    """One arch drawn as a wobbled stroke — layer several with shrinking
    half_w/top_y for the arcade."""
    x0, x1 = cx - half_w, cx + half_w
    rr = half_w
    pts_left = [(x0, base_y), (x0, top_y + rr)]
    d_left = wobble_path(pts_left, seed=seed, amp=wobble)
    d_arc = f"A{rr:.1f} {rr:.1f} 0 0 1 {x1:.1f} {top_y + rr:.1f}"
    d_right = wobble_path([(x1, top_y + rr), (x1, base_y)], seed=seed + 1, amp=wobble)[1:]
    d_right = "L" + d_right.split(" ", 1)[1] if d_right.startswith("M") else d_right
    return (f'<path d="{d_left} {d_arc} {d_right}" fill="none" stroke="{color}" '
            f'stroke-width="{width}"/>')


def doc_shelf(x, y, w, h, ink="#1D1F28", paper="#F1EBDA", accent="#B4531A", seed=11):
    """A shelf of leaning documents/spec-sheets — the board's archive texture."""
    r = _rng(seed)
    items = [f'<line x1="{x}" y1="{y + h}" x2="{x + w}" y2="{y + h}" stroke="{ink}" stroke-width="1.4"/>']
    cx = x
    while cx < x + w - 4:
        dw = r.uniform(5, 11)
        dh = r.uniform(h * 0.55, h * 0.95)
        lean = r.uniform(-4, 4)
        doc_x = cx + lean * 0.2
        items.append(f'<g transform="rotate({lean:.1f} {doc_x + dw / 2:.1f} {y + h:.1f})">'
                     f'<rect x="{doc_x:.1f}" y="{y + h - dh:.1f}" width="{dw:.1f}" height="{dh:.1f}" '
                     f'fill="{paper}" stroke="{ink}" stroke-width="0.8"/>')
        ly = y + h - dh + 2.5
        while ly < y + h - 2.5:
            lw = dw * r.uniform(0.5, 0.85)
            col = accent if r.random() < 0.08 else ink
            items.append(f'<line x1="{doc_x + 1.5:.1f}" y1="{ly:.1f}" '
                         f'x2="{doc_x + 1.5 + lw:.1f}" y2="{ly:.1f}" '
                         f'stroke="{col}" stroke-width="0.7" opacity="0.75"/>')
            ly += r.uniform(1.8, 2.8)
        items.append("</g>")
        cx += dw + r.uniform(1, 4)
    return "".join(items)


def bubble_lamp(cx, cord_top, cord_len, rx, ry, body="#E8752C", stripe="#B4531A",
                ink="#1D1F28", glow=True, seed=13):
    cy = cord_top + cord_len + ry
    stripes = []
    for i in range(-3, 4):
        off = i * rx / 3.6
        stripes.append(f"M{cx + off * 0.55:.1f} {cy - ry:.1f} "
                       f"C{cx + off:.1f} {cy - ry / 2:.1f} {cx + off:.1f} {cy + ry / 2:.1f} "
                       f"{cx + off * 0.55:.1f} {cy + ry:.1f}")
    glow_el = (f'<circle cx="{cx}" cy="{cy}" r="{rx * 2.1}" fill="{body}" opacity="0.10"/>'
               f'<circle cx="{cx}" cy="{cy}" r="{rx * 1.45}" fill="{body}" opacity="0.12"/>') if glow else ""
    return (glow_el
            + f'<path d="{wobble_path([(cx, cord_top), (cx, cord_top + cord_len)], seed=seed, amp=0.5)}" '
              f'stroke="{ink}" stroke-width="2" fill="none"/>'
            + f'<rect x="{cx - 5}" y="{cord_top + cord_len - 1}" width="10" height="6" rx="2" fill="{ink}"/>'
            + f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{body}"/>'
            + f'<path d="{" ".join(stripes)}" stroke="{stripe}" stroke-width="1.6" '
              f'fill="none" opacity="0.55"/>')
