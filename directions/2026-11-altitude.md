# Direction Altitude, 2026-11-16

On 2026-11-16 the owner authorised a full redesign of the Sylphx identity:
logo, palette and type from scratch, with nothing of the old identity kept.
The design lead made the decisions below. The three-direction study of
2026-09-28 ([README.md](README.md)) was not rerun; it stays as the record of
the earlier decision.

## The direction

A sylph is a spirit of the air. The identity is high, clear air:
near-neutral cool surfaces, ink for primary actions, one azure accent, and a
single brand gradient, the current (deep blue `#2F4BFF` → azure `#2FA8FF` at
55% → pale sky `#9FE3FF`), kept for the mark and rare brand moments.

## What replaced what

| | Before | Now |
| --- | --- | --- |
| Mark | Two stroked currents that cross into an x, cobalt under ink (Engineered, 2026-09-28) | Two identical solid blades, the second turned 180° about the centre: an S, a pair of wings, a stream of air; filled with the current |
| Wordmark | IBM Plex Sans SemiBold, tracking −0.02em | Geist SemiBold, tracking −0.04em |
| Lockup | Mark 1.45 cap heights, gap 0.36, minimum 88 px | Mark 1.5 cap heights, gap 0.30, minimum 80 px |
| Mark colours | Cobalt `#2448F5` / `#6B86FF`, warm ink `#15130F`, paper `#F2EEE6` | The current, ink `#0A0D14`, paper `#F4F6FA` |
| Favicon | Rectangles snapped to whole pixels at 16 and 32 px | The tile as a vector; the 16 px frames draw the mark in white |
| Primary action | Cobalt fill | Ink fill; azure is for links, focus and selection |
| Interface accent | Cobalt `#2448F5` (dark `#6B86FF`) | Azure `#1463FF` (dark `#4D94FF`) |
| Interface type | Inter and JetBrains Mono | Geist and Geist Mono, with Instrument Serif italic as an accent face |
| Radius | 4, 6, 10 px | 6, 10, 14, 20 px |
| Motion | 150 ms, `cubic-bezier(0, 0, 0.2, 1)` | 180 ms, `cubic-bezier(0.2, 0, 0, 1)` |

File names under `logo/` and every existing token name are unchanged, so
surfaces keep compiling; the values and drawings changed. New tokens:
`--sx-mark-current-start`, `-mid`, `-end`, `--sx-mark-dawn`,
`--sx-gradient-current`, `--sx-font-accent`, `--sx-radius-xl`.
`logo/construction/pixel-grids.txt` is gone with the snapped favicons.

## Contrast

Every text token was checked at 4.5:1 and every control border at 3:1 on
every surface in both themes (WCAG 2.2 AA). One value moved to pass: light
`border-control` from `#8A94A6` to `#828DA0` (2.77:1 → 3.04:1 on
`surface-sunken`).

## Similarity check

Not yet recorded. The repository rule asks for a visual comparison against
the marks of comparable developer platforms and of our other companies before
surfaces adopt a new mark; that comparison is still to be made for the
two-blade mark and added here.
