"""Before/after sheet for one polish round: previous round, this round, and
Noto Sans CJK TC, for the same characters, rendered in headless Chromium.

    python compare.py <chromium> <before.woff2> <after.woff2> <out.png> "<title>"
"""

import subprocess
import sys
import tempfile
from pathlib import Path

HAN = "開始遊戲勝利失敗分數等級金幣麻將大老二你好香港永"
WORDS = "開始遊戲 · 勝利 · 失敗 · 分數 12,480 · 等級 7 · 金幣 4,096 · 麻將 · 大老二 · 你好香港"


def main(chromium, before, after, out, title):
    latin = Path(after).resolve().parent.parent / "PipTrial-Regular.woff2"
    if not latin.exists():
        latin = Path(__file__).resolve().parent.parent / "PipTrial-Regular.woff2"
    cells = "".join(
        f'<div class="t"><div class="c" style="font-family:B">{c}</div><div class="c" style="font-family:A">{c}</div>'
        f'<div class="c n">{c}</div></div>' for c in HAN)
    html = f"""<!doctype html><meta charset="utf-8"><style>
@font-face {{ font-family: B; src: url("{Path(before).resolve().as_uri()}"); }}
@font-face {{ font-family: A; src: url("{Path(after).resolve().as_uri()}"); }}
@font-face {{ font-family: L; src: url("{latin.as_uri()}"); }}
body {{ margin:0; background:#F2EEE6; color:#15130F; padding:40px 48px; width:2000px; box-sizing:border-box; font-family:'Noto Sans CJK TC'; }}
h1 {{ font: 500 26px 'Noto Sans CJK TC'; margin:0 0 6px; }} p {{ margin:0 0 22px; color:#6E675C; font-size:18px; }}
.g {{ display:grid; grid-template-columns:repeat(6,1fr); gap:14px 22px; }}
.t {{ display:grid; grid-template-columns:repeat(3,1fr); border:1px solid #DDD5C6; background:#FBF8F2; }}
.c {{ font-size:84px; line-height:1; text-align:center; padding:12px 0; }}
.n {{ color:#8A8274; }}
.w {{ margin-top:26px; display:grid; grid-template-columns:150px 1fr; gap:10px 16px; align-items:baseline; font-size:26px; }}
.w span {{ font-size:16px; color:#6E675C; }}
</style><h1>{title}</h1><p>Each box: before (left) · after (middle) · Noto Sans CJK TC Regular (right, grey)</p>
<div class="g">{cells}</div>
<div class="w"><span>Before, 26 px</span><div style="font-family:L,B">{WORDS}</div>
<span>After, 26 px</span><div style="font-family:L,A">{WORDS}</div>
<span>Noto, 26 px</span><div>{WORDS}</div>
<span>After, 15 px</span><div style="font-family:L,A;font-size:15px">{WORDS}</div></div>"""
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "p.html"
        f.write_text(html, encoding="utf-8")
        subprocess.run(["timeout", "120", chromium, "--headless=new", "--no-sandbox", "--disable-gpu",
                        "--hide-scrollbars", "--force-device-scale-factor=2", "--allow-file-access-from-files",
                        "--window-size=2000,860", f"--screenshot={Path(out).resolve()}", "--virtual-time-budget=3000",
                        f"--user-data-dir={d}/prof", f.as_uri()], check=True, capture_output=True)
    print("wrote", out)


if __name__ == "__main__":
    main(*sys.argv[1:6])
