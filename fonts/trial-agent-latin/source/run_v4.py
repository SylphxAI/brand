"""Run the v4 Han trial: normalise skeletons by rule, encode, decode, brush, sizes.

    python run_v4.py <mmh-dir> <NotoSansTC[wght].ttf> <work-dir> [quick]
"""

import io
import json
import math
import sys
import time
from pathlib import Path

import brotli
from fontTools import subset
from fontTools.ttLib import TTFont

import hanstroke as hs
import hanv4


def woff2_size(path_or_font, text):
    f = path_or_font if isinstance(path_or_font, TTFont) else TTFont(path_or_font)
    opt = subset.Options()
    opt.layout_features = []
    opt.hinting = False
    opt.name_IDs = []
    opt.notdef_outline = False
    s = subset.Subsetter(opt)
    s.populate(text=text)
    s.subset(f)
    b = io.BytesIO()
    f.flavor = "woff2"
    f.save(b)
    return len(b.getvalue())


def main(mmh, noto, work, quick=None):
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    rep = {}
    raw, dic = hs.raw_skeletons(mmh, set(hs.HAN))
    raw = {c: raw[c] for c in hs.HAN}
    hs.build_font(raw, hs.BRUSHES["pebble"], "Before v3 pebble", work / "v3-pebble.ttf")
    t0 = time.perf_counter()
    norm = {c: hanv4.normalise(s, dic.get(c)) for c, s in raw.items()}
    rep["normalise_ms_per_char"] = round((time.perf_counter() - t0) / len(norm) * 1000, 1)
    blob, lib, _ = hs.encode(norm, dic)
    (work / "han24-v4.pips").write_bytes(blob)
    dec = hs.decode(blob)
    plain = hs.decode(hs.encode(norm, dic, share=False)[0])
    err = [math.dist(p, q) for c in norm for a, b in zip(norm[c], plain[c]) for p, q in zip(a, b)]
    rep["quantisation_mean_error_units"] = round(sum(err) / len(err), 2)
    t0 = time.perf_counter()
    hanv4.build_font(dec, "Pip Han v4", work / "v4.ttf")
    rep["brush_ms_per_char"] = round((time.perf_counter() - t0) / len(dec) * 1000)
    ref = hs.noto_instance(noto, hs.HAN)
    ref.save(work / "noto-ref-500.ttf")
    for n in ("v3-pebble", "v4"):
        f = TTFont(work / f"{n}.ttf")
        f.flavor = "woff2"
        f.save(work / f"{n}.woff2")
    rep["bytes_24"] = {
        "noto_tc_500_woff2": woff2_size(work / "noto-ref-500.ttf", hs.HAN),
        "v4_brushed_outlines_woff2": woff2_size(work / "v4.ttf", hs.HAN),
        "v4_pips_brotli": len(brotli.compress(blob, quality=11)),
        "v3_pips_brotli": len(brotli.compress(hs.encode(raw, dic)[0], quality=11)),
    }
    if not quick:
        big, dic_all = hs.raw_skeletons(mmh)

        def big5(c):
            try:
                c.encode("big5")
                return True
            except UnicodeEncodeError:
                return False

        trad = {c: s for c, s in big.items() if big5(c)}
        t0 = time.perf_counter()
        tn = {c: hanv4.normalise(s, dic_all.get(c)) for c, s in trad.items()}
        rep["large_set_chars"] = len(tn)
        rep["large_set_normalise_seconds"] = round(time.perf_counter() - t0, 1)
        rep["large_set_v4_pips_brotli"] = len(brotli.compress(hs.encode(tn, dic_all)[0], quality=11))
        rep["large_set_v3_pips_brotli"] = len(brotli.compress(hs.encode(trad, dic_all)[0], quality=11))
        text = "".join(trad)
        rep["large_set_noto_tc_500_woff2"] = woff2_size(hs.noto_instance(noto, text), text)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    (work / "report-v4.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:5])
