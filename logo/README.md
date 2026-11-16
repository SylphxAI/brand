# Sylphx logo

The mark is two wings and one current: two identical solid blades, the
second the first turned 180° about the centre, that read as an S, a pair of
wings and a stream of air. The colour versions fill the pair with one
gradient, the current (deep blue `#2F4BFF`, azure `#2FA8FF`, pale sky
`#9FE3FF`). The wordmark is *Sylphx* in Geist SemiBold, outlined. Every file
here is drawn by
[`construction/mark.py`](construction/mark.py) from
[`construction/mark.spec.json`](construction/mark.spec.json). Never edit an
output by hand: change the spec and rerun (see the repository README).

## Files

| Need | File |
| --- | --- |
| Lockup, light surfaces | `svg/sylphx-lockup-colour.svg` |
| Lockup, dark surfaces | `svg/sylphx-lockup-colour-on-dark.svg` |
| One colour | `svg/sylphx-lockup-black.svg`, `svg/sylphx-lockup-white.svg` |
| Mark alone | `svg/sylphx-symbol-{colour,colour-on-dark,black,white}.svg` |
| Wordmark alone | `svg/sylphx-wordmark-{ink,paper,black,white}.svg` |
| Rounded tile (docs, slides) | `svg/sylphx-tile.svg` |
| Ready-made PNGs | `png/` (lockups and wordmarks 1600 px wide, marks 1024 px) |
| Browser tab | `favicon/favicon.svg`, `favicon/favicon.ico` (16, 32, 48), `favicon/favicon-{16,32,48,192,512}.png`, `favicon/apple-touch-icon-180.png` |
| App stores and avatars | `app-icon/sylphx-app-icon-1024.{svg,png}` (full bleed; the store applies its corner mask) |
| Android adaptive icon | `app-icon/sylphx-android-foreground.svg` and `-432.png` on the ink field `#0A0D14` |
| Usage sheet | `sheet/usage.png` |

SVG view boxes are tight to the artwork. Clear space is added where the logo
is placed (a quarter of the mark's height), not inside the file.

```html
<link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon-180.png">
```

## Construction

The blade is one closed path of three cubic curves on a 64 grid:
`M58 6C34 2 8 14 7 39 17 27 33 21 52 23 56 18 58 12 58 6z`. The second blade
is the same path turned 180° about the centre (32, 32), so the pair is
point-symmetric and its centre is the centre of the grid. The pair's ink
spans x 6 to 58 and y 5.244 to 58.756; the masters are output on a 512 grid
(every coordinate times 8) with coordinates written out, not transformed.

The current is one linear gradient across the pair, not one per blade, in
user space: from 10% across the top edge of the pair's bounding box to 90%
across its bottom edge, with stops at 0, 0.55 and 1. Each file gives its
gradient its own id (`sx-current-<file>`), so files inlined on one page do
not collide. The black and white versions are flat.

In the lockup the mark is 1.5 times the wordmark's cap height, centred on it,
with a gap of 0.30 mark heights. The tile is a 512 square with a corner
radius of 116 on the ink field, the mark 0.60 of its width and centred.

## Small sizes

`favicon/favicon.svg` is the tile as a clean vector, and every favicon PNG
and ICO frame is rendered from it; nothing is snapped to pixels. At 16 px the
gradient has too few pixels to read against the ink field (its deep-blue end
goes dim), so the 16 px PNG and the 16 px ICO frame draw the mark in white.
From 32 px up the mark is in the current.

## Provenance

- **Designed, not traced.** The mark was drawn as geometry on 2026-11-16 as
  direction Altitude, an owner-authorised full redesign
  ([../directions/2026-11-altitude.md](../directions/2026-11-altitude.md)).
  It replaces the mark of direction Engineered (2026-09-28) and
  the two before it (a blocky S and an amber ring with a dot); those are in
  Git history only.
- **Type:** Geist SemiBold 1.900, from the `geist` npm package 1.9.2
  (`construction/fonts/`, SIL Open Font License 1.1, copyright Vercel,
  `construction/fonts/Geist-OFL.txt`), shaped with HarfBuzz and outlined with
  fontTools, tracking −0.04em.
- **Rendering:** resvg for every PNG; Pillow for the ICO and the sheet.
- **Hashes:** [`MANIFEST.sha256`](MANIFEST.sha256) lists the SHA-256 of every
  shipped file, the spec, the generator and the fonts. Rebuilding from the
  spec with the pinned versions in
  [`construction/requirements.txt`](construction/requirements.txt)
  reproduces every SVG, PNG and ICO byte for byte, and CI redraws them on
  every change: a hand-edited or traced file fails the build.
