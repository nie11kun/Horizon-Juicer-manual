# Summary

* [前言：系统概览与手册导航](README.md)

## 第一部分：HorizonJuicerCreator 配置生成软件指南

* [第 1 章 软件入门与路径配置](1_creator_getting_started/README.md)
  * [1.1 主工作台、菜单栏与版本历史](1_creator_getting_started/ui_overview.md)
  * [1.2 源仓库与输出目录设置](1_creator_getting_started/path_settings.md)
* [第 2 章 机床配置与程序生成](2_creator_machine_config/README.md)
  * [2.1 机床信息、系统平台与安全选项](2_creator_machine_config/machine_and_system_info.md)
  * [2.2 机床结构、修整器与硬件选配联动](2_creator_machine_config/structure_options.md)
  * [2.3 生成目录结构与规格编码解析](2_creator_machine_config/output_structure.md)
* [第 3 章 辅助工具箱](3_creator_tools/README.md)
  * [3.1 系统动态解锁口令计算器](3_creator_tools/password_calculator.md)
  * [3.2 批量删除程序注释工具](3_creator_tools/remove_comments.md)

## 第二部分：程序部署与系统管理

* [第 4 章 真机部署与 SinuTrain 仿真](4_deployment_and_sinutrain/README.md)
  * [4.1 真机 NC-Data 与 CF 卡部署流程](4_deployment_and_sinutrain/real_machine_deploy.md)
  * [4.2 SinuTrain 4.8 SP4 仿真导入与缓存刷新](4_deployment_and_sinutrain/sinutrain_simulation.md)
* [第 5 章 系统主页、底层设置、统计与备份](5_custom_and_system/README.md)
  * [5.1 CUSTOM 主页导航与设备编号信息](5_custom_and_system/custom_home.md)
  * [5.2 机床系统配置与安全解锁](5_custom_and_system/machine_settings.md)
  * [5.3 加工统计、砂轮记录与配件寿命管理](5_custom_and_system/stats_and_life.md)
  * [5.4 NC 全局参数备份与恢复](5_custom_and_system/backup_and_restore.md)

## 第三部分：Horizon-Juicer 机床操作与工艺功能指南

* [第 6 章 螺纹磨削与工艺参数](6_thread_grinding/README.md)
  * [6.1 主磨削参数与手动对刀操作](6_thread_grinding/main_grinding.md)
  * [6.2 工艺参数表、附加配置、Y 轴与 UW 挡块](6_thread_grinding/process_params.md)
  * [6.3 丝锥、蜗杆与环形槽专用功能](6_thread_grinding/tap_worm_ring.md)
  * [6.4 高级模块（上）：夹具自磨、倒角、空运行与两端变径](6_thread_grinding/advanced_modules.md)
  * [6.5 高级模块（下）：分段补偿与单/多段螺距变换](6_thread_grinding/seg_comp_and_pitch.md)
* [第 7 章 砂轮修整、滚轮与齿形模型](7_dressing_and_shapes/README.md)
  * [7.1 砂轮修整主参数与新/旧砂轮策略](7_dressing_and_shapes/dressing_main.md)
  * [7.2 滚轮类型与修整中心校准方法](7_dressing_and_shapes/wheel_setup.md)
  * [7.3 齿形参数、通用齿形模型与多线/外部轨迹](7_dressing_and_shapes/shape_profiles.md)
* [第 8 章 自动对刀系统](8_auto_tool_setting/README.md)
  * [8.1 外螺纹自动对刀标定与测量](8_auto_tool_setting/external_auto_set.md)
  * [8.2 内螺纹与磨削中心自动对刀标定](8_auto_tool_setting/internal_auto_set.md)
* [第 9 章 磨削中心复合功能](9_grinding_center/README.md)
  * [9.1 加工选择看板与多工序联合调度](9_grinding_center/center_overview.md)
  * [9.2 外圆与外圆台阶磨削及修整](9_grinding_center/cylindrical_and_step.md)
  * [9.3 左右端面磨削、修整及交叉补偿](9_grinding_center/endface_grinding.md)

## 第四部分：附录与故障排查

* [第 10 章 报警参考、信号定义与变量字典](10_appendix_and_troubleshooting/README.md)
  * [10.1 报警代码对照表与现场常见问题](10_appendix_and_troubleshooting/alarms_and_faq.md)
  * [10.2 全量 M 代码表与 PLC-NC 交互信号](10_appendix_and_troubleshooting/m_codes_and_signals.md)
  * [10.3 全量配置界面对应变量表](10_appendix_and_troubleshooting/config_ui_variables.md)
  * [10.4 全量全局变量与 R 参数索引表](10_appendix_and_troubleshooting/full_variable_index.md)
  * [10.5 条件编译与字符替换标记全表](10_appendix_and_troubleshooting/replace_markers.md)
