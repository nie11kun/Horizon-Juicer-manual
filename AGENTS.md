# Horizon-Juicer 手册工程编写与审核规范（Workspace Rules）

本仓库为基于 **HonKit + Calibre PDF** 构建的 `Horizon-Juicer` 与 `HorizonJuicerCreator` 官方中文工程手册。任何修改、扩写、重截图或构建发布，必须严格遵守以下规范：

---

## 1. 源码单一事实来源（Source of Truth）

编写与修改任何功能描述、变量下标、枚举值、报警代码、软键位与工艺公式前，必须直接核对上游工程源码（严禁凭记忆推测）：
- **NC / HMI 程序源库**：`c:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer\Source_Library\`（`.SPF` / `.MPF` / `.DEF` / `HMI/proj/*.com` / `Parameter_Index.md` / `M-sympol_Index.md`）
- **配置生成软件源码**：`c:\Users\Marco Nie\Development\WorkProgram\HorizonJuicerCreator\`（`creatorwindow.ui` / `generatepro.cpp`）

### 1.1 关键工程事实铁律（高频易错点）
1. **NC（0-based）与 HMI ACX（1-based）下标差 `+1`**：
   - `.SPF`、`MGUD.DEF` 与 `Parameter_Index.md` 采用 `0-based` 下标（如 `INI[36]`）；
   - SINUMERIK EasyScreen `.com`（`/NC/_N_NC_GD2_ACX/...`）固定使用 `1-based`（`HMI = NC + 1`，即 `INI[37]`）。
   - 核心变量表必须同时标注或明示换算关系，驱动类配置必须严格区分：`INI[36]` 内/外磨砂轮、`INI[37]` 修整轮、`INI[91]` 磨削中心外圆砂轮。
2. **SINUMERIK 访问权限与钥匙开关严格映射**：
   - **`ac1`**：制造商口令（最高口令级，向下兼容 `ac2`～`ac7`）
   - **`ac2`**：服务口令（向下兼容 `ac3`～`ac7`）
   - **`ac3`**：用户口令（解锁 `VS2 备份恢复`、`VS8→VS1 机床配置`、`a_setting` `Mask0/Mask1` 的 `VS3`、`a_info` 隐藏 `VS3`）
   - **`ac4`**：钥匙开关 **3 档**（解锁参数修改 `WR2, ac4` 及 `VS5 加工统计` / `VS1`、`VS4` 统计重置）
   - **`ac5` / `ac6` / `ac7`**：分别对应钥匙开关 **2 档 / 1 档 / 0 档（最低级）**
3. **分画面与按配置显隐的 `HS` / `VS` 软键纪律**：
   - 欢迎页 `a_custom.com` 底栏仅 `HS7 用户界面`，`VS1/2/3/5/8` 按权限与开关激活；
   - 进入加工区后，`HS4 自动对刀` 仅在勾选自动对刀时显示，`HS5 外圆 / HS6 端面 / HS7 加工选择` 仅在磨削中心（`;ifIsCenter`）显示；
   - `VS1~VS8` 各功能键归属不同子画面（`a_grind`、`a_process`、`a_dress`、`a_auto`、`a_center*`、`a_setting`、`a_stats`），示意图中严禁把不同画面的按钮混画到同一栏。
4. **两条不可省略的现场部署与刷新流程**：
   - **新设备首次导入必做重置**：导入程序包（或重建 `MGUD.DEF`）并首跑主程序后，必须在 `a_setting.com` `Mask1` 点击 **`VS3 重置数据 → Mask2 VS8 确认`** 执行 `SUB(UP6)`，初始化驱动类型（`INI[36]/[37]/[91]`）与读写权限锁；
   - **语言切换热刷新步骤**：进入 **调试（Setup）** 主画面后，**直接点击右侧垂直软键 `VS3 Change language`** 切换语言触发重读，**切勿点底部 `HS5 HMI`**。

---

## 2. 安全保密红线

- **严禁在任何 Markdown、图片、脚本日志或回复中出现** 口令派生公式、魔数常量、位变换名称或算出的具体解锁密码。仅描述挑战码→计算器→输入验证的交互步骤。

---

## 3. 图片采集、框选标注与原理图制作规范

1. **100% 自采与代码生成图表**：禁止复用旧版 `images/schematics/`（`hlp_pic*` / `panel_*`）或用户原始临时截图；目录 `images/schematics/` 不得存在。
2. **标注框与序号气泡规范（[tools/annotate_screenshots.py](tools/annotate_screenshots.py)）**：
   - 所有 UI 截图均需经 `tools/annotate_screenshots.py` 框选核心参数区/软键区，并附带 `Microsoft YaHei` 底部黑底蓝分割线图例栏；
   - **序号气泡不得遮挡关键文本或输入框数值**：优先使用贴边外挂模式（如 `out_l`、`out_r`、`top_r`、`bot_l`、`vleft`、`htop`）或精调坐标；
   - 如实机画面分辨率/DPI 变化或截图坐标更新，修改定义后**必须用 `read_file` 逐张全尺寸目检**确认零错位、零遮挡。
3. **2× 超采样技术示意图（[tools/generate_diagrams.py](tools/generate_diagrams.py) & [tools/build_diagrams_and_cover.py](tools/build_diagrams_and_cover.py)）**：
   - `images/diagrams/` 下架构图与原理图须以 `3200×1520` 绘制再 `LANCZOS` 降采样至 `1600×760`；
   - 使用 `msyh.ttc` / `msyhbd.ttc` 渲染混合中英文（禁用缺字终端字体与方框符号），复杂说明须经像素宽度换行防止溢出边框。

---

## 4. HonKit 排版、KaTeX 与构建验收门禁

1. **表格防截断规则**：
   - `[styles/website.css](styles/website.css)` 与 `[styles/pdf.css](styles/pdf.css)` 已启用表格单元格自动换行与 `code` 断行（`word-break: break-all; overflow-wrap: anywhere;`），并设置 `.markdown-section { overflow-x: visible !important; }` 防止静默裁切；
   - 撰写宽表时控制列数（通常 `<= 5` 列）与长连续路径/数组枚举（必要时用 `<br>` 分行）。
2. **KaTeX 与 HTML 转义安全**：
   - 同一段落中避免出现未转义的双 `$`（如 `$A_DBB[...]` 与 `$MN_...`）；正文中系统美元符变量统一写作 <code>&#36;A_DBB[...]</code>，或在独立代码块内书写；严禁把行内反引号 `` ` `` 跨入 `<code>...</code>` 标签。
3. **收尾必跑验证流水线**（每次修改完成后按序执行，不可跳过）：
   1. `python tools/audit_manual.py` → 确认全部 Markdown 与引用图片存在、无旧图、无敏感词、无散落 `$`，输出 `ALL AUDITS PASSED!`；
   2. `npm run build` → 确认 39 页无报错生成，检查 `_book/**/*.html` 中 `Bad <code> spans` 与 `katex-error` 均为 `0`；
   3. Playwright 视口表格溢出检查 → 在 `1366/1024/800/660px` 视口扫描全部生成页，`overflows` 须为 `0`；
   4. `npm run pdf` → 验证生成 `output.pdf`（大于 1 MB 且 `%PDF-` 头部有效）。
4. 工作流详细操作手册见项目 Skill：[horizon-juicer-manual-workflow](.agents/skills/horizon-juicer-manual-workflow/SKILL.md)。
