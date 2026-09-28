# Using the Sylphx brand

The usage sheet shows the rules at a glance: [logo/sheet/usage.png](../logo/sheet/usage.png).
Values below come from [tokens/brand.tokens.json](../tokens/brand.tokens.json);
if this page and the tokens disagree, the tokens win and this page is fixed.

## Logo

- Use the files in `logo/`, never a redrawn, traced or retyped logo.
- **Lockup** (mark + wordmark) wherever there is room; the **mark alone** only
  where the name is already visible or space is square (favicon, app icon,
  avatar, the console's top-left corner).
- **Colour** version on paper and light surfaces: cobalt under-current, ink
  over-current and wordmark. **Colour-on-dark** on ink and dark surfaces.
  **Black** or **white** only where one colour is all the medium allows.
- **Clear space:** a quarter of the mark's height on every side.
- **Minimum size:** mark 16 px (use the pixel-snapped favicons below 48 px);
  lockup 88 px wide.
- Don't recolour, rotate, outline, add effects, change the weave order,
  stretch, re-space the lockup, or set the wordmark in another typeface.

## Colour

Light is the default theme; dark is a full equal, chosen by the system
setting or the person. Use semantic tokens (`--sx-background`, `--sx-text`,
`--sx-accent`, …), never raw values.

| Role | Light | Dark |
| --- | --- | --- |
| Background (paper / ink) | `#F4F1EA` | `#121110` |
| Surface | `#FFFDF8` | `#191816` |
| Text | `#15130F` | `#F2EEE6` |
| Secondary text | `#55504A` | `#ABA59A` |
| Accent (cobalt) | `#2448F5` | `#6B86FF` |

- **Cobalt is the one accent.** It marks the primary action, the current
  place, links and focus. Never decoration, never a background wash larger
  than a badge.
- **Status colours are for status only:** success, warning, danger, info.
- **Contrast:** every text token meets 4.5:1 and every control border 3:1 on
  every surface, in both themes (WCAG 2.2 AA). A new token meets the same bar.
- No gradients, glows or glass on any surface. Depth comes from a 1 px
  border and surface steps.

## Type

- **IBM Plex Sans** for all text, interface and display (400, 500, 600).
  Display sizes use −0.03em tracking.
- **IBM Plex Mono** for code, resource names, ids, labels (upper case, +0.06em)
  and every number that is compared; tabular figures.
- Both are OFL; self-host them, never load them from a third party. Copy
  [fonts/fonts.css](../fonts/fonts.css) with the files beside it (its URLs are
  relative, so any path works); it is the only place the family names meet
  the files.
- Chinese and Japanese fall back to the platform's system CJK face at the
  same weights; never a web font for CJK.

## Icons

24 px grid, 1.75 px stroke, butt caps, miter joins, no fills; the icon takes
the text colour of its context, and the accent only when it marks the current
place. One icon per concept across site, docs and console.

## Motion

- 150 ms, linear-out (`cubic-bezier(0, 0, 0.2, 1)`) for every state change.
- Motion shows what changed; nothing moves for decoration. Numbers roll on
  change; focus rings snap.
- Under `prefers-reduced-motion`, durations are zero.

## Layout

- 4 px spacing grid; 32 px controls, 36 px table rows, 44 px touch targets.
- Radius 2–4 px. Structure is visible: hairline rules, mono section labels,
  aligned columns.
