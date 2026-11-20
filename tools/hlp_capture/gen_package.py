"""Generate SinuTrain capture packages with HorizonJuicerCreator for HMI help screenshots.

- Always old 828D mode (systemMode=0) so .com files go to siemens/sinumerik/hmi/proj (800x600 HMI).
- Backs up ~/HorizonJuicerCreator.json and restores it byte-for-byte in finally.
- Output: Horizon-Juicer-manual/tools/vm_bridge/packages/<name>(#<idx>-<custom>)/System-CF-Card

Usage:
    python tools/hlp_capture/gen_package.py ext_vw            # one config
    python tools/hlp_capture/gen_package.py all               # every config in CONFIGS
    python tools/hlp_capture/gen_package.py --list

Stop any `honkit serve` before running (generated packages contain .md files).
Polarity reminders (generatepro.cpp): 0=enabled for ifCenter/ifOperation/ifHasScrewTap/ifHasU;
1=enabled for ifHasWorm/ifHasLoadingArm. wareType: 0 VW,1 V,2 XZ,3 X_Back,4 hydraulic,5 XW,6 UW.
"""
import argparse
import ctypes
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
MANUAL = os.path.abspath(os.path.join(HERE, "..", ".."))
PKG_DIR = os.path.join(MANUAL, "tools", "vm_bridge", "packages")
SRC_DIR = r"C:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer"
EXE = os.path.join(SRC_DIR, "HorizonJuicerCreator", "HorizonJuicerCreator.exe")
USER_CFG = os.path.expanduser(r"~\HorizonJuicerCreator.json")

BASE = {
    "lng": 0, "hmiMode": 0, "systemMode": 0, "ifRemoveComments": 1,
    "ifHasEncryption": 0, "ifHasNoneTradeMark": 0,
    "grindWheelType": 0, "exGrindWheelType": 0, "dressWheelType": 0,
    "ifHasA": 0, "ifHasLoadingArm": 0, "ifHasWorm": 0, "ifHasScrewTap": 1,
    "ifHasReOp": 1, "ifOperation": 1, "measureMethord": 0, "probePos": 0,
    "ifCenter": 1, "ifHasU": 1, "ifNotHasUExternalPos": 0,
    "wheelType": 0, "shapeType": 0, "roughFeedInput": 1,
}

# name -> (machineName, machineNameLng, overrides)
CONFIGS = {
    # external, VW dresser, single/square roller, full option set (screw tap, worm, re-op, auto probe, loading arm, A axis)
    "ext_vw": ("HLPEXT1", "外螺纹磨床", {"machineType": 0, "wareType": 0, "wheelType": 0,
                                       "ifHasScrewTap": 0, "ifHasWorm": 1, "ifHasReOp": 0,
                                       "ifOperation": 0, "measureMethord": 2, "ifHasLoadingArm": 1,
                                       "ifHasA": 1}),
    # external, XZ interpolation dresser, double roller, no options
    "ext_xz": ("HLPEXT2", "外螺纹磨床", {"machineType": 0, "wareType": 2, "wheelType": 1}),
    # external, V dresser / hydraulic / XW
    "ext_v": ("HLPEXT3", "外螺纹磨床", {"machineType": 0, "wareType": 1}),
    "ext_hyd": ("HLPEXT4", "外螺纹磨床", {"machineType": 0, "wareType": 4}),
    "ext_xw": ("HLPEXT5", "外螺纹磨床", {"machineType": 0, "wareType": 5, "wheelType": 0}),
    # internal, XZ, auto probe front
    "int_xz": ("HLPINT1", "内螺纹磨床", {"machineType": 1, "wareType": 2, "wheelType": 0,
                                       "ifOperation": 0, "measureMethord": 1, "probePos": 0}),
    "int_xback": ("HLPINT2", "内螺纹磨床", {"machineType": 1, "wareType": 3,
                                          "ifOperation": 0, "measureMethord": 0, "probePos": 1}),
    "int_uw": ("HLPINT3", "内螺纹磨床", {"machineType": 1, "wareType": 6, "wheelType": 1}),
    # internal grinding centers
    "ctr_u": ("HLPCTR1", "内螺纹磨削中心", {"machineType": 1, "wareType": 2, "ifCenter": 0, "ifHasU": 0,
                                         "ifOperation": 0, "measureMethord": 1, "ifHasLoadingArm": 1}),
    "ctr_nou_back": ("HLPCTR2", "内螺纹磨削中心", {"machineType": 1, "wareType": 2, "ifCenter": 0,
                                                "ifHasU": 1, "ifNotHasUExternalPos": 0}),
    "ctr_nou_front": ("HLPCTR3", "内螺纹磨削中心", {"machineType": 1, "wareType": 2, "ifCenter": 0,
                                                 "ifHasU": 1, "ifNotHasUExternalPos": 1}),
}

user32 = ctypes.windll.user32
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except OSError:
    pass
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)


def find_window(pid):
    found = []

    def cb(hwnd, _):
        p = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
        if p.value == pid and user32.IsWindowVisible(hwnd):
            buf = ctypes.create_unicode_buffer(256)
            user32.GetWindowTextW(hwnd, buf, 256)
            if "HorizonJuicerCreator" in buf.value:
                found.append(hwnd)
        return True

    user32.EnumWindows(WNDENUMPROC(cb), 0)
    return found[0] if found else None


def print_window(hwnd):
    """Render a window to a PIL image with PrintWindow (works when the host screen is locked/covered)."""
    from PIL import Image
    gdi32 = ctypes.windll.gdi32

    class RECT(ctypes.Structure):
        _fields_ = [("l", ctypes.c_long), ("t", ctypes.c_long), ("r", ctypes.c_long), ("b", ctypes.c_long)]
    rc = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rc))
    w, h = rc.r - rc.l, rc.b - rc.t
    hdc = user32.GetWindowDC(hwnd)
    mdc = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(mdc, bmp)
    user32.PrintWindow(hwnd, mdc, 2)          # PW_RENDERFULLCONTENT

    class BIH(ctypes.Structure):
        _fields_ = [("biSize", ctypes.c_uint32), ("biWidth", ctypes.c_int32), ("biHeight", ctypes.c_int32),
                    ("biPlanes", ctypes.c_uint16), ("biBitCount", ctypes.c_uint16), ("biCompression", ctypes.c_uint32),
                    ("biSizeImage", ctypes.c_uint32), ("a", ctypes.c_int32), ("b", ctypes.c_int32),
                    ("c", ctypes.c_uint32), ("d", ctypes.c_uint32)]
    bi = BIH(ctypes.sizeof(BIH), w, -h, 1, 32, 0, 0, 0, 0, 0, 0)
    buf = ctypes.create_string_buffer(w * h * 4)
    gdi32.GetDIBits(mdc, bmp, 0, h, buf, ctypes.byref(bi), 0)
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(mdc)
    user32.ReleaseDC(hwnd, hdc)
    return Image.frombuffer("RGBA", (w, h), buf, "raw", "BGRA", 0, 1).convert("RGB")


def hide_offscreen(hwnd):
    """Move the Creator window off-screen without activating it, so automation never disturbs the user
    (PostMessage clicks and PrintWindow keep working off-screen)."""
    SWP_NOSIZE, SWP_NOZORDER, SWP_NOACTIVATE = 0x0001, 0x0004, 0x0010
    user32.SetWindowPos(hwnd, 0, -6000, -6000, 0, 0, SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE)


def click_rel(hwnd, rx, ry, wait=0.6):
    class RECT(ctypes.Structure):
        _fields_ = [("l", ctypes.c_long), ("t", ctypes.c_long), ("r", ctypes.c_long), ("b", ctypes.c_long)]
    rc = RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rc))
    x, y = int(rc.r * rx), int(rc.b * ry)
    lp = (y << 16) | (x & 0xFFFF)
    user32.PostMessageW(hwnd, 0x0201, 1, lp)
    time.sleep(0.05)
    user32.PostMessageW(hwnd, 0x0202, 0, lp)
    time.sleep(wait)


def generate(name):
    mname, lngname, ov = CONFIGS[name]
    cfg = dict(BASE)
    cfg.update(ov)
    cfg.update({"machineName": mname, "machineNameLng": lngname, "machineIndex": "01",
                "customInfo": "HLP", "programDir": {"sourceDir": SRC_DIR, "destDir": PKG_DIR}})
    assert cfg["systemMode"] == 0
    out = os.path.join(PKG_DIR, f"{mname}(#01-HLP)")
    if os.path.exists(out):
        shutil.rmtree(out)
    with open(USER_CFG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=4)
    proc = subprocess.Popen([EXE])
    try:
        hwnd = None
        for _ in range(60):
            hwnd = find_window(proc.pid)
            if hwnd:
                break
            time.sleep(0.2)
        if not hwnd:
            raise RuntimeError("Creator window not found")
        hide_offscreen(hwnd)
        time.sleep(3.0)
        click_rel(hwnd, 0.21, 0.60, 1.5)   # 机床配置 card
        click_rel(hwnd, 0.83, 0.94, 0.5)   # 程序生成
        marker = os.path.join(out, "System-CF-Card", "siemens", "sinumerik", "hmi", "proj", "a_custom.com")
        t0 = time.time()
        while time.time() - t0 < 60 and not os.path.exists(marker):
            time.sleep(0.5)
        if not os.path.exists(marker):
            raise RuntimeError(f"generation failed or not old-828D layout: {marker}")
        wait_until_stable(out)
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(5)
            except subprocess.TimeoutExpired:
                proc.kill()
    return os.path.basename(out)


def wait_until_stable(root, quiet=8.0, minimum=15.0, timeout=180.0):
    """Creator copies files first (keeping source mtimes) and applies ReplaceMarker processing afterwards.
    Wait until the package's file-size signature has not changed for `quiet` seconds (and at least
    `minimum` seconds overall); killing Creator earlier leaves markers unprocessed."""
    t0 = time.time()
    last, since = None, time.time()
    while time.time() - t0 < timeout:
        sig = []
        for dp, _, fns in os.walk(root):
            for fn in fns:
                try:
                    sig.append((dp, fn, os.path.getsize(os.path.join(dp, fn))))
                except OSError:
                    pass
        sig = hash(tuple(sorted(sig)))
        if sig != last:
            last, since = sig, time.time()
        elif time.time() - since >= quiet and time.time() - t0 >= minimum:
            return
        time.sleep(1.0)
    raise RuntimeError("Creator did not finish writing the package in time")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list or not a.names:
        for k, (m, _, ov) in CONFIGS.items():
            print(f"{k:14} {m}  {ov}")
        return
    names = list(CONFIGS) if a.names == ["all"] else a.names
    backup = open(USER_CFG, "rb").read() if os.path.exists(USER_CFG) else None
    try:
        for n in names:
            print(n, "->", generate(n), flush=True)
    finally:
        if backup is not None:
            with open(USER_CFG, "wb") as f:
                f.write(backup)
            print("restored", USER_CFG)


if __name__ == "__main__":
    sys.exit(main())
