"""Capture the help screenshots for one Creator configuration.

Flow per package: import -> refresh -> (unlock + 重置数据) -> GUD helper presets -> re-import package
(restores a_info.com) -> navigate & shoot -> raw/<name>.png.

Usage: python tools/hlp_capture/capture_set.py <config>    e.g. ext_vw / ext_xz / ext_hyd / int_xz / ctr_u
Package must have been generated with gen_package.py first.
"""
import sys
import time

import gen_package
import gud_helper
import hmi
import unlock_setting

PKG = {k: f"{v[0]}(#01-HLP)" for k, v in gen_package.CONFIGS.items()}


def S(name):
    hmi.click_screen(1050, 600, 300)      # park mouse outside the HMI
    print("  shot", name)
    return hmi.shot(name)


def com_sel(x, y, index):
    """Select item `index` of an enum field whose input box is at .com coordinates (x, y) (centre)."""
    hmi.click(int(1.25 * x), int(80 + 1.25 * y), 400)
    hmi.key("SELECT", 600)
    for _ in range(index):
        hmi.key("DOWN", 300)
    hmi.key("INPUT", 1800)


def to_welcome():
    hmi.key("CUSTOM", 1200)
    hmi.recall(1000)          # leave any hung/blank OEM mask (e.g. auto tool-setting dispatcher)
    hmi.key("CUSTOM", 1200)
    for _ in range(3):
        hmi.hs(8, 900)


def prepare(cfg, presets=(1, 5, 3)):
    pkg = PKG[cfg]
    hmi.import_package(pkg)
    to_welcome()
    if not unlock_setting.unlock():
        raise SystemExit("unlock failed")
    hmi.vs(3, 1500)          # 重置数据
    hmi.vs(8, 4000)          # 确认
    to_welcome()
    gud_helper.build()
    hmi.import_package(gud_helper.PKG)
    to_welcome()
    hmi.welcome_main_menu()
    hmi.vs(1, 1500)
    for k in presets:
        hmi.vs(k, 1000)
    hmi.hs(8, 1000)
    hmi.import_package(pkg)  # restore original a_info.com
    to_welcome()


def ext_vw():
    prepare("ext_vw")
    hmi.welcome_main_menu()
    hmi.hs(7, 1800); S("grind_main_ext")
    for vs, n in ((3, "grind_dryrun"), (4, "grind_segcomp"), (5, "grind_pitch"), (7, "grind_chamfer"), (8, "grind_diachange")):
        hmi.vs(vs, 1500); S(n); hmi.hs(1, 1200)
    com_sel(115, 60, 1); S("grind_tap"); com_sel(115, 60, 0); hmi.hs(1, 1200)
    com_sel(250, 60, 1); S("grind_ring"); com_sel(490, 10, 0)
    hmi.hs(1, 1200)
    hmi.hs(2, 1500); S("process_ext")
    hmi.vs(4, 1500); S("process_addon"); hmi.vs(8, 1200)
    hmi.vs(5, 1500); S("process_yaxis"); hmi.vs(8, 1200)
    hmi.hs(3, 1800); S("dress_main_ext")
    hmi.vs(4, 1500); S("roller_single_ext"); hmi.hs(3, 1500)
    hmi.vs(8, 1200); hmi.vs(1, 1500); S("shape_planet"); hmi.hs(3, 1500)
    hmi.hs(4, 1800); S("auto_ext")


def ext_xz():
    prepare("ext_xz", presets=(1,))
    hmi.welcome_main_menu()
    hmi.hs(7, 1800); hmi.hs(3, 1800)
    hmi.vs(5, 1500); S("roller_double_ext"); hmi.hs(3, 1500)
    hmi.vs(8, 1200); hmi.vs(1, 1500); S("shape_planet")


def ext_vform():
    """VW machine switched to form dressing (成型) -> 滚压轮 page."""
    hmi.hs(3, 1800)
    com_sel(365, 10, 1)        # 修整器类型 -> 成型
    hmi.vs(7, 1500); S("roller_form_ext")
    hmi.hs(3, 1500); com_sel(365, 10, 0)


def ext_hyd():
    prepare("ext_hyd", presets=(1,))
    hmi.welcome_main_menu()
    hmi.hs(7, 1800); hmi.hs(3, 1800)
    hmi.vs(7, 1500); hmi.vs(8, 1500); S("roller_hyd")


def int_xz():
    prepare("int_xz")
    hmi.welcome_main_menu()
    hmi.hs(7, 1800); S("grind_main_int")
    hmi.vs(6, 1500); S("grind_fixture"); hmi.hs(1, 1200)
    hmi.hs(3, 1800); S("dress_main_int")
    for vs, n in ((1, "shape_tri_int"), (2, "shape_trap_int"), (3, "shape_arc_int"), (4, "roller_single_int"), (6, "roller_square_int")):
        hmi.vs(vs, 1500); S(n); hmi.hs(3, 1500)
    com_sel(365, 10, 1)        # 成型
    hmi.vs(7, 1500); S("roller_form_int")
    hmi.hs(3, 1500); com_sel(365, 10, 0)
    hmi.hs(4, 1800); S("auto_int")


def int_form():
    prepare("int_xz", presets=(1,))
    hmi.welcome_main_menu()
    hmi.hs(7, 1800); hmi.hs(3, 1800)
    com_sel(365, 10, 1)        # 修整器类型 -> 成型
    hmi.vs(7, 1500); S("roller_form_int")
    hmi.hs(3, 1500); com_sel(365, 10, 0)


def ctr_auto():
    prepare("ctr_u", presets=(1, 5))
    hmi.welcome_main_menu()
    hmi.hs(7, 1800)
    for _ in range(3):
        hmi.hs(4, 3000)
        p = S("auto_center")
        from PIL import Image
        if len(set(Image.open(p).convert("L").crop((20, 80, 680, 520)).getdata())) > 20:   # page has content
            return
        to_welcome(); hmi.welcome_main_menu(); hmi.hs(7, 1800)


def ctr_u():
    prepare("ctr_u")
    hmi.welcome_main_menu()
    hmi.hs(7, 1800); S("center_select")
    hmi.hs(5, 1800); S("center_od_grind")
    hmi.vs(2, 1500); S("center_od_process")
    hmi.vs(3, 1500); S("center_od_dress")
    hmi.vs(5, 1500); S("center_step")
    hmi.hs(6, 1800); S("center_face_grind")
    hmi.vs(2, 1500); S("center_face_process")
    hmi.vs(3, 1500); S("center_face_dress")
    hmi.hs(4, 1800); S("auto_center")


# ---------------------------------------------------------------------------------------------------------
# Default-state captures (2026-11 rework): overview pages show the machine exactly as delivered (every hidden
# screen off, shape modes normal); each optional screen is captured with ONLY its own switch on.
# The GUD helper stays loaded (a_info.com is never captured) and is removed by finish().

def prepare_default(cfg):
    pkg = PKG[cfg]
    hmi.import_package(pkg)
    to_welcome()
    for _ in range(3):       # challenge OCR occasionally misreads -> retry with a fresh challenge code
        try:
            if unlock_setting.unlock():
                break
        except RuntimeError as e:
            print(" ", e)
        to_welcome()
    else:
        raise SystemExit("unlock failed")
    hmi.vs(3, 1500)          # 重置数据 -> factory defaults of every 机床配置 item
    hmi.vs(8, 4000)
    to_welcome()
    gud_helper.build()
    hmi.import_package(gud_helper.PKG)
    to_welcome()


def preset(key):
    to_welcome()
    gud_helper.press(key)
    to_welcome()
    hmi.welcome_main_menu()
    hmi.hs(7, 1800)          # 用户界面 -> 磨削参数


def finish(cfg):
    hmi.import_package(PKG[cfg])   # restores the real a_info.com
    to_welcome()


def def_ext():
    prepare_default("ext_min")
    preset("VS1")
    S("grind_main_ext")
    hmi.hs(2, 1800); S("process_batch")
    hmi.hs(3, 1800); S("dress_main_ext")
    preset("VS2"); hmi.hs(2, 1800); S("process_ext")
    preset("HS4"); hmi.hs(2, 1800); hmi.vs(4, 1500); S("process_addon")
    preset("HS5"); hmi.hs(2, 1800); hmi.vs(5, 1500); S("process_yaxis")
    for key, vs, name in (("VS3", 3, "grind_dryrun"), ("VS4", 4, "grind_segcomp"), ("VS5", 5, "grind_pitch"),
                          ("VS6", 5, "grind_multipitch"), ("VS7", 7, "grind_chamfer"), ("HS1", 8, "grind_diachange")):
        preset(key); hmi.vs(vs, 1500); S(name)
    preset("HS2"); com_sel(140, 60, 1); S("grind_ring"); com_sel(490, 10, 0)
    preset("HS6"); hmi.hs(3, 1800); hmi.vs(8, 1200); hmi.vs(1, 1500); S("shape_planet")
    preset("VS1")
    finish("ext_min")


def def_ext_fix():
    """Process pages on the 批量 table, and the ring page (磨削类型 field sits higher without 丝锥磨削)."""
    prepare_default("ext_min")
    preset("VS1")
    hmi.hs(2, 1800); hmi.vs(1, 1500); S("process_batch")
    preset("VS2"); hmi.hs(2, 1800); hmi.vs(1, 1500); S("process_ext")
    preset("HS2"); com_sel(140, 60, 1); S("grind_ring"); com_sel(490, 10, 0)
    preset("VS1")
    finish("ext_min")


def def_tap():
    prepare_default("ext_tap")
    preset("VS1")
    com_sel(115, 60, 1); S("grind_tap"); com_sel(115, 60, 0)
    finish("ext_tap")


def def_int():
    prepare_default("int_min")
    preset("VS1")
    S("grind_main_int")
    hmi.hs(3, 1800); S("dress_main_int")
    for vs, name in ((1, "shape_tri_int"), (2, "shape_trap_int"), (3, "shape_arc_int")):
        hmi.vs(vs, 1500); S(name); hmi.hs(3, 1500)
    preset("HS3"); hmi.vs(6, 1500); S("grind_fixture")
    preset("VS1")
    finish("int_min")


def def_ctr():
    prepare_default("ctr_u")
    preset("VS1")
    S("center_select")
    hmi.hs(5, 1800); S("center_od_grind")
    hmi.vs(2, 1500); S("center_od_process")
    hmi.vs(3, 1500); S("center_od_dress")
    hmi.vs(5, 1500); S("center_step")
    hmi.hs(6, 1800); S("center_face_grind")
    hmi.vs(2, 1500); S("center_face_process")
    hmi.vs(3, 1500); S("center_face_dress")
    hmi.hs(4, 3000); S("auto_center")
    finish("ctr_u")


def def_ctr_auto():
    """Center auto tool-setting page: the dispatcher mask sometimes stays blank -> retry."""
    from PIL import Image
    prepare_default("ctr_u")
    for n in range(4):
        preset("VS1")
        if n:
            hmi.hs(1, 2000)   # 磨削参数 first, then 自动对刀
        hmi.hs(4, 4000)
        p = S("auto_center")
        if len(set(Image.open(p).convert("L").crop((20, 80, 680, 520)).getdata())) > 20:
            break
    finish("ctr_u")


def _auto_presets(presets):
    """Use a small custom preset table (auto tool-setting mode values only; settings come from 重置数据)."""
    gud_helper.PRESETS = presets


def _shot_auto(key, name, tries=4):
    from PIL import Image
    for n in range(tries):
        preset(key)
        if n:                 # blank last time: open 磨削参数 (HS1) first, then 自动对刀 - reliably loads the page
            hmi.hs(1, 2000)
        hmi.hs(4, 4000)
        p = S(name)
        if len(set(Image.open(p).convert("L").crop((20, 80, 680, 520)).getdata())) > 20:
            return
    print("  WARNING blank page", name)


def def_auto_int():
    hole = [("TECHNOLOGY[159]", 1), ("TOOL_SET[23]", 0), ("TECHNOLOGY[129]", 0), ("TECHNOLOGY[128]", 0)]
    mode = lambda m: [("TECHNOLOGY[159]", 1), ("TOOL_SET[23]", 0), ("TECHNOLOGY[129]", 1), ("TECHNOLOGY[128]", m)]
    _auto_presets({
        "VS1": ("反向孔", hole),
        "VS2": ("腰形孔", [("TECHNOLOGY[159]", 1), ("TOOL_SET[23]", 1), ("TECHNOLOGY[129]", 0), ("TECHNOLOGY[128]", 0)]),
        "VS3": ("内滚道", [("TECHNOLOGY[159]", 0), ("TOOL_SET[23]", 0), ("TECHNOLOGY[129]", 0), ("TECHNOLOGY[128]", 0)]),
        "VS4": ("右端台阶", mode(1)),
        "VS5": ("右端孔", mode(2)),
        "VS6": ("外圆右端反", mode(3)),
    })
    prepare_default("int_xz")
    for key, name in (("VS1", "auto_int"), ("VS2", "auto_int_slot"), ("VS3", "auto_int_groove"),
                      ("VS4", "auto_int_step"), ("VS5", "auto_int_hole"), ("VS6", "auto_int_flat")):
        _shot_auto(key, name)
    preset("VS1")
    finish("int_xz")


def def_auto_ext():
    _auto_presets({"VS1": ("默认", [("TECHNOLOGY[128]", 0)])})
    prepare_default("ext_vw")
    _shot_auto("VS1", "auto_ext")
    finish("ext_vw")


def def_auto_ctr():
    _auto_presets({
        "VS1": ("全部测量", [("TECHNOLOGY[159]", 1), ("TOOL_SET[23]", 0), ("TECHNOLOGY[129]", 0), ("TECHNOLOGY[128]", 0),
                         ("TECHNOLOGY[176]", 1), ("INI[139]", 1), ("TOOL_SET[45]", 1)]),
        "VS2": ("复位", [("INI[139]", 0), ("TOOL_SET[45]", 0)]),
    })
    prepare_default("ctr_u")
    _shot_auto("VS1", "auto_center")
    preset("VS2")
    finish("ctr_u")


def def_hyd():
    prepare_default("ext_hyd")
    preset("VS1")
    hmi.hs(3, 1800); S("roller_hyd")
    finish("ext_hyd")


if __name__ == "__main__":
    for name in sys.argv[1:]:
        t0 = time.time()
        globals()[name]()
        print(name, "done in", round(time.time() - t0), "s")
