"""Han v4: calligraphic stroke skeletons simplified by rule into a UI face.

Every rule reads only the skeleton (stroke centre lines and their geometry),
never which character it is, so it runs the same on any character. Order:

1. gestures   hooks and dots get one standard length and a 45-degree angle
2. axes       near-horizontal and near-vertical segments become exactly 0 / 90
3. sweeps     撇 and 捺 become one gentle curve (a single quadratic)
4. spacing    free parallel strokes move toward even gaps
5. components side-by-side and stacked components get sans proportions: each
              fills its share of the box, shares follow stroke counts
6. frame      one em box for every character, squarer, with counters opened
              by a per-axis power warp (axis-aligned lines stay aligned)

The normalised skeleton is what the compact file stores; `brush` draws it
with a near-monoline UI brush whose weight drops for dense characters.
"""

import math

import pathops
import skia

import hanstroke as hs
from skeleton import _skia_to_pathops, tt_glyph

# ---- rule parameters (tuned by eye against Noto Sans TC, rounds in the PR) ----
AXIS_TOL = 16  # degrees from 0 / 90 that snap
HOOK_LEN, DOT_LEN = 70, 95
SWEEP_BULGE = (0.04, 0.10)  # min, max bulge of 撇/捺 as a share of length
EVEN_MAX_MOVE = 50
FRAME_HALF = 392  # half size of the face box (em units)
FRAME_CENTRE = (500, 380)
GAMMA = 0.82  # < 1 pushes inner strokes outward: bigger counters
ASPECT_KEEP = 0.6  # how much of a wide or tall character's aspect survives

WBASE = 90  # stroke width of a sparse character (Pip's stem is 104; CJK sits lighter)
H_CONTRAST = 0.9
L_REF, END_COST, W_MIN = 3300, 120, 0.62


def _seglen(a, b):
    return math.dist(a, b)


# ------------------------------------------------------------------ 1 gestures
def gestures(s):
    k, parts = hs.kind(s)
    s = [tuple(p) for p in s]
    if k == "hook" and len(s) >= 3:
        a, b = s[-2], s[-1]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        q = round(ang / (math.pi / 4)) * (math.pi / 4)
        s[-1] = (a[0] + HOOK_LEN * math.cos(q), a[1] + HOOK_LEN * math.sin(q))
    elif k == "dot":
        a, b = s[0], s[-1]
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        q = round((ang - math.pi / 4) / (math.pi / 2)) * (math.pi / 2) + math.pi / 4  # nearest diagonal
        h = DOT_LEN / 2
        s = [(mid[0] - h * math.cos(q), mid[1] - h * math.sin(q)), (mid[0] + h * math.cos(q), mid[1] + h * math.sin(q))]
    return s


# ------------------------------------------------------------------ 2 axes
def axes(s):
    s = [list(p) for p in s]
    for i in range(len(s) - 1):
        a, b = s[i], s[i + 1]
        ang = abs(math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))) % 180
        if min(ang, 180 - ang) <= AXIS_TOL:
            y = (a[1] + b[1]) / 2
            a[1] = b[1] = y
        elif abs(ang - 90) <= AXIS_TOL:
            x = (a[0] + b[0]) / 2
            a[0] = b[0] = x
    return [tuple(p) for p in s]


# ------------------------------------------------------------------ 3 sweeps
def sweeps(s):
    k, _ = hs.kind(s)
    if k not in ("pie", "na") or len(s) < 2:
        return s
    a, b = s[0], s[-1]
    L = _seglen(a, b) or 1
    nx, ny = -(b[1] - a[1]) / L, (b[0] - a[0]) / L
    dev = sum(((p[0] - a[0]) * nx + (p[1] - a[1]) * ny) for p in s[1:-1]) / max(1, len(s) - 2)
    sign = 1 if dev >= 0 else -1
    bulge = sign * max(SWEEP_BULGE[0] * L, min(SWEEP_BULGE[1] * L, abs(dev) * 1.5))
    c = ((a[0] + b[0]) / 2 + nx * bulge * 2, (a[1] + b[1]) / 2 + ny * bulge * 2)
    out = []
    for i in range(6):
        t = i / 5
        out.append(((1 - t) ** 2 * a[0] + 2 * t * (1 - t) * c[0] + t * t * b[0],
                    (1 - t) ** 2 * a[1] + 2 * t * (1 - t) * c[1] + t * t * b[1]))
    return out


# ------------------------------------------------------------------ 4 spacing
def _segments(strokes):
    """Every axis-aligned segment: (stroke, i, axis, pos, lo, hi)."""
    out = []
    for si, s in enumerate(strokes):
        for i in range(len(s) - 1):
            a, b = s[i], s[i + 1]
            if abs(a[1] - b[1]) < 0.5 and abs(a[0] - b[0]) > 1:
                out.append((si, i, "h", a[1], min(a[0], b[0]), max(a[0], b[0])))
            elif abs(a[0] - b[0]) < 0.5 and abs(a[1] - b[1]) > 1:
                out.append((si, i, "v", a[0], min(a[1], b[1]), max(a[1], b[1])))
    return out


def _touches(strokes, si):
    """Another stroke starts or ends on stroke si: it carries structure."""
    s = strokes[si]
    for sj, t in enumerate(strokes):
        if sj == si:
            continue
        for e in (t[0], t[-1]):
            for a, b in zip(s, s[1:]):
                L2 = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 or 1
                u = max(0, min(1, ((e[0] - a[0]) * (b[0] - a[0]) + (e[1] - a[1]) * (b[1] - a[1])) / L2))
                if math.dist((a[0] + u * (b[0] - a[0]), a[1] + u * (b[1] - a[1])), e) < 30:
                    return True
    return False


def spacing(strokes):
    strokes = [list(s) for s in strokes]
    free = {si for si, s in enumerate(strokes) if len(s) == 2 and not _touches(strokes, si)}
    for axis in ("h", "v"):
        segs = [x for x in _segments(strokes) if x[2] == axis]
        pos = {(x[0], x[1]): x[3] for x in segs}
        for _ in range(3):
            for si, i, _, p0, lo, hi in segs:
                if si not in free:
                    continue
                p = pos[(si, i)]
                over = [x for x in segs if (x[0], x[1]) != (si, i) and min(hi, x[5]) - max(lo, x[4]) > 0.5 * min(hi - lo, x[5] - x[4])]
                above = [pos[(x[0], x[1])] for x in over if pos[(x[0], x[1])] < p]
                below = [pos[(x[0], x[1])] for x in over if pos[(x[0], x[1])] > p]
                if not above or not below:
                    continue
                mid = (max(above) + min(below)) / 2
                pos[(si, i)] = max(p0 - EVEN_MAX_MOVE, min(p0 + EVEN_MAX_MOVE, p + (mid - p) * 0.6))
        for (si, i), p in pos.items():
            if si in free:
                strokes[si] = [(x, p) if axis == "h" else (p, y) for x, y in strokes[si]]
    return [[tuple(p) for p in s] for s in strokes]


# ------------------------------------------------------------------ 5 frame
def frame(strokes):
    xs = [p[0] for s in strokes for p in s]
    ys = [p[1] for s in strokes for p in s]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    w, h = max(x1 - x0, 1), max(y1 - y0, 1)
    a = w / h
    hx = hy = FRAME_HALF
    if a > 1:
        hy = FRAME_HALF * a ** -ASPECT_KEEP
    else:
        hx = FRAME_HALF * a ** ASPECT_KEEP
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2

    def warp(v, c, half_src, half_dst):
        u = (v - c) / (half_src or 1)
        u = math.copysign(abs(u) ** GAMMA, u)
        return u * half_dst

    return [[(FRAME_CENTRE[0] + warp(x, cx, w / 2, hx), FRAME_CENTRE[1] + warp(y, cy, h / 2, hy)) for x, y in s]
            for s in strokes]


# ------------------------------------------------------------------ 5 components
SPLIT_OPS = {"⿰": 0, "⿲": 0, "⿱": 1, "⿳": 1}  # axis along which parts sit
EQUALISE = 0.5  # part share: half its own extent, half an equal split (sans parts are more even than Kai)
SHARE_MIN = 0.26
GAP = 0.06  # gap between parts, share of the box
STRETCH = 1.35  # a part may stretch at most this much more on one axis


def _box(strokes):
    xs = [p[0] for s in strokes for p in s]
    ys = [p[1] for s in strokes for p in s]
    return min(xs), min(ys), max(xs), max(ys)


def components(strokes, entry):
    """Give each top-level part of a side-by-side or stacked character its
    sans share of the box (Kai squeezes left parts and lifts top parts)."""
    if not entry or not entry.get("decomposition"):
        return strokes
    try:
        tree, _ = hs.parse_ids(entry["decomposition"])
    except IndexError:
        return strokes
    if tree.get("op") not in SPLIT_OPS:
        return strokes
    ax = SPLIT_OPS[tree["op"]]
    m = entry.get("matches") or []
    groups = {}
    for i, s in enumerate(strokes):
        g = m[i][0] if i < len(m) and m[i] else None
        groups.setdefault(g, []).append(i)
    if None in groups:  # unmatched strokes join the nearest part
        for i in groups.pop(None):
            c = sum(p[ax] for p in strokes[i]) / len(strokes[i])
            best = min(groups, key=lambda g: abs(c - sum(p[ax] for j in groups[g] for p in strokes[j]) / sum(len(strokes[j]) for j in groups[g]))) if groups else 0
            groups.setdefault(best, []).append(i)
    keys = sorted(groups)
    if len(keys) < 2:
        return strokes
    x0, y0, x1, y1 = _box(strokes)
    lo, hi = (x0, x1) if ax == 0 else (y1, y0)  # y runs downward in reading order
    own = []
    for k in keys:
        bx0, by0, bx1, by1 = _box([strokes[i] for i in groups[k]])
        own.append((bx1 - bx0) if ax == 0 else (by1 - by0))
    w = [max(SHARE_MIN, (1 - EQUALISE) * o / sum(own) + EQUALISE / len(keys)) for o in own]
    tot = sum(w)
    span = hi - lo
    gap = GAP * span
    usable = span - gap * (len(keys) - 1)
    out = [list(s) for s in strokes]
    pos = lo
    across = (y1 - y0) if ax == 0 else (x1 - x0)
    for k, wk in zip(keys, w):
        size = usable * wk / tot
        a, b = pos, pos + size
        pos = b + gap
        idx = groups[k]
        bx0, by0, bx1, by1 = _box([strokes[i] for i in idx])
        along_own = (bx1 - bx0) if ax == 0 else (by1 - by0)
        across_own = (by1 - by0) if ax == 0 else (bx1 - bx0)
        s_along = abs(size) / max(along_own, 1)
        # across the split a part keeps its own place and grows at most like
        # it grows along (never shrinks), and never past the character's extent
        s_across = min(max(1.0, s_along), STRETCH, across / max(across_own, 1))
        s_along = min(s_along, s_across * STRETCH)
        cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2
        mid = (a + b) / 2
        for i in idx:
            if ax == 0:
                out[i] = [(mid + (x - cx) * s_along, cy + (y - cy) * s_across) for x, y in strokes[i]]
            else:
                out[i] = [(cx + (x - cx) * s_across, mid + (y - cy) * s_along) for x, y in strokes[i]]
    return [[tuple(p) for p in s] for s in out]


def normalise(strokes, entry=None):
    strokes = [axes(gestures(s)) for s in strokes]
    strokes = [sweeps(s) for s in strokes]
    strokes = components(strokes, entry)
    strokes = spacing(strokes)
    return frame(strokes)


# ------------------------------------------------------------------ brush
def brush(strokes):
    total = sum(hs.length(s) for s in strokes) + END_COST * len(strokes)
    W = WBASE * max(W_MIN, min(1.0, (L_REF / total) ** 0.5))
    out = pathops.Path()
    for s in strokes:
        k, parts = hs.kind(s)
        curved = k in ("pie", "na") and len(s) > 2
        pieces = []
        if curved:
            sp = skia.Path()
            pts = hs.catmull(s)
            sp.moveTo(*pts[0])
            for p in pts[1:]:
                sp.lineTo(*p)
            pieces.append((sp, W))
        else:
            for a, b in zip(s, s[1:]):
                sp = skia.Path()
                sp.moveTo(*a)
                sp.lineTo(*b)
                horiz = abs(a[1] - b[1]) < 0.5
                pieces.append((sp, W * (H_CONTRAST if horiz else 1.0)))
        for sp, w in pieces:
            paint = skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=w,
                               StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
            o = skia.Path()
            paint.getFillPath(sp, o, None, 0.1)
            q = pathops.Path()
            _skia_to_pathops(o, q)
            q.simplify(fix_winding=True, clockwise=True)
            out = pathops.op(out, q, pathops.PathOp.UNION, fix_winding=True, clockwise=True)
    return out


def build_font(chars, family, path):
    from fontTools.fontBuilder import FontBuilder
    glyphs, metrics, cmap = {".notdef": tt_glyph(pathops.Path()), "space": tt_glyph(pathops.Path())}, \
        {".notdef": (1000, 0), "space": (500, 0)}, {32: "space"}
    for ch, strokes in chars.items():
        n = f"uni{ord(ch):04X}"
        glyphs[n] = tt_glyph(brush(strokes))
        metrics[n] = (1000, 0)
        cmap[ord(ch)] = n
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(list(glyphs))
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=880, descent=-120)
    fb.setupNameTable({"familyName": family, "styleName": "Regular"}, mac=False)
    fb.setupOS2(sTypoAscender=880, sTypoDescender=-120, usWinAscent=1000, usWinDescent=200)
    fb.setupPost()
    fb.font.save(path)
