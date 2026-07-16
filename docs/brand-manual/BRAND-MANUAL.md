# Sylphx Brand Manual

**Version:** 1.0 · **Legal:** Sylphx Limited · **Product:** sylphx.com · **GitHub / npm:** SylphxAI · `@sylphx`  

Tokens: [`tokens/brand.tokens.json`](../../tokens/brand.tokens.json)  
Construction: [`logo/construction/sylphx-construction.svg`](../../logo/construction/sylphx-construction.svg)  
Legacy guidelines: [`guidelines/`](../../guidelines/)

---

## 1. Brand story

### Origin

Builders lost months gluing **Vercel + Supabase + Clerk + AI APIs + a dozen dashboards**. Agent systems made the glue worse: every tool had a different auth story, isolation model, and bill.

**Sylphx** exists so you **stop stitching tools together** — one AI-native platform: services, per-project data isolation, hibernate-to-zero economics, and deploy — plus open infrastructure (MCP, libraries) the ecosystem can trust.

### Narrative

1. **Fragmented stack tax** — time and money before first user.  
2. **One platform** — 22 services, one SDK, one key.  
3. **Real isolation** — dedicated Postgres + cache per project.  
4. **AI first-class** — gateway built-in, agents as customers (Customer Zero).  
5. **Open craft** — public tools that prove engineering quality.

### Mission

Give builders an **AI-native platform** that replaces vendor sprawl without dumbing down infrastructure.

### Vision

The default substrate for AI-era applications and agent systems.

### Promise

*Your entire stack, one platform.*

### Personality

| We are | We are not |
|--------|------------|
| Precise, modern, developer-honest | Enterprise beige vapor |
| AI-native | “AI wrapper” sticker brand |
| Open where it matters | Closed without reason |

---

## 2. Strategy

| Item | Definition |
|------|------------|
| **Category** | AI-native PaaS / developer platform + OSS |
| **Audience** | Builders, AI product engineers, MCP users |
| **Attributes** | Unified · AI-native · Precise |
| **Competitive frame** | Multi-vendor starter stack vs one SDK |
| **Proof** | Live platform, OSS stars/downloads, status page |

---

## 3. Verbal identity

| Element | Spec |
|---------|------|
| Legal | Sylphx Limited |
| Brand | **Sylphx** |
| GitHub org | SylphxAI (org only — not product title) |
| npm | `@sylphx/*` lowercase |
| **Avoid** | SylphX, Sylph X, styling product as “SylphxAI” |
| Tagline (product) | Stop stitching tools together. Ship with one platform. |
| Tagline (legacy guidelines) | Empowering developers to build the future with AI |
| Contact | hi@sylphx.com |

**Primary tagline for PaaS:** product hero line.  
**Legacy line:** OK for broad OSS intros until unified.

### Voice

Technical clarity, restrained confidence, short demos over adjectives.

### Pillars

1. Unified platform  
2. Isolation & hibernate economics  
3. AI built-in  
4. Open engineering proof  

---

## 4. Logo system

### 4.1 Master asset

| File | Size | Role |
|------|------|------|
| `logo/current/icon-512.png` | 512×512 | Master raster |
| `logo/current/icon.png` | 180×180 | General |
| `logo/current/icon-github.jpg` | org avatar | GitHub |

**Gap:** official SVG wordmark still missing from legacy checklist — do not invent; export from design source when available.

### 4.2 Construction (measured ratios)

Normalized to side **S** (e.g. S=512):

| Element | Ratio of S | Example @512 |
|---------|------------|--------------|
| Core disc radius | **0.088·S** | r ≈ 45 px |
| Ring outer radius | **0.275·S** | r ≈ 141 px |
| Ring stroke | **≈0.047·S** | ≈ 12 px |
| Icon field corner | **≈0.22·S** | continuous rounded square |
| Clear space | **≥0.10·S** | all sides |

**Geometry:** concentric **target / node** — solid core + open ring on dark field. Reads as focus, signal, platform core.

### 4.3 Color on icon (measured)

| Token | Hex | RGB | Role |
|-------|-----|-----|------|
| Mark orange | `#D87000` | 216, 112, 0 | Core + ring |
| Field | `#1A1414` / `#201818` | dark warm black | Icon background |

### 4.4 UI colors (guidelines — product chrome)

| Token | Hex | Role |
|-------|-----|------|
| Brand Blue | `#4A90E2` | Buttons, links, accents |
| Brand Dark | `#1A1A2E` | Dark surfaces, headers |
| Text primary | `#2C3E50` | Body |
| Success / Warning / Error | `#27AE60` / `#F39C12` / `#E74C3C` | Semantic |

**Note:** Icon orange and UI blue are **both official** — icon is mark color; blue is product system color. Do not recolor the icon ring to blue without a formal variant.

### 4.5 Sizes

| Context | Min |
|---------|-----|
| UI | 24×24 CSS px |
| Favicon | 16×16 |
| Clear space | 0.1·S |

### 4.6 Misuse

1. Stretch ring into ellipse.  
2. Fill ring solid (loses aperture).  
3. Multicolor gradient on ring without approval.  
4. Light field with low-contrast orange.  
5. Adding text inside the ring.  

---

## 5. Typography

| Role | Spec (guidelines) |
|------|-------------------|
| UI / web | **Inter** 400/500/600/700 |
| Code | **JetBrains Mono** |
| Badges | shields.io `flat-square` |

---

## 6. Imagery

- Dark product UI, code, architecture diagrams, agent workflows.  
- Prefer real platform screens over stock.  
- Orange + dark + blue accent photography grade.

---

## 7. Full branding stack checklist

| Element | Status |
|---------|--------|
| Story | ✅ |
| Strategy | ✅ |
| Verbal + naming rules | ✅ |
| Icon construction ratios | ✅ measured |
| Dual color systems documented | ✅ |
| Guidelines migrated | ✅ |
| SVG wordmark | ⬜ |
| Motion / sound | ⬜ |
| Trademark register | ⬜ |

---

## 8. Governance

Product + brand owner. Align npm, GitHub, and site naming with §3.  
