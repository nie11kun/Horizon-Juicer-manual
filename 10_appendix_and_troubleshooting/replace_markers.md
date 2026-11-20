# 10.5 条件编译与字符替换标记全表

本节对照 `Source_Library/ReplaceMarker.md`、`HorizonJuicerCreator/generatepro.cpp` 与 `oneReplace.json`，完整列出代码生成器执行的全部 **66 项条件编译标记（`;ifIs...`）**、**4 种源码书写语法**、**12 项文本占位/剥离规则** 以及 **47 项 Sinumerik ONE 跨平台替换映射**。

## 1. 替换标记编写规范（4 种语法形式）

当 `HorizonJuicerCreator` 判定某项特性 **不适用** 于当前配置时，会按正则匹配并把整行或整块替换为保留占位符（NC/HMI 文件替换为分号 `;`，在线帮助 HTML 替换为 `<!--removed-->`）：

| 适用文件类型 | 作用粒度 | 编写语法格式 | 裁剪后输出 |
| :--- | :--- | :--- | :--- |
| `.SPF` / `.MPF` / `.com` / `.ini` / `.txt` | **行级标记** | `<有效语句> ;ifIsXXX`（行末词边界匹配） | `;`（整行删除并留空注释符） |
| `.SPF` / `.MPF` / `.com` / `.ini` / `.txt` | **块级标记** | `;ifIsXXXBegin` … 多行代码 … `;ifIsXXXEnd` | `;`（跨行整块删除） |
| `HMI/hlp/**/*.html`（在线帮助） | **行级标记** | `<HTML 行><!--ifIsXXXLine-->` | `<!--removed-->` |
| `HMI/hlp/**/*.html`（在线帮助） | **块级标记** | `<!--ifIsXXXBegin-->` … 多行 HTML … `<!--ifIsXXXEnd-->` | `<!--removed-->` |

## 2. 全量 66 项 `;ifIs...` 条件编译标记索引表

> **驱动标记极性特别提醒**：在 `creatorwindow.ui` 中，`grindWheelType`、`exGrindWheelType`、`dressWheelType` 的下拉第 `0` 项为 **伺服**、第 `1` 项为 **变频器**。`generatepro.cpp` 在裁剪 `a_setting.com` 时：`0=伺服` 保留 `;ifIsNotSiFuIn...`（向 `INI[36]`/`INI[37]`/`INI[91]` 写入 `1`）；`1=变频器` 保留 `;ifIsSiFuIn...`（写入 `0`）。切勿仅凭英文名称字面误判。

### 2.1 语言与平台（4 项）

| 条件编译标记（`ReplaceMarker.md`） | 源码中文含义 | 保留条件（`generatepro.cpp`） | 作用目录 / 备注 |
| :--- | :--- | :--- | :--- |
| `ifIsCHS` | 中文 | `lng == 0`（中文） | `CMA`、`.MPF` 源码 |
| `ifIsENG` | 英文 | `lng == 1`（多语言） | `CMA`、`.MPF` 源码 |
| `ifIsOneSystem` | 是ONE系统 | `systemMode == 1`（新版 828D）或 `systemMode == 2`（Sinumerik ONE） | `HMI/lng`、`CMA` |
| `ifIsNotOneSystem` | 不是ONE系统 | `systemMode == 0`（老版 828D） | `HMI/lng`、`CMA` |

### 2.2 授权与机械手（4 项）

| 条件编译标记（`ReplaceMarker.md`） | 源码中文含义 | 保留条件（`generatepro.cpp`） | 作用目录 / 备注 |
| :--- | :--- | :--- | :--- |
| `ifIsHasEncryption` | 有循环加密 | `ifHasEncryption == 1`（启用后期加密） | `CMA`（校验序列号授权） |
| `ifIsNotHasEncryption` | 无循环加密 | `ifHasEncryption == 0`（无加密） | `CMA` |
| `ifIsHasLoadingArm` | 有机械手 | `ifHasLoadingArm == 1`（有机械手） | `MPF`、`CMA`、`HMI/proj` |
| `ifIsNotHasLoadingArm` | 无机械手 | `ifHasLoadingArm == 0`（无机械手） | `MPF`、`CMA`、`HMI/proj` |

### 2.3 机型与复合功能（9 项）

| 条件编译标记（`ReplaceMarker.md`） | 源码中文含义 | 保留条件（`generatepro.cpp`） | 作用目录 / 备注 |
| :--- | :--- | :--- | :--- |
| `ifIsExternal` | 外螺纹 | `machineType == 0`（外螺纹） | `CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp` |
| `ifIsHasWorm` | 有蜗杆 | `machineType == 0` 且 `wareType in {0,2}` 且 `ifHasWorm == 1` | `CMA`、`HMI/proj` |
| `ifIsNotHasWorm` | 没有蜗杆 | 除 `ifIsHasWorm` 成立外的所有配置（注意：`wareType!=0 && !=2` 或 `machineType==1` 时源码未删此反转块，主要与 `ifIsHasWorm` 成对在插补外磨下使用） | `CMA`、`HMI/proj` |
| `ifIsInternal` | 内螺纹 | `machineType == 1`（内螺纹） | `CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp` |
| `ifIsScrewTap` | 丝锥 | `machineType == 0` 且 `ifHasScrewTap == 0`（外螺纹丝锥） | `MPF`、`CMA`、`HMI/proj`、`HMI/hlp` |
| `ifIsNotScrewTap` | 不是丝锥 | `machineType == 1` 或 `ifHasScrewTap == 1`（非丝锥） | `MPF`、`CMA`、`HMI/proj`、`HMI/hlp` |
| `ifIsCenter` | 是磨削中心 | `machineType == 1` 且 `ifCenter == 0`（内螺纹磨削中心） | `CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp` |
| `ifIsNotCenter` | 不是磨削中心 | `machineType == 0` 或 `ifCenter == 1`（非磨削中心） | `CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp` |
| `ifIsInternalOnly` | 内螺纹非磨削中心 | `machineType == 1` 且 `ifCenter == 1`（纯内螺纹非磨削中心） | `HMI/proj`（`a_setting` 等） |

### 2.4 磨削中心 U 轴与外圆（4 项）

| 条件编译标记（`ReplaceMarker.md`） | 源码中文含义 | 保留条件（`generatepro.cpp`） | 作用目录 / 备注 |
| :--- | :--- | :--- | :--- |
| `ifIsHasU` | 磨削中心有U轴 | `machineType == 1` 且 `ifCenter == 0` 且 `ifHasU == 0`（有 U 轴） | `CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp` |
| `ifIsNotHasU` | 磨削中心无U轴 | `machineType == 1` 且 `ifCenter == 0` 且 `ifHasU == 1`；或 `machineType == 0`（注意 `ifCenter==1` 时源码亦会删除 `ifIsNotHasU` 中的 `proj/lng/hlp`） | `CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp` |
| `ifIsNotHasUBack` | 磨削中心无U轴-外圆砂轮在后 | 内螺纹磨削中心、`ifHasU == 1`（无 U 轴）且 `ifNotHasUExternalPos == 0`（外磨后置） | `CMA`、`HMI/proj`、`HMI/hlp` |
| `ifIsNotHasUFront` | 磨削中心无U轴-外圆砂轮在前 | 内螺纹磨削中心、`ifHasU == 1`（无 U 轴）且 `ifNotHasUExternalPos == 1`（外磨前置） | `CMA`、`HMI/proj`、`HMI/hlp` |

### 2.5 对刀与测量硬件（9 项）

| 条件编译标记（`ReplaceMarker.md`） | 源码中文含义 | 保留条件（`generatepro.cpp`） | 作用目录 / 备注 |
| :--- | :--- | :--- | :--- |
| `ifIsHasReOperate` | 有二次对刀 | `machineType == 0` 且 `ifHasReOp == 0`（外螺纹有二次对刀） | `HMI/proj`、`HMI/hlp` |
| `ifIsNotHasReOperate` | 无二次对刀 | `machineType == 1` 或 `ifHasReOp == 1`（无二次对刀） | `HMI/proj`、`HMI/hlp` |
| `ifIsAuto` | 有自动对刀 | `ifOperation == 0`（有自动对刀） | `CMA`、`HMI/proj`、`HMI/hlp` |
| `ifIsNotAuto` | 没有自动对刀 | `ifOperation == 1`（无自动对刀） | `CMA`、`HMI/proj`、`HMI/hlp` |
| `ifIsKaiGuanCeLiang` | 开关测量 | `ifOperation == 0` 且 `measureMethord == 0`（仅开关测量） | `CMA`、`HMI/proj`、`HMI/hlp` |
| `ifIsCeTouCeLiang` | 测头测量 | `ifOperation == 0` 且 `measureMethord == 1`（仅测头测量） | `CMA`、`HMI/proj`、`HMI/hlp` |
| `ifIsKaiGuanAndCeTouCeLiang` | 开关和测头 | `ifOperation == 0` 且 `measureMethord == 2`（开关和测头同时配置） | `CMA`、`HMI/proj`、`HMI/hlp` |
| `ifIsProbeFront` | 内螺纹测头前置 | `machineType == 1` 且 `ifOperation == 0` 且 `probePos == 0`（内螺纹自动对刀向前测量） | `a_setting.com` 专属初始赋值预设 |
| `ifIsNotProbeFront` | 内螺纹测头后置 | `machineType == 1` 且 `ifOperation == 0` 且 `probePos == 1`（内螺纹自动对刀向后测量） | `a_setting.com` 专属初始赋值预设 |

### 2.6 修整器构型组合（22 项）

| 条件编译标记（`ReplaceMarker.md`） | 源码中文含义 | 保留条件（`generatepro.cpp`） | 作用目录 / 备注 |
| :--- | :--- | :--- | :--- |
| `ifIsXW` | 是XW修整器 | `wareType == 5`（XW 修整器） | `MPF`、`CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp` |
| `ifIsNotXW` | 不是XW修整器 | `wareType != 5`（非 XW 修整器） | `MPF`、`CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp` |
| `ifIsUW` | 是UW修整器 | `wareType == 6`（UW 修整器，仅内螺纹） | `MPF`、`CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp` |
| `ifIsNotUW` | 不是UW修整器 | `wareType != 6`（非 UW 修整器） | `MPF`、`CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp` |
| `ifIsDressWare1` | VW/V | `wareType in {0, 2, 5, 6}`（VW、XZ、XW、UW 两轴插补系） | `HMI/proj`、`HMI/hlp` |
| `ifIsDressWare2` | V | `wareType == 1`（V 单轴成型） | `HMI/proj`、`HMI/hlp` |
| `ifIsDressWare3` | X_Z/X | `wareType == 2` 或 `wareType == 5`（XZ / XW） | `HMI/proj`、`HMI/hlp` |
| `ifIsDressWare4` | X_内后 | `wareType == 3`（X_Back 内后置成型） | `HMI/proj`、`HMI/hlp` |
| `ifIsDressWare5` | 液压 | `wareType == 4`（液压摆缸成型） | `HMI/proj`、`HMI/hlp` |
| `ifIsExternalVW` | 外螺纹VW修整器 | （`machineType == 0` 且 `wareType in {0, 1}`）或（`machineType == 1` 且 `wareType == 6`） | `CMA`、`HMI/hlp`（独立 V/W 或 U/W 轴控制段） |
| `ifIsFrontDress` | x向前修整 | `wareType != 3`（非 X_Back 后置修整的常规前向修整） | `CMA`、`HMI/proj`、`HMI/hlp` |
| `ifIsBackDress` | x向后修整 | `wareType == 3`（X_Back 后置修整） | `CMA`、`HMI/proj`、`HMI/hlp` |
| `ifIsVW` | vw修整器 | `wareType in {0, 2, 3, 4, 5, 6}`（即非纯 `V` 成型）；当 `wareType == 1` 时删除 | `CMA`、`HMI/proj`、`HMI/hlp` |
| `ifIsVWSR` | vw单方滚轮 | `wareType == 0` 且 `wheelType == 0`（VW 单/方滚轮） | `HMI/proj`、`HMI/hlp` |
| `ifIsVWSide` | vw双滚轮 | `wareType == 0` 且 `wheelType == 1`（VW 双滚轮） | `HMI/proj`、`HMI/hlp` |
| `ifIsV` | v修整器 | `wareType == 1`（V 单轴修整器） | `HMI/proj`、`HMI/hlp` |
| `ifIsXWai` | x外螺纹修整 | `machineType == 0` 且 `wareType in {2, 5}`（外螺纹 X 轴向修整） | `HMI/proj`、`HMI/hlp` |
| `ifIsXNeiFront` | x内螺纹向前 | `machineType == 1` 且 `wareType in {2, 5, 6}`（内螺纹前向修整） | `HMI/proj`、`HMI/hlp` |
| `ifIsXNeiBack` | x内螺纹向后 | `wareType == 3`（内螺纹 X_Back 向后修整） | `HMI/proj`、`HMI/hlp` |
| `ifIsVH` | 液压修整器 | `wareType == 4`（液压修整器） | `HMI/proj`、`HMI/hlp` |
| `ifIsXZSR` | xz单方滚轮 | `wareType in {2, 5, 6}` 且 `wheelType == 0`（XZ/XW/UW 单/方滚轮） | `HMI/proj`、`HMI/hlp` |
| `ifIsXZSide` | xz双滚轮 | `wareType in {2, 5, 6}` 且 `wheelType == 1`（XZ/XW/UW 双滚轮） | `HMI/proj`、`HMI/hlp` |

### 2.7 滚轮与齿形细分（6 项）

| 条件编译标记（`ReplaceMarker.md`） | 源码中文含义 | 保留条件（`generatepro.cpp`） | 作用目录 / 备注 |
| :--- | :--- | :--- | :--- |
| `ifIsSingleAndRound` | 单滚轮方滚轮 | `wareType in {0, 2, 5, 6}` 且 `wheelType == 0`（单/方滚轮） | `HMI/proj`、`HMI/hlp` |
| `ifIsSide` | 双滚轮 | `wareType in {0, 2, 5, 6}` 且 `wheelType == 1`（双滚轮） | `HMI/proj`、`HMI/hlp` |
| `ifIsAllShape` | 全套齿形 | `wareType in {0, 2, 5, 6}` 且 `shapeType == 0`（全套齿形） | `HMI/proj`、`HMI/hlp` |
| `ifIsArc` | 有双圆弧 | `wareType in {0, 2, 5, 6}` 且 `shapeType in {0, 1}`（含双圆弧） | `HMI/proj`、`HMI/hlp` |
| `ifIsOnlyArc` | 只有双圆弧 | `wareType in {0, 2, 5, 6}` 且 `shapeType == 1`（仅双圆弧） | `HMI/proj`、`HMI/hlp` |
| `ifIsHasOtherCommonShape` | 有其他通用齿形 | `wareType in {0, 2, 5, 6}` 且 `shapeType == 0`（含通用扩展齿形） | `HMI/proj`、`HMI/hlp` |

### 2.8 A 轴与电主轴驱动（8 项）

| 条件编译标记（`ReplaceMarker.md`） | 源码中文含义 | 保留条件（`generatepro.cpp`） | 作用目录 / 备注 |
| :--- | :--- | :--- | :--- |
| `ifIsHasA` | 有A轴 | `ifHasA == 0`（有机床 A 轴） | `a_setting.com`（可见开关与预设） |
| `ifIsNotHasA` | 没有A轴 | `ifHasA == 1`（无机床 A 轴） | `a_setting.com`（隐藏清零预设） |
| `ifIsSiFuInGrindWheel` | 砂轮电机是伺服 | `grindWheelType == 1`（**注意**：源码内 `0=伺服 / 1=变频`，此处实控写入 `INI[36]=0` 模拟量/变频分支） | `a_setting.com` `SUB(UP6)` |
| `ifIsNotSiFuInGrindWheel` | 砂轮电机是变频 | `grindWheelType == 0`（写入 `INI[36]=1` 西门子伺服分支） | `a_setting.com` `SUB(UP6)` |
| `ifIsSiFuInExGrindWheel` | 外磨电机是伺服 | `machineType == 1 && ifCenter == 0 && exGrindWheelType == 1`（写入 `INI[91]=0` 模拟量/变频分支） | `a_setting.com` `SUB(UP6)` |
| `ifIsNotSiFuInExGrindWheel` | 外磨电机是变频 | `machineType == 1 && ifCenter == 0 && exGrindWheelType == 0`（写入 `INI[91]=1` 西门子伺服分支） | `a_setting.com` `SUB(UP6)` |
| `ifIsSiFuInDressWheel` | 修整电机是伺服 | `dressWheelType == 1`（写入 `INI[37]=0` 模拟量/变频分支） | `a_setting.com` `SUB(UP6)` |
| `ifIsNotSiFuInDressWheel` | 修整电机是变频 | `dressWheelType == 0`（写入 `INI[37]=1` 西门子伺服分支） | `a_setting.com` `SUB(UP6)` |

## 3. 项目元数据占位符与自动文本替换规则（12 项）

| 源码标记 / 匹配目标 | 替换行为 | 替换内容 / 触发条件 | 作用目标文件 |
| :--- | :--- | :--- | :--- |
| `machineName` | 替换字符串 | 规范化后的机床型号（大写、`×`/`*` → `x`、`_` 还原 `/`） | `INFO_INIT.MPF`、`HMI/lng/*`、`hlp/**/index.html` |
| `machineCHS` | 替换字符串 | `machineNameLng` 设备中文/多语言描述名 | `INFO_INIT.MPF`、`HMI/lng/*`、`hlp/**/index.html` |
| `machineIndex` | 替换字符串 | `machineIndex` 设备出厂编号 | `INFO_INIT.MPF`、`HMI/proj/*.com`（含 `a_setting.com` `INI[130]`） |
| `customInfo` | 替换字符串 | `customInfo` 客户简称/项目代号 | `INFO_INIT.MPF` |
| `debugDate` | 替换字符串 | 程序包生成的系统时间戳 | `INFO_INIT.MPF` |
| `softwareVersion` | 替换字符串 | `HorizonJuicerCreator` 当前版本号（如 `V3.29.0`） | `INFO_INIT.MPF`、`hlp/**/index.html` |
| `specificationInfo` | 替换字符串 | 配置规格编码数字串（由 `machineType`..`ifHasNoneTradeMark` 依次拼接） | `INFO_INIT.MPF` |
| `passwordSource` | 替换字符串 | 6 位随机模板占位符（由 `a_setting.com` 动态口令机制接管） | `a_setting.com`（旧版占位兼容） |
| `chs.png` | 替换为 `eng.png` | 当 `lng == 1` 多语言模式时自动替换图标文件名引用 | `HMI/proj/*.com`、`HMI/cfg/*.ini` |
| `["\\图标.png",` / `],ac` | 兼容剥离 | 当 `hmiMode == 1`（兼容模式）时剥离图标引用与 `,ac` 修饰符 | `HMI/proj/*.com` |
| `;...` 行末/单行注释 | 正则删除为 `;` | 当 `ifRemoveComments == 0` 时保留 `;*` 与 `;"`、删除普通注释 | `.com` / `.spf` / `.mpf` |
| 文件名 `INFO_INIT.MPF` | 重命名主程序 | 重命名为 `<规范化 machineName>.MPF`（`×`/`*` → `x`、`/` → `_`） | `NC-Data/MPF/` |

## 4. Sinumerik ONE 跨平台信号替换全表（`oneReplace.json`，共 47 项）

当 `HorizonJuicerCreator` 选择 **数控系统 = `2 Sinumerik ONE`** 时，系统自动遍历 `MPF`、`CMA`、`HMI/proj` 与 `System-CF-Card/user`，执行下列 47 项精准文本替换（`CF 卡序列号` 模板测试项已做脱敏处理）：

| 类别 | 原 828D / 840D sl 符号 | 替换为 Sinumerik ONE 符号 | 说明 |
| :--- | :--- | :--- | :--- |
| NC 快速交换位 | <code>&#36;A_DBB[0]</code> | <code>&#36;A_IN[12]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[1]</code> | <code>&#36;A_IN[13]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[2]</code> | <code>&#36;A_IN[14]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[3]</code> | <code>&#36;A_IN[16]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[4]</code> | <code>&#36;A_IN[17]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[5]</code> | <code>&#36;A_IN[9]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[6]</code> | <code>&#36;A_IN[18]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[7]</code> | <code>&#36;A_IN[19]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[8]</code> | <code>&#36;A_IN[20]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[9]</code> | <code>&#36;A_IN[21]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[10]</code> | <code>&#36;A_IN[22]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[12]</code> | <code>&#36;A_IN[30]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[13]</code> | <code>&#36;A_IN[31]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[14]</code> | <code>&#36;A_IN[25]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[16]</code> | <code>&#36;A_IN[32]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[17]</code> | <code>&#36;A_IN[8]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[20]</code> | <code>&#36;A_IN[23]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[21]</code> | <code>&#36;A_IN[24]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[24]</code> | <code>&#36;A_IN[26]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[25]</code> | <code>&#36;A_IN[29]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[40]</code> | <code>&#36;A_IN[6]</code> | 映射 ONE 高速输入通道 |
| NC 快速交换位 | <code>&#36;A_DBB[41]</code> | <code>&#36;A_IN[7]</code> | 映射 ONE 高速输入通道 |
| HMI XML / 状态变量 | `aDbb[0]` | `digitInpVal[12]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[1]` | `digitInpVal[13]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[2]` | `digitInpVal[14]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[3]` | `digitInpVal[16]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[4]` | `digitInpVal[17]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[5]` | `digitInpVal[9]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[6]` | `digitInpVal[18]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[7]` | `digitInpVal[19]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[8]` | `digitInpVal[20]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[9]` | `digitInpVal[21]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[10]` | `digitInpVal[22]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[12]` | `digitInpVal[30]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[13]` | `digitInpVal[31]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[14]` | `digitInpVal[25]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[16]` | `digitInpVal[32]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[17]` | `digitInpVal[8]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[20]` | `digitInpVal[23]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[21]` | `digitInpVal[24]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[24]` | `digitInpVal[26]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[25]` | `digitInpVal[29]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[40]` | `digitInpVal[6]` | 映射 `digitInpVal` 数组 |
| HMI XML / 状态变量 | `aDbb[41]` | `digitInpVal[7]` | 映射 `digitInpVal` 数组 |
| CF 卡硬件序列号模板 | `<828D 测试 CF 卡序列号（已脱敏）>` | `<ONE 测试 CF 卡序列号（已脱敏）>` | 仅用于出厂模板匹配替换 |
| 测头接口 PLC 地址 | `DB2700.DBX1.0` | `DB10.DBX107.0` | ONE 测头实时状态位 |
| 测头接口 PLC 地址 | `DB2700.DBX1.1` | `DB10.DBX107.1` | ONE 测头实时状态位 |
