# hlp_capture —— HMI 帮助文档（hlp）制作工具

用于生成和维护 `Horizon-Juicer/Source_Library/HMI/hlp/chs` 下的 SINUMERIK HMI 在线帮助：正文编写、`.com` 帮助链接、SinuTrain 实机截图、自查。

所有命令都在 **Horizon-Juicer-manual 仓库根目录** 下执行：`python tools/hlp_capture/<脚本>`。
源码仓库路径默认是 `C:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer`，可以用环境变量 `HJ_SOURCE` 覆盖。

---

## 1. 内容规范

- **读者是终端操作人员**：只写怎么操作、怎么设置（取值怎么定、在哪里测量、填什么），以及设置后机床会做什么动作。
- **不写底层实现**：不出现变量名、数组下标（如 `INI[..]`）、NC/HMI 下标换算，也不写程序内部逻辑。修改权限（钥匙开关档位或口令级别）可以写。
- **先查源码再写**：先读 NC/HMI 源码，弄清参数的真实含义。
- **格式保持西门子原样**：HTML/XML 结构和 `main.css` 里的 class 都不能改。由 `build_hlp.py` 负责输出：UTF-8 BOM、CRLF 换行；`user_guide.xml` 用 Tab 缩进。
- **配置差异**：只能用 `Source_Library/ReplaceMarker.md` 里定义的标记，形式为 `<!--ifIsXxxBegin/End-->`。
- **锚点**：原有锚点（如 `S1D1`）一律保留，新增参数在后面续号，避免已发出的程序包里的帮助链接失效。
- **截图**：全部来自 SinuTrain 实机，挑战码之类的随机数据要遮掉。
  - 总览界面（磨削、工艺、修整、齿形等）一律用**出厂默认状态**截图：最小配置程序包（`ext_min` / `int_min`）+“重置数据”+ GUD 预设“默认”，不开任何隐藏界面，齿形保持普通模式。
  - 隐藏功能界面单独截图，且**只打开该功能自己的开关**（`gud_helper.py` 里每个功能一个预设）。
  - 红框只在需要时加，且必须在 `hlp_src/chs/img_caps.yaml` 写说明，构建时自动输出在图下方；`audit_hlp.py` 会检查。
- **隐藏功能要交代**：由机床配置开关控制显示的参数或界面，正文必须写“需在机床配置中开启 **xxx** 后显示”（`check_config.py` 会检查）。
- **Creator 不处理的标记**：`ifIsHasA`、`ifIsHasLoadingArm`、`ifIsHasWorm` 在帮助页面里不会被删除；`ifIsHasReOperate` 只在外螺纹机型里处理。这些内容要写成条件句（“带 A 轴的机床…”），二次对刀相关内容要再套一层 `ifIsExternal`。
- **"机床配置"界面**：在功能介绍章节里只说明它是配置管理界面、要访问需联系制造商，不展开细节。

## 1.1 多语言（chs / eng / rus）

- 三种语言的正文分别在 `hlp_src/chs|eng|rus/`，结构、锚点、图片文件名完全一致；中文定稿后再同步英文、俄文。
- 参数名称、选项、软键一律照抄该语言界面上显示的文字（取自 `HMI/lng/almc_<lng>.txt`，同一编号按配置有不同版本时取对应配置的版本），可在括号里补充含义。界面文字有错译或缺译时照实写，并在括号里说明。
- 程序报警写屏幕上实际显示的文字；只有中文的提示（程序里没有英俄分支）按中文原样写并注明含义。
- 所有脚本都接受 `--lng chs|eng|rus`（或环境变量 `HLP_LNG`），默认 chs：
  - `build_hlp.py --lng eng`、`audit_hlp.py --lng eng`、`check_mapping.py --lng eng`、`check_config.py --lng eng`
  - `gen_package.py --lng eng all`：英文/俄文时 Creator 用英文模式生成，包里同时带 chs/eng/rus 三套帮助
  - `verify_package.py --lng eng`
  - `capture_lang.py --lng eng [组…]`：按该语言界面采全部截图（存到 `raw/<lng>/`），结束后自动导回基线包并切回中文界面
  - `install_images.py --lng eng`：装入 `hlp/<lng>/UserGuide/resources/img`
- 构建脚本里的固定字样（推荐设置、取值范围、修改权限等）按语言输出，见 `build_hlp.py` 的 `L10N`。

## 2. 目录

| 路径 | 说明 |
|---|---|
| `hlp_src/chs/section_N.yaml` | 帮助正文唯一源（HTML 为生成物，勿手改） |
| `hlp_src/chs/toc.yaml` | 目录源 → `index.html` + `user_guide.xml` |
| `raw/` | 原始 800×600 截图（gitignore） |
| `out/` | 清单、调研卷宗等中间产物（gitignore） |

## 3. 完整流程

1. **调研**：
   - `inventory.py`：生成参数清单。
   - `masks.py a_grind.com Mask1`：查看某个 Mask 的界面布局。
   - `xref.py --file a_grind.com`：查某个参数在程序里的真实用法。
2. **编写**：修改 `hlp_src/chs/*.yaml`。
3. **构建**：运行 `build_hlp.py`，生成 HTML 和目录。
4. **挂链接**：先运行 `link_help.py` 做演练，确认无误后加 `--write` 写入。
   - 它按 YAML 里的 `var` 给 `.com` 的 DEF 挂帮助链接，或修复失效链接。
   - 只改 DEF 末尾的帮助字段，其余字节不动。
5. **采图**：
   - `gen_package.py <配置>`：生成采图包（老版 828D 模式）。
   - `capture_set.py <配置>`：在 SinuTrain 里截图。
   - `install_images.py`：裁剪、加框、压缩，然后装入帮助目录。
   - **最后用 `tinifier.bat <文件或目录>` 压缩新增或更新的图片**（用户自带的 TinyPNG 压缩脚本，在 PATH 中，直接命令行调用；目录会递归处理）。只传本次改动的文件，避免重复消耗额度。手册 `images/` 下新增或更新的截图同样处理。
6. **自查**：运行 `audit_hlp.py`，必须输出 `ALL HLP AUDITS PASSED`。加 `--delete-orphans` 会删除没人引用的图片。
   - `check_config.py` 必须 `TOTAL 0`：配置标记与机床配置开关的说明是否齐全。
   - 再运行 `check_mapping.py`，必须输出 `TOTAL 0`。它逐个控件核对：帮助名称与界面标签、下拉选项是否都写进范围、修改权限、没有控件引用的参数条目，并严格扫描正文里的变量名。
7. **实机核对**：
   - `gen_package.py all` 生成全部配置的程序包，再运行 `verify_package.py`：确认没有该机型不具备的功能内容残留（ERROR 必须为 0）。
   - 在 SinuTrain 里选中一个参数按 **HELP**，确认跳转到正确的说明。
8. **恢复环境**：导回基线程序包 `SKR7620B(#02-Latest20261119)`。
9. **提交**：Horizon-Juicer 在 `niekun` 分支按阶段提交；本仓库提交但不推送，除非明确要求。

## 4. 脚本一览

| 脚本 | 作用 |
|---|---|
| `inventory.py` | 扫描 `HMI/proj/*.com`，输出全部 DEF 控件清单（`out/inventory.json/md`） |
| `xref.py` | 每个参数的界面文字、Parameter_Index 释义、NC 程序引用行 |
| `masks.py` | 按 Mask 打印控件布局 |
| `build_hlp.py` | YAML → HTML / 目录 |
| `link_help.py` | 自动挂接 / 修复 `.com` 帮助链接 |
| `audit_hlp.py` | 链接、标记、图片、变量泄露自查 |
| `check_config.py` | 配置标记与“机床配置开关”说明检查 |
| `verify_package.py` | 检查各配置 Creator 生成包里的帮助是否残留不具备的功能 |
| `check_mapping.py` | 帮助与界面逐项对应检查（标签、选项、权限、未引用条目、内部名称） |
| `html2yaml.py` | 把旧帮助页一次性导入为 YAML |
| `gen_package.py` | 调用 HorizonJuicerCreator 生成采图包（窗口在屏幕外后台运行，自动备份并还原 `~/HorizonJuicerCreator.json`） |
| `hmi.py` | SinuTrain 操作封装：导入并刷新、软键与面板按键、截图 |
| `unlock_setting.py` | 解锁"机床配置"：OCR 读取挑战码，调用 Creator 自带的口令计算页得到结果，不使用剪贴板，也不输出或保存口令 |
| `gud_helper.py` | 临时覆盖 `a_info.com`，用软键写入 GUD 预设，用来打开各隐藏界面 |
| `capture_set.py` | 按配置批量截图（`ext_vw` / `ext_xz` / `ext_hyd` / `int_xz` / `ctr_u` 等） |
| `capture_lang.py` | 按语言一次采全部帮助截图（分组：demo ext tap int auto_int auto_ext ctr hyd uw；`demo` 包机型为 TEST，用于欢迎页和出厂信息） |
| `install_images.py` | 截图遮挡、加框、量化压缩并装入 `resources/img` |
| `ocr_digits.ps1` | Windows 内置 OCR（只返回数字） |

## 5. YAML 写法要点

- `params` 中每个参数：`id`、`name`、`rec`、`range`、`unit`、`ac`（修改权限级别）、`text`、`var`（只供维护参考，不输出）、`marks`。
- 文本行写成 `?ifIsInternal: …`，就只在该配置下保留；步骤（`steps`）里同样支持。
- 同一锚点在互斥配置下需要重复出现时，加 `dup: true`。
- 只在表格或软键中出现、没有输入控件的参数，加 `nofield: true`（或在范围里写"软键"），check_mapping 不会把它当成未引用。
- 控件的帮助链接以 `var` 为准：链接指向的条目的 `var` 与控件不一致时，`link_help.py` 会自动改指（机床配置页除外）。所以同一变量在多个页面有说明时，每个条目都要写上该 `var`。
- 行内写法：`**强调**`、`[文字](section_3.html#S3D4)`。

## 6. VM / SinuTrain 注意事项

- **桥接代理**：在虚拟机里运行 `tools/vm_bridge/vm_agent.bat`。
  - `vm_agent.ps1` 只能写**纯 ASCII**：Windows PowerShell 5.1 会按 ANSI 读取没有 BOM 的文件，有中文代理就启动不了。
  - 改了 ps1 之后要重启 bat。
- **窗口要求**：SinuTrain 全屏、不拆分窗口。HMI 画面在屏幕坐标 (150,71)–(950,671)。`.com` 里的坐标换算到 HMI 约为 (1.25x, 80+1.25y)。
- **下拉框**：打开后高亮总在第一项，按 DOWN 的次数等于目标项的序号。
- **欢迎页菜单**：VS8 在主菜单和扩展菜单之间切换。
- **新导入的程序包**：必须先执行"机床配置 → 重置数据"。
- **界面卡在空白页**：按左下角 **^**（RECALL）退出。
- **自动对刀界面空白**：先点 **磨削参数**（HS1），再点 **自动对刀**（HS4），一般就能正常显示（`capture_set._shot_auto` 重试时已这样做）。
- **键盘快捷键**（SinuTrain 手册，`hmi.SHORTCUTS` / `hmi.hotkey()`，经 vm_agent 的 send_keys 发送）：
  - F1–F8 = 水平软键 1–8；Shift+F1–F8 = 垂直软键 1–8；F9 = RECALL（^）；Shift+F9 = ETC（>）
  - F10 = MENU SELECT；Shift+F10 = MACHINE；F11 = CHANNEL；F12 = HELP；PgUp/PgDn = 翻页
  - Enter = INPUT；Insert = INSERT；小键盘 5 = SELECT；Esc = ALARM CANCEL
  - Ctrl+Alt+Shift+1 = JOG，3 = RESET，4 = CYCLE START，5 = CYCLE STOP，6 = MDA，7 = SINGLE BLOCK，8 = AUTO
  - **Ctrl+Alt+Shift+2 = 关闭 SinuTrain 机床**，采图时不要发送
  - 机床概览：Enter 启动所选机床，Del 删除，Ctrl+C 复制，Ctrl+T 创建用户模板
- **SinuTrain 菜单**：机床 → 启动/关闭/重启/导入/导出；视图 → 划分为小窗口（拆分）/显示控制面板；工具 → 用户模板、HMI 附加语言。
- **GUD 预设**：变量名不能用 `G0…`，会被 EasyScreen 拒绝；隐藏字段（位置 0,0,0）的写入不会生效。
- **Creator 生成**：必须等它写完程序包、标记处理完毕再结束进程，`gen_package.py` 已经处理了这一点。
- **与用户共用机器**：采图期间用户可以照常使用宿主机，但不能操作虚拟机，SinuTrain 也不能最小化。开始采图前先确认 VM 空闲。
- **安全**：仓库和脚本里严禁出现口令算法或口令明文。
