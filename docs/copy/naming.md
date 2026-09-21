# Sylphx product naming policy (brand copy)

**Status:** Binding for brand copy. This file projects company naming law; it
does not create, extend, or retire names on its own.

**Authority:** [SylphxAI/owner](https://github.com/SylphxAI/owner) is the naming
and lifecycle authority — `company/ownership.md` §4 (Naming) and §5 (Public
locators) — and [`company/portfolio.md`](https://github.com/SylphxAI/owner/blob/main/company/portfolio.md)
is the lifecycle register. Brand copy must not carry a name the register does
not, and a rename is not complete until the owning repository's cut is.

## Current names

| Layer | Name | Notes |
|-------|------|-------|
| Company | **Sylphx** | Never "SylphX"/"Sylph X". "SylphxAI" is the GitHub org identifier only, not a product name. |
| Models product | **Sylphx Models** | Model catalog and official Responses service. Site `https://sylphx.ai/`; API `https://api.sylphx.ai/v1`; Models-issued keys. Category noun: models. Former names: Sylphx AI (as a single product and as the later hub). |
| Agent product | **Sylphx Bot** | Agent objective and graph. Site `https://sylphx.bot/`; API `https://api.sylphx.bot`; Bot-issued credentials. Category noun: agent. Former names: Sylphx Agents, Sylphx Bots, Spiron. |
| Cloud platform | **Sylphx Cloud** | The PaaS / capability platform. Apex `https://sylphx.com/`; CLI `sylphx`. Former names: Sylphx Apps, Sylphx Platform. |
| Agent-native runtime (client) | **Keel** | |
| Managed DB/Redis/Typesense TLS edge | **Data Edge** | Infra descriptor; not a customer product brand. Repo `SylphxAI/data-edge`. |

## Host grammar

Every public product has a purchased root where owned, otherwise
`{product}.sylphx.com`, and an API at `api.{site-host}`. A purchased root
belongs to one product: no product takes a second-level `{product}.<root>`
name.

| Surface | Site | API |
|---------|------|-----|
| Sylphx Cloud | `https://sylphx.com/` | `https://api.sylphx.com` |
| Sylphx Models | `https://sylphx.ai/` | `https://api.sylphx.ai/v1` |
| Sylphx Bot | `https://sylphx.bot/` | `https://api.sylphx.bot` |
| Other products | `https://{product}.sylphx.com` | `https://api.{product}.sylphx.com` |

Former hosts must not be presented as current homes: `api.models.sylphx.ai`
and `models.sylphx.ai` (the former Models hosts), `agents.sylphx.ai` and
`api.agents.sylphx.ai` (the former Agents and family-hub hosts),
`agents.sylphx.com` and `api.agents.sylphx.com` (former Agents hosts), and the
non-destination `ai.sylphx.com` and `platform.sylphx.com`.

## Former names

These names must not be used as current product names. Historical mapping is
allowed.

| Former name | Current name |
|-------------|--------------|
| Sylphx AI (as a single product, and as the later family/hub name) | Sylphx Models (`https://sylphx.ai/`); the name is retired |
| Sylphx Platform | Sylphx Cloud |
| Sylphx Agents (site `https://agents.sylphx.ai`) | Sylphx Bot (site `https://sylphx.bot/`) |
| Sylphx Bots (site `bots.sylphx.com`) | Sylphx Bot (site `https://sylphx.bot/`) |
| Spiron | Sylphx Bot |
| Gateway | Retired; not a current name for any Sylphx product |
| Decisions; Sylphx Proof (interim 2026-09-18, reversed by owner 2026-09-21) | Sylphx Decision (repo `SylphxAI/decision`) |

## Rules

1. **"Sylphx AI" is retired.** There is no family, hub, or other brand-only
   surface; Sylphx Models is the product at `https://sylphx.ai/`. Never use the
   name for a product, service, runtime, or API surface.
2. **Products are peers.** Sylphx Models and Sylphx Bot keep their own
   contracts, credentials, roots, and SDKs. No group, family, or hub is a second
   writer, admission path, or credential issuer.
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
   references may map Spiron to Sylphx Bot.
9. **"Agent" is a category noun, not a name.** Write "Sylphx Bot" (or "Bot") for
   the product, and "agent" for the category, an instance, or a customer's own
   agent. Never "Sylphx Agent" as a product name.
