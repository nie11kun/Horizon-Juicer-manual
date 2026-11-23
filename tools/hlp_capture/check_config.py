"""Configuration-dependency check for the help text.

1. Config markers: a help entry whose fields only exist under a Creator marker (e.g. ifIsHasReOperate,
   ifIsScrewTap) must itself be wrapped in that marker (cell / block / toc marks), otherwise the help
   describes a function the machine does not have.
2. Hidden switches: fields that are only shown when a 机床配置 switch is on (LOAD/CHANGE `IF switch ... X.WR=2`)
   must say so in the help text ("需在机床配置中开启 …").
3. Keyword scan: free text mentioning optional functions outside a matching marker.

Usage: python tools/hlp_capture/check_config.py
"""
import collections
import glob
import os
import re

import yaml

import inventory
from inventory import parse_def_line, split_fields

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "hlp_src", inventory.LANG)
CFG_WORD = {"chs": "机床配置", "eng": "machine configuration", "rus": "конфигурац"}[inventory.LANG]
TEXTS = inventory.load_texts()

# a marker is satisfied by itself or by a narrower marker that implies it
IMPLIES = {
    "ifIsInternal": {"ifIsInternalOnly", "ifIsCenter", "ifIsHasU", "ifIsNotHasU", "ifIsNotHasUBack",
                     "ifIsNotHasUFront", "ifIsXNeiFront", "ifIsXNeiBack", "ifIsDressWare4", "ifIsProbeFront",
                     "ifIsNotProbeFront"},
    "ifIsExternal": {"ifIsExternalVW", "ifIsXWai", "ifIsHasWorm", "ifIsScrewTap"},
    "ifIsCenter": {"ifIsHasU", "ifIsNotHasU", "ifIsNotHasUBack", "ifIsNotHasUFront"},
    "ifIsNotHasU": {"ifIsNotHasUBack", "ifIsNotHasUFront"},
    "ifIsAuto": {"ifIsKaiGuanCeLiang", "ifIsCeTouCeLiang", "ifIsKaiGuanAndCeTouCeLiang", "ifIsProbeFront",
                 "ifIsNotProbeFront"},
}
# markers that never restrict content (language etc.)
IGNORE = {"ifIsCHS", "ifIsENG", "ifIsHasEncryption", "ifIsNotHasEncryption"}


def satisfied(req, have):
    return req in have or bool(IMPLIES.get(req, set()) & have)


def load_cells():
    toc = yaml.safe_load(open(os.path.join(SRC, "toc.yaml"), encoding="utf-8"))
    secmarks = {}

    for part in toc.get("parts", []):
        for it in part.get("entries", []) or []:
            secmarks[it["ref"].replace(".html", "")] = list(part.get("marks", []) or []) + list(it.get("marks", []) or [])
    cells = collections.defaultdict(list)
    for fp in glob.glob(os.path.join(SRC, "section_*.yaml")):
        sec = os.path.basename(fp)[:-5]
        doc = yaml.safe_load(open(fp, encoding="utf-8"))

        def walk(bs, mk):
            for b in bs or []:
                m = mk + list(b.get("marks", []) or [])
                for p in b.get("params", []) or []:
                    cells[(sec, p["id"])].append((set(m + list(p.get("marks", []) or [])), p))
                walk(b.get("body"), m)
        walk(doc["blocks"], list(secmarks.get(sec, [])) + list(doc.get("marks", []) or []))
    return cells, secmarks


def switch_vars():
    """var -> setting label for every switch on the 机床配置 page."""
    out = {}
    for line in open(os.path.join(inventory.PROJ, "a_setting.com"), encoding="utf-8-sig"):
        p = parse_def_line(line)
        if not p:
            continue
        f = split_fields(p[1]) + [""] * 12
        m = re.search(r'_ACX/([A-Z_]+\[\d+\])', f[6])
        lab = inventory.resolve(f[3].split(",")[0].strip(), TEXTS).strip('"').lstrip("-")
        if m and lab and f[1].strip().startswith("*"):
            out[m.group(1)] = lab
    return out


def hidden_fields(switches):
    """(file, field name) -> set of switch labels that make it visible."""
    dep = collections.defaultdict(set)
    for fp in glob.glob(os.path.join(inventory.PROJ, "*.com")):
        fn = os.path.basename(fp)
        local = {}
        stack = []
        mask = ""
        hidden4 = set()
        cand = collections.defaultdict(set)
        for line in open(fp, encoding="utf-8-sig"):
            s = line.split(";")[0].strip()
            mm = re.match(r"//M\((\w+)", s)
            if mm:
                mask, local, stack = mm.group(1), {}, []
            p = parse_def_line(line)
            if p:
                f = split_fields(p[1]) + [""] * 12
                m = re.search(r'_ACX/([A-Z_]+\[\d+\])', f[6])
                if m:
                    local[p[0]] = m.group(1)
                if re.search(r"WR[04]", f[4]):
                    hidden4.add((mask, p[0]))              # hidden by default
                continue
            mi = re.match(r"IF\s+(.*)", s, re.I)
            if mi:
                names = re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\.VAL|([A-Za-z_][A-Za-z0-9_]*)\s*[=<>]", mi.group(1))
                labs = {switches[local[n]] for pair in names for n in pair if n in local and local[n] in switches}
                stack.append(labs)
                continue
            if re.match(r"ELSE\b", s, re.I) and stack:
                pass                       # else-branch is still governed by the same switch
                continue
            if re.match(r"ENDIF\b", s, re.I) and stack:
                stack.pop()
                continue
            mw = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\.WR\s*=\s*([0-4])", s)
            if mw:
                if mw.group(2) in "04":
                    hidden4.add((mask, mw.group(1)))       # this field can be hidden
                elif stack and set().union(*stack):
                    cand[(mask, mw.group(1))] |= set().union(*stack)
        for k, labs in cand.items():
            if k in hidden4:                               # shown only when the switch is on
                dep[(fn,) + k] |= labs
    return dep


def main():
    cells, secmarks = load_cells()
    switches = switch_vars()
    hid = hidden_fields(switches)
    issues = collections.defaultdict(list)
    req_by_cell = collections.defaultdict(list)
    sw_by_cell = collections.defaultdict(set)
    for fp in sorted(glob.glob(os.path.join(inventory.PROJ, "*.com"))):
        fn = os.path.basename(fp)
        for it in inventory.scan_file(fp, TEXTS):
            m = re.match(r"(section_\d+)#(S\d+D\d+)", it.get("help", "") or "")
            if not m:
                continue
            key = (m.group(1), m.group(2))
            req_by_cell[key].append(set(x for x in it["marks"] if x not in IGNORE))
            if (fn, it["mask"], it["name"]) in hid:
                sw_by_cell[key] |= hid[(fn, it["mask"], it["name"])]
    for key, reqs in sorted(req_by_cell.items()):
        if key not in cells:
            continue
        common = set.intersection(*reqs) if reqs else set()
        for have, p in cells[key]:
            have = set(have)
            miss = [r for r in sorted(common) if not satisfied(r, have)]
            if miss:
                issues["marker"].append(f"{key[0]}#{key[1]} 「{p['name']}」 字段只在 {miss} 下存在，帮助未加标记 (有 {sorted(have)})")
    for key, labs in sorted(sw_by_cell.items()):
        if key not in cells or key[0] == "section_7":
            continue
        txt = " ".join(f'{p.get("text", "")} {p.get("range", "")}' for _, p in cells[key])
        if CFG_WORD not in txt.lower():
            issues["switch"].append(f"{key[0]}#{key[1]} 「{cells[key][0][1]['name']}」 由机床配置 {sorted(labs)} 控制显示，帮助未说明")
    for cat, items in issues.items():
        print(f"== {cat}: {len(items)}")
        for x in items:
            print("  ", x)
    print("TOTAL", sum(len(v) for v in issues.values()))


if __name__ == "__main__":
    main()
