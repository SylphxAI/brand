#!/usr/bin/env python3
"""Draw every Sylphx logo file from mark.spec.json.

Outputs (under logo/):
  svg/       symbol, wordmark and lockup masters in every colour variant, the tile
  png/       renders of the masters
  favicon/   favicon.svg (the tile as a vector), favicon.ico, PNG sizes, apple-touch icon
  app-icon/  full-bleed store icon and the Android adaptive foreground
  sheet/     the usage sheet

Run from the repository root:
  pip install -r logo/construction/requirements.txt   (Python 3.14)
  python3 logo/construction/mark.py
"""

from __future__ import annotations

import io
import json
import re
from pathlib import Path

import resvg_py
import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
LOGO = HERE.parent
SPEC = json.loads((HERE / "mark.spec.json").read_text())
M = SPEC["mark"]
C = SPEC["colours"]

# Colour variants: (mark fill, wordmark). CURRENT is the gradient, drawn per file.
CURRENT = "current"
VARIANTS = {
    "colour": (CURRENT, C["ink"]),
    "colour-on-dark": (CURRENT, C["paper"]),
    "black": (C["black"], C["black"]),
    "white": (C["white"], C["white"]),
}


def fmt(x: float) -> str:
    s = f"{x:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def write(rel: str, data: str | bytes) -> None:
    path = LOGO / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        path.write_text(data)
    else:
        path.write_bytes(data)


def svg(w: float, h: float, body: str, vb_x: float = 0, vb_y: float = 0) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{fmt(vb_x)} {fmt(vb_y)} {fmt(w)} {fmt(h)}" '
        f'width="{fmt(w)}" height="{fmt(h)}" role="img" aria-label="Sylphx">{body}</svg>\n'
    )


def png(svg_text: str, width: int) -> Image.Image:
    return Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=svg_text, width=width)))).convert("RGBA")


def save_png(rel: str, im: Image.Image) -> None:
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    write(rel, buf.getvalue())


# ── The symbol ──────────────────────────────────────────────────────────────


def blade() -> list[tuple[str, list[tuple[float, float]]]]:
    """The blade as (command, points) on the blade grid: one M, then cubic segments, closed."""
    tokens = re.findall(r"[MCz]|-?\d+(?:\.\d+)?", M["blade"])
    assert tokens[0] == "M" and tokens[3] == "C" and tokens[-1] == "z", "blade must be M, one run of C, z"
    nums = [float(t) for t in tokens[4:-1]]
    assert len(nums) % 6 == 0, "each cubic segment takes three points"
    pts = [(nums[i], nums[i + 1]) for i in range(0, len(nums), 2)]
    return [("M", [(float(tokens[1]), float(tokens[2]))])] + [("C", pts[i : i + 3]) for i in range(0, len(pts), 3)]


def blades() -> list[list[tuple[str, list[tuple[float, float]]]]]:
    """Both blades on the blade grid: the second is the first rotated 180 degrees about the centre."""
    g = M["blade_grid"]
    first = blade()
    return [first, [(cmd, [(g - x, g - y) for x, y in pts]) for cmd, pts in first]]


def cubic_extent(p0: float, p1: float, p2: float, p3: float) -> tuple[float, float]:
    """Smallest and largest value one coordinate of a cubic takes for t in 0..1."""
    a, b, c = -p0 + 3 * p1 - 3 * p2 + p3, 2 * (p0 - 2 * p1 + p2), p1 - p0  # derivative / 3
    ts = []
    if abs(a) < 1e-12:
        if abs(b) > 1e-12:
            ts.append(-c / b)
    else:
        disc = b * b - 4 * a * c
        if disc >= 0:
            ts += [(-b + disc**0.5) / (2 * a), (-b - disc**0.5) / (2 * a)]
    vals = [p0, p3] + [
        (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t * t * p2 + t**3 * p3 for t in ts if 0 < t < 1
    ]
    return min(vals), max(vals)


def symbol_bounds() -> tuple[float, float, float, float]:
    """Tight bounds of the pair on the blade grid, from the curves themselves (not their control points)."""
    xs, ys = [], []
    for b in blades():
        cur = b[0][1][0]
        for _cmd, (c1, c2, end) in b[1:]:
            xs += cubic_extent(cur[0], c1[0], c2[0], end[0])
            ys += cubic_extent(cur[1], c1[1], c2[1], end[1])
            cur = end
    return min(xs), min(ys), max(xs), max(ys)


def symbol_box(k: float = 1.0) -> tuple[float, float]:
    """Width and height of the symbol's ink at k output units per blade-grid unit."""
    x0, y0, x1, y1 = symbol_bounds()
    return (x1 - x0) * k, (y1 - y0) * k


def symbol(fill: str, cx: float, cy: float, k: float, uid: str) -> str:
    """Both blades as one path, centred on (cx, cy) at k output units per blade-grid unit.

    Coordinates are written out, not transformed, so the gradient spans the pair
    as one field. The pair is point-symmetric, so its centre is the grid centre.
    """
    half = M["blade_grid"] / 2
    pt = lambda p: f"{fmt(cx + (p[0] - half) * k)} {fmt(cy + (p[1] - half) * k)}"
    d = "".join("".join(cmd + " ".join(pt(p) for p in pts) for cmd, pts in b) + "z" for b in blades())
    if fill != CURRENT:
        return f'<path fill="{fill}" d="{d}"/>'
    w, h = symbol_box(k)
    left, top = cx - w / 2, cy - h / 2
    cur = C["current"]
    (fx, fy), (tx, ty) = cur["from"], cur["to"]
    stops = "".join(f'<stop offset="{fmt(o)}" stop-color="{c}"/>' for o, c in cur["stops"])
    gid = f"sx-current-{uid}"
    return (
        f'<defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{fmt(left + fx * w)}" y1="{fmt(top + fy * h)}" '
        f'x2="{fmt(left + tx * w)}" y2="{fmt(top + ty * h)}">{stops}</linearGradient></defs>'
        f'<path fill="url(#{gid})" d="{d}"/>'
    )


# ── The wordmark ────────────────────────────────────────────────────────────


def wordmark() -> tuple[str, float, float, tuple[float, float, float, float]]:
    """Wordmark outline in font units (baseline y = 0, y down): path, cap height, scale to 1000/em, ink bounds."""
    wm = SPEC["wordmark"]
    font = TTFont(HERE / wm["font"])
    font.flavor = None  # HarfBuzz reads TrueType, not WOFF2
    upem = font["head"].unitsPerEm
    buf = io.BytesIO()
    font.save(buf)
    face = hb.Face(buf.getvalue())
    hbfont = hb.Font(face)
    hbfont.scale = (upem, upem)
    text = hb.Buffer()
    text.add_str(wm["text"])
    text.guess_segment_properties()
    hb.shape(hbfont, text, {"kern": True, "liga": True})
    glyphs = font.getGlyphSet()
    order = font.getGlyphOrder()
    pen, bounds = SVGPathPen(glyphs), BoundsPen(glyphs)
    x, tracking = 0.0, wm["tracking_em"] * upem
    infos, positions = text.glyph_infos, text.glyph_positions
    for n, (info, pos) in enumerate(zip(infos, positions)):
        t = (1, 0, 0, -1, x + pos.x_offset, -pos.y_offset)
        glyphs[order[info.codepoint]].draw(TransformPen(pen, t))
        glyphs[order[info.codepoint]].draw(TransformPen(bounds, t))
        x += pos.x_advance + (tracking if n < len(infos) - 1 else 0)
    return pen.getCommands(), font["OS/2"].sCapHeight * 1000 / upem, 1000 / upem, bounds.bounds


# ── Masters ─────────────────────────────────────────────────────────────────


def tile_svg(uid: str, fill: str = CURRENT) -> str:
    g = M["grid"]
    k = M["tile_symbol_ratio"] * g / symbol_box()[0]
    return svg(g, g, f'<rect width="{g}" height="{g}" rx="{M["tile_corner_radius"]}" fill="{C["field"]}"/>' + symbol(fill, g / 2, g / 2, k, uid))


def masters() -> dict[str, str]:
    out: dict[str, str] = {}
    g = M["grid"]
    k0 = g / M["blade_grid"]
    cx = cy = g / 2
    sw, sh = symbol_box(k0)
    for name, (fill, _w) in VARIANTS.items():
        out[f"svg/sylphx-symbol-{name}.svg"] = svg(sw, sh, symbol(fill, cx, cy, k0, f"symbol-{name}"), cx - sw / 2, cy - sh / 2)

    out["svg/sylphx-tile.svg"] = tile_svg("tile")

    path, cap, s, (x0, y0, x1, y1) = wordmark()
    ww, wh = (x1 - x0) * s, (y1 - y0) * s
    tf = f'transform="translate({fmt(-x0 * s)} {fmt(-y0 * s)}) scale({fmt(s)})"'
    for name, colour in (("ink", C["ink"]), ("paper", C["paper"]), ("black", C["black"]), ("white", C["white"])):
        out[f"svg/sylphx-wordmark-{name}.svg"] = svg(ww, wh, f'<path fill="{colour}" {tf} d="{path}"/>')

    lk = SPEC["lockup"]
    sym_h = lk["symbol_height_per_cap_height"] * cap
    k = sym_h / symbol_box()[1]
    sym_w = symbol_box(k)[0]
    gap = lk["gap_per_symbol_height"] * sym_h
    cap_mid = -cap / 2  # the symbol centres on the cap height; baseline is y = 0
    top = min(cap_mid - sym_h / 2, y0 * s)
    bottom = max(cap_mid + sym_h / 2, y1 * s)
    width = sym_w + gap + ww
    for name, (fill, wcol) in VARIANTS.items():
        body = symbol(fill, sym_w / 2, cap_mid - top, k, f"lockup-{name}") + (
            f'<path fill="{wcol}" transform="translate({fmt(sym_w + gap - x0 * s)} {fmt(-top)}) scale({fmt(s)})" d="{path}"/>'
        )
        out[f"svg/sylphx-lockup-{name}.svg"] = svg(width, bottom - top, body)
    return out


# ── Icons ───────────────────────────────────────────────────────────────────


def favicon_png(px: int) -> Image.Image:
    """The tile at px; at the smallest sizes the mark is flat (see spec, favicon)."""
    fv = SPEC["favicon"]
    return png(tile_svg("favicon", fv["flat_mark_colour"] if px <= fv["flat_mark_max_px"] else CURRENT), px)


def full_bleed(size: int, ratio: float, uid: str) -> str:
    k = ratio * size / symbol_box()[1]
    return svg(size, size, f'<rect width="{size}" height="{size}" fill="{C["field"]}"/>' + symbol(CURRENT, size / 2, size / 2, k, uid))


# ── Build ───────────────────────────────────────────────────────────────────


def main() -> None:
    ms = masters()
    for rel, text in ms.items():
        write(rel, text)
        width = 1600 if ("lockup" in rel or "wordmark" in rel) else 1024
        save_png(f"png/{Path(rel).stem}.png", png(text, width))

    write("favicon/favicon.svg", tile_svg("favicon"))
    for px in (16, 32, 48, 192, 512):
        save_png(f"favicon/favicon-{px}.png", favicon_png(px))
    buf = io.BytesIO()
    favicon_png(48).save(buf, "ICO", sizes=[(16, 16), (32, 32), (48, 48)], append_images=[favicon_png(16), favicon_png(32)])
    write("favicon/favicon.ico", buf.getvalue())
    ai = SPEC["app_icon"]
    save_png("favicon/apple-touch-icon-180.png", png(full_bleed(180, ai["symbol_ratio"], "touch-icon"), 180).convert("RGB"))

    icon = full_bleed(ai["size"], ai["symbol_ratio"], "app-icon")
    write("app-icon/sylphx-app-icon-1024.svg", icon)
    save_png("app-icon/sylphx-app-icon-1024.png", png(icon, ai["size"]).convert("RGB"))
    canvas = ai["android_adaptive_canvas"]
    ratio = ai["symbol_ratio"] * (72 / 108)
    sw, sh = symbol_box()
    # the mask is a circle: the corners of the mark's box must stay inside it
    assert ratio * (sw * sw + sh * sh) ** 0.5 / sh <= ai["android_safe_diameter_ratio"], "symbol leaves the Android safe zone"
    fg = svg(canvas, canvas, symbol(CURRENT, canvas / 2, canvas / 2, ratio * canvas / sh, "android-foreground"))
    write("app-icon/sylphx-android-foreground.svg", fg)
    save_png("app-icon/sylphx-android-foreground-432.png", png(fg, canvas))

    sheet(ms)


def sheet(ms: dict[str, str]) -> None:
    """Usage sheet: lockups on paper and ink, clear space, minimum sizes, favicons, tile."""
    W, H = 1600, 1000
    im = Image.new("RGBA", (W, H), C["paper"])
    im.alpha_composite(Image.new("RGBA", (W // 2, H // 2), C["ink"]), (W // 2, 0))
    lk = png(ms["svg/sylphx-lockup-colour.svg"], 560)
    im.alpha_composite(lk, (120, (H // 2 - lk.height) // 2))
    lkd = png(ms["svg/sylphx-lockup-colour-on-dark.svg"], 560)
    im.alpha_composite(lkd, (W // 2 + 120, (H // 2 - lkd.height) // 2))

    lk2 = png(ms["svg/sylphx-lockup-colour.svg"], 480)
    sw, sh = symbol_box()
    lk_w, lk_h = (float(v) for v in re.search(r'width="([\d.]+)" height="([\d.]+)"', ms["svg/sylphx-lockup-colour.svg"]).groups())
    sym_h_px = SPEC["lockup"]["symbol_height_per_cap_height"] * wordmark()[1] * lk2.width / lk_w
    pad = round(SPEC["clear_space"]["per_symbol_height"] * sym_h_px)
    ox, oy = 120, H // 2 + (H // 2 - lk2.height) // 2
    im.alpha_composite(lk2, (ox, oy))
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = ox - pad, oy - pad, ox + lk2.width + pad, oy + lk2.height + pad
    for x in range(x0, x1, 12):
        d.line([(x, y0), (x + 6, y0)], fill=C["accent"])
        d.line([(x, y1), (x + 6, y1)], fill=C["accent"])
    for y in range(y0, y1, 12):
        d.line([(x0, y), (x0, y + 6)], fill=C["accent"])
        d.line([(x1, y), (x1, y + 6)], fill=C["accent"])

    mins = SPEC["minimum_size_px"]
    mid = H // 2 + H // 4  # everything in the right half centres on this line
    row = [
        png(ms["svg/sylphx-symbol-colour.svg"], round(mins["symbol"] * sw / sh)),
        png(ms["svg/sylphx-lockup-colour.svg"], mins["lockup_width"]),
        favicon_png(16),
        favicon_png(32),
        favicon_png(48),
        png(ms["svg/sylphx-tile.svg"], 160),
    ]
    x = W // 2 + 120
    for item in row:
        im.alpha_composite(item, (x, mid - item.height // 2))
        x += item.width + 40
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "PNG", optimize=True)
    write("sheet/usage.png", buf.getvalue())


if __name__ == "__main__":
    main()
