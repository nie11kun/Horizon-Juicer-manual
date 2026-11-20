# 10.3 MGUD 全局变量索引与条件编译标记

## 1. 索引偏移黄金铁律（0-based vs 1-based）

> **阅读与二次修改前必读**：  
> - **NC 控制器子程序 / `MGUD.DEF` / `Parameter_Index.md`**：采用 **0-based** 数组下标（如 `INI[0]`、`DRESSER[0]`、`TECHNOLOGY[56]`）；  
> - **SINUMERIK EasyScreen HMI 界面 `.com` 脚本（`/NC/_N_NC_GD2_ACX/...`）**：西门子底层规定从 **`1`** 开始索引（即 **HMI 索引 = NC 索引 + 1**）。例如 NC 程序读写的 `INI[16]`（螺旋升角使能），在 `a_setting.com` 里绑定的是 `"/NC/_N_NC_GD2_ACX/INI[17]"`！  
> 若需手动查改 `.com` 脚本绑定，请务必谨记 **加 1** 换算规则。

### 1.1 高频核心变量 0-based（NC）与 1-based（HMI ACX）速查对照表

| 变量数组 | NC 下标（0-based） | HMI ACX 绑定（1-based） | 核心功能 / 控制含义 |
| :--- | :--- | :--- | :--- |
| **`INI`** | `INI[16]` / `INI[36]` / `INI[68]`<br>`INI[84]` / `INI[130]` / `INI[144]`<br>`INI[149]` | `INI[17]` / `INI[37]` / `INI[69]`<br>`INI[85]` / `INI[131]` / `INI[145]`<br>`INI[150]` | 螺旋升角使能 / 砂轮驱动类型 / 自磨夹具使能<br>内磨退出方式 / 出厂编号 / 恒转速模式<br>外圆在线量仪开关 |
| **`PROCESS`** | `PROCESS[15]` / `PROCESS[41..48]`<br>`PROCESS[94]` / `PROCESS[122]` | `PROCESS[16]` / `PROCESS[42..49]`<br>`PROCESS[95]` / `PROCESS[123]` | 扩展工艺开关 / 磨削中心 5 工序勾选及接触位<br>外圆台阶总开关 / 机械手辅助参数 |
| **`TECHNOLOGY`** | `TECHNOLOGY[56/57/109/127]`<br>`TECHNOLOGY[158/232/307/310]`<br>`TECHNOLOGY[368/431]` | `TECHNOLOGY[57/58/110/128]`<br>`TECHNOLOGY[159/233/308/311]`<br>`TECHNOLOGY[369/432]` | 备份页 / 统计页 / 两端变径 / 内磨测量模式<br>开关测头切换 / 自磨夹具显示 / 附加冷却 / 分段补偿<br>配件寿命界面显示 / 平面修砂轮显示开关 |
| **`DRESSER`** | `DRESSER[0/3/4/5]`<br>`DRESSER[56/110/112/141]` | `DRESSER[1/4/5/6]`<br>`DRESSER[57/111/113/142]` | 修整器类型 / 滚轮类型 / 齿形选择 / 新旧砂轮<br>插补平面 / 外部齿形显示 / 双圆弧比例 / 平面修锥度(mm) |
| **`TOOL_SET`** | `TOOL_SET[8/10/16]`<br>`TOOL_SET[41/57/59]` | `TOOL_SET[9/11/17]`<br>`TOOL_SET[42/58/60]` | 首次二次对刀 / 测头水平距 / 机械手按钮开关<br>对刀结果微调 / 首件工件标志 / 螺距变换总开关 |
| **`RING` / `SCREW_TAP`** | `RING[0]` / `RING[49]`<br>`SCREW_TAP[0]` | `RING[1]` / `RING[50]`<br>`SCREW_TAP[1]` | 螺纹环形槽切换 / 环形槽显示开关<br>丝锥铲磨总开关 |

## 2. `MGUD.DEF` 核心全局数组清单

因全局名称数量超过 60 个，激活 `MGUD.DEF` 前必须确保 **`MD18120 >= 70`**。各主要组数组定义与规模如下：

| 数组 / 变量名 | 类型与规模 | 管理职责范围 |
| :--- | :--- | :--- |
| `AXIS_VER` / `AXIS_HORI` / `AXIS_EW` | `STRING[1]` | 当前修整垂直轴、水平轴及磨削中心外圆切入轴名（如 `X` / `U` / `V` / `W`） |
| `SHAPE` / `WORM_SHAPE` / `WHICH_COMMON_SHAPE` / `SHAPE_EXTERNAL` | `STRING[20]` | 当前生效的齿形子程序、蜗杆齿形、通用齿形及外部自定义轨迹文件名 |
| **`INI[260]`** | `REAL` | 工件基本几何、左右端坐标、速度设定、各类核心功能初始化标志位 |
| **`DRESSER[240]`** | `REAL` | 修整器类型、砂轮新旧状态、报警码 `DRESSER[6]`、粗精修与磨削中心修整坐标 |
| **`WHEEL[30]`** | `REAL` | 修整滚轮直径、线速度、圆弧半径、间距、滚压轮停留与初始/当前接触位 |
| **`GRIND[10]`** | `REAL` | 磨削类型、按键触发态镜像、中径单次调整、空运行热机开关等 |
| **`PROCESS[130]`** | `REAL` | 当前/初始磨削接触位、工艺累计磨削量、磨削中心外圆/端面/台阶参数与开关 |
| **`TECHNOLOGY[500]`** | `REAL` | 批量/单件四道工序工艺表、梯度进刀、分头补偿、多段补偿、多螺距、反向孔与 Y 轴等 |
| **`TOOL_SET[150]`** | `REAL` | 首次/二次对刀基准、DRF 偏置采样、测量水平距、开关/测头机构与界面限值 |
| **`SHAPE_MODEL[140]`** | `REAL` | 三角、梯形、双圆弧、行星齿、多线修整及批量起始工序选择等参数 |
| **`RING[50]`** / **`SCREW_TAP[20]`** | `REAL` | 环形槽 4 组阵列参数 / 丝锥直槽螺旋槽与跳齿铲磨参数 |
| `COMMON_*[20]` | `REAL` | 通用 10 线段积木齿形模型计算数组（长度、夹角、圆弧及交点参考坐标） |
| `DIY[10]` / `WORK[10]` / `TECH_TIME[10]` | `REAL` / `INT` | DIY 独立工艺、多头工件计数及当前各工序已执行次数 |
| `TECH_DRESS_DEEP[80]` / `_FEED[80]` / `WHEEL_LINESPEED_DRESS[80]` / `TECH_DRESS_TIME[80]` | `REAL` / `INT` | 工序内及批量/单件/外圆/端面分立修整参数组 |
| `SERVICE_LIFE[50]` / `_TXT[50]` | `REAL` / `STRING[100]` | 滚轮、夹具、金刚笔 1/2 设定寿命、当前累计、报警阈值及重置时间 |
| `CUR_WHEEL` / `WHEEL_GRIND_CUMU[100]` / `WHEEL_CHANGED_DATA[100]` | `INT` / `STRING[30]` | 99 组更换新砂轮加工产量及换轮时间戳台账 |
| `DRESS_WHEEL_NUM[100]` / `_DATE[100]` | `STRING[30]` | 100 个金刚石滚轮编码与上线启用时间档案 |
| `CHOICE` / `BACKUP_*` / `RESTORE_*` / `BR_MSG` | `REAL` / `STRING` | 全局参数备份与恢复控制及文件名变量 |

## 3. 专用 `R` 参数占用约定

| `R` 参数区间 | 专属用途 |
| :--- | :--- |
| **`R299 ~ R296`** | 模拟量控制输出给定：内磨砂轮 1 转速（`R299`）、外圆砂轮 2 转速（`R298`）、修整轮 1/2 转速（`R297` / `R296`） |
| **`R280 ~ R282`** | 同步动作与退刀中断采集暂存：退刀瞬时 `X`（`R280`）、`Z`（`R281`）、`VW` 同步退刀标记（`R282`） |
| **`R240 ~ R267`** | **内螺纹反向孔倒角**：倒角总个数（`R240`）、C 移角（`R241`）、倒角深度（`R242`）、底面 C 角（`R243`）及 `R244~R267` 第 1～24 孔 Z 坐标 |
| **`R100 ~ R102`** | **桁架机械手**：吹气时头架转速（`R100`）、保持时间（`R101`）、卡盘/尾架联动开关（`R102`） |
| **`R20 ~ R40`（局部复用）** | `自磨夹具 R 变量版` 专用起止与进刀参数 |
| **`R3 ~ R29`（蜗杆复用）** | 蜗杆修整循环计算中心距、当前直径/位置及粗精修临时参数 |

## 4. `ReplaceMarker.md` 条件编译标记全表（`;ifIs...`）

`HorizonJuicerCreator` 依据下表在源码（`.SPF`/`.MPF`/`.com`/`.txt`）中识别行末 `;ifIs...` 单行裁剪或成对 `;ifIs...Begin` ～ `;ifIs...End` 块级裁剪标记：

| 功能分类 | 允许使用的条件编译标记 |
| :--- | :--- |
| **语言与系统授权** | `ifIsCHS` / `ifIsENG` / `ifIsHasEncryption` / `ifIsNotHasEncryption` / `ifIsHasLoadingArm` / `ifIsNotHasLoadingArm` / `ifIsOneSystem` / `ifIsNotOneSystem` |
| **机型与丝锥/蜗杆/中心** | `ifIsExternal` / `ifIsInternal` / `ifIsHasWorm` / `ifIsNotHasWorm` / `ifIsScrewTap` / `ifIsNotScrewTap` / `ifIsCenter` / `ifIsNotCenter` / `ifIsInternalOnly` |
| **磨削中心外磨轴系** | `ifIsHasU` / `ifIsNotHasU` / `ifIsNotHasUBack` / `ifIsNotHasUFront` |
| **对刀与测量硬件** | `ifIsHasReOperate` / `ifIsNotHasReOperate` / `ifIsAuto` / `ifIsNotAuto` / `ifIsKaiGuanCeLiang` / `ifIsCeTouCeLiang` / `ifIsKaiGuanAndCeTouCeLiang` / `ifIsProbeFront` / `ifIsNotProbeFront` |
| **修整器架构组合** | `ifIsXW` / `ifIsNotXW` / `ifIsUW` / `ifIsNotUW` / `ifIsDressWare1`（VW/V）/ `ifIsDressWare2`（V）/ `ifIsDressWare3`（XZ/X）/ `ifIsDressWare4`（X内后）/ `ifIsDressWare5`（液压）/ `ifIsExternalVW` / `ifIsFrontDress` / `ifIsBackDress` / `ifIsVW` / `ifIsVWSR` / `ifIsVWSide` / `ifIsV` / `ifIsXWai` / `ifIsXNeiFront` / `ifIsXNeiBack` / `ifIsVH` / `ifIsXZSR` / `ifIsXZSide` |
| **滚轮与齿形细分** | `ifIsSingleAndRound` / `ifIsSide` / `ifIsAllShape` / `ifIsArc` / `ifIsOnlyArc` / `ifIsHasOtherCommonShape` |
| **A 轴与电主轴驱动** | `ifIsHasA` / `ifIsNotHasA` / `ifIsSiFuInGrindWheel` / `ifIsNotSiFuInGrindWheel` / `ifIsSiFuInExGrindWheel` / `ifIsNotSiFuInExGrindWheel` / `ifIsSiFuInDressWheel` / `ifIsNotSiFuInDressWheel` |
