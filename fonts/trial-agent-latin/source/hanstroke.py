"""Han v3: standard structure as stroke skeletons, our own brush, compact storage.

    python hanstroke.py <mmh-dir> <NotoSansTC[wght].ttf> <out-dir>

1. Structure. Stroke centre lines (medians), stroke order and the component
   tree come from Make Me a Hanzi (graphics.txt: Arphic Public License,
   derived from Arphic PL UKai and KaitiM; dictionary.txt: LGPL 3). The
   medians keep the standard structure and Kai proportions; brush entry and
   exit flicks are removed and nearly straight parts made straight. (Snapping
   the medians onto Source Han's medial axis was tried and dropped: it broke
   strokes where Kai and Sans positions differ.) Noto Sans TC is only the
   comparison reference.
2. Brush. Each stroke is re-drawn by a parametric brush that knows the stroke
   type (橫 豎 撇 捺 點 提 折 鉤), read from the stroke's geometry alone.
   BRUSHES holds the variants.
3. Storage. Characters are encoded as component placements plus stroke
   skeletons; a component used by more than one character (same component,
   same slot) is stored once. The specimen fonts are built from the decoded
   bytes, so they prove the round trip.
"""

import json
import math
from pathlib import Path

import brotli
import numpy as np
import pathops
import skia
from fontTools import subset
from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

from skeleton import _skia_to_pathops, tt_glyph

HAN = "開始遊戲勝利失敗分數等級金幣麻將大老二你好香港永"
REF_WEIGHT = 500


# ----------------------------------------------------------------- data
def load_mmh(d, chars=None):
    g, dic = {}, {}
    for line in open(Path(d) / "graphics.txt", encoding="utf8"):
        j = json.loads(line)
        if chars is None or j["character"] in chars:
            g[j["character"]] = j["medians"]
    for line in open(Path(d) / "dictionary.txt", encoding="utf8"):
        j = json.loads(line)
        if chars is None or j["character"] in chars:
            dic[j["character"]] = j
    return g, dic


def mmh_to_em(pts):
    """Make Me a Hanzi's 1024 box (y up, 900 top) to our em (880 top, -120 bottom)."""
    return [(x * 1000 / 1024, (y + 124) * 1000 / 1024 - 120) for x, y in pts]


def resample(pts, step=8.0):
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        L = math.dist(a, b)
        n = max(1, int(L / step))
        for i in range(1, n + 1):
            t = i / n
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return out


def rdp(pts, eps):
    if len(pts) < 3:
        return list(pts)
    a, b = np.array(pts[0]), np.array(pts[-1])
    ab = b - a
    n = np.linalg.norm(ab) or 1.0
    d = [abs(ab[0] * (p[1] - a[1]) - ab[1] * (p[0] - a[0])) / n for p in pts[1:-1]]
    i = int(np.argmax(d)) + 1
    if d[i - 1] > eps:
        return rdp(pts[: i + 1], eps)[:-1] + rdp(pts[i:], eps)
    return [pts[0], pts[-1]]


# ----------------------------------------------------------------- reference
def noto_instance(src, text):
    f = TTFont(src)
    opt = subset.Options()
    opt.layout_features = []
    opt.hinting = False
    opt.notdef_outline = True
    s = subset.Subsetter(opt)
    s.populate(text=text)
    s.subset(f)
    return instancer.instantiateVariableFont(f, {"wght": REF_WEIGHT}, inplace=False)


def _turn(a, b, c):
    v1 = (b[0] - a[0], b[1] - a[1])
    v2 = (c[0] - b[0], c[1] - b[1])
    n1, n2 = math.hypot(*v1), math.hypot(*v2)
    if n1 < 1e-6 or n2 < 1e-6:
        return 0.0
    return math.degrees(math.acos(max(-1, min(1, (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)))))


ENTRY_FLICK = 60  # a sharp first leg shorter than this is a Kai brush entry, not structure
EXIT_FLICK = 45  # same at the end (real hooks are longer)
STRAIGHT = 14  # a part that deviates less than this from its chord is a straight line


def rdp_idx(pts, eps, lo=0, hi=None):
    """Indices kept by Ramer-Douglas-Peucker."""
    hi = len(pts) - 1 if hi is None else hi
    if hi - lo < 2:
        return [lo, hi]
    a, b = pts[lo], pts[hi]
    n = math.dist(a, b) or 1
    best, bi = -1, lo
    for i in range(lo + 1, hi):
        p = pts[i]
        d = abs((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])) / n
        if d > best:
            best, bi = d, i
    if best > eps:
        return rdp_idx(pts, eps, lo, bi)[:-1] + rdp_idx(pts, eps, bi, hi)
    return [lo, hi]


def fit_line(pts):
    """Least-squares line (point, unit direction), refit without outliers."""
    P = np.array(pts, dtype=float)
    for _ in range(2):
        c = P.mean(axis=0)
        u = np.linalg.svd(P - c)[2][0]
        r = np.abs((P - c) @ np.array([-u[1], u[0]]))
        keep = r < max(8.0, np.percentile(r, 70))
        if keep.sum() >= 2:
            P = P[keep]
    c = P.mean(axis=0)
    u = np.linalg.svd(P - c)[2][0]
    return c, u


def _intersect(c1, u1, c2, u2):
    m = np.array([u1, -u2]).T
    if abs(np.linalg.det(m)) < 1e-3:
        return None
    t = np.linalg.solve(m, c2 - c1)
    return c1 + u1 * t[0]


def clean(pts, valid=None):
    """Turn a median into a skeleton.

    The line is cut at its turns (coarse simplification); a part that is
    nearly straight becomes a straight line fitted to its snapped points (so
    a horizontal follows Source Han's horizontal exactly), a curved part is
    kept, lightly simplified. A short first or last part that turns sharply
    is a Kai brush entry or exit flick and is dropped."""
    if valid is None:
        valid = [True] * len(pts)
    idx = rdp_idx(pts, 12.0)
    parts = []
    for i, j in zip(idx, idx[1:]):
        seg = pts[i:j + 1]
        a, b = seg[0], seg[-1]
        n = math.dist(a, b) or 1
        dev = max(abs((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])) / n for p in seg)
        if dev < max(STRAIGHT, 0.06 * n):
            good = [p for p, v in zip(seg, valid[i:j + 1]) if v] or seg
            if len(good) >= 2:
                c, u = fit_line(good)
                ends = [c + u * float(np.dot(np.array(e) - c, u)) for e in (a, b)]
                parts.append(("line", (c, u), [tuple(ends[0]), tuple(ends[1])]))
                continue
        parts.append(("curve", None, [pts[k] for k in rdp_idx(seg, 4.0)]))
    # merge consecutive pieces that continue in the same direction
    def plen(p):
        return length(p[2])
    if len(parts) >= 2 and plen(parts[0]) < ENTRY_FLICK and _turn(parts[0][2][0], parts[0][2][-1], parts[1][2][-1]) > 35:
        parts = parts[1:]
    if len(parts) >= 2 and plen(parts[-1]) < EXIT_FLICK and _turn(parts[-2][2][0], parts[-1][2][0], parts[-1][2][-1]) > 35:
        parts = parts[:-1]
    out = []
    for k, (typ, line, P) in enumerate(parts):
        P = list(P)
        if out:
            prev = parts[k - 1]
            if typ == "line" and prev[0] == "line":
                x = _intersect(np.array(prev[1][0]), np.array(prev[1][1]), np.array(line[0]), np.array(line[1]))
                if x is not None and math.dist(tuple(x), P[0]) < 40:
                    out[-1] = tuple(x)
            P = P[1:]
        out += P
    return rdp(out, 2.0) if len(out) > 2 else out


def raw_skeletons(mmh_dir, chars=None):
    """One cleaned centre line per stroke, from the stroke data."""
    g, dic = load_mmh(mmh_dir, chars)
    return {c: [clean(resample(mmh_to_em(m))) for m in g[c]] for c in g}, dic


# ----------------------------------------------------------------- components
OPS = {"⿰": "LR", "⿱": "TB", "⿲": "LMR", "⿳": "TMB", "⿴": "OI", "⿵": "OI", "⿶": "OI",
       "⿷": "OI", "⿸": "OI", "⿹": "OI", "⿺": "OI", "⿻": "XX"}


def parse_ids(s, i=0):
    c = s[i]
    if c in OPS:
        n = len(OPS[c])
        kids, j = [], i + 1
        for _ in range(n):
            k, j = parse_ids(s, j)
            kids.append(k)
        return {"op": c, "kids": kids}, j
    return {"char": c}, i + 1


def nodes(tree, path=(), slot="W"):
    yield path, tree, slot
    if "kids" in tree:
        for i, k in enumerate(tree["kids"]):
            yield from nodes(k, path + (i,), OPS[tree["op"]][i])


def component_keys(ch, dic, nstrokes):
    """(key, path, stroke indices) for every named component of ch with two
    or more strokes. key = (component, slot)."""
    d = dic.get(ch)
    if not d or not d.get("decomposition") or d["decomposition"] in ("？",):
        return []
    try:
        tree, _ = parse_ids(d["decomposition"])
    except IndexError:
        return []
    m = d.get("matches") or []
    out = []
    for path, node, slot in nodes(tree):
        if not path or "char" not in node or node["char"] in "？":
            continue
        idx = [i for i in range(min(nstrokes, len(m))) if m[i] is not None and tuple(m[i][: len(path)]) == path]
        if len(idx) >= 2:
            out.append(((node["char"], slot), path, idx))
    return out


# ----------------------------------------------------------------- encoding
def zz(v):
    return (v << 1) ^ (v >> 31)


def varint(n, out):
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return


def put_strokes(strokes, box, out):
    x0, y0, x1, y1 = box
    sx, sy = max(x1 - x0, 1e-6), max(y1 - y0, 1e-6)
    varint(len(strokes), out)
    for s in strokes:
        varint(len(s), out)
        px = py = 0
        for x, y in s:
            qx = round((x - x0) / sx * 255)
            qy = round((y - y0) / sy * 255)
            varint(zz(qx - px), out)
            varint(zz(qy - py), out)
            px, py = qx, qy


def bbox(strokes):
    xs = [x for s in strokes for x, _ in s]
    ys = [y for s in strokes for _, y in s]
    return min(xs), min(ys), max(xs), max(ys)


EM_BOX = (0.0, -120.0, 1000.0, 880.0)


def qbox(b):
    """A placement box, quantised to 1000/255-unit steps on the em."""
    return tuple(max(0, min(255, round((v - o) / 1000 * 255))) for v, o in zip(b, (0, -120, 0, -120)))


def encode(skel, dic, share=True):
    """Bytes for every character in skel. Shared components (same component in
    the same slot, used by two or more characters) are stored once."""
    keys = {ch: component_keys(ch, dic, len(s)) for ch, s in skel.items()}
    count = {}
    for ch, ks in keys.items():
        for k, _, _ in ks:
            count[k] = count.get(k, 0) + 1
    shared = {k for k, n in count.items() if n >= 2} if share else set()
    lib, lib_ids, plan = [], {}, {}
    for ch in skel:
        used, places = set(), []
        # largest shared components first; skip ones inside a chosen one
        for k, path, idx in sorted(keys[ch], key=lambda t: -len(t[2])):
            if k in shared and not used & set(idx):
                if k not in lib_ids:
                    sts = [skel[ch][i] for i in idx]
                    lib_ids[k] = len(lib)
                    lib.append((k, sts, bbox(sts)))
                places.append((lib_ids[k], idx))
                used |= set(idx)
        plan[ch] = (places, [i for i in range(len(skel[ch])) if i not in used])
    out = bytearray(b"PIPS")
    varint(len(lib), out)
    for _, sts, b in lib:
        put_strokes(sts, b, out)
    varint(len(plan), out)
    for ch, (places, loose) in plan.items():
        varint(ord(ch), out)
        # stroke order: a list of (placement number or 255 loose, index) is
        # not needed for drawing, so it is not stored
        varint(len(places), out)
        for lid, idx in places:
            varint(lid, out)
            out += bytes(qbox(bbox([skel[ch][i] for i in idx])))
        put_strokes([skel[ch][i] for i in loose], EM_BOX, out)
    return bytes(out), lib, plan


def get_varint(b, i):
    n = s = 0
    while True:
        c = b[i]
        i += 1
        n |= (c & 0x7F) << s
        s += 7
        if not c & 0x80:
            return n, i


def unzz(v):
    return (v >> 1) ^ -(v & 1)


def get_strokes(b, i, box):
    x0, y0, x1, y1 = box
    sx, sy = x1 - x0, y1 - y0
    n, i = get_varint(b, i)
    out = []
    for _ in range(n):
        k, i = get_varint(b, i)
        px = py = 0
        s = []
        for _ in range(k):
            dx, i = get_varint(b, i)
            dy, i = get_varint(b, i)
            px += unzz(dx)
            py += unzz(dy)
            s.append((px, py))
        out.append(s)
    # return normalised points; the caller maps them into a box
    return [[(x0 + x / 255 * sx, y0 + y / 255 * sy) for x, y in s] for s in out], i


def decode(b):
    assert b[:4] == b"PIPS"
    i = 4
    n, i = get_varint(b, i)
    lib = []
    for _ in range(n):
        sts, i = get_strokes(b, i, (0, 0, 1, 1))
        lib.append(sts)
    m, i = get_varint(b, i)
    chars = {}
    for _ in range(m):
        cp, i = get_varint(b, i)
        k, i = get_varint(b, i)
        strokes = []
        for _ in range(k):
            lid, i = get_varint(b, i)
            q = b[i:i + 4]
            i += 4
            x0, y0, x1, y1 = (q[0] / 255 * 1000, q[1] / 255 * 1000 - 120, q[2] / 255 * 1000, q[3] / 255 * 1000 - 120)
            strokes += [[(x0 + x * (x1 - x0), y0 + y * (y1 - y0)) for x, y in s] for s in lib[lid]]
        loose, i = get_strokes(b, i, EM_BOX)
        chars[chr(cp)] = strokes + loose
    return chars


# ----------------------------------------------------------------- stroke types
def split_corners(pts, angle=50):
    """Split a centre line at sharp turns (折)."""
    parts, cur = [], [pts[0]]
    for a, b, c in zip(pts, pts[1:], pts[2:]):
        cur.append(b)
        v1 = (b[0] - a[0], b[1] - a[1])
        v2 = (c[0] - b[0], c[1] - b[1])
        n1, n2 = math.hypot(*v1), math.hypot(*v2)
        if n1 > 1e-6 and n2 > 1e-6:
            cosang = (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)
            if cosang < math.cos(math.radians(angle)):
                parts.append(cur)
                cur = [b]
    cur.append(pts[-1])
    parts.append(cur)
    return [p for p in parts if len(p) >= 2]


def length(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def kind(pts):
    """Stroke type from geometry alone (y up)."""
    parts = split_corners(pts)
    L = length(pts)
    if len(parts) > 1:
        last = parts[-1]
        if length(last) < min(150, 0.3 * L):
            return "hook", parts
        return "turn", parts
    a, b = pts[0], pts[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    if L < 150:
        return "dot", parts
    if abs(dy) <= 0.27 * abs(dx):
        return "h", parts
    if abs(dx) <= 0.27 * abs(dy):
        return "v", parts
    if dy < 0 and dx < 0:
        return "pie", parts
    if dy < 0 and dx > 0:
        return "na", parts
    if dy > 0 and dx > 0:
        return "ti", parts
    return "pie", parts


# ----------------------------------------------------------------- brush
BRUSHES = {
    # soft round pebble: low contrast, round ends, gentle taper and swell
    "pebble": dict(W=96, hc=0.84, cap=2.0, press=1.0, pie_end=0.55, na_end=1.22, na_tip=1.0,
                   dot=(0.8, 1.12), ti_end=0.6, hook_end=0.6),
    # pop brush: higher contrast, a press at the start of every stroke,
    # sharper sweeps, a flared 捺: calligraphy simplified into a game logo hand
    "pop": dict(W=100, hc=0.66, cap=2.0, press=1.22, pie_end=0.32, na_end=1.42, na_tip=0.75,
                dot=(0.65, 1.25), ti_end=0.35, hook_end=0.35),
    # chunky block: heavy, squarish soft ends (superellipse), barely any taper
    "block": dict(W=108, hc=0.92, cap=4.5, press=1.0, pie_end=0.85, na_end=1.08, na_tip=1.0,
                  dot=(0.95, 1.05), ti_end=0.85, hook_end=0.8),
}

L_REF = 5600
END_COST = 150


def catmull(pts, step=5.0):
    """A smooth curve through the points (centripetal-free Catmull-Rom)."""
    if len(pts) < 3:
        return resample(pts, step)
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = [pts[0]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        n = max(2, int(math.dist(p1, p2) / step))
        for k in range(1, n + 1):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    return out


def smoothstep(a, b, t):
    x = max(0.0, min(1.0, (t - a) / (b - a)))
    return x * x * (3 - 2 * x)


def profile(k, t, piece_horizontal, B, W):
    """Width at t (0..1 along the whole stroke) for stroke type k."""
    press = 1 + (B["press"] - 1) * math.exp(-t / 0.07)
    if k == "h" or (k in ("turn", "hook") and piece_horizontal):
        return W * B["hc"] * press
    if k == "v" or k in ("turn", "hook"):
        return W * press
    if k == "pie":
        return W * press * (1 + (B["pie_end"] - 1) * smoothstep(0.3, 1.0, t))
    if k == "na":
        w = W * (0.85 + (B["na_end"] - 0.85) * smoothstep(0.2, 0.85, t))
        return w * (1 + (B["na_tip"] - 1) * smoothstep(0.85, 1.0, t))
    if k == "dot":
        d0, d1 = B["dot"]
        return W * (d0 + (d1 - d0) * t)
    if k == "ti":
        return W * press * (1 + (B["ti_end"] - 1) * t)
    return W


def cap(c, tangent, r, n, sign):
    """Half superellipse of radius r at point c, facing along +tangent (sign 1)
    or -tangent (sign -1). n = 2 is a circle; larger n is squarer."""
    tx, ty = tangent
    nx, ny = -ty, tx
    pts = []
    for i in range(17):
        a = -math.pi / 2 + math.pi * i / 16
        ca, sa = math.cos(a), math.sin(a)
        u = math.copysign(abs(ca) ** (2 / n), ca) * r * sign
        v = math.copysign(abs(sa) ** (2 / n), sa) * r * sign
        pts.append((c[0] + tx * u + nx * v, c[1] + ty * u + ny * v))
    return pts


def piece_outline(pts, widths, B):
    """Offset outline of one smooth piece with superellipse caps."""
    tans = []
    for i in range(len(pts)):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        d = math.dist(a, b) or 1
        tans.append(((b[0] - a[0]) / d, (b[1] - a[1]) / d))
    left = [(p[0] - t[1] * w / 2, p[1] + t[0] * w / 2) for p, t, w in zip(pts, tans, widths)]
    right = [(p[0] + t[1] * w / 2, p[1] - t[0] * w / 2) for p, t, w in zip(pts, tans, widths)]
    poly = left + cap(pts[-1], tans[-1], widths[-1] / 2, B["cap"], 1)[::-1][1:-1] + right[::-1] \
        + cap(pts[0], tans[0], widths[0] / 2, B["cap"], -1)[::-1][1:-1]
    sp = skia.Path()
    sp.moveTo(*poly[0])
    for q in poly[1:]:
        sp.lineTo(*q)
    sp.close()
    return sp


def brush_glyph(strokes, B):
    total = sum(length(s) for s in strokes) + END_COST * len(strokes)
    W = B["W"] * max(0.72, min(1.05, (L_REF / total) ** 0.4))
    shapes = []
    for s in strokes:
        k, parts = kind(s)
        L = length(s) or 1
        done = 0.0
        for j, part in enumerate(parts):
            pts = catmull(part)
            seg_len = length(part)
            horiz = abs(part[-1][1] - part[0][1]) <= 0.27 * abs(part[-1][0] - part[0][0])
            ws, acc = [], 0.0
            for i, p in enumerate(pts):
                if i:
                    acc += math.dist(pts[i - 1], p)
                t = (done + acc) / L
                w = profile(k, t, horiz, B, W)
                if k == "hook" and j == len(parts) - 1:
                    w = W * (1 + (B["hook_end"] - 1) * (acc / (seg_len or 1)))
                ws.append(w)
            shapes.append(piece_outline(pts, ws, B))
            done += seg_len
    out = pathops.Path()
    for sp in shapes:
        q = pathops.Path()
        _skia_to_pathops(sp, q)
        q.simplify(fix_winding=True, clockwise=True)
        out = pathops.op(out, q, pathops.PathOp.UNION, fix_winding=True, clockwise=True)
    return out


def build_font(chars, B, family, path):
    glyphs, metrics, cmap = {}, {}, {}
    glyphs[".notdef"] = tt_glyph(pathops.Path())
    metrics[".notdef"] = (1000, 0)
    glyphs["space"] = tt_glyph(pathops.Path())
    metrics["space"] = (500, 0)
    cmap[32] = "space"
    for ch, strokes in chars.items():
        n = f"uni{ord(ch):04X}"
        g = tt_glyph(brush_glyph(strokes, B))
        glyphs[n] = g
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
