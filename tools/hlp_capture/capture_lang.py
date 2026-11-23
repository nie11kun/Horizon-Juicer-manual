"""Capture every help screenshot for one help language (eng / rus; also works for chs).

All pictures are taken in the default factory state like the chs set (capture_set.def_*): minimal packages,
"重置数据" (Reset) and the GUD preset "default"; optional screens are captured with ONLY their own switch on.
Raw pictures go to raw/<lng>/ (raw/ for chs); install them with `install_images.py --lng <lng>`.

Usage (Horizon-Juicer-manual root; generate the packages first with `gen_package.py --lng eng all`):
    python tools/hlp_capture/capture_lang.py --lng eng            # all groups
    python tools/hlp_capture/capture_lang.py --lng rus ext int    # only some groups
Groups: demo ext tap int auto_int auto_ext ctr hyd uw
"""
import sys
import time

import capture_set as cs
import gud_helper
import hmi
import inventory
import unlock_setting

S, com_sel, preset, prepare_default, finish = cs.S, cs.com_sel, cs.preset, cs.prepare_default, cs.finish
STD_PRESETS = dict(gud_helper.PRESETS)


def _presets(extra=None):
    gud_helper.PRESETS = dict(STD_PRESETS)
    gud_helper.PRESETS.update(extra or {})


def g_demo():
    """Welcome page, factory info, statistics / accessory life / backup screens, machine configuration login."""
    _presets({"HS6": ("统计备份配件", gud_helper.only(("TECHNOLOGY[57]", 1), ("TECHNOLOGY[58]", 1),
                                                   ("TECHNOLOGY[135]", 1), ("TECHNOLOGY[369]", 1)))})
    prepare_default("demo")
    preset("HS6")
    cs.to_welcome(); hmi.welcome_main_menu(); S("welcome_main")
    hmi.vs(5, 2000); S("stats"); hmi.hs(8, 1200)
    cs.to_welcome(); hmi.welcome_main_menu()
    hmi.vs(3, 2000); S("parts_life")
    hmi.vs(1, 2000); S("roller_record")
    cs.to_welcome(); hmi.welcome_main_menu()
    hmi.vs(2, 2000); S("backup_restore"); hmi.hs(8, 1200)
    cs.to_welcome()
    hmi.welcome_ext_menu(); hmi.vs(1, 1500)
    unlock_setting.read_challenge()          # shows the challenge code (masked by install_images)
    S("_pw")
    cs.to_welcome()
    preset("VS1")
    finish("demo")                           # real a_info.com again
    cs.to_welcome(); hmi.welcome_main_menu()
    hmi.vs(1, 2000); S("info"); hmi.hs(8, 1200)


def g_ext():
    _presets()
    prepare_default("ext_min")
    preset("VS1")
    S("grind_main_ext")
    hmi.hs(2, 1800); hmi.vs(1, 1500); S("process_batch")
    hmi.hs(3, 1800); S("dress_main_ext")
    hmi.vs(4, 1500); S("roller_single_ext"); hmi.hs(3, 1500)
    com_sel(365, 10, 1); hmi.vs(7, 1500); S("roller_form_ext"); hmi.hs(3, 1500); com_sel(365, 10, 0)
    preset("VS2"); hmi.hs(2, 1800); hmi.vs(1, 1500); S("process_ext")
    preset("HS4"); hmi.hs(2, 1800); hmi.vs(4, 1500); S("process_addon")
    preset("HS5"); hmi.hs(2, 1800); hmi.vs(5, 1500); S("process_yaxis")
    for key, vs, name in (("VS3", 3, "grind_dryrun"), ("VS4", 4, "grind_segcomp"), ("VS5", 5, "grind_pitch"),
                          ("VS6", 5, "grind_multipitch"), ("VS7", 7, "grind_chamfer"), ("HS1", 8, "grind_diachange")):
        preset(key); hmi.vs(vs, 1500); S(name)
    preset("HS2"); com_sel(140, 60, 1); S("grind_ring"); com_sel(490, 10, 0)
    preset("HS6"); hmi.hs(3, 1800); hmi.vs(8, 1200); hmi.vs(1, 1500); S("shape_planet")
    preset("VS1")
    finish("ext_min")
    prepare_default("ext_xz")
    preset("VS1")
    hmi.hs(3, 1800); hmi.vs(5, 1500); S("roller_double_ext")
    finish("ext_xz")


def g_tap():
    _presets()
    cs.def_tap()


def g_int():
    _presets()
    prepare_default("int_min")
    preset("VS1")
    S("grind_main_int")
    hmi.hs(3, 1800); S("dress_main_int")
    for vs, name in ((1, "shape_tri_int"), (2, "shape_trap_int"), (3, "shape_arc_int"),
                     (4, "roller_single_int"), (6, "roller_square_int")):
        hmi.vs(vs, 1500); S(name); hmi.hs(3, 1500)
    com_sel(365, 10, 1); hmi.vs(7, 1500); S("roller_form_int"); hmi.hs(3, 1500); com_sel(365, 10, 0)
    preset("HS3"); hmi.vs(6, 1500); S("grind_fixture")
    preset("VS1")
    cs.to_welcome()
    for _ in range(4):                       # challenge OCR occasionally misreads -> retry
        try:
            if unlock_setting.unlock():
                S("int_setting_p1")
                break
        except RuntimeError as e:
            print(" ", e)
        cs.to_welcome()
    finish("int_min")


def g_auto_int():
    cs.def_auto_int()
    # help view: 测量水平距.Z selected on the reverse-hole page, HELP pressed
    prepare_default("int_xz")
    cs._shot_auto("VS1", "_auto_tmp")
    hmi.click(619, 139, 600)
    hmi.key("HELP", 3000); S("help_view"); hmi.key("HELP", 1500)
    finish("int_xz")


def g_auto_ext():
    cs.def_auto_ext()


def g_ctr():
    _presets()
    cs.def_ctr()
    cs.def_auto_ctr()


def g_hyd():
    _presets()
    cs.def_hyd()


def g_uw():
    _presets()
    prepare_default("int_uw")
    preset("VS1")
    hmi.hs(2, 1800); hmi.vs(6, 1500); S("process_stop")
    finish("int_uw")


GROUPS = ["demo", "ext", "tap", "int", "auto_int", "auto_ext", "ctr", "hyd", "uw"]

if __name__ == "__main__":
    print("language", inventory.LANG)
    for g in sys.argv[1:] or GROUPS:
        t0 = time.time()
        globals()["g_" + g]()
        print(g, "done in", round(time.time() - t0), "s")
    hmi.import_package("SKR7620B(#02-Latest20261119)")   # back to the user's baseline package
    hmi.set_language("chs")
    cs.to_welcome()
