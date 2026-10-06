"""Build Pip Trial (Latin) and Pip Trial TC (24 Han trial glyphs).

    python build.py            # writes ../PipTrial-Regular.{ttf,woff2} and ../PipTrialTC-Regular.{ttf,woff2}

Requires fonttools[woff], skia-python and skia-pathops (requirements.txt).
"""

import sys
from pathlib import Path

from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib import TTFont, newTable

from skeleton import bounds, outline, tt_glyph

HERE = Path(__file__).resolve().parent
OUT = HERE.parent

VERSION = "0.100"
COPYRIGHT = "Copyright 2026 Sylphx Limited"
LICENSE = "This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://openfontlicense.org"
LICENSE_URL = "https://openfontlicense.org"
VENDOR = "SYLX"

ASCII_NAMES = {
    32: "space", 33: "exclam", 34: "quotedbl", 35: "numbersign", 36: "dollar", 37: "percent",
    38: "ampersand", 39: "quotesingle", 40: "parenleft", 41: "parenright", 42: "asterisk",
    43: "plus", 44: "comma", 45: "hyphen", 46: "period", 47: "slash", 48: "zero", 49: "one",
    50: "two", 51: "three", 52: "four", 53: "five", 54: "six", 55: "seven", 56: "eight",
    57: "nine", 58: "colon", 59: "semicolon", 60: "less", 61: "equal", 62: "greater",
    63: "question", 64: "at", 91: "bracketleft", 92: "backslash", 93: "bracketright",
    94: "asciicircum", 95: "underscore", 96: "grave", 123: "braceleft", 124: "bar",
    125: "braceright", 126: "asciitilde",
}
for c in range(65, 91):
    ASCII_NAMES[c] = chr(c)
for c in range(97, 123):
    ASCII_NAMES[c] = chr(c)


def finish(fb, family, upm_metrics, cmap, glyphs, metrics, fea=None, xh=0, cap=0, unicode_ranges=None):
    asc, desc = upm_metrics
    order = [".notdef"] + [n for n in glyphs if n != ".notdef"]
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=asc, descent=desc, lineGap=0)
    ps = family.replace(" ", "") + "-Regular"
    fb.setupNameTable({
        "copyright": COPYRIGHT,
        "familyName": family,
        "styleName": "Regular",
        "uniqueFontIdentifier": f"{VERSION};{VENDOR};{ps}",
        "fullName": f"{family} Regular",
        "version": f"Version {VERSION}",
        "psName": ps,
        "manufacturer": "Sylphx Limited",
        "designer": "Sylphx Limited",
        "vendorURL": "https://sylphx.com",
        "licenseDescription": LICENSE,
        "licenseInfoURL": LICENSE_URL,
    }, mac=False)
    ymin = min((g.yMin for g in glyphs.values() if hasattr(g, "yMin") and g.numberOfContours), default=desc)
    ymax = max((g.yMax for g in glyphs.values() if hasattr(g, "yMax") and g.numberOfContours), default=asc)
    fb.setupOS2(
        version=4,
        achVendID=VENDOR,
        fsType=0,
        usWeightClass=400,
        sTypoAscender=asc,
        sTypoDescender=desc,
        sTypoLineGap=0,
        usWinAscent=max(asc, ymax),
        usWinDescent=max(-desc, -ymin),
        sxHeight=xh,
        sCapHeight=cap,
        fsSelection=0x40 | 0x80,  # REGULAR | USE_TYPO_METRICS
        ulUnicodeRange1=unicode_ranges or 1,
        ulCodePageRange1=1,  # Latin 1
    )
    fb.setupPost(keepGlyphNames=True)
    from fontTools.misc.timeTools import timestampFromString
    ts = timestampFromString("Tue Oct 06 00:00:00 2026")
    fb.setupHead(unitsPerEm=1000, fontRevision=float(VERSION), created=ts, modified=ts)
    fb.font["head"].flags |= 1 << 3  # integer ppem
    if fea:
        addOpenTypeFeaturesFromString(fb.font, fea)
    gasp = newTable("gasp")
    gasp.version = 1
    gasp.gaspRange = {0xFFFF: 0x000F}
    fb.font["gasp"] = gasp
    prep = newTable("prep")
    from fontTools.ttLib.tables import ttProgram
    prep.program = ttProgram.Program()
    prep.program.fromAssembly(["PUSHW[]", "511", "SCANCTRL[]", "PUSHB[]", "4", "SCANTYPE[]"])
    fb.font["prep"] = prep
    return fb.font


def notdef(width, asc_line, stem):
    from skeleton import Sk
    s = Sk().line(60, 60, 60, asc_line - 60, width - 60, asc_line - 60, width - 60, 60).Z()
    return outline(s, stem * 0.6)


def build_latin():
    import latin

    glyphs, metrics, cmap = {}, {}, {}
    nd = notdef(500, latin.CAP, latin.STEM)
    glyphs[".notdef"] = tt_glyph(nd)
    metrics[".notdef"] = (500, int(bounds(nd)[0]))
    for code, name in sorted(ASCII_NAMES.items()):
        sk, lsb, rsb = latin.G[name]()
        cmap[code] = name
        if sk is None:  # space
            glyphs[name] = tt_glyph(outline(__import__("skeleton").Sk(), latin.STEM))
            metrics[name] = (lsb, 0)
            continue
        p = outline(sk, latin.STEM)
        x0, _, x1, _ = bounds(p)
        if name in latin.TABULAR or name in latin.MATH:
            adv = latin.FIG_W if name in latin.TABULAR else latin.MATH_W
            dx = round((adv - (x1 - x0)) / 2 - x0)
        else:
            dx = round(lsb - x0)
            adv = round(lsb + (x1 - x0) + rsb)
        glyphs[name] = tt_glyph(p, dx)
        metrics[name] = (adv, 0)
    cmap[0xA0] = "space"  # no-break space shares the space glyph
    fb = FontBuilder(1000, isTTF=True)
    font = finish(fb, "Pip Trial", (950, -250), cmap, glyphs, metrics, latin.KERN, latin.X, latin.CAP)
    # left side bearing from the compiled glyph bounds
    glyf = font["glyf"]
    for n in font.getGlyphOrder():
        g = glyf[n]
        g.recalcBounds(glyf)
        adv, _ = font["hmtx"][n]
        font["hmtx"][n] = (adv, g.xMin if g.numberOfContours else 0)
    return font


def build_cjk():
    import han

    glyphs, metrics, cmap = {}, {}, {}
    nd = notdef(1000, 880, han.STEM)
    glyphs[".notdef"] = tt_glyph(nd)
    metrics[".notdef"] = (1000, 0)
    from skeleton import Sk
    glyphs["space"] = tt_glyph(outline(Sk(), han.STEM))
    metrics["space"] = (500, 0)
    cmap[32] = "space"
    cmap[0xA0] = "space"
    for ch, fn in han.G.items():
        name = f"uni{ord(ch):04X}"
        p = outline(han.to_font(fn()), han.STEM)
        glyphs[name] = tt_glyph(p)
        metrics[name] = (1000, 0)
        cmap[ord(ch)] = name
    fb = FontBuilder(1000, isTTF=True)
    font = finish(fb, "Pip Trial TC", (880, -120), cmap, glyphs, metrics, xh=520, cap=700)
    glyf = font["glyf"]
    for n in font.getGlyphOrder():
        g = glyf[n]
        g.recalcBounds(glyf)
        adv, _ = font["hmtx"][n]
        font["hmtx"][n] = (adv, g.xMin if g.numberOfContours else 0)
    os2 = font["OS/2"]
    os2.ulUnicodeRange2 |= 1 << (59 - 32)  # CJK Unified Ideographs
    os2.ulCodePageRange1 = 1 | (1 << 20)  # Latin 1, Chinese Traditional
    os2.panose.bFamilyType = 2  # text and display
    os2.panose.bProportion = 9  # every Han glyph is one em wide
    font["post"].isFixedPitch = 1
    return font


def save(font, stem):
    ttf = OUT / f"{stem}.ttf"
    font.save(ttf)
    f2 = TTFont(ttf)
    f2.flavor = "woff2"
    f2.save(OUT / f"{stem}.woff2")
    print("wrote", ttf.name, f"{stem}.woff2", len(font.getGlyphOrder()), "glyphs")


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    which = sys.argv[1:] or ["latin", "cjk"]
    if "latin" in which:
        save(build_latin(), "PipTrial-Regular")
    if "cjk" in which:
        save(build_cjk(), "PipTrialTC-Regular")
