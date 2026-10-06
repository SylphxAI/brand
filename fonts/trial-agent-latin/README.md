# Pip Trial (experiment)

A trial display typeface made in code, to judge by eye
how good a face made this way can be. It is not part of the brand and no
surface uses it.

- **Pip Trial Regular**: the 95 printable ASCII glyphs, kerning for the common
  pairs (AV, To, Ty, LT, P., and more), tabular figures (every digit is the
  same width, so scores and timers do not jitter), and a tailed `l` that tells
  `l`, `I` and `1` apart in UI text.
- **Pip Trial TC Regular**: 24 Traditional Chinese characters
  (開始遊戲勝利失敗分數等級金幣麻將大老二你好香港永) in Pip's style. Their
  structure comes unchanged from Noto Sans TC (the Source Han Sans design,
  Taiwan forms, SIL OFL 1.1); only the outlines are restyled, by rule.

- **Han v3 trial** ([han-v3/](han-v3/)): the same 24 characters as stroke
  skeletons drawn by our own parametric brushes, stored as components plus
  strokes. That directory is under the Arphic Public License; see its README.

Latin metrics: 1000 units per em, x-height 520, cap height 700, ascender
740, descender -200, one stroke width of 104, overshoot 12 on round letters.

## How it is made

**Latin.** Every glyph is a set of centre lines (lines, cubic curves and
elliptical arcs) written in [source/latin.py](source/latin.py).
[source/skeleton.py](source/skeleton.py) expands each line at one width with
round caps and joins, merges overlaps into one clean outline in TrueType
direction, and converts it to quadratic curves. Equal stems follow by
construction; side bearings come from each glyph's ink box. Nothing is traced
from or copied out of another font.

**Traditional Chinese.** [source/derive_tc.py](source/derive_tc.py) takes
Noto Sans TC and applies three rules that read only the outline, so they run
the same on any character:

1. Weight: the instance of its weight axis (500) whose single-stroke stem
   matches Pip's Latin stem. The source's own weight design keeps dense
   characters open.
2. Rounded terminals: a morphological opening by 26 units (erode, then
   dilate, with a disc) rounds every convex corner. Thin parts the opening
   would delete (tapered tips, small dots) are kept with a smaller radius.
3. Soft joins: a closing by 9 units eases the inner corners where strokes meet.

The morphology runs on a 2-pixels-per-unit bitmap (exact distance maps), and
potrace turns the result back into smooth curves.

```bash
python -m venv .venv && .venv/bin/pip install -r source/requirements.txt
.venv/bin/python source/build.py                                  # PipTrial-Regular .ttf and .woff2
.venv/bin/python source/derive_tc.py NotoSansTC[wght].ttf ref.ttf # PipTrialTC-Regular, plus the unmodified instance
.venv/bin/python source/specimens.py /usr/bin/chromium Inter.ttf Fredoka.ttf ref.ttf  # specimens/*.png
```

The specimens are rendered by headless Chromium, so shaping and kerning are
the browser's. Inter and Fredoka are only loaded for the comparison image and
are not shipped here.

## Specimens

![Glyph set](specimens/01-glyph-set.png)
![Pangram at sizes](specimens/02-pangram-sizes.png)
![Game UI](specimens/03-game-ui.png)
![Comparison](specimens/04-comparison.png)
![Han trial](specimens/05-han-trial.png)

## Licence

Pip Trial: Copyright 2026 Sylphx Limited. Pip Trial TC: Copyright 2014-2021
Adobe, with Reserved Font Name 'Source', and Copyright 2026 Sylphx Limited.
Both under the SIL Open Font License 1.1 ([OFL.txt](OFL.txt)).
