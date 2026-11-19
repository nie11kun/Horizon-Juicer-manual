# 2.3 生成目录结构与规格编码解析

每次在 `HorizonJuicerCreator` 成功运行 **程序生成** 后，软件都会在指定的 **程序生成目录** 下创建一个按标准规范命名的设备交付根文件夹：

```text
<destDir>/<machineName>(#<machineIndex>-<customInfo>)/
```

例如：`SK7420(#01-DemoPlant)` 或 `SKR7620B(#02-DemoCenter)`。

## 1. 标准输出目录树（老版 828D / Sinumerik ONE 与新版 828D 对比）

以下为标准交付包内部的完整文件与目录规划：

```text
SKR7620B(#02-DemoCenter)/
├── M-sympol_Index.md            # M 代码与机械手交互信号参考清单（随包附带便于现场查表）
├── Parameter_Index.md           # MGUD 全局变量与 R 参数详细索引表
├── NC-Data/                     # 需导入数控系统 NC 侧的程序与变量定义文件
│   ├── DEF/
│   │   └── MGUD.DEF             # 全局变量定义文件（需先激活生效）
│   ├── MPF/
│   │   └── SKR7620B.MPF         # 由 INFO_INIT.MPF 自动重命名而来的设备初始化主程序
│   └── CMA/                     # 裁剪后的有效子程序集（*.SPF）
│       ├── A_GRINDING.SPF       # 线程磨削总入口
│       ├── A_GRIND_CENTER.SPF   # 磨削中心总入口（仅磨削中心保留）
│       ├── B_SCREW.SPF          # 螺纹磨削主流程
│       ├── B_DRESS.SPF          # 砂轮修整主流程
│       ├── B_OPERATION.SPF      # 对刀主流程
│       └── ...                  # 仅包含当前勾选结构所需的全部 C_/D_/E_/F_/... 子程序
└── System-CF-Card/              # 需覆盖导入机床 CF 卡 / SinuTrain hmi 目录的文件
    ├── oem/                     # 新版 828D / Sinumerik ONE 的主要载体，含 extdev.ini、slhlp 等
    ├── siemens/                 # 老版 828D / 840D sl（SinuTrain）核心界面运行目录（新版 828D 无此目录）
    │   └── sinumerik/
    │       ├── hmi/
    │       │   ├── cfg/         # custom.ini、easyscreen.ini、slamconfig.ini、machine_sec.ini 等
    │       │   ├── hlp/         # chs/eng 嵌入式帮助网页与 pic1..pic76 图包
    │       │   ├── ico/         # 按系统类型精选的 ico800 / ico1024 图标资源
    │       │   ├── lng/         # almc_chs.txt / almc_eng.txt / almc_rus.txt 多语言文本库
    │       │   └── proj/        # 经条件编译与兼容处理后的 *.com 界面文件
    └── user/                    # 用户级覆盖与个性化配置目录
```

> **提示**：细心的工程师会发现，**`828D 新版` 生成包的 `System-CF-Card/` 下只有 `oem/` 与 `user/`，而不包含 `siemens/`**；而 **`828D 老版` 则包含 `oem/`、`siemens/`、`user/` 三个子目录**。这是 `HorizonJuicerCreator` 依据目标系统授权与目录优先级的精确设计，部署时只需将 `System-CF-Card` 下的全部子目录整体并入目标机对应根目录即可。

## 2. 规格编码字符串（specificationInfo）变长拼接规则

在 `generatepro.cpp` 构建过程中，软件会按界面当前显示分支动态拼接一条 **变长位置数字串 `specificationInfo`**（仅包含当前机型有效选项，并非定长字符串！），并打印在内部生成日志及配置文件追溯记录中。拼接顺序严格如下：

1. **固定首位**：`machineType`（`0` 外螺纹 / `1` 内螺纹）
2. **外螺纹前缀（仅 `machineType=0`）**：`ifHasScrewTap`（`0` 是 / `1` 否）
3. **修整器架构**：`wareType`（`0=VW, 1=V, 2=XZ, 3=X_Back, 4=液压, 5=XW, 6=UW`）
4. **蜗杆与滚轮/齿形插补分支**：
   - 若 `machineType=0` 且 `wareType` 属于 `0/2/5/6`：追加 `ifHasWorm`（`0/1`）；
   - 若 `wareType` 属于插补型（`0/2/5/6`）：依次追加 `wheelType`（`0/1`）+ `shapeType`（`0/1`）；
5. **二次对刀与自动对刀分支**：
   - 若 `machineType=0`：追加 `ifHasReOp`（`0/1`）；
   - 追加 `ifOperation`（`0` 有 / `1` 无）；
   - 仅当 `ifOperation=0`（有自动对刀）时：追加 `measureMethord`（`0/1/2`），若同时 `machineType=1`（内螺纹）则再追加 `probePos`（`0=向前 / 1=向后`）；
6. **磨削中心与 U 轴分支（仅 `machineType=1`）**：
   - 追加 `ifCenter`（`0` 是 / `1` 不是）；
   - 仅当 `ifCenter=0` 时：追加 `ifHasU`（`0` 有 / `1` 无）；若 `ifHasU=1`（无 U 轴）再追加 `ifNotHasUExternalPos`（`0=后置 / 1=前置`）；
7. **辅助轴、驱动与尾部选项（所有机型固定追加）**：
   - `ifHasA` + `grindWheelType` + `[若 内螺纹且磨削中心(1+0) 则插入 exGrindWheelType]` + `dressWheelType` + `ifRemoveComments` + `ifHasLoadingArm` + `ifHasEncryption` + `ifHasNoneTradeMark`。

> **编码解码示例**：对照 `2.2` 示例图（`SKR7620B` 内螺纹磨削中心：内螺纹 `1` + XZ `2` + 单/方滚轮 `0` + 全套齿形 `0` + 有对刀 `0` + 测头 `1` + 向前 `0` + 磨削中心 `0` + 有U轴 `0` + 有A轴 `0` + 三伺服 `000` + 不删注释 `1` + 无机械手 `0` + 不加密 `0` + 保留商标 `0`），生成的 `specificationInfo` 即为 **`12000100000001000`**。

## 3. 交付前自检清单

在将生成的程序包拷贝前往调试现场之前，建议按以下 4 步快速复核：

1. 检查 `NC-Data/MPF/` 下主初始化文件是否已成功命名为 `<机床型号>.MPF`（且文件名不含特殊非法字符）；
2. 用文本编辑器打开 `NC-Data/MPF/<机床型号>.MPF`，预先根据机床丝杠行程、电机特性调整轴快速/慢速及主轴等待延时默认值（如 `INI[54]`～`INI[71]`）；
3. 核对 `NC-Data/CMA/` 下是否包含当前配置应有的关键入口（例如勾选了 **磨削中心** 则必有 `A_GRIND_CENTER.SPF`、`H_GRINDING.SPF`、`L_GRINDING.SPF`、`Q_GRINDING.SPF`）；
4. 若客户机床使用了 `Sinumerik ONE`，抽查一个 `NC-Data/CMA/` 子程序确认 <code>&#36;A_DBB[...]</code> 是否已正确按 `oneReplace.json` 转换为 <code>&#36;A_IN[...]</code> 等目标语句；
5. 导入实机后务必在 `CUSTOM → 扩展菜单 → 机床配置` 解锁后执行一次 **`VS3 → Mask2` 配置重置**（详见 [4.1 节](../4_deployment_and_sinutrain/real_machine_deploy.md)）。
