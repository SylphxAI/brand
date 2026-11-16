# Using the Sylphx brand

The usage sheet shows the rules at a glance: [logo/sheet/usage.png](../logo/sheet/usage.png).
Values below come from [tokens/brand.tokens.json](../tokens/brand.tokens.json);
if this page and the tokens disagree, the tokens win and this page is fixed.

The direction is *Altitude* (2026-11-16,
[directions/2026-11-altitude.md](../directions/2026-11-altitude.md)): a sylph
is a spirit of the air, and the identity is high, clear air. Near-neutral cool
surfaces, ink for primary actions, one azure accent, and one gradient, the
current, kept for the mark and rare brand moments.

## Logo

- Use the files in `logo/`, never a redrawn, traced or retyped logo.
- **The mark** is two identical solid blades, the second the first turned
  180° about the centre. Together they read as an S, a pair of wings and a
  stream of air. The wordmark is *Sylphx* in Geist SemiBold, tracking
  −0.04em, outlined.
- **Lockup** (mark + wordmark) wherever there is room; the **mark alone** only
  where the name is already visible or space is square (favicon, app icon,
  avatar, the console's top-left corner). In the lockup the mark is 1.5 cap
  heights tall, centred on the cap height, with a gap of 0.30 mark heights.
- **Colour** version on light surfaces: mark in the current, wordmark in ink.
  **Colour-on-dark** on dark surfaces and code: the same mark, wordmark in
  paper. **Black** or **white** only where one colour is all the medium
  allows.
- **Tile:** the mark in the current on a rounded ink field, for docs, slides
  and the favicon. App icons are the same field full-bleed; the platform
  applies its own corner mask.
- **Clear space:** a quarter of the mark's height on every side.
- **Minimum size:** mark 16 px; lockup 80 px wide. In a browser tab use the
  favicon files: at 16 px they draw the mark in white, because the gradient
  has too few pixels to read.
- Don't recolour the mark or change the gradient's stops or direction, fill
  each blade with its own gradient, rotate, flip, outline, add shadows or
  glows, separate or re-space the blades, stretch, re-space the lockup, or
  set the wordmark in another typeface.

## Colour

Cool near-neutrals carry everything. Light is the site default; the console
follows the system setting, and dark is a full equal. Use semantic tokens
(`--sx-background`, `--sx-text`, `--sx-accent`, …), never raw values.

| Role | Token | Light | Dark |
| --- | --- | --- | --- |
| Page | `--sx-background` | `#FAFBFD` | `#06080C` |
| Cards, inputs, panels | `--sx-surface` | `#FFFFFF` | `#0C0F15` |
| Menus, popovers, dialogs | `--sx-surface-raised` | `#FFFFFF` | `#12161E` |
| Wells, console sidebar | `--sx-surface-sunken` | `#F1F4F8` | `#040508` |
| Text, and the primary action (ink) | `--sx-text` | `#0A0D14` | `#EEF1F6` |
| Secondary text | `--sx-text-secondary` | `#4B5565` | `#9BA4B4` |
| Tertiary text | `--sx-text-tertiary` | `#667085` | `#7F8999` |
| Dividers, card edges | `--sx-border` | `#E2E7EE` | `#1C222D` |
| Control borders | `--sx-border-control` | `#828DA0` | `#5A6577` |
| Azure | `--sx-accent` | `#1463FF` | `#4D94FF` |
| Azure text and links | `--sx-accent-text` | `#0F56E6` | `#6AA8FF` |
| Selection tint | `--sx-accent-soft` / `--sx-on-accent-soft` | `#E6F0FF` / `#0B3A9E` | `#0F2347` / `#C7DEFF` |
| Code ground, both themes | `--sx-code-background` / `--sx-code-text` | `#0A0D14` / `#D9DFEA` | the same |
| The current | `--sx-gradient-current` | `#2F4BFF` → `#2FA8FF` (55%) → `#9FE3FF`, 135° | the same |

- **Ink is the primary action.** The one primary button of a view is filled
  with `--sx-text` and lettered in `--sx-background`; it inverts with the
  theme.
- **Azure is links, focus and selection.** `--sx-accent-text` for links,
  `--sx-accent` for the focus ring, selected controls and current-place
  markers, `--sx-accent-soft` for selected rows. Hover of an azure fill is
  `--sx-accent-hover`.
- **The gradient is for the mark and at most one brand moment per page** (a
  hero line, an illustration, a launch graphic). Never on text smaller than
  display, controls, borders or status. `--sx-mark-dawn` (`#FFB58A`) is a
  warm counterpoint for illustration only.
- **Status colours are for status only:** success, warning, danger, info.
- **On code**, the ink ground (`--sx-code-background`, dark in both themes),
  status text uses `--sx-status-*-on-dark`, and comments and the `$` prompt
  use `--sx-code-comment`.
- **Contrast:** every text token meets 4.5:1 and every control border 3:1 on
  every surface, in both themes (WCAG 2.2 AA). A new token meets the same bar.
- **Depth** comes from surface steps (sunken, page, raised) and 1 px borders.
  Only menus, popovers and dialogs float, with `--sx-shadow-float`. No glass,
  glows or neon.

## Type

- **Geist** for interface and display, weights 400, 500 and 600 only. The
  scale is `--sx-type-*`: display 72 px and headline 44 px at weight 500,
  headline 24 px and title 16 px at 600, body 18, 15 and 13 px, labels 13 px.
  Display and headlines tighten their tracking (−0.045em to −0.02em); display
  drops to 40 px on mobile.
- **Geist Mono** for code, commands, resource names, ids, mono labels (upper
  case, +0.06em) and every number that is compared, with tabular,
  slashed-zero figures (`--sx-font-data-features`).
- **Instrument Serif italic** (`--sx-font-accent`) for a word or short phrase
  inside a display line, at most once per page. Never for body text, the
  interface or the console.
- All three are OFL; self-host them, never load them from a third party. Copy
  [fonts/fonts.css](../fonts/fonts.css) with the files beside it (its URLs are
  relative, so any path works); it is the only place the family names meet
  the files.
- Chinese and Japanese use **Noto Sans TC**, **SC** and **JP** (OFL), next in
  `--sx-font-sans`, chosen by the page `lang`; CJK headlines use 0 tracking
  and 1.2 line height. This repository does not ship those files yet, so they
  fall through to the system CJK face.

## Icons

20 px icons on a 24 px grid, 1.5 px stroke, round joins, no fills; the icon
takes the text colour of its context, and the accent only when it marks the
current place. One icon per concept across site, docs and console.

## Radius

6 px for tags in tables, 10 px for buttons, inputs and chips, 14 px for cards,
code and dialogs, 20 px for hero panels and screenshots, full for badges and
avatars (`--sx-radius-sm`, `-md`, `-lg`, `-xl`, `-full`).

## Motion

- 180 ms, `cubic-bezier(0.2, 0, 0, 1)` for every state change: quick out,
  soft settle, never a bounce.
- Motion shows what changed; nothing moves for decoration. Numbers roll on
  change; focus rings snap.
- Under `prefers-reduced-motion`, durations are zero.

## Layout

- 4 px spacing grid. Marketing pages: 12 columns, max 1200 px, 24 px gutters,
  120 px between sections (72 px on mobile).
- Console: 248 px sidebar, 64 px top bar, content up to 1440 px.
- 36 px controls, 40 px table rows, 44 px touch targets and hero calls to
  action.
- Focus is a 2 px azure ring with a 2 px offset.
