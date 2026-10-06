"""Render the specimen PNGs with headless Chromium (real shaping and kerning).

    python specimens.py <chromium> <inter.ttf> <fredoka.ttf>

Inter and Fredoka (SIL OFL) are only loaded from local paths for the
comparison image; they are not shipped or copied. Noto Sans CJK TC comes from
the system's font set.
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


def main(chromium, inter, fredoka):
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

    # 5. Han trial next to Noto Sans CJK TC
    big = "".join(
        f'<div class="cell" style="height:150px;flex-direction:column"><div style="font-family:PipTC;font-size:104px;line-height:1">{c}</div></div>'
        f'<div class="cell" style="height:150px"><div style="font-family:\'Noto Sans CJK TC\';font-size:104px;line-height:1;color:{MUTED}">{c}</div></div>'
        for c in HAN
    )
    words = ["開始遊戲", "勝利！", "失敗", "分數 12,480", "等級 7", "金幣 4,096", "麻將", "大老二", "你好，香港"]
    wl = " · ".join(words)
    body = f"""<p class="label">24 Han trial glyphs: Pip Trial TC (black) beside Noto Sans CJK TC Regular (grey)</p>
<div class="grid" style="grid-template-columns:repeat(12,1fr)">{big}</div>
<div class="cmp" style="margin-top:28px"><p class="label" style="margin:0">Pip Trial TC<br>28 / 16 px</p>
<div><div style="font-family:Pip,PipTC;font-size:28px">{wl}</div><div style="font-family:Pip,PipTC;font-size:16px;margin-top:8px">{wl}</div></div></div>
<div class="cmp"><p class="label" style="margin:0">Noto Sans CJK TC<br>28 / 16 px</p>
<div style="font-family:'Noto Sans CJK TC'"><div style="font-size:28px">{wl}</div><div style="font-size:16px;margin-top:8px">{wl}</div></div></div>"""
    shot(chromium, page(body, inter, fredoka, 2000), "05-han-trial.png", 2000, 1120)


if __name__ == "__main__":
    main(*sys.argv[1:4])
