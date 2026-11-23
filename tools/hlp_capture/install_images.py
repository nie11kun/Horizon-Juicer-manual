"""Install captured screenshots into Source_Library/HMI/hlp/chs/UserGuide/resources/img.

- source: tools/hlp_capture/raw/<name>.png (800x600 HMI captures)
- optional highlight frames (HMI pixel coords) with numbered badges, masks for random data
- palette-quantized PNG to keep the help folder small
Usage: python tools/hlp_capture/install_images.py [name ...]   (default: all images referenced by the help)
"""
import glob
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
import inventory  # noqa: E402
RAW = os.path.join(HERE, "raw") if inventory.LANG == "chs" else os.path.join(HERE, "raw", inventory.LANG)

DST = os.path.join(inventory.ROOT, "Source_Library", "HMI", "hlp", inventory.LANG, "UserGuide", "resources", "img")
UG = os.path.dirname(os.path.dirname(DST))

ALIAS = {"setting_password": "_pw", "setting_list": "int_setting_p1"}
MASKS = {"setting_password": [(600, 505, 700, 532)]}           # random challenge code
FRAMES = {                                                     # (x0, y0, x1, y1); every framed image needs a
    "dress_main_int": [(400, 140, 698, 308)],                  # caption in hlp_src/<lang>/img_caps.yaml
    "dress_main_ext": [(400, 140, 698, 308)],
    "welcome_main": [(700, 42, 800, 545), (600, 552, 700, 600)],
    "process_batch": [(36, 128, 664, 350)],
    "center_select": [(702, 163, 798, 487)],
}
RED = (230, 30, 30)


def badge(draw, x, y, n):
    r = 11
    draw.ellipse((x - r, y - r, x + r, y + r), fill=RED)
    try:
        f = ImageFont.truetype("msyhbd.ttc", 15)
    except OSError:
        f = ImageFont.load_default()
    draw.text((x, y), str(n), fill="white", font=f, anchor="mm")


def install(name):
    src = os.path.join(RAW, ALIAS.get(name, name) + ".png")
    if not os.path.exists(src):
        return False
    im = Image.open(src).convert("RGB")
    d = ImageDraw.Draw(im)
    for box in MASKS.get(name, []):
        d.rectangle(box, fill=im.getpixel((box[0] - 5, box[1] + 5)))
    for i, (x0, y0, x1, y1) in enumerate(FRAMES.get(name, []), 1):
        d.rounded_rectangle((x0 + 1, y0 + 1, x1 - 2, y1 - 2), radius=6, outline=RED, width=3)
    im = im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    im.save(os.path.join(DST, name + ".png"), optimize=True)
    return True


def referenced():
    names = set()
    for fp in glob.glob(os.path.join(UG, "*.html")):
        names |= set(re.findall(r'resources/img/([^"]+)\.png', open(fp, encoding="utf-8-sig").read()))
    return sorted(names)


if __name__ == "__main__":
    names = sys.argv[1:] or referenced()
    missing = [n for n in names if not install(n)]
    print(f"installed {len(names) - len(missing)}, missing raw: {missing}")
