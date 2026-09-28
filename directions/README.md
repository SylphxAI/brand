# Visual directions, 2026-09-28

The owner ordered a complete redesign of sylphx.com: site, docs, sign-in and
console. Three complete identity systems were built and rendered onto real
pages (home, the Database product page, a docs page, the console home and a
console resource page) at 1440 px and 390 px, in dark and light. The owner
asked the design lead to choose on the evidence, without a review
checkpoint. **Chosen: Engineered.** The Sylphx brand is now built from it
([`../logo/README.md`](../logo/README.md), [`../tokens/`](../tokens/)).

**The figures on the boards are illustrative layout text, not claims.** On a
real page every number and claim is true and sourced: product counts and
status badges from the product registry, prices from the live price catalog,
speed figures only when measured (owner standard, sourced numbers).

Everything here is rebuilt by `python3 directions/build.py` (headless
Chromium plus Pillow). The boards are in `out/`:

| Direction | Identity | Pages, desktop | Pages, mobile |
| --- | --- | --- | --- |
| A. Signal | `out/a-signal-1-identity.png` | `out/a-signal-2-desktop.png` | `out/a-signal-3-mobile.png` |
| B. Atmosphere | `out/b-atmosphere-1-identity.png` | `out/b-atmosphere-2-desktop.png` | `out/b-atmosphere-3-mobile.png` |
| C. Engineered | `out/c-engineered-1-identity.png` | `out/c-engineered-2-desktop.png` | `out/c-engineered-3-mobile.png` |

## A. Signal

Graphite surfaces, one amber signal colour, Geist type, a 1.5 px outline icon
set, and 120–180 ms motion with no bounce. The mark is a block split by an
S-shaped gap of air.

- **Takes** Vercel's and Linear's restraint, density and keyboard-first speed.
- **Rejects** their colourless anonymity: the one warm signal makes it ours.
- **Why not.** It is the best-made version of the look almost every developer
  platform already has (dark, near-black, one accent). Put beside Vercel,
  Linear and Railway it reads as one of them. It also keeps the amber of the
  site the owner judged below the bar.

## B. Atmosphere

Deep night-sky surfaces, indigo and cyan light, Instrument Serif for display
and Instrument Sans for text, duotone rounded icons, and soft 240–320 ms
drifting motion. The mark is three tapered strokes fanned like a wing.

- **Takes** Stripe's and Clerk's use of colour and light as the brand.
- **Rejects** decoration inside the product; the console stays flat.
- **Why not.** The mark fails the size test: at 26 px in the navigation bar it
  is an unreadable sliver, and at 16 px it is gone. The serif display face
  splits the site's and the console's voices. The glow depends on gradients
  that cost paint time and contrast in light mode.

## C. Engineered (chosen)

Warm paper and ink, one cobalt accent, IBM Plex Sans and Plex Mono, a 1.75 px
geometric icon set with square ends, mono labels, visible structure, and
150 ms stepped motion with no decoration. The mark is two currents that
cross and weave into an x, the x of Sylphx.

- **Takes** Railway's and Resend's technical honesty, mono labels and visible
  grid; Stripe's documentation discipline.
- **Rejects** dark-only hacker styling: light paper is the default, dark is a
  full equal theme.
- **Why.**
  - *Distinctive.* Among the 25 developer platforms checked
    (`out/similarity-competitors.png`) almost all are dark
    with a single accent; a paper-and-ink default with a mono-labelled
    structure is recognisable from a thumbnail.
  - *Legible at every size.* The knot holds at 26 px in the navigation, reads
    as an x at 32 px, and the two tones separate it on both themes.
  - *Fit.* Sylphx is infrastructure people trust with data; a page that reads
    like a precise specification says that. Dense tables, mono numbers and
    resource names (`orgs/acme/projects/shop/…`) are native to the style
    rather than bolted on.
  - *Cheap to render.* Flat surfaces and no gradients or glass keep paint
    cost low, which the LCP-under-1-second target needs.
- **Fixed while building the brand.** The first mockups had a hero grid that
  was too loud, feature cards that stayed three-across on mobile, and an
  activity feed whose nested rows inherited the row rule. These are mockup
  faults, recorded so the design system does not repeat them.

## Similarity check

Sized to a small company (owner decision 2026-09-27, owner#781): a visual
comparison, no search or filing. The knot does not resemble the marks of
Vercel, Supabase, Neon, Railway, Render, Fly, Clerk, OpenRouter, Netlify,
Cloudflare, Firebase, PostHog, Resend, Linear, Stripe, Convex, Upstash, Turso,
Appwrite, Sentry, Temporal, WorkOS, Inngest, Modal or E2B, nor the marks
of our other companies. Cobalt `#2448F5` sits apart from Stripe's violet `#635BFF`.
