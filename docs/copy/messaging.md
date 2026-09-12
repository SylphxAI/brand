# Sylphx — messaging kit

> **Positioning revision — PROPOSAL, not adopted.** Prepared 2026-09-12 for the
> owner's brand decision; nothing here ships until the owner accepts it. Story
> follows current owner law: [SylphxAI/owner](https://github.com/SylphxAI/owner)
> `standards/authority.md` §11 (Naming), §13 (Public locators), §3.1
> (Composition), §4 (Credentials); register
> [PORTFOLIO.md](https://github.com/SylphxAI/owner/blob/main/PORTFOLIO.md).
> Law at cut SHAs `d3bbe6deb7155ca8186aae3df029b5471ac5b242` (#435) and
> `fd5a1d89c7db78cff9ef6d33d620eabf6fe90eae` (#436).

## Elevator — EN

Sylphx is a cloud company of independent services: Cloud (hosting and
composition), Identity, Data, Compute, Events, Observability, Commerce, and the
Sylphx AI family — Sylphx Models and Sylphx Agents. Every product is bought
à la carte, with its own site, API, credentials, SDK, and first success.
Sylphx Cloud is the front door when you want the pieces assembled: it hosts and
provisions the services you choose, and never implements or proxies a peer's
API.

## Primary tagline options (PROPOSAL — owner decision)

**Not locked.** The current line stays one candidate; alternatives fit the
composer story. The owner picks one (or none) before any public surface uses a
tagline. This table is the tagline home — other files point here.

| # | Line | Why it fits | Risk / tradeoff |
|---|------|-------------|-----------------|
| **A (current)** | *Stop stitching tools together. Ship with one platform.* | Keeps the live frame and the real pain — vendor glue; "one platform" reads as Cloud the front door. | "One platform" can be heard as one product / one SDK, which is the model we retired; "stitching" frames integration as the enemy while we sell independent services built to compose. |
| **B** | *Take what you need. It all fits.* | À-la-carte plus composition in six words; buyer-first, no jargon. | Needs the product list or a sub-line beside it to say what "it" is. |
| **C** | *Independent services. One company. Built to compose.* | States the post-cut model literally; echoes the composition law. | Longer; less catchy; no motion verb. |
| **D** | *Start with one service. Compose the rest.* | Buyer journey (start small) plus the Cloud front door; no bundle claim. | "Compose" needs a supporting line for non-platform readers. |

**Recommendation for review:** C as the accurate platform line, or B if the
owner prefers the shortest hero. A remains viable only if the owner wants to
keep the live frame and accept its bundle reading.

## Secondary lines

| Use | Line |
|-----|------|
| Category | Independent cloud services · composer platform |
| AI family | The AI brand family: Sylphx Models and Sylphx Agents |
| OSS / broad | Empowering developers to build the future with AI |
| Infra narrative | Building AI agent infrastructure |

## Pillars

1. **Independent by default** — every product stands alone: its own site,
   contract, credentials, docs, pricing, and SDK. Buy one or several; nothing
   requires the rest.
2. **Composed on purpose** — Sylphx Cloud hosts and provisions the services
   you choose. Peers stay independently purchasable and callable; no mandatory
   mesh, no proxied APIs.
3. **Real isolation, honest economics** — per-project Postgres + managed
   cache; idle scales to zero and wakes on demand.
4. **AI as a family** — the `sylphx.ai` hub over Sylphx Models (catalog and
   official Responses service) and Sylphx Agents (autonomous agent OS), each
   an independent product.
5. **Open craft** — MCP servers and libraries prove the engineering in public.

## Objection frames

| Objection | Frame |
|-----------|--------|
| “I’ll just use Vercel + Supabase + Clerk.” | Sylphx is à la carte too: start with one product and add the rest when they earn their place. The difference is that one company builds every piece to compose — and Cloud is the front door when you want the assembly done. |
| “Do I have to buy the whole platform?” | No. Products are sold and used independently — a Models, Identity, Data, or Compute signup needs no Cloud account. Cloud composes only what you choose. |
| “Is isolation real?” | Per-project Postgres and managed cache — not shared soft tenancy cosplay. |
| “Another AI wrapper?” | Sylphx AI is a family, not a wrapper: Sylphx Models is the catalog and official Responses service; Sylphx Agents is the agent OS. Independent products, independent contracts. |
| “Lock-in?” | Each product owns its contract and issues its own credentials; there is no company mega-SDK. Evaluate each product's export path in its docs. |

## Prefer / avoid

| Prefer | Avoid |
|--------|--------|
| Independent services, à la carte, compose, front door, family hub | Bundle claims: “one SDK”, “one key”, “replaces the frankenstack” |
| Product-owned site, contract, credentials, docs | “Sylphx AI” as a single product name |
| Hibernate, isolation, credits | Fake SOC2 claims without evidence |
| Builder, ship, deploy | Enterprise jargon without substance |
