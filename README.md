# Sylphx brand

The one home of the [Sylphx](https://sylphx.com) identity: the name and how to
write it, the logo in every lockup and colour, the small-size and app icons,
the colour, type, spacing and motion tokens, the usage rules, where every file
came from, and the trademark status. Every Sylphx surface (sylphx.com, the
docs, the console, the CLI, READMEs, the GitHub organization) takes its
identity from here and keeps no redrawn copy or hand-picked colour
(owner standard, `standards/experience.md`, "Brand home").

The current identity is **Engineered**, chosen 2026-09-28 from three complete
directions: paper and ink, one cobalt accent, IBM Plex, and a mark of two
currents that weave into the x of Sylphx. Why, and the alternatives:
[directions/README.md](directions/README.md).

| Need | Where |
| --- | --- |
| The name, spelling and product naming | [docs/name.md](docs/name.md) |
| Company facts | [COMPANY.md](COMPANY.md) |
| How to use the logo, colour, type, icons and motion | [guidelines/guidelines.md](guidelines/guidelines.md) and the usage sheet [logo/sheet/usage.png](logo/sheet/usage.png) |
| Logo files, construction, small sizes, provenance | [logo/README.md](logo/README.md) |
| Design tokens | [tokens/brand.tokens.json](tokens/brand.tokens.json) (source) and [tokens/brand.css](tokens/brand.css) (generated) |
| Fonts to self-host | [fonts/](fonts/) (IBM Plex Sans and Mono, OFL) and the loader [fonts/fonts.css](fonts/fonts.css) |
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
pip install pillow numpy fonttools brotli uharfbuzz resvg-py
python3 logo/construction/mark.py     # every file under logo/ from mark.spec.json
python3 scripts/build_tokens.py       # tokens/brand.css from tokens/brand.tokens.json
python3 scripts/manifest.py           # logo/MANIFEST.sha256
```

CI checks that `tokens/brand.css` and `logo/MANIFEST.sha256` match their
sources. A new direction for the identity lands here first, with a
similarity check recorded, and the surfaces follow.
