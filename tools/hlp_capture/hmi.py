"""SinuTrain HMI driver for help-doc captures (full-screen, non-split SinuTrain window in the VM).

Coordinates:
  - screen  : VM screen pixels (screenshot image == screen, 1920x1139 visible)
  - hmi     : 800x600 HMI area, origin at screen (HMI_X0, HMI_Y0)
Calibrated 2026-11-20 with SinuTrain maximized, View = single window (not split).

Usage (from Horizon-Juicer-manual root):
    python tools/hlp_capture/hmi.py shot welcome          -> tools/hlp_capture/raw/welcome.png (800x600)
    python tools/hlp_capture/hmi.py hs 1 | vs 3 | key CUSTOM | click 400 300
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "vm_bridge"))
import host_sinutrain_shot as bridge  # noqa: E402
from PIL import Image  # noqa: E402

RAW = os.path.join(HERE, "raw")
HMI_X0, HMI_Y0 = 150, 71

# Panel keys, screen coordinates (full-screen layout)
KEYS = {
    "MACHINE": (1230, 208), "PROGRAM": (1288, 208), "OFFSET": (1344, 208),
    "PROGRAM_MANAGER": (1230, 265), "ALARM": (1288, 265), "CUSTOM": (1344, 265),
    "MENU_SELECT": (1230, 322), "MENU_FUNCTION": (1288, 322), "MENU_USER": (1344, 322),
    "ALARM_CANCEL": (1152, 400), "NEXT_WINDOW": (1230, 400), "UP": (1287, 400), "PAGE_UP": (1344, 400),
    "GROUP_CHANNEL": (1152, 457), "LEFT": (1230, 457), "SELECT": (1287, 457), "RIGHT": (1344, 457),
    "INSERT": (1422, 457),
    "HELP": (1152, 514), "END": (1230, 514), "DOWN": (1287, 514), "PAGE_DOWN": (1344, 514),
    "INPUT": (1422, 514),
    "JOG": (325, 734), "REPOS": (389, 734), "REF_POINT": (452, 734),
    "MDA": (325, 882), "AUTO": (325, 957),
    "RESET": (263, 1033), "SINGLE_BLOCK": (326, 1033), "CYCLE_STOP": (390, 1033), "CYCLE_START": (453, 1033),
}


def _rect():
    return bridge.send_cmd("status")["data"]["sinutrainRect"]


_R = None


def click_screen(sx, sy, wait_ms=500):
    global _R
    if _R is None:
        _R = _rect()
    rx = (sx - _R["left"]) / _R["width"]
    ry = (sy - _R["top"]) / _R["height"]
    bridge.send_cmd("click_rel", rx=rx, ry=ry, waitMs=wait_ms)


def click(x, y, wait_ms=500):
    """Click at HMI 800x600 coordinates."""
    click_screen(HMI_X0 + x, HMI_Y0 + y, wait_ms)


def hs(i, wait_ms=900):
    """Horizontal softkey 1..8 (bottom bar)."""
    click(50 + 100 * (i - 1), 578, wait_ms)


def vs(i, wait_ms=900):
    """Vertical softkey 1..8 (right column)."""
    click(750, 64 + 66 * (i - 1), wait_ms)


def recall(wait_ms=800):
    """'^' recall key at HMI bottom-left."""
    click(9, 557, wait_ms)


def key(name, wait_ms=700):
    click_screen(*KEYS[name], wait_ms=wait_ms)


def keys(text, wait_ms=400):
    bridge.send_cmd("send_keys", keys=text, waitMs=wait_ms)


def shot(name, full=False):
    """Capture; save 800x600 HMI crop to raw/<name>.png (and full screen if full=True)."""
    os.makedirs(RAW, exist_ok=True)
    bridge.send_cmd("screenshot", filename="_hlp_full.png")
    im = Image.open(os.path.join(bridge.OUT_DIR, "_hlp_full.png")).convert("RGB")
    out = os.path.join(RAW, f"{name}.png")
    im.crop((HMI_X0, HMI_Y0, HMI_X0 + 800, HMI_Y0 + 600)).save(out)
    if full:
        im.save(os.path.join(RAW, f"{name}_full.png"))
    return out


def wait(sec):
    time.sleep(sec)


def toggle(y, downs=1, x=330):
    """Enum field in a_setting list: click field at HMI (x,y), SELECT opens list, move DOWN n (UP if <0), INPUT."""
    click(x, y, 400)
    key("SELECT", 600)
    for _ in range(abs(downs)):
        key("DOWN" if downs > 0 else "UP", 300)
    key("INPUT", 700)


LANG_ROW = {"eng": 158, "rus": 178, "chs": 198}


def set_language(lng, settle=10):
    """Setup -> VS3 Change language -> pick row -> VS8 OK (forces HMI to reload OEM files)."""
    key("MENU_SELECT", 900)
    hs(6, 1500)            # 调试 / Setup
    vs(3, 1200)            # Change language
    click(300, LANG_ROW[lng], 500)
    vs(8, 500)             # OK
    time.sleep(settle)


def import_package(pkg_subdir):
    """Copy package System-CF-Card into VM SinuTrain, then refresh via ENG->CHS language switch."""
    print(bridge.send_cmd("import_cf", timeout=120.0, packageSubDir=pkg_subdir)["message"])
    set_language("eng")
    set_language("chs")
    key("CUSTOM", 1500)


def open_user_ui():
    """From welcome page enter the machine UI (HS7 用户界面)."""
    key("CUSTOM", 1200)
    hs(7, 1500)


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "shot":
        print(shot(args[0], full="--full" in args))
    elif cmd == "hs":
        hs(int(args[0]))
    elif cmd == "vs":
        vs(int(args[0]))
    elif cmd == "key":
        key(args[0])
    elif cmd == "click":
        click(int(args[0]), int(args[1]))
    elif cmd == "recall":
        recall()
    elif cmd == "import":
        import_package(args[0])
    elif cmd == "lang":
        set_language(args[0])
    elif cmd == "ui":
        open_user_ui()
