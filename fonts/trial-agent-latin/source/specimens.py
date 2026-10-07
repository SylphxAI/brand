"""Render the specimen PNGs with headless Chromium (real shaping and kerning).

    python specimens.py <chromium> <inter.ttf> <fredoka.ttf> [<noto-tc-instance.ttf>] [<han-v3 dir>] [<han-v4 dir> [<out.png> [<title>]]]

Inter and Fredoka (SIL OFL) are only loaded from local paths for the
comparison image; they are not shipped or copied. The optional fourth font is
the unmodified Noto Sans TC instance that derive_tc.py writes, for the Han
comparison.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "specimens"

PAPER, INK, ACCENT, MUTED = "#F2EEE6", "#15130F", "#2448F5", "#6E675C"


def page(body, inter, fredoka, width):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Pip; src: url("{(ROOT / 'PipTrial-Regular.woff2').as_uri()}"); }}
@font-face {{ font-family: PipTC; src: url("{(ROOT / 'PipTrialTC-Regular.woff2').as_uri()}"); }}
@font-face {{ font-family: InterRef; src: url("{Path(inter).resolve().as_uri()}"); font-weight: 100 900; }}
@font-face {{ font-family: FredokaRef; src: url("{Path(fredoka).resolve().as_uri()}"); font-weight: 300 700; }}
html, body {{ margin: 0; background: {PAPER}; color: {INK}; }}
body {{ width: {width}px; padding: 56px 64px; box-sizing: border-box; font-family: Pip, PipTC; font-kerning: normal; }}
.label {{ font: 500 15px/1.2 InterRef; letter-spacing: .06em; text-transform: uppercase; color: {MUTED}; margin: 0 0 10px; }}
.row {{ margin: 0 0 34px; }}
.grid {{ display: grid; gap: 0; }}
.cell {{ border: 1px solid #DDD5C6; margin: -1px 0 0 -1px; display: flex; align-items: center; justify-content: center; }}
.cmp {{ display: grid; grid-template-columns: 150px 1fr; align-items: baseline; gap: 18px; border-top: 1px solid #DDD5C6; padding: 18px 0; }}
.game {{ background: radial-gradient(120% 140% at 20% 0%, #3B2E9E 0%, #1B1640 55%, #0E0B22 100%); color: #fff; border-radius: 28px; padding: 36px 40px; }}
.pill {{ display: inline-block; padding: 12px 26px 14px; border-radius: 999px; font-size: 30px; }}
</style></head><body>{body}</body></html>"""


def shot(chromium, html, name, width, height):
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "p.html"
        f.write_text(html, encoding="utf-8")
        subprocess.run([
            "timeout", "120", chromium, "--headless=new", "--no-sandbox", "--disable-gpu",
            "--hide-scrollbars", "--force-device-scale-factor=2", "--allow-file-access-from-files",
            f"--window-size={width},{height}", f"--screenshot={OUT / name}",
            "--virtual-time-budget=3000", f"--user-data-dir={d}/prof", f.as_uri(),
        ], check=True, capture_output=True)
    print("wrote", name)


UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = "abcdefghijklmnopqrstuvwxyz"
FIGS = "0123456789"
PUNCT = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
HAN = "開始遊戲勝利失敗分數等級金幣麻將大老二你好香港永"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main(chromium, inter, fredoka, ref_tc=None):
    OUT.mkdir(exist_ok=True)

    # 1. alphabet
    w = 1600
    cells = "".join(f'<div class="cell" style="height:120px;font-size:84px">{esc(c)}</div>' for c in UPPER + LOWER + FIGS + PUNCT)
    body = f"""<p class="label">Pip Trial Regular, 95 printable ASCII glyphs</p>
<div class="grid" style="grid-template-columns:repeat(13,1fr)">{cells}</div>"""
    shot(chromium, page(body, inter, fredoka, w), "01-glyph-set.png", w, 1180)

    # 2. pangram at sizes
    pg = "Sphinx of black quartz, judge my vow. 0123456789"
    rows = "".join(
        f'<div class="row"><p class="label">{s} px</p><div style="font-size:{s}px;line-height:1.15">{esc(pg)}</div></div>'
        for s in (96, 56, 32, 20, 14, 11)
    )
    body = rows + f"""<div class="row"><p class="label">Kerning on</p><div style="font-size:88px">AVATAR · Today · Typo · LT Wave · P. F. Yo</div></div>"""
    shot(chromium, page(body, inter, fredoka, 2400), "02-pangram-sizes.png", 2400, 1240)

    # 3. game UI mock
    body = f"""<div class="game">
<div style="display:flex;justify-content:space-between;align-items:center;font-size:30px;opacity:.9">
  <span>Stage 7 · Candy Docks</span><span>♥ 3 &nbsp; ⏱ 01:42</span></div>
<div style="font-size:120px;line-height:1;margin:34px 0 8px;color:#FFD84A;letter-spacing:.01em">LEVEL UP!</div>
<div style="font-size:52px">Score 12,480 <span style="opacity:.6">/ best 11,905</span></div>
<div style="margin-top:34px;display:flex;gap:16px">
  <span class="pill" style="background:#FFD84A;color:#1B1640">Play again</span>
  <span class="pill" style="background:rgba(255,255,255,.14)">Next level →</span></div>
<div style="margin-top:30px;font-size:18px;opacity:.75">Coins 4,096 · Gems 27 · Rank #318 · Tap to continue</div>
</div>"""
    shot(chromium, page(body, inter, fredoka, 1200), "03-game-ui.png", 1200, 640)

    # 4. comparison strip
    line = "LEVEL UP! Score 12,480"
    small = "Quick wins: tap Play, collect 3 stars, unlock world 2."
    faces = [("Pip Trial", "Pip", 400), ("Fredoka", "FredokaRef", 500), ("Inter", "InterRef", 500)]
    rows = "".join(
        f'<div class="cmp"><p class="label" style="margin:0">{n}</p><div><div style="font-family:{f};font-weight:{wt};font-size:84px;line-height:1.1">{line}</div>'
        f'<div style="font-family:{f};font-weight:{wt};font-size:22px;margin-top:10px">{small}</div></div></div>'
        for n, f, wt in faces
    )
    body = f'<p class="label">Same text, same size: Pip Trial against Fredoka Medium and Inter Medium</p>{rows}'
    shot(chromium, page(body, inter, fredoka, 1500), "04-comparison.png", 1500, 820)

    # 5. Han: derived from Noto Sans TC, beside the same weight unmodified
    if not ref_tc:
        return
    big = "".join(
        f'<div class="cell" style="height:150px"><div style="font-family:PipTC;font-size:104px;line-height:1">{c}</div></div>'
        f'<div class="cell" style="height:150px"><div style="font-family:RefTC;font-size:104px;line-height:1;color:{MUTED}">{c}</div></div>'
        for c in HAN
    )
    words = ["開始遊戲", "勝利！", "失敗", "分數 12,480", "等級 7", "金幣 4,096", "麻將", "大老二", "你好，香港"]
    wl = " · ".join(words)
    body = f"""<style>@font-face {{ font-family: RefTC; src: url("{Path(ref_tc).resolve().as_uri()}"); }}</style>
<p class="label">Pip Trial TC (black) beside Noto Sans TC at the same weight, unmodified (grey). Structure from Source Han Sans; rounding by rule</p>
<div class="grid" style="grid-template-columns:repeat(12,1fr)">{big}</div>
<div class="cmp" style="margin-top:28px"><p class="label" style="margin:0">Pip Trial TC<br>28 / 16 px</p>
<div><div style="font-family:Pip,PipTC;font-size:28px">{wl}</div><div style="font-family:Pip,PipTC;font-size:16px;margin-top:8px">{wl}</div></div></div>
<div class="cmp"><p class="label" style="margin:0">Noto Sans TC<br>same weight<br>28 / 16 px</p>
<div style="font-family:Pip,RefTC"><div style="font-size:28px">{wl}</div><div style="font-size:16px;margin-top:8px">{wl}</div></div></div>"""
    shot(chromium, page(body, inter, fredoka, 2000), "05-han-trial.png", 2000, 1140)


def han_v3(chromium, inter, fredoka, v3):
    """Brush variants rendered from the decoded stroke data, beside Noto Sans TC."""
    v3 = Path(v3)
    faces = [("Noto Sans TC 500 (reference)", "RefV3", MUTED)] + [
        (f"Brush: {n}", f"B{n}", INK) for n in ("pebble", "pop", "block")]
    fonts = "".join(
        f'@font-face {{ font-family: B{n}; src: url("{(v3 / f"brush-{n}.woff2").as_uri()}"); }}'
        for n in ("pebble", "pop", "block"))
    fonts += f'@font-face {{ font-family: RefV3; src: url("{(v3 / "noto-ref-500.ttf").as_uri()}"); }}'
    words = "開始遊戲 · 勝利 · 失敗 · 分數 12,480 · 等級 7 · 金幣 4,096 · 麻將 · 大老二 · 你好香港"
    rows = "".join(
        f'<div class="cmp" style="grid-template-columns:230px 1fr"><p class="label" style="margin:0">{label}</p>'
        f'<div><div style="font-family:{fam};font-size:66px;line-height:1.15;color:{col};letter-spacing:.02em">{HAN}</div>'
        f'<div style="font-family:Pip,{fam};font-size:26px;margin-top:10px;color:{col}">{words}</div>'
        f'<div style="font-family:Pip,{fam};font-size:15px;margin-top:6px;color:{col}">{words}</div></div></div>'
        for label, fam, col in faces)
    body = f"""<style>{fonts}</style>
<p class="label">Han v3: standard stroke skeletons re-drawn by three parametric brushes, rendered from the compact stroke file (decoded), beside Noto Sans TC</p>{rows}"""
    shot(chromium, page(body, inter, fredoka, 2000), "06-han-v3-brushes.png", 2000, 1180)
    big = "永大港數將你戲"
    rows = "".join(
        f'<div class="cmp" style="grid-template-columns:230px 1fr"><p class="label" style="margin:0">{label}</p>'
        f'<div style="font-family:{fam};font-size:170px;line-height:1.1;color:{col};letter-spacing:.06em">{big}</div></div>'
        for label, fam, col in faces)
    body = f"""<style>{fonts}</style><p class="label">Han v3 close-up: stroke ends, contrast and hooks per brush</p>{rows}"""
    shot(chromium, page(body, inter, fredoka, 2000), "07-han-v3-closeup.png", 2000, 1000)


def han_v4(chromium, inter, fredoka, d, out="08-han-v4.png", title=None):
    """Before (v3 pebble), after (v4 UI), and Noto Sans TC 500, at 64 px and in UI lines."""
    d = Path(d)
    fonts = "".join(f'@font-face {{ font-family: {fam}; src: url("{(d / f).as_uri()}"); }}' for fam, f in
                    (("V3", "v3-pebble.woff2"), ("V4", "v4.woff2"), ("RefV4", "noto-ref-500.ttf")))
    words = "開始遊戲 · 勝利 · 失敗 · 分數 12,480 · 等級 7 · 金幣 4,096 · 麻將 · 大老二 · 你好香港"
    faces = [("Before: v3 pebble", "V3", INK), ("After: v4 UI", "V4", INK), ("Noto Sans TC 500", "RefV4", MUTED)]
    rows = "".join(
        f'<div class="cmp" style="grid-template-columns:200px 1fr"><p class="label" style="margin:0">{label}</p>'
        f'<div><div style="font-family:{fam};font-size:64px;line-height:1.15;color:{col}">{HAN}</div>'
        f'<div style="font-family:Pip,{fam};font-size:28px;margin-top:10px;color:{col}">{words}</div>'
        f'<div style="font-family:Pip,{fam};font-size:16px;margin-top:6px;color:{col}">{words}</div></div></div>'
        for label, fam, col in faces)
    title = title or "Han v4: calligraphic skeletons simplified by rule, one near-monoline UI brush, beside Noto Sans TC"
    body = f"<style>{fonts}</style><p class=\"label\">{title}</p>{rows}"
    shot(chromium, page(body, inter, fredoka, 2000), out, 2000, 900)


if __name__ == "__main__":
    if len(sys.argv) > 6:
        han_v4(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[6], *sys.argv[7:9])
    elif len(sys.argv) > 5:
        han_v3(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[5])
    else:
        main(*sys.argv[1:5])
