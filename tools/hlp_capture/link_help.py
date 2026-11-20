"""Attach/repair HMI help links in Source_Library/HMI/proj/*.com.

For every visible DEF field the help field `"UserGuide/section_N.html","SnDm"` is set to the anchor whose YAML
`var` matches the field's variable (same screen's section preferred, configuration markers used to pick between
alternatives). Existing links are kept when their anchor still exists and agrees with the field's var
(a link to an anchor that documents a different var is re-pointed, except in a_setting.com). Only the help field at the end of the
DEF body is touched; everything else in the line stays byte-identical.

Usage: python tools/hlp_capture/link_help.py            (dry run, report)
       python tools/hlp_capture/link_help.py --write
"""
import argparse
import collections
import glob
import os
import re

import yaml

from inventory import PROJ, parse_def_line, split_fields, MARK_RE  # noqa: F401
import inventory

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "hlp_src", "chs")
HLP = os.path.join(inventory.ROOT, "Source_Library", "HMI", "hlp", "chs", "UserGuide")

FILE_SECTION = {
    "a_grind.com": "section_1", "a_process.com": "section_2", "a_dress.com": "section_3",
    "a_dressware.com": "section_4", "a_auto.com": "section_5", "a_shapecommon.com": "section_6",
    "a_setting.com": "section_7", "a_stats.com": "section_8", "a_info.com": "section_9",
    "a_custom.com": "section_9", "a_centerwaiyuan.com": "section_26", "a_centerduanmian.com": "section_27",
    "a_centermain.com": "section_28", "a_backup_restore.com": "section_31",
}
# fields without an NC variable, matched by label text: (file or *, label regex) -> anchor
LABEL_RULES = [
    ("a_grind.com", r"参数锁定开关", "section_1", "S1D56"),
    ("a_dressware.com", r"参数锁定开关", "section_4", "S4D17"),
    ("a_dressware.com", r"修整轮间距", "section_4", "S4D8"),
    ("a_stats.com", r"参数锁定开关|修整次数", "section_8", "S8D3"),
    ("a_stats.com", r"重置", "section_8", "S8D13"),
    ("a_dress.com", r"外部程序|外部齿型", "section_3", "S3D28"),
    ("a_dress.com", r"^齿高$|^抬刀$", "section_3", "S3D29"),
    ("a_dress.com", r"MODEL_NAME|蜗杆", "section_3", "S3D30"),
    ("a_dress.com", r"修整轮类型", "section_3", "S3D31"),
    ("a_setting.com", r"口令验证", "section_7", "S7D1"),
    ("a_shapecommon.com", r"多线修整", "section_6", "S6D30"),
    ("a_shapecommon.com", r"^牙数$", "section_6", "S6D31"),
    ("a_shapecommon.com", r"间隔螺距", "section_6", "S6D32"),
    ("a_shapecommon.com", r"齿高补偿", "section_6", "S6D33"),
    ("a_centerwaiyuan.com", r"磨削起点|磨削终点", "section_26", "S26D56"),
]
SETTING_GROUPS = [("磨削相关", "S7D2"), ("修整相关", "S7D3"), ("对刀相关", "S7D4"),
                  ("磨削中心相关", "S7D5"), ("隐藏界面激活", "S7D6"), ("输入范围限制", "S7D7")]


def norm_var(v):
    v = v.strip().replace("/NC/_N_NC_GD2_ACX/", "")
    m = re.fullmatch(r"\$?R\[?(\d+)\]?", v)
    if m:
        return f"R[{m.group(1)}]"
    return v


def expand(var_text):
    """'A[1]~A[5]、B[2] / C[3]' -> {'A[1]',...,'A[5]','B[2]','C[3]'}"""
    out = set()
    for part in re.split(r"[、/；;，,]|\s{2,}", var_text):
        part = re.sub(r"[（(].*?[）)]|批量|单件|槽距|槽升量|进刀|角度|锥度|转速", " ", part).strip()
        for tok in re.findall(r"\$?[A-Z_]+\[?\d*\]?(?:\s*~\s*\$?[A-Z_]+\[?\d+\]?)?", part):
            m = re.fullmatch(r"\$?([A-Z_]+)\[?(\d+)\]?\s*~\s*\$?([A-Z_]+)\[?(\d+)\]?", tok)
            if m and m.group(1) == m.group(3):
                for i in range(int(m.group(2)), int(m.group(4)) + 1):
                    out.add(norm_var(f"{m.group(1)}[{i}]"))
            else:
                out.add(norm_var(tok.replace(" ", "")))
    return out


def load_anchors():
    """var -> [(section, id, marks)], plus set of all anchors per section (from built HTML)."""
    by_var = collections.defaultdict(list)
    for fp in glob.glob(os.path.join(SRC, "section_*.yaml")):
        sec = os.path.basename(fp)[:-5]
        doc = yaml.safe_load(open(fp, encoding="utf-8"))

        def walk(blocks, inherited):
            for b in blocks or []:
                mk = inherited + list(b.get("marks", []) or [])
                for p in b.get("params", []) or []:
                    if p.get("var"):
                        for v in expand(str(p["var"])):
                            by_var[v].append((sec, p["id"], mk + list(p.get("marks", []) or [])))
                walk(b.get("body"), mk)
        walk(doc.get("blocks"), [])
    exists = {}
    for fp in glob.glob(os.path.join(HLP, "section_*.html")):
        exists[os.path.basename(fp)[:-5]] = set(re.findall(r'name="(S\d+D\d+)"', open(fp, encoding="utf-8-sig").read()))
    return by_var, exists


def choose(cands, sec, marks):
    if not cands:
        return None
    same = [c for c in cands if c[0] == sec] or cands
    best = max(same, key=lambda c: (len(set(c[2]) & set(marks)) - len(set(c[2]) - set(marks))))
    return best[0], best[1]


def set_help(line, sec, aid):
    p = parse_def_line(line)
    name, body, tail = p
    fields = split_fields(body)
    help_txt = f'"UserGuide/{sec}.html","{aid}"'
    while len(fields) < 10:
        fields.append("")
    if len(fields) == 10:
        fields.append(help_txt)
    else:
        fields[10] = help_txt
    new_body = "/".join(fields)
    i = line.index(body)
    return line[:i] + new_body + line[i + len(body):]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    by_var, exists = load_anchors()
    stats = collections.Counter()
    unmatched = collections.defaultdict(list)
    for fp in sorted(glob.glob(os.path.join(PROJ, "*.com"))):
        fn = os.path.basename(fp)
        sec = FILE_SECTION.get(fn)
        raw = open(fp, "rb").read()
        bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig")
        nl = "\r\n" if "\r\n" in text else "\n"
        lines = text.split(nl)
        stack, group = [], None
        changed = False
        for k, line in enumerate(lines):
            s = line.strip()
            for mk in re.findall(r";\s*(ifIs[A-Za-z0-9]+?)(Begin|End)\b", s):
                if not s.startswith("DEF"):
                    if mk[1] == "Begin":
                        stack.append(mk[0])
                    elif mk[0] in stack:
                        stack.remove(mk[0])
            p = parse_def_line(line)
            if not p:
                continue
            fields = split_fields(p[1]) + [""] * 12
            pos = fields[8].strip()
            if not pos or pos.startswith("0,0,0") or "WR0" in fields[4]:
                continue
            label = inventory.resolve(fields[3].split(",")[0].strip(), TEXTS).strip('"')
            if fn == "a_setting.com":
                for g, gid in SETTING_GROUPS:
                    if g in label:
                        group = gid
            varm = re.search(r'"([^"]+)"', fields[6])
            var = norm_var(varm.group(1)) if varm else ""
            if var.startswith("$AA_") or var.startswith("$AC_") or var.startswith("/Plc") or var.startswith("$A_"):
                continue
            marks = list(stack) + MARK_RE.findall(p[2])
            cur = re.search(r'"UserGuide/(section_\d+)\.html"\s*,\s*"(S\d+D\d+)"', fields[10])
            target = None
            cands = by_var.get(var, []) if var else []
            if cur and cur.group(2) in exists.get(cur.group(1), set()):
                # keep a valid link unless the parameter's var is documented under a different anchor
                if fn == "a_setting.com" or not cands or (cur.group(1), cur.group(2)) in {(c[0], c[1]) for c in cands}:
                    stats["kept"] += 1
                    continue
                target = choose(cands, sec, marks)
                print(f"  relink {fn}:L{k + 1} {label or p[0]} {var}: {cur.group(2)} -> {target[1]}")
                stats["relinked"] += 1
                lines[k] = set_help(line, *target)
                changed = True
                continue
            target = choose(cands, sec, marks) if var else None
            if not target:
                for f, rx, tsec, tid in LABEL_RULES:
                    if f == fn and re.search(rx, label or p[0]):
                        target = (tsec, tid)
                        break
            if not target and fn == "a_setting.com" and group:
                target = ("section_7", group)
            if not target:
                if cur:
                    stats["broken_unfixed"] += 1
                unmatched[fn].append(f"L{k + 1} {label or p[0]} {var}")
                continue
            stats["fixed" if cur else "added"] += 1
            lines[k] = set_help(line, *target)
            changed = True
        if changed and a.write:
            out = nl.join(lines)
            open(fp, "wb").write((b"\xef\xbb\xbf" if bom else b"") + out.encode("utf-8"))
    print(dict(stats))
    for fn, items in unmatched.items():
        print(f"== {fn} unmatched {len(items)}")
        for it in items[:40]:
            print("  ", it)


TEXTS = inventory.load_texts()

if __name__ == "__main__":
    main()
