"""Unlock HMI '机床配置' (a_setting Mask0) for screenshot sessions - fully automatic.

Flow: (caller is on the HMI welcome page) VS1 -> Mask0, VS3 shows the challenge code
      -> challenge read by Windows OCR -> typed into HorizonJuicerCreator's own '口令计算' page
      -> result read by Windows OCR inside this process -> typed into the HMI field.
No algorithm is implemented here; the code is never printed, logged or stored
(temporary crops are deleted immediately). Clipboard is not used (VMware clipboard sync can lock it).

Usage: python tools/hlp_capture/unlock_setting.py          (from the HMI welcome page)
"""
import ctypes
import os
import subprocess
import tempfile
import time

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except OSError:
    pass
from PIL import Image, ImageOps  # noqa: E402

import gen_package as g  # noqa: E402
import hmi  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OCR_PS1 = os.path.join(HERE, "ocr_digits.ps1")
user32 = ctypes.windll.user32


def _ocr(img, dark_text=True):
    im = img.convert("L")
    if not dark_text:
        im = ImageOps.invert(im)
    im = im.point(lambda v: 0 if v < 200 else 255)
    im = ImageOps.expand(im.resize((im.width * 4, im.height * 4), Image.LANCZOS), border=40, fill=255)
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    try:
        im.save(path)
        r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", OCR_PS1, path],
                           capture_output=True, text=True)
        return r.stdout.strip()
    finally:
        os.remove(path)


def read_challenge():
    hmi.vs(3, 1000)
    p = hmi.shot("_challenge")
    try:
        code = _ocr(Image.open(p).crop((600, 505, 700, 530)), dark_text=True)
    finally:
        os.remove(p)
    if len(code) != 6:
        raise RuntimeError(f"challenge OCR failed ({len(code)} digits)")
    return code


def _type_chars(hwnd, text):
    for ch in text:
        user32.PostMessageW(hwnd, 0x0102, ord(ch), 0)   # WM_CHAR
        time.sleep(0.08)


def _calc(challenge):
    proc = subprocess.Popen([g.EXE])
    try:
        h = None
        for _ in range(60):
            h = g.find_window(proc.pid)
            if h:
                break
            time.sleep(0.2)
        g.hide_offscreen(h)
        time.sleep(3)
        g.click_rel(h, 0.50, 0.60, 1.5)       # 口令计算 card
        g.click_rel(h, 0.387, 0.42, 0.5)      # challenge input box
        _type_chars(h, challenge)
        code = ""
        for _ in range(4):                      # result appears after a short calculation delay
            time.sleep(1.5)
            win = g.print_window(h)
            k = win.width / 1000.0              # layout measured on a 1000px-wide capture
            code = _ocr(win.crop((int(350 * k), int(465 * k), int(650 * k), int(535 * k))), dark_text=False)
            del win
            if code.isdigit() and len(code) >= 4:
                break
    finally:
        proc.kill()
    if not code.isdigit() or len(code) < 4:
        raise RuntimeError("calculator OCR failed")
    return code


def unlock():
    """From the HMI welcome page: open 机床配置 and unlock it. Returns True when the list page shows."""
    hmi.welcome_ext_menu()
    hmi.vs(1, 1500)
    code = _calc(read_challenge())
    hmi.click(280, 93, 400)
    hmi.keys(code, 300)
    hmi.keys("{ENTER}", 1500)
    del code
    p = hmi.shot("_unlock_check")
    im = Image.open(p).convert("RGB").crop((10, 75, 100, 98))   # red '磨削相关:' header on unlocked list
    ok = any(r > 180 and gg < 90 and b < 90 for r, gg, b in im.get_flattened_data())
    os.remove(p)
    print("unlocked" if ok else "unlock FAILED")
    return ok


if __name__ == "__main__":
    unlock()
