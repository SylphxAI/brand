# Sylphx product naming policy (brand copy)

**Status:** Binding for brand copy. This file projects company naming law; it
does not create, extend, or retire names on its own.

**Authority:** [SylphxAI/owner](https://github.com/SylphxAI/owner) is the naming
and lifecycle authority — `standards/authority.md` §11 (Naming) and §13 (Public
locators) — and [`PORTFOLIO.md`](https://github.com/SylphxAI/owner/blob/main/PORTFOLIO.md)
is the lifecycle register. Brand copy must not carry a name the register does
not, and a rename is not complete until the owning repository's cut is.

## Current names

| Layer | Name | Notes |
|-------|------|-------|
| Company | **Sylphx** | Never "SylphX"/"Sylph X". "SylphxAI" is the GitHub org identifier only, not a product name. |
| AI brand family | **Sylphx AI** | Umbrella over the company's AI products; hub `https://sylphx.ai/`. Not a product: no contract, credentials, or API of its own. Members today: Sylphx Models and Sylphx Agents. |
| AI family member — models | **Sylphx Models** | Model catalog and official Responses service. Site `https://models.sylphx.ai`; API `https://api.models.sylphx.ai/v1`; keys `sk-sx-…`. Short display in service tiles: **Models** (next to Database / Auth). Former name: Sylphx AI (as a single product). |
| AI family member — agents | **Sylphx Agents** | Agent objective and graph. Site `https://agents.sylphx.ai`; API `https://api.agents.sylphx.ai/v1`. Former names: Sylphx Bots, Spiron. |
| Cloud platform | **Sylphx Cloud** | The PaaS / capability platform. Apex `https://sylphx.com/`; CLI `sylphx`. Former names: Sylphx Apps, Sylphx Platform. |
| Agent-native runtime (client) | **Keel** | |
| Managed DB/Redis/Typesense TLS edge | **Data Edge** | Infra descriptor; not a customer product brand. Repo `SylphxAI/data-edge`. |

## Host grammar

Every public product has a purchased root where owned, otherwise
`{product}.sylphx.com`, with an API at `api.{site-host}`; product APIs include
`/v1`. AI family members use the family root `sylphx.ai`:
`{product}.sylphx.ai` for the site and `api.{product}.sylphx.ai` for the API.
The hub `https://sylphx.ai/` is a brand surface, not a product, and owns no API.

| Surface | Site | API |
|---------|------|-----|
| Sylphx Cloud | `https://sylphx.com/` | `https://api.sylphx.com` |
| Sylphx AI (family hub) | `https://sylphx.ai/` | — none; members issue their own credentials |
| Sylphx Models | `https://models.sylphx.ai` | `https://api.models.sylphx.ai/v1` |
| Sylphx Agents | `https://agents.sylphx.ai` | `https://api.agents.sylphx.ai/v1` |
| Other products | `https://{product}.sylphx.com` | `https://api.{product}.sylphx.com` |

Former hosts must not be presented as current homes: `api.sylphx.ai` (the
former AI product peel), `agents.sylphx.com` and `api.agents.sylphx.com`
(former Agents hosts), and the non-destination `ai.sylphx.com` and
`platform.sylphx.com`.

## Former names

These names must not be used as current product names. Historical mapping is
allowed.

| Former name | Current name |
|-------------|--------------|
| Sylphx AI (as a single product) | Sylphx AI is the family (hub `https://sylphx.ai/`); the model service is Sylphx Models |
| Sylphx Platform | Sylphx Cloud |
| Sylphx Bots (site `bots.sylphx.com`) | Sylphx Agents (site `https://agents.sylphx.ai`) |
| Spiron | Sylphx Agents |
| Gateway | Retired; not a current name for any Sylphx product |

## Rules

1. **"Sylphx AI" names only the family or its hub.** Never use it for a single
   product, service, runtime, or API.
2. **Family members are independent products.** Sylphx Models and Sylphx Agents
   keep their own contracts, credentials, sites, and SDKs. The family is not a
   second writer, admission path, or credential issuer.
3. **"Gateway" is retired as a product name.** It must never name a Sylphx
   product, service, runtime, repo display name, deployment, or API.
4. "Gateway" may appear only as generic English or a third-party concept (e.g.,
   industry phrase "API gateway", an upstream partner's "agent gateway" pattern).
5. Sylphx Models runtimes are **Edge** (request serving), **Control**
   (catalog/policy/reconciliation), **Console** (UI), and **Platform Batch**.
   Never "Gateway Edge".
6. In copy, prefer concrete nouns: SDK, Postgres, hibernate, models, deploy.
   Do not use "gateway" as a marketing noun.
7. New identifiers, files, and docs must not introduce `*-gateway` names for
   Sylphx components. Existing non-conforming identifiers are being renamed in a
   clean cut; do not re-introduce them.
8. **"Spiron" is retired as a product name.** It must never name a current
   Sylphx product, service, repo display name, or marketing noun. Historical
   references may map Spiron to Sylphx Agents.
