"""Skeleton strokes to clean TrueType outlines.

Every glyph is drawn as centre-line strokes (lines, cubic curves and
elliptical arcs) plus a few filled dots. Skia expands each stroke at one fixed
width with round caps and round joins, skia-pathops merges the overlaps into
one non-overlapping outline with TrueType (clockwise) direction, and cu2qu
turns the cubics into quadratic splines. Nothing is traced or copied.
"""

import math

import pathops
import skia
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.filterPen import FilterPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

# Rounds are drawn slightly squarer than a true ellipse (handle length times
# SQUARE): softer and chunkier, closer to a game UI than a geometric circle.
SQUARE = 1.07


class Sk:
    """A glyph skeleton: open or closed centre lines plus filled dots."""

    def __init__(self):
        self.path = skia.Path()
        self.fill = skia.Path()
        self._cur = None

    # centre lines -------------------------------------------------------
    def M(self, x, y):
        self.path.moveTo(x, y)
        self._cur = (x, y)
        return self

    def L(self, *pts):
        for x, y in zip(pts[::2], pts[1::2]):
            self.path.lineTo(x, y)
            self._cur = (x, y)
        return self

    def C(self, x1, y1, x2, y2, x3, y3):
        self.path.cubicTo(x1, y1, x2, y2, x3, y3)
        self._cur = (x3, y3)
        return self

    def Z(self):
        self.path.close()
        return self

    def line(self, *pts):
        self.M(pts[0], pts[1])
        return self.L(*pts[2:])

    def arc(self, cx, cy, rx, ry, a0, a1, move=True, square=SQUARE):
        """Elliptical arc from angle a0 to a1 (degrees, counter-clockwise)."""
        n = max(1, math.ceil(abs(a1 - a0) / 90 - 1e-9))
        step = (a1 - a0) / n
        t0 = math.radians(a0)
        p = (cx + rx * math.cos(t0), cy + ry * math.sin(t0))
        if move:
            self.M(*p)
        else:
            self.L(*p)
        for i in range(n):
            ta = math.radians(a0 + step * i)
            tb = math.radians(a0 + step * (i + 1))
            k = 4 / 3 * math.tan((tb - ta) / 4) * square
            c1 = (cx + rx * (math.cos(ta) - k * math.sin(ta)), cy + ry * (math.sin(ta) + k * math.cos(ta)))
            c2 = (cx + rx * (math.cos(tb) + k * math.sin(tb)), cy + ry * (math.sin(tb) - k * math.cos(tb)))
            p3 = (cx + rx * math.cos(tb), cy + ry * math.sin(tb))
            self.C(*c1, *c2, *p3)
        return self

    def ell(self, cx, cy, rx, ry, square=SQUARE):
        self.arc(cx, cy, rx, ry, 0, 360, square=square)
        return self.Z()

    # filled shapes ------------------------------------------------------
    def dot(self, x, y, r):
        self.fill.addCircle(x, y, r)
        return self

    # placement ----------------------------------------------------------
    def add(self, other, dx=0.0, dy=0.0, sx=1.0, sy=1.0):
        """Merge another skeleton, scaled then moved. Scaling a skeleton keeps
        the stroke width, which is what lets components be reused."""
        m = skia.Matrix()
        m.setAll(sx, 0, dx, 0, sy, dy, 0, 0, 1)
        self.path.addPath(other.path, m)
        self.fill.addPath(other.fill, m)
        return self


def _skia_to_pathops(sp, out):
    pen = out.getPen()
    it = skia.Path.Iter(sp, False)
    open_ = False
    while True:
        verb, pts = it.next()
        if verb == skia.Path.kDone_Verb:
            break
        if verb == skia.Path.kMove_Verb:
            if open_:
                pen.closePath()
            pen.moveTo((pts[0].x(), pts[0].y()))
            open_ = True
        elif verb == skia.Path.kLine_Verb:
            pen.lineTo((pts[1].x(), pts[1].y()))
        elif verb == skia.Path.kQuad_Verb:
            pen.qCurveTo((pts[1].x(), pts[1].y()), (pts[2].x(), pts[2].y()))
        elif verb == skia.Path.kCubic_Verb:
            pen.curveTo((pts[1].x(), pts[1].y()), (pts[2].x(), pts[2].y()), (pts[3].x(), pts[3].y()))
        elif verb == skia.Path.kConic_Verb:
            quads = skia.Path.ConvertConicToQuads(pts[0], pts[1], pts[2], it.conicWeight(), 2)
            for i in range(1, len(quads), 2):
                pen.qCurveTo((quads[i].x(), quads[i].y()), (quads[i + 1].x(), quads[i + 1].y()))
        elif verb == skia.Path.kClose_Verb:
            pen.closePath()
            open_ = False
    if open_:
        pen.closePath()


def outline(sk, width):
    """Expand a skeleton at `width` and return one clean pathops.Path."""
    paint = skia.Paint(
        Style=skia.Paint.kStroke_Style,
        StrokeWidth=width,
        StrokeCap=skia.Paint.kRound_Cap,
        StrokeJoin=skia.Paint.kRound_Join,
        AntiAlias=True,
    )
    stroked = skia.Path()
    if sk.path.countVerbs():
        paint.getFillPath(sk.path, stroked, None, 0.05)
    stroked.addPath(sk.fill)
    p = pathops.Path()
    _skia_to_pathops(stroked, p)
    p.simplify(fix_winding=True, keep_starting_points=False, clockwise=True)
    return p


def bounds(p):
    if not len(p):
        return (0, 0, 0, 0)
    return p.bounds


class _DropDegenerate(FilterPen):
    """Drop segments whose points all round to the current point."""

    def __init__(self, out):
        super().__init__(out)
        self.cur = None

    def _same(self, pts):
        return all((round(x), round(y)) == self.cur for x, y in pts)

    def moveTo(self, pt):
        self.cur = (round(pt[0]), round(pt[1]))
        self._outPen.moveTo(pt)

    def lineTo(self, pt):
        if not self._same([pt]):
            self._outPen.lineTo(pt)
            self.cur = (round(pt[0]), round(pt[1]))

    def qCurveTo(self, *pts):
        if pts[-1] is None:
            self._outPen.qCurveTo(*pts)
            return
        # round, then drop off-curve points that repeat their neighbour
        r = [(round(x), round(y)) for x, y in pts]
        kept, prev = [], self.cur
        for q in r[:-1]:
            if q != prev:
                kept.append(q)
                prev = q
        end = r[-1]
        if kept and kept[-1] == end:
            kept.pop()
        if not kept:
            if end != self.cur:
                self._outPen.lineTo(end)
        else:
            self._outPen.qCurveTo(*kept, end)
        self.cur = end

    def curveTo(self, *pts):
        if self._same(pts):
            return
        self._outPen.curveTo(*pts)
        self.cur = (round(pts[-1][0]), round(pts[-1][1]))


def tt_glyph(p, dx=0):
    """A TrueType glyph from a pathops path, moved right by dx units."""
    tt = TTGlyphPen(None)
    pen = Cu2QuPen(_DropDegenerate(tt), max_err=0.6, reverse_direction=False)
    p.draw(TransformPen(pen, (1, 0, 0, 1, dx, 0)))
    g = tt.glyph()
    return g
