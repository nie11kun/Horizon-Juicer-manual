# 第 10 章 报警参考、信号定义与变量字典

本章汇集现场电气调试、售后维修及程序二次开发所需的核心底层查考资料，全部参数与代码均与 `Horizon-Juicer` 源码库及 `HorizonJuicerCreator V3.29.0` 生成输出保持严格一致：

- [10.1 报警代码对照表与现场常见问题](alarms_and_faq.md) —— `C_ALARM.SPF` 全套 14 项 `DRESSER[6]` 报警原因与处理、配件寿命与授权停机提示、密码页状态诊断及现场 FAQ；
- [10.2 全量 M 代码表与 PLC-NC 交互信号](m_codes_and_signals.md) —— `M0`～`M99` 逐号全量 M 代码（含 `M206`/`M03`/`M04` 扩展说明）、`M80`～`M97` 桁架机器人握手、<code>&#36;A_DBB</code> 与 `DB4900` 全量 46 项交换表及 14 项快速 I/O 与测头接口；
- [10.3 全量配置界面对应变量表](config_ui_variables.md) —— 机床端 `a_setting.com`（`Mask1` 6 大类 93 项可见配置 + `PROCESS[122]` + 9 项后台隐藏变量 + `SUB(UP1)`～`SUB(UP9)` 动态读写联动）及 PC 端 `HorizonJuicerCreator` 31 项 JSON 配置全量对照；
- [10.4 全量全局变量与 R 参数索引表](full_variable_index.md) —— `0-based` vs `1-based` 索引转换铁律、`MGUD.DEF` 全部 60 项声明总览、`Parameter_Index.md` 全部 30 个分类 1,553 条变量全量展开（对应全部 1,561 个数据行）及 22 项补充系统/备份变量；
- [10.5 条件编译与字符替换标记全表](replace_markers.md) —— 4 种源码/HTML 替换标记语法、`ReplaceMarker.md` 与 `generatepro.cpp` 全部 66 项 `;ifIs...` 条件编译裁剪规则、12 项元数据占位替换以及 `oneReplace.json` 47 项 Sinumerik ONE 跨平台信号映射。
