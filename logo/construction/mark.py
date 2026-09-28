#!/usr/bin/env python3
"""Draw every Sylphx logo file from mark.spec.json.

Outputs (under logo/):
  svg/       symbol, wordmark and lockup masters in every colour variant, the tile
  png/       renders of the masters
  favicon/   pixel-snapped 16 and 32 px icons, favicon.svg and .ico, PNG sizes, apple-touch icon
  app-icon/  full-bleed store icon and the Android adaptive foreground
  sheet/     the usage sheet
  construction/pixel-grids.txt   the snapped grids, for review in a diff

Run from the repository root:
  pip install pillow numpy fonttools brotli uharfbuzz resvg-py
  python3 logo/construction/mark.py
"""

from __future__ import annotations

import io
import json
from pathlib import Path

import numpy as np
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

# Colour variants: (under current, over current, wordmark)
VARIANTS = {
    "colour": (C["accent"], C["ink"], C["ink"]),
    "colour-on-dark": (C["accent_on_dark"], C["paper"], C["paper"]),
    "black": (C["black"], C["black"], C["black"]),
    "white": (C["white"], C["white"], C["white"]),
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


def currents(cx: float, cy: float, k: float) -> tuple[str, str]:
    """The rising (under) and falling (over) currents as path data, scaled by k about (cx, cy)."""
    h, p = M["half_span"] * k, M["control_pull"] * k
    under = f"M{fmt(cx - h)} {fmt(cy - h)}C{fmt(cx + p)} {fmt(cy - h)} {fmt(cx - p)} {fmt(cy + h)} {fmt(cx + h)} {fmt(cy + h)}"
    over = f"M{fmt(cx + h)} {fmt(cy - h)}C{fmt(cx - p)} {fmt(cy - h)} {fmt(cx + p)} {fmt(cy + h)} {fmt(cx - h)} {fmt(cy + h)}"
    return under, over


def symbol(under_c: str, over_c: str, cx: float, cy: float, k: float, uid: str) -> str:
    under, over = currents(cx, cy, k)
    w = M["stroke_width"] * k
    gap = M["weave_gap"] * k
    g = M["grid"]
    return (
        f'<defs><mask id="w{uid}" maskUnits="userSpaceOnUse" x="-{g}" y="-{g}" width="{3 * g}" height="{3 * g}">'
        f'<rect x="-{g}" y="-{g}" width="{3 * g}" height="{3 * g}" fill="#fff"/>'
        f'<path d="{over}" fill="none" stroke="#000" stroke-width="{fmt(w + 2 * gap)}"/></mask></defs>'
        f'<path d="{under}" fill="none" stroke="{under_c}" stroke-width="{fmt(w)}" mask="url(#w{uid})"/>'
        f'<path d="{over}" fill="none" stroke="{over_c}" stroke-width="{fmt(w)}"/>'
    )


def symbol_box(k: float = 1.0) -> tuple[float, float]:
    """Width and height of the symbol's ink: flat ends, horizontal at the tips."""
    return 2 * M["half_span"] * k, (2 * M["half_span"] + M["stroke_width"]) * k


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


def masters() -> dict[str, str]:
    out: dict[str, str] = {}
    g = M["grid"]
    cx = cy = g / 2
    sw, sh = symbol_box()
    for name, (u, o, _w) in VARIANTS.items():
        out[f"svg/sylphx-symbol-{name}.svg"] = svg(sw, sh, symbol(u, o, cx, cy, 1, name), cx - sw / 2, cy - sh / 2)

    u, o, _ = VARIANTS["colour-on-dark"]
    r = M["tile_corner_radius"]
    out["svg/sylphx-tile.svg"] = svg(
        g, g,
        f'<rect width="{g}" height="{g}" rx="{r}" fill="{C["field"]}"/>'
        + symbol(u, o, cx, cy, M["tile_symbol_scale"], "tile"),
    )

    path, cap, s, (x0, y0, x1, y1) = wordmark()
    ww, wh = (x1 - x0) * s, (y1 - y0) * s
    tf = f'transform="translate({fmt(-x0 * s)} {fmt(-y0 * s)}) scale({fmt(s)})"'
    for name, colour in (("ink", C["ink"]), ("paper", C["paper"]), ("black", C["black"]), ("white", C["white"])):
        out[f"svg/sylphx-wordmark-{name}.svg"] = svg(ww, wh, f'<path fill="{colour}" {tf} d="{path}"/>')

    lk = SPEC["lockup"]
    sym_h = lk["symbol_height_per_cap_height"] * cap
    k = sym_h / sh
    sym_w = sw * k
    gap = lk["gap_per_symbol_height"] * sym_h
    cap_mid = -cap / 2  # the symbol centres on the cap height; baseline is y = 0
    top = min(cap_mid - sym_h / 2, y0 * s)
    bottom = max(cap_mid + sym_h / 2, y1 * s)
    width = sym_w + gap + ww
    for name, (u, o, wcol) in VARIANTS.items():
        body = symbol(u, o, sym_w / 2, cap_mid - top, k, f"l{name}") + (
            f'<path fill="{wcol}" transform="translate({fmt(sym_w + gap - x0 * s)} {fmt(-top)}) scale({fmt(s)})" d="{path}"/>'
        )
        out[f"svg/sylphx-lockup-{name}.svg"] = svg(width, bottom - top, body)
    return out


# ── Pixel-snapped icons ────────────────────────────────────────────────────


def hexrgb(h: str) -> np.ndarray:
    return np.array([int(h[i : i + 2], 16) for i in (1, 3, 5)], dtype=float)


def snap(tile_svg: str, px: int) -> list[str]:
    """Whole-pixel grid: '.' empty, 'f' field, 'a' accent, 'p' paper.

    Each pixel takes the colour that covers most of it (supersampled 16x), so
    every edge lands on a pixel boundary and the two currents stay two tones.
    """
    ss = 16
    im = np.asarray(png(tile_svg, px * ss)).astype(float)
    cols = {"f": hexrgb(C["field"]), "a": hexrgb(C["accent_on_dark"]), "p": hexrgb(C["paper"])}
    keys = list(cols)
    ref = np.stack([cols[k] for k in keys])
    alpha = im[..., 3] / 255
    rgb = im[..., :3]
    nearest = np.argmin(((rgb[..., None, :] - ref) ** 2).sum(-1), axis=-1)
    rows = []
    for y in range(px):
        row = ""
        for x in range(px):
            blk_a = alpha[y * ss : (y + 1) * ss, x * ss : (x + 1) * ss]
            if blk_a.mean() < 0.5:
                row += "."
                continue
            blk = nearest[y * ss : (y + 1) * ss, x * ss : (x + 1) * ss][blk_a > 0.5]
            counts = np.bincount(blk, minlength=len(keys))
            # an ink pixel wins when it covers at least 40%: thin strokes survive
            ink = [i for i, key in enumerate(keys) if key != "f"]
            best = max(ink, key=lambda i: counts[i])
            row += keys[best] if counts[best] >= 0.4 * blk.size else "f"
        rows.append(row)
    return rows


def grid_svg(rows: list[str]) -> str:
    colours = {"f": C["field"], "a": C["accent_on_dark"], "p": C["paper"]}
    rects = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            ch = row[x]
            start = x
            while x < len(row) and row[x] == ch:
                x += 1
            if ch != ".":
                rects.append(f'<rect x="{start}" y="{y}" width="{x - start}" height="1" fill="{colours[ch]}"/>')
    n = len(rows)
    return svg(n, n, "".join(rects)).replace("<svg ", '<svg shape-rendering="crispEdges" ', 1)


def grid_png(rows: list[str]) -> Image.Image:
    n = len(rows)
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    colours = {"f": C["field"], "a": C["accent_on_dark"], "p": C["paper"]}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), tuple(int(v) for v in hexrgb(colours[ch])) + (255,))
    return im


def full_bleed(size: int, ratio: float) -> str:
    u, o, _ = VARIANTS["colour-on-dark"]
    _sw, sh = symbol_box()
    k = ratio * size / sh
    return svg(size, size, f'<rect width="{size}" height="{size}" fill="{C["field"]}"/>' + symbol(u, o, size / 2, size / 2, k, "fb"))


# ── Build ───────────────────────────────────────────────────────────────────


def main() -> None:
    ms = masters()
    for rel, text in ms.items():
        write(rel, text)
        width = 1600 if ("lockup" in rel or "wordmark" in rel) else 1024
        save_png(f"png/{Path(rel).stem}.png", png(text, width))

    tile = ms["svg/sylphx-tile.svg"]
    grids = {px: snap(tile, px) for px in (16, 32)}
    write("construction/pixel-grids.txt", "".join(f"{px} px\n" + "\n".join(g) + "\n\n" for px, g in grids.items()))
    write("favicon/favicon.svg", grid_svg(grids[32]))
    for px, g in grids.items():
        save_png(f"favicon/favicon-{px}.png", grid_png(g))
    for px in (48, 192, 512):
        save_png(f"favicon/favicon-{px}.png", png(tile, px))
    buf = io.BytesIO()
    png(tile, 48).save(buf, "ICO", sizes=[(16, 16), (32, 32), (48, 48)], append_images=[grid_png(grids[16]), grid_png(grids[32])])
    write("favicon/favicon.ico", buf.getvalue())
    ai = SPEC["app_icon"]
    save_png("favicon/apple-touch-icon-180.png", png(full_bleed(180, ai["symbol_ratio"]), 180).convert("RGB"))

    icon = full_bleed(ai["size"], ai["symbol_ratio"])
    write("app-icon/sylphx-app-icon-1024.svg", icon)
    save_png("app-icon/sylphx-app-icon-1024.png", png(icon, ai["size"]).convert("RGB"))
    canvas = ai["android_adaptive_canvas"]
    ratio = ai["symbol_ratio"] * (72 / 108)
    assert ratio <= ai["android_safe_diameter_ratio"], "symbol leaves the Android safe zone"
    u, o, _ = VARIANTS["colour-on-dark"]
    _sw, sh = symbol_box()
    fg = svg(canvas, canvas, symbol(u, o, canvas / 2, canvas / 2, ratio * canvas / sh, "fg"))
    write("app-icon/sylphx-android-foreground.svg", fg)
    save_png("app-icon/sylphx-android-foreground-432.png", png(fg, canvas))

    sheet(ms, grids)


def sheet(ms: dict[str, str], grids: dict[int, list[str]]) -> None:
    """Usage sheet: lockups on paper and ink, clear space, minimum sizes, favicons, app icon."""
    W, H = 1600, 1000
    im = Image.new("RGBA", (W, H), C["paper"])
    im.alpha_composite(Image.new("RGBA", (W // 2, H // 2), C["ink"]), (W // 2, 0))
    lk = png(ms["svg/sylphx-lockup-colour.svg"], 560)
    im.alpha_composite(lk, (120, (H // 2 - lk.height) // 2))
    lkd = png(ms["svg/sylphx-lockup-colour-on-dark.svg"], 560)
    im.alpha_composite(lkd, (W // 2 + 120, (H // 2 - lkd.height) // 2))

    lk2 = png(ms["svg/sylphx-lockup-colour.svg"], 480)
    pad = int(SPEC["clear_space"]["per_symbol_height"] * lk2.height)
    ox, oy = 120, H // 2 + 130
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
    im.alpha_composite(png(ms["svg/sylphx-symbol-colour.svg"], 13), (960, H // 2 + 190))
    im.alpha_composite(png(ms["svg/sylphx-lockup-colour.svg"], mins["lockup_width"]), (1000, H // 2 + 190))
    im.alpha_composite(grid_png(grids[16]), (1120, H // 2 + 188))
    im.alpha_composite(grid_png(grids[32]), (1150, H // 2 + 180))
    im.alpha_composite(png(ms["svg/sylphx-tile.svg"], 160), (1220, H // 2 + 120))
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "PNG", optimize=True)
    write("sheet/usage.png", buf.getvalue())


if __name__ == "__main__":
    main()
