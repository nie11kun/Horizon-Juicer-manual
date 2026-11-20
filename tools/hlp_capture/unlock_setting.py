"""Unlock HMI '机床配置' (a_setting Mask0) for screenshot sessions.

Reads the 6-digit challenge from the HMI (shown after VS3), feeds it to HorizonJuicerCreator's own
'口令计算' page via the clipboard, copies the result back via the clipboard and types it into the HMI.
No algorithm is implemented here and the code is never printed or stored (clipboard is cleared).

Usage: python tools/hlp_capture/unlock_setting.py <challenge>
  (open 机床配置 first, press VS3, read the code at the bottom right of the HMI screen)
"""
import ctypes
import subprocess
import sys
import time

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except OSError:
    pass
import gen_package as g  # noqa: E402
import hmi  # noqa: E402


def _setclip(s):
    subprocess.run(["powershell", "-NoProfile", "-Command", f'Set-Clipboard -Value "{s}"'], check=True)


def _getclip():
    return subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
                          capture_output=True, text=True).stdout.strip()


def unlock(challenge):
    proc = subprocess.Popen([g.EXE])
    try:
        h = None
        for _ in range(60):
            h = g.find_window(proc.pid)
            if h:
                break
            time.sleep(0.2)
        time.sleep(3)
        g.click_rel(h, 0.50, 0.60, 1.5)      # 口令计算 card
        _setclip(challenge)
        time.sleep(0.3)
        g.click_rel(h, 0.711, 0.42, 1.0)     # 识别并粘贴
        _setclip("x")
        g.click_rel(h, 0.50, 0.734, 1.0)     # 复制解锁口令
        code = _getclip()
        _setclip(" ")
        if not code.isdigit():
            raise RuntimeError("calculator returned no numeric code")
        hmi.click(280, 93, 400)
        hmi.keys(code, 300)
        hmi.keys("{ENTER}", 1500)
        print("entered", len(code), "digits")
    finally:
        proc.kill()


if __name__ == "__main__":
    unlock(sys.argv[1])
