"""Pip Trial: centre-line skeletons for the 95 printable ASCII glyphs.

Units per em 1000. Ink metrics: baseline 0, x-height 520, cap height 700,
ascender 740, descender -200. Every stroke is STEM units wide, so stems are
equal by construction; round letters overshoot by OS units at both lines.
Each entry returns (skeleton, left side bearing, right side bearing).
"""

from skeleton import Sk

STEM = 104
H = STEM / 2
OS = 12  # overshoot of rounds past baseline, x-height and cap height

X = 520
CAP = 700
ASC = 740
DESC = -200

# skeleton lines: flat strokes sit half a stem inside the ink line
xT, xB = X - H, H  # x-height top and baseline for flats
cT, cB = CAP - H, H
aT = ASC - H
dB = DESC + H
# rounds
xRT, xRB = X - H + OS, H - OS
cRT, cRB = CAP - H + OS, H - OS
DOT_R = 62
FIG_W = 600  # tabular figures: every digit has this advance

# side bearings (ink to advance edge)
S, R, D, O = 62, 44, 14, 32  # straight, round, diagonal, open


def bowl(cx, rx, top=xRT, bot=xRB):
    return Sk().ell(cx, (top + bot) / 2, rx, (top - bot) / 2)


def arch(x0, x1, top=xRT, join=330, down=xB):
    """n-shoulder from a stem at x0 to a stem at x1."""
    w = x1 - x0
    s = Sk().M(x0, join)
    s.C(x0, join + (top - join) * 0.75, x0 + w * 0.22, top, x0 + w * 0.52, top)
    s.C(x0 + w * 0.82, top, x1, top - (top - join) * 0.35, x1, join)
    s.L(x1, down)
    return s


G = {}


def g(name):
    def deco(fn):
        G[name] = fn
        return fn
    return deco


# ---------------------------------------------------------------- lowercase
@g("a")
def _():
    return bowl(205, 205).add(Sk().line(410, xT, 410, xB)), R, S


@g("b")
def _():
    return bowl(205, 205).add(Sk().line(0, aT, 0, xB)), S, R


@g("c")
def _():
    return Sk().arc(215, 260, 215, (xRT - xRB) / 2, 42, 318), R, O


@g("d")
def _():
    return bowl(205, 205).add(Sk().line(410, aT, 410, xB)), R, S


@g("e")
def _():
    cy = 260
    s = Sk().arc(215, cy, 215, (xRT - xRB) / 2, 0, 318)
    s.line(0 + 0, cy, 430, cy)
    return s, R, O


@g("f")
def _():
    s = Sk().M(100, xB).L(100, 540).C(100, 640, 150, aT, 240, aT).C(275, aT, 300, aT - 6, 322, aT - 16)
    s.line(0, xT, 270, xT)
    return s, D + 10, D


@g("g")
def _():
    s = bowl(205, 205)
    s.M(410, xT).L(410, -20).C(410, -110, 345, dB, 230, dB).C(140, dB, 80, dB + 20, 46, dB + 56)
    return s, R, S


@g("h")
def _():
    return Sk().line(0, aT, 0, xB).add(arch(0, 390)), S, S


@g("i")
def _():
    return Sk().line(0, xT, 0, xB).dot(0, 662, DOT_R), S, S


@g("j")
def _():
    s = Sk().M(0, xT).L(0, -60).C(0, -120, -30, dB, -95, dB).C(-120, dB, -140, dB + 6, -156, dB + 14)
    return s.dot(0, 662, DOT_R), D, S


@g("k")
def _():
    s = Sk().line(0, aT, 0, xB)
    s.line(350, xT, 40, 215)
    s.line(150, 300, 380, xB)
    return s, S, D


@g("l")
def _():
    # a small rightward tail tells l apart from I and 1 in UI text
    s = Sk().M(0, aT).L(0, 150).C(0, 80, 35, xB, 100, xB).L(118, xB)
    return s, S, D + 6


@g("m")
def _():
    return Sk().line(0, xT, 0, xB).add(arch(0, 310)).add(arch(310, 620)), S, S


@g("n")
def _():
    return Sk().line(0, xT, 0, xB).add(arch(0, 390)), S, S


@g("o")
def _():
    return bowl(225, 225), R, R


@g("p")
def _():
    return bowl(205, 205).add(Sk().line(0, xT, 0, dB)), S, R


@g("q")
def _():
    return bowl(205, 205).add(Sk().line(410, xT, 410, dB)), R, S


@g("r")
def _():
    s = Sk().line(0, xT, 0, xB)
    s.M(0, 320).C(0, 430, 70, xRT, 180, xRT).C(220, xRT, 252, xRT - 8, 276, xRT - 22)
    return s, S, D


@g("s")
def _():
    s = Sk().M(345, 420).C(318, 462, 262, xRT, 195, xRT).C(105, xRT, 48, 438, 48, 372)
    s.C(48, 300, 110, 282, 196, 262).C(292, 240, 360, 214, 360, 146)
    s.C(360, 78, 296, xRB, 196, xRB).C(122, xRB, 62, 64, 28, 108)
    return s, O, O


@g("t")
def _():
    s = Sk().M(100, 640).L(100, 160).C(100, 80, 140, xB, 210, xB).C(240, xB, 266, xB + 5, 290, xB + 15)
    s.line(0, xT, 270, xT)
    return s, D + 10, D


@g("u")
def _():
    s = Sk().M(0, xT).L(0, 200).C(0, 90, 70, xRB, 190, xRB).C(300, xRB, 390, 90, 390, 200)
    s.line(390, xT, 390, xB)
    return s, S, S


@g("v")
def _():
    return Sk().line(0, xT, 215, xB, 430, xT), D, D


@g("w")
def _():
    return Sk().line(0, xT, 160, xB, 320, 440, 480, xB, 640, xT), D, D


@g("x")
def _():
    s = Sk().line(0, xT, 400, xB).line(400, xT, 0, xB)
    return s, D, D


@g("y")
def _():
    s = Sk().line(430, xT, 150, dB + 20)
    s.M(150, dB + 20).C(135, dB - 4, 110, dB, 70, dB)
    # left arm meets the long stroke
    t = (xT - 70) / (xT - (dB + 20))
    s.line(0, xT, 430 - 280 * t, 70)
    return s, D, D


@g("z")
def _():
    return Sk().line(20, xT, 380, xT, 20, xB, 390, xB), D + 20, D + 20


# ---------------------------------------------------------------- uppercase
@g("A")
def _():
    s = Sk().line(0, cB, 260, cT, 520, cB)
    y = 240
    t = (y - cB) / (cT - cB)
    s.line(260 * t, y, 520 - 260 * t, y)
    return s, D, D


@g("B")
def _():
    s = Sk().M(0, 370).L(220, 370).C(320, 370, 380, 430, 380, 512).C(380, 594, 320, cT, 220, cT).L(0, cT).L(0, cB)
    s.L(240, cB).C(350, cB, 420, 115, 420, 212).C(420, 309, 350, 370, 240, 370)
    return s, S, R


@g("C")
def _():
    return Sk().arc(300, 350, 300, cRT - 350, 42, 318), R, O


@g("D")
def _():
    s = Sk().M(0, cB).L(0, cT).L(200, cT).C(400, cT, 500, 520, 500, 350).C(500, 180, 400, cB, 200, cB).Z()
    return s, S, R


@g("E")
def _():
    s = Sk().line(390, cT, 0, cT, 0, cB, 400, cB).line(0, 352, 340, 352)
    return s, S, O


@g("F")
def _():
    s = Sk().line(390, cT, 0, cT, 0, cB).line(0, 352, 340, 352)
    return s, S, O


@g("G")
def _():
    rx, cy = 300, 350
    s = Sk().arc(300, cy, rx, cRT - cy, 42, 360)
    s.L(600, 310).L(380, 310)
    return s, R, S - 10


@g("H")
def _():
    return Sk().line(0, cT, 0, cB).line(470, cT, 470, cB).line(0, 362, 470, 362), S, S


@g("I")
def _():
    return Sk().line(0, cT, 0, cB), S, S


@g("J")
def _():
    s = Sk().M(320, cT).L(320, 230).C(320, 110, 245, cRB, 155, cRB).C(85, cRB, 34, 72, 8, 130)
    return s, O - 8, S


@g("K")
def _():
    s = Sk().line(0, cT, 0, cB).line(430, cT, 40, 300).line(150, 400, 450, cB)
    return s, S, D


@g("L")
def _():
    return Sk().line(0, cT, 0, cB, 380, cB), S, D + 10


@g("M")
def _():
    return Sk().line(0, cB, 0, cT, 300, 230, 600, cT, 600, cB), S, S


@g("N")
def _():
    return Sk().line(0, cB, 0, cT, 470, cB, 470, cT), S, S


@g("O")
def _():
    return Sk().ell(325, 350, 325, cRT - 350), R, R


@g("P")
def _():
    s = Sk().M(0, cB).L(0, cT).L(230, cT).C(350, cT, 420, 580, 420, 480).C(420, 380, 350, 310, 230, 310).L(0, 310)
    return s, S, R


@g("Q")
def _():
    s = Sk().ell(325, 350, 325, cRT - 350)
    s.line(390, 170, 590, -20)
    return s, R, R - 10


@g("R")
def _():
    s = Sk().M(0, cB).L(0, cT).L(230, cT).C(350, cT, 420, 590, 420, 490).C(420, 390, 350, 330, 230, 330).L(0, 330)
    s.line(230, 330, 440, cB)
    return s, S, D


@g("S")
def _():
    s = Sk().M(450, 572).C(412, 632, 340, cRT, 255, cRT).C(140, cRT, 62, 598, 62, 506)
    s.C(62, 410, 140, 382, 255, 356).C(380, 328, 460, 290, 460, 196)
    s.C(460, 100, 375, cRB, 255, cRB).C(155, cRB, 74, 74, 30, 140)
    return s, O, O


@g("T")
def _():
    return Sk().line(0, cT, 500, cT).line(250, cT, 250, cB), D, D


@g("U")
def _():
    s = Sk().M(0, cT).L(0, 260).C(0, 115, 100, cRB, 240, cRB).C(380, cRB, 480, 115, 480, 260).L(480, cT)
    return s, S, S


@g("V")
def _():
    return Sk().line(0, cT, 270, cB, 540, cT), D, D


@g("W")
def _():
    return Sk().line(0, cT, 190, cB, 370, 600, 550, cB, 740, cT), D, D


@g("X")
def _():
    return Sk().line(0, cT, 480, cB).line(480, cT, 0, cB), D, D


@g("Y")
def _():
    return Sk().line(0, cT, 250, 330, 500, cT).line(250, 330, 250, cB), D, D


@g("Z")
def _():
    return Sk().line(30, cT, 460, cT, 20, cB, 470, cB), D + 20, D + 20


# ---------------------------------------------------------------- figures
# Tabular: one advance for every digit, so scores and timers do not jitter.
FT, FB = cT, cB
FRT, FRB = cRT, cRB


@g("zero")
def _():
    return Sk().ell(240, 350, 240, FRT - 350), None, None


@g("one")
def _():
    return Sk().line(40, 520, 250, FT, 250, FB), None, None


@g("two")
def _():
    s = Sk().M(40, 520).C(50, 610, 130, FRT, 240, FRT).C(360, FRT, 440, 590, 440, 490)
    s.C(440, 390, 370, 330, 250, 240).L(40, FB).L(450, FB)
    return s, None, None


@g("three")
def _():
    s = Sk().M(52, 580).C(92, 630, 160, FRT, 240, FRT).C(350, FRT, 420, 598, 420, 515)
    s.C(420, 425, 345, 372, 225, 372)
    s.M(225, 372).C(362, 372, 452, 310, 452, 210).C(452, 100, 362, FRB, 240, FRB).C(150, FRB, 80, 72, 38, 134)
    return s, None, None


@g("four")
def _():
    return Sk().line(350, FB, 350, FT, 30, 220, 480, 220), None, None


@g("five")
def _():
    s = Sk().M(420, FT).L(110, FT).L(80, 390).C(130, 418, 186, 428, 245, 428)
    s.C(372, 428, 452, 344, 452, 232).C(452, 112, 362, FRB, 242, FRB).C(152, FRB, 82, 72, 40, 134)
    return s, None, None


@g("six")
def _():
    s = Sk().ell(250, 215, 205, 215 - FRB)
    s.M(372, 626).C(334, 648, 292, FRT, 252, FRT).C(122, FRT, 45, 540, 45, 330).L(45, 215)
    return s, None, None


@g("seven")
def _():
    return Sk().line(40, FT, 450, FT, 170, FB), None, None


@g("eight")
def _():
    s = Sk().ell(240, 515, 172, FRT - 515).ell(240, 205, 205, 205 - FRB)
    return s, None, None


@g("nine")
def _():
    s = Sk().ell(232, 485, 205, FRT - 485)
    s.M(437, 485).L(437, 370).C(437, 160, 360, FRB, 230, FRB).C(190, FRB, 150, 50, 110, 72)
    return s, None, None


# ---------------------------------------------------------------- punctuation
@g("space")
def _():
    return None, 230, None


@g("exclam")
def _():
    return Sk().line(0, cT, 0, 240).dot(0, DOT_R, DOT_R), S - 4, S - 4


@g("quotedbl")
def _():
    return Sk().line(0, cT, 0, 480).line(160, cT, 160, 480), S, S


@g("numbersign")
def _():
    s = Sk().line(170, 620, 120, 80).line(350, 620, 300, 80)
    s.line(40, 450, 470, 450).line(20, 250, 450, 250)
    return s, O, O


@g("dollar")
def _():
    s = Sk().M(420, 532).C(386, 586, 322, 612, 245, 612).C(145, 612, 72, 556, 72, 478)
    s.C(72, 398, 142, 370, 245, 348).C(358, 324, 430, 290, 430, 208)
    s.C(430, 126, 352, 86, 245, 86).C(160, 86, 88, 112, 46, 168)
    s.line(245, 730, 245, -30)
    return s, O, O


@g("percent")
def _():
    s = Sk().ell(130, 520, 110, 130).ell(530, 180, 110, 130)
    s.line(520, cT, 140, cB)
    return s, R, R


@g("ampersand")
def _():
    s = Sk().M(500, cB).L(170, 410).C(125, 462, 112, 500, 112, 540).C(112, 612, 166, 660, 236, 660)
    s.C(306, 660, 356, 614, 356, 552).C(356, 484, 300, 440, 210, 392)
    s.C(108, 338, 46, 280, 46, 190).C(46, 98, 124, 40, 232, 40).C(340, 40, 420, 104, 470, 220).L(490, 290)
    return s, R, D


@g("quotesingle")
def _():
    return Sk().line(0, cT, 0, 480), S, S


@g("parenleft")
def _():
    s = Sk().M(200, 740).C(85, 620, 40, 470, 40, 310).C(40, 150, 85, 0, 200, -120)
    return s, R, O - 10


@g("parenright")
def _():
    s = Sk().M(0, 740).C(115, 620, 160, 470, 160, 310).C(160, 150, 115, 0, 0, -120)
    return s, O - 10, R


@g("asterisk")
def _():
    s = Sk()
    cx, cy, r = 170, 560, 120
    import math
    for a in (90, 210, 330):
        t = math.radians(a)
        s.line(cx, cy, cx + r * math.cos(t), cy + r * math.sin(t))
    for a in (30, 150, 270):
        t = math.radians(a)
        s.line(cx, cy, cx + r * 0.9 * math.cos(t), cy + r * 0.9 * math.sin(t))
    return s, O, O


@g("plus")
def _():
    return Sk().line(0, 300, 380, 300).line(190, 110, 190, 490), O, O


@g("comma")
def _():
    s = Sk().dot(50, DOT_R, DOT_R)
    s.M(80, 70).C(80, 10, 55, -50, 20, -110)
    return s, D + 20, D + 20


@g("hyphen")
def _():
    return Sk().line(0, 280, 230, 280), O, O


@g("period")
def _():
    return Sk().dot(0, DOT_R, DOT_R), S - 10, S - 10


@g("slash")
def _():
    return Sk().line(0, -60, 320, 720), D, D


@g("colon")
def _():
    return Sk().dot(0, DOT_R, DOT_R).dot(0, X - DOT_R, DOT_R), S - 10, S - 10


@g("semicolon")
def _():
    s = Sk().dot(50, X - DOT_R, DOT_R).dot(50, DOT_R, DOT_R)
    s.M(80, 70).C(80, 10, 55, -50, 20, -110)
    return s, D + 20, D + 20


@g("less")
def _():
    return Sk().line(380, 520, 20, 300, 380, 80), O, O


@g("equal")
def _():
    return Sk().line(0, 390, 380, 390).line(0, 210, 380, 210), O, O


@g("greater")
def _():
    return Sk().line(0, 520, 360, 300, 0, 80), O, O


@g("question")
def _():
    s = Sk().M(40, 548).C(62, 624, 138, 660, 226, 660).C(336, 660, 416, 600, 416, 510)
    s.C(416, 424, 356, 384, 290, 352).C(240, 328, 222, 300, 222, 252).L(222, 240)
    s.dot(222, DOT_R, DOT_R)
    return s, O, O


@g("at")
def _():
    s = Sk().ell(360, 300, 125, 145, square=1.0)
    s.M(485, 440).L(485, 210).C(485, 150, 520, 120, 570, 120).C(650, 120, 700, 220, 700, 330)
    s.C(700, 530, 548, 660, 365, 660).C(180, 660, 40, 512, 40, 300).C(40, 92, 182, -50, 372, -50)
    s.C(455, -50, 525, -30, 575, 0)
    return s, R, R


@g("bracketleft")
def _():
    return Sk().line(200, 740, 40, 740, 40, -120, 200, -120), S, O - 10


@g("backslash")
def _():
    return Sk().line(0, 720, 320, -60), D, D


@g("bracketright")
def _():
    return Sk().line(0, 740, 160, 740, 160, -120, 0, -120), O - 10, S


@g("asciicircum")
def _():
    return Sk().line(0, 420, 190, 650, 380, 420), O, O


@g("underscore")
def _():
    return Sk().line(0, -90, 440, -90), D, D


@g("grave")
def _():
    return Sk().line(0, 700, 110, 590), O, O


@g("braceleft")
def _():
    s = Sk().M(240, 740).C(160, 740, 125, 705, 125, 625).L(125, 420).C(125, 350, 95, 310, 30, 310)
    s.C(95, 310, 125, 270, 125, 200).L(125, -5).C(125, -85, 160, -120, 240, -120)
    return s, R, O - 10


@g("bar")
def _():
    return Sk().line(0, 760, 0, -160), S, S


@g("braceright")
def _():
    s = Sk().M(0, 740).C(80, 740, 115, 705, 115, 625).L(115, 420).C(115, 350, 145, 310, 210, 310)
    s.C(145, 310, 115, 270, 115, 200).L(115, -5).C(115, -85, 80, -120, 0, -120)
    return s, O - 10, R


@g("asciitilde")
def _():
    s = Sk().M(0, 250).C(60, 330, 120, 345, 195, 305).C(270, 265, 330, 275, 390, 355)
    return s, O, O


MATH = {"plus", "equal", "less", "greater"}
MATH_W = 560  # math signs share one advance, so they line up in tables

TABULAR = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"}

# Kerning: ink-based pairs for the common collisions, in font units.
KERN = """
@LC_ROUND = [a c d e g o q s];
@LC_DIAG = [v w y];
@PUNCT = [period comma];
@QUOTES = [quotesingle quotedbl];
feature kern {
  pos A [V W] -60;
  pos A Y -64;
  pos A T -56;
  pos A [v w y] -34;
  pos A @QUOTES -60;
  pos [V W] A -60;
  pos Y A -64;
  pos T A -56;
  pos T @LC_ROUND -84;
  pos T [r u m n p] -60;
  pos T @LC_DIAG -56;
  pos T @PUNCT -90;
  pos T colon -40;
  pos T hyphen -60;
  pos [V W] @LC_ROUND -50;
  pos [V W] @PUNCT -80;
  pos Y @LC_ROUND -80;
  pos Y [u r m n p] -56;
  pos Y @PUNCT -90;
  pos L T -84;
  pos L [V W] -70;
  pos L Y -84;
  pos L @QUOTES -96;
  pos L [v w y] -30;
  pos P A -50;
  pos P @PUNCT -110;
  pos P @LC_ROUND -24;
  pos F A -40;
  pos F @PUNCT -96;
  pos F @LC_ROUND -30;
  pos [r] @PUNCT -64;
  pos @LC_DIAG @PUNCT -56;
  pos [K X] [O C G Q o e c] -26;
  pos [O D Q] [V W Y] -24;
  pos [O D Q] [A X] -20;
  pos [V W Y] [O C G Q] -24;
  pos [f] @LC_ROUND -10;
  pos [f] @QUOTES 40;
  pos @QUOTES A -60;
  pos @QUOTES @LC_ROUND -30;
  pos [k x] @LC_ROUND -16;
  pos @LC_ROUND [v w y x] -10;
  pos L O -24;
  pos R [T V W Y] -20;
  pos [T V W Y] [i j] -10;
} kern;
"""
