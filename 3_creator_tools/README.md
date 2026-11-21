# 第 3 章 辅助工具箱

除核心的程序裁剪生成工作流外，`HorizonJuicerCreator` 主工作台还内置了两款独立的工程实用工具，分别服务于现场调试解锁与交付代码清理：

- [3.1 系统动态解锁口令计算器](password_calculator.md) —— 为调试/售后人员计算进入机床端 **机床配置**（`a_setting.com`）底层设定页所需的 6 位动态密码或历史版口令（提供 `HorizonJuicerCreator` 桌面端及需向管理员申请账户密码的网页版 [https://hjpc.niekun.net/](https://hjpc.niekun.net/)）；
- [3.2 批量删除程序注释工具](remove_comments.md) —— 脱离主生成流程，独立对任意存量或手改程序目录递归清理 `;` 行尾注释，同时完整保留结构化标签注释。
