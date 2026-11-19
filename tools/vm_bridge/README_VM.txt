Horizon-Juicer SinuTrain 虚拟机实时截图桥接说明
=============================================

1. 请确保 VMware 虚拟机中已开启“共享文件夹”，宿主机路径
   C:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer-manual
   对应虚拟机内的共享目录：
   \\vmware-host\Shared Folders\Development\WorkProgram\Horizon-Juicer-manual

2. 在虚拟机桌面或资源管理器打开：
   \\vmware-host\Shared Folders\Development\WorkProgram\Horizon-Juicer-manual\tools\vm_bridge

3. 双击运行 vm_agent.bat（保持弹出的命令行窗口处于打开状态，请勿关闭）。

4. 运行后，宿主机将自动：
   - 备份您虚拟机当前的 SinuTrain hmi 目录；
   - 导入测试程序包并通过语言切换刷新界面；
   - 自动操作 SinuTrain 并保存完整窗口图及裁剪后的高清 HMI 纯画面图；
   - 完成后自动还原您原本的 SinuTrain hmi 目录。
