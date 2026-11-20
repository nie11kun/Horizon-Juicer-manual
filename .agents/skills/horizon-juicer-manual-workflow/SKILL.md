---
name: horizon-juicer-manual-workflow
description: >-
  End-to-end authoring, VM SinuTrain capture, screenshot annotation, diagram
  generation, HonKit web/PDF build, and Playwright QA workflow for the
  Horizon-Juicer & HorizonJuicerCreator user manual. Activate when updating
  chapters, refreshing UI captures/diagrams, tuning HonKit CSS/tables, or
  verifying builds in Horizon-Juicer-manual.
---

# Horizon-Juicer 手册制作与维护全流程（Runbook）

本 Skill 固化了 `Horizon-Juicer-manual` 从源码核验、VM SinuTrain 实时采图、标注画图到 HonKit Web/PDF 发布验收的完整工程流水线。

---

## 阶段一：源码核查（零臆测原则）

1. **Creator 配置核对**（`c:\Users\Marco Nie\Development\WorkProgram\HorizonJuicerCreator`）：
   - 下拉枚举值与控件显隐联动 → 读取 `creatorwindow.ui`；
   - 输出目录结构、`systemMode`（`0=老828D / 1=新828D / 2=ONE`）、`specificationInfo`、驱动开关转换与裁剪逻辑 → 读取 `generatepro.cpp`。
2. **NC 与 HMI 界面核对**（`c:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer\Source_Library`）：
   - 画面与软键权限（`ac1~ac7`）、掩码路由（如 `a_auto.com` `Mask21->23..27`）→ 读取 `HMI/proj/*.com`；
   - 注意 **`NC 0-based` vs `HMI ACX 1-based（+1）`** 对应关系及驱动参数区分（`INI[36]` 内/外磨轮、`INI[37]` 修整轮、`INI[91]` 外圆轮）；
   - 工艺/修整/对刀/在线量仪逻辑 → 读取对应 `.SPF`（如 `B_C_MOV.SPF`、`J_GRIND_ONLINE.SPF`、`D_EXTERNE_SHAPE.SPF`、`D_LINE_TOOL_SHAPE.SPF`、`M-sympol_Index.md`）。

---

## 阶段二：UI 实时采集与 SinuTrain 刷新

1. **Creator 桌面截图**：使用 [tools/capture_creator_ui.py](../../../tools/capture_creator_ui.py) 自动启动并捕获主界面、路径设置、外/内螺纹配置、口令计算、删注释与版本历史页。
2. **VM SinuTrain 界面捕获与热刷新**：
   - 将 Creator 输出包内 `System-CF-Card` 拷贝到 VM `C:\Siemens\SinuTrain\SINUMERIK CNC-SW 840D sl 4.8 SP4\hmi`（先备份基线）；
   - 在 SinuTrain 中刷新新版画面：**调试（Setup）** 主界面 → **直接点击右侧 `VS3 Change language`**（**勿点底部 `HS5 HMI`**）→ 切换为英文点确认 → 再切回简体中文点确认；
   - 按 `800×600`（标准 SINUMERIK HMI 窗口区域）裁剪原图，确保无临时调试残影（如测试报警/临时状态栏），必要时在 `tools/annotate_screenshots.py` 使用 `erase_rects` 采样邻近背景色遮除，或放入 `tools/raw_overrides/` 优先替换干净底图；
   - **`MGUD.DEF` 兼容红线**：`TECHNOLOGY[431]` 等新字段依赖新版 `MGUD.DEF`（`TECHNOLOGY[500]`）；若 SinuTrain 或真机尚在运行 `TECHNOLOGY[420]` 等旧版定义，切勿在未备份 GUD 数据的情况下直接覆盖/激活 `MGUD.DEF`，须先备份原有 GUD 再升级激活并执行 `VS3 重置数据`。
   - 如需解锁 `a_setting` `Mask1`，必须通过 `HorizonJuicerCreator` 口令计算器或现场挑战码交互完成；严禁在任何文件留存密码公式或硬编码密码。

---

## 阶段三：标注画图与视觉目检

1. **HMI 与软件截图框选标注**（[tools/annotate_screenshots.py](../../../tools/annotate_screenshots.py)）：
   - 规范坐标与气泡模式：尽量使用 `out_l`、`out_r`、`top_r`、`bot_l`、`vleft`（右侧 VS）、`htop`（底栏 HS），确保编号气泡不遮挡界面文字或输入框数值；
   - 运行 `python tools/annotate_screenshots.py` 输出至 `images/creator_*.png` 与 `images/sinutrain/hmi_*.png`。
2. **2× 超采样原理图与封面/架构图**（[tools/generate_diagrams.py](../../../tools/generate_diagrams.py)、[tools/build_diagrams_and_cover.py](../../../tools/build_diagrams_and_cover.py)）：
   - `diag_*.png` 使用 `3200×1520` 画布 + `msyh.ttc` / `msyhbd.ttc` 绘制并 `LANCZOS` 降采样到 `1600×760`；
   - 长文本使用 `wrap_text_px` 按像素宽度换行，避免压线或出框。
   - **特别核对点**：`diag_mcp_keys.png`、`hmi_navigation_map.png`、`arch_ecosystem_flow.png` 中权限必须遵循 `ac1=制造商口令 / ac2=服务口令 / ac3=用户口令 / ac4..7=钥匙开关3..0档`，软键必须按画面分离、标明选配显隐。
3. **目检门禁**：任何重绘或重标注图片必须调用 `read_file` 查看完整输出 PNG，核查文字清晰度、框线包围完整度与气泡对齐度。

---

## 阶段四：Markdown 撰写与样式规则

1. 新增章节或改名须同步更新 `SUMMARY.md`，非手册元文档/脚本目录加入 `.bookignore`（如 `.agents`、`AGENTS.md`、`tools`）；含敏感词检查清单的 `tools/audit_manual.py` 必须留在 `.gitignore` 中，严禁推送到公有仓库。
2. **禁止裸数字下标缩写**：正文与表格引用 NC/HMI 数组或 PLC 地址时，必须写出完整变量名与下标（如 `SHAPE_MODEL[1]` / `SHAPE_MODEL[2]`、`NC：PROCESS[45] / HMI：PROCESS[46]`、`INI[157]` / `INI[160]`、<code>&#36;A_DBB[3]</code> / <code>&#36;A_DBB[4]</code>、`DB4900.DBX3.0` / `DB4900.DBX4.0`），严禁省略数组前缀写成 `（1/2）`、`（103）`、`[160]`、`HMI 44` 等裸数字；密集参数节首须补充 0-based NC vs `+1` HMI 换算说明。
3. **Markdown 表格防断列**：严禁在表格单元格内出现未转义的竖线 `|`（包括行内代码 `` `/user|oem|siemens/...` `` 内部），否则 HonKit 会提前拆分出多余列并遗留裸反引号；多路径/多选项改用顿号、`或`、`/` 或 `<br>`。
4. `$` 符号安全：正文系统变量写为 `<code>&#36;A_DBB[...]</code>`，数学公式用 `$...$` 或 `$$...$$`，不可留孤立 `$`。
5. 宽表格布局：优先控制在 3～5 列；长列表用 `<br>` 分隔；保持 [styles/website.css](../../../styles/website.css) 中 `.markdown-section { overflow-x: visible !important; }` 及 `td code { word-break: break-all; overflow-wrap: anywhere; }` 不被覆盖。

---

## 阶段五：完整 QA 验收流程

按顺序执行并全部通过后方可交付：

1. **HonKit 静态站点构建与审计流水线**：
   ```powershell
   npm run build
   python tools/audit_manual.py
   ```
   确认 39 页零报错生成、`SUMMARY.md` 无缺页/孤儿页、图片全存在、无旧图/敏感词/散落 `$`、无裸数字下标缩写、Markdown 表格列数一致，且 `_book/**/*.html` 中 `<table>` 列数完全匹配（`td == th`）、`<code>` 标签完整、零残余反引号/星号与零 `katex-error`，输出 `ALL AUDITS PASSED!`。
2. **Playwright 多视口表格防溢出实测**：
   - 使用 Python `playwright.sync_api` 打开 `_book/` 全部 39 个 HTML 页面，在 `1366px（带侧边栏）`、`1024px（带侧边栏）`、`800px`、`660px` 视口下检测 `.markdown-section table` 的 `getBoundingClientRect().right` 与 `scrollWidth` 是否超过 `.markdown-section`，确认溢出数为 `0`，并对复杂表格与最新改动页面截图 `read_file` 复查。
3. **PDF 导出与检验（先停 Serve 防 OOM）**：
   ```powershell
   # 先停止端口 4000 / 35729 上运行的 honkit serve，避免 chokidar 监听 _ebook_tmp 触发堆溢出
   npm run pdf
   ```
   确认退出码为 `0`、`output.pdf` 大于 `1 MB` 且文件头为 `%PDF-`。
4. **Git 提交与 GitHub Pages 部署核验**：
   - `git status` 确认 `tools/audit_manual.py` 未被暂存/跟踪，仅提交手册正文、规范与资产变更；
   - 推送 `origin main` 后，通过 `.github/workflows/deploy.yml` 自动构建并发布至 `gh-pages`（保持 `CNAME`=`hj-manual.niekun.net`），验证 Actions 运行为 `success`。
5. **本地预览服务验证**：
   后台启动 `npm run serve`，检查 `http://localhost:4000/` 及代表章节返回 `HTTP 200`。
