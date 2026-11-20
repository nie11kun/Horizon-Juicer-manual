"""参数语义调研卷宗生成器。

基于 inventory.json，为每个界面可编辑参数汇总：
界面文字/枚举/单位/权限/配置标记、Parameter_Index.md 释义、现有帮助正文、
NC 程序（CMA/MPF/SPF/DEF）中的引用行。输出 tools/hlp_capture/out/xref/<画面>.md。

用法: python tools/hlp_capture/xref.py [--max-uses 12] [--file a_grind.com]
"""
import argparse
import collections
import glob
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("HJ_SOURCE", r"C:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer")
SL = os.path.join(ROOT, "Source_Library")
OUT = os.path.join(HERE, "out")
HLP = os.path.join(SL, "HMI", "hlp", "chs", "UserGuide")


def load_param_index():
    idx = {}
    with open(os.path.join(SL, "Parameter_Index.md"), encoding="utf-8") as f:
        for line in f:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and re.match(r"^\$?\w+\[\d+\]$", cells[0]):
                idx.setdefault(cells[0], []).append(" / ".join(c for c in cells[1:] if c))
    return idx


def load_nc_sources():
    files = []
    for ext in ("SPF", "spf", "MPF", "DEF"):
        files += glob.glob(os.path.join(SL, "**", f"*.{ext}"), recursive=True)
    src = {}
    for fp in sorted(set(files)):
        if os.sep + "HMI" + os.sep in fp:
            continue
        with open(fp, encoding="utf-8", errors="ignore") as f:
            src[os.path.relpath(fp, SL)] = f.read().splitlines()
    return src


def load_help():
    out = {}
    for fp in glob.glob(os.path.join(HLP, "section_*.html")):
        t = open(fp, encoding="utf-8-sig", errors="ignore").read()
        sec = os.path.basename(fp)[:-5]
        for m in re.finditer(r'name="(S\d+D\d+)"', t):
            end = t.find('</div>', m.end())
            chunk = t[m.start():end if end > 0 else m.end() + 2000]
            txt = re.sub(r"<!--.*?-->", "", chunk, flags=re.S)
            txt = re.sub(r"<br\s*/?>", " ⏎ ", txt)
            txt = re.sub(r"<[^>]+>", " ", txt)
            txt = html.unescape(re.sub(r"\s+", " ", txt)).strip()
            out[f"{sec}#{m.group(1)}"] = txt[len('name="') + len(m.group(1)) + 2:]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-uses", type=int, default=12)
    ap.add_argument("--file")
    a = ap.parse_args()
    inv = json.load(open(os.path.join(OUT, "inventory.json"), encoding="utf-8"))
    pidx = load_param_index()
    src = load_nc_sources()
    helps = load_help()
    os.makedirs(os.path.join(OUT, "xref"), exist_ok=True)
    byfile = collections.OrderedDict()
    for it in inv:
        if not it["visible"] or not it["var"].startswith("/NC/") or it["wr"] in ("0", "1"):
            continue
        if a.file and it["file"] != a.file:
            continue
        byfile.setdefault(it["file"], collections.OrderedDict()).setdefault(it["var"], []).append(it)
    for fn, vars_ in byfile.items():
        md = [f"# {fn} 参数调研卷宗", ""]
        for var, its in vars_.items():
            nc = its[0]["nc"]
            m = re.match(r"(\w+)\[(\d+)\]", nc)
            if m:
                pat = re.compile(rf"\b{m.group(1)}\[\s*{m.group(2)}\s*\]")
            else:
                nc = var.split("/")[-1]
                pat = re.compile(rf"\b{re.escape(nc)}\b")
            uses = []
            for rel, lines in src.items():
                for i, l in enumerate(lines, 1):
                    if pat.search(l):
                        uses.append(f"{rel}:{i}: {l.strip()[:160]}")
            md.append(f"## {nc}  (HMI {var.split('/')[-1]})")
            for it in its:
                md.append(f"- L{it['line']} {it['mask']} 「{it['long']}」/「{it['short']}」 "
                          f"单位[{it['unit']}] 类型[{it['type']}] 限值/枚举[{it['limits']}] "
                          f"WR{it['wr']} ac{it['ac']} 标记[{' '.join(it['marks'])}] "
                          f"帮助[{it['help']}] 注释[{it['comment']}]")
            for p in pidx.get(nc, []):
                md.append(f"- 索引: {p}")
            hs = {it["help"] for it in its if it["help"]}
            for h in hs:
                md.append(f"- 现有帮助: {helps.get(h, '(锚点缺失)')[:600]}")
            md.append(f"- NC 引用 {len(uses)} 处:")
            md += [f"    - {u}" for u in uses[:a.max_uses]]
            md.append("")
        with open(os.path.join(OUT, "xref", fn.replace(".com", ".md")), "w", encoding="utf-8") as f:
            f.write("\n".join(md))
        print(fn, len(vars_))


if __name__ == "__main__":
    main()
