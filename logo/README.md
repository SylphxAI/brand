# Sylphx logo

## Current

| File | Role |
|------|------|
| `current/icon.png` | Primary icon (portfolio / general) |
| `current/icon-512.png` | High-res icon |
| `current/icon-github.jpg` | Org avatar snapshot |

## Gaps

Legacy checklist expected SVG primary + mono black/white wordmarks — **not yet present** as files. Add under `current/` when available; do not invent replacements without design ownership.

## Reverse-engineered vectors (v0)

**Added:** complete SVG pack derived from existing rasters / masters.

icon.svg wordmark.svg mono variants

See `reverse/README.md` for method and accuracy disclaimer.
Primary shipping vectors live in `current/*.svg` with PNG previews `*-from-svg.png` / `*-512.png`.

## Recraft vectorize (FAL)

Primary clean SVG from raster via `fal-ai/recraft/vectorize`:

- `*-recraft.svg` — Recraft output (preferred reverse vector)
- `*-recraft-512.png` / preview PNGs
- Previous drafts kept as `*.pre-recraft` / potrace / vision where present

Epiow: `icon-recraft.svg` is an alternate; **canonical master remains `logo.svg`**.
