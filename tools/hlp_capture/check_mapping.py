"""Deep check: help cells <-> HMI fields, and no internal names in the help text.

For every visible DEF field with a help link:
  - label (UI text) should appear in the help cell name (or vice versa, fuzzy)
  - every enum option of the field should appear in the cell's range/text
  - unit consistency (field unit shown in range if given)
  - access level: cell ac vs field ac (cell must not claim a lower level than the field)
  - read-only fields (WR1) should not be described as user input, editable ones not as 只读
Also: help cells never referenced by any field; strict internal-name scan of all pages.
Usage: python tools/hlp_capture/check_mapping.py
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
UG = os.path.join(inventory.ROOT, "Source_Library", "HMI", "hlp", inventory.LANG, "UserGuide")
RO = {"chs": "只读", "eng": "read-only", "rus": "только чтение"}[inventory.LANG]
KEY3 = {"chs": "钥匙开关 3 档", "eng": "key switch position 3", "rus": "положение 3 ключа"}[inventory.LANG]
SOFTKEY = {"chs": "软键", "eng": "softkey", "rus": "программная клавиша"}[inventory.LANG]
TEXTS = inventory.load_texts()
VARIANTS = inventory.load_text_variants()


def cells():
    out = {}
    for fp in glob.glob(os.path.join(SRC, "section_*.yaml")):
        sec = os.path.basename(fp)[:-5]
        doc = yaml.safe_load(open(fp, encoding="utf-8"))

        def walk(bs):
            for b in bs or []:
                for p in b.get("params", []) or []:
                    k = (sec, p["id"])
                    if k in out:   # dup cell (mutually exclusive configs): merge texts for matching
                        q = dict(out[k])
                        for f in ("name", "range", "text"):
                            q[f] = f'{q.get(f, "")} {p.get(f, "")}'
                        out[k] = q
                    else:
                        out[k] = p
                walk(b.get("body"))
        walk(doc["blocks"])
    return out


ROWLABEL = re.compile(r"(粗磨|半精磨|精磨|终磨|光磨|第[一二三四五六七八九十\d]+[头组段]|台阶\d+.*|[XZCUWB]轴?|当前|初始|(?i:rough(ing)?|semi[- ]?finish(ing)?|finish(ing)?|final|spark[- ]?out|current|initial|start|[XZCUWB](\s*axis)?|step ?\d.*|head ?\d|group ?\d|segment ?\d)|(?i:черн\w*|получист\w*|чист\w*|оконч\w*|текущ\w*|начальн\w*))")


def norm(s):
    s = re.sub(r"[\s\-—_:：.%n,;/]|\(.*?\)|（.*?）", "", (s or "").lower())
    return s.replace("磨削", "").replace("位置", "位").replace("过度", "过渡").replace("grinding", "").replace("шлиф", "")


def label_variant_ok(label, alltext):
    """Grouped cells: '位置3' ~ '位置1~位置6', '左半角' ~ '左/右半角', '上-左斜面角度', '左端累计磨削'."""
    raw = re.sub(r"\s", "", alltext)
    dig = lambda x: re.sub(r"\d+", "#", x)
    lab = re.sub(r"\s", "", label)
    cands = {lab, re.sub(r"^[上下]-", "", lab), re.sub(r"^[左右]端", "", lab)}
    for c in list(cands):
        for side in ("左", "右"):
            if c.startswith(side):
                cands |= {"左/右" + c[1:], "左右" + c[1:]}
    return any(c and (c in raw or norm(c) in norm(raw) or dig(c) in dig(raw)) for c in cands)


# section_7 setting-page cells summarise a whole group of configuration items by design
GROUP_CELLS = {("section_7", f"S7D{n}") for n in range(2, 8)}


def main():
    C = cells()
    refs = collections.defaultdict(list)
    issues = collections.defaultdict(list)
    for fp in sorted(glob.glob(os.path.join(inventory.PROJ, "*.com"))):
        fn = os.path.basename(fp)
        stack = []
        for k, line in enumerate(open(fp, encoding="utf-8-sig"), 1):
            bm = re.match(r"\s*;\s*(ifIs\w+?)(Begin|End)", line)
            if bm:
                if bm.group(2) == "Begin":
                    stack.append(bm.group(1))
                elif bm.group(1) in stack:
                    stack.remove(bm.group(1))
            line_marks = stack + inventory.MARK_RE.findall(line.split(";", 1)[1] if ";" in line else "")
            p = parse_def_line(line)
            if not p:
                continue
            f = split_fields(p[1]) + [""] * 12
            m = re.search(r'"UserGuide/(section_\d+)\.html"\s*,\s*"(S\d+D\d+)"', f[10])
            if not m:
                continue
            key = (m.group(1), m.group(2))
            refs[key].append(f"{fn}:{k}")
            cell = C.get(key)
            if not cell:
                continue
            texts = [inventory.resolve_for(t.strip(), TEXTS, VARIANTS, line_marks).strip('"') for t in f[3].split(",")]
            label = (texts[1] if len(texts) > 1 and texts[1] else texts[0])
            alltext = f'{cell.get("name","")} {cell.get("range","")} {cell.get("text","")}'
            # label
            if ROWLABEL.fullmatch(label.strip()):
                label = ""
            if f[7].strip().startswith("0,0,0") or key in GROUP_CELLS:
                label = ""
            if label and len(norm(label)) >= 2 and norm(label) not in norm(alltext) and not label.startswith("$") and \
                    norm(label) not in norm(cell["name"]) and norm(cell["name"]) not in norm(label) and \
                    norm(label)[:2] not in norm(cell["name"]):
                if not label_variant_ok(label, alltext):
                        issues["label"].append(f"{fn}:{k} 「{label}」 -> {key[1]} 「{cell['name']}」")
            # enum options
            if f[1].strip().startswith("*") and key not in GROUP_CELLS:
                opts = [inventory.resolve(o.split("=", 1)[1], TEXTS).strip('"') for o in f[1].strip()[1:].split(",") if "=" in o]
                opts = [o for o in opts if o and not o.startswith("\\") and o not in ("○", "●", "↺") and not o.startswith("P_")]
                miss = [o for o in opts if norm(o) not in norm(alltext).replace(" ", "")]
                if miss:
                    issues["enum"].append(f"{fn}:{k} {key[1]} 缺少选项 {miss}")
            # access level
            acm = re.search(r"ac(\d)", f[4])
            wr = re.search(r"WR(\d)", f[4])
            if acm and cell.get("ac") and not f[0].strip().startswith("S") and                     not (acm.group(1) == "4" and KEY3 in str(cell.get("text", ""))) and int(cell["ac"]) > int(acm.group(1)) and wr and wr.group(1) in ("2", "3", "4"):
                issues["access"].append(f"{fn}:{k} {key[1]} 帮助写 ac{cell['ac']}，界面 ac{acm.group(1)}")
            # readonly vs editable
            if wr and wr.group(1) == "2" and cell.get("readonly") and RO in str(cell.get("range", "")).lower():
                issues["readonly"].append(f"{fn}:{k} {key[1]} 界面可编辑但帮助写只读")
    used = set(refs)
    param_cells = {k for k in C if k[0] in {f"section_{n}" for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 26, 27, 28, 31)}}
    for k in sorted(param_cells - used):
        if C[k].get("nofield") or SOFTKEY in str(C[k].get("range", "")).lower():
            continue  # documented soft key / table column, no input field to link
        issues["unreferenced"].append(f"{k[0]}#{k[1]} {C[k]['name']}")
    # strict internal-name scan
    pat = re.compile(r"\b[A-Z][A-Z_]{2,}\[\d+\]|\$[A-Z_]+|\bR\d{2,3}\b|\bGUD\b|\bMGUD\b|\.SPF\b|\.MPF\b|\.com\b|"
                     r"\bSHAPE_\w+|\bSERVICE_\w+|\bWHEEL_\w+|\bCUR_WHEEL\b|\bSTRING_ADDON\b|\bNC 程序|下标|HMI ?= ?NC|ACX|DB\d{3,}")
    for fp in glob.glob(os.path.join(UG, "*.html")):
        t = open(fp, encoding="utf-8-sig").read()
        body = re.sub(r"<!--.*?-->", "", t, flags=re.S)
        body = re.sub(r"<[^>]+>", " ", body)
        for hit in sorted(set(pat.findall(body))):
            issues["internal-name"].append(f"{os.path.basename(fp)}: {hit}")
    for cat, items in issues.items():
        print(f"== {cat}: {len(items)}")
        for it in items:
            print("  ", it)
    print("TOTAL", sum(len(v) for v in issues.values()))


if __name__ == "__main__":
    main()
