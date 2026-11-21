"""Temporary GUD preset helper (_tmp_gud_helper) for SinuTrain captures.

Builds tools/vm_bridge/packages/_tmp_gud_helper/System-CF-Card/siemens/sinumerik/hmi/proj/a_info.com:
an override of the factory-info page (never captured) whose vertical softkeys write preset GUD values
(1-based HMI ACX indices). All captured .com files stay 100 % original.

Welcome page -> VS1 (出厂信息) opens it. Presets:
  VS1 全部界面开  : all hidden-screen display switches on (single pitch change)
  VS2 多螺距      : TOOL_SET[62]=2 (multi pitch-change screen)
  VS3 扩展工艺开  : PROCESS[16]=1
  VS4 扩展工艺关  : PROCESS[16]=0
  VS5 自动对刀开  : INI[70]=1
  VS6 全部界面关  : all display switches off
Remove it afterwards by re-importing the real package (import_cf overwrites a_info.com).

Usage:
    python tools/hlp_capture/gud_helper.py build
    python tools/hlp_capture/gud_helper.py press <1-6>     (HMI must be on the welcome page)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = "_tmp_gud_helper"
OUT = os.path.join(HERE, "..", "vm_bridge", "packages", PKG, "System-CF-Card", "siemens", "sinumerik", "hmi", "proj")

# hidden display / option switches from a_setting.com Mask1 (HMI 1-based)
DISPLAY_SWITCHES = [
    "TECHNOLOGY[57]", "TECHNOLOGY[58]", "TECHNOLOGY[135]", "TOOL_SET[17]", "TECHNOLOGY[233]",
    "INI[22]", "TECHNOLOGY[292]", "TECHNOLOGY[109]", "TECHNOLOGY[56]", "TECHNOLOGY[310]",
    "TECHNOLOGY[127]", "TECHNOLOGY[360]", "TECHNOLOGY[369]", "RING[50]", "WORK[5]",
    "TECHNOLOGY[368]", "INI[149]", "DRESSER[59]", "SHAPE_MODEL[64]", "INI[155]",
    "DRESSER[111]", "TECHNOLOGY[59]", "TECHNOLOGY[303]", "DRESSER[115]",
]

# factory-default data: every hidden screen off, shape modes normal, basic process table
STD = [(v, 0) for v in DISPLAY_SWITCHES] + [
    ("TOOL_SET[62]", 0), ("PROCESS[16]", 0), ("DRESSER[112]", 0), ("SHAPE_MODEL[26]", 0),
    ("SHAPE_MODEL[7]", 0), ("SHAPE_MODEL[27]", 0), ("SHAPE_MODEL[111]", 0), ("INI[145]", 0),
    ("TECHNOLOGY[234]", 0), ("TECHNOLOGY[129]", 0), ("INI[149]", 0)]


def only(*items):
    """STD plus the given switch(es) -> exactly one optional screen visible."""
    d = dict(STD)
    d.update(dict(items))
    return list(d.items())


# softkey -> (title, values). VS1..VS8 and HS1..HS6 on the helper page (HS8 = back)
PRESETS = {
    "VS1": ("默认", only()),
    "VS2": ("扩展工艺", only(("PROCESS[16]", 1))),
    "VS3": ("空运行", only(("TECHNOLOGY[56]", 1))),
    "VS4": ("分段补偿", only(("TECHNOLOGY[310]", 1))),
    "VS5": ("螺距变换", only(("TOOL_SET[62]", 1))),
    "VS6": ("多螺距", only(("TOOL_SET[62]", 2))),
    "VS7": ("反向孔倒角", only(("INI[22]", 1))),
    "VS8": ("自动对刀开", [("INI[70]", 1)]),
    "HS1": ("变径磨削", only(("TECHNOLOGY[109]", 1))),
    "HS2": ("环形槽", only(("RING[50]", 1))),
    "HS3": ("自磨夹具", only(("TECHNOLOGY[233]", 1))),
    "HS4": ("附加配置", only(("TECHNOLOGY[127]", 1))),
    "HS5": ("Y轴设置", only(("TECHNOLOGY[360]", 1))),
    "HS6": ("附加齿型", only(("DRESSER[115]", 1))),
}


def build():
    names = {}
    lines = [";**********************_tmp_gud_helper (capture only)**********************",
             '//M(Mask0/"GUD HELPER v4"//)', ""]
    for _, items in PRESETS.values():  # noqa
        for var, _v in items:
            if var not in names:
                n = f"PV{len(names)}"  # G0.. names are rejected by EasyScreen (G-code clash)
                names[var] = n
                # hidden (0,0,0) fields are not written to the NC on SinuTrain -> keep them small but visible
                i = len(names) - 1
                lines.append(f'\tDEF {n}=(I///"{var}","{var}",,/WR2,ac7//"/NC/_N_NC_GD2_ACX/{var}"'
                             f'/{10 + (i // 12) * 170},{150 + (i % 12) * 16},100/{110 + (i // 12) * 170},'
                             f'{150 + (i % 12) * 16},40/);')
    lines.append('\tDEF MSG=(S////WR1,ac7///0,0,0/20,20,500/);')
    for i, var in enumerate(["TECHNOLOGY[56]", "INI[70]", "PROCESS[16]", "TOOL_SET[62]"]):   # read-back
        lines.append(f'\tDEF CHK{i}=(I///"{var}","{var}",,/WR1,ac7//"/NC/_N_NC_GD2_ACX/{var}"'
                     f'/20,{60 + 20 * i},150/180,{60 + 20 * i},60/);')
    lines.append("")
    lines.append('\tHS8=("返回",ac7,se1);')
    for k, (title, _) in PRESETS.items():
        lines.append(f'\t{k}=("{title}",ac7,se1);')
    lines += ["", "\tPRESS(HS8)", "\t\tEXIT", "\tEND_PRESS"]
    for k, (title, items) in PRESETS.items():
        lines.append(f"\tPRESS({k})")
        for var, v in items:
            lines.append(f"\t\t{names[var]}.VAL={v}")
        lines.append(f'\t\tMSG.VAL="{title} OK"')
        lines.append("\tEND_PRESS")
    lines += ["", "//END", ""]
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "a_info.com"), "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(lines))
    print("built", os.path.join(OUT, "a_info.com"), len(names), "vars")


def press(key):
    """Apply preset `key` ('VS1'..'HS6'); HMI must be on the welcome page, leaves it on the welcome page."""
    import hmi
    hmi.welcome_main_menu()
    hmi.vs(1, 1500)        # welcome VS1 -> 出厂信息 (overridden)
    (hmi.vs if key.startswith("VS") else hmi.hs)(int(key[2:]), 1500)
    hmi.hs(8, 1200)


if __name__ == "__main__":
    if sys.argv[1] == "build":
        build()
    elif sys.argv[1] == "press":
        press(sys.argv[2])
