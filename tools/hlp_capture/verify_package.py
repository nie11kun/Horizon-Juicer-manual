"""Check the help inside Creator-generated packages: content for functions the configuration does NOT
have must be gone.

For each package from gen_package.CONFIGS, derive the markers whose content must be removed from the
config flags, then look for any surviving `<!--ifIsXxxBegin-->` / `<!--ifIsXxxLine-->` of those markers
in the package's help pages (= Creator did not process that marker for help, so the text is shown on
a machine without the function).

Usage: python tools/hlp_capture/verify_package.py [config ...]     (default: every generated package)
"""
import glob
import os
import re
import sys

import yaml

import gen_package

# markers Creator does not strip from help pages at all (checked 2026-11): the help text under them is
# written as a condition ("带 A 轴的机床…"), so a leftover is reported as a note, not an error
NOT_STRIPPED = {"ifIsHasA", "ifIsNotHasA", "ifIsHasLoadingArm", "ifIsNotHasLoadingArm", "ifIsHasWorm"}
TOC = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "hlp_src", "chs", "toc.yaml"),
                          encoding="utf-8"))
GATE = {e["ref"]: set(e.get("marks", []) or []) for part in TOC["parts"] for e in part.get("entries", [])}

PKG_DIR = gen_package.PKG_DIR


def absent(cfg):
    c = dict(gen_package.BASE)
    c.update(gen_package.CONFIGS[cfg][2])
    ext = c["machineType"] == 0
    center = not ext and c["ifCenter"] == 0
    auto = c["ifOperation"] == 0
    a = set()
    if ext:
        a |= {"ifIsInternal", "ifIsInternalOnly", "ifIsCenter", "ifIsHasU", "ifIsNotHasU", "ifIsNotHasUBack",
              "ifIsNotHasUFront", "ifIsXNeiFront", "ifIsXNeiBack", "ifIsProbeFront", "ifIsNotProbeFront"}
    else:
        a |= {"ifIsExternal", "ifIsExternalVW", "ifIsXWai", "ifIsHasWorm", "ifIsScrewTap"}
    if not ext:
        a |= {"ifIsHasReOperate"} if True else set()
    a |= {"ifIsNotCenter"} if center else {"ifIsCenter", "ifIsHasU", "ifIsNotHasU", "ifIsNotHasUBack", "ifIsNotHasUFront"}
    if not center:
        pass
    elif c["ifHasU"] == 0:
        a |= {"ifIsNotHasU", "ifIsNotHasUBack", "ifIsNotHasUFront"}
    else:
        a |= {"ifIsHasU", "ifIsNotHasUFront" if c["ifNotHasUExternalPos"] == 0 else "ifIsNotHasUBack"}
    if not center and not ext:
        pass
    if center:
        a.add("ifIsInternalOnly")
    if ext:
        a |= {"ifIsHasReOperate"} if c["ifHasReOp"] != 0 else {"ifIsNotHasReOperate"}
    a |= {"ifIsNotAuto"} if auto else {"ifIsAuto", "ifIsKaiGuanCeLiang", "ifIsCeTouCeLiang", "ifIsKaiGuanAndCeTouCeLiang"}
    if auto:
        m = c["measureMethord"]
        a |= {0: {"ifIsCeTouCeLiang", "ifIsKaiGuanAndCeTouCeLiang"}, 1: {"ifIsKaiGuanCeLiang", "ifIsKaiGuanAndCeTouCeLiang"},
              2: set()}.get(m, set())
    a.add("ifIsNotHasA" if c["ifHasA"] == 1 else "ifIsHasA")
    if c["ifHasLoadingArm"] != 1:
        a.add("ifIsHasLoadingArm")
    else:
        a.add("ifIsNotHasLoadingArm")
    if not (ext and c["ifHasWorm"] == 1):
        a.add("ifIsHasWorm")
    if not (ext and c["ifHasScrewTap"] == 0):
        a.add("ifIsScrewTap")
    ware = c["wareType"]
    dw = {0: "ifIsDressWare1", 1: "ifIsDressWare2", 2: "ifIsDressWare3", 3: "ifIsDressWare4", 4: "ifIsDressWare5"}
    for k, m in dw.items():
        # Creator keeps DressWare1 for V(1) and UW(6), DressWare3 for XW(5) - verified against generated .com
        if k != ware and not (ware in (1, 6) and m == "ifIsDressWare1") and not (ware == 5 and m == "ifIsDressWare3"):
            a.add(m)
    a.add("ifIsUW" if ware != 6 else "ifIsNotUW")
    a.add("ifIsXW" if ware != 5 else "ifIsNotXW")
    if c["wheelType"] == 0:     # hydraulic keeps the wheelType fields in .com too (hidden at runtime)
        a.add("ifIsSide")
    else:
        a.add("ifIsSingleAndRound")
    return a


def hlp_dir(name):
    hits = glob.glob(os.path.join(PKG_DIR, name + "(*", "**", "hlp", "chs", "UserGuide"), recursive=True)
    return hits[0] if hits else None


def main():
    cfgs = sys.argv[1:] or list(gen_package.CONFIGS)
    bad = 0
    for cfg in cfgs:
        d = hlp_dir(gen_package.CONFIGS[cfg][0])
        if not d:
            print(f"{cfg}: package not generated")
            continue
        ab = absent(cfg)
        left = {}
        for fp in glob.glob(os.path.join(d, "*.html")):
            if GATE.get(os.path.basename(fp), set()) & ab:
                continue                      # whole page is not in this machine's table of contents
            t = open(fp, encoding="utf-8-sig", errors="ignore").read()
            for m in re.findall(r"<!--(ifIs[A-Za-z0-9]+?)(?:Begin|Line)-->", t):
                if m in ab:
                    left.setdefault(m, set()).add(os.path.basename(fp))
        real = {m: fs for m, fs in left.items() if m not in NOT_STRIPPED}
        print(f"== {cfg} ({gen_package.CONFIGS[cfg][0]}): {'OK' if not real else 'LEFT OVER'}")
        for m, fs in sorted(left.items()):
            bad += m not in NOT_STRIPPED
            print(f"   {'note' if m in NOT_STRIPPED else 'ERROR'} {m}: {sorted(fs)}")
    print("TOTAL", bad)


if __name__ == "__main__":
    main()
