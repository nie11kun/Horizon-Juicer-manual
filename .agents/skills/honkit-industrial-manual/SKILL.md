---
name: honkit-industrial-manual
description: >-
  Reusable workflow and quality standards for building complete HonKit web and
  Calibre PDF engineering/software user manuals: source-verified content,
  automated UI/VM screenshot capture and pixel-aligned callout annotation, 2x
  supersampled CJK technical diagrams, overflow-proof CSS tables, and
  Playwright/DOM QA checks. Use whenever creating or upgrading a HonKit manual.
---

# HonKit Industrial & Software Manual Workflow

A reusable, source-driven blueprint for producing complete technical user and engineering manuals with **HonKit** (static website + live preview + Calibre PDF export) and automated **Pillow / Playwright** visual pipelines.

---

## 1. Source-of-Truth Verification First

Never write UI enumerations, variable mappings, access levels, or configuration behaviors from memory:
1. Extract exact dropdown labels, enums, and conditional visibility logic directly from UI definitions (`.ui`, XML, form code) and generator/business code.
2. When indexing differs between subsystems (e.g., 0-based backend vs 1-based UI/PLC/HMI bindings), always state both indices explicitly and add a consolidated cross-reference table in the appendix.
3. Redact secrets strictly: never write password derivation formulas, salts, constants, or computed unlock passwords into docs, diagrams, or scripts; verify against an automated secret-keyword scan.

---

## 2. Live Capture & Pixel-Aligned Callout Annotation

Do not rely on outdated manual crops or ad-hoc user screenshots when live software or VM targets can be captured cleanly:
1. **Clean Baseline Capture**: Automate desktop/VM captures (fixing window size / crop coordinates), clean up temporary test artifacts on screen (e.g., transient alarm banners) or mask them deterministically from nearby background pixels.
2. **Structured Annotation Pipeline**:
   - Draw translucent rounded highlight boxes with numbered circular badges paired with a dark bottom legend bar wrapped cleanly with a CJK-capable font (`msyh.ttc` / `PingFang`).
   - **Never occlude target text or input values**: place badges on outer edges (`out_l`, `out_r`, `top_r`, `bot_l`, or adjacent to softkey labels like `vleft` / `htop`) instead of blindly stamping inside tight UI rows.
   - Verify bounding boxes match actual UI regions and every label cites exact verified variable names and screen names (never conflate softkeys that belong to different masks).
3. **Full-Resolution Visual Inspection**: Inspect every generated/updated PNG directly using an image reader before embedding.

---

## 3. High-DPI Supersampled Technical Diagrams

For architecture flows, hardware panels, and geometric schematics:
1. Draw at **2× resolution** (e.g., `3200×1520` -> `1600×760` via `Image.Resampling.LANCZOS`) so curves, arrowheads, and CJK text stay razor-sharp in both web browsers and high-DPI PDF prints.
2. Always use a unified font with full CJK + ASCII symbol coverage (avoid terminal monospace fonts that render `↔` or CJK characters as tofu boxes; prefer ASCII `<->` or TrueType fonts that include every glyph used).
3. Implement pixel-width text wrapping (`textbbox` measurement) that never splits ASCII identifiers mid-token, preventing text overflow outside rounded cards.
4. Separate mutually exclusive UI states clearly (e.g., Welcome Screen vs Runtime Screen softkeys; optional vs mandatory hardware keys).

---

## 4. HonKit Web & PDF Formatting Standards

### 4.1 Preventing Table Right-Edge Clipping
HonKit's default theme sets `.markdown-section { overflow: hidden; }` and tables with long `<code>` identifiers often silently clip on the right in narrower viewports (`1024px–1366px` with open sidebar) or A4 PDF margins. Enforce both:
- **`styles/website.css`**:
  - `.markdown-section { overflow-x: visible !important; }`
  - `table { width: 100%; max-width: 100%; table-layout: auto; }`
  - `th, td { min-width: 0; overflow-wrap: anywhere; word-break: break-word; }`
  - `th code, td code { white-space: normal; word-break: break-all; overflow-wrap: anywhere; }`
  - `table code:before, table code:after { content: none; }` (prevents HonKit pseudo-element spacing artifacts inside tight cells)
- **`styles/pdf.css`**: mirror `table { width: 100%; font-size: 9pt; }`, `tr { page-break-inside: avoid; }`, `thead { display: table-header-group; }`, and `td code { word-break: break-all; font-size: 8.2pt; }`.
- **Markdown authoring**: keep tables concise (`<= 5` columns where possible) and insert `<br>` between dense code enumerations.

### 4.2 KaTeX & Escaping Hygiene
- HonKit `katex` treats any pair of unescaped `$` on the same paragraph as math. Escape prose/HTML currency/system `$` variables cleanly inside HTML `<code>&#36;VAR</code>` rather than raw `$VAR` when two appear in the same paragraph or inside table cells.
- Never nest Markdown backticks `` ` `` inside `<code>...</code>` tags.

### 4.3 Exclusions & Repo Hygiene
- Add non-chapter workspace directories/files (`.agents`, `AGENTS.md`, `tools`, `.github`, build outputs) to `.bookignore` so HonKit ignores them cleanly.
- Keep temporary contact sheets and unembedded working images outside the repository asset directory (or remove/git-ignore them) so final builds ship zero unused images.

---

## 5. Automated QA Gate (Run Before Every Delivery)

1. **Static Audit Script**:
   - Check every `SUMMARY.md` link exists and is non-empty; check zero orphan `.md` chapters.
   - Verify every `![]()` image resolves to a valid non-empty image file; fail on banned legacy image prefixes/directories.
   - Scan outside code blocks for stray unescaped `$` and scan all text for forbidden secret keywords.
2. **HonKit Build + HTML Scan**:
   - Run `npm run build` (`honkit build`) and scan all `_book/**/*.html` for broken ``<code>...`...</code>`` spans and `.katex-error`.
3. **Playwright Multi-Viewport DOM Overflow Audit**:
   - Serve or load every generated `_book/**/*.html` in headless Chromium across desktop-with-sidebar (`1366px`, `1024px`) and tablet/narrow (`800px`, `660px`) viewports; verify `tbl.getBoundingClientRect().right <= sec.getBoundingClientRect().right + 2` and `tbl.scrollWidth <= sec.clientWidth + 2` across all pages. Capture sample screenshots of dense tables and inspect visually.
4. **PDF Export Verification**:
   - Run `npm run pdf` (Calibre `ebook-convert`), verify exit code `0`, size threshold, and `%PDF-` header.
5. **Live Preview Verification**:
   - Start `npm run serve` (port `4000`) and confirm `HTTP 200` on root and deep chapter URLs.
