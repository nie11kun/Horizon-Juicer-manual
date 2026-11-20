# 10.4 全量全局变量与 R 参数索引表

本节汇集 `MGUD.DEF` 全部 60 条自定义全局变量声明、`Parameter_Index.md` 全部 30 个分类共 1,553 条变量明细（对应 `Parameter_Index.md` 全部 1,561 个非空表格行中的 8 个子分组标题与 1,553 个独立条目），以及 `Parameter_Index.md` 未展开的 22 项系统/备份统计变量。

> **0-based（NC）与 1-based（HMI ACX）下标偏移铁律**：<br>• `.SPF` / `.MPF` 子程序、`MGUD.DEF` 与 `Parameter_Index.md` 使用 **0-based** 下标（例如 `DRESSER[0]`、`INI[36]`）；<br>• EasyScreen `.com` 界面脚本（`/NC/_N_NC_GD2_ACX/...`）使用 **1-based** 下标（**HMI 下标 = NC 下标 + 1**，例如 `DRESSER[1]`、`INI[37]`）；<br>• `MGUD.DEF` 自定义变量名超过 60 个，激活前必须确保通用机床数据 **`MD18120 >= 70`**。若将早期 `TECHNOLOGY[420]` 控制器升级至 `TECHNOLOGY[500]` 新版 `MGUD.DEF`，激活前务必先备份原 GUD 数据，激活后执行 `VS3 重置数据` 并恢复业务参数。

### 快速分类导航目录

- [1. `MGUD.DEF` 全局变量声明总表（60 项）](#mgud-def-list)
- **2. `Parameter_Index.md` 全量明细（30 类 / 1,553 项）**：[PLC_NC交换变量（33 项）](#pi-sec-1) · [与桁架机器人交互相关的信号（13 项）](#pi-sec-2) · [快速输入输出信号（8 项）](#pi-sec-3) · [自动测量信号（6 项）](#pi-sec-4) · [修整主参数(DRESSER)（146 项）](#pi-sec-5) · [初始化参数(INI)（163 项）](#pi-sec-6) · [对刀(TOOL_SET)（70 项）](#pi-sec-7) · [滚轮参数(WHEEL)（20 项）](#pi-sec-8) · [磨削参数(GRIND)（10 项）](#pi-sec-9) · [工序基本参数（130 项）](#pi-sec-10) · [工艺表格参数（432 项）](#pi-sec-11) · [DIY参数（14 项）](#pi-sec-12) · [工件头数参数（8 项）](#pi-sec-13) · [当前磨削次数参数（10 项）](#pi-sec-14) · [修整进给量参数（29 项）](#pi-sec-15) · [修整速度参数（29 项）](#pi-sec-16) · [修整轮线速度参数（35 项）](#pi-sec-17) · [磨削修整次数参数（29 项）](#pi-sec-18) · [R参数使用情况（7 项）](#pi-sec-19) · [内螺纹反相孔倒角参数（28 项）](#pi-sec-20) · [内螺纹夹具自磨R参数版程序参数（22 项）](#pi-sec-21) · [蜗杆用R参数（23 项）](#pi-sec-22) · [通用齿形模型变量（78 项）](#pi-sec-23) · [SHAPE MODEL（136 项）](#pi-sec-24) · [RING GROOVE（31 项）](#pi-sec-25) · [SCREW TAP（19 项）](#pi-sec-26) · [SERVICE_LIFE（15 项）](#pi-sec-27) · [SERVICE_LIFE_TXT（7 项）](#pi-sec-28) · [DRESS_WHEEL_NUM（1 项）](#pi-sec-29) · [DRESS_WHEEL_DATE（1 项）](#pi-sec-30)
- [3. `MGUD.DEF` 补充系统与备份变量表（22 项）](#mgud-extra-vars)

<a id="mgud-def-list"></a>

## 1. `MGUD.DEF` 全局变量声明全量清单（60 项）

| 变量 / 数组声明 | 数据类型 | 存储与下标基准 | 用途说明 |
| :--- | :--- | :--- | :--- |
| `AXIS_VER` | `STRING[1]` | 标量（无下标） | 垂直轴 |
| `AXIS_HORI` | `STRING[1]` | 标量（无下标） | 水平轴 |
| `AXIS_EW` | `STRING[1]` | 标量（无下标） | 磨削中心外圆砂轮切入轴名（有 U 轴时为 `U`，共用轴时为 `X`） |
| `SHAPE` | `STRING[20]` | 标量（无下标） | 齿形程序名称 |
| `WORM_SHAPE` | `STRING[20]` | 标量（无下标） | 蜗杆专用齿形子程序名称 |
| `WHICH_COMMON_SHAPE` | `STRING[20]` | 标量（无下标） | 通用齿形程序名称 |
| `SHAPE_EXTERNAL` | `STRING[20]` | 标量（无下标） | 外部齿形程序名称 |
| `DRESSER[240]` | `REAL` | NC `DRESSER[0]`～`DRESSER[239]`<br>HMI `DRESSER[1]`～`DRESSER[240]` | 修整主参数(DRESSER) |
| `INI[260]` | `REAL` | NC `INI[0]`～`INI[259]`<br>HMI `INI[1]`～`INI[260]` | 初始化参数(INI) |
| `TOOL_SET[150]` | `REAL` | NC `TOOL_SET[0]`～`TOOL_SET[149]`<br>HMI `TOOL_SET[1]`～`TOOL_SET[150]` | 对刀(TOOL_SET) |
| `WHEEL[30]` | `REAL` | NC `WHEEL[0]`～`WHEEL[29]`<br>HMI `WHEEL[1]`～`WHEEL[30]` | 滚轮参数(WHEEL) |
| `TRI[20]` | `REAL` | NC `TRI[0]`～`TRI[19]`<br>HMI `TRI[1]`～`TRI[20]` | 三角齿形(TRI) |
| `TRAP[20]` | `REAL` | NC `TRAP[0]`～`TRAP[19]`<br>HMI `TRAP[1]`～`TRAP[20]` | 梯形(TRAP) |
| `DARC[30]` | `REAL` | NC `DARC[0]`～`DARC[29]`<br>HMI `DARC[1]`～`DARC[30]` | 双圆弧(DARC) |
| `GRIND[10]` | `REAL` | NC `GRIND[0]`～`GRIND[9]`<br>HMI `GRIND[1]`～`GRIND[10]` | 磨削参数(GRIND) |
| `PROCESS[130]` | `REAL` | NC `PROCESS[0]`～`PROCESS[129]`<br>HMI `PROCESS[1]`～`PROCESS[130]` | 工序基本参数 |
| `TECHNOLOGY[500]` | `REAL` | NC `TECHNOLOGY[0]`～`TECHNOLOGY[499]`<br>HMI `TECHNOLOGY[1]`～`TECHNOLOGY[500]` | 工艺表格参数 |
| `DIY[10]` | `REAL` | NC `DIY[0]`～`DIY[9]`<br>HMI `DIY[1]`～`DIY[10]` | DIY参数 |
| `WORK[10]` | `REAL` | NC `WORK[0]`～`WORK[9]`<br>HMI `WORK[1]`～`WORK[10]` | 工件头数参数 |
| `TECH_TIME[10]` | `INT` | NC `TECH_TIME[0]`～`TECH_TIME[9]`<br>HMI `TECH_TIME[1]`～`TECH_TIME[10]` | 当前磨削次数参数 |
| `TECH_DRESS_DEEP[80]` | `REAL` | NC `TECH_DRESS_DEEP[0]`～`TECH_DRESS_DEEP[79]`<br>HMI `TECH_DRESS_DEEP[1]`～`TECH_DRESS_DEEP[80]` | 修整进给量参数 |
| `TECH_DRESS_FEED[80]` | `REAL` | NC `TECH_DRESS_FEED[0]`～`TECH_DRESS_FEED[79]`<br>HMI `TECH_DRESS_FEED[1]`～`TECH_DRESS_FEED[80]` | 修整速度参数 |
| `WHEEL_LINESPEED_DRESS[80]` | `REAL` | NC `WHEEL_LINESPEED_DRESS[0]`～`WHEEL_LINESPEED_DRESS[79]`<br>HMI `WHEEL_LINESPEED_DRESS[1]`～`WHEEL_LINESPEED_DRESS[80]` | 修整轮线速度参数 |
| `TECH_DRESS_TIME[80]` | `INT` | NC `TECH_DRESS_TIME[0]`～`TECH_DRESS_TIME[79]`<br>HMI `TECH_DRESS_TIME[1]`～`TECH_DRESS_TIME[80]` | 磨削修整次数参数 |
| `PARA_LOCK_SWITCH[30]` | `INT` | NC `PARA_LOCK_SWITCH[0]`～`PARA_LOCK_SWITCH[29]`<br>HMI `PARA_LOCK_SWITCH[1]`～`PARA_LOCK_SWITCH[30]` | 界面参数锁定开关状态预留数组 |
| `COMMON_VER_TOP` | `REAL` | 标量（无下标） | 通用齿形模型变量 |
| `COMMON_VER_BOTTOM` | `REAL` | 标量（无下标） | 通用齿形模型变量 |
| `COMMON_VER_HEIGHT` | `REAL` | 标量（无下标） | 通用齿形模型变量 |
| `COMMON_MACHINE_STATUS` | `REAL` | 标量（无下标） | 通用齿形模型变量 |
| `COMMON_ANG_MODIFY` | `REAL` | 标量（无下标） | 通用齿形模型变量 |
| `COMMON_LENGTH[20]` | `REAL` | NC `COMMON_LENGTH[1]`～`COMMON_LENGTH[20]`<br>HMI `COMMON_LENGTH[1]`～`COMMON_LENGTH[20]` | 通用齿形模型变量 |
| `COMMON_ANG[20]` | `REAL` | NC `COMMON_ANG[1]`～`COMMON_ANG[20]`<br>HMI `COMMON_ANG[1]`～`COMMON_ANG[20]` | 通用齿形模型变量 |
| `COMMON_RND[20]` | `REAL` | NC `COMMON_RND[1]`～`COMMON_RND[20]`<br>HMI `COMMON_RND[1]`～`COMMON_RND[20]` | 通用齿形模型变量 |
| `COMMON_STATUS_CACU[20]` | `REAL` | NC `COMMON_STATUS_CACU[0]`～`COMMON_STATUS_CACU[10]`<br>HMI `COMMON_STATUS_CACU[1]`～`COMMON_STATUS_CACU[11]` | 通用齿形模型变量 |
| `COMMON_LENGTH_ADD[20]` | `REAL` | NC `COMMON_LENGTH_ADD[0]`～`COMMON_LENGTH_ADD[10]`<br>HMI `COMMON_LENGTH_ADD[1]`～`COMMON_LENGTH_ADD[11]` | 通用齿形模型变量 |
| `COMMON_POINT_REF_VER[20]` | `REAL` | NC `COMMON_POINT_REF_VER[1]`～`COMMON_POINT_REF_VER[20]`<br>HMI `COMMON_POINT_REF_VER[1]`～`COMMON_POINT_REF_VER[20]` | 通用齿形模型变量 |
| `COMMON_POINT_REF_HORI[20]` | `REAL` | NC `COMMON_POINT_REF_HORI[1]`～`COMMON_POINT_REF_HORI[20]`<br>HMI `COMMON_POINT_REF_HORI[1]`～`COMMON_POINT_REF_HORI[20]` | 通用齿形模型变量 |
| `SHAPE_MODEL[140]` | `REAL` | NC `SHAPE_MODEL[0]`～`SHAPE_MODEL[139]`<br>HMI `SHAPE_MODEL[1]`～`SHAPE_MODEL[140]` | 通用齿形参数 |
| `RING[50]` | `REAL` | NC `RING[0]`～`RING[49]`<br>HMI `RING[1]`～`RING[50]` | 环形槽程序参数 |
| `SCREW_TAP[20]` | `REAL` | NC `SCREW_TAP[0]`～`SCREW_TAP[19]`<br>HMI `SCREW_TAP[1]`～`SCREW_TAP[20]` | 丝锥程序参数 |
| `CHOICE` | `REAL` | 标量（无下标） | 参数备份恢复运行模式（`0` 加工 / `1` 备份 / `2` 恢复） |
| `BACKUP_TYPE` | `REAL` | 标量（无下标） | 备份模式（`0` 备份全部 MGUD 变量 / `1` 按自定义列表备份） |
| `BACKUP_POS` | `REAL` | 标量（无下标） | 备份目标存储位置（`0` 内置 / `1` 后 USB / `2` 前 USB / `3` CF 卡） |
| `RESTORE_POS` | `REAL` | 标量（无下标） | 恢复源存储位置（`0` 内置 / `1` 后 USB / `2` 前 USB / `3` CF 卡） |
| `FILE_LINE_COUNT` | `REAL` | 标量（无下标） | 自定义参数列表文件的总行数（含空行与分号注释行） |
| `LIST_NAME` | `STRING[30]` | 标量（无下标） | 备份参数列表文件名称 |
| `LIST_DIR` | `STRING[30]` | 标量（无下标） | 备份参数列表文件所在文件夹路径-指定为 SPF 目录内的文件夹 |
| `BACKUP_NAME` | `STRING[30]` | 标量（无下标） | 备份文件名称 |
| `BACKUP_DIR` | `STRING[30]` | 标量（无下标） | 备份文件夹名称 |
| `RESTORE_NAME` | `STRING[30]` | 标量（无下标） | 恢复文件名称 |
| `RESTORE_DIR` | `STRING[30]` | 标量（无下标） | 恢复文件夹名称 |
| `BR_MSG` | `STRING[150]` | 标量（无下标） | 备份/恢复执行状态与多语言提示消息 |
| `CUR_WHEEL` | `INT` | 标量（无下标） | 当前砂轮更换记录序号（`1～99` 索引 `WHEEL_GRIND_CUMU` 与 `WHEEL_CHANGED_DATA`） |
| `WHEEL_GRIND_CUMU[100]` | `INT` | NC `WHEEL_GRIND_CUMU[0]`～`WHEEL_GRIND_CUMU[99]`<br>HMI `WHEEL_GRIND_CUMU[1]`～`WHEEL_GRIND_CUMU[100]` | 99 组更换砂轮周期对应的工件加工产量累计数组 |
| `WHEEL_CHANGED_DATA[100]` | `STRING[30]` | NC `WHEEL_CHANGED_DATA[0]`～`WHEEL_CHANGED_DATA[99]`<br>HMI `WHEEL_CHANGED_DATA[1]`～`WHEEL_CHANGED_DATA[100]` | 99 组更换砂轮操作的时间戳记录数组 |
| `STRING_ADDON[10]` | `STRING[30]` | NC `STRING_ADDON[0]`～`STRING_ADDON[9]`<br>HMI `STRING_ADDON[1]`～`STRING_ADDON[10]` | 备用字符串数组 |
| `SERVICE_LIFE[50]` | `REAL` | NC `SERVICE_LIFE[0]`～`SERVICE_LIFE[49]`<br>HMI `SERVICE_LIFE[1]`～`SERVICE_LIFE[50]` | 其他配件使用寿命 |
| `SERVICE_LIFE_TXT[50]` | `STRING[100]` | NC `SERVICE_LIFE_TXT[0]`～`SERVICE_LIFE_TXT[49]`<br>HMI `SERVICE_LIFE_TXT[1]`～`SERVICE_LIFE_TXT[50]` | 其他配件使用寿命 |
| `DRESS_WHEEL_NUM[100]` | `STRING[30]` | NC `DRESS_WHEEL_NUM[0]`～`DRESS_WHEEL_NUM[99]`<br>HMI `DRESS_WHEEL_NUM[1]`～`DRESS_WHEEL_NUM[100]` | 100 组金刚石滚轮编号档案数组 |
| `DRESS_WHEEL_DATE[100]` | `STRING[30]` | NC `DRESS_WHEEL_DATE[0]`～`DRESS_WHEEL_DATE[99]`<br>HMI `DRESS_WHEEL_DATE[1]`～`DRESS_WHEEL_DATE[100]` | 100 组金刚石滚轮上线启用日期档案数组 |

## 2. `Parameter_Index.md` 全量变量明细表（30 类 / 1,553 项）

<a id="pi-sec-1"></a>

### 2.1 PLC_NC交换变量（33 项）

| NC 信号变量 | PLC 地址 / 通道映射 | 含义与备注 |
| :--- | :--- | :--- |
| <code>&#36;A_DBB[0]</code> | `DB4900.DBX0.0` | 是否修整 <code>&#36;A_IN[11]</code>-840Dsl |
| <code>&#36;A_DBB[1]</code> | `DB4900.DBX1.0` | 是否手动对刀 |
| <code>&#36;A_DBB[2]</code> | `DB4900.DBX2.0` | 是否退刀，异步动作信号 |
| <code>&#36;A_DBB[3]</code> | `DB4900.DBX3.0` | 液压动作回退到位 |
| <code>&#36;A_DBB[4]</code> | `DB4900.DBX4.0` | 液压动作伸出到位 |
| <code>&#36;A_DBB[5]</code> | `DB4900.DBX5.0` | 是否自动对刀 |
| <code>&#36;A_DBB[6]</code> | `DB4900.DBX6.0` | C轴旋转 |
| <code>&#36;A_DBB[7]</code> | `DB4900.DBX7.0` | 自动对刀测量机构1汽缸回退到位 |
| <code>&#36;A_DBB[8]</code> | `DB4900.DBX8.0` | 自动对刀测量机构1汽缸伸出到位 |
| <code>&#36;A_DBB[9]</code> | `DB4900.DBX9.0` | 自动门1打开开关 |
| <code>&#36;A_DBB[10]</code> | `DB4900.DBX10.0` | 自动门1关闭开关 |
| <code>&#36;A_DBB[11]</code> | `DB4900.DBX11.0` | 360功能生效 |
| <code>&#36;A_DBB[12]</code> | `DB4900.DBX12.0` | 砂轮当前状态(0停止/1启动) |
| <code>&#36;A_DBB[13]</code> | `DB4900.DBX13.0` | 修整轮当前状态(0停止/1启动) |
| <code>&#36;A_DBB[14]</code> | `DB4900.DBX14.0` | A轴夹紧动作检测信号(0未松开/1已松开) |
| <code>&#36;A_DBB[15]</code> | `DB4900.DBX15.0` | 浮子开关信号 【主轴冷却单元】 |
| <code>&#36;A_DBB[16]</code> | `DB4900.DBX16.0` | 外圆砂轮当前状态(0停止/1启动) |
| <code>&#36;A_DBB[17]</code> | `DB4900.DBX17.0` | 液压卡盘夹紧到位时为1，未到位为0 |
| <code>&#36;A_DBB[18]</code> | `DB4900.DBX18.0` | 液压卡盘松开到位时为1，未到位为0 |
| <code>&#36;A_DBB[19]</code> | `DB4900.DBX19.0` | zc插补期间x退刀，同步动作信号 |
| <code>&#36;A_DBB[20]</code> | `DB4900.DBX20.0` | 自动对刀测量机构2汽缸回退到位 |
| <code>&#36;A_DBB[21]</code> | `DB4900.DBX21.0` | 自动对刀测量机构2汽缸伸出到位 |
| <code>&#36;A_DBB[22]</code> | `DB4900.DBX22.0` | 罩壳门2打开开关 |
| <code>&#36;A_DBB[23]</code> | `DB4900.DBX23.0` | 罩壳门2关闭开关 |
| <code>&#36;A_DBB[24]</code> | `DB4900.DBX24.0` | 主轴电机故障标记 |
| <code>&#36;A_DBB[25]</code> | `DB4900.DBX25.0` | 断电回退信号 |
| <code>&#36;A_DBB[26]</code> | `DB4900.DBX26.0` | 液压外圆修整器回退到位 |
| <code>&#36;A_DBB[27]</code> | `DB4900.DBX27.0` | 液压外圆修整器伸出到位 |
| <code>&#36;A_DBB[28]</code> | `DB4900.DBX28.0` | 自动尾架顶紧到位为1 |
| <code>&#36;A_DBB[29]</code> | `DB4900.DBX29.0` | 自动尾架松开到位为1 |
| <code>&#36;A_DBB[80]</code> | `DB4900.DBX80.0` | 侧门是否关闭到位(磨削中心) |
| <code>&#36;A_DBB[40]</code> | `DB4900.DBX40.0` | 力矩电机测试信号-夹紧 |
| <code>&#36;A_DBB[41]</code> | `DB4900.DBX41.0` | 力矩电机测试信号-松开 |

<a id="pi-sec-2"></a>

### 2.2 与桁架机器人交互相关的信号（13 项）

| NC 信号变量 | PLC 地址 / 通道映射 | 含义与备注 |
| :--- | :--- | :--- |
| <code>&#36;A_DBB[30]</code> | `DB4900.DBX30.0` | 机器人发给系统,请求尾驾松开信号 |
| <code>&#36;A_DBB[31]</code> | `DB4900.DBX31.0` | 机器人发给系统,请求尾驾夹紧信号 |
| <code>&#36;A_DBB[32]</code> | `DB4900.DBX32.0` | 机器人发给系统,机械手服务中信号 |
| <code>&#36;A_DBB[33]</code> | `DB4900.DBX33.0` | 机器人发给系统,请求卡盘到原位（卡盘松开）信号 |
| <code>&#36;A_DBB[34]</code> | `DB4900.DBX34.0` | 机器人发给系统,请求卡盘到工作位（卡盘夹紧）信号（原索引笔误写为 DB4900.DBX33.0） |
| <code>&#36;A_DBB[60]</code> | `DB4900.DBX60.0` | 系统发给机器人,罩壳顶部门已打开信号,M80置1(有效),M81置0 |
| <code>&#36;A_DBB[61]</code> | `DB4900.DBX61.0` | 系统发给机器人,预完成,通知机械手准备,M82置1(有效),M83置0 |
| <code>&#36;A_DBB[62]</code> | `DB4900.DBX62.0` | 系统发给机器人,机床故障,M84置1(有效),M85置0 |
| <code>&#36;A_DBB[63]</code> | `DB4900.DBX63.0` | 系统发给机器人,尾架缩回到位,M86置1(有效),M87置0 |
| <code>&#36;A_DBB[64]</code> | `DB4900.DBX64.0` | 系统发给机器人,尾架伸出到位,M88置1(有效),M89置0 |
| <code>&#36;A_DBB[65]</code> | `DB4900.DBX65.0` | 系统发给机器人,卡盘松开到位,M92置1(有效),M93置0（原索引笔误写为 DB4900.DBX63.0） |
| <code>&#36;A_DBB[66]</code> | `DB4900.DBX66.0` | 系统发给机器人,卡盘夹紧到位,M94置1(有效),M95置0（原索引笔误写为 DB4900.DBX64.0） |
| <code>&#36;A_DBB[67]</code> | `DB4900.DBX67.0` | 系统发给机器人,机床旋转头架结束（吹气时使用）,M96置1(有效),M97置0（原索引笔误写为 DB4900.DBX64.0） |

<a id="pi-sec-3"></a>

### 2.3 快速输入输出信号（8 项）

| NC 信号变量 | PLC 地址 / 通道映射 | 含义与备注 |
| :--- | :--- | :--- |
| <code>&#36;A_IN[1]</code> | 快速 I/O / 测头硬件接口 | 在线测量-信号sr |
| <code>&#36;A_IN[2]</code> | 快速 I/O / 测头硬件接口 | 在线测量-信号st |
| <code>&#36;A_IN[3]</code> | 快速 I/O / 测头硬件接口 | 在线测量-信号f2 |
| <code>&#36;A_IN[4]</code> | 快速 I/O / 测头硬件接口 | 在线测量-信号f3 |
| <code>&#36;A_IN[10]</code> | 快速 I/O / 测头硬件接口 | 在线测量-自动模式信号 |
| <code>&#36;A_IN[11]</code> | 快速 I/O / 测头硬件接口 | 在线测量-就绪信号 |
| <code>&#36;A_IN[15]</code> | 快速 I/O / 测头硬件接口 | 粗磨消空程输入信号 |
| <code>&#36;A_OUT[3]</code> | 快速 I/O / 测头硬件接口 | 在线测量-启动 |

<a id="pi-sec-4"></a>

### 2.4 自动测量信号（6 项）

| NC 信号变量 | PLC 地址 / 通道映射 | 含义与备注 |
| :--- | :--- | :--- |
| <code>&#36;A_PROBE[1]</code> | 快速 I/O / 测头硬件接口 | 测量探头1偏转（测量探头接触上为1 未接触为0） |
| <code>&#36;A_PROBE[2]</code> | 快速 I/O / 测头硬件接口 | 测量探头2偏转 |
| <code>&#36;AC_MEA[1]</code> | 快速 I/O / 测头硬件接口 | 测量探头1任务状态（测量探头启动测量为0 接触为1 脱开也保持不变 下次启动测量置0） |
| <code>&#36;AC_MEA[2]</code> | 快速 I/O / 测头硬件接口 | 测量探头2任务状态 |
| `DB2700.DBX1.0` | 快速 I/O / 测头硬件接口 | 测头1信号状态 |
| `DB2700.DBX1.1` | 快速 I/O / 测头硬件接口 | 测头2信号状态 |

<a id="pi-sec-5"></a>

### 2.5 修整主参数(DRESSER)（146 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `AXIS_VER` | `AXIS_VER` | 修整垂直轴 | — |
| `AXIS_HORI` | `AXIS_HORI` | 修整水平轴 | — |
| `SHAPE` | `SHAPE` | 齿形程序的程序名 | — |
| `SHAPE_EXTERNAL` | `SHAPE_EXTERNAL` | 外部齿形程序的程序名 | — |
| `DRESSER[0]` | `DRESSER[1]` | 修整器选择 | 0VW/1XZ/2滚压V/3液压/4滚压X |
| `DRESSER[1]` | `DRESSER[2]` | 滚压轮齿高 | — |
| `DRESSER[2]` | `DRESSER[3]` | 两轮中心距 | — |
| `DRESSER[3]` | `DRESSER[4]` | 修整轮类型(0单/1双/2方) | — |
| `DRESSER[4]` | `DRESSER[5]` | 齿形选择(0三角/1梯形/2双圆弧) | — |
| `DRESSER[5]` | `DRESSER[6]` | 砂轮状态(0新/1旧) | — |
| `DRESSER[6]` | `DRESSER[7]` | 修整报警(0无报警) | — |
| `DRESSER[7]` | `DRESSER[8]` | 渐开线程序垂直最高点 | 外部齿形程序调用测试 |
| `DRESSER[8]` | `DRESSER[9]` | 机械手时下次磨削修整量计算 | — |
| `DRESSER[9]` | `DRESSER[10]` | 砂轮修整累积 | — |
| `DRESSER[10]` | `DRESSER[11]` | 当前速度 | — |
| `DRESSER[11]` | `DRESSER[12]` | 粗修次数 | — |
| `DRESSER[12]` | `DRESSER[13]` | 精修次数 | — |
| `DRESSER[13]` | `DRESSER[14]` | 新砂轮初始余量对应修整次数 | — |
| `DRESSER[14]` | `DRESSER[15]` | 粗修进给 | — |
| `DRESSER[15]` | `DRESSER[16]` | 精修进给 | — |
| `DRESSER[16]` | `DRESSER[17]` | 粗修速度 | — |
| `DRESSER[17]` | `DRESSER[18]` | 精修速度 | — |
| `DRESSER[18]` | `DRESSER[19]` | 当前粗修次数 | — |
| `DRESSER[19]` | `DRESSER[20]` | 当前精修次数 | — |
| `DRESSER[20]` | `DRESSER[21]` | 当前新砂轮抬刀需要修整次数 | — |
| `DRESSER[21]` | `DRESSER[22]` | 修整轮与砂轮中心位置水平坐标 | — |
| `DRESSER[22]` | `DRESSER[23]` | 砂轮宽 | — |
| `DRESSER[23]` | `DRESSER[24]` | 砂轮初始直径 | — |
| `DRESSER[24]` | `DRESSER[25]` | 砂轮当前直径 | — |
| `DRESSER[25]` | `DRESSER[26]` | 纯修整粗修次数 | — |
| `DRESSER[26]` | `DRESSER[27]` | 纯修整精修次数 | — |
| `DRESSER[27]` | `DRESSER[28]` | 纯修整粗修进给 | — |
| `DRESSER[28]` | `DRESSER[29]` | 纯修整精修进给 | — |
| `DRESSER[29]` | `DRESSER[30]` | 纯修整粗修速度 | — |
| `DRESSER[30]` | `DRESSER[31]` | 纯修整精修速度 | — |
| `DRESSER[31]` | `DRESSER[32]` | 修左侧砂轮齿形时使用的滚轮半径 | — |
| `DRESSER[32]` | `DRESSER[33]` | 修右侧砂轮齿形时使用的滚轮半径 | — |
| `DRESSER[33]` | `DRESSER[34]` | 左修整轮对砂轮中心 | — |
| `DRESSER[34]` | `DRESSER[35]` | 右修整轮对砂轮中心 | — |
| `DRESSER[35]` | `DRESSER[36]` | 砂轮最小直径 | — |
| `DRESSER[36]` | `DRESSER[37]` | 修整时砂轮转速 | — |
| `DRESSER[37]` | `DRESSER[38]` | 成型X修整时修整器在前还是在后 | 0=前 / 1=后 |
| `DRESSER[38]` | `DRESSER[39]` | 界面工艺修整量总量 | — |
| `DRESSER[39]` | `DRESSER[40]` | 双圆弧自动计算参数 | (0否1是) |
| `DRESSER[40]` | `DRESSER[41]` | 外部齿形程序读取参数标记 | — |
| `DRESSER[41]` | `DRESSER[42]` | 外部齿形程序右起点角度 | — |
| `DRESSER[42]` | `DRESSER[43]` | 外部齿形程序左起点角度 | — |
| `DRESSER[43]` | `DRESSER[44]` | 外部齿形程序顶部平台长度 | — |
| `DRESSER[44]` | `DRESSER[45]` | 外部齿形修整右半边0/左半边1标记 | — |
| `DRESSER[45]` | `DRESSER[46]` | 外部齿形右终点角度 | — |
| `DRESSER[46]` | `DRESSER[47]` | 外部齿形左终点角度 | — |
| `DRESSER[47]` | `DRESSER[48]` | 成型修整粗修停留时间 | — |
| `DRESSER[48]` | `DRESSER[49]` | 成型修整当前停留时间 | — |
| `DRESSER[49]` | `DRESSER[50]` | 砂轮最大磨削直径 | — |
| `DRESSER[50]` | `DRESSER[51]` | 外部齿形程序类型 | (-1外螺纹/1内螺纹) |
| `DRESSER[51]` | `DRESSER[52]` | 外部齿形程序右终点水平坐标 | — |
| `DRESSER[52]` | `DRESSER[53]` | 夹具磨削-停留时间 | — |
| `DRESSER[53]` | `DRESSER[54]` | 夹具磨削-磨削次数 | — |
| `DRESSER[54]` | `DRESSER[55]` | 磨削中心-外磨砂轮修整时头架停止转动并移动到固定角度(0否1是) | — |
| `DRESSER[55]` | `DRESSER[56]` | 磨削中心-外磨砂轮修整时头架移动固定角度 | — |
| `DRESSER[56]` | `DRESSER[57]` | 通用齿型程序-插补修整平面选择（0=G17 1-2几何轴 / 1=G18 1-3几何轴 / 2=G19 2-3几何轴） | — |
| `DRESSER[57]` | `DRESSER[58]` | 磨削中修整是否提前一刀启动滚轮(0否1是) | — |
| `DRESSER[58]` | `DRESSER[59]` | 螺纹/外圆/端面-磨削中每次修整对磨削位置补偿量界面参数是否打开(0隐藏/1打开) | — |
| `DRESSER[59]` | `DRESSER[60]` | 外磨砂轮相对中心偏转角度(默认0即不补偿) | 如果外磨砂轮从始至终不修端面平面部分，需要外圆修整时根据这个角度对左右端面初始接触进行补偿，也就是外磨起点终点 |
| `DRESSER[60]` | `DRESSER[61]` | 夹具磨削,Z轴左端位置 | — |
| `DRESSER[61]` | `DRESSER[62]` | 夹具磨削,Z轴右端位置 | — |
| `DRESSER[62]` | `DRESSER[63]` | 夹具磨削,X轴初始接触 | — |
| `DRESSER[63]` | `DRESSER[64]` | 夹具修整砂轮,Z轴左端位置 | — |
| `DRESSER[64]` | `DRESSER[65]` | 夹具修整砂轮,Z轴右端位置 | — |
| `DRESSER[65]` | `DRESSER[66]` | 夹具修整砂轮,X轴初始接触 | — |
| `DRESSER[66]` | `DRESSER[67]` | 夹具修整砂轮,修整次数 | — |
| `DRESSER[67]` | `DRESSER[68]` | 夹具修整砂轮,进刀量 | — |
| `DRESSER[68]` | `DRESSER[69]` | 夹具磨削/修整砂轮,修整次数累积 | — |
| `DRESSER[69]` | `DRESSER[70]` | 夹具磨削,进刀量 | — |
| `DRESSER[70]` | `DRESSER[71]` | 修整一次磨削位补偿量 | — |
| `DRESSER[71]` | `DRESSER[72]` | 修整一次磨削位补偿量累计 | — |
| `DRESSER[72]` | `DRESSER[73]` | 外圆磨砂轮修整终点的Z坐标 | — |
| `DRESSER[73]` | `DRESSER[74]` | 外圆磨砂轮修整,当前粗修次数 | — |
| `DRESSER[74]` | `DRESSER[75]` | 外圆磨砂轮修整,当前精修次数 | — |
| `DRESSER[75]` | `DRESSER[76]` | 外圆磨砂轮修整,程序用粗修次数 | — |
| `DRESSER[76]` | `DRESSER[77]` | 外圆磨砂轮修整,程序用精修次数 | — |
| `DRESSER[77]` | `DRESSER[78]` | 外圆磨砂轮修整,粗修进刀量 | — |
| `DRESSER[78]` | `DRESSER[79]` | 外圆磨砂轮修整,精修进刀量 | — |
| `DRESSER[79]` | `DRESSER[80]` | 外圆磨砂轮修整,粗修进给速度 | — |
| `DRESSER[80]` | `DRESSER[81]` | 外圆磨砂轮修整,精修进给速度 | — |
| `DRESSER[81]` | `DRESSER[82]` | 外圆磨砂轮修整,共用修整速度 | — |
| `DRESSER[82]` | `DRESSER[83]` | 外圆磨砂轮修整,界面设定粗修次数 | — |
| `DRESSER[83]` | `DRESSER[84]` | 外圆磨砂轮修整,界面设定精修次数 | — |
| `DRESSER[84]` | `DRESSER[85]` | 外圆磨砂轮修整,界面设定粗修进给量 | — |
| `DRESSER[85]` | `DRESSER[86]` | 外圆磨砂轮修整,界面设定精修进给量 | — |
| `DRESSER[86]` | `DRESSER[87]` | 外圆磨砂轮修整,界面设定粗修进给速度 | — |
| `DRESSER[87]` | `DRESSER[88]` | 外圆磨砂轮修整,界面设定精修进给速度 | — |
| `DRESSER[88]` | `DRESSER[89]` | 金刚笔与U轴砂轮外圆接触时的当前U坐标 | — |
| `DRESSER[89]` | `DRESSER[90]` | 外圆外圆部分磨砂轮新旧(0新1旧) | — |
| `DRESSER[90]` | `DRESSER[91]` | 外圆磨砂轮等效初始直径 | — |
| `DRESSER[91]` | `DRESSER[92]` | 外圆磨砂轮等效当前直径 | — |
| `DRESSER[92]` | `DRESSER[93]` | 外圆磨削中修整一次磨削位补偿量-输入正值则往轴方向正向补偿 | — |
| `DRESSER[93]` | `DRESSER[94]` | 外圆磨砂轮修整起点的Z坐标 | — |
| `DRESSER[94]` | `DRESSER[95]` | 外圆磨砂轮侧面修整,界面设定粗修次数 | — |
| `DRESSER[95]` | `DRESSER[96]` | 外圆磨砂轮侧面修整,界面设定精修次数 | — |
| `DRESSER[96]` | `DRESSER[97]` | 外圆磨砂轮侧面修整,界面设定粗修进给量 | — |
| `DRESSER[97]` | `DRESSER[98]` | 外圆磨砂轮侧面修整,界面设定精修进给量 | — |
| `DRESSER[98]` | `DRESSER[99]` | 端面磨削中修整一次磨削位补偿量-输入正值则往轴方向正向补偿 | — |
| `DRESSER[99]` | `DRESSER[100]` | 外部齿型程序外围斜线长度(外部程序内部赋值) | — |
| `DRESSER[100]` | `DRESSER[101]` | 外圆磨砂轮侧面修整,U轴初始位置,即起点,靠近头架 | — |
| `DRESSER[101]` | `DRESSER[102]` | 外圆磨砂轮侧面修整,U轴结束位置,终点,远离头架 | — |
| `DRESSER[102]` | `DRESSER[103]` | 外圆磨砂轮侧面修整,粗修进给速度 | — |
| `DRESSER[103]` | `DRESSER[104]` | 外圆磨砂轮侧面修整,精修进给速度 | — |
| `DRESSER[104]` | `DRESSER[105]` | 外圆磨砂轮侧面修整,当前粗修次数 | — |
| `DRESSER[105]` | `DRESSER[106]` | 外圆磨砂轮侧面修整,当前精修次数 | — |
| `DRESSER[106]` | `DRESSER[107]` | 外部齿型程序无外围延长部分修整(0有1无) | — |
| `DRESSER[107]` | `DRESSER[108]` | 外圆磨砂轮侧面修整,公用进给速度 | — |
| `DRESSER[108]` | `DRESSER[109]` | 外圆磨砂轮侧面修整,Z轴修整当前位置 | — |
| `DRESSER[109]` | `DRESSER[110]` | 外圆磨砂轮左端面,磨削中是否修整累计计数(0不修整/1修整) | — |
| `DRESSER[110]` | `DRESSER[111]` | 外部齿形程序相关界面参数显示(0否1是) | — |
| `DRESSER[111]` | `DRESSER[112]` | 三角齿型-是否带丝底凹槽(0无1有) | — |
| `DRESSER[112]` | `DRESSER[113]` | 双圆弧界面自动计算标准切换（标准 0.9 / 1.2 切换） | — |
| `DRESSER[113]` | `DRESSER[114]` | 新砂轮是否是成型砂轮(0否1是) | — |
| `DRESSER[114]` | `DRESSER[115]` | 开放附加齿型选择(0否/1是) | — |
| `DRESSER[115]` | `DRESSER[116]` | 外部齿形程序左终点水平坐标 | — |
| `DRESSER[116]` | `DRESSER[117]` | 夹具修整砂轮转速 | — |
| `DRESSER[117]` | `DRESSER[118]` | 夹具修整修整轮转速 | — |
| `DRESSER[118]` | `DRESSER[119]` | 夹具磨削砂轮转速 | — |
| `DRESSER[119]` | `DRESSER[120]` | 金刚笔与U轴砂轮外圆初始接触时的坐标 | — |
| `DRESSER[120]` | `DRESSER[121]` | 端面砂轮修整,程序用粗修次数 | — |
| `DRESSER[121]` | `DRESSER[122]` | 端面砂轮修整,程序用精修次数 | — |
| `DRESSER[122]` | `DRESSER[123]` | 端面砂轮修整,程序用粗修进刀量 | — |
| `DRESSER[123]` | `DRESSER[124]` | 端面砂轮修整,程序用精修进刀量 | — |
| `DRESSER[124]` | `DRESSER[125]` | 端面砂轮修整,程序用粗修进给速度 | — |
| `DRESSER[125]` | `DRESSER[126]` | 端面砂轮修整,程序用精修进给速度 | — |
| `DRESSER[126]` | `DRESSER[127]` | 金刚笔与U轴砂轮端面初始接触时的Z坐标 | — |
| `DRESSER[127]` | `DRESSER[128]` | 外磨累积修整量 | — |
| `DRESSER[128]` | `DRESSER[129]` | 端面累积修整量 | — |
| `DRESSER[129]` | `DRESSER[130]` | 外圆端面部分磨砂轮新旧(0新1旧) | — |
| `DRESSER[130]` | `DRESSER[131]` | 端面修整砂轮当前转速 | — |
| `DRESSER[131]` | `DRESSER[132]` | 外部齿形程序右终点垂直坐标 | — |
| `DRESSER[132]` | `DRESSER[133]` | 外圆修整锥度微调(正 左低右高/负 左高右低) | — |
| `DRESSER[133]` | `DRESSER[134]` | 新砂轮修整模式(0抬齿高/1偏半个砂轮宽度)-实际 | — |
| `DRESSER[134]` | `DRESSER[135]` | 新砂轮修整模式1偏半个砂轮宽度：当前左水平位置 | — |
| `DRESSER[135]` | `DRESSER[136]` | 新砂轮修整模式1偏半个砂轮宽度：当前右水平位置 | — |
| `DRESSER[136]` | `DRESSER[137]` | 端面修整锥度微调(正 前大后小/负 前小后大) | — |
| `DRESSER[137]` | `DRESSER[138]` | 外圆砂轮最小磨削直径 | — |
| `DRESSER[138]` | `DRESSER[139]` | 外部齿形程序左终点垂直坐标 | — |
| `DRESSER[139]` | `DRESSER[140]` | 是否使用外部齿形程序(0否/1是-左右分开修整/2是-带刀具的连续轨迹曲线) | — |
| `DRESSER[140]` | `DRESSER[141]` | UW修整器-修整位.X | — |
| `DRESSER[141]` | `DRESSER[142]` | 平面修砂轮即内孔磨砂轮修整时锥度(正值为修整后砂轮左大右小-单位mm) | — |

<a id="pi-sec-6"></a>

### 2.6 初始化参数(INI)（163 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `INI[0]` | `INI[1]` | 螺纹旋向(0右旋/1左旋) | — |
| `INI[1]` | `INI[2]` | 工件磨削左端坐标 | — |
| `INI[2]` | `INI[3]` | 工件磨削右端坐标 | — |
| `INI[3]` | `INI[4]` | 磨削长度 | — |
| `INI[4]` | `INI[5]` | 螺距 | — |
| `INI[5]` | `INI[6]` | 导程 | — |
| `INI[6]` | `INI[7]` | 磨削起点 | — |
| `INI[7]` | `INI[8]` | 磨削终点 | — |
| `INI[8]` | `INI[9]` | 磨削中点 | — |
| `INI[9]` | `INI[10]` | 磨削总角度 | — |
| `INI[10]` | `INI[11]` | 外螺纹时表示对刀起始位置的X值 | (内螺纹时为砂轮中心与头架中心重合时的X坐标) |
| `INI[11]` | `INI[12]` | 滚压轮修整中反向距离 | — |
| `INI[12]` | `INI[13]` | 外圆台阶长度 | — |
| `INI[13]` | `INI[14]` | 外圆台阶分段 | — |
| `INI[14]` | `INI[15]` | 单位长度锥度值(半径方向)，内螺纹大头往小头磨,外螺纹小头往大头磨 | — |
| `INI[15]` | `INI[16]` | 锥度对应的全长X增量(半径方向) | — |
| `INI[16]` | `INI[17]` | 螺旋升角使能 | — |
| `INI[17]` | `INI[18]` | 螺旋升角值 | — |
| `INI[18]` | `INI[19]` | 蜗杆齿高 | — |
| `INI[19]` | `INI[20]` | 断电回退后退距离(限制最大5mm) | — |
| `INI[20]` | `INI[21]` | 螺旋升角值 | — |
| `INI[21]` | `INI[22]` | 内螺纹反向孔倒角-界面开启(0隐藏/1开启) | — |
| `INI[22]` | `INI[23]` | 内螺纹反向孔倒角-每段起始z坐标自动测量 | 0手动输入/1根据第一倒角位置计算后续位置/2自动探测第一孔位置计算 |
| `INI[23]` | `INI[24]` | 退刀位置 | — |
| `INI[24]` | `INI[25]` | 全长导程补偿 | — |
| `INI[25]` | `INI[26]` | 退刀计算标志位 | — |
| `INI[26]` | `INI[27]` | 单件小批量/批量生产 | — |
| `INI[27]` | `INI[28]` | 头架在程序结束调整到合适角度 | — |
| `INI[28]` | `INI[29]` | 内螺纹时台面起始位置 外螺纹机械手上料位置Z | — |
| `INI[29]` | `INI[30]` | 工件安装位置允许的最大误差 | — |
| `INI[30]` | `INI[31]` | 磨削中心工件长度设置 | — |
| `INI[31]` | `INI[32]` | 腰型孔角度(展开图尺寸) | — |
| `INI[32]` | `INI[33]` | 腰型孔长(展开图尺寸) | — |
| `INI[33]` | `INI[34]` | 腰型孔宽(展开图尺寸) | — |
| `INI[34]` | `INI[35]` | 内螺纹螺母外圆直径 | — |
| `INI[35]` | `INI[36]` | 工件端面到反相器孔距离 | — |
| `INI[36]` | `INI[37]` | 砂轮类型选择(0模拟量/1伺服/2异步电机) | — |
| `INI[37]` | `INI[38]` | 修整轮类型选择(0模拟量/1伺服/2异步电机) | — |
| `INI[38]` | `INI[39]` | 螺旋升角自动计算 | — |
| `INI[39]` | `INI[40]` | 工件中径 | — |
| `INI[40]` | `INI[41]` | 新砂轮磨削接触位计算标记 | — |
| `INI[41]` | `INI[42]` | 磨削中心-外圆磨削-磨削中修整是否修整端面部分(0否/1是) | — |
| `INI[42]` | `INI[43]` | (外螺纹自动对刀)砂轮中心与接近开关/测头中心重合时Z轴坐标 | — |
| `INI[43]` | `INI[44]` | 耳朵深度 | — |
| `INI[44]` | `INI[45]` | 内螺纹反向孔倒角-反向孔个数 | — |
| `INI[45]` | `INI[46]` | 内螺纹反向孔倒角-反向孔间z向距离 | — |
| `INI[46]` | `INI[47]` | 内螺纹反向孔倒角-起始位补偿z | — |
| `INI[47]` | `INI[48]` | 磨削中不正常退出标记(0正常/1不正常) | — |
| `INI[48]` | `INI[49]` | 自动对刀测头Z轴方向起始位置(此位置手动大概对出来保证安全) | — |
| `INI[49]` | `INI[50]` | 自动对刀工件C方向合适角度，换向器孔方便测量 | — |
| `INI[50]` | `INI[51]` | 自动对刀测头接触工件右端面Z坐标 | — |
| `INI[51]` | `INI[52]` | 内螺纹自动对刀-开关测量-测量位.X | — |
| `INI[52]` | `INI[53]` | 自动对刀开关测量方式下，开关进入工件开始测量Z起始位置 | — |
| `INI[53]` | `INI[54]` | 对刀时砂轮转速 | — |
| `INI[54]` | `INI[55]` | X轴快速离开的动作的速度 | — |
| `INI[55]` | `INI[56]` | X轴快速接近/参与实际有效加工的动作的速度 | — |
| `INI[56]` | `INI[57]` | Z轴快速转换的动作的速度 | — |
| `INI[57]` | `INI[58]` | Z轴慢速转换的动作的速度 | — |
| `INI[58]` | `INI[59]` | C轴快速到位的速度 | — |
| `INI[59]` | `INI[60]` | C轴慢速参与加工的速度 | — |
| `INI[60]` | `INI[61]` | A轴到位的速度 | — |
| `INI[61]` | `INI[62]` | V轴快速离开砂轮的速度 | — |
| `INI[62]` | `INI[63]` | V轴快速接近砂轮的速度 | — |
| `INI[63]` | `INI[64]` | W轴快速离开砂轮的速度 | — |
| `INI[64]` | `INI[65]` | W轴快速接近砂轮的速度 | — |
| `INI[65]` | `INI[66]` | X轴慢速转换的动作的速度 | — |
| `INI[66]` | `INI[67]` | 磨削中心-外圆磨削-磨削中修整端面部分标记 | — |
| `INI[67]` | `INI[68]` | 自磨修整头架修整器C起始角度 | — |
| `INI[68]` | `INI[69]` | 是否自磨夹具(0否/1是) | — |
| `INI[69]` | `INI[70]` | 是否有自动对刀(0没有/1有) | — |
| `INI[70]` | `INI[71]` | 程序结束是否关闭修整/对刀键(0否/1是) | — |
| `INI[71]` | `INI[72]` | 砂轮启动等待转速到位延时时间 | — |
| `INI[72]` | `INI[73]` | 磨削中进行过修整后的标记，用来判断是否需要X到位(0未修整/1刚刚修整过) | — |
| `INI[73]` | `INI[74]` | 磨削工件计数(磨削完毕后累加) | — |
| `INI[74]` | `INI[75]` | 磨削几件后修整(次数到达后,下一次开始时修整) | — |
| `INI[75]` | `INI[76]` | 磨削几件后修整标记位 | — |
| `INI[76]` | `INI[77]` | 蜗杆模数输入 | — |
| `INI[77]` | `INI[78]` | 上一次新砂轮直径缓存 | — |
| `INI[78]` | `INI[79]` | 有无二次对刀(0无1有) | — |
| `INI[79]` | `INI[80]` | 程序结束砂轮是否停止(0停/1不停转速保持/2不停低速旋转) | — |
| `INI[80]` | `INI[81]` | 对刀头架转速 | — |
| `INI[81]` | `INI[82]` | 打环形槽砂轮转速 | — |
| `INI[82]` | `INI[83]` | 内螺纹反向孔倒角-使能(0不倒角/1倒角) | — |
| `INI[83]` | `INI[84]` | 内螺纹反向孔倒角-自动测量第几个孔(最右侧孔为第一个) | — |
| `INI[84]` | `INI[85]` | 内螺纹是否螺旋退出工件(0否1是) | — |
| `INI[85]` | `INI[86]` | 是否使用机械手(0否1是) | — |
| `INI[86]` | `INI[87]` | 输入螺距(调用内部齿形/磨螺纹):0/输入模数(调用蜗杆齿形):1 | — |
| `INI[87]` | `INI[88]` | 通用齿形模块齿形右侧高低微调 | — |
| `INI[88]` | `INI[89]` | 新砂轮插补修整模式(0抬齿高/1偏半个砂轮宽度)-设定 | — |
| `INI[89]` | `INI[90]` | 夹具磨削z轴安全起始位置 | — |
| `INI[90]` | `INI[91]` | 自动对刀后是否直接磨削(0否1是) | — |
| `INI[91]` | `INI[92]` | 外圆砂轮类型选择(0模拟量/1伺服/2异步电机) | — |
| `INI[92]` | `INI[93]` | 外圆砂轮程序结束砂轮是否停止(0立刻停/1低速旋转直到程序结束/2低速旋转程序结束也不停) | — |
| `INI[93]` | `INI[94]` | 外圆磨削工件计数(磨削完毕后累加) | — |
| `INI[94]` | `INI[95]` | 外圆磨削几件后修整(次数到达后,下一次开始时修整) | — |
| `INI[95]` | `INI[96]` | 外圆磨削几件后修整标记位 | — |
| `INI[96]` | `INI[97]` | 外圆磨削中不正常退出标记(0正常/1不正常) | — |
| `INI[97]` | `INI[98]` | 外圆0是单件磨削模式,1是批量磨削模式 | — |
| `INI[98]` | `INI[99]` | 端面磨削工件计数(磨削完毕后累加) | — |
| `INI[99]` | `INI[100]` | 端面磨削几件后修整(次数到达后,下一次开始时修整) | — |
| `INI[100]` | `INI[101]` | 端面磨削几件后修整标记位 | — |
| `INI[101]` | `INI[102]` | 左端面磨削中不正常退出标记(0正常/1不正常) | — |
| `INI[102]` | `INI[103]` | 右端面磨削中不正常退出标记(0正常/1不正常) | — |
| `INI[103]` | `INI[104]` | 端面0是单件磨削模式,1是批量磨削模式 | — |
| `INI[104]` | `INI[105]` | 右端面进行过纯修整标记 | — |
| `INI[105]` | `INI[106]` | U轴快速转换的动作的速度 | — |
| `INI[106]` | `INI[107]` | U轴慢速转换的动作的速度 | — |
| `INI[107]` | `INI[108]` | 外磨砂轮后退安全位置 | — |
| `INI[108]` | `INI[109]` | 外磨砂轮磨削z起始安全位置 | — |
| `INI[109]` | `INI[110]` | 对刀模式(zc插补0/静止对刀1) | — |
| `INI[110]` | `INI[111]` | 内螺纹反向孔倒角-精磨/终磨不进行倒角(0否1是) | — |
| `INI[111]` | `INI[112]` | 执行修整中每20次重新运行砂轮转速子程序(默认为跳过)(0否1是) | — |
| `INI[112]` | `INI[113]` | 砂轮静止启动延时 | — |
| `INI[113]` | `INI[114]` | 砂轮动态启动延时 | — |
| `INI[114]` | `INI[115]` | 修整轮静止启动延时 | — |
| `INI[115]` | `INI[116]` | 修整轮动态启动延时 | — |
| `INI[116]` | `INI[117]` | 在线测量FA速度 | — |
| `INI[117]` | `INI[118]` | 在线测量F3速度 | — |
| `INI[118]` | `INI[119]` | 在线测量F2速度 | — |
| `INI[119]` | `INI[120]` | 在线测量延时 | — |
| `INI[120]` | `INI[121]` | 工件外径 | — |
| `INI[121]` | `INI[122]` | 三线测量 | — |
| `INI[122]` | `INI[123]` | 钢球直径 | — |
| `INI[123]` | `INI[124]` | 终尺寸H | — |
| `INI[124]` | `INI[125]` | 外圆测量点1 | — |
| `INI[125]` | `INI[126]` | 外圆测量点2 | — |
| `INI[126]` | `INI[127]` | 外圆测量点3 | — |
| `INI[127]` | `INI[128]` | 外圆测量三点偏移报警阈值 | — |
| `INI[128]` | `INI[129]` | 外圆测量三点最小值 | — |
| `INI[129]` | `INI[130]` | 外圆测量三点最大值 | — |
| `INI[130]` | `INI[131]` | 机床出厂编号设置 | — |
| `INI[131]` | `INI[132]` | 右端/外圆测量合适角度 | — |
| `INI[132]` | `INI[133]` | 滚压轮修整退出距离 | — |
| `INI[133]` | `INI[134]` | 磨削中心：外圆测量跳动值 | — |
| `INI[134]` | `INI[135]` | 任意点对刀位置输入 | — |
| `INI[135]` | `INI[136]` | 螺纹旋转退出转速 | — |
| `INI[136]` | `INI[137]` | 右端面测量安全值 | — |
| `INI[137]` | `INI[138]` | 右端面测量阈值 | — |
| `INI[138]` | `INI[139]` | 外圆是否测量圆度(0否1是) | — |
| `INI[139]` | `INI[140]` | 磨削中心右端测量与设置当前差值 | — |
| `INI[140]` | `INI[141]` | 磨削中心工件长度测量 | — |
| `INI[141]` | `INI[142]` | 全长锥度补偿(半径方向补偿) | — |
| `INI[142]` | `INI[143]` | 外圆砂轮静止启动延时 | — |
| `INI[143]` | `INI[144]` | 外圆砂轮动态启动延时 | — |
| `INI[144]` | `INI[145]` | 砂轮是否恒转速(0否1是) | — |
| `INI[145]` | `INI[146]` | 磨削中心外圆保持分段磨削段数 | — |
| `INI[146]` | `INI[147]` | 磨削中心外圆粗磨/端面/台阶磨削停留时间 | — |
| `INI[147]` | `INI[148]` | 外圆粗磨/端面/台阶进刀速度 | — |
| `INI[148]` | `INI[149]` | 界面三线测量参数显示 | — |
| `INI[149]` | `INI[150]` | 界面外圆在线测量参数显示 | — |
| `INI[150]` | `INI[151]` | 砂轮最高速度限制 | — |
| `INI[151]` | `INI[152]` | 滚轮最高速度限制 | — |
| `INI[152]` | `INI[153]` | 磨削中心外圆砂轮最高速度限制 | — |
| `INI[153]` | `INI[154]` | 修整时A轴角度调整 | — |
| `INI[154]` | `INI[155]` | 显示修整时A轴角度调整参数(0不显示1显示) | — |
| `INI[155]` | `INI[156]` | 修整轮反向旋转(0不反1反) | — |
| `INI[156]` | `INI[157]` | 磨削中心：工件是否在旋转(0未旋转1旋转中) | — |
| `INI[157]` | `INI[158]` | 自动对刀-测量机构1-伸出缩回是否有检测信号(0有1没有) | — |
| `INI[158]` | `INI[159]` | 转完A轴是否关闭液压(0关1不关) | — |
| `INI[159]` | `INI[160]` | 自动对刀测量是否二次慢速检测(0两次/1一次) | — |
| `INI[160]` | `INI[161]` | 自动对刀-测量机构2-伸出缩回是否有检测信号(0有1没有) | — |
| `INI[161]` | `INI[162]` | 寿命管理-当前滚轮序号 | — |
| `INI[162]` | `INI[163]` | 自动对刀-反向孔-是否只测量上下C角度同时补偿端面Z到偏刀调整(0否1是) | — |

<a id="pi-sec-7"></a>

### 2.7 对刀(TOOL_SET)（70 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `TOOL_SET[0]` | `TOOL_SET[1]` | 初始对刀点Z轴坐标 | — |
| `TOOL_SET[1]` | `TOOL_SET[2]` | 对刀完成后Z轴坐标(自动对刀) | — |
| `TOOL_SET[2]` | `TOOL_SET[3]` | 对刀完成时手轮偏置值 | — |
| `TOOL_SET[3]` | `TOOL_SET[4]` | 完成对刀时砂轮X轴坐标 | — |
| `TOOL_SET[4]` | `TOOL_SET[5]` | 计算出的C轴起始角度 | — |
| `TOOL_SET[5]` | `TOOL_SET[6]` | C轴初始角度 | — |
| `TOOL_SET[6]` | `TOOL_SET[7]` | 磨削中心外磨加工完后砂轮低速运行转速 | — |
| `TOOL_SET[7]` | `TOOL_SET[8]` | 内螺纹反向孔倒角-自动计算时每个孔第二条滚道起点z偏移量(默认0表示和第一条起点相差360度) | — |
| `TOOL_SET[8]` | `TOOL_SET[9]` | 对刀类型(0首次/1二次) | — |
| `TOOL_SET[9]` | `TOOL_SET[10]` | 测头半径 | — |
| `TOOL_SET[10]` | `TOOL_SET[11]` | 测头与砂轮距离(Z向) | — |
| `TOOL_SET[11]` | `TOOL_SET[12]` | 界面中径调整限制值(默认0表示限制为正负1) | — |
| `TOOL_SET[12]` | `TOOL_SET[13]` | 工艺界面除粗磨外进给量设置限制值(默认0表示限制为正负0.1) | — |
| `TOOL_SET[13]` | `TOOL_SET[14]` | 修整界面进给量设置限制值(默认0表示限制为 0~0.1) | — |
| `TOOL_SET[14]` | `TOOL_SET[15]` | 磨削中心-外圆端面修整进给量设置限制值(默认0表示限制为 0~0.1) | — |
| `TOOL_SET[15]` | `TOOL_SET[16]` | 自动对刀-外围移动动作速度 | — |
| `TOOL_SET[16]` | `TOOL_SET[17]` | 界面机械手按钮使能(0关1开) | — |
| `TOOL_SET[17]` | `TOOL_SET[18]` | 内螺纹反向孔倒角-是否平滑曲线-第一次对位置时不要平滑(0否1是) | — |
| `TOOL_SET[18]` | `TOOL_SET[19]` | 侧门关闭是否有检测开关(0没有1有) | — |
| `TOOL_SET[19]` | `TOOL_SET[20]` | (0起点对刀/1中点对刀/2任意) | — |
| `TOOL_SET[20]` | `TOOL_SET[21]` | 对刀完成时手轮偏置值 | — |
| `TOOL_SET[21]` | `TOOL_SET[22]` | 对刀完成后Z轴坐标(手动对刀) | — |
| `TOOL_SET[22]` | `TOOL_SET[23]` | (0=圆形孔,1=腰型孔) | — |
| `TOOL_SET[23]` | `TOOL_SET[24]` | 自动对刀-旋转轴快速测量速度 | — |
| `TOOL_SET[24]` | `TOOL_SET[25]` | 外圆半精磨进刀速度 | — |
| `TOOL_SET[25]` | `TOOL_SET[26]` | 外圆精磨进刀速度 | — |
| `TOOL_SET[26]` | `TOOL_SET[27]` | 外圆终磨进刀速度 | — |
| `TOOL_SET[27]` | `TOOL_SET[28]` | 磨削中心外圆半精磨磨削停留时间 | — |
| `TOOL_SET[28]` | `TOOL_SET[29]` | 磨削中心外圆精磨磨削停留时间 | — |
| `TOOL_SET[29]` | `TOOL_SET[30]` | 磨削中心外圆终磨磨削停留时间 | — |
| `TOOL_SET[30]` | `TOOL_SET[31]` | 环形槽磨削进刀后停留时间 | — |
| `TOOL_SET[31]` | `TOOL_SET[32]` | 自动对刀是否有接近开关测量机构 | — |
| `TOOL_SET[32]` | `TOOL_SET[33]` | 测头接触上边沿C角度 | — |
| `TOOL_SET[33]` | `TOOL_SET[34]` | 测头接触下边沿C角度 | — |
| `TOOL_SET[34]` | `TOOL_SET[35]` | 测头接触左边沿Z坐标 | — |
| `TOOL_SET[35]` | `TOOL_SET[36]` | 测头接触右边沿Z坐标 | — |
| `TOOL_SET[36]` | `TOOL_SET[37]` | 测头在孔中间Z坐标 | — |
| `TOOL_SET[37]` | `TOOL_SET[38]` | 接近开关接触第一个齿C坐标 | — |
| `TOOL_SET[38]` | `TOOL_SET[39]` | 接近开关接触第二个齿C坐标 | — |
| `TOOL_SET[39]` | `TOOL_SET[40]` | 接近开关接触齿底C坐标 | — |
| `TOOL_SET[40]` | `TOOL_SET[41]` | 是否已进行过二次对刀的标记 | — |
| `TOOL_SET[41]` | `TOOL_SET[42]` | 自动对刀结果调整 | — |
| `TOOL_SET[42]` | `TOOL_SET[43]` | Z轴偏刀微调 | — |
| `TOOL_SET[43]` | `TOOL_SET[44]` | 内螺纹自动对刀测量方向(1向前测量/-1向后测量) | — |
| `TOOL_SET[44]` | `TOOL_SET[45]` | 磨削中心自动对刀是否测量左端面(0否1是) | — |
| `TOOL_SET[45]` | `TOOL_SET[46]` | 磨削中心自动对刀左端测量设置 | — |
| `TOOL_SET[46]` | `TOOL_SET[47]` | 磨削中心自动对刀左端实际测量 | — |
| `TOOL_SET[47]` | `TOOL_SET[48]` | 磨削中心自动对刀左端测量阈值 | — |
| `TOOL_SET[48]` | `TOOL_SET[49]` | 磨削中心自动对刀左端测量误差 | — |
| `TOOL_SET[49]` | `TOOL_SET[50]` | 自动对刀是否有测量头测量结构 | — |
| `TOOL_SET[50]` | `TOOL_SET[51]` | 外螺纹自动对刀测量头中心(左)到接近开关(右)的水平距离 | — |
| `TOOL_SET[51]` | `TOOL_SET[52]` | 接近开关(0-测量机构1/1-测量机构2) | — |
| `TOOL_SET[52]` | `TOOL_SET[53]` | 测量头(0-测量机构1/1-测量机构2) | — |
| `TOOL_SET[53]` | `TOOL_SET[54]` | 测量中AC_MEA信号的状态 | — |
| `TOOL_SET[54]` | `TOOL_SET[55]` | 测量中<code>&#36;A_PROBE</code>信号的状态 | — |
| `TOOL_SET[55]` | `TOOL_SET[56]` | 当前正在进行接近开关0/测量头1机构测量 | — |
| `TOOL_SET[56]` | `TOOL_SET[57]` | 首件工件对刀c角度设置（0=当前 C 起始角 / 1=0° 对刀） | — |
| `TOOL_SET[57]` | `TOOL_SET[58]` | 是否是首件工件对刀,0是1否,用于批量但每件都手动对刀时保持尺寸一致性 | — |
| `TOOL_SET[58]` | `TOOL_SET[59]` | 磨削中心测左端面前让C转一角度,避开卡盘 | — |
| `TOOL_SET[59]` | `TOOL_SET[60]` | 变螺距工件：是否有变螺距 | — |
| `TOOL_SET[60]` | `TOOL_SET[61]` | 变螺距工件：变螺距模式(0给定角度/1给定终点位置) | — |
| `TOOL_SET[61]` | `TOOL_SET[62]` | 螺距变换界面隐藏(0隐藏/1单/2多) | — |
| `TOOL_SET[62]` | `TOOL_SET[63]` | 自动对刀-直线轴快速测量速度 | — |
| `TOOL_SET[63]` | `TOOL_SET[64]` | 自动对刀-直线轴慢速测量速度 | — |
| `TOOL_SET[64]` | `TOOL_SET[65]` | 变螺距工件：砂轮在孔1处z坐标 | — |
| `TOOL_SET[65]` | `TOOL_SET[66]` | 变螺距工件：砂轮在孔2处z坐标 | — |
| `TOOL_SET[66]` | `TOOL_SET[67]` | 变螺距工件：中间段螺距 | — |
| `TOOL_SET[67]` | `TOOL_SET[68]` | 变螺距工件：位置1位置2相对c旋转角度 | — |
| `TOOL_SET[68]` | `TOOL_SET[69]` | 磨削中心：自动对刀标记 | — |
| `TOOL_SET[69]` | `TOOL_SET[70]` | 自动对刀-旋转轴慢速测量速度 | — |

<a id="pi-sec-8"></a>

### 2.8 滚轮参数(WHEEL)（20 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `WHEEL[0]` | `WHEEL[1]` | 修整轮直径 | — |
| `WHEEL[1]` | `WHEEL[2]` | 修整轮线速度 | — |
| `WHEEL[2]` | `WHEEL[3]` | 双滚轮间距 | — |
| `WHEEL[3]` | `WHEEL[4]` | 方滚轮厚度 | — |
| `WHEEL[4]` | `WHEEL[5]` | 单滚轮左圆弧半径 | — |
| `WHEEL[5]` | `WHEEL[6]` | 单滚轮右圆弧半径 | — |
| `WHEEL[6]` | `WHEEL[7]` | 双滚轮左圆弧半径 | — |
| `WHEEL[7]` | `WHEEL[8]` | 双滚轮右圆弧半径 | — |
| `WHEEL[8]` | `WHEEL[9]` | 方滚轮左圆弧半径 | — |
| `WHEEL[9]` | `WHEEL[10]` | 方滚轮右圆弧半径 | — |
| `WHEEL[10]` | `WHEEL[11]` | 当前左端接触位置 | — |
| `WHEEL[11]` | `WHEEL[12]` | 当前右端接触位置 | — |
| `WHEEL[12]` | `WHEEL[13]` | 初始左端接触位置 | — |
| `WHEEL[13]` | `WHEEL[14]` | 初始右端接触位置 | — |
| `WHEEL[14]` | `WHEEL[15]` | 滚压轮接触位置 | — |
| `WHEEL[15]` | `WHEEL[16]` | 双滚轮垂直误差 | — |
| `WHEEL[16]` | `WHEEL[17]` | 液压左开关 | — |
| `WHEEL[17]` | `WHEEL[18]` | 液压右开关 | — |
| `WHEEL[18]` | `WHEEL[19]` | 成型修整轮精修停留时间 | — |
| `WHEEL[19]` | `WHEEL[20]` | 修整轮转速 | — |

<a id="pi-sec-9"></a>

### 2.9 磨削参数(GRIND)（10 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `GRIND[0]` | `GRIND[1]` | 磨削类型(0外螺纹/1内螺纹/2蜗杆/3外圆/4环形槽) | — |
| `GRIND[1]` | `GRIND[2]` | 是否修整(0否/1是) | — |
| `GRIND[2]` | `GRIND[3]` | 是否对刀(0否/1手动/2自动/3自动+手动) | — |
| `GRIND[3]` | `GRIND[4]` | 磨削循环类型 | — |
| `GRIND[4]` | `GRIND[5]` | 单次中径调整值 | — |
| `GRIND[5]` | `GRIND[6]` | 是否外圆修整(0否/1是) | — |
| `GRIND[6]` | `GRIND[7]` | 是否端面修整(0否/1是) | — |
| `GRIND[7]` | `GRIND[8]` | 当前磨削左端面/右端面(0左/1右) | — |
| `GRIND[8]` | `GRIND[9]` | 机械手是否进行测试程序(0否1是) | — |
| `GRIND[9]` | `GRIND[10]` | 启动空运行热机程序(0否1是) | — |

<a id="pi-sec-10"></a>

### 2.10 工序基本参数（130 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `PROCESS[0]` | `PROCESS[1]` | 工艺类型(0界面/1DIY) | — |
| `PROCESS[1]` | `PROCESS[2]` | 选择工艺 | — |
| `PROCESS[2]` | `PROCESS[3]` | 当前工艺 | — |
| `PROCESS[3]` | `PROCESS[4]` | 修整标记(0不修整/1修整) | — |
| `PROCESS[4]` | `PROCESS[5]` | 当前砂轮进入工件位置 | — |
| `PROCESS[5]` | `PROCESS[6]` | DIY工序计数 | — |
| `PROCESS[6]` | `PROCESS[7]` | 单双磨削 | — |
| `PROCESS[7]` | `PROCESS[8]` | 当前磨削是否修整累计 | — |
| `PROCESS[8]` | `PROCESS[9]` | 磨削进给量 | — |
| `PROCESS[9]` | `PROCESS[10]` | 磨削速度 | — |
| `PROCESS[10]` | `PROCESS[11]` | 磨削砂轮线速度 | — |
| `PROCESS[11]` | `PROCESS[12]` | 磨削工件时X进给速度 | — |
| `PROCESS[12]` | `PROCESS[13]` | 工艺设定磨削总量 | — |
| `PROCESS[13]` | `PROCESS[14]` | 初始磨削接触位置 | — |
| `PROCESS[14]` | `PROCESS[15]` | 工艺磨削总量累计 | — |
| `PROCESS[15]` | `PROCESS[16]` | 精简工艺参数/扩展工艺参数 | — |
| `PROCESS[16]` | `PROCESS[17]` | 磨削安全位置 | — |
| `PROCESS[17]` | `PROCESS[18]` | 修砂轮后是否不进刀加工一次(0否1是) 按头数修整时此设置无效 | — |

#### 磨削中心相关

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `PROCESS[18]` | `PROCESS[19]` | 外圆磨当前所在工艺 | — |
| `PROCESS[19]` | `PROCESS[20]` | 外圆磨当前循环是否修整累计 | — |
| `PROCESS[20]` | `PROCESS[21]` | 外圆磨当前接触工件位置 | — |
| `PROCESS[21]` | `PROCESS[22]` | 外圆磨程序共用进给量 | — |
| `PROCESS[22]` | `PROCESS[23]` | 外圆磨程序共用Z轴进给速度 | — |
| `PROCESS[23]` | `PROCESS[24]` | 外圆磨程序共用砂轮线速度 | — |
| `PROCESS[24]` | `PROCESS[25]` | 加工台阶一(0否1是) | — |
| `PROCESS[25]` | `PROCESS[26]` | 加工台阶二(0否1是) | — |
| `PROCESS[26]` | `PROCESS[27]` | 修砂轮后磨削标记 | — |
| `PROCESS[27]` | `PROCESS[28]` | 磨削中心:右端面磨削单面壁厚 | — |
| `PROCESS[28]` | `PROCESS[29]` | 外圆磨削是否修砂轮标志(1Y0N) | — |
| `PROCESS[29]` | `PROCESS[30]` | 外圆磨时程序执行用C轴旋转速度 | — |
| `PROCESS[30]` | `PROCESS[31]` | 外圆磨粗磨时C轴旋转速度 | — |
| `PROCESS[31]` | `PROCESS[32]` | 外圆磨半精磨时C轴旋转速度 | — |
| `PROCESS[32]` | `PROCESS[33]` | 外圆磨精磨时C轴旋转速度 | — |
| `PROCESS[33]` | `PROCESS[34]` | 外圆磨终磨时C轴旋转速度 | — |
| `PROCESS[34]` | `PROCESS[35]` | 磨削中心:左端面磨削当前接触工件位置 | — |
| `PROCESS[35]` | `PROCESS[36]` | 磨削中心:端面磨削进给速度 | — |
| `PROCESS[36]` | `PROCESS[37]` | 夹具修整：砂轮修整速度 | — |
| `PROCESS[37]` | `PROCESS[38]` | 磨削中心:右端面磨削当前接触工件位置 | — |
| `PROCESS[38]` | `PROCESS[39]` | 磨削中心:端面磨削C转速 | — |
| `PROCESS[39]` | `PROCESS[40]` | 夹具修整：夹具磨削速度 | — |
| `PROCESS[40]` | `PROCESS[41]` | 磨削中心:端面磨削进给量 | — |
| `PROCESS[41]` | `PROCESS[42]` | 磨削中心:是否磨螺纹(0否/1是) | — |
| `PROCESS[42]` | `PROCESS[43]` | 磨削中心:是否使用工艺界面(0否/1是) | — |
| `PROCESS[43]` | `PROCESS[44]` | 磨削中心:是否磨外圆(0是/1否) | — |
| `PROCESS[44]` | `PROCESS[45]` | 磨削中心:是否磨左端面(0否/1是) | — |
| `PROCESS[45]` | `PROCESS[46]` | 磨削中心:是否磨右端面(0否/1是) | — |
| `PROCESS[46]` | `PROCESS[47]` | 磨削中心:外圆磨初始接触位置 | — |
| `PROCESS[47]` | `PROCESS[48]` | 磨削中心:右端面磨削初始接触位置 | — |
| `PROCESS[48]` | `PROCESS[49]` | 磨削中心:左端面磨削初始接触位置 | — |
| `PROCESS[49]` | `PROCESS[50]` | 磨削中心:磨端面时砂轮转速 | — |
| `PROCESS[50]` | `PROCESS[51]` | 磨削中心:外磨修整器是否液压控制(0否1是) | — |
| `PROCESS[51]` | `PROCESS[52]` | 磨削中心:是否已进行过侧面修整的标记 | — |
| `PROCESS[52]` | `PROCESS[53]` | 是否有自动门(0否1是) | — |
| `PROCESS[53]` | `PROCESS[54]` | 磨削中心:测头顶部在工件中心时的X坐标 | — |
| `PROCESS[54]` | `PROCESS[55]` | 磨削中心:腰形孔缺口深度 | — |
| `PROCESS[55]` | `PROCESS[56]` | 磨削中心:外圆上台阶距左端面 | — |
| `PROCESS[56]` | `PROCESS[57]` | 当前加工台阶工序(0台阶一 1台阶二) | — |
| `PROCESS[57]` | `PROCESS[58]` | 磨削中心:外圆砂轮方向(有U轴或X轴外磨前置1/没有U轴外磨后置-1) | — |
| `PROCESS[58]` | `PROCESS[59]` | 外圆工艺磨削总量累计 | — |
| `PROCESS[59]` | `PROCESS[60]` | 外圆单双向 | — |
| `PROCESS[60]` | `PROCESS[61]` | 左端面工艺磨削总量累计 | — |
| `PROCESS[61]` | `PROCESS[62]` | 右端面工艺磨削总量累计 | — |
| `PROCESS[62]` | `PROCESS[63]` | 端面单双向 | — |
| `PROCESS[63]` | `PROCESS[64]` | 端面磨削砂轮线速度 | — |
| `PROCESS[64]` | `PROCESS[65]` | 端面磨削粗磨砂轮线速度 | — |
| `PROCESS[65]` | `PROCESS[66]` | 端面磨削精磨砂轮线速度 | — |
| `PROCESS[66]` | `PROCESS[67]` | 左端面磨削粗磨砂轮线速度 | — |
| `PROCESS[67]` | `PROCESS[68]` | 左端面磨削精磨砂轮线速度 | — |
| `PROCESS[68]` | `PROCESS[69]` | 右端面磨削粗磨砂轮线速度 | — |
| `PROCESS[69]` | `PROCESS[70]` | 右端面磨削精磨砂轮线速度 | — |
| `PROCESS[70]` | `PROCESS[71]` | 粗磨端面单双向 | — |
| `PROCESS[71]` | `PROCESS[72]` | 精磨端面单双向 | — |
| `PROCESS[72]` | `PROCESS[73]` | 左端面粗磨端面单双向 | — |
| `PROCESS[73]` | `PROCESS[74]` | 左端面精磨端面单双向 | — |
| `PROCESS[74]` | `PROCESS[75]` | 右端面粗磨端面单双向 | — |
| `PROCESS[75]` | `PROCESS[76]` | 右端面精磨端面单双向 | — |
| `PROCESS[76]` | `PROCESS[77]` | 端面磨削粗磨进给量 | — |
| `PROCESS[77]` | `PROCESS[78]` | 端面磨削精磨进给量 | — |
| `PROCESS[78]` | `PROCESS[79]` | 左端面磨削粗磨进给量 | — |
| `PROCESS[79]` | `PROCESS[80]` | 左端面磨削精磨进给量 | — |
| `PROCESS[80]` | `PROCESS[81]` | 右端面磨削粗磨进给量 | — |
| `PROCESS[81]` | `PROCESS[82]` | 右端面磨削精磨进给量 | — |
| `PROCESS[82]` | `PROCESS[83]` | 端面磨削粗磨进给速度 | — |
| `PROCESS[83]` | `PROCESS[84]` | 端面磨削精磨进给速度 | — |
| `PROCESS[84]` | `PROCESS[85]` | 左端面磨削粗磨进给速度 | — |
| `PROCESS[85]` | `PROCESS[86]` | 左端面磨削精磨进给速度 | — |
| `PROCESS[86]` | `PROCESS[87]` | 右端面磨削粗磨进给速度 | — |
| `PROCESS[87]` | `PROCESS[88]` | 右端面磨削精磨进给速度 | — |
| `PROCESS[88]` | `PROCESS[89]` | 端面磨削粗磨C转速 | — |
| `PROCESS[89]` | `PROCESS[90]` | 端面磨削精磨C转速 | — |
| `PROCESS[90]` | `PROCESS[91]` | 左端面磨削粗磨C转速 | — |
| `PROCESS[91]` | `PROCESS[92]` | 左端面磨削精磨C转速 | — |
| `PROCESS[92]` | `PROCESS[93]` | 右端面磨削粗磨C转速 | — |
| `PROCESS[93]` | `PROCESS[94]` | 右端面磨削精磨C转速 | — |
| `PROCESS[94]` | `PROCESS[95]` | 是否磨台阶 | — |
| `PROCESS[95]` | `PROCESS[96]` | 磨台阶头架转速 | — |
| `PROCESS[96]` | `PROCESS[97]` | 磨台阶粗磨头架转速 | — |
| `PROCESS[97]` | `PROCESS[98]` | 磨台阶精磨头架转速 | — |
| `PROCESS[98]` | `PROCESS[99]` | 磨台阶进刀量 | — |
| `PROCESS[99]` | `PROCESS[100]` | 磨台阶粗磨进刀量 | — |
| `PROCESS[100]` | `PROCESS[101]` | 磨台阶精磨进刀量 | — |
| `PROCESS[101]` | `PROCESS[102]` | 磨台阶速度 | — |
| `PROCESS[102]` | `PROCESS[103]` | 磨台阶粗磨速度 | — |
| `PROCESS[103]` | `PROCESS[104]` | 磨台阶精磨速度 | — |
| `PROCESS[104]` | `PROCESS[105]` | 磨台阶单双 | — |
| `PROCESS[105]` | `PROCESS[106]` | 磨台阶粗磨单双 | — |
| `PROCESS[106]` | `PROCESS[107]` | 磨台阶精磨单双 | — |
| `PROCESS[107]` | `PROCESS[108]` | 磨台阶工艺磨削量累计 | — |
| `PROCESS[108]` | `PROCESS[109]` | 磨台阶一当前磨削位置 | — |
| `PROCESS[109]` | `PROCESS[110]` | 磨台阶砂轮线速度 | — |
| `PROCESS[110]` | `PROCESS[111]` | 磨台阶粗磨砂轮线速度 | — |
| `PROCESS[111]` | `PROCESS[112]` | 磨台阶精磨砂轮线速度 | — |
| `PROCESS[112]` | `PROCESS[113]` | 退刀槽宽度 | — |
| `PROCESS[113]` | `PROCESS[114]` | 单件工艺设定总量 | — |
| `PROCESS[114]` | `PROCESS[115]` | 外圆工艺设定总量 | — |
| `PROCESS[115]` | `PROCESS[116]` | 台阶工艺设定总量 | — |
| `PROCESS[116]` | `PROCESS[117]` | 左端面工艺设定总量 | — |
| `PROCESS[117]` | `PROCESS[118]` | 右端面工艺设定总量 | — |
| `PROCESS[118]` | `PROCESS[119]` | 磨削中心只磨内螺纹时程序结束是否返回z安全位置(0返回1不返回) | — |
| `PROCESS[119]` | `PROCESS[120]` | 加工中转换动作固定快速速度 | — |
| `PROCESS[120]` | `PROCESS[121]` | 内螺纹头架防护罩自动控制(0无1有) | — |
| `PROCESS[121]` | `PROCESS[122]` | 手动对刀-非首件对刀-X轴是否直接移动到初始磨削接触(0否1是) | — |
| `PROCESS[122]` | `PROCESS[123]` | 机械手-装夹中是否检测吹气清洁卡盘(0否1是) | — |
| `PROCESS[123]` | `PROCESS[124]` | 外部连续曲线轨迹齿型高度 | — |
| `PROCESS[124]` | `PROCESS[125]` | 外部连续曲线轨迹抬刀高度 | — |
| `PROCESS[125]` | `PROCESS[126]` | 大砂轮时-磨削几件后修整 | — |
| `PROCESS[126]` | `PROCESS[127]` | 小砂轮时-磨削几件后修整 | — |
| `PROCESS[127]` | `PROCESS[128]` | 砂轮直径分界-磨削几件后修整 | — |
| `PROCESS[128]` | `PROCESS[129]` | 程序结束修整轮是否停止(0停/1不停转速保持/2不停且低速旋转) | — |
| `PROCESS[129]` | `PROCESS[130]` | 修整轮不停低速旋转转速 | — |

<a id="pi-sec-11"></a>

### 2.11 工艺表格参数（432 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `TECHNOLOGY[0]` | `TECHNOLOGY[1]` | 粗修单双磨削 | — |
| `TECHNOLOGY[1]` | `TECHNOLOGY[2]` | 半粗修单双磨削 | — |
| `TECHNOLOGY[2]` | `TECHNOLOGY[3]` | 半精修单双磨削 | — |
| `TECHNOLOGY[3]` | `TECHNOLOGY[4]` | 精修单双磨削 | — |
| `TECHNOLOGY[4]` | `TECHNOLOGY[5]` | 外圆工艺粗磨当前砂轮转速 | — |
| `TECHNOLOGY[5]` | `TECHNOLOGY[6]` | 外圆工艺半精磨当前砂轮转速 | — |
| `TECHNOLOGY[6]` | `TECHNOLOGY[7]` | 外圆工艺精磨当前砂轮转速 | — |
| `TECHNOLOGY[7]` | `TECHNOLOGY[8]` | 外圆工艺终磨当前砂轮转速 | — |
| `TECHNOLOGY[8]` | `TECHNOLOGY[9]` | 外圆修整当前砂轮转速 | — |
| `TECHNOLOGY[9]` | `TECHNOLOGY[10]` | 砂轮不停低速旋转转速 | — |
| `TECHNOLOGY[10]` | `TECHNOLOGY[11]` | 粗磨次数 | — |
| `TECHNOLOGY[11]` | `TECHNOLOGY[12]` | 半粗磨次数 | — |
| `TECHNOLOGY[12]` | `TECHNOLOGY[13]` | 半精磨次数 | — |
| `TECHNOLOGY[13]` | `TECHNOLOGY[14]` | 精磨次数 | — |
| `TECHNOLOGY[14]` | `TECHNOLOGY[15]` | 台阶粗磨当前砂轮转速 | — |
| `TECHNOLOGY[15]` | `TECHNOLOGY[16]` | 台阶精磨当前砂轮转速 | — |
| `TECHNOLOGY[16]` | `TECHNOLOGY[17]` | 单件粗磨砂轮转速 | — |
| `TECHNOLOGY[17]` | `TECHNOLOGY[18]` | 单件半粗磨砂轮转速 | — |
| `TECHNOLOGY[18]` | `TECHNOLOGY[19]` | 单件精磨砂轮转速 | — |
| `TECHNOLOGY[19]` | `TECHNOLOGY[20]` | 单件终磨砂轮转速 | — |
| `TECHNOLOGY[20]` | `TECHNOLOGY[21]` | 粗磨进给量 | — |
| `TECHNOLOGY[21]` | `TECHNOLOGY[22]` | 半粗磨进给量 | — |
| `TECHNOLOGY[22]` | `TECHNOLOGY[23]` | 半精磨进给量 | — |
| `TECHNOLOGY[23]` | `TECHNOLOGY[24]` | 精磨进给量 | — |
| `TECHNOLOGY[24]` | `TECHNOLOGY[25]` | 扩展单件粗磨修整砂轮转速 | — |
| `TECHNOLOGY[25]` | `TECHNOLOGY[26]` | 扩展单件半粗磨修整砂轮转速 | — |
| `TECHNOLOGY[26]` | `TECHNOLOGY[27]` | 扩展单件精磨修整砂轮转速 | — |
| `TECHNOLOGY[27]` | `TECHNOLOGY[28]` | 扩展单件终磨修整砂轮转速 | — |
| `TECHNOLOGY[28]` | `TECHNOLOGY[29]` | 高速移动缓冲距离 | — |
| `TECHNOLOGY[29]` | `TECHNOLOGY[30]` | 高速移动缓冲启动速度 | — |
| `TECHNOLOGY[30]` | `TECHNOLOGY[31]` | 粗磨速度 | — |
| `TECHNOLOGY[31]` | `TECHNOLOGY[32]` | 半粗磨速度 | — |
| `TECHNOLOGY[32]` | `TECHNOLOGY[33]` | 半精磨速度 | — |
| `TECHNOLOGY[33]` | `TECHNOLOGY[34]` | 精磨速度 | — |
| `TECHNOLOGY[34]` | `TECHNOLOGY[35]` | 空运行热机-自动卡盘动作(0否1是) | — |
| `TECHNOLOGY[35]` | `TECHNOLOGY[36]` | 空运行热机-Z轴正向起始位置 | — |
| `TECHNOLOGY[36]` | `TECHNOLOGY[37]` | 台阶一磨削初始位选择(0外圆当前接触/1外圆初始接触) | — |
| `TECHNOLOGY[37]` | `TECHNOLOGY[38]` | 外圆磨削完成后是否直接磨削左端面(0否1是) | — |
| `TECHNOLOGY[38]` | `TECHNOLOGY[39]` | 空运行热机-Z轴负向终止位置 | — |
| `TECHNOLOGY[39]` | `TECHNOLOGY[40]` | 空运行热机-X轴后方起始位置 | — |
| `TECHNOLOGY[40]` | `TECHNOLOGY[41]` | 粗磨是否修整累计 | — |
| `TECHNOLOGY[41]` | `TECHNOLOGY[42]` | 半粗磨是否修整累计 | — |
| `TECHNOLOGY[42]` | `TECHNOLOGY[43]` | 半精磨是否修整累计 | — |
| `TECHNOLOGY[43]` | `TECHNOLOGY[44]` | 精磨是否修整累计 | — |
| `TECHNOLOGY[44]` | `TECHNOLOGY[45]` | 外圆磨削终点补偿距离 | — |
| `TECHNOLOGY[45]` | `TECHNOLOGY[46]` | 左端面磨削终点补偿距离 | — |
| `TECHNOLOGY[46]` | `TECHNOLOGY[47]` | 右端面磨削终点补偿距离 | — |
| `TECHNOLOGY[47]` | `TECHNOLOGY[48]` | 台阶磨削终点补偿距离 | — |
| `TECHNOLOGY[48]` | `TECHNOLOGY[49]` | 空运行热机-X轴前方终止位置 | — |
| `TECHNOLOGY[49]` | `TECHNOLOGY[50]` | 空运行热机-砂轮转速 | — |
| `TECHNOLOGY[50]` | `TECHNOLOGY[51]` | 磨削砂轮线速度 | — |
| `TECHNOLOGY[51]` | `TECHNOLOGY[52]` | 磨削砂轮线速度 | — |
| `TECHNOLOGY[52]` | `TECHNOLOGY[53]` | 磨削砂轮线速度 | — |
| `TECHNOLOGY[53]` | `TECHNOLOGY[54]` | 磨削砂轮线速度 | — |
| `TECHNOLOGY[54]` | `TECHNOLOGY[55]` | 空运行热机-运行中轴速度 | — |
| `TECHNOLOGY[55]` | `TECHNOLOGY[56]` | 空运行热机-界面按钮开启(0否1是) | — |
| `TECHNOLOGY[56]` | `TECHNOLOGY[57]` | 参数备份恢复界面可开启(0否1是) | — |
| `TECHNOLOGY[57]` | `TECHNOLOGY[58]` | 加工统计界面可开启(0否1是) | — |
| `TECHNOLOGY[58]` | `TECHNOLOGY[59]` | 新砂轮是否是成型砂轮界面参数显示(0隐藏1显示) | — |
| `TECHNOLOGY[59]` | `TECHNOLOGY[60]` | 自动门选择(自动门1/自动门2) | — |
| `TECHNOLOGY[60]` | `TECHNOLOGY[61]` | 粗磨头架转速 | — |
| `TECHNOLOGY[61]` | `TECHNOLOGY[62]` | 半粗磨头架转速 | — |
| `TECHNOLOGY[62]` | `TECHNOLOGY[63]` | 精磨头架转速 | — |
| `TECHNOLOGY[63]` | `TECHNOLOGY[64]` | 终磨头架转速 | — |
| `TECHNOLOGY[64]` | `TECHNOLOGY[65]` | 自动门是否检测开关信号(0不检测/1检测) | — |
| `TECHNOLOGY[65]` | `TECHNOLOGY[66]` | 内螺纹左旋从工件左侧加工(0否1是) | — |
| `TECHNOLOGY[66]` | `TECHNOLOGY[67]` | 空运行热机-自动开冷却水(0否1是) | — |
| `TECHNOLOGY[67]` | `TECHNOLOGY[68]` | 内螺纹反向孔倒角-第二滚道起点z偏移-基准直径(小于此直径调用基准偏移) | — |
| `TECHNOLOGY[68]` | `TECHNOLOGY[69]` | 内螺纹反向孔倒角-第二滚道起点z偏移-基准偏移 | — |
| `TECHNOLOGY[69]` | `TECHNOLOGY[70]` | 内螺纹反向孔倒角-第二滚道起点z偏移-直径补偿(直径每大1mm偏移补偿量) | — |
| `TECHNOLOGY[70]` | `TECHNOLOGY[71]` | 批量粗磨砂轮转速 | — |
| `TECHNOLOGY[71]` | `TECHNOLOGY[72]` | 批量半粗磨砂轮转速 | — |
| `TECHNOLOGY[72]` | `TECHNOLOGY[73]` | 批量精磨砂轮转速 | — |
| `TECHNOLOGY[73]` | `TECHNOLOGY[74]` | 批量终磨砂轮转速 | — |
| `TECHNOLOGY[74]` | `TECHNOLOGY[75]` | 批量粗磨修整砂轮转速 | — |
| `TECHNOLOGY[75]` | `TECHNOLOGY[76]` | 批量半粗磨修整砂轮转速 | — |
| `TECHNOLOGY[76]` | `TECHNOLOGY[77]` | 批量精磨修整砂轮转速 | — |
| `TECHNOLOGY[77]` | `TECHNOLOGY[78]` | 批量终磨修整砂轮转速 | — |
| `TECHNOLOGY[78]` | `TECHNOLOGY[79]` | 外圆磨粗磨次数 | — |
| `TECHNOLOGY[79]` | `TECHNOLOGY[80]` | 外圆磨粗磨几次修砂轮设定 | — |
| `TECHNOLOGY[80]` | `TECHNOLOGY[81]` | 外圆磨粗磨进给量 | — |
| `TECHNOLOGY[81]` | `TECHNOLOGY[82]` | 外圆磨粗磨进给速度 | — |
| `TECHNOLOGY[82]` | `TECHNOLOGY[83]` | 外圆磨粗磨砂轮线速度 | — |
| `TECHNOLOGY[83]` | `TECHNOLOGY[84]` | 外圆磨半精磨次数 | — |
| `TECHNOLOGY[84]` | `TECHNOLOGY[85]` | 外圆磨半精磨几次修砂轮设定 | — |
| `TECHNOLOGY[85]` | `TECHNOLOGY[86]` | 外圆磨半精磨进给量 | — |
| `TECHNOLOGY[86]` | `TECHNOLOGY[87]` | 外圆磨半精磨进给速度 | — |
| `TECHNOLOGY[87]` | `TECHNOLOGY[88]` | 外圆磨半精磨砂轮线速度 | — |
| `TECHNOLOGY[88]` | `TECHNOLOGY[89]` | 外圆磨精磨次数 | — |
| `TECHNOLOGY[89]` | `TECHNOLOGY[90]` | 外圆磨精磨几次修砂轮设定 | — |
| `TECHNOLOGY[90]` | `TECHNOLOGY[91]` | 外圆磨精磨进给量 | — |
| `TECHNOLOGY[91]` | `TECHNOLOGY[92]` | 外圆磨精磨进给速度 | — |
| `TECHNOLOGY[92]` | `TECHNOLOGY[93]` | 外圆磨精磨砂轮线速度 | — |
| `TECHNOLOGY[93]` | `TECHNOLOGY[94]` | 外圆磨终磨次数 | — |
| `TECHNOLOGY[94]` | `TECHNOLOGY[95]` | 外圆磨终磨几次修砂轮设定 | — |
| `TECHNOLOGY[95]` | `TECHNOLOGY[96]` | 外圆磨终磨进给量 | — |
| `TECHNOLOGY[96]` | `TECHNOLOGY[97]` | 外圆磨终磨进给速度 | — |
| `TECHNOLOGY[97]` | `TECHNOLOGY[98]` | 外圆磨终磨砂轮线速度 | — |
| `TECHNOLOGY[98]` | `TECHNOLOGY[99]` | 磨削中心:端面磨削粗磨已磨削次数 | — |
| `TECHNOLOGY[99]` | `TECHNOLOGY[100]` | 磨削中心:左端面磨削粗磨设定磨削次数 | — |
| `TECHNOLOGY[100]` | `TECHNOLOGY[101]` | 磨削中心:端面磨削粗磨已磨削次数 | — |
| `TECHNOLOGY[101]` | `TECHNOLOGY[102]` | 磨削中心:右端面磨削粗磨设定磨削次数 | — |
| `TECHNOLOGY[102]` | `TECHNOLOGY[103]` | 磨削中心:右端面磨削砂轮线速度 | — |
| `TECHNOLOGY[103]` | `TECHNOLOGY[104]` | 磨削中心:右端面磨削量累计 | — |
| `TECHNOLOGY[104]` | `TECHNOLOGY[105]` | 磨削中心:左端面磨削量累计 | — |
| `TECHNOLOGY[105]` | `TECHNOLOGY[106]` | 磨削中心:右端面磨削几个循环调用修整程序 | — |
| `TECHNOLOGY[106]` | `TECHNOLOGY[107]` | 磨削中心:端面磨削中修整次数 | — |
| `TECHNOLOGY[107]` | `TECHNOLOGY[108]` | 按头数计数修整-头数磨削累计计数(此数值循环中不清零，可跨循环次数及工序计数) | — |
| `TECHNOLOGY[108]` | `TECHNOLOGY[109]` | 螺纹两端变径磨削-界面开启(0隐藏/1开启) | — |
| `TECHNOLOGY[109]` | `TECHNOLOGY[110]` | 螺纹两端变径磨削-使能(0不变/1变) | — |
| `TECHNOLOGY[110]` | `TECHNOLOGY[111]` | 批量磨削粗修单双磨削 | — |
| `TECHNOLOGY[111]` | `TECHNOLOGY[112]` | 批量磨削半粗修单双磨削 | — |
| `TECHNOLOGY[112]` | `TECHNOLOGY[113]` | 批量磨削半精修单双磨削 | — |
| `TECHNOLOGY[113]` | `TECHNOLOGY[114]` | 批量磨削精修单双磨削 | — |
| `TECHNOLOGY[114]` | `TECHNOLOGY[115]` | 螺纹两端变径磨削-右端变径量(正值向后退刀) | — |
| `TECHNOLOGY[115]` | `TECHNOLOGY[116]` | 螺纹两端变径磨削-右端变径过渡角度(大于0) | — |
| `TECHNOLOGY[116]` | `TECHNOLOGY[117]` | 螺纹两端变径磨削--左端变径量(正值向前进刀) | — |
| `TECHNOLOGY[117]` | `TECHNOLOGY[118]` | 螺纹两端变径磨削--左端变径过渡角度(大于0) | — |
| `TECHNOLOGY[118]` | `TECHNOLOGY[119]` | 粗磨进刀量是否梯度变化(0否1是) - 当总变化量大于设定进刀量的两倍时不梯度进刀 | — |
| `TECHNOLOGY[119]` | `TECHNOLOGY[120]` | 粗磨或半精磨进刀量梯度总变化量(第一刀和最后一刀差值) | — |
| `TECHNOLOGY[120]` | `TECHNOLOGY[121]` | 批量磨削粗磨次数 | — |
| `TECHNOLOGY[121]` | `TECHNOLOGY[122]` | 批量磨削半粗磨次数 | — |
| `TECHNOLOGY[122]` | `TECHNOLOGY[123]` | 批量磨削半精磨次数 | — |
| `TECHNOLOGY[123]` | `TECHNOLOGY[124]` | 批量磨削精磨次数 | — |
| `TECHNOLOGY[124]` | `TECHNOLOGY[125]` | 半精磨进刀量是否梯度变化(0否1是) - 当总变化量大于设定进刀量的两倍时不梯度进刀 | — |
| `TECHNOLOGY[125]` | `TECHNOLOGY[126]` | 多头磨削时每头进刀位置是否补偿(0否1是) 最多补偿6头 | — |
| `TECHNOLOGY[126]` | `TECHNOLOGY[127]` | 工艺界面附加配置界面显示(0隐藏1显示) 进刀量梯度变化 每头进刀位置补偿 | — |
| `TECHNOLOGY[127]` | `TECHNOLOGY[128]` | 内螺纹自动对刀-测量模式选择(0测量反向孔/1测量右端小台阶/2测量右端定位孔/3测量外圆直线及右端面内壁) | — |
| `TECHNOLOGY[128]` | `TECHNOLOGY[129]` | 内螺纹自动对刀-是否可选测量右端面小台阶(0否1是) | — |
| `TECHNOLOGY[129]` | `TECHNOLOGY[130]` | 外螺纹-磨削安全后退距离(相对初始磨削接触位) | — |
| `TECHNOLOGY[130]` | `TECHNOLOGY[131]` | 批量磨削粗磨进给量 | — |
| `TECHNOLOGY[131]` | `TECHNOLOGY[132]` | 批量磨削半粗磨进给量 | — |
| `TECHNOLOGY[132]` | `TECHNOLOGY[133]` | 批量磨削半精磨进给量 | — |
| `TECHNOLOGY[133]` | `TECHNOLOGY[134]` | 批量磨削精磨进给量 | — |
| `TECHNOLOGY[134]` | `TECHNOLOGY[135]` | 修整轮生命周期统计界面显示(0不显示1显示) | — |
| `TECHNOLOGY[135]` | `TECHNOLOGY[136]` | 修整轮修整生命周期次数设置 | — |
| `TECHNOLOGY[136]` | `TECHNOLOGY[137]` | 修整轮修整次数累计 | — |
| `TECHNOLOGY[137]` | `TECHNOLOGY[138]` | 修整轮修整量累计 | — |
| `TECHNOLOGY[138]` | `TECHNOLOGY[139]` | 螺纹两端变径磨削-右端变径无效牙角度(大于0) | — |
| `TECHNOLOGY[139]` | `TECHNOLOGY[140]` | 螺纹两端变径磨削-左端变径无效牙角度(大于0) | — |
| `TECHNOLOGY[140]` | `TECHNOLOGY[141]` | 批量磨削粗磨速度 | — |
| `TECHNOLOGY[141]` | `TECHNOLOGY[142]` | 批量磨削半粗磨速度 | — |
| `TECHNOLOGY[142]` | `TECHNOLOGY[143]` | 批量磨削半精磨速度 | — |
| `TECHNOLOGY[143]` | `TECHNOLOGY[144]` | 批量磨削精磨速度 | — |
| `TECHNOLOGY[144]` | `TECHNOLOGY[145]` | 多头磨削时每头进刀位置补偿.X-第1头 | — |
| `TECHNOLOGY[145]` | `TECHNOLOGY[146]` | 多头磨削时每头进刀位置补偿.X-第2头 | — |
| `TECHNOLOGY[146]` | `TECHNOLOGY[147]` | 多头磨削时每头进刀位置补偿.X-第3头 | — |
| `TECHNOLOGY[147]` | `TECHNOLOGY[148]` | 多头磨削时每头进刀位置补偿.X-第4头 | — |
| `TECHNOLOGY[148]` | `TECHNOLOGY[149]` | 多头磨削时每头进刀位置补偿.X-第5头 | — |
| `TECHNOLOGY[149]` | `TECHNOLOGY[150]` | 多头磨削时每头进刀位置补偿.X-第6头 | — |
| `TECHNOLOGY[150]` | `TECHNOLOGY[151]` | 批量磨削粗磨是否修整累计 | — |
| `TECHNOLOGY[151]` | `TECHNOLOGY[152]` | 批量磨削半粗磨是否修整累计 | — |
| `TECHNOLOGY[152]` | `TECHNOLOGY[153]` | 批量磨削半精磨是否修整累计 | — |
| `TECHNOLOGY[153]` | `TECHNOLOGY[154]` | 批量磨削精磨是否修整累计 | — |
| `TECHNOLOGY[154]` | `TECHNOLOGY[155]` | 螺纹两端变径磨削-无效牙位置(0平顺加工/1等大加工) | — |
| `TECHNOLOGY[155]` | `TECHNOLOGY[156]` | 自动对刀-测量反向孔-伸入孔检测一定角度范围(0否1是) | — |
| `TECHNOLOGY[156]` | `TECHNOLOGY[157]` | 自动对刀-测量反向孔-伸入孔检测角度范围大小(大于0) | — |
| `TECHNOLOGY[157]` | `TECHNOLOGY[158]` | 自动对刀-测量反向孔-伸入孔检测每次移动角度(大于0) | — |
| `TECHNOLOGY[158]` | `TECHNOLOGY[159]` | 自动对刀-内螺纹-测量方式选择(0开关1测头) | — |
| `TECHNOLOGY[159]` | `TECHNOLOGY[160]` | 工艺界面头架转速设置限制值(默认0表示限制为60转) | — |
| `TECHNOLOGY[160]` | `TECHNOLOGY[161]` | 批量磨削磨削砂轮线速度 | — |
| `TECHNOLOGY[161]` | `TECHNOLOGY[162]` | 批量磨削磨削砂轮线速度 | — |
| `TECHNOLOGY[162]` | `TECHNOLOGY[163]` | 批量磨削磨削砂轮线速度 | — |
| `TECHNOLOGY[163]` | `TECHNOLOGY[164]` | 批量磨削磨削砂轮线速度 | — |
| `TECHNOLOGY[164]` | `TECHNOLOGY[165]` | 环形槽-第1组-槽升量 | — |
| `TECHNOLOGY[165]` | `TECHNOLOGY[166]` | 环形槽-第2组-槽升量 | — |
| `TECHNOLOGY[166]` | `TECHNOLOGY[167]` | 环形槽-第3组-槽升量 | — |
| `TECHNOLOGY[167]` | `TECHNOLOGY[168]` | 环形槽-第4组-槽升量 | — |
| `TECHNOLOGY[168]` | `TECHNOLOGY[169]` | 外螺纹左旋从工件右侧加工(0否1是) | — |
| `TECHNOLOGY[169]` | `TECHNOLOGY[170]` | 有机械手时-卡盘夹紧松开延时时间 | — |
| `TECHNOLOGY[170]` | `TECHNOLOGY[171]` | 单件磨削粗修单双磨削 | — |
| `TECHNOLOGY[171]` | `TECHNOLOGY[172]` | 单件磨削半粗修单双磨削 | — |
| `TECHNOLOGY[172]` | `TECHNOLOGY[173]` | 单件磨削半精修单双磨削 | — |
| `TECHNOLOGY[173]` | `TECHNOLOGY[174]` | 单件磨削精修单双磨削 | — |
| `TECHNOLOGY[174]` | `TECHNOLOGY[175]` | 丝锥-粗磨不铲磨(0否1是) | — |
| `TECHNOLOGY[175]` | `TECHNOLOGY[176]` | 磨削中心-自动对刀-测量内滚道模式-是否测量右端面(0否1是) | — |
| `TECHNOLOGY[176]` | `TECHNOLOGY[177]` | 内螺纹自动对刀-开关测量-测量起始位.x | — |
| `TECHNOLOGY[177]` | `TECHNOLOGY[178]` | 磨削中心-台阶二当前磨削位置 | — |
| `TECHNOLOGY[178]` | `TECHNOLOGY[179]` | 磨削中心-台阶二距离台阶一Z距离 | — |
| `TECHNOLOGY[179]` | `TECHNOLOGY[180]` | 磨削中心-台阶二终点补偿 | — |
| `TECHNOLOGY[180]` | `TECHNOLOGY[181]` | 单件磨削粗磨次数 | — |
| `TECHNOLOGY[181]` | `TECHNOLOGY[182]` | 单件磨削半粗磨次数 | — |
| `TECHNOLOGY[182]` | `TECHNOLOGY[183]` | 单件磨削半精磨次数 | — |
| `TECHNOLOGY[183]` | `TECHNOLOGY[184]` | 单件磨削精磨次数 | — |
| `TECHNOLOGY[184]` | `TECHNOLOGY[185]` | 台阶二磨削初始位选择(0台阶一当前接触/1台阶一初始接触) | — |
| `TECHNOLOGY[185]` | `TECHNOLOGY[186]` | 台阶二台阶长度 | — |
| `TECHNOLOGY[186]` | `TECHNOLOGY[187]` | 台阶二保持分段设置 | — |
| `TECHNOLOGY[187]` | `TECHNOLOGY[188]` | 台阶一粗磨磨削方式 | — |
| `TECHNOLOGY[188]` | `TECHNOLOGY[189]` | 台阶一粗磨磨削次数 | — |
| `TECHNOLOGY[189]` | `TECHNOLOGY[190]` | 台阶一粗磨进给深度 | — |
| `TECHNOLOGY[190]` | `TECHNOLOGY[191]` | 单件磨削粗磨进给量 | — |
| `TECHNOLOGY[191]` | `TECHNOLOGY[192]` | 单件磨削半粗磨进给量 | — |
| `TECHNOLOGY[192]` | `TECHNOLOGY[193]` | 单件磨削半精磨进给量 | — |
| `TECHNOLOGY[193]` | `TECHNOLOGY[194]` | 单件磨削精磨进给量 | — |
| `TECHNOLOGY[194]` | `TECHNOLOGY[195]` | 台阶一粗磨磨削速度 | — |
| `TECHNOLOGY[195]` | `TECHNOLOGY[196]` | 台阶一粗磨砂轮线速度 | — |
| `TECHNOLOGY[196]` | `TECHNOLOGY[197]` | 台阶一粗磨头架转速 | — |
| `TECHNOLOGY[197]` | `TECHNOLOGY[198]` | 台阶一粗磨砂轮转速 | — |
| `TECHNOLOGY[198]` | `TECHNOLOGY[199]` | 台阶一精磨磨削方式 | — |
| `TECHNOLOGY[199]` | `TECHNOLOGY[200]` | 台阶一精磨磨削次数 | — |
| `TECHNOLOGY[200]` | `TECHNOLOGY[201]` | 单件磨削粗磨速度 | — |
| `TECHNOLOGY[201]` | `TECHNOLOGY[202]` | 单件磨削半粗磨速度 | — |
| `TECHNOLOGY[202]` | `TECHNOLOGY[203]` | 单件磨削半精磨速度 | — |
| `TECHNOLOGY[203]` | `TECHNOLOGY[204]` | 单件磨削精磨速度 | — |
| `TECHNOLOGY[204]` | `TECHNOLOGY[205]` | 台阶一精磨进给深度 | — |
| `TECHNOLOGY[205]` | `TECHNOLOGY[206]` | 台阶一精磨磨削速度 | — |
| `TECHNOLOGY[206]` | `TECHNOLOGY[207]` | 台阶一精磨砂轮线速度 | — |
| `TECHNOLOGY[207]` | `TECHNOLOGY[208]` | 台阶一精磨头架转速 | — |
| `TECHNOLOGY[208]` | `TECHNOLOGY[209]` | 台阶一精磨砂轮转速 | — |
| `TECHNOLOGY[209]` | `TECHNOLOGY[210]` | 台阶二粗磨磨削方式 | — |
| `TECHNOLOGY[210]` | `TECHNOLOGY[211]` | 单件磨削粗磨是否修整累计 | — |
| `TECHNOLOGY[211]` | `TECHNOLOGY[212]` | 单件磨削半粗磨是否修整累计 | — |
| `TECHNOLOGY[212]` | `TECHNOLOGY[213]` | 单件磨削半精磨是否修整累计 | — |
| `TECHNOLOGY[213]` | `TECHNOLOGY[214]` | 单件磨削精磨是否修整累计 | — |
| `TECHNOLOGY[214]` | `TECHNOLOGY[215]` | 台阶二粗磨磨削次数 | — |
| `TECHNOLOGY[215]` | `TECHNOLOGY[216]` | 台阶二粗磨进给深度 | — |
| `TECHNOLOGY[216]` | `TECHNOLOGY[217]` | 台阶二粗磨磨削速度 | — |
| `TECHNOLOGY[217]` | `TECHNOLOGY[218]` | 台阶二粗磨砂轮线速度 | — |
| `TECHNOLOGY[218]` | `TECHNOLOGY[219]` | 台阶二粗磨头架转速 | — |
| `TECHNOLOGY[219]` | `TECHNOLOGY[220]` | 台阶二粗磨砂轮转速 | — |
| `TECHNOLOGY[220]` | `TECHNOLOGY[221]` | 单件磨削磨削砂轮线速度 | — |
| `TECHNOLOGY[221]` | `TECHNOLOGY[222]` | 单件磨削磨削砂轮线速度 | — |
| `TECHNOLOGY[222]` | `TECHNOLOGY[223]` | 单件磨削磨削砂轮线速度 | — |
| `TECHNOLOGY[223]` | `TECHNOLOGY[224]` | 单件磨削磨削砂轮线速度 | — |
| `TECHNOLOGY[224]` | `TECHNOLOGY[225]` | 台阶二精磨磨削方式 | — |
| `TECHNOLOGY[225]` | `TECHNOLOGY[226]` | 台阶二精磨磨削次数 | — |
| `TECHNOLOGY[226]` | `TECHNOLOGY[227]` | 台阶二精磨进给深度 | — |
| `TECHNOLOGY[227]` | `TECHNOLOGY[228]` | 台阶二精磨磨削速度 | — |
| `TECHNOLOGY[228]` | `TECHNOLOGY[229]` | 台阶二精磨砂轮线速度 | — |
| `TECHNOLOGY[229]` | `TECHNOLOGY[230]` | 台阶二精磨头架转速 | — |
| `TECHNOLOGY[230]` | `TECHNOLOGY[231]` | 磨削中心外圆/端面加工头架旋转方向(0正转/1反转) | — |
| `TECHNOLOGY[231]` | `TECHNOLOGY[232]` | 夹具修整：夹具磨削头架转速 | — |
| `TECHNOLOGY[232]` | `TECHNOLOGY[233]` | 自磨夹具界面隐藏(0隐藏/1开启) | — |
| `TECHNOLOGY[233]` | `TECHNOLOGY[234]` | 粗磨自动计算(0否1是) | — |
| `TECHNOLOGY[234]` | `TECHNOLOGY[235]` | 内螺纹螺旋退出方式(0退到中心/1后退固定距离) | — |
| `TECHNOLOGY[235]` | `TECHNOLOGY[236]` | 内螺纹螺旋退出方式为后退固定距离时的距离 | — |
| `TECHNOLOGY[236]` | `TECHNOLOGY[237]` | 台阶二精磨砂轮转速 | — |
| `TECHNOLOGY[237]` | `TECHNOLOGY[238]` | 反向孔倒角-倒角两端预倒角角度 | — |
| `TECHNOLOGY[238]` | `TECHNOLOGY[239]` | 反向孔倒角-倒角两端预倒角深度 | — |
| `TECHNOLOGY[239]` | `TECHNOLOGY[240]` | 外圆粗磨单双磨削 | — |
| `TECHNOLOGY[240]` | `TECHNOLOGY[241]` | 外圆半精磨单双磨削 | — |
| `TECHNOLOGY[241]` | `TECHNOLOGY[242]` | 外圆精修单双磨削 | — |
| `TECHNOLOGY[242]` | `TECHNOLOGY[243]` | 外圆终磨单双磨削 | — |
| `TECHNOLOGY[243]` | `TECHNOLOGY[244]` | 磨削中心:左端面磨削精磨设定磨削次数 | — |
| `TECHNOLOGY[244]` | `TECHNOLOGY[245]` | 磨削中心:右端面磨削精磨设定磨削次数 | — |
| `TECHNOLOGY[245]` | `TECHNOLOGY[246]` | 磨削中心:当前端面磨削精磨设定磨削次数 | — |
| `TECHNOLOGY[246]` | `TECHNOLOGY[247]` | 磨削中心:当前端面磨削粗磨设定磨削次数 | — |
| `TECHNOLOGY[247]` | `TECHNOLOGY[248]` | 端面粗磨磨削中修整次数 | — |
| `TECHNOLOGY[248]` | `TECHNOLOGY[249]` | 端面精磨磨削中修整次数 | — |
| `TECHNOLOGY[249]` | `TECHNOLOGY[250]` | 左端面粗磨磨削中修整次数 | — |
| `TECHNOLOGY[250]` | `TECHNOLOGY[251]` | 左端面精磨磨削中修整次数 | — |
| `TECHNOLOGY[251]` | `TECHNOLOGY[252]` | 右端面粗磨磨削中修整次数 | — |
| `TECHNOLOGY[252]` | `TECHNOLOGY[253]` | 右端面精磨磨削中修整次数 | — |
| `TECHNOLOGY[253]` | `TECHNOLOGY[254]` | 端面粗磨磨削中修整设定 | — |
| `TECHNOLOGY[254]` | `TECHNOLOGY[255]` | 端面精磨磨削中修整设定 | — |
| `TECHNOLOGY[255]` | `TECHNOLOGY[256]` | 左端面粗磨磨削中修整设定 | — |
| `TECHNOLOGY[256]` | `TECHNOLOGY[257]` | 左端面精磨磨削中修整设定 | — |
| `TECHNOLOGY[257]` | `TECHNOLOGY[258]` | 右端面粗磨磨削中修整设定 | — |
| `TECHNOLOGY[258]` | `TECHNOLOGY[259]` | 右端面精磨磨削中修整设定 | — |
| `TECHNOLOGY[259]` | `TECHNOLOGY[260]` | 界面左端面工艺粗磨当前砂轮转速 | — |
| `TECHNOLOGY[260]` | `TECHNOLOGY[261]` | 界面左端面工艺精磨当前砂轮转速 | — |
| `TECHNOLOGY[261]` | `TECHNOLOGY[262]` | 界面右端面工艺粗磨当前砂轮转速 | — |
| `TECHNOLOGY[262]` | `TECHNOLOGY[263]` | 界面右端面工艺精磨当前砂轮转速 | — |
| `TECHNOLOGY[263]` | `TECHNOLOGY[264]` | 当前台阶粗磨次数 | — |
| `TECHNOLOGY[264]` | `TECHNOLOGY[265]` | 当前台阶精磨次数 | — |
| `TECHNOLOGY[265]` | `TECHNOLOGY[266]` | 初始台阶粗磨次数 | — |
| `TECHNOLOGY[266]` | `TECHNOLOGY[267]` | 初始台阶精磨次数 | — |
| `TECHNOLOGY[267]` | `TECHNOLOGY[268]` | 单件粗磨头架转速 | — |
| `TECHNOLOGY[268]` | `TECHNOLOGY[269]` | 单件半粗磨头架转速 | — |
| `TECHNOLOGY[269]` | `TECHNOLOGY[270]` | 单件精磨头架转速 | — |
| `TECHNOLOGY[270]` | `TECHNOLOGY[271]` | 单件终磨头架转速 | — |
| `TECHNOLOGY[271]` | `TECHNOLOGY[272]` | 倒角1终点:X向补偿 | — |
| `TECHNOLOGY[272]` | `TECHNOLOGY[273]` | 倒角2终点:X向补偿 | — |
| `TECHNOLOGY[273]` | `TECHNOLOGY[274]` | 倒角3终点:X向补偿 | — |
| `TECHNOLOGY[274]` | `TECHNOLOGY[275]` | 倒角4终点:X向补偿 | — |
| `TECHNOLOGY[275]` | `TECHNOLOGY[276]` | 倒角5终点:X向补偿 | — |
| `TECHNOLOGY[276]` | `TECHNOLOGY[277]` | 倒角6终点:X向补偿 | — |
| `TECHNOLOGY[277]` | `TECHNOLOGY[278]` | 倒角7终点:X向补偿 | — |
| `TECHNOLOGY[278]` | `TECHNOLOGY[279]` | 倒角8终点:X向补偿 | — |
| `TECHNOLOGY[279]` | `TECHNOLOGY[280]` | 倒角9终点:X向补偿 | — |
| `TECHNOLOGY[280]` | `TECHNOLOGY[281]` | 倒角10终点:X向补偿 | — |
| `TECHNOLOGY[281]` | `TECHNOLOGY[282]` | 倒角11终点:X向补偿 | — |
| `TECHNOLOGY[282]` | `TECHNOLOGY[283]` | 倒角12终点:X向补偿 | — |
| `TECHNOLOGY[283]` | `TECHNOLOGY[284]` | 倒角13终点:X向补偿 | — |
| `TECHNOLOGY[284]` | `TECHNOLOGY[285]` | 倒角14终点:X向补偿 | — |
| `TECHNOLOGY[285]` | `TECHNOLOGY[286]` | 倒角15终点:X向补偿 | — |
| `TECHNOLOGY[286]` | `TECHNOLOGY[287]` | 倒角16终点:X向补偿 | — |
| `TECHNOLOGY[287]` | `TECHNOLOGY[288]` | 倒角17终点:X向补偿 | — |
| `TECHNOLOGY[288]` | `TECHNOLOGY[289]` | 倒角18终点:X向补偿 | — |
| `TECHNOLOGY[289]` | `TECHNOLOGY[290]` | 倒角19终点:X向补偿 | — |
| `TECHNOLOGY[290]` | `TECHNOLOGY[291]` | 倒角20终点:X向补偿 | — |
| `TECHNOLOGY[291]` | `TECHNOLOGY[292]` | 倒角终点X向补偿参数是否显示(0否1是) | — |
| `TECHNOLOGY[292]` | `TECHNOLOGY[293]` | 倒角终点X向补偿模式(0倒角结束直接补偿/1倒角结束到下一倒角开始渐变补偿) | — |
| `TECHNOLOGY[293]` | `TECHNOLOGY[294]` | 粗磨消空程使能(0否1是) | — |
| `TECHNOLOGY[294]` | `TECHNOLOGY[295]` | 粗磨消空程-空行程粗磨头架转速 | — |
| `TECHNOLOGY[295]` | `TECHNOLOGY[296]` | 外圆在线测量使能(0否1是) | — |
| `TECHNOLOGY[296]` | `TECHNOLOGY[297]` | 磨削中心-外圆磨削补偿 | — |
| `TECHNOLOGY[297]` | `TECHNOLOGY[298]` | 磨削中心-左端面磨削补偿 | — |
| `TECHNOLOGY[298]` | `TECHNOLOGY[299]` | 磨削中心-右端面磨削补偿 | — |
| `TECHNOLOGY[299]` | `TECHNOLOGY[300]` | 断电回退使能(0否1是) | — |
| `TECHNOLOGY[300]` | `TECHNOLOGY[301]` | 变径磨削-平滑轨迹使能(0否1是) | — |
| `TECHNOLOGY[301]` | `TECHNOLOGY[302]` | 变螺距-平滑轨迹使能(0否1是) | — |
| `TECHNOLOGY[302]` | `TECHNOLOGY[303]` | 砂轮修整-新砂轮轮廓部分是否单独修整参数(0否1是) | — |
| `TECHNOLOGY[303]` | `TECHNOLOGY[304]` | 砂轮修整-新砂轮轮廓部分单独参数修整量 | — |
| `TECHNOLOGY[304]` | `TECHNOLOGY[305]` | 砂轮修整-新砂轮轮廓部分单独参数修整速度 | — |
| `TECHNOLOGY[305]` | `TECHNOLOGY[306]` | 砂轮修整-新砂轮轮廓部分实际修整量 | — |
| `TECHNOLOGY[306]` | `TECHNOLOGY[307]` | 砂轮修整-新砂轮轮廓部分实际修整速度 | — |
| `TECHNOLOGY[307]` | `TECHNOLOGY[308]` | 磨削冷却附加通道(0无/1-M28/2-M38) | — |
| `TECHNOLOGY[308]` | `TECHNOLOGY[309]` | 成型修整结束是否靠磨侧面(0否1是) | — |
| `TECHNOLOGY[309]` | `TECHNOLOGY[310]` | 分段补偿中径/导程-界面开启(0隐藏1开启) | — |
| `TECHNOLOGY[310]` | `TECHNOLOGY[311]` | 分段补偿中径/导程使能(0否1是) | — |
| `TECHNOLOGY[311]` | `TECHNOLOGY[312]` | 分段补偿中径 工件总段数 | — |
| `TECHNOLOGY[312]` | `TECHNOLOGY[313]` | 第1段中径补偿量 索引号 312 开始 | — |
| `TECHNOLOGY[313]` | `TECHNOLOGY[314]` | 第2段中径补偿量 | — |
| `TECHNOLOGY[314]` | `TECHNOLOGY[315]` | 第3段中径补偿量 | — |
| `TECHNOLOGY[315]` | `TECHNOLOGY[316]` | 第4段中径补偿量 | — |
| `TECHNOLOGY[316]` | `TECHNOLOGY[317]` | 第5段中径补偿量 | — |
| `TECHNOLOGY[317]` | `TECHNOLOGY[318]` | 第6段中径补偿量 | — |
| `TECHNOLOGY[318]` | `TECHNOLOGY[319]` | 第7段中径补偿量 | — |
| `TECHNOLOGY[319]` | `TECHNOLOGY[320]` | 第8段中径补偿量 | — |
| `TECHNOLOGY[320]` | `TECHNOLOGY[321]` | 第9段中径补偿量 | — |
| `TECHNOLOGY[321]` | `TECHNOLOGY[322]` | 第10段中径补偿量 | — |
| `TECHNOLOGY[322]` | `TECHNOLOGY[323]` | 第1段导程补偿量 索引号 322 开始 | — |
| `TECHNOLOGY[323]` | `TECHNOLOGY[324]` | 第2段导程补偿量 | — |
| `TECHNOLOGY[324]` | `TECHNOLOGY[325]` | 第3段导程补偿量 | — |
| `TECHNOLOGY[325]` | `TECHNOLOGY[326]` | 第4段导程补偿量 | — |
| `TECHNOLOGY[326]` | `TECHNOLOGY[327]` | 第5段导程补偿量 | — |
| `TECHNOLOGY[327]` | `TECHNOLOGY[328]` | 第6段导程补偿量 | — |
| `TECHNOLOGY[328]` | `TECHNOLOGY[329]` | 第7段导程补偿量 | — |
| `TECHNOLOGY[329]` | `TECHNOLOGY[330]` | 第8段导程补偿量 | — |
| `TECHNOLOGY[330]` | `TECHNOLOGY[331]` | 第9段导程补偿量 | — |
| `TECHNOLOGY[331]` | `TECHNOLOGY[332]` | 第10段导程补偿量 | — |
| `TECHNOLOGY[332]` | `TECHNOLOGY[333]` | 第1段补偿坐标.Z 索引号 332 开始 | — |
| `TECHNOLOGY[333]` | `TECHNOLOGY[334]` | 第2段补偿坐标.Z | — |
| `TECHNOLOGY[334]` | `TECHNOLOGY[335]` | 第3段补偿坐标.Z | — |
| `TECHNOLOGY[335]` | `TECHNOLOGY[336]` | 第4段补偿坐标.Z | — |
| `TECHNOLOGY[336]` | `TECHNOLOGY[337]` | 第5段补偿坐标.Z | — |
| `TECHNOLOGY[337]` | `TECHNOLOGY[338]` | 第6段补偿坐标.Z | — |
| `TECHNOLOGY[338]` | `TECHNOLOGY[339]` | 第7段补偿坐标.Z | — |
| `TECHNOLOGY[339]` | `TECHNOLOGY[340]` | 第8段补偿坐标.Z | — |
| `TECHNOLOGY[340]` | `TECHNOLOGY[341]` | 第9段补偿坐标.Z | — |
| `TECHNOLOGY[341]` | `TECHNOLOGY[342]` | 预留 / 暂未使用 | — |
| `TECHNOLOGY[342]` | `TECHNOLOGY[343]` | 多头磨削时每头角度补偿.C-第1头 | — |
| `TECHNOLOGY[343]` | `TECHNOLOGY[344]` | 多头磨削时每头角度补偿.C-第2头 | — |
| `TECHNOLOGY[344]` | `TECHNOLOGY[345]` | 多头磨削时每头角度补偿.C-第3头 | — |
| `TECHNOLOGY[345]` | `TECHNOLOGY[346]` | 多头磨削时每头角度补偿.C-第4头 | — |
| `TECHNOLOGY[346]` | `TECHNOLOGY[347]` | 多头磨削时每头角度补偿.C-第5头 | — |
| `TECHNOLOGY[347]` | `TECHNOLOGY[348]` | 多头磨削时每头角度补偿.C-第6头 | — |
| `TECHNOLOGY[348]` | `TECHNOLOGY[349]` | 预留 / 暂未使用 | — |
| `TECHNOLOGY[349]` | `TECHNOLOGY[350]` | 自动对刀-测量内滚道-第一次进入滚道如果接触上是否先退出再左右移动(0否1是) | — |
| `TECHNOLOGY[350]` | `TECHNOLOGY[351]` | 成型修整结束靠磨侧面-后退距离 | — |
| `TECHNOLOGY[351]` | `TECHNOLOGY[352]` | 成型修整结束靠磨侧面-靠磨距离 | — |
| `TECHNOLOGY[352]` | `TECHNOLOGY[353]` | 是否有Y轴(0否1是) | — |
| `TECHNOLOGY[353]` | `TECHNOLOGY[354]` | 有Y轴-电主轴端面距离A中心距离(砂轮在A左侧为正) | — |
| `TECHNOLOGY[354]` | `TECHNOLOGY[355]` | 磨削Y基准位置(A0情况) | — |
| `TECHNOLOGY[355]` | `TECHNOLOGY[356]` | 修整Y基准位置(A0情况) | — |
| `TECHNOLOGY[356]` | `TECHNOLOGY[357]` | 是否自动计算磨削/修整Y轴实际位置(0否1是) | — |
| `TECHNOLOGY[357]` | `TECHNOLOGY[358]` | 磨削Y轴实际位置 | — |
| `TECHNOLOGY[358]` | `TECHNOLOGY[359]` | 修整Y轴实际位置 | — |
| `TECHNOLOGY[359]` | `TECHNOLOGY[360]` | Y轴设置界面开启(0隐藏1开启) | — |
| `TECHNOLOGY[360]` | `TECHNOLOGY[361]` | 有Y轴-磨杆长度 | — |
| `TECHNOLOGY[361]` | `TECHNOLOGY[362]` | UW轴修整时-夹紧位置 | — |
| `TECHNOLOGY[362]` | `TECHNOLOGY[363]` | UW轴修整时-松开位置 | — |
| `TECHNOLOGY[363]` | `TECHNOLOGY[364]` | UW轴修整时-夹紧力矩 | — |
| `TECHNOLOGY[364]` | `TECHNOLOGY[365]` | UW轴修整时-是否有力矩夹紧轴控制(0否1是) | — |
| `TECHNOLOGY[365]` | `TECHNOLOGY[366]` | 有Y轴-砂轮修整中心到磨杆端面距离 | — |
| `TECHNOLOGY[366]` | `TECHNOLOGY[367]` | UW轴修整时-监控范围 | — |
| `TECHNOLOGY[367]` | `TECHNOLOGY[368]` | 工艺界面压力检测信号显示(0隐藏1显示) | — |
| `TECHNOLOGY[368]` | `TECHNOLOGY[369]` | 配件寿命管理界面显示(0隐藏1显示) | — |
| `TECHNOLOGY[369]` | `TECHNOLOGY[370]` | 工艺设置双向进刀时进刀量模式(0双向总和/1单次进刀量) | — |
| `TECHNOLOGY[370]` | `TECHNOLOGY[371]` | 工艺设置双向进刀时进刀量模式为单次进刀时的进刀量-批量-1 | — |
| `TECHNOLOGY[371]` | `TECHNOLOGY[372]` | 工艺设置双向进刀时进刀量模式为单次进刀时的进刀量-批量-2 | — |
| `TECHNOLOGY[372]` | `TECHNOLOGY[373]` | 工艺设置双向进刀时进刀量模式为单次进刀时的进刀量-批量-3 | — |
| `TECHNOLOGY[373]` | `TECHNOLOGY[374]` | 工艺设置双向进刀时进刀量模式为单次进刀时的进刀量-批量-4 | — |
| `TECHNOLOGY[374]` | `TECHNOLOGY[375]` | 工艺设置双向进刀时进刀量模式为单次进刀时的进刀量-单件-1 | — |
| `TECHNOLOGY[375]` | `TECHNOLOGY[376]` | 工艺设置双向进刀时进刀量模式为单次进刀时的进刀量-单件-2 | — |
| `TECHNOLOGY[376]` | `TECHNOLOGY[377]` | 工艺设置双向进刀时进刀量模式为单次进刀时的进刀量-单件-3 | — |
| `TECHNOLOGY[377]` | `TECHNOLOGY[378]` | 工艺设置双向进刀时进刀量模式为单次进刀时的进刀量-单件-4 | — |
| `TECHNOLOGY[378]` | `TECHNOLOGY[379]` | 变径磨削模式，0=螺纹+变径磨削，1=变径单独磨削 | — |
| `TECHNOLOGY[379]` | `TECHNOLOGY[380]` | 变径磨削-变径单独磨削-磨削次数 | — |
| `TECHNOLOGY[380]` | `TECHNOLOGY[381]` | 多头磨削时每头锥度补偿.x-第1头 | — |
| `TECHNOLOGY[381]` | `TECHNOLOGY[382]` | 多头磨削时每头锥度补偿.x-第2头 | — |
| `TECHNOLOGY[382]` | `TECHNOLOGY[383]` | 多头磨削时每头锥度补偿.x-第3头 | — |
| `TECHNOLOGY[383]` | `TECHNOLOGY[384]` | 多头磨削时每头锥度补偿.x-第4头 | — |
| `TECHNOLOGY[384]` | `TECHNOLOGY[385]` | 多头磨削时每头锥度补偿.x-第5头 | — |
| `TECHNOLOGY[385]` | `TECHNOLOGY[386]` | 多头磨削时每头锥度补偿.x-第6头 | — |
| `TECHNOLOGY[386]` | `TECHNOLOGY[387]` | 反向孔倒角-反向孔类型(0双滚道等距/1单滚道不等距) | — |
| `TECHNOLOGY[387]` | `TECHNOLOGY[388]` | 内螺纹-安全位置Z距磨削右端最小值(默认30) | — |
| `TECHNOLOGY[388]` | `TECHNOLOGY[389]` | 倒角21终点:X向补偿 | — |
| `TECHNOLOGY[389]` | `TECHNOLOGY[390]` | 倒角22终点:X向补偿 | — |
| `TECHNOLOGY[390]` | `TECHNOLOGY[391]` | 倒角23终点:X向补偿 | — |
| `TECHNOLOGY[391]` | `TECHNOLOGY[392]` | 倒角24终点:X向补偿 | — |
| `TECHNOLOGY[392]` | `TECHNOLOGY[393]` | 反向孔倒角-单滚道-孔间距-12 | — |
| `TECHNOLOGY[393]` | `TECHNOLOGY[394]` | 反向孔倒角-单滚道-孔间距-23 | — |
| `TECHNOLOGY[394]` | `TECHNOLOGY[395]` | 反向孔倒角-单滚道-孔间距-34 | — |
| `TECHNOLOGY[395]` | `TECHNOLOGY[396]` | 反向孔倒角-单滚道-孔间距-45 | — |
| `TECHNOLOGY[396]` | `TECHNOLOGY[397]` | 反向孔倒角-单滚道-孔间距-56 | — |
| `TECHNOLOGY[397]` | `TECHNOLOGY[398]` | 反向孔倒角-单滚道-孔间距-67 | — |
| `TECHNOLOGY[398]` | `TECHNOLOGY[399]` | 反向孔倒角-单滚道-孔间距-78 | — |
| `TECHNOLOGY[399]` | `TECHNOLOGY[400]` | 反向孔倒角-单滚道-孔间距-89 | — |
| `TECHNOLOGY[400]` | `TECHNOLOGY[401]` | 反向孔倒角-单滚道-孔间距-910 | — |
| `TECHNOLOGY[401]` | `TECHNOLOGY[402]` | 反向孔倒角-单滚道-孔间距-1011 | — |
| `TECHNOLOGY[402]` | `TECHNOLOGY[403]` | 反向孔倒角-单滚道-孔间距-1112 | — |
| `TECHNOLOGY[403]` | `TECHNOLOGY[404]` | 反向孔倒角-单滚道-孔间距-1213 | — |
| `TECHNOLOGY[404]` | `TECHNOLOGY[405]` | 反向孔倒角-单滚道-孔间距-1314 | — |
| `TECHNOLOGY[405]` | `TECHNOLOGY[406]` | 反向孔倒角-单滚道-孔间距-1415 | — |
| `TECHNOLOGY[406]` | `TECHNOLOGY[407]` | 反向孔倒角-单滚道-孔间距-1516 | — |
| `TECHNOLOGY[407]` | `TECHNOLOGY[408]` | 反向孔倒角-单滚道-孔间距-1617 | — |
| `TECHNOLOGY[408]` | `TECHNOLOGY[409]` | 反向孔倒角-单滚道-孔间距-1718 | — |
| `TECHNOLOGY[409]` | `TECHNOLOGY[410]` | 反向孔倒角-单滚道-孔间距-1819 | — |
| `TECHNOLOGY[410]` | `TECHNOLOGY[411]` | 反向孔倒角-单滚道-孔间距-1920 | — |
| `TECHNOLOGY[411]` | `TECHNOLOGY[412]` | 反向孔倒角-单滚道-孔间距-2021 | — |
| `TECHNOLOGY[412]` | `TECHNOLOGY[413]` | 反向孔倒角-单滚道-孔间距-2122 | — |
| `TECHNOLOGY[413]` | `TECHNOLOGY[414]` | 反向孔倒角-单滚道-孔间距-2223 | — |
| `TECHNOLOGY[414]` | `TECHNOLOGY[415]` | 反向孔倒角-单滚道-孔间距-2324 | — |
| `TECHNOLOGY[415]` | `TECHNOLOGY[416]` | 预留 / 暂未使用 | — |
| `TECHNOLOGY[416]` | `TECHNOLOGY[417]` | 预留 / 暂未使用 | — |
| `TECHNOLOGY[417]` | `TECHNOLOGY[418]` | 多螺距变换-坐标变换位-位置2 | — |
| `TECHNOLOGY[418]` | `TECHNOLOGY[419]` | 多螺距变换-坐标变换位-位置3 | — |
| `TECHNOLOGY[419]` | `TECHNOLOGY[420]` | 多螺距变换-坐标变换位-位置4 | — |
| `TECHNOLOGY[420]` | `TECHNOLOGY[421]` | 多螺距变换-坐标变换位-位置5 | — |
| `TECHNOLOGY[421]` | `TECHNOLOGY[422]` | 多螺距变换-变螺距角度-角度1 | — |
| `TECHNOLOGY[422]` | `TECHNOLOGY[423]` | 多螺距变换-变螺距角度-角度2 | — |
| `TECHNOLOGY[423]` | `TECHNOLOGY[424]` | 多螺距变换-变螺距角度-角度3 | — |
| `TECHNOLOGY[424]` | `TECHNOLOGY[425]` | 多螺距变换-变螺距角度-角度4 | — |
| `TECHNOLOGY[425]` | `TECHNOLOGY[426]` | 多螺距变换-变螺距角度-角度5 | — |
| `TECHNOLOGY[426]` | `TECHNOLOGY[427]` | 多螺距变换-螺距变换值-螺距1 | — |
| `TECHNOLOGY[427]` | `TECHNOLOGY[428]` | 多螺距变换-螺距变换值-螺距2 | — |
| `TECHNOLOGY[428]` | `TECHNOLOGY[429]` | 多螺距变换-螺距变换值-螺距3 | — |
| `TECHNOLOGY[429]` | `TECHNOLOGY[430]` | 多螺距变换-螺距变换值-螺距4 | — |
| `TECHNOLOGY[430]` | `TECHNOLOGY[431]` | 多螺距变换-螺距变换值-螺距5 | — |
| `TECHNOLOGY[431]` | `TECHNOLOGY[432]` | 是否显示平面修修整 | — |

<a id="pi-sec-12"></a>

### 2.12 DIY参数（14 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `DIY[0]` | `DIY[1]` | DIY单双磨削 | — |
| `DIY[1]` | `DIY[2]` | DIY磨削次数 | — |
| `DIY[2]` | `DIY[3]` | DIY磨削进给量 | — |
| `DIY[3]` | `DIY[4]` | DIY磨削速度 | — |
| `DIY[4]` | `DIY[5]` | DIY是否修整累计 | — |
| `DIY[5]` | `DIY[6]` | DIY砂轮线速度 | — |

#### 磨削中心相关

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `DIY[7]` | `DIY[8]` | DIY外圆磨削次数 | — |
| `DIY[8]` | `DIY[9]` | DIY外圆磨削循环几次修砂轮设定 | — |
| `DIY[9]` | `DIY[10]` | DIY外圆磨削循环进给量 | — |
| `DIY[10]` | `DIY[11]` | DIY外圆磨削进给速度 | — |
| `DIY[11]` | `DIY[12]` | DIY外圆磨削砂轮线速度 | — |
| `DIY[12]` | `DIY[13]` | 外圆磨时C轴旋转速度 | — |
| `DIY[13]` | `DIY[14]` | 外圆DIY单双磨削 | — |
| `DIY[14]` | `DIY[15]` | DIY外圆磨削转速速度 | — |

<a id="pi-sec-13"></a>

### 2.13 工件头数参数（8 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `WORK[0]` | `WORK[1]` | 头数 | — |
| `WORK[1]` | `WORK[2]` | 当前头数 | — |
| `WORK[2]` | `WORK[3]` | 平均头数角度 | — |
| `WORK[3]` | `WORK[4]` | 当前头角度 | — |
| `WORK[4]` | `WORK[5]` | 是否按头数修整参数显示(0隐藏1显示) | — |
| `WORK[5]` | `WORK[6]` | 是否按头数修整(0多头磨完计数一次/1按头数计数修整) | — |
| `WORK[6]` | `WORK[7]` | 当前工艺修整设定传递 | — |
| `WORK[7]` | `WORK[8]` | 内螺纹-是否正向进刀磨削(0否1是) | — |

<a id="pi-sec-14"></a>

### 2.14 当前磨削次数参数（10 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `TECH_TIME[0]` | `TECH_TIME[1]` | 当前粗磨次数 | — |
| `TECH_TIME[1]` | `TECH_TIME[2]` | 当前半粗磨次数 | — |
| `TECH_TIME[2]` | `TECH_TIME[3]` | 当前半精磨次数 | — |
| `TECH_TIME[3]` | `TECH_TIME[4]` | 当前精磨次数 | — |
| `TECH_TIME[4]` | `TECH_TIME[5]` | 当前DIY次数 | — |

#### 磨削中心相关

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `TECH_TIME[5]` | `TECH_TIME[6]` | 外圆磨当前粗磨次数 | — |
| `TECH_TIME[6]` | `TECH_TIME[7]` | 外圆磨当前半精磨次数 | — |
| `TECH_TIME[7]` | `TECH_TIME[8]` | 外圆磨当前精磨次数 | — |
| `TECH_TIME[8]` | `TECH_TIME[9]` | 外圆磨当前终磨次数 | — |
| `TECH_TIME[9]` | `TECH_TIME[10]` | 外圆磨当前DIY磨削次数 | — |

<a id="pi-sec-15"></a>

### 2.15 修整进给量参数（29 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `TECH_DRESS_DEEP[0]` | `TECH_DRESS_DEEP[1]` | 修整进给量 | — |
| `TECH_DRESS_DEEP[1]` | `TECH_DRESS_DEEP[2]` | 粗修修整进给量 | — |
| `TECH_DRESS_DEEP[2]` | `TECH_DRESS_DEEP[3]` | 半粗修修整进给量 | — |
| `TECH_DRESS_DEEP[3]` | `TECH_DRESS_DEEP[4]` | 半精修修整进给量 | — |
| `TECH_DRESS_DEEP[4]` | `TECH_DRESS_DEEP[5]` | 精修修整进给量 | — |
| `TECH_DRESS_DEEP[5]` | `TECH_DRESS_DEEP[6]` | DIY修整进给量 | — |
| `TECH_DRESS_DEEP[6]` | `TECH_DRESS_DEEP[7]` | 外圆磨程序工用修整进给量 | — |
| `TECH_DRESS_DEEP[7]` | `TECH_DRESS_DEEP[8]` | 外圆磨粗磨修整进给量 | — |
| `TECH_DRESS_DEEP[8]` | `TECH_DRESS_DEEP[9]` | 外圆磨半精磨修整进给量 | — |
| `TECH_DRESS_DEEP[9]` | `TECH_DRESS_DEEP[10]` | 外圆磨精磨修整进给量 | — |
| `TECH_DRESS_DEEP[10]` | `TECH_DRESS_DEEP[11]` | 外圆磨终磨修整进给量 | — |
| `TECH_DRESS_DEEP[11]` | `TECH_DRESS_DEEP[12]` | 外圆磨DIY工序修整进给量 | — |
| `TECH_DRESS_DEEP[21]` | `TECH_DRESS_DEEP[22]` | 批量粗修修整进给量 | — |
| `TECH_DRESS_DEEP[22]` | `TECH_DRESS_DEEP[23]` | 批量半粗修修整进给量 | — |
| `TECH_DRESS_DEEP[23]` | `TECH_DRESS_DEEP[24]` | 批量半精修修整进给量 | — |
| `TECH_DRESS_DEEP[24]` | `TECH_DRESS_DEEP[25]` | 批量精修修整进给量 | — |
| `TECH_DRESS_DEEP[31]` | `TECH_DRESS_DEEP[32]` | 单件粗修修整进给量 | — |
| `TECH_DRESS_DEEP[32]` | `TECH_DRESS_DEEP[33]` | 单件半粗修修整进给量 | — |
| `TECH_DRESS_DEEP[33]` | `TECH_DRESS_DEEP[34]` | 单件半精修修整进给量 | — |
| `TECH_DRESS_DEEP[34]` | `TECH_DRESS_DEEP[35]` | 单件精修修整进给量 | — |
| `TECH_DRESS_DEEP[35]` | `TECH_DRESS_DEEP[36]` | 端面磨程序公用修整进给量 | — |
| `TECH_DRESS_DEEP[36]` | `TECH_DRESS_DEEP[37]` | 端面磨粗磨修整进给量 | — |
| `TECH_DRESS_DEEP[37]` | `TECH_DRESS_DEEP[38]` | 端面磨精磨修整进给量 | — |
| `TECH_DRESS_DEEP[38]` | `TECH_DRESS_DEEP[39]` | 左端面磨粗磨修整进给量 | — |
| `TECH_DRESS_DEEP[39]` | `TECH_DRESS_DEEP[40]` | 左端面磨精磨修整进给量 | — |
| `TECH_DRESS_DEEP[40]` | `TECH_DRESS_DEEP[41]` | 右端面磨粗磨修整进给量 | — |
| `TECH_DRESS_DEEP[41]` | `TECH_DRESS_DEEP[42]` | 右端面磨精磨修整进给量 | — |
| `TECH_DRESS_DEEP[42]` | `TECH_DRESS_DEEP[43]` | 左右通用端面磨粗磨修整进给量 | — |
| `TECH_DRESS_DEEP[43]` | `TECH_DRESS_DEEP[44]` | 左右通用端面磨精磨修整进给量 | — |

<a id="pi-sec-16"></a>

### 2.16 修整速度参数（29 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `TECH_DRESS_FEED[0]` | `TECH_DRESS_FEED[1]` | 修整速度 | — |
| `TECH_DRESS_FEED[1]` | `TECH_DRESS_FEED[2]` | 粗修整速度 | — |
| `TECH_DRESS_FEED[2]` | `TECH_DRESS_FEED[3]` | 半粗修整速度 | — |
| `TECH_DRESS_FEED[3]` | `TECH_DRESS_FEED[4]` | 半精修整速度 | — |
| `TECH_DRESS_FEED[4]` | `TECH_DRESS_FEED[5]` | 精修整速度 | — |
| `TECH_DRESS_FEED[5]` | `TECH_DRESS_FEED[6]` | DIY整速度 | — |
| `TECH_DRESS_FEED[6]` | `TECH_DRESS_FEED[7]` | 外圆磨程序共用修整速度 | — |
| `TECH_DRESS_FEED[7]` | `TECH_DRESS_FEED[8]` | 外圆磨程序粗磨中修整速度 | — |
| `TECH_DRESS_FEED[8]` | `TECH_DRESS_FEED[9]` | 外圆磨程序半精磨中修整速度 | — |
| `TECH_DRESS_FEED[9]` | `TECH_DRESS_FEED[10]` | 外圆磨程序精磨中修整速度 | — |
| `TECH_DRESS_FEED[10]` | `TECH_DRESS_FEED[11]` | 外圆磨程序终磨中修整速度 | — |
| `TECH_DRESS_FEED[11]` | `TECH_DRESS_FEED[12]` | 外圆磨程序DIY工序中修整速度 | — |
| `TECH_DRESS_FEED[21]` | `TECH_DRESS_FEED[22]` | 批量粗修整速度 | — |
| `TECH_DRESS_FEED[22]` | `TECH_DRESS_FEED[23]` | 批量半粗修整速度 | — |
| `TECH_DRESS_FEED[23]` | `TECH_DRESS_FEED[24]` | 批量半精修整速度 | — |
| `TECH_DRESS_FEED[24]` | `TECH_DRESS_FEED[25]` | 批量精修整速度 | — |
| `TECH_DRESS_FEED[31]` | `TECH_DRESS_FEED[32]` | 单件粗修整速度 | — |
| `TECH_DRESS_FEED[32]` | `TECH_DRESS_FEED[33]` | 单件半粗修整速度 | — |
| `TECH_DRESS_FEED[33]` | `TECH_DRESS_FEED[34]` | 单件半精修整速度 | — |
| `TECH_DRESS_FEED[34]` | `TECH_DRESS_FEED[35]` | 单件精修整速度 | — |
| `TECH_DRESS_FEED[35]` | `TECH_DRESS_FEED[36]` | 端面磨程序共用修整速度 | — |
| `TECH_DRESS_FEED[36]` | `TECH_DRESS_FEED[37]` | 端面磨程序粗磨中修整速度 | — |
| `TECH_DRESS_FEED[37]` | `TECH_DRESS_FEED[38]` | 端面磨程序精磨中修整速度 | — |
| `TECH_DRESS_FEED[38]` | `TECH_DRESS_FEED[39]` | 左端面磨程序粗磨中修整速度 | — |
| `TECH_DRESS_FEED[39]` | `TECH_DRESS_FEED[40]` | 左端面磨程序精磨中修整速度 | — |
| `TECH_DRESS_FEED[40]` | `TECH_DRESS_FEED[41]` | 右端面磨程序粗磨中修整速度 | — |
| `TECH_DRESS_FEED[41]` | `TECH_DRESS_FEED[42]` | 右端面磨程序精磨中修整速度 | — |
| `TECH_DRESS_FEED[42]` | `TECH_DRESS_FEED[43]` | 左右通用端面磨程序粗磨中修整速度 | — |
| `TECH_DRESS_FEED[43]` | `TECH_DRESS_FEED[44]` | 左右通用端面磨程序精磨中修整速度 | — |

<a id="pi-sec-17"></a>

### 2.17 修整轮线速度参数（35 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `WHEEL_LINESPEED_DRESS[0]` | `WHEEL_LINESPEED_DRESS[1]` | 修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[1]` | `WHEEL_LINESPEED_DRESS[2]` | 单纯修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[2]` | `WHEEL_LINESPEED_DRESS[3]` | 工艺修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[3]` | `WHEEL_LINESPEED_DRESS[4]` | 粗磨修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[4]` | `WHEEL_LINESPEED_DRESS[5]` | 半粗磨修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[5]` | `WHEEL_LINESPEED_DRESS[6]` | 半精磨修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[6]` | `WHEEL_LINESPEED_DRESS[7]` | 精磨修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[7]` | `WHEEL_LINESPEED_DRESS[8]` | DIY砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[8]` | `WHEEL_LINESPEED_DRESS[9]` | 外圆磨过程中修整程序共用砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[9]` | `WHEEL_LINESPEED_DRESS[10]` | 外圆磨粗磨过程中修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[10]` | `WHEEL_LINESPEED_DRESS[11]` | 外圆磨半精磨过程中修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[11]` | `WHEEL_LINESPEED_DRESS[12]` | 外圆磨精磨过程中修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[12]` | `WHEEL_LINESPEED_DRESS[13]` | 外圆磨终磨过程中修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[13]` | `WHEEL_LINESPEED_DRESS[14]` | 外圆磨DIY工序中修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[14]` | `WHEEL_LINESPEED_DRESS[15]` | 外圆磨修整程序执行用砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[15]` | `WHEEL_LINESPEED_DRESS[16]` | 外圆磨修整界面设定砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[23]` | `WHEEL_LINESPEED_DRESS[24]` | 批量粗磨修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[24]` | `WHEEL_LINESPEED_DRESS[25]` | 批量半粗磨修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[25]` | `WHEEL_LINESPEED_DRESS[26]` | 批量半精磨修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[26]` | `WHEEL_LINESPEED_DRESS[27]` | 批量精磨修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[33]` | `WHEEL_LINESPEED_DRESS[34]` | 单件粗磨修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[34]` | `WHEEL_LINESPEED_DRESS[35]` | 单件半粗磨修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[35]` | `WHEEL_LINESPEED_DRESS[36]` | 单件半精磨修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[36]` | `WHEEL_LINESPEED_DRESS[37]` | 单件精磨修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[37]` | `WHEEL_LINESPEED_DRESS[38]` | 端面磨过程中修整程序公用砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[38]` | `WHEEL_LINESPEED_DRESS[39]` | 端面磨粗磨过程中修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[39]` | `WHEEL_LINESPEED_DRESS[40]` | 端面磨精磨过程中修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[40]` | `WHEEL_LINESPEED_DRESS[41]` | 端面磨修整程序执行用砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[41]` | `WHEEL_LINESPEED_DRESS[42]` | 端面磨修整界面设定砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[42]` | `WHEEL_LINESPEED_DRESS[43]` | 左端面磨粗磨过程中修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[43]` | `WHEEL_LINESPEED_DRESS[44]` | 左端面磨精磨过程中修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[44]` | `WHEEL_LINESPEED_DRESS[45]` | 右端面磨粗磨过程中修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[45]` | `WHEEL_LINESPEED_DRESS[46]` | 右端面磨精磨过程中修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[46]` | `WHEEL_LINESPEED_DRESS[47]` | 左右通用端面磨粗磨过程中修整砂轮线速度 | — |
| `WHEEL_LINESPEED_DRESS[47]` | `WHEEL_LINESPEED_DRESS[48]` | 左右通用端面磨精磨过程中修整砂轮线速度 | — |

<a id="pi-sec-18"></a>

### 2.18 磨削修整次数参数（29 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `TECH_DRESS_TIME[0]` | `TECH_DRESS_TIME[1]` | 粗磨修整次数 | — |
| `TECH_DRESS_TIME[1]` | `TECH_DRESS_TIME[2]` | 半粗磨修整次数 | — |
| `TECH_DRESS_TIME[2]` | `TECH_DRESS_TIME[3]` | 半精磨修整次数 | — |
| `TECH_DRESS_TIME[3]` | `TECH_DRESS_TIME[4]` | 精磨修整次数 | — |
| `TECH_DRESS_TIME[4]` | `TECH_DRESS_TIME[5]` | DIY修整次数 | — |
| `TECH_DRESS_TIME[5]` | `TECH_DRESS_TIME[6]` | 当前磨削修整次数 | — |
| `TECH_DRESS_TIME[6]` | `TECH_DRESS_TIME[7]` | 外圆磨削当前磨削修整次数 | — |
| `TECH_DRESS_TIME[7]` | `TECH_DRESS_TIME[8]` | 外圆磨削粗磨工序修整次数 | — |
| `TECH_DRESS_TIME[8]` | `TECH_DRESS_TIME[9]` | 外圆磨削半精磨工序修整次数 | — |
| `TECH_DRESS_TIME[9]` | `TECH_DRESS_TIME[10]` | 外圆磨削精磨工序修整次数 | — |
| `TECH_DRESS_TIME[10]` | `TECH_DRESS_TIME[11]` | 外圆磨削终磨工序修整次数 | — |
| `TECH_DRESS_TIME[11]` | `TECH_DRESS_TIME[12]` | 外圆磨削DIY工序中修整次数 | — |
| `TECH_DRESS_TIME[20]` | `TECH_DRESS_TIME[21]` | 批量粗磨修整次数 | — |
| `TECH_DRESS_TIME[21]` | `TECH_DRESS_TIME[22]` | 批量半粗磨修整次数 | — |
| `TECH_DRESS_TIME[22]` | `TECH_DRESS_TIME[23]` | 批量半精磨修整次数 | — |
| `TECH_DRESS_TIME[23]` | `TECH_DRESS_TIME[24]` | 批量精磨修整次数 | — |
| `TECH_DRESS_TIME[30]` | `TECH_DRESS_TIME[31]` | 单件粗磨修整次数 | — |
| `TECH_DRESS_TIME[31]` | `TECH_DRESS_TIME[32]` | 单件半粗磨修整次数 | — |
| `TECH_DRESS_TIME[32]` | `TECH_DRESS_TIME[33]` | 单件半精磨修整次数 | — |
| `TECH_DRESS_TIME[33]` | `TECH_DRESS_TIME[34]` | 单件精磨修整次数 | — |
| `TECH_DRESS_TIME[34]` | `TECH_DRESS_TIME[35]` | 端面磨削当前磨削修整次数 | — |
| `TECH_DRESS_TIME[35]` | `TECH_DRESS_TIME[36]` | 端面磨削粗磨工序修整次数 | — |
| `TECH_DRESS_TIME[36]` | `TECH_DRESS_TIME[37]` | 端面磨削精磨工序修整次数 | — |
| `TECH_DRESS_TIME[37]` | `TECH_DRESS_TIME[38]` | 左端面磨削粗磨工序修整次数 | — |
| `TECH_DRESS_TIME[38]` | `TECH_DRESS_TIME[39]` | 左端面磨削精磨工序修整次数 | — |
| `TECH_DRESS_TIME[39]` | `TECH_DRESS_TIME[40]` | 右端面磨削粗磨工序修整次数 | — |
| `TECH_DRESS_TIME[40]` | `TECH_DRESS_TIME[41]` | 右端面磨削精磨工序修整次数 | — |
| `TECH_DRESS_TIME[41]` | `TECH_DRESS_TIME[42]` | 左右通用端面磨削粗磨工序修整次数 | — |
| `TECH_DRESS_TIME[42]` | `TECH_DRESS_TIME[43]` | 左右通用端面磨削精磨工序修整次数 | — |

<a id="pi-sec-19"></a>

### 2.19 R参数使用情况（7 项）

| `R` 参数 | 变量含义 | 备注 |
| :--- | :--- | :--- |
| `R299` | 模拟量砂轮1转速 | — |
| `R298` | 模拟量砂轮2转速 | — |
| `R297` | 模拟量修整轮1转速 | — |
| `R296` | 模拟量修整轮2转速 | — |
| `R280` | 退刀时存储X轴当前坐标 | 同步动作中不可以使用自定义变量，可以设置机床数据 18660[1]=20，开放20个 real 类型 MGUD 变量：SYG_RM[0]-SYG_RM[19]，可以在同步动作中使用，注意变量名称是系统固定的 |
| `R281` | 退刀时存储Z轴当前坐标 | 同步动作中不可以使用自定义变量，如上介绍 |
| `R282` | vw修整器z回退中修整同步动作标记 | 同步动作中不可以使用自定义变量，如上介绍 |

<a id="pi-sec-20"></a>

### 2.20 内螺纹反相孔倒角参数（28 项）

| `R` 参数 | 变量含义 | 备注 |
| :--- | :--- | :--- |
| `R240` | 倒角个数（范围 1～24） | — |
| `R241` | 倒角面C移动角度 | — |
| `R242` | 倒角深度 | — |
| `R243` | 倒角底面C角度 | — |
| `R244` | 倒角1:Z起始位置 | — |
| `R245` | 倒角2:Z起始位置 | — |
| `R246` | 倒角3:Z起始位置 | — |
| `R247` | 倒角4:Z起始位置 | — |
| `R248` | 倒角5:Z起始位置 | — |
| `R249` | 倒角6:Z起始位置 | — |
| `R250` | 倒角7:Z起始位置 | — |
| `R251` | 倒角8:Z起始位置 | — |
| `R252` | 倒角9:Z起始位置 | — |
| `R253` | 倒角10:Z起始位置 | — |
| `R254` | 倒角11:Z起始位置 | — |
| `R255` | 倒角12:Z起始位置 | — |
| `R256` | 倒角13:Z起始位置 | — |
| `R257` | 倒角14:Z起始位置 | — |
| `R258` | 倒角15:Z起始位置 | — |
| `R259` | 倒角16:Z起始位置 | — |
| `R260` | 倒角17:Z起始位置 | — |
| `R261` | 倒角18:Z起始位置 | — |
| `R262` | 倒角19:Z起始位置 | — |
| `R263` | 倒角20:Z起始位置 | — |
| `R264` | 倒角21:Z起始位置 | — |
| `R265` | 倒角22:Z起始位置 | — |
| `R266` | 倒角23:Z起始位置 | — |
| `R267` | 倒角24:Z起始位置 | — |

<a id="pi-sec-21"></a>

### 2.21 内螺纹夹具自磨R参数版程序参数（22 项）

| `R` 参数 | 变量含义 | 备注 |
| :--- | :--- | :--- |
| `R20` | 安全起始位置.Z | — |
| `R22` | 修整左端位置.Z | — |
| `R23` | 修整右端位置.Z | — |
| `R24` | 修整头架角度.C | — |
| `R25` | 修整接触位置.X | — |
| `R26` | 修整次数 | — |
| `R27` | 每次进刀量 | — |
| `R28` | 修整水平速度 | — |
| `R29` | 修整砂轮转速 | — |
| `R30` | 修整滚轮转速 | — |
| `R32` | 磨削砂轮在卡爪左端坐标.Z | — |
| `R33` | 磨削砂轮在卡爪右端坐标.Z | — |
| `R34` | 磨削砂轮和卡爪接触坐标.X | — |
| `R35` | 磨削进刀量 | — |
| `R36` | 磨削水平移动速度 | — |
| `R37` | 磨削头架转速 | — |
| `R38` | 进刀后光刀停留时间 | — |
| `R39` | 磨削次数 | — |
| `R40` | 磨削砂轮转速 | — |
| `R100` | 机械手上料吹气时头架旋转转速 | — |
| `R101` | 机械手上料吹气时头架旋转保持时间 | — |
| `R102` | 机械手- 内螺纹时是否包含尾架动作，外螺纹时是否包含卡盘动作 | — |

<a id="pi-sec-22"></a>

### 2.22 蜗杆用R参数（23 项）

| `R` 参数 | 变量含义 | 备注 |
| :--- | :--- | :--- |
| `R3` | 修整次数 | — |
| `R7` | 当前V轴修整位置 | — |
| `R8` | 砂轮宽度 | — |
| `R9` | 当前砂轮直径 | — |
| `R10` | 修整轮中心间距 | L=W左-W右+B+r1+r2 |
| `R11` | 左修整轮比右修整轮高出的举例 | — |
| `R12` | 修整轮电主轴转速 | — |
| `R13` | 电主轴启动延时 | — |
| `R14` | 双滚轮间距的中心和砂轮中心重合时的W坐标 | W=(W左+W右)/2 W方向修整中心 |
| `R15` | 修整轮圆弧中心和砂轮中心在V方向重合时的V坐标 | 砂轮中心V坐标 |
| `R16` | 修整结束水平轴停泊点 | — |
| `R17` | 修整结束垂直轴停泊点 | — |
| `R29` | 修整轮圆弧半径,生成蜗杆程序时确定,此处变量只检验 | — |

#### 修整参数

| `R` 参数 | 变量含义 | 备注 |
| :--- | :--- | :--- |
| `R18` | 粗修进给速度 | — |
| `R19` | 精修进给速度 | — |
| `R20` | 粗修进给量 | — |
| `R21` | 精修进给量 | — |
| `R22` | 修整定位速度 | — |
| `R23` | 修整返回速度 | — |

#### 不需要修改的参数

| `R` 参数 | 变量含义 | 备注 |
| :--- | :--- | :--- |
| `R28` | 修整偏移距离 | — |
| `R25` | 当前修整次数 | — |
| `R26` | 当前修整进给速度 | — |
| `R27` | 当前修整进给量 | — |

<a id="pi-sec-23"></a>

### 2.23 通用齿形模型变量（78 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `WHICH_COMMON_SHAPE` | `WHICH_COMMON_SHAPE` | 齿形选择 | — |
| `COMMON_VER_TOP` | `COMMON_VER_TOP` | 齿形最高点位置 | — |
| `COMMON_VER_BOTTOM` | `COMMON_VER_BOTTOM` | 齿形最低点位置 | — |
| `COMMON_VER_HEIGHT` | `COMMON_VER_HEIGHT` | 实际齿高 | — |
| `COMMON_MACHINE_STATUS` | `COMMON_MACHINE_STATUS` | 机床类型 | — |
| `COMMON_ANG_MODIFY` | `COMMON_ANG_MODIFY` | 不同机床类型的角度计算变量 | — |
| `COMMON_LENGTH[1]` | `COMMON_LENGTH[1]` | 第1段线长度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_LENGTH[2]` | `COMMON_LENGTH[2]` | 第2段线长度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_LENGTH[3]` | `COMMON_LENGTH[3]` | 第3段线长度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_LENGTH[4]` | `COMMON_LENGTH[4]` | 第4段线长度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_LENGTH[5]` | `COMMON_LENGTH[5]` | 第5段线长度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_LENGTH[6]` | `COMMON_LENGTH[6]` | 第6段线长度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_LENGTH[7]` | `COMMON_LENGTH[7]` | 第7段线长度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_LENGTH[8]` | `COMMON_LENGTH[8]` | 第8段线长度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_LENGTH[9]` | `COMMON_LENGTH[9]` | 第9段线长度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_LENGTH[10]` | `COMMON_LENGTH[10]` | 第10段线长度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_ANG[1]` | `COMMON_ANG[1]` | 第1段线角度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_ANG[2]` | `COMMON_ANG[2]` | 第2段线角度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_ANG[3]` | `COMMON_ANG[3]` | 第3段线角度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_ANG[4]` | `COMMON_ANG[4]` | 第4段线角度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_ANG[5]` | `COMMON_ANG[5]` | 第5段线角度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_ANG[6]` | `COMMON_ANG[6]` | 第6段线角度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_ANG[7]` | `COMMON_ANG[7]` | 第7段线角度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_ANG[8]` | `COMMON_ANG[8]` | 第8段线角度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_ANG[9]` | `COMMON_ANG[9]` | 第9段线角度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_ANG[10]` | `COMMON_ANG[10]` | 第10段线角度 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_RND[1]` | `COMMON_RND[1]` | 第1段线圆弧半径 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_RND[2]` | `COMMON_RND[2]` | 第2段线圆弧半径 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_RND[3]` | `COMMON_RND[3]` | 第3段线圆弧半径 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_RND[4]` | `COMMON_RND[4]` | 第4段线圆弧半径 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_RND[5]` | `COMMON_RND[5]` | 第5段线圆弧半径 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_RND[6]` | `COMMON_RND[6]` | 第6段线圆弧半径 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_RND[7]` | `COMMON_RND[7]` | 第7段线圆弧半径 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_RND[8]` | `COMMON_RND[8]` | 第8段线圆弧半径 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_RND[9]` | `COMMON_RND[9]` | 第9段线圆弧半径 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_RND[10]` | `COMMON_RND[10]` | 第10段线圆弧半径 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_STATUS_CACU[0]` | `COMMON_STATUS_CACU[1]` | 中间点轮廓相对原线段加或减 | — |
| `COMMON_STATUS_CACU[1]` | `COMMON_STATUS_CACU[2]` | 第1段线轮廓相对原线段加或减 | — |
| `COMMON_STATUS_CACU[2]` | `COMMON_STATUS_CACU[3]` | 第2段线轮廓相对原线段加或减 | — |
| `COMMON_STATUS_CACU[3]` | `COMMON_STATUS_CACU[4]` | 第3段线轮廓相对原线段加或减 | — |
| `COMMON_STATUS_CACU[4]` | `COMMON_STATUS_CACU[5]` | 第4段线轮廓相对原线段加或减 | — |
| `COMMON_STATUS_CACU[5]` | `COMMON_STATUS_CACU[6]` | 第5段线轮廓相对原线段加或减 | — |
| `COMMON_STATUS_CACU[6]` | `COMMON_STATUS_CACU[7]` | 第6段线轮廓相对原线段加或减 | — |
| `COMMON_STATUS_CACU[7]` | `COMMON_STATUS_CACU[8]` | 第7段线轮廓相对原线段加或减 | — |
| `COMMON_STATUS_CACU[8]` | `COMMON_STATUS_CACU[9]` | 第8段线轮廓相对原线段加或减 | — |
| `COMMON_STATUS_CACU[9]` | `COMMON_STATUS_CACU[10]` | 第9段线轮廓相对原线段加或减 | — |
| `COMMON_STATUS_CACU[10]` | `COMMON_STATUS_CACU[11]` | 第10段线轮廓相对原线段加或减 | — |
| `COMMON_LENGTH_ADD[0]` | `COMMON_LENGTH_ADD[1]` | 中间点轮廓增加/减少部分长度 | — |
| `COMMON_LENGTH_ADD[1]` | `COMMON_LENGTH_ADD[2]` | 第1段轮廓增加/减少部分长度 | — |
| `COMMON_LENGTH_ADD[2]` | `COMMON_LENGTH_ADD[3]` | 第2段轮廓增加/减少部分长度 | — |
| `COMMON_LENGTH_ADD[3]` | `COMMON_LENGTH_ADD[4]` | 第3段轮廓增加/减少部分长度 | — |
| `COMMON_LENGTH_ADD[4]` | `COMMON_LENGTH_ADD[5]` | 第4段轮廓增加/减少部分长度 | — |
| `COMMON_LENGTH_ADD[5]` | `COMMON_LENGTH_ADD[6]` | 第5段轮廓增加/减少部分长度 | — |
| `COMMON_LENGTH_ADD[6]` | `COMMON_LENGTH_ADD[7]` | 第6段轮廓增加/减少部分长度 | — |
| `COMMON_LENGTH_ADD[7]` | `COMMON_LENGTH_ADD[8]` | 第7段轮廓增加/减少部分长度 | — |
| `COMMON_LENGTH_ADD[8]` | `COMMON_LENGTH_ADD[9]` | 第8段轮廓增加/减少部分长度 | — |
| `COMMON_LENGTH_ADD[9]` | `COMMON_LENGTH_ADD[10]` | 第9段轮廓增加/减少部分长度 | — |
| `COMMON_LENGTH_ADD[10]` | `COMMON_LENGTH_ADD[11]` | 第10段轮廓增加/减少部分长度 | — |
| `COMMON_POINT_REF_VER[1]` | `COMMON_POINT_REF_VER[1]` | 第1点相对垂直坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_VER[2]` | `COMMON_POINT_REF_VER[2]` | 第2点相对垂直坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_VER[3]` | `COMMON_POINT_REF_VER[3]` | 第3点相对垂直坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_VER[4]` | `COMMON_POINT_REF_VER[4]` | 第4点相对垂直坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_VER[5]` | `COMMON_POINT_REF_VER[5]` | 第5点相对垂直坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_VER[6]` | `COMMON_POINT_REF_VER[6]` | 第6点相对垂直坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_VER[7]` | `COMMON_POINT_REF_VER[7]` | 第7点相对垂直坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_VER[8]` | `COMMON_POINT_REF_VER[8]` | 第8点相对垂直坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_VER[9]` | `COMMON_POINT_REF_VER[9]` | 第9点相对垂直坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_VER[10]` | `COMMON_POINT_REF_VER[10]` | 第10点相对垂直坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_HORI[1]` | `COMMON_POINT_REF_HORI[1]` | 第1点相对水平坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_HORI[2]` | `COMMON_POINT_REF_HORI[2]` | 第2点相对水平坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_HORI[3]` | `COMMON_POINT_REF_HORI[3]` | 第3点相对水平坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_HORI[4]` | `COMMON_POINT_REF_HORI[4]` | 第4点相对水平坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_HORI[5]` | `COMMON_POINT_REF_HORI[5]` | 第5点相对水平坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_HORI[6]` | `COMMON_POINT_REF_HORI[6]` | 第6点相对水平坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_HORI[7]` | `COMMON_POINT_REF_HORI[7]` | 第7点相对水平坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_HORI[8]` | `COMMON_POINT_REF_HORI[8]` | 第8点相对水平坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_HORI[9]` | `COMMON_POINT_REF_HORI[9]` | 第9点相对水平坐标 | 通用齿形 `1～10` 段同下标引用 |
| `COMMON_POINT_REF_HORI[10]` | `COMMON_POINT_REF_HORI[10]` | 第10点相对水平坐标 | 通用齿形 `1～10` 段同下标引用 |

<a id="pi-sec-24"></a>

### 2.24 SHAPE MODEL（136 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `SHAPE_MODEL[0]` | `SHAPE_MODEL[1]` | 外部修整程序位置(0内置/1后USB/2前USB/3 CF卡) | 后部USB地址需要在逻辑驱动器中配置好，名称设置为 "//DEV_3" |
| `SHAPE_MODEL[1]` | `SHAPE_MODEL[2]` | 三角-左齿根圆弧半径 | — |
| `SHAPE_MODEL[2]` | `SHAPE_MODEL[3]` | 三角-右齿根圆弧半径 | — |
| `SHAPE_MODEL[3]` | `SHAPE_MODEL[4]` | 梯形-左齿根圆弧半径 | — |
| `SHAPE_MODEL[4]` | `SHAPE_MODEL[5]` | 梯形-右齿根圆弧半径 | — |
| `SHAPE_MODEL[5]` | `SHAPE_MODEL[6]` | 三角-锥度 输入锥度比值 如 1/16/2 | — |
| `SHAPE_MODEL[6]` | `SHAPE_MODEL[7]` | 三角-齿型选择参数显示(0否1是) | — |
| `SHAPE_MODEL[7]` | `SHAPE_MODEL[8]` | 双圆弧齿形旋转角(左正右负) | — |
| `SHAPE_MODEL[8]` | `SHAPE_MODEL[9]` | 三角-多线修整(0否1是) | — |
| `SHAPE_MODEL[9]` | `SHAPE_MODEL[10]` | 三角-多线齿数 | — |
| `SHAPE_MODEL[10]` | `SHAPE_MODEL[11]` | 扩展梯形-螺距 | — |
| `SHAPE_MODEL[11]` | `SHAPE_MODEL[12]` | 梯形-锥度 输入锥度比值 如 1/16/2 | — |
| `SHAPE_MODEL[12]` | `SHAPE_MODEL[13]` | 扩展梯形-中径宽度 | — |
| `SHAPE_MODEL[13]` | `SHAPE_MODEL[14]` | 扩展梯形-中径高度 | — |
| `SHAPE_MODEL[14]` | `SHAPE_MODEL[15]` | 扩展梯形-齿底高度 | — |
| `SHAPE_MODEL[15]` | `SHAPE_MODEL[16]` | 扩展梯形-左半角 | — |
| `SHAPE_MODEL[16]` | `SHAPE_MODEL[17]` | 扩展梯形-右半角 | — |
| `SHAPE_MODEL[17]` | `SHAPE_MODEL[18]` | 扩展梯形-左齿尖R | — |
| `SHAPE_MODEL[18]` | `SHAPE_MODEL[19]` | 扩展梯形-右齿尖R | — |
| `SHAPE_MODEL[19]` | `SHAPE_MODEL[20]` | 扩展梯形-左齿底R | — |
| `SHAPE_MODEL[20]` | `SHAPE_MODEL[21]` | 扩展梯形-右齿底R | — |
| `SHAPE_MODEL[21]` | `SHAPE_MODEL[22]` | 扩展梯形-延长斜线角度 | — |
| `SHAPE_MODEL[22]` | `SHAPE_MODEL[23]` | 双圆弧-钢球直径 | — |
| `SHAPE_MODEL[23]` | `SHAPE_MODEL[24]` | 双圆弧-接触角 | — |
| `SHAPE_MODEL[24]` | `SHAPE_MODEL[25]` | 扩展梯形-齿顶模式(0平顶/1锥顶) | — |
| `SHAPE_MODEL[25]` | `SHAPE_MODEL[26]` | 梯形-是否是扩展梯形(0否1偏梯形/2戴帽梯形) | — |
| `SHAPE_MODEL[26]` | `SHAPE_MODEL[27]` | 梯形-梯形修整模式选择参数显示(0否1是) | — |
| `SHAPE_MODEL[27]` | `SHAPE_MODEL[28]` | 双圆弧-齿底过渡方式(0斜角1圆角) | — |
| `SHAPE_MODEL[28]` | `SHAPE_MODEL[29]` | 双圆弧-齿底圆角半径 | — |
| `SHAPE_MODEL[29]` | `SHAPE_MODEL[30]` | 三角-多线-间隔螺距(0表示无间隔) | — |
| `SHAPE_MODEL[30]` | `SHAPE_MODEL[31]` | 行星齿-左圆弧半径-初始 | — |
| `SHAPE_MODEL[31]` | `SHAPE_MODEL[32]` | 行星齿-左圆弧半径-调整 | — |
| `SHAPE_MODEL[32]` | `SHAPE_MODEL[33]` | 行星齿-左圆弧半径-当前 | — |
| `SHAPE_MODEL[33]` | `SHAPE_MODEL[34]` | 行星齿-右圆弧半径-初始 | — |
| `SHAPE_MODEL[34]` | `SHAPE_MODEL[35]` | 行星齿-右圆弧半径-调整 | — |
| `SHAPE_MODEL[35]` | `SHAPE_MODEL[36]` | 行星齿-右圆弧半径-当前 | — |
| `SHAPE_MODEL[36]` | `SHAPE_MODEL[37]` | 行星齿-左圆弧偏心-初始 | — |
| `SHAPE_MODEL[37]` | `SHAPE_MODEL[38]` | 行星齿-左圆弧偏心-调整 | — |
| `SHAPE_MODEL[38]` | `SHAPE_MODEL[39]` | 行星齿-左圆弧偏心-当前 | — |
| `SHAPE_MODEL[39]` | `SHAPE_MODEL[40]` | 行星齿-右圆弧偏心-初始 | — |
| `SHAPE_MODEL[40]` | `SHAPE_MODEL[41]` | 行星齿-右圆弧偏心-调整 | — |
| `SHAPE_MODEL[41]` | `SHAPE_MODEL[42]` | 行星齿-右圆弧偏心-当前 | — |
| `SHAPE_MODEL[42]` | `SHAPE_MODEL[43]` | 行星齿-修整圆弧角度（范围 45°～90°） 修整到水平状态为90度 | — |
| `SHAPE_MODEL[43]` | `SHAPE_MODEL[44]` | 行星齿-过渡斜线角度-水平方向夹角 | — |
| `SHAPE_MODEL[44]` | `SHAPE_MODEL[45]` | 行星齿-过渡斜线长度 | — |
| `SHAPE_MODEL[45]` | `SHAPE_MODEL[46]` | 行星齿-齿顶圆弧半径 | — |
| `SHAPE_MODEL[46]` | `SHAPE_MODEL[47]` | 行星齿-中径 | — |
| `SHAPE_MODEL[47]` | `SHAPE_MODEL[48]` | 行星齿-小径 | — |
| `SHAPE_MODEL[48]` | `SHAPE_MODEL[49]` | 行星齿-中径接触角(圆心垂直向下夹角) | — |
| `SHAPE_MODEL[49]` | `SHAPE_MODEL[50]` | 行星齿-齿顶过渡方式(0圆弧/1平顶) | — |
| `SHAPE_MODEL[50]` | `SHAPE_MODEL[51]` | 环形槽进刀速度 | — |
| `SHAPE_MODEL[51]` | `SHAPE_MODEL[52]` | 预留 / 暂未使用 | — |
| `SHAPE_MODEL[52]` | `SHAPE_MODEL[53]` | 预留 / 暂未使用 | — |
| `SHAPE_MODEL[53]` | `SHAPE_MODEL[54]` | 预留 / 暂未使用 | — |
| `SHAPE_MODEL[54]` | `SHAPE_MODEL[55]` | 预留 / 暂未使用 | — |
| `SHAPE_MODEL[55]` | `SHAPE_MODEL[56]` | 预留 / 暂未使用 | — |
| `SHAPE_MODEL[56]` | `SHAPE_MODEL[57]` | 预留 / 暂未使用 | — |
| `SHAPE_MODEL[57]` | `SHAPE_MODEL[58]` | 预留 / 暂未使用 | — |
| `SHAPE_MODEL[58]` | `SHAPE_MODEL[59]` | 预留 / 暂未使用 | — |
| `SHAPE_MODEL[59]` | `SHAPE_MODEL[60]` | 预留 / 暂未使用 | — |
| `SHAPE_MODEL[60]` | `SHAPE_MODEL[61]` | 批量磨削-起始加工工序选择(0粗磨/1半精磨/2精磨/3终磨) | — |
| `SHAPE_MODEL[61]` | `SHAPE_MODEL[62]` | 批量磨削-起始工序起始循环(如果大于本工序循环次数则直接进入下一工序) | — |
| `SHAPE_MODEL[62]` | `SHAPE_MODEL[63]` | 批量磨削-起始加工工序选择标记 | — |
| `SHAPE_MODEL[63]` | `SHAPE_MODEL[64]` | 批量磨削-起始加工工序选择功能使能(起始工序之前的部分会自动加入当前接触位置直接进到位) | — |
| `SHAPE_MODEL[64]` | `SHAPE_MODEL[65]` | 批量磨削-起始加工工序选择(第一次循环标记) | — |
| `SHAPE_MODEL[65]` | `SHAPE_MODEL[66]` | 当前-多线齿数 | — |
| `SHAPE_MODEL[66]` | `SHAPE_MODEL[67]` | 梯形-多线齿数 | — |
| `SHAPE_MODEL[67]` | `SHAPE_MODEL[68]` | 双圆弧-多线齿数 | — |
| `SHAPE_MODEL[68]` | `SHAPE_MODEL[69]` | 当前-锥度-输入锥度比值 如 1/16/2 | — |
| `SHAPE_MODEL[69]` | `SHAPE_MODEL[70]` | 当前-多线修整(0否1是) | — |
| `SHAPE_MODEL[70]` | `SHAPE_MODEL[71]` | 当前-多线-间隔螺距(0表示无间隔) | — |
| `SHAPE_MODEL[71]` | `SHAPE_MODEL[72]` | 当前-多线-齿高补偿 offset 正值为左边齿越来越矮 | — |
| `SHAPE_MODEL[72]` | `SHAPE_MODEL[73]` | 当前-多线-当前修整齿编号(第一齿为0) | — |
| `SHAPE_MODEL[73]` | `SHAPE_MODEL[74]` | 三角-多线-齿高补偿 正值为左边齿越来越矮 | — |
| `SHAPE_MODEL[74]` | `SHAPE_MODEL[75]` | 梯形-多线修整(0否1是) | — |
| `SHAPE_MODEL[75]` | `SHAPE_MODEL[76]` | 梯形-多线-间隔螺距(0表示无间隔) | — |
| `SHAPE_MODEL[76]` | `SHAPE_MODEL[77]` | 梯形-多线-齿高补偿 offset 正值为左边齿越来越矮 | — |
| `SHAPE_MODEL[77]` | `SHAPE_MODEL[78]` | 双圆弧-多线修整(0否1是) | — |
| `SHAPE_MODEL[78]` | `SHAPE_MODEL[79]` | 双圆弧-多线-间隔螺距(0表示无间隔) | — |
| `SHAPE_MODEL[79]` | `SHAPE_MODEL[80]` | 双圆弧-多线-齿高补偿 offset 正值为左边齿越来越矮 | — |

#### 双圆弧

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `SHAPE_MODEL[80]` | `SHAPE_MODEL[81]` | 左圆弧半径当前 | — |
| `SHAPE_MODEL[81]` | `SHAPE_MODEL[82]` | 右圆弧半径当前 | — |
| `SHAPE_MODEL[82]` | `SHAPE_MODEL[83]` | 左偏心当前 | — |
| `SHAPE_MODEL[83]` | `SHAPE_MODEL[84]` | 右偏心当前 | — |
| `SHAPE_MODEL[84]` | `SHAPE_MODEL[85]` | 过度1斜线角度 | — |
| `SHAPE_MODEL[85]` | `SHAPE_MODEL[86]` | 过度1斜线长度延长 | — |
| `SHAPE_MODEL[86]` | `SHAPE_MODEL[87]` | 过度2斜线角度 | — |
| `SHAPE_MODEL[87]` | `SHAPE_MODEL[88]` | 过度2斜线长度 | — |
| `SHAPE_MODEL[88]` | `SHAPE_MODEL[89]` | 圆弧部分角度 | — |
| `SHAPE_MODEL[89]` | `SHAPE_MODEL[90]` | 双圆弧齿形右侧高低微调 | — |

#### 梯形

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `SHAPE_MODEL[90]` | `SHAPE_MODEL[91]` | 齿底长度 | — |
| `SHAPE_MODEL[91]` | `SHAPE_MODEL[92]` | 齿底左圆弧半径 | — |
| `SHAPE_MODEL[92]` | `SHAPE_MODEL[93]` | 齿底右圆弧半径 | — |
| `SHAPE_MODEL[93]` | `SHAPE_MODEL[94]` | 左斜面角度 | — |
| `SHAPE_MODEL[94]` | `SHAPE_MODEL[95]` | 右斜面角度 | — |
| `SHAPE_MODEL[95]` | `SHAPE_MODEL[96]` | 齿高 | — |
| `SHAPE_MODEL[96]` | `SHAPE_MODEL[97]` | 延长线角度 | — |
| `SHAPE_MODEL[97]` | `SHAPE_MODEL[98]` | 上-左斜面角度 | — |
| `SHAPE_MODEL[98]` | `SHAPE_MODEL[99]` | 上-右斜面角度 | — |
| `SHAPE_MODEL[99]` | `SHAPE_MODEL[100]` | 上-齿高 | — |

#### 三角

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `SHAPE_MODEL[100]` | `SHAPE_MODEL[101]` | 齿底圆弧半径 | — |
| `SHAPE_MODEL[101]` | `SHAPE_MODEL[102]` | 下-左半角 | — |
| `SHAPE_MODEL[102]` | `SHAPE_MODEL[103]` | 下-右半角 | — |
| `SHAPE_MODEL[103]` | `SHAPE_MODEL[104]` | 总-齿高 | — |
| `SHAPE_MODEL[104]` | `SHAPE_MODEL[105]` | 延长线角度 | — |
| `SHAPE_MODEL[105]` | `SHAPE_MODEL[106]` | 上-左斜面角度 | — |
| `SHAPE_MODEL[106]` | `SHAPE_MODEL[107]` | 上-右斜面角度 | — |
| `SHAPE_MODEL[107]` | `SHAPE_MODEL[108]` | 上-齿高 | — |
| `SHAPE_MODEL[108]` | `SHAPE_MODEL[109]` | 预留 / 暂未使用 | — |
| `SHAPE_MODEL[109]` | `SHAPE_MODEL[110]` | 预留 / 暂未使用 | — |
| `SHAPE_MODEL[110]` | `SHAPE_MODEL[111]` | 双圆弧-扩展齿型(0否1是) | — |
| `SHAPE_MODEL[111]` | `SHAPE_MODEL[112]` | 双圆弧-延长线角度 | — |
| `SHAPE_MODEL[112]` | `SHAPE_MODEL[113]` | 双圆弧-左圆弧半径初始 | — |
| `SHAPE_MODEL[113]` | `SHAPE_MODEL[114]` | 双圆弧-右圆弧半径初始 | — |
| `SHAPE_MODEL[114]` | `SHAPE_MODEL[115]` | 双圆弧-左偏心初始 | — |
| `SHAPE_MODEL[115]` | `SHAPE_MODEL[116]` | 双圆弧-右偏心初始 | — |
| `SHAPE_MODEL[116]` | `SHAPE_MODEL[117]` | 双圆弧-左圆弧半径调整 | — |
| `SHAPE_MODEL[117]` | `SHAPE_MODEL[118]` | 双圆弧-右圆弧半径调整 | — |
| `SHAPE_MODEL[118]` | `SHAPE_MODEL[119]` | 双圆弧-左偏心调整 | — |
| `SHAPE_MODEL[119]` | `SHAPE_MODEL[120]` | 双圆弧-右偏心调整 | — |
| `SHAPE_MODEL[120]` | `SHAPE_MODEL[121]` | 外部齿形程序延长右第1段角度 自动赋值 | — |
| `SHAPE_MODEL[121]` | `SHAPE_MODEL[122]` | 外部齿形程序延长右第1段长度 | — |
| `SHAPE_MODEL[122]` | `SHAPE_MODEL[123]` | 外部齿形程序延长右第2段角度 自动赋值 | — |
| `SHAPE_MODEL[123]` | `SHAPE_MODEL[124]` | 外部齿形程序延长右第2段长度 自动计算 | — |
| `SHAPE_MODEL[124]` | `SHAPE_MODEL[125]` | 外部齿形程序延长右第3段角度 | — |
| `SHAPE_MODEL[125]` | `SHAPE_MODEL[126]` | 外部齿形程序延长右第3段长度 自动计算 | — |
| `SHAPE_MODEL[126]` | `SHAPE_MODEL[127]` | 外部齿形程序延长右第4段角度 自动赋值 | — |
| `SHAPE_MODEL[127]` | `SHAPE_MODEL[128]` | 外部齿形程序延长右第4段长度 自动赋值 | — |
| `SHAPE_MODEL[130]` | `SHAPE_MODEL[131]` | 外部齿形程序延长左第1段角度 自动赋值 | — |
| `SHAPE_MODEL[131]` | `SHAPE_MODEL[132]` | 外部齿形程序延长左第1段长度 | — |
| `SHAPE_MODEL[132]` | `SHAPE_MODEL[133]` | 外部齿形程序延长左第2段角度 自动赋值 | — |
| `SHAPE_MODEL[133]` | `SHAPE_MODEL[134]` | 外部齿形程序延长左第2段长度 自动计算 | — |
| `SHAPE_MODEL[134]` | `SHAPE_MODEL[135]` | 外部齿形程序延长左第3段角度 | — |
| `SHAPE_MODEL[135]` | `SHAPE_MODEL[136]` | 外部齿形程序延长左第3段长度 自动计算 | — |
| `SHAPE_MODEL[136]` | `SHAPE_MODEL[137]` | 外部齿形程序延长左第4段角度 自动赋值 | — |
| `SHAPE_MODEL[137]` | `SHAPE_MODEL[138]` | 外部齿形程序延长左第4段长度 自动赋值 | — |

<a id="pi-sec-25"></a>

### 2.25 RING GROOVE（31 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `RING[0]` | `RING[1]` | 螺纹0/环形槽1 | — |
| `RING[1]` | `RING[2]` | 总槽数 | — |
| `RING[2]` | `RING[3]` | 起始磨削槽 | — |
| `RING[3]` | `RING[4]` | 终止磨削槽 | — |
| `RING[4]` | `RING[5]` | 需加工槽数 | — |
| `RING[5]` | `RING[6]` | 已加工槽数 | — |
| `RING[6]` | `RING[7]` | 当前槽的X相对偏移量 | — |
| `RING[7]` | `RING[8]` | 当前槽的Z相对偏移量 | — |
| `RING[8]` | `RING[9]` | 当前槽起始磨削位置X | — |
| `RING[9]` | `RING[10]` | 当前槽起始磨削位置Z | — |
| `RING[10]` | `RING[11]` | 环形槽组1螺距 | — |
| `RING[11]` | `RING[12]` | 环形槽组1槽数 | — |
| `RING[12]` | `RING[13]` | 环形槽组1组间水平偏移 | — |
| `RING[13]` | `RING[14]` | 环形槽组1组间垂直偏移 | — |
| `RING[14]` | `RING[15]` | 环形槽组1槽间锥度偏移 | — |
| `RING[20]` | `RING[21]` | 环形槽组2螺距 | — |
| `RING[21]` | `RING[22]` | 环形槽组2槽数 | — |
| `RING[22]` | `RING[23]` | 环形槽组2组间水平偏移 | — |
| `RING[23]` | `RING[24]` | 环形槽组2组间垂直偏移 | — |
| `RING[24]` | `RING[25]` | 环形槽组2槽间锥度偏移 | — |
| `RING[30]` | `RING[31]` | 环形槽组3螺距 | — |
| `RING[31]` | `RING[32]` | 环形槽组3槽数 | — |
| `RING[32]` | `RING[33]` | 环形槽组3组间水平偏移 | — |
| `RING[33]` | `RING[34]` | 环形槽组3组间垂直偏移 | — |
| `RING[34]` | `RING[35]` | 环形槽组3槽间锥度偏移 | — |
| `RING[40]` | `RING[41]` | 环形槽组4螺距 | — |
| `RING[41]` | `RING[42]` | 环形槽组4槽数 | — |
| `RING[42]` | `RING[43]` | 环形槽组4组间水平偏移 | — |
| `RING[43]` | `RING[44]` | 环形槽组4组间垂直偏移 | — |
| `RING[44]` | `RING[45]` | 环形槽组4槽间锥度偏移 | — |
| `RING[49]` | `RING[50]` | 显示环形槽选择参数 | — |

<a id="pi-sec-26"></a>

### 2.26 SCREW TAP（19 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `SCREW_TAP[0]` | `SCREW_TAP[1]` | 螺纹0/丝锥1 | — |
| `SCREW_TAP[1]` | `SCREW_TAP[2]` | 丝锥槽数 | — |
| `SCREW_TAP[2]` | `SCREW_TAP[3]` | 直槽0/螺旋槽1 | — |
| `SCREW_TAP[3]` | `SCREW_TAP[4]` | 螺旋槽右旋0/左旋1 | — |
| `SCREW_TAP[4]` | `SCREW_TAP[5]` | 螺旋槽升角 | — |
| `SCREW_TAP[5]` | `SCREW_TAP[6]` | B轴初始角 | — |
| `SCREW_TAP[6]` | `SCREW_TAP[7]` | 是否跳齿(0否1是) | — |
| `SCREW_TAP[7]` | `SCREW_TAP[8]` | 跳齿c起始角度调整 | — |
| `SCREW_TAP[8]` | `SCREW_TAP[9]` | 跳齿每槽角度调整 | — |
| `SCREW_TAP[9]` | `SCREW_TAP[10]` | B轴快速动作速度 | — |
| `SCREW_TAP[10]` | `SCREW_TAP[11]` | B轴慢速动作速度 | — |
| `SCREW_TAP[11]` | `SCREW_TAP[12]` | 跳齿后退距离 | — |
| `SCREW_TAP[12]` | `SCREW_TAP[13]` | 跳齿每齿停留时间 | — |
| `SCREW_TAP[13]` | `SCREW_TAP[14]` | C轴对刀DRF | — |
| `SCREW_TAP[14]` | `SCREW_TAP[15]` | 预留 / 暂未使用 | — |
| `SCREW_TAP[15]` | `SCREW_TAP[16]` | 预留 / 暂未使用 | — |
| `SCREW_TAP[16]` | `SCREW_TAP[17]` | B轴随动系数 | — |
| `STRING_ADDON[0]` | `STRING_ADDON[1]` | 外部程序调用文件夹目录 | — |
| `STRING_ADDON[1]` | `STRING_ADDON[2]` | 当前工序名称 | — |

<a id="pi-sec-27"></a>

### 2.27 SERVICE_LIFE（15 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `SERVICE_LIFE[0]` | `SERVICE_LIFE[1]` | 设定滚轮寿命 | — |
| `SERVICE_LIFE[1]` | `SERVICE_LIFE[2]` | 设定夹具寿命 | — |
| `SERVICE_LIFE[2]` | `SERVICE_LIFE[3]` | 设定金刚笔1寿命 | — |
| `SERVICE_LIFE[3]` | `SERVICE_LIFE[4]` | 设定金刚笔2寿命 | — |
| `SERVICE_LIFE[4]` | `SERVICE_LIFE[5]` | 预留 / 暂未使用 | — |
| `SERVICE_LIFE[5]` | `SERVICE_LIFE[6]` | 滚轮报警限制 | — |
| `SERVICE_LIFE[6]` | `SERVICE_LIFE[7]` | 夹具报警限制 | — |
| `SERVICE_LIFE[7]` | `SERVICE_LIFE[8]` | 金刚笔1报警限制 | — |
| `SERVICE_LIFE[8]` | `SERVICE_LIFE[9]` | 金刚笔2报警限制 | — |
| `SERVICE_LIFE[9]` | `SERVICE_LIFE[10]` | 预留 / 暂未使用 | — |
| `SERVICE_LIFE[10]` | `SERVICE_LIFE[11]` | 滚轮目前寿命 | — |
| `SERVICE_LIFE[11]` | `SERVICE_LIFE[12]` | 夹具目前寿命 | — |
| `SERVICE_LIFE[12]` | `SERVICE_LIFE[13]` | 金刚笔1目前寿命 | — |
| `SERVICE_LIFE[13]` | `SERVICE_LIFE[14]` | 金刚笔2目前寿命 | — |
| `SERVICE_LIFE[19]` | `SERVICE_LIFE[20]` | 是否报警 | — |

<a id="pi-sec-28"></a>

### 2.28 SERVICE_LIFE_TXT（7 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `SERVICE_LIFE_TXT[0]` | `SERVICE_LIFE_TXT[1]` | 滚轮寿命重置时间 | — |
| `SERVICE_LIFE_TXT[1]` | `SERVICE_LIFE_TXT[2]` | 夹具寿命重置时间 | — |
| `SERVICE_LIFE_TXT[2]` | `SERVICE_LIFE_TXT[3]` | 金刚笔1寿命重置时间 | — |
| `SERVICE_LIFE_TXT[3]` | `SERVICE_LIFE_TXT[4]` | 金刚笔2寿命重置时间 | — |
| `SERVICE_LIFE_TXT[4]` | `SERVICE_LIFE_TXT[5]` | 预留 / 暂未使用 | — |
| `SERVICE_LIFE_TXT[5]` | `SERVICE_LIFE_TXT[6]` | 滚轮编号 | — |
| `SERVICE_LIFE_TXT[6]` | `SERVICE_LIFE_TXT[7]` | 夹具编号 | — |

<a id="pi-sec-29"></a>

### 2.29 DRESS_WHEEL_NUM（1 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `DRESS_WHEEL_NUM[0]` | `DRESS_WHEEL_NUM[1]` | 滚轮编号1,依次类推共100个 | — |

<a id="pi-sec-30"></a>

### 2.30 DRESS_WHEEL_DATE（1 项）

| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `DRESS_WHEEL_DATE[0]` | `DRESS_WHEEL_DATE[1]` | 滚轮编号1的时间,依次类推共100个 | — |

<a id="mgud-extra-vars"></a>

## 3. `MGUD.DEF` 补充系统与备份变量表（22 项）

以下 22 项变量在 `MGUD.DEF` 中声明且被 `a_setting.com`、`a_backup_restore.com`、`a_stats.com`、`B_DRESS.SPF` 或 `D_BACKUP_ALL_PARA.SPF` 实际读写，但未在 `Parameter_Index.md` 中单独列出：

| NC 变量 / 范围（0-based） | HMI 引用 / 范围（1-based） | 类型 | 功能含义与来源 |
| :--- | :--- | :--- | :--- |
| `AXIS_EW` | `AXIS_EW` | `STRING[1]` | 磨削中心外圆砂轮切入轴名称（有 U 轴时为 `U`，共用轴时为 `X`，见 `C_PAR_INI.SPF` / `A_GRIND_CENTER.SPF`） |
| `WORM_SHAPE` | `WORM_SHAPE` | `STRING[20]` | 蜗杆专用齿形子程序名（初始化时写入 `SHAPE`） |
| `INI[257]` | `INI[258]` | `REAL` | `a_setting.com` `Mask0` SRAM 持久化随机挑战码种子变量（仅底层安全验证滚动更新） |
| `TRI[0]～TRI[19]` | `TRI[1]～TRI[20]` | `REAL[20]` | 三角齿形历史兼容参数数组（已逐步迁移至 `SHAPE_MODEL`，保留于整机备份表） |
| `TRAP[0]～TRAP[19]` | `TRAP[1]～TRAP[20]` | `REAL[20]` | 梯形齿形历史兼容参数数组（已逐步迁移至 `SHAPE_MODEL`，保留于整机备份表） |
| `DARC[0]～DARC[29]` | `DARC[1]～DARC[30]` | `REAL[30]` | 双圆弧齿形历史兼容参数数组（已逐步迁移至 `SHAPE_MODEL`，保留于整机备份表） |
| `PARA_LOCK_SWITCH[0]～PARA_LOCK_SWITCH[29]` | `PARA_LOCK_SWITCH[1]～PARA_LOCK_SWITCH[30]` | `INT[30]` | HMI 界面参数读写锁定开关预留数组（纳入 `D_BACKUP_ALL_PARA.SPF` 备份） |
| `CHOICE` | `CHOICE` | `REAL` | `a_backup_restore.com` 运行模式选择（`0` 正常加工 / `1` 备份数据 / `2` 恢复数据） |
| `BACKUP_TYPE` | `BACKUP_TYPE` | `REAL` | 备份范围模式（`0` 全量备份 MGUD / `1` 按自定义清单文件备份） |
| `BACKUP_POS` | `BACKUP_POS` | `REAL` | 备份目标介质位置（`0` 内置 / `1` 后 USB（不可写）/ `2` 前 USB / `3` CF 卡） |
| `RESTORE_POS` | `RESTORE_POS` | `REAL` | 恢复源介质位置（`0` 内置 / `1` 后 USB / `2` 前 USB / `3` CF 卡） |
| `FILE_LINE_COUNT` | `FILE_LINE_COUNT` | `REAL` | 自定义变量列表文件的总行数（含空行与 `;` 注释行） |
| `LIST_NAME` | `LIST_NAME` | `STRING[30]` | 自定义备份参数列表文件名（默认 `.TXT` 文档，不含扩展名） |
| `LIST_DIR` | `LIST_DIR` | `STRING[30]` | 自定义备份参数列表所在文件夹名（位于 `_N_SPF_DIR` 内） |
| `BACKUP_NAME` | `BACKUP_NAME` | `STRING[30]` | 生成的备份数据文件名 |
| `BACKUP_DIR` | `BACKUP_DIR` | `STRING[30]` | 生成的备份目标文件夹名 |
| `RESTORE_NAME` | `RESTORE_NAME` | `STRING[30]` | 待恢复的数据文件名 |
| `RESTORE_DIR` | `RESTORE_DIR` | `STRING[30]` | 待恢复的数据源文件夹名 |
| `BR_MSG` | `BR_MSG` | `STRING[150]` | `a_backup_restore.com` 备份/恢复执行状态与多语言提示消息 |
| `CUR_WHEEL` | `CUR_WHEEL` | `INT` | 当前砂轮更换记录序号（换轮后在 `B_DRESS.SPF` 中自增，范围 `1～99`） |
| `WHEEL_GRIND_CUMU[0]～WHEEL_GRIND_CUMU[99]` | `WHEEL_GRIND_CUMU[1]～WHEEL_GRIND_CUMU[100]` | `INT[100]` | 各期砂轮累计磨削工件计数台账（新轮切换时 `WHEEL_GRIND_CUMU[CUR_WHEEL]=0`） |
| `WHEEL_CHANGED_DATA[0]～WHEEL_CHANGED_DATA[99]` | `WHEEL_CHANGED_DATA[1]～WHEEL_CHANGED_DATA[100]` | `STRING[30][100]` | 各期砂轮更换日期时间戳台账（格式 `YYYY-MM-DD HH:MM`） |
