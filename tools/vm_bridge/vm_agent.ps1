param(
    [Parameter(Mandatory=$true)]
    [string]$BridgeDir
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms

Add-Type @"
using System;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Text;

public static class VmWin32 {
    [DllImport("user32.dll")]
    public static extern bool SetProcessDPIAware();

    [DllImport("user32.dll")]
    public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);

    public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern bool EnumWindows(EnumWindowsProc enumProc, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);

    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);

    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

    [DllImport("user32.dll")]
    public static extern bool IsIconic(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int X, int Y);

    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);

    [StructLayout(LayoutKind.Sequential)]
    public struct RECT {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }

    public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
    public const uint MOUSEEVENTF_LEFTUP   = 0x0004;

    [DllImport("user32.dll")]
    public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);

    // Prefer the HMI window (title contains 840D); in split-window mode the panel window lacks it.
    public static IntPtr FindSinuTrainWindow(out string title, out RECT rect) {
        IntPtr found = IntPtr.Zero, fallback = IntPtr.Zero;
        string foundTitle = "", fallbackTitle = "";
        RECT foundRect = new RECT(), fallbackRect = new RECT();
        EnumWindows((hWnd, lParam) => {
            if (!IsWindowVisible(hWnd)) return true;
            StringBuilder sb = new StringBuilder(512);
            GetWindowText(hWnd, sb, 512);
            string t = sb.ToString();
            if (t.Contains("SinuTrain for SINUMERIK Operate") || t.Contains("SINUMERIK Operate")) {
                RECT r;
                if (GetWindowRect(hWnd, out r) && (r.Right - r.Left) > 600 && (r.Bottom - r.Top) > 400) {
                    if (t.Contains("840D")) {
                        found = hWnd; foundTitle = t; foundRect = r;
                        return false;
                    }
                    if (fallback == IntPtr.Zero) { fallback = hWnd; fallbackTitle = t; fallbackRect = r; }
                }
            }
            return true;
        }, IntPtr.Zero);
        if (found == IntPtr.Zero) { found = fallback; foundTitle = fallbackTitle; foundRect = fallbackRect; }
        title = foundTitle;
        rect = foundRect;
        return found;
    }

    public static void LeftClick(int x, int y) {
        SetCursorPos(x, y);
        System.Threading.Thread.Sleep(60);
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(40);
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, UIntPtr.Zero);
    }
}
"@

[void][VmWin32]::SetProcessDPIAware()

$SinuTrainHmiDir = "C:\Siemens\SinuTrain\SINUMERIK CNC-SW 840D sl 4.8 SP4\hmi"
$BackupDir = "C:\Temp\hj_sinutrain_hmi_backup"
$OutDir = Join-Path $BridgeDir "out"
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }

$HeartbeatFile = Join-Path $BridgeDir "heartbeat.json"
$CmdFile = Join-Path $BridgeDir "cmd.json"

function Get-ScreenAndWindowInfo {
    $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $title = ""
    $rect = New-Object VmWin32+RECT
    $hwnd = [VmWin32]::FindSinuTrainWindow([ref]$title, [ref]$rect)
    return @{
        timestamp = (Get-Date).ToString("o")
        epoch = [int64](([DateTimeOffset]::UtcNow).ToUnixTimeSeconds())
        machine = $env:COMPUTERNAME
        screenWidth = $bounds.Width
        screenHeight = $bounds.Height
        sinutrainHmiExists = (Test-Path $SinuTrainHmiDir)
        sinutrainHwnd = [int64]$hwnd
        sinutrainTitle = $title
        sinutrainRect = @{
            left = $rect.Left
            top = $rect.Top
            right = $rect.Right
            bottom = $rect.Bottom
            width = ($rect.Right - $rect.Left)
            height = ($rect.Bottom - $rect.Top)
        }
    }
}

function Capture-RegionToPng([int]$x, [int]$y, [int]$w, [int]$h, [string]$destPath) {
    $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $sx = [Math]::Max($bounds.X, $x)
    $sy = [Math]::Max($bounds.Y, $y)
    $sw = [Math]::Max(1, [Math]::Min($bounds.Right - $sx, ($x + $w) - $sx))
    $sh = [Math]::Max(1, [Math]::Min($bounds.Bottom - $sy, ($y + $h) - $sy))
    $bmp = New-Object System.Drawing.Bitmap($sw, $sh)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($sx, $sy, 0, 0, (New-Object System.Drawing.Size($sw, $sh)))
    $g.Dispose()
    $bmp.Save($destPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
}

function Write-Heartbeat {
    $info = Get-ScreenAndWindowInfo
    $json = $info | ConvertTo-Json -Depth 5
    [System.IO.File]::WriteAllText($HeartbeatFile, $json, [System.Text.UTF8Encoding]::new($false))
}

function Invoke-BridgeCommand($cmdObj) {
    $action = $cmdObj.action
    $result = @{ id = $cmdObj.id; action = $action; ok = $true; message = "" }

    try {
        switch ($action) {
            "status" {
                $result.data = Get-ScreenAndWindowInfo
            }
            "backup_hmi" {
                if (-not (Test-Path $SinuTrainHmiDir)) { throw "HMI dir not found: $SinuTrainHmiDir" }
                if (-not (Test-Path $BackupDir)) { New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null }
                $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
                $snapDir = Join-Path $BackupDir $stamp
                New-Item -ItemType Directory -Force -Path $snapDir | Out-Null
                foreach ($sub in @("user", "oem", "siemens")) {
                    $src = Join-Path $SinuTrainHmiDir $sub
                    if (Test-Path $src) {
                        Copy-Item -Path $src -Destination (Join-Path $snapDir $sub) -Recurse -Force
                    }
                }
                [System.IO.File]::WriteAllText((Join-Path $BackupDir "latest.txt"), $snapDir, [System.Text.UTF8Encoding]::new($false))
                $result.data = @{ backupDir = $snapDir }
                $result.message = "HMI backed up to $snapDir"
            }
            "restore_hmi" {
                $snapDir = $cmdObj.backupDir
                if ([string]::IsNullOrWhiteSpace($snapDir)) {
                    $latestFile = Join-Path $BackupDir "latest.txt"
                    if (-not (Test-Path $latestFile)) { throw "No backup record found" }
                    $snapDir = (Get-Content $latestFile -Raw).Trim()
                }
                if (-not (Test-Path $snapDir)) { throw "Backup dir not found: $snapDir" }
                $skipped = 0
                foreach ($sub in @("user", "oem", "siemens")) {
                    $src = Join-Path $snapDir $sub
                    $dst = Join-Path $SinuTrainHmiDir $sub
                    if (Test-Path $src) {
                        if (-not (Test-Path $dst)) { New-Item -ItemType Directory -Force -Path $dst | Out-Null }
                        foreach ($item in (Get-ChildItem -LiteralPath $src -Recurse -File)) {
                            $rel = $item.FullName.Substring($src.Length).TrimStart("\")
                            $targetFile = Join-Path $dst $rel
                            $targetDir = Split-Path -Parent $targetFile
                            if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Force -Path $targetDir | Out-Null }
                            try {
                                Copy-Item -LiteralPath $item.FullName -Destination $targetFile -Force -ErrorAction Stop
                            } catch {
                                $skipped++
                            }
                        }
                    }
                }
                $cacheHlp = Join-Path $SinuTrainHmiDir "siemens\sinumerik\sys_cache\hmi\hlp"
                if (Test-Path $cacheHlp) { Remove-Item -Path $cacheHlp -Recurse -Force -ErrorAction SilentlyContinue }
                $result.data = @{ skippedLocked = $skipped }
                $result.message = "Restored HMI from $snapDir (skippedLocked=$skipped)"
            }
            "import_cf" {
                $pkgRel = $cmdObj.packageSubDir
                $pkgCfDir = Join-Path $BridgeDir ("packages\" + $pkgRel + "\System-CF-Card")
                if (-not (Test-Path $pkgCfDir)) { throw "System-CF-Card not found: $pkgCfDir" }
                foreach ($sub in @("user", "oem", "siemens")) {
                    $src = Join-Path $pkgCfDir $sub
                    $dst = Join-Path $SinuTrainHmiDir $sub
                    if (Test-Path $src) {
                        if (-not (Test-Path $dst)) { New-Item -ItemType Directory -Force -Path $dst | Out-Null }
                        Copy-Item -Path (Join-Path $src "*") -Destination $dst -Recurse -Force
                    }
                }
                $cacheHlp = Join-Path $SinuTrainHmiDir "siemens\sinumerik\sys_cache\hmi\hlp"
                if (Test-Path $cacheHlp) { Remove-Item -Path $cacheHlp -Recurse -Force -ErrorAction SilentlyContinue }
                $result.message = "Imported System-CF-Card from $pkgRel"
            }
            "screenshot" {
                $info = Get-ScreenAndWindowInfo
                $hwnd = [IntPtr][int64]$info.sinutrainHwnd
                if ($hwnd -eq [IntPtr]::Zero) { throw "SinuTrain window not found" }
                if ([VmWin32]::IsIconic($hwnd)) { [void][VmWin32]::ShowWindow($hwnd, 9) }
                [void][VmWin32]::SetForegroundWindow($hwnd)
                Start-Sleep -Milliseconds 300
                $info = Get-ScreenAndWindowInfo
                $r = $info.sinutrainRect
                $fullName = if ($cmdObj.filename) { $cmdObj.filename } else { "shot.png" }
                $fullPath = Join-Path $OutDir $fullName
                Capture-RegionToPng $r.left $r.top $r.width $r.height $fullPath
                $result.data = @{
                    fullPath = $fullPath
                    rect = $r
                }
                $result.message = "Captured $fullName"
            }
            "click_rel" {
                $info = Get-ScreenAndWindowInfo
                $hwnd = [IntPtr][int64]$info.sinutrainHwnd
                if ($hwnd -eq [IntPtr]::Zero) { throw "SinuTrain window not found" }
                [void][VmWin32]::SetForegroundWindow($hwnd)
                Start-Sleep -Milliseconds 120
                $r = $info.sinutrainRect
                $rx = [double]$cmdObj.rx
                $ry = [double]$cmdObj.ry
                $px = [int][Math]::Round($r.left + $r.width * $rx)
                $py = [int][Math]::Round($r.top + $r.height * $ry)
                [VmWin32]::LeftClick($px, $py)
                $waitMs = if ($cmdObj.waitMs) { [int]$cmdObj.waitMs } else { 400 }
                Start-Sleep -Milliseconds $waitMs
                $result.data = @{ clickedX = $px; clickedY = $py }
            }
            "send_keys" {
                $info = Get-ScreenAndWindowInfo
                $hwnd = [IntPtr][int64]$info.sinutrainHwnd
                if ($hwnd -ne [IntPtr]::Zero) {
                    [void][VmWin32]::SetForegroundWindow($hwnd)
                    Start-Sleep -Milliseconds 120
                }
                [System.Windows.Forms.SendKeys]::SendWait($cmdObj.keys)
                $waitMs = if ($cmdObj.waitMs) { [int]$cmdObj.waitMs } else { 300 }
                Start-Sleep -Milliseconds $waitMs
            }
            "move_window" {
                $info = Get-ScreenAndWindowInfo
                $hwnd = [IntPtr][int64]$info.sinutrainHwnd
                if ($hwnd -eq [IntPtr]::Zero) { throw "SinuTrain window not found" }
                [void][VmWin32]::ShowWindow($hwnd, 9)
                [void][VmWin32]::MoveWindow($hwnd, [int]$cmdObj.x, [int]$cmdObj.y, [int]$cmdObj.w, [int]$cmdObj.h, $true)
                [void][VmWin32]::SetForegroundWindow($hwnd)
                Start-Sleep -Milliseconds 600
                $result.data = Get-ScreenAndWindowInfo
            }
            "maximize" {
                $info = Get-ScreenAndWindowInfo
                $hwnd = [IntPtr][int64]$info.sinutrainHwnd
                if ($hwnd -eq [IntPtr]::Zero) { throw "SinuTrain window not found" }
                [void][VmWin32]::ShowWindow($hwnd, 3)
                [void][VmWin32]::SetForegroundWindow($hwnd)
                Start-Sleep -Milliseconds 300
                $result.data = Get-ScreenAndWindowInfo
            }
            default {
                throw "Unknown action: $action"
            }
        }
    } catch {
        $result.ok = $false
        $result.message = $_.Exception.Message
    }

    $respFile = Join-Path $BridgeDir ("resp_" + $cmdObj.id + ".json")
    $respJson = $result | ConvertTo-Json -Depth 6
    [System.IO.File]::WriteAllText($respFile, $respJson, [System.Text.UTF8Encoding]::new($false))
}

Write-Host "VM Bridge Agent started. Monitoring: $BridgeDir"
while ($true) {
    try {
        Write-Heartbeat
        if (Test-Path $CmdFile) {
            Start-Sleep -Milliseconds 80
            $raw = [System.IO.File]::ReadAllText($CmdFile, [System.Text.UTF8Encoding]::new($false))
            Remove-Item $CmdFile -Force -ErrorAction SilentlyContinue
            if (-not [string]::IsNullOrWhiteSpace($raw)) {
                $cmdObj = $raw | ConvertFrom-Json
                Write-Host ("[$(Get-Date -Format HH:mm:ss)] Executing: $($cmdObj.action) ($($cmdObj.id))")
                Invoke-BridgeCommand $cmdObj
            }
        }
    } catch {
        Write-Host "Loop error: $($_.Exception.Message)"
    }
    Start-Sleep -Milliseconds 400
}
