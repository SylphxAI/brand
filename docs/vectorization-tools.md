# Image → Vector：有咩模型／工具可以「睇圖勾線」

Potrace / 手砌 SVG **唔會理解** logo 結構，只係跟邊緣。  
要「睇完圖再勾返所有線」，業界實際有幾類方案：

---

## 1. 專用 AI Vectorizer（最啱你而家呢個需求）

| 工具 | 做咩 | API | 我哋而家 |
|------|------|-----|----------|
| **[Recraft Vectorize](https://fal.ai/models/fal-ai/recraft/vectorize)** | 專門 raster → **真 SVG** | FAL：`fal-ai/recraft/vectorize` | ⛔ 本機 **冇 `FAL_KEY`** |
| **[Recraft Studio AI Vectorizer](https://www.recraft.ai/ai-image-vectorizer)** | 網頁上傳 PNG/JPG → SVG | 產品 UI | 你可人手上傳 |
| **[Vectorizer.AI](https://vectorizer.ai/)** | Logo / 平面圖 AI 矢量化，預覽＋匯出 SVG/EPS | 有付費 API | 未接 |
| **Canva Vectorizer** | 快速 JPG/PNG → vector | 產品內 | 人手 |

**推薦順序（logo 逆向）：**  
1. **Recraft Vectorize (FAL)** — 你話有 FAL credential，接上 `FAL_KEY` 我就可以批量跑  
2. **Vectorizer.AI** — 對「已係平面 logo 的 PNG」通常最乾淨  
3. Vision LLM 寫 SVG（下面第 2 點）— 適合 **簡單幾何**（例如 Sylphx 同心圓）

### FAL Recraft 用法（接好 key 之後）

```bash
export FAL_KEY="..."   # 唔好 commit
# image_url 或 upload 後：
# POST fal-ai/recraft/vectorize
# input: { "image_url": "https://.../logo.png" }
# output: { "image": { "url": "...svg", "content_type": "image/svg+xml" } }
```

限制（FAL docs）：PNG/JPG/WEBP、<5MB、解析度 <16MP、邊長 256–4096。

---

## 2. Vision LLM「理解圖 → 寫 SVG 碼」

| 模型 | 路線 | 適合 |
|------|------|------|
| **Gemini 2.5 Pro / Flash**（OpenRouter） | 睇圖 + 輸出 `<svg>` | 簡單／中等幾何 icon |
| **GPT-5.x vision** | 同上 | 簡單 icon、字標結構描述 |
| **Claude Sonnet vision** | 同上 | 結構說明＋簡化 path |

**已試（本機 OpenRouter）：**

| Logo | 結果 |
|------|------|
| **Sylphx** | ✅ 可用 — 同心圓 + rounded square 好得近 |
| **Nakuz** | ⚠️ 近似鳥形，未夠準 |
| **Cubeage cube** | ❌ Vision 版差過 **potrace** — 保留 potrace 做主檔 |
| **MiniMax** | ❌ 理解錯成 nested diamond |
| **Epiow** | ❌ 改壞咗 E／arc — **保留原 SVG master** |

結論：Vision→SVG **唔係萬能**；複雜 3D ribbon / 多層透明要靠 **專用 vectorizer** 或原檔。

---

## 3. 經典 / 開源描邊（無「理解」，但穩）

| 工具 | 說明 |
|------|------|
| **Potrace** / potracer | 黑白輪廓；Cubeage 效果好 |
| **vtracer** | 彩色分層描邊，有時靚過 potrace |
| **Adobe Illustrator Image Trace** | 桌面最強之一 |
| **Inkscape Trace Bitmap** | 免費桌面 |

---

## 4. 生成式 Vector（Text→SVG，唔係逆向）

| 模型 | 說明 |
|------|------|
| **Recraft V3/V4 Vector** | 直接出 SVG；偏「新畫」唔係 1:1 跟原圖 |
| OpenRouter 上部分 Recraft 模型 | 可出 `image/svg+xml` |

適合 **重畫品牌**，唔適合「像素級跟舊 logo」。

---

## 5. 建議我哋點做

| 優先 | 行動 |
|------|------|
| **P0** | 你提供 **`FAL_KEY`** → 我對 Sylphx / Nakuz / MiniMax / Cubeage 原圖跑 **`fal-ai/recraft/vectorize`** 批量入 `logo/current/*-recraft.svg` |
| **P1** | 複雜 mark 人手用 **Vectorizer.AI** 上傳原 PNG，下載 SVG drop 入 repo |
| **P2** | 簡單 icon 繼續用 **Gemini vision→SVG** 做 draft |
| **P3** | 有 Illustrator 原檔就直接 `logo/sources/original/` — 永遠最準 |

---

## 6. 而家 repo 入面嘅檔

| 品牌 | 主推 vector | 備註 |
|------|-------------|------|
| Cubeage | `mark.svg` (potrace) | `mark-vision.svg` 僅實驗 |
| Sylphx | `icon.svg` (Gemini vision v1) | 幾何乾淨 |
| Nakuz | `icon.svg` (vision) | 待 Recraft  refining |
| MiniMax | `icon.svg` (vision/potrace 混) | 待 Recraft |
| Epiow | `logo.svg` **原 master** | 唔使 vision 取代 |

---

*接 FAL key 之後開一張 work item：batch vectorize all brand rasters.*
