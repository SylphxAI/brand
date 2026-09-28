# Sylphx logo

The mark is two currents that cross and weave into an x, the x of Sylphx:
the rising current (cobalt) passes under the falling one (ink). The wordmark
is *Sylphx* in IBM Plex Sans SemiBold, outlined. Every file here is drawn by
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
| Android adaptive icon | `app-icon/sylphx-android-foreground.svg` and `-432.png` on the ink field `#15130F` |
| Usage sheet | `sheet/usage.png` |

SVG view boxes are tight to the artwork. Clear space is added where the logo
is placed (a quarter of the mark's height), not inside the file.

```html
<link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon-180.png">
```

## Construction

On a 512 grid, each current is one cubic curve from one corner of a 300 × 300
square to the opposite corner, leaving and arriving horizontally (control
points 40 units past the centre line), stroked 70 units wide with flat ends.
The falling current is drawn whole; the rising current is cut where the
falling one crosses it, with a 28-unit gap on each side, so the weave reads
at every size. In the lockup the mark is 1.45 times the wordmark's cap
height, centred on it, with a gap of 0.36 mark heights.

## Small sizes

At 16 and 32 px the curves fall between pixels, so the favicons are snapped
to whole pixels: each pixel takes the tone covering most of it, and a current
wins a pixel it covers by 40% so the strokes stay continuous. The grids are
in [`construction/pixel-grids.txt`](construction/pixel-grids.txt) for review.
From 48 px up every file uses the vector.

## Provenance

- **Designed, not traced.** The mark was drawn as geometry on 2026-09-28 as
  part of direction Engineered, chosen from three complete directions
  ([../directions/README.md](../directions/README.md)). It replaces two
  earlier marks (a blocky S and an amber ring with a dot) and every traced
  or vectorised copy of them; those are in Git history only.
- **Type:** IBM Plex Sans SemiBold 3.201 (`construction/fonts/`, SIL Open
  Font License 1.1, `construction/fonts/IBM-Plex-OFL.txt`), shaped with
  HarfBuzz and outlined with fontTools, tracking −0.02em.
- **Rendering:** resvg for every PNG; Pillow for the ICO and the sheet.
- **Hashes:** [`MANIFEST.sha256`](MANIFEST.sha256) lists the SHA-256 of every
  shipped file, the spec, the generator and the fonts. Rebuilding from the
  spec reproduces the SVGs byte for byte.
