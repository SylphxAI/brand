"""Quick raster proof of a built font (glyph grid), for drawing iterations."""

import sys

import skia
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont


class SkPen(BasePen):
    def __init__(self, gs, path):
        super().__init__(gs)
        self.p = path

    def _moveTo(self, pt):
        self.p.moveTo(*pt)

    def _lineTo(self, pt):
        self.p.lineTo(*pt)

    def _curveToOne(self, a, b, c):
        self.p.cubicTo(*a, *b, *c)

    def _qCurveToOne(self, a, b):
        self.p.quadTo(*a, *b)

    def _closePath(self):
        self.p.close()


def main(font_path, out, size=96, cols=16, text=None):
    f = TTFont(font_path)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    names = [cmap[ord(c)] for c in text] if text else [n for n in f.getGlyphOrder() if n != ".notdef"]
    scale = size / 1000
    cell = size * 1.3
    rows = (len(names) + cols - 1) // cols
    surf = skia.Surface(int(cell * cols + 20), int(cell * rows + 20))
    c = surf.getCanvas()
    c.clear(skia.ColorWHITE)
    guide = skia.Paint(Color=skia.Color(200, 220, 255), StrokeWidth=1)
    ink = skia.Paint(Color=skia.Color(20, 20, 20), AntiAlias=True)
    for i, n in enumerate(names):
        x = 10 + (i % cols) * cell
        base = 10 + (i // cols) * cell + size * 0.95
        for y in (0, 520, 700):
            c.drawLine(x, base - y * scale, x + cell - 4, base - y * scale, guide)
        adv = f["hmtx"][n][0] * scale
        c.drawLine(x + adv, base - 900 * scale, x + adv, base + 200 * scale, guide)
        c.drawLine(x, base - 900 * scale, x, base + 200 * scale, guide)
        p = skia.Path()
        gs[n].draw(SkPen(gs, p))
        m = skia.Matrix()
        m.setAll(scale, 0, x, 0, -scale, base, 0, 0, 1)
        p.transform(m)
        c.drawPath(p, ink)
    surf.makeImageSnapshot().save(out, skia.kPNG)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 96,
         int(sys.argv[4]) if len(sys.argv) > 4 else 16)
