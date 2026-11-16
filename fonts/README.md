# Fonts

Geist (400, 500, 600), Geist Mono (400, 500) and Instrument Serif (400
italic), WOFF2, Latin and Latin Extended subsets, as every Sylphx surface
self-hosts them ([guidelines](../guidelines/guidelines.md#type)). Copyright
The Geist Project Authors (Geist and Geist Mono, made by Vercel) and The
Instrument Serif Project Authors, SIL Open Font License 1.1
([OFL.txt](OFL.txt)). Taken from the `@fontsource/geist`,
`@fontsource/geist-mono` and `@fontsource/instrument-serif` packages, each
version 5.3.0; hashes are in
[../logo/MANIFEST.sha256](../logo/MANIFEST.sha256). Geist comes from
`@fontsource/geist`, not `@fontsource/geist-sans`: the latter is the 2023
release under the family name "Geist Sans" with no Latin Extended subset.

Chinese and Japanese use Noto Sans TC, SC and JP, which come next in
`--sx-font-sans`. No CJK files ship here yet, so those scripts fall through
to the system CJK face.

[fonts.css](fonts.css) is the loader: the `@font-face` rules that bind these
files to the family names `tokens/brand.css` uses. A surface copies it as-is
and keeps the files in the same directory beside it: its `src` URLs are
relative to the stylesheet, so the pair works at any path, including under a
subpath, with no rewrite.
