"""HMI 参数清单生成器。

扫描 Source_Library/HMI/proj/*.com，提取每个 DEF 控件：
所在画面/Mask、GUD 变量（HMI 1-based 与 NC 0-based）、界面文字（almc_chs.txt）、
权限、配置标记、显示位置、当前帮助锚点。输出 JSON + Markdown 清单。

用法: python tools/hlp_capture/inventory.py [--out DIR]
"""
import argparse
import collections
import json
import os
import re
import sys


def _pick_lang():
    """--lng chs|eng|rus (removed from argv so the scripts' own parsers never see it) or env HLP_LNG."""
    if "--lng" in sys.argv:
        i = sys.argv.index("--lng")
        os.environ["HLP_LNG"] = sys.argv[i + 1]
        del sys.argv[i:i + 2]
    return os.environ.get("HLP_LNG", "chs")


LANG = _pick_lang()

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("HJ_SOURCE", r"C:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer")
HMI = os.path.join(ROOT, "Source_Library", "HMI")
PROJ = os.path.join(HMI, "proj")
LNG = os.path.join(HMI, "lng", f"almc_{LANG}.txt")

MARK_RE = re.compile(r"\bifIs[A-Za-z0-9]+")


def load_texts(path=LNG):
    texts = {}
    with open(path, encoding="utf-8-sig", errors="ignore") as f:
        for line in f:
            m = re.match(r'\s*(\d+)\s+\d+\s+\d+\s+"(.*?)"', line)
            if m:
                texts[m.group(1)] = m.group(2)
    return texts


def load_text_variants(path=LNG):
    """id -> [(text, [marks])]: the lng files hold config-specific versions of one text id
    (e.g. 85165 = 对刀起始位.X ;ifIsExternal / 工件中心.X ;ifIsInternal)."""
    out = collections.defaultdict(list)
    with open(path, encoding="utf-8-sig", errors="ignore") as f:
        for line in f:
            m = re.match(r'\s*(\d+)\s+\d+\s+\d+\s+"(.*?)"(.*)', line)
            if m:
                out[m.group(1)].append((m.group(2), MARK_RE.findall(m.group(3))))
    return out


def resolve_for(s, texts, variants, marks):
    """Like resolve(), but picks the text version whose config marks the field has."""
    implied = {"ifIsScrewTap": "ifIsExternal", "ifIsCenter": "ifIsInternal", "ifIsInternalOnly": "ifIsInternal"}
    marks = set(marks) | {implied[x] for x in marks if x in implied}

    def one(m):
        vs = variants.get(m.group(1), [])
        fit = [t for t, ms in vs if ms and set(ms) <= set(marks)]
        return fit[0] if len(fit) == 1 else texts.get(m.group(1), m.group(0))
    return re.sub(r"\$(\d{5})", one, s)


def split_fields(body):
    """按 '/' 拆分 DEF 括号体，忽略引号与圆括号内的 '/'。"""
    out, cur, q, depth = [], [], False, 0
    for ch in body:
        if ch == '"':
            q = not q
        elif not q and ch == "(":
            depth += 1
        elif not q and ch == ")":
            depth -= 1
        if ch == "/" and not q and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return out


def resolve(s, texts):
    return re.sub(r"\$(\d{5})", lambda m: texts.get(m.group(1), m.group(0)), s)


def nc_index(var):
    m = re.match(r"/NC/_N_NC_GD2_ACX/(\w+)\[(\d+)\]", var or "")
    if not m:
        return ""
    return f"{m.group(1)}[{int(m.group(2)) - 1}]"


def parse_def_line(line):
    """返回 (name, body, trailing_comment) 或 None。"""
    s = line.strip()
    if not s.startswith("DEF "):
        return None
    m = re.match(r"DEF\s+(\w+)\s*=\s*\(", s)
    if not m:
        return None
    i, depth, q = m.end() - 1, 0, False
    for j in range(i, len(s)):
        ch = s[j]
        if ch == '"':
            q = not q
        elif not q and ch == "(":
            depth += 1
        elif not q and ch == ")":
            depth -= 1
            if depth == 0:
                return m.group(1), s[i + 1:j], s[j + 1:]
    return None


def scan_file(path, texts):
    base = os.path.basename(path)
    items = []
    stack = []
    mask = ""
    mask_title = ""
    with open(path, encoding="utf-8-sig", errors="ignore") as f:
        lines = f.read().splitlines()
    for ln, raw in enumerate(lines, 1):
        s = raw.strip()
        # 区块标记
        for mk in re.findall(r";\s*(ifIs[A-Za-z0-9]+?)(Begin|End)\b", s):
            if not s.startswith("DEF"):
                if mk[1] == "Begin":
                    stack.append(mk[0])
                elif stack and stack[-1] == mk[0]:
                    stack.pop()
                elif mk[0] in stack:
                    stack.remove(mk[0])
        mm = re.match(r"//M\((\w+)/([^/]*)/", s)
        if mm:
            mask = mm.group(1)
            mask_title = resolve(mm.group(2), texts).strip('"')
            continue
        p = parse_def_line(raw)
        if not p:
            continue
        name, body, tail = p
        fl = split_fields(body) + [""] * 12
        typ, limits, default, txt, attr, pic, var, pos_s, pos_i, colors = fl[:10]
        help_f = fl[10]
        tparts = [t.strip() for t in txt.split(",")]
        long_t = resolve(tparts[0], texts) if tparts else ""
        short_t = resolve(tparts[1], texts) if len(tparts) > 1 else ""
        unit_t = resolve(tparts[3], texts) if len(tparts) > 3 else ""
        hm = re.search(r'"UserGuide/(section_\d+)\.html"\s*,\s*"(S\d+D\d+)"', help_f)
        pos_i_s = pos_i.strip()
        visible = bool(pos_i_s) and not pos_i_s.startswith("0,0,0")
        comment = tail.split(";", 1)[1].strip() if ";" in tail else ""
        line_marks = MARK_RE.findall(comment)
        wr = re.search(r"WR(\d)", attr)
        ac = re.search(r"ac(\d)", attr)
        varm = re.search(r'"([^"]+)"', var)
        items.append({
            "file": base, "line": ln, "mask": mask, "mask_title": mask_title,
            "name": name, "type": typ.strip(), "limits": resolve(limits, texts),
            "default": default, "long": long_t, "short": short_t, "unit": unit_t,
            "wr": wr.group(1) if wr else "", "ac": ac.group(1) if ac else "",
            "pic": pic.strip('"'), "var": varm.group(1) if varm else "",
            "nc": nc_index(varm.group(1) if varm else ""),
            "pos": pos_i_s, "visible": visible,
            "marks": list(stack) + line_marks,
            "help": f"{hm.group(1)}#{hm.group(2)}" if hm else "",
            "comment": comment,
        })
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    texts = load_texts()
    allitems = []
    for fn in sorted(os.listdir(PROJ)):
        if fn.endswith(".com"):
            allitems += scan_file(os.path.join(PROJ, fn), texts)
    with open(os.path.join(a.out, "inventory.json"), "w", encoding="utf-8") as f:
        json.dump(allitems, f, ensure_ascii=False, indent=1)
    # Markdown：按文件/Mask 分组，同一变量去重
    md = ["# HMI 参数清单（自动生成）", "",
          "NC 下标 = HMI ACX 下标 - 1。仅列出界面可见控件（输入位置非 0,0,0）。", ""]
    groups = collections.OrderedDict()
    for it in allitems:
        if not it["visible"]:
            continue
        groups.setdefault((it["file"], it["mask"], it["mask_title"]), []).append(it)
    stats = collections.Counter()
    for (fn, mk, mt), its in groups.items():
        md += [f"## {fn} · {mk} · {mt}", "",
               "| 行 | 界面文字 | HMI 变量 / NC | 权限 | 配置标记 | 帮助 |",
               "|---|---|---|---|---|---|"]
        seen = set()
        for it in its:
            key = (it["var"] or it["name"], it["long"], tuple(it["marks"]))
            if key in seen:
                continue
            seen.add(key)
            stats["visible"] += 1
            stats["with_help"] += bool(it["help"])
            label = (it["long"] or it["short"] or it["name"]).replace("|", "/")
            v = f'{it["var"].replace("/NC/_N_NC_GD2_ACX/", "")} / {it["nc"]}' if it["nc"] else it["var"]
            md.append(f'| {it["line"]} | {label} | {v} | WR{it["wr"]} ac{it["ac"]} | '
                      f'{" ".join(it["marks"])} | {it["help"]} |')
        md.append("")
    md.insert(3, f'可见控件 {stats["visible"]} 个（同 Mask 去重），已有帮助 {stats["with_help"]} 个。')
    with open(os.path.join(a.out, "inventory.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(dict(stats), "->", a.out)


if __name__ == "__main__":
    main()
