# Fonts

IBM Plex Sans (400, 500, 600) and IBM Plex Mono (400, 500), WOFF2, Latin and
Latin Extended subsets, as every Sylphx surface self-hosts them
([guidelines](../guidelines/guidelines.md#type)). Copyright IBM Corp., SIL Open
Font License 1.1 ([OFL.txt](OFL.txt)). Taken from the `@fontsource/ibm-plex-sans`
and `@fontsource/ibm-plex-mono` packages (IBM Plex 3.x); hashes are in
[../logo/MANIFEST.sha256](../logo/MANIFEST.sha256).

Chinese and Japanese text uses the system CJK face at the same weights; no
CJK web font is shipped.

[fonts.css](fonts.css) is the loader: the `@font-face` rules that bind these
files to the family names `tokens/brand.css` uses. A surface copies it as-is
and keeps the files in the same directory beside it: its `src` URLs are
relative to the stylesheet, so the pair works at any path, including under a
subpath, with no rewrite.
