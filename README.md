# Sylphx brand

The one home of the [Sylphx](https://sylphx.com) identity: the name and how to
write it, the logo in every lockup and colour, the small-size and app icons,
the colour, type, spacing and motion tokens, the usage rules, where every file
came from, and the trademark status. Every Sylphx surface (sylphx.com, the
docs, the console, the CLI, READMEs, the GitHub organization) takes its
identity from here and keeps no redrawn copy or hand-picked colour
(owner standard, `standards/experience.md`, "Brand home").

The direction is *Altitude*, an owner-authorised full redesign of 2026-11-16
([directions/2026-11-altitude.md](directions/2026-11-altitude.md)): high,
clear air. Near-neutral cool surfaces, ink for primary actions, one azure
accent, Geist and Geist Mono, and one gradient, the current, kept for the
mark and rare brand moments. The mark is two blades, one turned 180° from the
other, that read as an S, a pair of wings and a stream of air.

| Need | Where |
| --- | --- |
| The name, spelling and product naming | [docs/name.md](docs/name.md) |
| Company facts | [COMPANY.md](COMPANY.md) |
| How to use the logo, colour, type, icons and motion | [guidelines/guidelines.md](guidelines/guidelines.md) and the usage sheet [logo/sheet/usage.png](logo/sheet/usage.png) |
| Logo files, construction, small sizes, provenance | [logo/README.md](logo/README.md) |
| Design tokens | [tokens/brand.tokens.json](tokens/brand.tokens.json) (source) and [tokens/brand.css](tokens/brand.css) (generated) |
| Fonts to self-host | [fonts/](fonts/) (Geist, Geist Mono and Instrument Serif, OFL) and the loader [fonts/fonts.css](fonts/fonts.css) |
| Voice | [docs/voice.md](docs/voice.md) |
| Trademark status | [docs/trademarks.md](docs/trademarks.md) |
| Where the brand appears | [docs/surfaces.md](docs/surfaces.md) |

## Quick picks

| Need | File |
| --- | --- |
| Website header, documents, slides | `logo/svg/sylphx-lockup-colour.svg` (`-colour-on-dark` on dark) |
| The mark alone | `logo/svg/sylphx-symbol-colour.svg` (`-colour-on-dark`, `-black`, `-white`) |
| Browser tab | `logo/favicon/favicon.svg`, `favicon.ico`, `apple-touch-icon-180.png` |
| App stores, avatars | `logo/app-icon/sylphx-app-icon-1024.png` |
| CSS | `tokens/brand.css` (`--sx-*`) |

## Changing the brand

Edit a source, regenerate, and commit the outputs in the same pull request:

```bash
pip install -r logo/construction/requirements.txt
python3 logo/construction/mark.py     # every file under logo/ from mark.spec.json
python3 scripts/build_tokens.py       # tokens/brand.css from tokens/brand.tokens.json
python3 scripts/manifest.py           # logo/MANIFEST.sha256
```

CI checks that `tokens/brand.css` and `logo/MANIFEST.sha256` match their
sources and that `mark.py` redraws every file under `logo/` byte for byte. A new direction for the identity lands here first, with a
similarity check recorded, and the surfaces follow.
