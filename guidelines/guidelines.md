# Using the Sylphx brand

The usage sheet shows the rules at a glance: [logo/sheet/usage.png](../logo/sheet/usage.png).
Values below come from [tokens/brand.tokens.json](../tokens/brand.tokens.json);
if this page and the tokens disagree, the tokens win and this page is fixed.

## Logo

- Use the files in `logo/`, never a redrawn, traced or retyped logo.
- **Lockup** (mark + wordmark) wherever there is room; the **mark alone** only
  where the name is already visible or space is square (favicon, app icon,
  avatar, the console's top-left corner).
- **Colour** version on light surfaces: cobalt under-current, ink
  over-current and wordmark. **Colour-on-dark** on dark surfaces and code.
  **Black** or **white** only where one colour is all the medium allows.
- **Clear space:** a quarter of the mark's height on every side.
- **Minimum size:** mark 16 px (use the pixel-snapped favicons below 48 px);
  lockup 88 px wide.
- Don't recolour, rotate, outline, add effects, change the weave order,
  stretch, re-space the lockup, or set the wordmark in another typeface.

## Colour

The interface follows the Sylphx DESIGN.md (`SylphxAI/cloud`, direction
*Clear air, one live current*): cool neutrals carry everything, and cobalt
comes in small doses. Light is the site default; the console follows the
system setting, and dark is a full equal. Use semantic tokens
(`--sx-background`, `--sx-text`, `--sx-accent`, …), never raw values.

| Role | Token | Light | Dark |
| --- | --- | --- | --- |
| Page (Clear Air) | `--sx-background` | `#F6F8FB` | `#080C14` |
| Cards, inputs, dialogs | `--sx-surface`, `--sx-surface-raised` | `#FFFFFF` | `#101623` |
| Wells, console sidebar | `--sx-surface-sunken` | `#EDF1F6` | `#05080E` |
| Text (Midnight) | `--sx-text` | `#0B1220` | `#E6EAF2` |
| Secondary text (Slate) | `--sx-text-secondary` | `#4A5466` | `#98A2B5` |
| Dividers, card edges | `--sx-border` | `#D6DCE6` | `#222B3B` |
| Control borders | `--sx-border-control` | `#7A8599` | `#5D687C` |
| Cobalt (Current Cobalt) | `--sx-accent` | `#2448F5` | `#6B86FF` |
| Cobalt text and links | `--sx-accent-text` | `#1E3BD0` | `#6B86FF` |
| Selection tint (Updraft) | `--sx-accent-soft` / `--sx-on-accent-soft` | `#E8EDFF` / `#1A2A80` | `#16204A` / `#C9D3FF` |
| Code ground, both themes | `--sx-code-background` / `--sx-code-text` | `#0B1220` / `#D7DEEA` | the same |

- **Cobalt is the one current.** It marks the primary action, links, focus,
  selection and diagram current lines: one cobalt-filled element per view.
  Hover is `--sx-accent-hover`.
- **Status colours are for status only:** success, warning, danger, info.
- **On code** — the Midnight ground (`--sx-code-background`, dark in both
  themes) — status text uses `--sx-status-*-on-dark`, and comments and the `$`
  prompt use `--sx-code-comment`.
- **Contrast:** every text token meets 4.5:1 and every control border 3:1 on
  every surface, in both themes (WCAG 2.2 AA). A new token meets the same bar.
- **Depth** comes from surface steps (sunken, page, raised) and 1 px borders.
  Only menus, popovers and dialogs float, with `--sx-shadow-float` (in dark,
  a 1 px `--sx-border-strong` edge instead). No warm beige, gradients, glass,
  glows or neon.

## Type

- **Inter** for interface and display, weights 400, 500 and 600 only. The
  scale is `--sx-type-*` (display 64 px, headlines 40 and 24 px, title 16 px,
  body 18, 15 and 13 px, labels 13 px); display and headlines tighten their
  tracking, display drops to 40 px on mobile.
- **JetBrains Mono** for code, commands, resource names, ids, mono labels
  (upper case, +0.08em) and every number that is compared, with tabular,
  slashed-zero figures (`--sx-font-data-features`).
- Both are OFL; self-host them, never load them from a third party. Copy
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

## Motion

- 150 ms, linear-out (`cubic-bezier(0, 0, 0.2, 1)`) for every state change.
- Motion shows what changed; nothing moves for decoration. Numbers roll on
  change; focus rings snap.
- Under `prefers-reduced-motion`, durations are zero.

## Layout

- 4 px spacing grid. Marketing pages: 12 columns, max 1200 px, 24 px gutters,
  120 px between sections (72 px on mobile).
- Console: 240 px sidebar, 60 px top bar, content up to 1440 px.
- 36 px controls, 40 px table rows, 44 px touch targets and hero calls to
  action.
- Radius 4 px for tags in tables, 6 px for buttons, inputs and chips, 10 px for
  cards, code, dialogs and screenshots, full for badges and avatars.
- Focus is a 2 px cobalt ring with a 2 px offset.
