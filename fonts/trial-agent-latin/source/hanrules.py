"""Rules that turn a Han skeleton into a finished glyph.

Each rule reads only the skeleton (its strokes, their lengths, directions and
positions), never the character's identity, so it applies to any character a
future set adds. Order: layout (size and centre of gravity), optical weight,
then per-stroke width (contrast, ends) and the outline.

Grid: 1000 units, y down, the ideographic em box (0 = 880 above the
baseline, 1000 = 120 below it).
"""

import math

import pathops
import skia

from skeleton import Sk, _skia_to_pathops

STEM = 78  # reference stroke width for a character of reference density
FACE = 860  # the largest ink extent a character may have (grid units)
CENTRE = (500, 500)
L_REF = 5400  # effective length (grid units) of a character of reference density
END_COST = 150  # each stroke adds two ends, which take space like this much length

# Rule weights, tuned by eye against Noto Sans CJK TC (see the rounds in specimens/).
WEIGHT_EXP = 0.55  # stroke width ~ (L_REF / length) ** WEIGHT_EXP
WEIGHT_MIN, WEIGHT_MAX = 0.70, 1.06
H_CONTRAST = 0.84  # horizontals are this much thinner than verticals
TAPER_PIE = 0.50  # a left-falling stroke ends at this fraction of its width
SWELL_NA = 1.16  # a right-falling stroke ends this much wider
DOT_START = 0.78  # a dot starts thinner and ends full (a teardrop)
HOOK_END = 0.62  # a hook tapers to this fraction
CENTROID_BLEND = 0.5  # 0 = centre the ink box, 1 = centre the stroke centroid
SMALL_CHAR = 2600  # below this skeleton length a character keeps a smaller face


# --------------------------------------------------------------- strokes
def strokes(sk):
    """Split a skeleton into one skia.Path per stroke (subpath)."""
    out, cur = [], None
    it = skia.Path.Iter(sk.path, False)
    while True:
        verb, pts = it.next()
        if verb == skia.Path.kDone_Verb:
            break
        if verb == skia.Path.kMove_Verb:
            cur = skia.Path()
            cur.moveTo(pts[0])
            out.append(cur)
        elif verb == skia.Path.kLine_Verb:
            cur.lineTo(pts[1])
        elif verb == skia.Path.kCubic_Verb:
            cur.cubicTo(pts[1], pts[2], pts[3])
        elif verb == skia.Path.kQuad_Verb:
            cur.quadTo(pts[1], pts[2])
        elif verb == skia.Path.kClose_Verb:
            cur.close()
    return [p for p in out if p.countPoints() > 1]


def length(p):
    m = skia.PathMeasure(p, False)
    total = 0.0
    while True:
        total += m.getLength()
        if not m.nextContour():
            return total


def samples(p, n=24):
    m = skia.PathMeasure(p, False)
    L = m.getLength()
    return [m.getPosTan(L * i / n)[0] for i in range(n + 1)], L


def tangent_at(p, t):
    m = skia.PathMeasure(p, False)
    pos, tan = m.getPosTan(m.getLength() * t)
    return (tan.x(), tan.y())


def has_curve(p):
    return bool(p.getSegmentMasks() & int(skia.Path.kCubic_SegmentMask))


# --------------------------------------------------------------- rule 1: layout
def layout(sk):
    """Same visual size and centre of gravity for every character.

    The ink box is scaled so its larger side is FACE (sparse characters keep a
    smaller face, as in every CJK face, so 二 does not look bloated), then the
    character is moved so a blend of its box centre and its stroke centroid
    (length-weighted) sits at the em centre.
    """
    ss = strokes(sk)
    pts, wsum = [], 0.0
    cx = cy = 0.0
    for p in ss:
        sp, L = samples(p)
        for q in sp:
            pts.append((q.x(), q.y()))
            cx += q.x() * L / len(sp)
            cy += q.y() * L / len(sp)
        wsum += L
    fill = sk.fill.computeTightBounds()
    xs = [x for x, _ in pts] + ([fill.left(), fill.right()] if not sk.fill.isEmpty() else [])
    ys = [y for _, y in pts] + ([fill.top(), fill.bottom()] if not sk.fill.isEmpty() else [])
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    total = sum(length(p) for p in ss)
    face = FACE if total >= SMALL_CHAR else FACE * (0.9 + 0.1 * total / SMALL_CHAR)
    s = face / max(x1 - x0, y1 - y0, 1)
    s = min(s, 1.25)
    bx, by = (x0 + x1) / 2, (y0 + y1) / 2
    gx, gy = cx / wsum, cy / wsum
    mx = bx + (gx - bx) * CENTROID_BLEND
    my = by + (gy - by) * CENTROID_BLEND
    out = Sk()
    out.add(sk, dx=CENTRE[0] - mx * s, dy=CENTRE[1] - my * s, sx=s, sy=s)
    return out


# --------------------------------------------------------------- rule 2: optical weight
def weight(sk):
    """Denser characters (more stroke length in the same box) get thinner
    strokes, so every character carries about the same grey."""
    ss = strokes(sk)
    total = sum(length(p) for p in ss) + END_COST * len(ss)
    f = (L_REF / max(total, 1)) ** WEIGHT_EXP
    return STEM * max(WEIGHT_MIN, min(WEIGHT_MAX, f))


# --------------------------------------------------------------- rule 3: per-stroke width
def classify(p):
    """Name a stroke by its geometry only."""
    L = length(p)
    pts = [p.getPoint(i) for i in range(p.countPoints())]
    a, b = pts[0], pts[-1]
    dx, dy = b.x() - a.x(), b.y() - a.y()
    if not has_curve(p) and len(pts) == 2:
        if L < 190 and abs(dx) > 0.2 * L and abs(dy) > 0.2 * L:
            return "dot"
        if abs(dy) <= 0.12 * abs(dx):
            return "h"
        if abs(dx) <= 0.12 * abs(dy):
            return "v"
        if dx > 0 and dy < 0:
            return "rise"  # 提
        return "slant"
    ex, ey = tangent_at(p, 0.98)
    if has_curve(p) and ex < -0.2 and ey > 0.1:
        return "pie"  # ends falling to the left
    if has_curve(p) and ex > 0.4 and ey >= -0.05 and dx > 0 and dy > 0:
        return "na"  # ends running out to the right
    if not has_curve(p) and len(pts) >= 3:
        # a short last leg that turns back up-left is a hook
        l2 = pts[-2]
        hx, hy = b.x() - l2.x(), b.y() - l2.y()
        if math.hypot(hx, hy) < 130 and hx < 0 and hy < 0:
            return "hook"
        return "poly"
    return "curve"


def pieces(p, w0, w1, n=None, start=0.0):
    """A stroke whose width runs from w0 to w1 over [start, 1] of its length,
    as one filled outline: the centre line offset on both sides along its
    normal, closed by round ends. Returned as (outline, 0): width 0 marks a
    ready outline for stroke_union."""
    m = skia.PathMeasure(p, False)
    L = m.getLength()
    N = max(16, int(L / 8))
    left, right = [], []
    for i in range(N + 1):
        t = i / N
        pos, tan = m.getPosTan(L * t)
        k = 0.0 if t <= start else (t - start) / (1 - start)
        k = k * k * (3 - 2 * k)  # ease in and out
        r = (w0 + (w1 - w0) * k) / 2
        nx, ny = -tan.y(), tan.x()
        left.append((pos.x() + nx * r, pos.y() + ny * r))
        right.append((pos.x() - nx * r, pos.y() - ny * r))
    out = skia.Path()
    out.moveTo(*left[0])
    for q in left[1:]:
        out.lineTo(*q)
    for q in reversed(right):
        out.lineTo(*q)
    out.close()
    a = m.getPosTan(0)[0]
    b = m.getPosTan(L)[0]
    c0, c1 = skia.Path(), skia.Path()
    c0.addCircle(a.x(), a.y(), w0 / 2)
    c1.addCircle(b.x(), b.y(), w1 / 2)
    return [(out, 0), (c0, 0), (c1, 0)]


def split_poly(p):
    """A polyline as (segment, is_horizontal) pairs."""
    pts = [p.getPoint(i) for i in range(p.countPoints())]
    out = []
    for a, b in zip(pts, pts[1:]):
        s = skia.Path()
        s.moveTo(a)
        s.lineTo(b)
        out.append((s, abs(b.y() - a.y()) <= 0.12 * abs(b.x() - a.x())))
    return out


def widths(sk, w):
    """Every stroke as (path, width) pieces."""
    out = []
    for p in strokes(sk):
        kind = classify(p)
        if kind == "h":
            out.append((p, w * H_CONTRAST))
        elif kind in ("v", "slant", "rise"):
            out.append((p, w))
        elif kind == "dot":
            out += pieces(p, w * DOT_START, w * 1.05)
        elif kind == "pie":
            out += pieces(p, w, w * TAPER_PIE, start=0.4)
        elif kind == "na":
            out += pieces(p, w * 0.9, w * SWELL_NA, start=0.3)
        elif kind == "hook":
            # the turn keeps one width (a mixed width shows a knob at the
            # corner); only the hook itself tapers
            pts = [p.getPoint(i) for i in range(p.countPoints())]
            body = skia.Path()
            body.moveTo(pts[0])
            for q in pts[1:-1]:
                body.lineTo(q)
            out.append((body, w))
            leg = skia.Path()
            leg.moveTo(pts[-2])
            leg.lineTo(pts[-1])
            out += pieces(leg, w, w * HOOK_END)
        elif kind == "poly":
            out.append((p, w))
        else:
            out.append((p, w))
    return out


# --------------------------------------------------------------- outline
def stroke_union(parts, fill=None):
    """Union every part. Each part is cleaned on its own first, so contour
    direction never cancels ink where parts overlap."""
    ops = []
    for p, w in parts:
        if w == 0:
            o = p
        else:
            paint = skia.Paint(
                Style=skia.Paint.kStroke_Style, StrokeWidth=w,
                StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join,
            )
            o = skia.Path()
            paint.getFillPath(p, o, None, 0.05)
        q = pathops.Path()
        _skia_to_pathops(o, q)
        q.simplify(fix_winding=True, clockwise=True)
        ops.append(q)
    if fill is not None and not fill.isEmpty():
        q = pathops.Path()
        _skia_to_pathops(fill, q)
        q.simplify(fix_winding=True, clockwise=True)
        ops.append(q)
    out = pathops.Path()
    for q in ops:
        out = pathops.op(out, q, pathops.PathOp.UNION, fix_winding=True, clockwise=True)
    return out


# --------------------------------------------------------------- rule 4: even counters
EVEN_STEPS = 3
EVEN_MAX_MOVE = 60  # never move a stroke further than this (grid units)


def _line(p):
    pts = [p.getPoint(i) for i in range(p.countPoints())]
    return pts[0], pts[-1]


def even_counters(sk):
    """Free parallel strokes (a plain horizontal or vertical that nothing
    hangs from) move toward the middle of their neighbours, so the white
    spaces between parallel strokes even out. Turns, curves and strokes that
    carry another stroke stay fixed and act as anchors."""
    ss = strokes(sk)
    kinds = [classify(p) for p in ss]
    ends = []
    for j, p in enumerate(ss):
        a, b = _line(p)
        ends += [(j, a), (j, b)]

    def carries(i):
        a, b = _line(ss[i])
        ax, ay, bx, by = a.x(), a.y(), b.x(), b.y()
        L2 = (bx - ax) ** 2 + (by - ay) ** 2 or 1
        for j, e in ends:
            if j == i:
                continue
            t = max(0, min(1, ((e.x() - ax) * (bx - ax) + (e.y() - ay) * (by - ay)) / L2))
            if math.hypot(ax + t * (bx - ax) - e.x(), ay + t * (by - ay) - e.y()) < 30:
                return True
        return False

    for axis in ("h", "v"):
        items = []  # [stroke index or None, position, span lo, span hi, free]
        for i, (p, k) in enumerate(zip(ss, kinds)):
            if k == axis:
                a, b = _line(p)
                pos = a.y() if axis == "h" else a.x()
                lo, hi = sorted((a.x(), b.x()) if axis == "h" else (a.y(), b.y()))
                items.append([i, pos, lo, hi, not carries(i)])
            elif k in ("poly", "hook"):
                for seg, horiz in split_poly(p):
                    a, b = _line(seg)
                    if (axis == "h") == horiz and (horiz or abs(b.x() - a.x()) <= 0.12 * abs(b.y() - a.y())):
                        pos = a.y() if axis == "h" else a.x()
                        lo, hi = sorted((a.x(), b.x()) if axis == "h" else (a.y(), b.y()))
                        items.append([None, pos, lo, hi, False])
        start = {id(it): it[1] for it in items}
        for _ in range(EVEN_STEPS):
            for it in items:
                if not it[4]:
                    continue
                over = [o for o in items if o is not it and min(it[3], o[3]) - max(it[2], o[2]) > 0.6 * min(it[3] - it[2], o[3] - o[2])]
                above = [o[1] for o in over if o[1] < it[1]]
                below = [o[1] for o in over if o[1] > it[1]]
                if not above or not below:
                    continue
                mid = (max(above) + min(below)) / 2
                target = it[1] + (mid - it[1]) * 0.6
                lim = start[id(it)]
                it[1] = max(lim - EVEN_MAX_MOVE, min(lim + EVEN_MAX_MOVE, target))
        for it in items:
            if it[4] and abs(it[1] - start[id(it)]) > 0.5:
                d = it[1] - start[id(it)]
                m = skia.Matrix()
                if axis == "h":
                    m.setTranslate(0, d)
                else:
                    m.setTranslate(d, 0)
                ss[it[0]].transform(m)
    out = Sk()
    for p in ss:
        out.path.addPath(p)
    out.fill = sk.fill
    return out


def finish(sk):
    """Skeleton (grid) -> clean outline (font units)."""
    sk = even_counters(sk)
    sk = layout(sk)
    w = weight(sk)
    parts = widths(sk, w)
    flip = skia.Matrix()
    flip.setAll(1, 0, 0, 0, -1, 880, 0, 0, 1)
    def moved(p):
        q = skia.Path(p)
        q.transform(flip)
        return q

    return stroke_union([(moved(p), wd) for p, wd in parts], moved(sk.fill))
