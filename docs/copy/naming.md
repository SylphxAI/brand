# Sylphx product naming policy (SSOT)

**Status:** Binding. This policy is the company-level naming SSOT for products and
services. Repo-level naming conventions must not contradict it.

## Locked product names

| Layer | Name | Notes |
|-------|------|-------|
| Company | **Sylphx** | Never "SylphX"/"Sylph X". "SylphxAI" is the GitHub org identifier only, not a product name. |
| Platform | **Sylphx Platform** | The PaaS / capability platform. |
| AI product | **Sylphx AI** | Model catalog, routing, metering. Domain `api.sylphx.ai`. |
| AI service (Platform catalog tile) | **Models** | Short display name next to Database / Auth. Full: Sylphx AI. |
| Assistants | **Spiron** | Business-grade AI assistants. |
| Agent-native runtime (client) | **Keel** | |
| Managed DB/Redis/Typesense TLS edge | **Data Edge** | Infra descriptor; not a customer product brand. Repo `SylphxAI/data-edge`. |

## Rules

1. **"Gateway" is retired as a product name.** It must never name a Sylphx product,
   service, runtime, repo display name, deployment, or API.
2. "Gateway" may appear only as generic English or a third-party concept (e.g.,
   industry phrase "API gateway", an upstream partner's "agent gateway" pattern).
3. Sylphx AI runtimes are **Edge** (request serving), **Control** (catalog/policy/
   reconciliation), **Console** (UI), and **Platform Batch**. Never "Gateway Edge".
4. In copy, prefer concrete nouns: SDK, Postgres, hibernate, models, deploy.
   Do not use "gateway" as a marketing noun.
5. New identifiers, files, and docs must not introduce `*-gateway` names for Sylphx
   components. Existing non-conforming identifiers are being renamed in a clean cut;
   do not re-introduce them.
