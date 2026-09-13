# Name clearance — desk research

**Status:** Adopted reference material (2026-09-13). **Research, not legal
advice**; it states no legal conclusions. **Outstanding: the human test-kit run
and attorney clearance (see §8).** It does not change naming law or brand copy:
the binding naming policy remains [`docs/copy/naming.md`](../copy/naming.md),
and [SylphxAI/owner](https://github.com/SylphxAI/owner) remains the naming and
lifecycle authority.

**Prepared:** 2026-09-13 (UTC), pre-launch. **Companion files:**
[`name-test-kit.md`](./name-test-kit.md) (ready-to-run human tests) and
[`trademark-clearance-brief-template.md`](./trademark-clearance-brief-template.md)
(ready-to-send attorney brief).

## 1. Question

The estate renamed the AI product to **Sylphx Models** (hub `https://sylphx.ai/`)
and kept **Sylphx Agents** under the **Sylphx AI** family. The open questions:

1. Is the umbrella `Sylphx` defensible enough to launch under?
2. Do `Sylphx AI` (family), `Sylphx Models`, and `Sylphx Agents` create
   confusion with names already in market?
3. What evidence would change the naming decision, and what tests can a human
   run before professional clearance lands?

## 2. Method and access limits

Desk readback only (public web, public registers, WHOIS/RDAP, package
registries, and public trademark aggregators). **No professional clearance
search has been run.**

| Check | What was done (date) | Result |
|---|---|---|
| UK company names | Companies House name search for `sylphx`, `sylph`, `sphyx`, `sylphix` (2026-09-13) | Queried; see §3.3 |
| US trademark records | Justia Trademarks readback for `sylph`, `sylphx`, `sylphix`, `sylphai`, `adalflow`, `adal`; spot detail pages (2026-09-12/13) | Partially queried; see §3.4 |
| UK trademark register | UKIPO search service | **Not queried.** The service returns an anti-automation security check; requires counsel or a human session |
| EU trademark register | EUIPO eSearch | **Not queried.** JavaScript application; no results rendered from this seat; requires counsel |
| TMview (multi-office view) | API/front-end attempts | **Not queried.** Did not respond from this seat |
| Domains | WHOIS/RDAP + DNS for `sylphx.com`, `sylphx.ai`, `sylph.ai`, `sylph.com`, `sylphix.com`, `sylphai.com`, `sphyx.in` (2026-09-12/13) | Queried; see §3.2 |
| Software registries | npm registry, crates.io, PyPI, App Store search, GitHub users/repos (2026-09-12) | Queried; see §3.1 and §3.3 |
| Web presence | Direct reads of candidate sites (2026-09-12/13) | Queried; see §3.3 |

> A perfect desk readback is impossible from an agent seat: the UKIPO service
> explicitly ships an anti-data-mining check and EUIPO eSearch is a
> JavaScript application. Treat the trademark rows below as *signals*, not
> clearance. The attorney brief in the companion file exists to close exactly
> this gap.

## 3. Observations (public evidence; accessed 2026-09-13 UTC unless noted)

### 3.1 Our estate today

| Fact | Value | Source |
|---|---|---|
| UK company | `SYLPHX LIMITED`, company number 16438428, incorporated 8 May 2025 | [Companies House search](https://find-and-update.company-information.service.gov.uk/search?q=sylphx) |
| Primary domain | `sylphx.com` created 2025-04-17, expires 2028-04-17 (registrant redacted) | RDAP `https://rdap.verisign.com/com/v1/domain/sylphx.com` |
| Family hub domain | `sylphx.ai` created 2026-03-02, registrant country GB | WHOIS (Cloudflare registrar) |
| AI member hosts | `models.sylphx.ai` and `agents.sylphx.ai` resolve in DNS (CNAME `cname.sylphx.com`) | `dig` 2026-09-12 |
| npm packages | `@sylphx/cli` 0.22.8, `@sylphx/sdk` 0.28.0 published | npm registry |
| Rust crates | `sylphx-cli`, `sylphx-sdk`, `sylphx-sdk-core`, `sylphx-sdk-management`, … | crates.io search |
| GitHub | Org `SylphxAI` is the estate; the unrelated user `github.com/sylphx` has existed since 2014-03-16 with 0 public repos | GitHub API |

**Observation:** the company, the `.com`, the `.ai`, the npm scope, the crate
prefix, and the GitHub org are all in hand. Only `sylphx.ai` is new (March
2026), so brand use under the word `Sylphx` is recent and first-use evidence is
thin outside the code estate.

### 3.2 The `sylph*` domain neighbourhood

| Domain | Registered | What it currently is | Source |
|---|---|---|---|
| `sylphx.com` | 2025-04-17 | Ours (estate domain) | RDAP |
| `sylphx.ai` | 2026-03-02 | Ours (family hub) | WHOIS |
| `sylph.ai` | 2023-06-12 | US startup; redirects to `https://adalagent.ai/` | WHOIS + HTTP redirect |
| `sylphai.com` | 2022-04-14 | Registered; historically labelled "SylphAI" (current owner to verify) | RDAP |
| `sylphix.com` | 2023-03-02 | Sylphix Technologies (AI products) | RDAP + site |
| `sylph.com` | 1996-03-29 | Parked; page says "This domain may be for sale" | RDAP + site |
| `sphyx.in` | resolves (43.254.28.133) | Sphyx Digital Private Limited (India; brand/marketing/CRM/ERP) | DNS + site |

**Observation:** three live domains differ from ours by one character
(`sylph.ai`, `sylphix.com`) or one letter dropped/replaced (`sphyx.in`), and a
fourth (`sylphai.com`) by one insertion of `x`. `sylph.com` is a parked
1996 domain that could re-enter any market.

### 3.3 Adjacent names/companies in market

| Name | What it is | Evidence |
|---|---|---|
| **SylphAI, Inc.** (US; per public listings; `sylph.ai` → `adalagent.ai`) | AI agent harness company: AdaL ("automation-first agent harness"), CLI, worker agents (coding, deep research, browser), agent infra, AdalFlow SDK, `atskills.one` skills catalogue; GitHub org `SylphAI-Inc` | [adalagent.ai](https://adalagent.ai/); [github.com/SylphAI-Inc](https://github.com/SylphAI-Inc) |
| **Sylphix Technologies** (`sylphix.com`) | "AI products that do the work"; site describes products incl. SylphHire, SylphAvatar, SylphTalk | [sylphix.com](https://sylphix.com/) |
| **SYLPHIX** (US trademark 99400274) | Filed 2025-09-18, owner Yang Wang, class 21 (crockery, cookware; housewares), status per aggregator: new application | [Justia record](https://trademarks.justia.com/994/00/sylphix-99400274.html) |
| **Sylph Industries Ltd** (India; BSE 511447) | Formerly Sylph Technologies Ltd; listed IT/technology company; uses `sylphtechnologies.com` | [Screener company page](https://www.screener.in/company/511447/) |
| **Sphyx Digital Private Limited** (`sphyx.in`) | India build-and-grow agency (brand, marketing, CRM/ERP) | [sphyx.in](https://sphyx.in/) |
| **SYLPH LIMITED** (UK 17047490) | Incorporated 2026-02-23 (active); part of a long tail of `SYLPH*` UK companies (Sylph Editions, Sylph Productions, Sylph Properties, Sylph Beauty & Cosmetics, Sylph Software Ltd (dissolved), …) | [Companies House search](https://find-and-update.company-information.service.gov.uk/search?q=sylph) |
| **Sylph** personal-name / dictionary uses | `Sylph` is an ordinary English word (a spirit of the air); GitHub user `Sylph`, PyPI package `sylph`, GitHub user `Sylphix` (2024) | GitHub API; PyPI; dictionary sense |

### 3.4 Trademark-like records seen in the US readback

Aggregator (Justia) readback only; verify each on USPTO TSDR before relying on
it. Status strings below are the aggregator's codes.

| Mark | Serial | Class / goods | Status (aggregator) |
|---|---|---|---|
| SYLPH | 87369729 | 11 — heating/lighting/air apparatus (Shenzhen WizEvo Tech) | 700 Registered (No. 5301137) |
| SYLPH | 79355433 | 9 — gas chromatography apparatus (Ball Wave Inc.) | 630 New application |
| SYLPH | 98072491 | 14 — jewellery (Evolution Infinity Holdings) | 630 New application |
| SYLPH | 50059005 | 25 — clothing (Shanghai Jinxiyao Trading) | 630 New application |
| SYLPH | 98590720 | 34 — e-cigarettes (Modern Motive Limited) | 630 New application |
| SYLPH | 86494525 | 11 — electric fans | 606 Abandoned — no statement of use |
| SYLPH (Sylph Salons) | 73288213 | 42 — weight reduction, health/beauty services | 618 Abandoned (backfile) |
| SYLPHIX | 99400274 | 21 — housewares/cookware | New application |
| SYLPH SOLUTIONS | 99910911 | 7 / 40 / 41 — wind turbines, materials treatment, entertainment (Edward Anderson) | 630 New application |

Notes:

- No US record for `SYLPHX` was returned by the aggregator query; no record for
  `SylphAI`/`AdalFlow` was returned either. This is **not** proof of
  availability — it is a desk signal only.
- The live class 9 `SYLPH` record above covers chromatography apparatus, not
  software or SaaS. The class number alone does not measure scope; similarity
  of goods/services is a counsel question.

## 4. Inferences (analysis of the observations above — not legal conclusions)

1. **The single largest confusion pair is `Sylphx` ↔ `SylphAI`.**
   `SylphAI, Inc.` is active in exactly our space (agent harness, worker
   agents, model/SDK infrastructure), its legal name is one character away
   from our GitHub org `SylphxAI`, and `sylph.ai` sits one character from
   `sylphx.ai`. Search engines, model answers, and word of mouth have a high
   chance of merging the two.
2. **`Sylphx` vs `Sylphix` is a spelling/recognition collision, not (on current
   evidence) a software-class trademark collision.** The one US `SYLPHIX`
   record found is class 21 housewares; the Sylphix site is an AI product
   studio. Same-sector *attention* collision is likely even without class
   overlap.
3. **`Sylphx` vs `SYLPH` (dictionary word, many marks in unrelated classes).**
   A spread of live US `SYLPH` word marks exists (classes 9/11/14/25/34 …) and
   older class 42 use is abandoned. On today's evidence, class-scope overlap
   for software/SaaS is not apparent in the US, but the word itself is
   crowded across classes and is an ordinary noun — which weakens natural
   distinctiveness arguments.
4. **The family label `Sylphx AI` is the weakest element of the structure.**
   "AI" is ubiquitous and non-distinctive; `Sylphx AI` is the form most likely
   to be read as the neighbour `SylphAI` when spoken or searched. The
   distinctive asset is the coined string `Sylphx`; the sub-names `Models` and
   `Agents` are category words that describe exactly what they are.
5. **Pronunciation/spelling friction is real but testable.** `ph` + `x` have no
   natural English reading; plausible writes are `Sylph`, `Sylphix`,
   `Sylphex`, `Sylph X`, `Silfex`. Voice input, referrals, and word of mouth
   will produce variants. This is the cheapest thing to measure before
   launch — see the test kit.
6. **Handle/domain hygiene matters at this size.** The `.com`, `.ai`, npm
   scope and GitHub org are ours, but `github.com/sylphx` is a dormant 2014
   user account, `github.com/Sylphix` and `github.com/SylphAI-Inc` exist, and
   social handles (`@sylphx`) were not verified as available or ours. A
   stranger trying to find us by handle can land on someone else.

## 5. Assumptions and unknowns

**Assumptions used above**

- The `sylphx.ai` registrant is the estate (registrant proxy hides the name;
  GB registrant + the estate's own naming decision).
- `adalagent.ai` and `sylph.ai` belong to the same company, whose legal name
  public listings give as SylphAI, Inc. — based on the redirect and the
  shared product/company pages; not independently verified in a company
  register.

**Unknowns that matter**

- EU/UK trademark position for `SYLPH`, `SYLPHX`, `SYLPHX AI`, `SYLPHX MODELS`,
  `SYLPHX AGENTS` in classes 9 and 42 (not queried — counsel required).
- Whether SylphAI, Inc. or Sylphix Technologies hold (or will file) marks in
  classes 9/42 in the UK/EU/US.
- Social handles (`x.com/sylphx`, LinkedIn, Discord vanity) and app-store
  names for `Sylphx`.
- Whether `SYLPHX` has been used publicly long enough for unregistered
  goodwill, and where first use is provable.

## 6. What would change the naming decision

These are pre-registered decision triggers — if any fires, the naming decision
gets revisited rather than defended by default:

| Trigger | Source |
|---|---|
| Counsel finds an earlier live identical/similar mark in classes 9/42 in UK, EU or US with overlapping goods/services, or rates opposition risk high | Attorney brief |
| Say-and-spell test: fewer than ~80% of participants spell `Sylphx` correctly on the first try, or a majority volunteer `Sylphix`/`Sylph` | Test kit |
| Recognition test: fewer than ~75% place `Models` / `Agents` / `Cloud` correctly after a 10-second exposure | Test kit |
| Confusion probe: a participant says `Sylphx` and `SylphAI`/`Sylphix` are the same company or cannot tell them apart | Test kit |
| SylphAI, Inc. or Sylphix Technologies expands to UK/EU under a `Sylph*` AI-infrastructure brand, or files in classes 9/42 | Watch / counsel |
| The handle/domain set we need (e.g. `@sylphx`) is permanently unavailable or would be too costly | Channel check |

## 7. Options on the table (for the decision, not a legal recommendation)

| Option | What changes | Cost / risk |
|---|---|---|
| **A. Keep and strengthen** | Keep `Sylphx` + `Sylphx AI` family + `Sylphx Models`/`Sylphx Agents`; file word marks; always render the `x` and the family as one string | Requires early filings and disciplined usage; confusion with `SylphAI` remains a watch item |
| **B. Keep umbrella, soften family label** | Keep `Sylphx` for company/estate; use `Sylphx AI` only descriptively; make `Sylphx Models` / `Sylphx Agents` the primary marks | Copy/law change; reduces the `Sylphx AI`/`SylphAI` read-alike surface |
| **C. Adjust before launch** | Change the family label or sub-brand spelling now (e.g. avoid a second `-x`-style synonym); keep `Sylphx` as company mark | Cheapest moment to change is now; needs the test kit + counsel first |
| **D. Rename the umbrella** | New coined word entirely | Highest cost; only justified if counsel or tests show high risk |

## 8. Next actions

1. Run the [test kit](./name-test-kit.md) — ~15 minutes with 5 people; it is
   designed to be run by a human without legal input. **Outstanding — not yet
   run.**
2. Send the [attorney brief](./trademark-clearance-brief-template.md) as-is
   (fill placeholders) for UK/EU/US clearance searches in classes 9 and 42.
   **Outstanding — not yet sent.**
3. Keep a watch list: SylphAI, Inc. (US), Sylphix Technologies, Sylph
   Industries Ltd (IN), SYLPH/SYLPHIX US filings, `@sylphx` handles.
4. Re-run this note after counsel feedback; only then amend
   [`docs/copy/naming.md`](../copy/naming.md) if the decision changes.
