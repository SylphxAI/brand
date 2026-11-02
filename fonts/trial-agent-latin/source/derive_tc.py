"""Pip Trial TC: Traditional Chinese derived from Noto Sans TC, in Pip's style.

    python derive_tc.py <NotoSansTC[wght].ttf> [<reference-out.ttf>]

The structure of every character comes unchanged from Noto Sans TC (the
Source Han Sans design, Taiwan forms, SIL OFL 1.1). Nothing is redrawn. Our
style is applied as rules that read only the outline, so they run the same on
any character:

1. Weight: an instance of the weight axis whose single-stroke stem matches
   Pip's Latin stem (104 units). The source's own weight design thins dense
   characters, which a plain outline offset would clog.
2. Rounded terminals: a morphological opening (erode, then dilate, by
   ROUND units) rounds every convex corner, so stroke ends and turns become
   round like Pip's, while counters and stroke widths keep their size.
   Thin parts the opening would delete (tapered tips, small dots) are kept,
   rounded by a smaller radius.
3. Soft joins: a small closing (dilate, then erode, by JOIN units) eases the
   inner corners where strokes meet, the ink-pooling look of a round brush.

The optional second argument writes the same weight instance, unmodified,
for the side-by-side specimen.
"""

import sys
import time
from pathlib import Path

import numpy as np
import pathops
import potrace
from scipy import ndimage
import skia
from fontTools import subset
from fontTools.pens.basePen import BasePen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

from skeleton import _DropDegenerate, _skia_to_pathops

HERE = Path(__file__).resolve().parent
OUT = HERE.parent

WEIGHT = 500  # wght where the stem of 丨 is 103 units, Pip's Latin stem is 104
ROUND = 26  # corner radius of the opening (units per em 1000)
JOIN = 9  # radius of the closing at inner corners
KEEP = 10  # thin parts wider than 2 * KEEP survive the rounding
TEXT = "開始遊戲勝利失敗分數等級金幣麻將大老二你好香港永" + "，、。！？・·「」"

FAMILY = "Pip Trial TC"
PS = "PipTrialTC-Regular"
VERSION = "0.200"
COPYRIGHT = ("Copyright 2014-2021 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'. "
             "Copyright 2026 Sylphx Limited.")
DESCRIPTION = ("Derived from Noto Sans TC (Source Han Sans) by rounding its outlines; "
               "the character structure is unchanged.")
LICENSE = ("This Font Software is licensed under the SIL Open Font License, Version 1.1. "
           "This license is available with a FAQ at: https://openfontlicense.org")


def to_pathops(glyphset, name):
    sp = skia.Path()
    glyphset[name].draw(_SkiaPen(sp, glyphset))
    p = pathops.Path()
    _skia_to_pathops(sp, p)
    p.simplify(fix_winding=True, clockwise=True)
    return p


class _SkiaPen(BasePen):
    """Any fontTools drawing into a skia.Path (BasePen resolves implied
    on-curve points of TrueType quadratics)."""

    def __init__(self, out, glyphset=None):
        super().__init__(glyphset)
        self.out = out

    def _moveTo(self, pt):
        self.out.moveTo(*pt)

    def _lineTo(self, pt):
        self.out.lineTo(*pt)

    def _curveToOne(self, a, b, c):
        self.out.cubicTo(*a, *b, *c)

    def _qCurveToOne(self, a, b):
        self.out.quadTo(*a, *b)

    def _closePath(self):
        self.out.close()


def to_skia(p):
    out = skia.Path()
    p.draw(_SkiaPen(out))
    return out


SCALE = 2  # raster pixels per font unit for the morphology


def raster(p):
    """Fill a pathops outline into a boolean grid (SCALE px per unit) with a
    margin, and return it with the transform back to font units."""
    x0, y0, x1, y1 = p.bounds
    m = ROUND + 8
    x0, y0, x1, y1 = x0 - m, y0 - m, x1 + m, y1 + m
    w, h = int((x1 - x0) * SCALE) + 1, int((y1 - y0) * SCALE) + 1
    surf = skia.Surface(w, h)
    c = surf.getCanvas()
    c.clear(skia.ColorBLACK)
    mat = skia.Matrix()
    mat.setAll(SCALE, 0, -x0 * SCALE, 0, -SCALE, y1 * SCALE, 0, 0, 1)
    c.concat(mat)
    c.drawPath(to_skia(p), skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
    img = surf.makeImageSnapshot().toarray()[:, :, 0]
    return img >= 128, (x0, y1)


def disc_open(a, r):
    """Opening by a disc of radius r px: erode then dilate, via distance maps."""
    core = ndimage.distance_transform_edt(a) > r
    return ndimage.distance_transform_edt(~core) <= r


def disc_close(a, r):
    grown = ndimage.distance_transform_edt(~a) <= r
    return ndimage.distance_transform_edt(grown) > r


def style_bitmap(a):
    r = ROUND * SCALE
    o = disc_open(a, r)  # round every convex corner by ROUND
    # The opening also deletes parts thinner than 2 * ROUND (tapered tips,
    # small dots). Keep the deleted pieces that are real strokes, not the
    # slivers cut from corners: a corner sliver has no point deeper than KEEP.
    lost = a & ~o
    lab, n = ndimage.label(lost)
    if n:
        depth = ndimage.distance_transform_edt(lost)
        deep = ndimage.maximum(depth, lab, index=np.arange(1, n + 1))
        keep = np.isin(lab, np.nonzero(deep > KEEP * SCALE)[0] + 1)
        o |= disc_open(keep, KEEP * SCALE * 0.8)
    if JOIN:
        o = disc_close(o, JOIN * SCALE)  # soften inner corners
    return o


def trace(a, origin):
    """Vectorise a bitmap with potrace (smooth cubic curves)."""
    x0, top = origin
    bm = potrace.Bitmap(~a)  # potracer traces the False cells
    plist = bm.trace(turdsize=8, alphamax=1.0, opticurve=True, opttolerance=0.2)

    def u(pt):
        return (x0 + pt.x / SCALE, top - pt.y / SCALE)

    out = skia.Path()
    for curve in plist:
        out.moveTo(*u(curve.start_point))
        for seg in curve.segments:
            if seg.is_corner:
                out.lineTo(*u(seg.c))
                out.lineTo(*u(seg.end_point))
            else:
                out.cubicTo(*u(seg.c1), *u(seg.c2), *u(seg.end_point))
        out.close()
    q = pathops.Path()
    _skia_to_pathops(out, q)
    q.simplify(fix_winding=True, clockwise=True)
    # drop specks (the tracer leaves one at the bitmap corner)
    kept = pathops.Path()
    pen = kept.getPen()
    for contour in q.contours:
        x0c, y0c, x1c, y1c = contour.bounds
        if max(x1c - x0c, y1c - y0c) >= 20:
            contour.draw(pen)
    return kept


def style(p):
    a, origin = raster(p)
    return trace(style_bitmap(a), origin)


def tt(p):
    pen = TTGlyphPen(None)
    p.draw(Cu2QuPen(_DropDegenerate(pen), max_err=0.5, reverse_direction=False))
    return pen.glyph()


def instance(src):
    f = TTFont(src)
    opt = subset.Options()
    opt.layout_features = ["*"]
    opt.hinting = False
    opt.notdef_outline = True
    opt.name_IDs = ["*"]
    s = subset.Subsetter(opt)
    s.populate(text=TEXT + " ")
    s.subset(f)
    return instancer.instantiateVariableFont(f, {"wght": WEIGHT}, inplace=False)


def rename(f):
    name = f["name"]
    name.names = []
    for nid, val in {
        0: COPYRIGHT, 1: FAMILY, 2: "Regular", 3: f"{VERSION};SYLX;{PS}", 4: f"{FAMILY} Regular",
        5: f"Version {VERSION}", 6: PS, 8: "Sylphx Limited", 9: "Ryoko Nishizuka (Source Han Sans); Sylphx Limited",
        10: DESCRIPTION, 11: "https://sylphx.com", 13: LICENSE, 14: "https://openfontlicense.org",
    }.items():
        name.setName(val, nid, 3, 1, 0x409)
    for t in ("STAT", "DSIG", "meta"):
        if t in f:
            del f[t]
    f["OS/2"].achVendID = "SYLX"
    f["OS/2"].usWeightClass = 400
    f["OS/2"].fsSelection = (f["OS/2"].fsSelection & ~0b1100001) | 0x40
    f["head"].fontRevision = float(VERSION)
    f["head"].macStyle = 0
    # vertical metrics: one set, from the source's typo metrics
    os2, hhea = f["OS/2"], f["hhea"]
    os2.fsSelection |= 1 << 7  # USE_TYPO_METRICS
    hhea.ascent, hhea.descent, hhea.lineGap = os2.sTypoAscender, os2.sTypoDescender, os2.sTypoLineGap
    glyf = f["glyf"]
    drawn = [glyf[n] for n in f.getGlyphOrder() if glyf[n].numberOfContours]
    os2.usWinAscent = max(g.yMax for g in drawn)
    os2.usWinDescent = max(0, -min(g.yMin for g in drawn))
    os2.panose.bFamilyType = 2
    os2.panose.bProportion = 9  # nearly every glyph is one em wide
    f["post"].isFixedPitch = 1
    f["post"].formatType = 2.0
    f["post"].extraNames = []
    f["post"].mapping = {}
    for t in f["cmap"].tables:
        if t.isUnicode() and 0x20 in t.cmap:
            t.cmap[0xA0] = t.cmap[0x20]
    from fontTools.ttLib import newTable
    from fontTools.ttLib.tables import ttProgram
    prep = newTable("prep")
    prep.program = ttProgram.Program()
    prep.program.fromAssembly(["PUSHW[]", "511", "SCANCTRL[]", "PUSHB[]", "4", "SCANTYPE[]"])
    f["prep"] = prep


def main(src, ref_out=None):
    f = instance(src)
    if ref_out:
        f.save(ref_out)
    gs = f.getGlyphSet()
    glyf = f["glyf"]
    cmap = f.getBestCmap()
    targets = {cmap[ord(c)] for c in TEXT if ord(c) in cmap}
    t0 = time.perf_counter()
    new = {}
    for n in sorted(targets):
        new[n] = tt(style(to_pathops(gs, n)))
    dt = time.perf_counter() - t0
    for n, g in new.items():
        glyf[n] = g
        g.recalcBounds(glyf)
        adv, _ = f["hmtx"][n]
        f["hmtx"][n] = (adv, g.xMin if g.numberOfContours else 0)
    if "gvar" in f:
        del f["gvar"]
    rename(f)
    f.save(OUT / f"{PS}.ttf")
    w = TTFont(OUT / f"{PS}.ttf")
    w.flavor = "woff2"
    w.save(OUT / f"{PS}.woff2")
    print(f"styled {len(new)} glyphs in {dt:.2f} s ({dt / len(new) * 1000:.0f} ms per glyph)")


if __name__ == "__main__":
    main(*sys.argv[1:3])
