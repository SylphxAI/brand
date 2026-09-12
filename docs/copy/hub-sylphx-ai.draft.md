# Sylphx AI hub — draft copy for `https://sylphx.ai/`

> **Status: DRAFT — not adopted, not published.** This is a proposal for the
> family hub copy. The hub is a brand surface, not a product (owner decision
> 2026-09-12; `SylphxAI/owner` `standards/authority.md` §11/§13). Open items
> before anything ships: who owns hub content and who owns its hosting and
> deployment. Do not reuse this as current copy until the owner decides.

## Hero

**Eyebrow:** Sylphx AI — the AI brand family

**H1:** Models and agents, one family.

**Sub:** Sylphx AI is the home for the company's AI products. Each member is an
independent product with its own site, API, and credentials.

**CTAs:** [Sylphx Models](https://models.sylphx.ai) · [Sylphx Agents](https://agents.sylphx.ai)

## Members

| Product | What it is | Doors |
|---------|------------|-------|
| Sylphx Models | Model catalog and official Responses service | site `https://models.sylphx.ai` · API `https://api.models.sylphx.ai/v1` |
| Sylphx Agents | Autonomous agent OS and graph | site `https://agents.sylphx.ai` · API `https://api.agents.sylphx.ai` |

## What this hub is not

- Not a product: no contract, credentials, or API of its own.
- No signup and no key issuance — each member issues its own credentials.
- Not a second account, admission path, or control plane over the members.

## Footer

Sylphx AI is a brand family of Sylphx Limited.

---

## Open items (before publishing)

1. **Content ownership** — who writes and owns hub copy (Brand? Owner register?
   a marketing surface?). This draft is not carrying that decision.
2. **Deployment ownership** — who ships the hub. The `sylphx.ai` /
   `www.sylphx.ai` names are inside Cloud's desired hostname set; the content
   source and deploy path are unassigned.
3. **Member list** — today Models and Agents; how future family members join.
4. **Depth** — whether the hub repeats member pricing/console content or only
   ever points at the members.

**Recommendation on items 1–2 (proposal — owner decision, not implemented
here).** Keep hub *content* in this brand repo: the hub is a brand/marketing
surface with no contract, credentials, or API (owner
`standards/authority.md` §11/§13), so its copy belongs with the brand SSOT and
should graduate from this draft to a copy home only when the owner adopts it,
with member names and doors mirrored from owner law rather than authored here.
Deploy it as a static site through Cloud's already-required product edge —
`sylphx.ai`/`www.sylphx.ai` are inside Cloud's desired hostname set per §13 —
so the path is brand-owned content, platform-owned hosting/DNS, no new origin
and no product-shaped runtime. The alternative is a fully platform-owned site
that authors its own copy; the open decision is which side owns the build, and
it should be recorded before the hub is published.
