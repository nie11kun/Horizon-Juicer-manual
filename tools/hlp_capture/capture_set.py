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


if __name__ == "__main__":
    for name in sys.argv[1:]:
        t0 = time.time()
        globals()[name]()
        print(name, "done in", round(time.time() - t0), "s")
