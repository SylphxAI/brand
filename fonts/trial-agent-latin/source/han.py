"""Pip Trial TC: 24 Traditional Chinese characters, drawn as strokes.

The same pipeline as the Latin: centre-line strokes at one width, round caps
and joins, so the Han glyphs share the Latin's rounded, monoline voice (the
rounded "yuan" style). Characters are drawn on a 1000-unit grid with y going
down (writing order is easier to read that way); `to_font` flips them onto the
ideographic em box (880 above, 120 below the baseline). Components (口, 女,
禾, 木, 攵, 貝, 月, 亻, 糸, 氵) are drawn once in their own 1000 box and placed
by scaling the centre lines, which keeps every stroke the same width.
"""

import skia

from skeleton import Sk

STEM = 74


def to_font(sk):
    out = Sk()
    out.add(sk, dx=0, dy=880, sx=1, sy=-1)
    return out


def put(dst, comp, x0, y0, x1, y1):
    """Place a component drawn in 0..1000 into the box (x0, y0)-(x1, y1)."""
    return dst.add(comp, dx=x0, dy=y0, sx=(x1 - x0) / 1000, sy=(y1 - y0) / 1000)


# stroke helpers (grid coordinates, y down) -----------------------------------
def H(s, x0, x1, y):
    return s.line(x0, y, x1, y)


def V(s, x, y0, y1):
    return s.line(x, y0, x, y1)


def VG(s, x, y0, y1, hook=60):
    """Vertical with a hook to the left at the bottom (竖钩)."""
    return s.line(x, y0, x, y1, x - hook, y1 - hook * 0.75)


def pie(s, x0, y0, x1, y1, straight=0.35):
    """Left-falling stroke (撇): starts steep and sweeps out to the left."""
    s.M(x0, y0)
    s.C(x0, y0 + (y1 - y0) * (0.3 + straight), x0 - (x0 - x1) * 0.35, y1 - (y1 - y0) * 0.1, x1, y1)
    return s


def na(s, x0, y0, x1, y1):
    """Right-falling stroke (捺): eases into a flatter end."""
    s.M(x0, y0)
    s.C(x0 + (x1 - x0) * 0.3, y0 + (y1 - y0) * 0.55, x0 + (x1 - x0) * 0.62, y1 - (y1 - y0) * 0.04, x1, y1)
    return s


def dot(s, x0, y0, x1, y1):
    return s.line(x0, y0, x1, y1)


# components (each in its own 0..1000 box) -------------------------------------
def kou():
    s = Sk()
    V(s, 150, 120, 900)
    s.line(150, 120, 850, 120, 850, 900)
    H(s, 150, 850, 860)
    return s


def ri():
    s = kou()
    H(s, 150, 850, 490)
    return s


def nv():
    """女"""
    s = Sk()
    s.M(470, 70).L(250, 560).C(450, 640, 650, 760, 840, 930)
    pie(s, 730, 400, 170, 930, 0.25)
    H(s, 80, 920, 430)
    return s


def he():
    """禾"""
    s = Sk()
    s.M(800, 70).C(620, 140, 420, 180, 230, 200)
    H(s, 90, 910, 400)
    V(s, 500, 170, 960)
    pie(s, 480, 430, 80, 820, 0.2)
    na(s, 520, 440, 900, 760)
    return s


def mu():
    """木"""
    s = Sk()
    H(s, 80, 920, 330)
    V(s, 500, 60, 960)
    pie(s, 480, 360, 70, 820, 0.2)
    na(s, 520, 360, 930, 780)
    return s


def pu():
    """攵"""
    s = Sk()
    pie(s, 400, 60, 170, 420, 0.1)
    H(s, 300, 900, 260)
    pie(s, 760, 260, 130, 960, 0.15)
    na(s, 350, 520, 940, 950)
    return s


def bei():
    """貝"""
    s = Sk()
    V(s, 200, 70, 700)
    s.line(200, 70, 800, 70, 800, 700)
    H(s, 200, 800, 280)
    H(s, 200, 800, 490)
    H(s, 200, 800, 700)
    pie(s, 400, 760, 170, 960, 0.1)
    dot(s, 610, 790, 820, 950)
    return s


def yue():
    """月"""
    s = Sk()
    s.M(220, 80).L(220, 620).C(220, 800, 170, 890, 90, 960)
    s.line(220, 80, 800, 80, 800, 930, 720, 880)
    H(s, 220, 800, 360)
    H(s, 220, 800, 620)
    return s


def ren():
    """亻"""
    s = Sk()
    pie(s, 600, 60, 120, 540, 0.15)
    V(s, 420, 350, 960)
    return s


def si():
    """糸"""
    s = Sk()
    s.line(560, 60, 300, 340, 620, 320)
    s.line(700, 210, 220, 660, 820, 620)
    dot(s, 700, 500, 820, 660)
    V(s, 520, 650, 960)
    dot(s, 320, 760, 170, 920)
    dot(s, 700, 760, 840, 900)
    return s


def shui():
    """氵"""
    s = Sk()
    dot(s, 260, 110, 400, 230)
    dot(s, 190, 380, 330, 500)
    s.line(160, 900, 400, 590)
    return s


# characters -------------------------------------------------------------------
G = {}


def char(ch):
    def deco(fn):
        G[ch] = fn
        return fn
    return deco


@char("永")
def _():
    s = Sk()
    dot(s, 460, 70, 550, 160)
    s.line(320, 260, 510, 260, 510, 910, 430, 855)
    s.line(150, 440, 370, 440).C(310, 610, 220, 720, 90, 820)
    s.M(820, 310).C(760, 390, 680, 450, 590, 490)
    na(s, 560, 420, 940, 880)
    return s


@char("開")
def _():
    s = Sk()
    V(s, 140, 90, 940)
    s.line(140, 90, 430, 90, 430, 380)
    H(s, 140, 430, 235)
    H(s, 140, 430, 380)
    s.line(570, 90, 860, 90, 860, 920, 795, 875)
    V(s, 570, 90, 380)
    H(s, 570, 860, 235)
    H(s, 570, 860, 380)
    H(s, 300, 700, 520)
    H(s, 270, 730, 690)
    s.M(430, 520).L(430, 720).C(430, 810, 400, 860, 330, 900)
    V(s, 580, 520, 900)
    return s


@char("始")
def _():
    s = put(Sk(), nv(), 50, 70, 470, 940)
    s.line(700, 90, 550, 410, 880, 380)
    dot(s, 770, 250, 880, 400)
    put(s, kou(), 520, 500, 900, 940)
    return s


@char("遊")
def _():
    s = Sk()
    dot(s, 150, 110, 230, 200)
    s.line(80, 350, 250, 350, 150, 640)
    s.M(150, 640).C(210, 820, 320, 880, 520, 880).C(700, 880, 850, 890, 950, 915)
    # 方
    dot(s, 440, 60, 490, 140)
    H(s, 330, 610, 200)
    s.line(400, 340, 570, 340, 550, 690, 495, 650)
    s.M(440, 200).L(440, 440).C(440, 570, 400, 650, 320, 720)
    # 𠂉
    s.M(730, 60).C(715, 130, 690, 190, 640, 250)
    H(s, 700, 930, 170)
    # 子
    s.line(680, 320, 880, 320, 790, 420)
    VG(s, 790, 420, 730, 50)
    H(s, 640, 940, 530)
    return s


@char("戲")
def _():
    s = Sk()
    # 虍
    V(s, 300, 60, 210)
    H(s, 300, 450, 135)
    H(s, 140, 540, 240)
    s.M(150, 240).L(150, 520).C(150, 700, 120, 810, 70, 900)
    s.line(230, 330, 500, 330, 470, 390)
    s.M(320, 290).L(320, 440).C(320, 470, 340, 485, 380, 485).L(530, 485)
    # 业
    V(s, 280, 580, 880)
    V(s, 430, 580, 880)
    dot(s, 205, 650, 225, 770)
    dot(s, 515, 650, 495, 770)
    H(s, 170, 550, 900)
    # 戈
    H(s, 580, 930, 330)
    s.M(690, 80).C(710, 450, 790, 720, 930, 900).L(935, 780)
    s.line(870, 500, 590, 860)
    dot(s, 820, 110, 900, 200)
    return s


@char("勝")
def _():
    s = put(Sk(), yue(), 40, 70, 420, 950)
    dot(s, 560, 80, 610, 170)
    dot(s, 840, 80, 780, 170)
    H(s, 490, 910, 240)
    H(s, 450, 950, 370)
    s.M(690, 250).L(690, 370).C(660, 460, 580, 530, 470, 590)
    na(s, 710, 380, 950, 570)
    s.line(490, 660, 880, 660, 860, 930, 790, 885)
    s.M(680, 580).C(670, 760, 600, 860, 470, 945)
    return s


@char("利")
def _():
    s = put(Sk(), he(), 40, 60, 600, 960)
    V(s, 700, 180, 700)
    VG(s, 880, 70, 940, 65)
    return s


@char("失")
def _():
    s = Sk()
    s.M(330, 80).C(310, 210, 250, 300, 170, 370)
    H(s, 200, 800, 290)
    H(s, 90, 910, 520)
    s.M(500, 70).L(500, 520).C(480, 720, 330, 860, 100, 945)
    na(s, 530, 560, 930, 930)
    return s


@char("敗")
def _():
    s = put(Sk(), bei(), 30, 70, 520, 950)
    put(s, pu(), 500, 60, 960, 960)
    return s


@char("分")
def _():
    s = Sk()
    s.M(400, 90).C(360, 250, 260, 370, 90, 460)
    na(s, 600, 90, 940, 450)
    s.line(250, 500, 760, 500, 740, 900, 660, 850)
    s.M(480, 500).C(470, 710, 380, 850, 170, 950)
    return s


@char("數")
def _():
    s = Sk()
    # 婁 (compressed): 毌 then 女
    H(s, 110, 490, 100)
    V(s, 150, 190, 450)
    s.line(150, 190, 450, 190, 450, 450)
    H(s, 100, 500, 320)
    H(s, 150, 450, 450)
    V(s, 300, 50, 520)
    put(s, nv(), 70, 500, 520, 950)
    put(s, pu(), 520, 60, 960, 960)
    return s


@char("等")
def _():
    s = Sk()
    s.M(270, 60).C(240, 150, 190, 210, 110, 270)
    H(s, 220, 450, 150)
    dot(s, 300, 180, 350, 260)
    s.M(660, 60).C(630, 150, 580, 210, 510, 270)
    H(s, 610, 900, 150)
    dot(s, 700, 180, 750, 260)
    H(s, 260, 740, 380)
    V(s, 500, 300, 560)
    H(s, 120, 880, 560)
    H(s, 90, 910, 700)
    VG(s, 700, 600, 940, 70)
    dot(s, 360, 770, 440, 860)
    return s


@char("級")
def _():
    s = put(Sk(), si(), 30, 60, 440, 960)
    s.M(620, 120).L(620, 420).C(610, 680, 560, 830, 460, 945)
    s.line(500, 120, 820, 120, 720, 400, 890, 400).C(830, 580, 740, 700, 640, 790)
    na(s, 630, 540, 950, 930)
    return s


@char("金")
def _():
    s = Sk()
    pie(s, 500, 60, 70, 470, 0.0)
    na(s, 500, 60, 930, 460)
    H(s, 300, 700, 400)
    H(s, 210, 790, 580)
    V(s, 500, 400, 900)
    dot(s, 320, 680, 380, 800)
    dot(s, 680, 680, 620, 800)
    H(s, 100, 900, 900)
    return s


@char("幣")
def _():
    s = Sk()
    # 敝 left
    V(s, 290, 60, 200)
    dot(s, 160, 90, 190, 170)
    dot(s, 420, 90, 390, 170)
    V(s, 110, 230, 520)
    s.line(110, 230, 470, 230, 470, 520, 430, 490)
    V(s, 290, 230, 500)
    dot(s, 200, 320, 220, 410)
    dot(s, 380, 320, 360, 410)
    put(s, pu(), 520, 50, 930, 540)
    # 巾
    V(s, 230, 640, 870)
    s.line(230, 640, 770, 640, 770, 870, 720, 835)
    V(s, 500, 570, 960)
    return s


@char("麻")
def _():
    s = Sk()
    dot(s, 500, 60, 545, 140)
    H(s, 130, 920, 200)
    s.M(150, 200).L(150, 500).C(150, 720, 120, 840, 60, 945)
    m = Sk()
    H(m, 80, 900, 330)
    V(m, 500, 60, 960)
    pie(m, 480, 360, 70, 820, 0.2)
    dot(m, 560, 420, 830, 640)
    put(s, m, 240, 270, 590, 950)
    put(s, mu(), 590, 270, 940, 950)
    return s


@char("將")
def _():
    s = Sk()
    # 爿: short upright, a rising tick, a falling sweep, and the long upright
    V(s, 300, 60, 960)
    s.line(160, 170, 175, 400)
    s.line(80, 500, 300, 430)
    pie(s, 230, 580, 80, 800, 0.1)
    s.M(570, 60).C(550, 140, 510, 200, 440, 260)
    s.line(520, 150, 840, 150).C(800, 300, 650, 420, 440, 490)
    dot(s, 600, 250, 680, 330)
    H(s, 420, 940, 640)
    VG(s, 790, 530, 940, 70)
    dot(s, 560, 710, 620, 810)
    return s


@char("大")
def _():
    s = Sk()
    H(s, 100, 900, 330)
    s.M(500, 60).L(500, 330).C(490, 600, 350, 820, 100, 940)
    na(s, 520, 380, 930, 920)
    return s


@char("老")
def _():
    s = Sk()
    V(s, 470, 60, 400)
    H(s, 250, 700, 210)
    H(s, 90, 910, 400)
    s.M(800, 80).C(690, 330, 460, 520, 150, 680)
    s.line(450, 700, 790, 560)
    s.M(450, 560).L(450, 850).C(450, 905, 475, 925, 540, 925).L(850, 925).L(870, 840)
    return s


@char("二")
def _():
    s = Sk()
    H(s, 220, 780, 300)
    H(s, 100, 900, 780)
    return s


@char("你")
def _():
    s = put(Sk(), ren(), 40, 60, 400, 960)
    s.M(560, 70).C(540, 180, 500, 260, 430, 330)
    s.line(520, 240, 900, 240, 860, 320)
    VG(s, 690, 320, 930, 65)
    dot(s, 550, 510, 470, 720)
    dot(s, 810, 510, 890, 700)
    return s


@char("好")
def _():
    s = put(Sk(), nv(), 50, 70, 480, 940)
    s.line(560, 140, 880, 140, 720, 360)
    VG(s, 720, 360, 920, 70)
    H(s, 490, 950, 540)
    return s


@char("香")
def _():
    s = put(Sk(), he(), 80, 40, 920, 560)
    put(s, ri(), 240, 540, 760, 960)
    return s


@char("港")
def _():
    s = put(Sk(), shui(), 30, 60, 340, 960)
    H(s, 450, 900, 220)
    V(s, 560, 70, 460)
    V(s, 790, 70, 460)
    H(s, 390, 950, 460)
    dot(s, 570, 520, 490, 610)
    dot(s, 780, 520, 860, 610)
    s.line(500, 660, 820, 660, 820, 780)
    H(s, 500, 820, 780)
    s.M(500, 660).L(500, 880).C(500, 920, 520, 935, 570, 935).L(900, 935).L(915, 860)
    return s
