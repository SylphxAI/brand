# Fonts

Inter (400, 500, 600) and JetBrains Mono (400, 500), WOFF2, Latin and Latin
Extended subsets, as every Sylphx surface self-hosts them
([guidelines](../guidelines/guidelines.md#type)). Copyright The Inter Project
Authors and The JetBrains Mono Project Authors, SIL Open Font License 1.1
([OFL.txt](OFL.txt)). Taken from the `@fontsource/inter` and
`@fontsource/jetbrains-mono` packages, version 5.3.0; hashes are in
[../logo/MANIFEST.sha256](../logo/MANIFEST.sha256).

Chinese and Japanese use Noto Sans TC, SC and JP, which come next in
`--sx-font-sans`. No CJK files ship here yet, so those scripts fall through
to the system CJK face.

[fonts.css](fonts.css) is the loader: the `@font-face` rules that bind these
files to the family names `tokens/brand.css` uses. A surface copies it as-is
and keeps the files in the same directory beside it: its `src` URLs are
relative to the stylesheet, so the pair works at any path, including under a
subpath, with no rewrite.
