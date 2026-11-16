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

Sized to a small company, as the previous direction's was (owner decision
2026-09-27, owner#781): a visual comparison, no search or filing. Recorded
2026-11-16. The comparison was made against the marks as generally known, not
against a freshly rendered side-by-side sheet; a sheet like
`out/similarity-competitors.png` should be regenerated before any trademark
step.

The two-blade mark does not resemble the marks of Vercel, Supabase, Neon,
Railway, Render, Fly, Clerk, OpenRouter, Netlify, Cloudflare, Firebase,
PostHog, Resend, Linear, Stripe, Convex, Upstash, Turso, Appwrite, Sentry,
Temporal, WorkOS, Inngest, Modal or E2B, nor the marks of our other companies.

Nearest neighbours, and what separates the mark from each:

- **Tailwind CSS**: two wave shapes in cyan. Theirs are two copies of one
  rounded wave, stacked and offset sideways, in one flat colour; ours are two
  pointed blades related by a half turn about the centre, which is what draws
  the S, and they carry the three-stop current from indigo to pale sky.
- **Shazam**: an S from two hooks in blue. Theirs is two open stroked hooks
  inside a disc; ours is two closed, filled blades with no enclosing shape.
- **Surfshark**: a single teal S-like fin. One shape with a cut-out, against
  our two separate shapes.
- **Windsurf**: wind as a motif. Their mark is a set of parallel strokes; no
  rotational pair and no S.

Azure `#1463FF` sits apart from Stripe's violet `#635BFF`, Tailwind's cyan
`#38BDF8` and Supabase's green. The primary action colour is ink, so the
accent appears far less than a brand colour usually does.

Risk judged acceptable for launch. Tailwind CSS is the closest and is a
developer brand our audience knows, so the mark is always used with the
gradient or in single-colour ink or white, never in flat cyan.
