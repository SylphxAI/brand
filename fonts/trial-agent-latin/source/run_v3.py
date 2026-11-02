"""Run the v3 Han trial: stroke skeletons, encode, decode, brush fonts, sizes.

    python run_v3.py <mmh-dir> <NotoSansTC[wght].ttf> <v2 PipTrialTC.ttf> <work-dir>
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

OUT = Path(__file__).resolve().parent.parent


def woff2_subset(font_or_path, text):
    f = TTFont(font_or_path) if not isinstance(font_or_path, TTFont) else font_or_path
    opt = subset.Options()
    opt.layout_features = []
    opt.hinting = False
    opt.flavor = "woff2"
    opt.name_IDs = []
    opt.notdef_outline = False
    s = subset.Subsetter(opt)
    s.populate(text=text)
    s.subset(f)
    b = io.BytesIO()
    f.flavor = "woff2"
    f.save(b)
    return len(b.getvalue())


def main(mmh, noto, v2, work):
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    report = {}
    t0 = time.perf_counter()
    skel, dic = hs.raw_skeletons(mmh, set(hs.HAN))
    skel = {c: skel[c] for c in hs.HAN}
    ref = hs.noto_instance(noto, hs.HAN)
    report["skeleton_seconds_per_char"] = round((time.perf_counter() - t0) / len(hs.HAN), 3)
    ref.save(work / "noto-ref-500.ttf")
    blob, lib, plan = hs.encode(skel, dic)
    (work / "han24.pips").write_bytes(blob)
    chars = hs.decode(blob)
    # quantisation alone: without sharing, strokes decode in their own order
    plain = hs.decode(hs.encode(skel, dic, share=False)[0])
    err = [math.dist(p, q) for ch in skel for a, b in zip(skel[ch], plain[ch]) for p, q in zip(a, b)]
    report["quantisation_mean_error_units"] = round(sum(err) / len(err), 2)
    report["quantisation_max_error_units"] = round(max(err), 2)
    report["pips_brotli_without_sharing_24"] = len(brotli.compress(hs.encode(skel, dic, share=False)[0], quality=11))
    report["shared_components_24"] = [f"{k[0]}:{k[1]}" for k, _, _ in lib]
    for name, B in hs.BRUSHES.items():
        t0 = time.perf_counter()
        p = work / f"brush-{name}.ttf"
        hs.build_font(chars, B, f"Pip Han {name}", p)
        report[f"brush_{name}_ms_per_char"] = round((time.perf_counter() - t0) / len(chars) * 1000)
        f = TTFont(p)
        f.flavor = "woff2"
        f.save(work / f"brush-{name}.woff2")
    text = hs.HAN
    report["bytes_24"] = {
        "noto_tc_500_woff2": woff2_subset(work / "noto-ref-500.ttf", text),
        "v2_rounded_woff2": woff2_subset(v2, text),
        "pips_raw": len(blob),
        "pips_brotli": len(brotli.compress(blob, quality=11)),
    }
    if len(sys.argv) > 5:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        return
    # large set: every Make Me a Hanzi character in Big5 (Traditional), unsnapped medians
    big, dic_all = hs.raw_skeletons(mmh)
    def is_big5(c):
        try:
            c.encode("big5")
            return True
        except UnicodeEncodeError:
            return False
    trad = {c: s for c, s in big.items() if is_big5(c)}
    report["large_set_chars"] = len(trad)
    blob_l, lib_l, plan_l = hs.encode(trad, dic_all)
    report["large_set_pips_brotli_without_sharing"] = len(brotli.compress(hs.encode(trad, dic_all, share=False)[0], quality=11))
    report["large_set_pips_raw"] = len(blob_l)
    report["large_set_pips_brotli"] = len(brotli.compress(blob_l, quality=11))
    report["large_set_library_components"] = len(lib_l)
    placed = sum(len(p) for p, _ in plan_l.values())
    report["large_set_placements"] = placed
    uses = {}
    for p, _ in plan_l.values():
        for lid, _ in p:
            uses[lid] = uses.get(lid, 0) + 1
    top = sorted(uses.items(), key=lambda t: -t[1])[:20]
    report["large_set_top_components"] = [f"{lib_l[i][0][0]}({lib_l[i][0][1]}) x{n}" for i, n in top]
    text_l = "".join(trad)
    report["large_set_noto_tc_500_woff2"] = woff2_subset(hs.noto_instance(noto, text_l), text_l)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    (work / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:5])
