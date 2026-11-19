@echo off
chcp 65001 >nul
setlocal
set "BRIDGE_DIR=%~dp0"
if "%BRIDGE_DIR:~-1%"=="\" set "BRIDGE_DIR=%BRIDGE_DIR:~0,-1%"
set "AGENT_LOCAL=%TEMP%\hj_vm_agent.ps1"
copy /Y "%BRIDGE_DIR%\vm_agent.ps1" "%AGENT_LOCAL%" >nul
echo ========================================================================
echo  Horizon-Juicer SinuTrain VM Bridge Agent
echo  Bridge Folder: %BRIDGE_DIR%
echo  Keep this window open while screenshots are being captured.
echo ========================================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%AGENT_LOCAL%" -BridgeDir "%BRIDGE_DIR%"
pause
