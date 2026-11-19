# 第 10 章 报警参考、信号定义与变量字典

本章汇集现场电气调试、售后维修及程序二次开发所需的核心底层查考资料，全部参数与代码均与 `Horizon-Juicer` 源码库及 `HorizonJuicerCreator V3.29.0` 生成输出保持严格一致：

- [10.1 报警代码对照表与现场常见问题](alarms_and_faq.md) —— `C_ALARM.SPF` 全套 14 项 `DRESSER[6]` 报警原因与处理、配件寿命与授权停机提示、密码页状态诊断及现场 FAQ；
- [10.2 M 代码、PLC-NC 交互信号与机械手接口](m_codes_and_signals.md) —— `M0`～`M99` 系统/定制 M 代码、`M80`～`M97` 桁架机器人握手信号、<code>&#36;A_DBB</code> 与 `DB4900` 交换表、`Sinumerik ONE` 信号差异及在线量仪/测头接口；
- [10.3 MGUD 全局变量索引与条件编译标记](variables_and_markers.md) —— `MGUD.DEF` 全局变量数组总览、`R` 参数占用约定、`0-based` vs `1-based` 索引转换铁律以及全部 `;ifIs...` 条件编译裁剪标记对照。
