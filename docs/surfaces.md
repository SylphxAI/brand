# Where the brand appears

Each surface consumes this repository's files or tokens; none keeps a copy.

| Surface | Uses | How it stays current |
| --- | --- | --- |
| sylphx.com (site, docs, console, sign-in) | `tokens/brand.css`, `logo/svg/*`, `logo/favicon/*` | The platform repository (`SylphxAI/cloud`, `web/`) pulls them at a pinned commit with hashes checked against `logo/MANIFEST.sha256` |
| GitHub organization avatar | `logo/app-icon/sylphx-app-icon-1024.png` | Uploaded by the owner when the mark changes |
| `SylphxAI/.github` profile README | `logo/svg/sylphx-lockup-colour.svg`, copy from `docs/voice.md` | Linked from this repository, not copied |
| npm and README badges | the lockup and the accent `#2448F5` | Through [Mark](https://mark.sylphx.com) (owner documentation standard) |
| status.sylphx.com | lockup, favicon, tokens | Pulled like sylphx.com |
