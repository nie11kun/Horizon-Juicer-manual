# 第 4 章 真机部署与 SinuTrain 仿真

完成程序包生成后，即可进入部署或仿真验证阶段。本章涵盖两种完全不同的目标运行环境及其关键配置细节：

- [4.1 真机 NC-Data 与 CF 卡部署流程](real_machine_deploy.md) —— 面向 SINUMERIK 828D（老版/新版）、Sinumerik ONE 及 840D sl 实机的系统导入、GUD 内存参数调整（`MD18120`）、USB 逻辑驱动器配置与缓存清除方法；
- [4.2 SinuTrain 4.8 SP4 仿真导入与缓存刷新](sinutrain_simulation.md) —— 面向 VM 虚拟机或本机 `SinuTrain for SINUMERIK Operate 4.8 SP4` 的一键界面导入、语言切换热刷新与实时效果查验。

## 部署前 5 项必检清单（现场通用）

| 检查序号 | 核心核对项 | 标准要求 / 操作提醒 |
| :---: | :--- | :--- |
| **1** | **NC 内存参数** | 激活新版 `MGUD.DEF` 前确保 `MD18120 >= 70`（`MM_NUM_GUD_NAMES_NCK`），避免全局变量内存不足报错 |
| **2** | **旧版 GUD 备份** | 若将旧控制器升级至含 `TECHNOLOGY[500]` 的新版 `MGUD.DEF`，重新激活前务必先**备份原有 GUD 数据**，防止已有标定参数清零 |
| **3** | **严格导入顺序** | 先导入并 **激活** `NC-Data/DEF/MGUD.DEF`，随后才导入 `NC-Data/CMA/*.SPF` 与 `NC-Data/MPF/<机床型号>.MPF` |
| **4** | **首次重置（必做）** | 新设备或重建 `MGUD.DEF` 后，必须解锁 **机床配置** 执行一次 **`VS3 重置数据 → Mask2 VS8 确认`**，写入驱动类型（`INI[36]`/`INI[37]`/`INI[91]`）与权限锁 |
| **5** | **缓存与外设接口** | 更新 `hlp` 后清理 `sys_cache/hmi/hlp` 并用 `VS3 Change language` 刷新；前置 USB 须配置 `extdev.ini`，后置 USB 逻辑名须设为 `//DEV_3` |
