"""
Automated screenshot and demo package capture script for HorizonJuicerCreator.exe.
Uses Win32 PostMessage (WM_LBUTTONDOWN/WM_LBUTTONUP) in client coordinates +
PrintWindow(hwnd, dc, 2) so it works reliably even in non-interactive sessions.
Safely backs up and restores C:/Users/<user>/HorizonJuicerCreator.json.
"""

import ctypes
from ctypes import wintypes
import json
import os
import subprocess
import time
from PIL import Image

EXE_PATH = r"C:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer\HorizonJuicerCreator\HorizonJuicerCreator.exe"
USER_CFG = os.path.expanduser(r"~\HorizonJuicerCreator.json")
MANUAL_DIR = r"c:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer-manual"
IMG_DIR = os.path.join(MANUAL_DIR, "images")
DEMO_DEST = os.path.join(
    r"C:\Users\Marco Nie\.gemini\antigravity\brain\4170654c-8b49-4f7b-996b-4304aec2104a\scratch\demo_packages"
)

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(DEMO_DEST, exist_ok=True)

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
user32.SetProcessDPIAware()


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


def list_windows_by_pid(pid):
    results = []

    def cb(hwnd, lparam):
        if not user32.IsWindowVisible(hwnd):
            return True
        wpid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(wpid))
        if wpid.value == pid:
            buf = ctypes.create_unicode_buffer(512)
            user32.GetWindowTextW(hwnd, buf, 512)
            r = RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(r))
            w = r.right - r.left
            h = r.bottom - r.top
            if w > 200 and h > 150:
                results.append((hwnd, buf.value, r))
        return True

    user32.EnumWindows(WNDENUMPROC(cb), 0)
    return results


def capture_hwnd(hwnd, filepath):
    r = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    w = r.right - r.left
    h = r.bottom - r.top
    hwnd_dc = user32.GetWindowDC(hwnd)
    mfc_dc = gdi32.CreateCompatibleDC(hwnd_dc)
    bmp = gdi32.CreateCompatibleBitmap(hwnd_dc, w, h)
    gdi32.SelectObject(mfc_dc, bmp)
    ok = user32.PrintWindow(hwnd, mfc_dc, 2)
    if not ok:
        user32.PrintWindow(hwnd, mfc_dc, 0)

    bmpinfo = bytearray(40)
    ctypes.c_uint32.from_buffer(bmpinfo, 0).value = 40
    ctypes.c_int32.from_buffer(bmpinfo, 4).value = w
    ctypes.c_int32.from_buffer(bmpinfo, 8).value = -h
    ctypes.c_uint16.from_buffer(bmpinfo, 12).value = 1
    ctypes.c_uint16.from_buffer(bmpinfo, 14).value = 32
    ctypes.c_uint32.from_buffer(bmpinfo, 16).value = 0

    buf = bytearray(w * h * 4)
    gdi32.GetDIBits(
        mfc_dc,
        bmp,
        0,
        h,
        (ctypes.c_char * len(buf)).from_buffer(buf),
        bytes(bmpinfo),
        0,
    )
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(mfc_dc)
    user32.ReleaseDC(hwnd, hwnd_dc)

    img = Image.frombuffer("RGBA", (w, h), buf, "raw", "BGRA", 0, 1).convert("RGB")
    extrema = img.getextrema()
    is_blank = all(mx < 15 for _, mx in extrema)
    img.save(filepath)
    print(f"Captured {os.path.basename(filepath)} ({w}x{h}) blank={is_blank}")
    return img


def wait_for_window(pid, title_contains=None, exclude_hwnds=None, timeout=10.0):
    exclude_hwnds = exclude_hwnds or set()
    t0 = time.time()
    while time.time() - t0 < timeout:
        wins = list_windows_by_pid(pid)
        for hwnd, title, r in wins:
            if hwnd in exclude_hwnds:
                continue
            if title_contains is None or title_contains in title:
                return hwnd, title, r
        time.sleep(0.2)
    return None, None, None


def post_click_rel(hwnd, rx, ry, wait=0.5):
    cr = RECT()
    user32.GetClientRect(hwnd, ctypes.byref(cr))
    x = int(round(cr.right * rx))
    y = int(round(cr.bottom * ry))
    lp = (y << 16) | (x & 0xFFFF)
    user32.PostMessageW(hwnd, 0x0200, 0, lp)  # WM_MOUSEMOVE
    user32.PostMessageW(hwnd, 0x0201, 1, lp)  # WM_LBUTTONDOWN
    time.sleep(0.06)
    user32.PostMessageW(hwnd, 0x0202, 0, lp)  # WM_LBUTTONUP
    time.sleep(wait)


def post_key(hwnd, vk, wait=0.25):
    user32.PostMessageW(hwnd, 0x0100, vk, 0)
    time.sleep(0.05)
    user32.PostMessageW(hwnd, 0x0101, vk, 0)
    time.sleep(wait)


def kill_proc(proc):
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


def write_cfg(cfg):
    with open(USER_CFG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)


def main():
    backup_data = None
    if os.path.exists(USER_CFG):
        with open(USER_CFG, "r", encoding="utf-8") as f:
            backup_data = f.read()

    try:
        base_cfg = json.loads(backup_data) if backup_data else {}

        # ------------------------------------------------------------
        # Pass 1: Main workbench + dialogs + password calc + comments + External Demo
        # ------------------------------------------------------------
        ext_cfg = dict(base_cfg)
        ext_cfg.update({
            "machineName": "SK7420",
            "machineNameLng": "外螺纹数控丝锥磨床",
            "machineIndex": "01",
            "customInfo": "DemoPlant",
            "lng": 0,
            "machineType": 0,
            "ifHasScrewTap": 0,
            "wareType": 0,
            "ifHasWorm": 1,
            "wheelType": 0,
            "shapeType": 0,
            "ifHasReOp": 0,
            "ifOperation": 0,
            "measureMethord": 0,
            "probePos": 0,
            "ifCenter": 1,
            "ifHasU": 1,
            "ifNotHasUExternalPos": 0,
            "ifHasA": 0,
            "grindWheelType": 0,
            "exGrindWheelType": 0,
            "dressWheelType": 0,
            "ifRemoveComments": 1,
            "hmiMode": 0,
            "systemMode": 0,
            "ifHasLoadingArm": 0,
            "ifHasEncryption": 0,
            "ifHasNoneTradeMark": 0,
            "programDir": {
                "sourceDir": r"C:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer",
                "destDir": DEMO_DEST,
            },
        })
        write_cfg(ext_cfg)

        proc = subprocess.Popen([EXE_PATH])
        try:
            main_hwnd, title, r = wait_for_window(proc.pid, "HorizonJuicerCreator", timeout=12)
            if not main_hwnd:
                raise RuntimeError("Main window did not appear")
            time.sleep(1.0)
            capture_hwnd(main_hwnd, os.path.join(IMG_DIR, "creator_main_workbench.png"))

            # Click "打开" in menubar (top left client area) -> Down + Enter to open 参数设置
            post_click_rel(main_hwnd, 0.025, 0.015, wait=0.35)
            post_key(main_hwnd, 0x28, wait=0.15)  # VK_DOWN
            post_key(main_hwnd, 0x0D, wait=0.5)   # VK_RETURN
            set_hwnd, _, _ = wait_for_window(proc.pid, "设置", exclude_hwnds={main_hwnd}, timeout=4)
            if set_hwnd:
                time.sleep(0.35)
                capture_hwnd(set_hwnd, os.path.join(IMG_DIR, "creator_settings_dialog.png"))
                user32.PostMessageW(set_hwnd, 0x0010, 0, 0)
                time.sleep(0.35)

            # Click "帮助" in menubar -> Down -> Down -> Enter for 版本历史
            post_click_rel(main_hwnd, 0.068, 0.015, wait=0.35)
            post_key(main_hwnd, 0x28, wait=0.12)
            post_key(main_hwnd, 0x28, wait=0.12)
            post_key(main_hwnd, 0x0D, wait=0.5)
            hist_hwnd, _, _ = wait_for_window(proc.pid, "版本", exclude_hwnds={main_hwnd}, timeout=4)
            if hist_hwnd:
                time.sleep(0.35)
                capture_hwnd(hist_hwnd, os.path.join(IMG_DIR, "creator_about_history.png"))
                user32.PostMessageW(hist_hwnd, 0x0010, 0, 0)
                time.sleep(0.35)

            # Card 2: 口令计算 (center card) - leave input empty so no secret algorithm pair is exposed
            post_click_rel(main_hwnd, 0.50, 0.56, wait=0.6)
            capture_hwnd(main_hwnd, os.path.join(IMG_DIR, "creator_password_calc.png"))
            # Back button (top-left of central container)
            post_click_rel(main_hwnd, 0.16, 0.075, wait=0.5)

            # Card 3: 删除注释 (right card)
            post_click_rel(main_hwnd, 0.79, 0.56, wait=0.6)
            capture_hwnd(main_hwnd, os.path.join(IMG_DIR, "creator_remove_comments.png"))
            post_click_rel(main_hwnd, 0.16, 0.075, wait=0.5)

            # Card 1: 机床配置 (left card) - External machine
            post_click_rel(main_hwnd, 0.21, 0.56, wait=0.7)
            capture_hwnd(main_hwnd, os.path.join(IMG_DIR, "creator_config_external.png"))

            # Click "程序生成" (bottom right button)
            post_click_rel(main_hwnd, 0.83, 0.94, wait=0.5)
            t0 = time.time()
            while time.time() - t0 < 40:
                if os.path.exists(os.path.join(DEMO_DEST, "SK7420(#01-DemoPlant)", "NC-Data", "MPF", "SK7420.MPF")):
                    time.sleep(1.8)
                    break
                time.sleep(0.5)
        finally:
            kill_proc(proc)
            time.sleep(0.5)

        # ------------------------------------------------------------
        # Pass 2: Internal Grinding Center (SKR7620B, old 828D mode for SinuTrain 4.8 SP4)
        # ------------------------------------------------------------
        ctr_cfg = dict(base_cfg)
        ctr_cfg.update({
            "machineName": "SKR7620B",
            "machineNameLng": "内螺纹磨削中心",
            "machineIndex": "02",
            "customInfo": "DemoCenter",
            "lng": 0,
            "machineType": 1,
            "ifHasScrewTap": 1,
            "wareType": 2,
            "ifHasWorm": 0,
            "wheelType": 0,
            "shapeType": 0,
            "ifHasReOp": 1,
            "ifOperation": 0,
            "measureMethord": 1,
            "probePos": 0,
            "ifCenter": 0,
            "ifHasU": 0,
            "ifNotHasUExternalPos": 0,
            "ifHasA": 0,
            "grindWheelType": 0,
            "exGrindWheelType": 0,
            "dressWheelType": 0,
            "ifRemoveComments": 1,
            "hmiMode": 0,
            "systemMode": 0,
            "ifHasLoadingArm": 0,
            "ifHasEncryption": 0,
            "ifHasNoneTradeMark": 0,
            "programDir": {
                "sourceDir": r"C:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer",
                "destDir": DEMO_DEST,
            },
        })
        write_cfg(ctr_cfg)
        proc2 = subprocess.Popen([EXE_PATH])
        try:
            main_hwnd, _, _ = wait_for_window(proc2.pid, "HorizonJuicerCreator", timeout=12)
            if not main_hwnd:
                raise RuntimeError("Main window 2 did not appear")
            time.sleep(0.9)
            post_click_rel(main_hwnd, 0.21, 0.56, wait=0.7)
            post_click_rel(main_hwnd, 0.83, 0.94, wait=0.5)
            t0 = time.time()
            while time.time() - t0 < 40:
                if os.path.exists(os.path.join(DEMO_DEST, "SKR7620B(#02-DemoCenter)", "NC-Data", "MPF", "SKR7620B.MPF")):
                    time.sleep(1.8)
                    break
                time.sleep(0.5)
            capture_hwnd(main_hwnd, os.path.join(IMG_DIR, "creator_config_center.png"))
        finally:
            kill_proc(proc2)

    finally:
        if backup_data is not None:
            with open(USER_CFG, "w", encoding="utf-8") as f:
                f.write(backup_data)
            print("Restored original HorizonJuicerCreator.json successfully.")


if __name__ == "__main__":
    main()
