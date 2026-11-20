"""HMI 帮助文档构建器：tools/hlp_capture/hlp_src/<lng>/*.yaml -> Source_Library/HMI/hlp/<lng>/。

输出严格沿用原西门子帮助格式：UTF-8 BOM + CRLF、main.css 既有 class
（head1~head4 / parameterCell / parameterExplain / var_mark / highlight / list / alarm1），
配置差异使用 ReplaceMarker.md 中定义的 <!--ifIsXxxBegin--> / <!--ifIsXxxEnd--> 标记。

YAML 源格式见 tools/hlp_capture/README.md。
用法: python tools/hlp_capture/build_hlp.py [--lng chs] [--check]
"""
import argparse
import html
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("HJ_SOURCE", r"C:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer")
SRC = os.path.join(HERE, "hlp_src")
DST = os.path.join(ROOT, "Source_Library", "HMI", "hlp")

AC_TEXT = {
    "1": "制造商口令", "2": "服务口令", "3": "用户口令",
    "4": "钥匙开关3档", "5": "钥匙开关2档", "6": "钥匙开关1档", "7": "钥匙开关0档（无限制）",
}
IND = "    "


class Out:
    def __init__(self):
        self.lines = []

    def w(self, depth, s):
        self.lines.append(IND * depth + s)

    def text(self):
        return "\r\n".join(self.lines) + "\r\n"


def inline(s):
    """行内标记：**强调**、[文字](链接)、`代码`。其余字符做 HTML 转义。"""
    s = str(s)
    parts = re.split(r"(\*\*.+?\*\*|\[[^\]]+\]\([^)]+\)|`[^`]+`)", s)
    out = []
    for p in parts:
        if p.startswith("**") and p.endswith("**") and len(p) > 4:
            out.append(f'<b class="highlight">{html.escape(p[2:-2], quote=False)}</b>')
        elif re.fullmatch(r"\[[^\]]+\]\([^)]+\)", p):
            t, h = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", p).groups()
            out.append(f'<a href="{h}" class="highlight">{html.escape(t, quote=False)}</a>')
        elif p.startswith("`") and p.endswith("`") and len(p) > 2:
            out.append(f"<b>{html.escape(p[1:-1], quote=False)}</b>")
        else:
            out.append(html.escape(p, quote=False))
    return "".join(out)


def marks_of(node):
    m = node.get("marks") if isinstance(node, dict) else None
    if not m:
        return []
    return [m] if isinstance(m, str) else list(m)


def open_marks(o, d, marks):
    for m in marks:
        o.w(d, f"<!--{m}Begin-->")


def close_marks(o, d, marks):
    for m in reversed(marks):
        o.w(d, f"<!--{m}End-->")


COND_LINE = re.compile(r"^\?([\w,]+):\s?(.*)$")


def text_lines(o, d, text):
    """多行文本 -> 每行 '<br>' 结尾；以 '?ifIsA,ifIsB: ' 开头的行仅在对应配置下保留。"""
    for raw in str(text).rstrip("\n").split("\n"):
        m = COND_LINE.match(raw)
        if m:
            ms = m.group(1).split(",")
            open_marks(o, d, ms)
            o.w(d, inline(m.group(2)) + "<br>")
            close_marks(o, d, ms)
        else:
            o.w(d, inline(raw) + "<br>")


def img_tag(img):
    if isinstance(img, str):
        img = {"src": img}
    h = img.get("h", 300)
    return f'<img src="resources/img/{img["src"]}" height="{h}">'


def nc_of(var):
    m = re.match(r"(\w+)\[(\d+)\]$", var or "")
    return f"{m.group(1)}[{int(m.group(2)) - 1}]" if m else ""


def emit_param(o, d, p, ids):
    pid = p["id"]
    if pid in ids:
        raise ValueError(f"重复锚点 {pid}")
    ids.add(pid)
    marks = marks_of(p)
    open_marks(o, d, marks)
    o.w(d, '<div class="parameterCell">')
    o.w(d + 1, '<table border="1" cellspacing="0" cellpadding="2" width="100%">')
    o.w(d + 2, "<tr>")
    o.w(d + 3, f'<td><a class="var_mark" name="{pid}">{inline(p["name"])}</a></td>')
    o.w(d + 3, f'<td>推荐设置：{inline(p.get("rec", "无"))}</td>')
    o.w(d + 2, "</tr>")
    o.w(d + 2, "<tr>")
    o.w(d + 3, "<td>取值范围</td>")
    rng = str(p.get("range", "无"))
    if p.get("unit"):
        rng += f'（单位：{p["unit"]}）'
    o.w(d + 3, f"<td>{inline(rng)}</td>")
    o.w(d + 2, "</tr>")
    o.w(d + 1, "</table>")
    o.w(d + 1, '<p class="parameterExplain">')
    if p.get("text"):
        text_lines(o, d + 2, p["text"])
    info = []
    if p.get("var"):
        nc = nc_of(p["var"])
        info.append(f'对应变量：{p["var"]}' + (f"（NC 程序中为 {nc}）" if nc else ""))
    if p.get("ac"):
        info.append(f'修改权限：{AC_TEXT[str(p["ac"])]}' + ("" if str(p["ac"]) == "7" else "及以上"))
    if p.get("readonly"):
        info.append("界面只读显示，由程序自动写入")
    if info:
        o.w(d + 2, "<i>" + html.escape("；".join(info), quote=False) + "</i><br>")
    o.w(d + 1, "</p>")
    for im in p.get("imgs", []) or []:
        o.w(d + 1, img_tag(im) + "<br>")
    o.w(d, "</div>")
    close_marks(o, d, marks)


def emit_steps(o, d, steps, ids):
    o.w(d, '<ol class="list">')
    for st in steps:
        if isinstance(st, str):
            st = {"t": st}
        marks = marks_of(st)
        open_marks(o, d + 1, marks)
        if "steps" in st and "t" not in st:  # 纯嵌套
            emit_steps(o, d + 1, st["steps"], ids)
        else:
            o.w(d + 1, f'<li>{inline(st["t"])}</li>' + (
                f'<br>{img_tag(st["img"])}<br><br>' if st.get("img") else ""))
            if st.get("note"):
                o.w(d + 1, '<p class="parameterExplain">')
                text_lines(o, d + 2, st["note"])
                o.w(d + 1, "</p>")
            for extra in st.get("imgs", []) or []:
                o.w(d + 1, f"{img_tag(extra)}<br><br>")
            if st.get("steps"):
                emit_steps(o, d + 1, st["steps"], ids)
        close_marks(o, d + 1, marks)
    o.w(d, "</ol>")


def emit_blocks(o, d, blocks, ids):
    for b in blocks or []:
        marks = marks_of(b)
        open_marks(o, d, marks)
        if "param" in b:
            emit_param(o, d, b["param"], ids)
        elif "params" in b:
            for p in b["params"]:
                emit_param(o, d, p, ids)
        elif "p" in b:
            o.w(d, "<p>")
            text_lines(o, d + 1, b["p"])
            o.w(d, "</p>")
        elif "note" in b:
            o.w(d, '<p class="parameterExplain">')
            text_lines(o, d + 1, b["note"])
            o.w(d, "</p>")
        elif "img" in b:
            o.w(d, f"{img_tag(b['img'])}<br>")
            if isinstance(b["img"], dict) and b["img"].get("cap"):
                o.w(d, f'<p class="parameterExplain">{inline(b["img"]["cap"])}</p>')
        elif "steps" in b:
            emit_steps(o, d, b["steps"], ids)
        elif "table" in b:
            o.w(d, '<table class="tableStyle" border="1" cellspacing="0" cellpadding="2" width="100%">')
            for i, row in enumerate(b["table"]):
                tag = "th" if i == 0 else "td"
                o.w(d + 1, "<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in row) + "</tr>")
            o.w(d, "</table>")
        elif "alarm" in b:
            o.w(d, f'<div class="alarm1">{inline(b["alarm"])}')
            emit_steps(o, d + 1, b.get("steps_", b.get("items", [])), ids)
            o.w(d, "</div>")
        elif "hr" in b:
            o.w(d, "<hr>")
        elif "h3" in b or "h4" in b:
            cls = "head3" if "h3" in b else "head4"
            title = b.get("h3", b.get("h4"))
            o.w(d, f'<div class="{cls}">{inline(title)}')
            o.w(d + 1, "<hr>")
            emit_blocks(o, d + 1, b.get("body", []), ids)
            o.w(d, "</div>")
        else:
            raise ValueError(f"未知块: {list(b)}")
        close_marks(o, d, marks)


def build_section(doc):
    o = Out()
    ids = set()
    o.w(0, "﻿<html>")
    o.w(1, "<head>")
    o.w(2, '<meta http-equiv="Content-Type" content="text/html; charset="UTF-8"/>')
    o.w(2, f"<title>{html.escape(doc['title'])}</title>")
    o.w(2, '<link rel="stylesheet" type="text/css" media="screen" href="main.css" />')
    o.w(1, "</head>")
    o.w(1, "")
    o.w(1, "<body>")
    o.w(2, f'<div class="head1"><a href="index.html">{html.escape(doc["head1"])}</a>')
    o.w(3, "<hr>")
    o.w(3, f'<div class="head2">{html.escape(doc["title"])}')
    o.w(4, "<hr>")
    if doc.get("refs"):
        o.w(4, "<p>")
        text_lines(o, 5, doc["refs"])
        o.w(4, "</p>")
        o.w(4, "<hr>")
    emit_blocks(o, 4, doc.get("blocks"), ids)
    o.w(3, "</div>")
    o.w(2, "</div>")
    o.w(1, "</body>")
    o.w(0, "</html>")
    return o.text(), ids


def build_toc(toc):
    """index.html + user_guide.xml。"""
    ih = Out()
    ih.w(0, "﻿<!DOCTYPE html>")
    ih.w(0, "<html>")
    ih.w(0, "<head>")
    ih.w(1, '<meta charset="utf-8" />')
    ih.w(1, "<title>User Guide</title>")
    ih.w(1, '<link rel="stylesheet" type="text/css" media="screen" href="main.css" />')
    ih.w(0, "</head>")
    ih.w(0, "")
    ih.w(0, "<body>")
    for line in toc["header"]:
        ih.w(1, f"<h1>{line}</h1>")
    ih.w(1, "<hr>")
    ih.w(1, "<ol>")
    xm = Out()
    xm.w(0, '<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
    xm.w(0, "<!DOCTYPE HMI_SL_HELP>")
    xm.w(0, f'<HMI_SL_HELP language="{toc["language"]}">')
    xm.w(1, f'<BOOK ref="index.html" title="{toc["book"]}" helpdir="UserGuide">')
    for part in toc["parts"]:
        first = part["entries"][0]["ref"]
        ih.w(2, f'<li><a class="title1" href="{first}">{part["title"]}</a></li>')
        ih.w(2, "<ol>")
        xm.w(2, f'<ENTRY ref ="{first}" title="{part["title"]}" >')
        for e in part["entries"]:
            ms = marks_of(e)
            open_marks(ih, 3, ms)
            ih.w(3, f'<li><a class="title2" href="{e["ref"]}">{e["title"]}</a></li>')
            close_marks(ih, 3, ms)
            for m in ms:
                xm.w(3, f"<!--{m}Begin-->")
            xm.w(3, f'<ENTRY ref ="{e["ref"]}" title="{e["title"]}" >')
            xm.w(4, f'<INDEX_ENTRY ref="{e["ref"]}" title="{e["title"]}" />')
            xm.w(3, "</ENTRY>")
            for m in reversed(ms):
                xm.w(3, f"<!--{m}End-->")
        ih.w(2, "</ol>")
        xm.w(2, "</ENTRY>")
    ih.w(1, "</ol>")
    ih.w(0, "")
    ih.w(0, "</body>")
    ih.w(0, "</html>")
    xm.w(1, "</BOOK>")
    xm.w(0, "</HMI_SL_HELP>")
    return ih.text(), xm.text()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lng", default="chs")
    ap.add_argument("--only", help="只构建指定 section 文件名，如 section_1")
    a = ap.parse_args()
    sdir = os.path.join(SRC, a.lng)
    ddir = os.path.join(DST, a.lng, "UserGuide")
    all_ids = {}
    for fn in sorted(os.listdir(sdir)):
        if not fn.endswith(".yaml") or fn == "toc.yaml":
            continue
        name = fn[:-5]
        if a.only and name != a.only:
            continue
        doc = yaml.safe_load(open(os.path.join(sdir, fn), encoding="utf-8"))
        text, ids = build_section(doc)
        for i in ids:
            if i in all_ids:
                sys.exit(f"锚点 {i} 同时出现在 {all_ids[i]} 与 {name}")
            all_ids[i] = name
        with open(os.path.join(ddir, f"{name}.html"), "w", encoding="utf-8", newline="") as f:
            f.write(text)
        print(f"{name}.html  锚点 {len(ids)}")
    tocp = os.path.join(sdir, "toc.yaml")
    if os.path.exists(tocp) and not a.only:
        toc = yaml.safe_load(open(tocp, encoding="utf-8"))
        ih, xm = build_toc(toc)
        with open(os.path.join(ddir, "index.html"), "w", encoding="utf-8", newline="") as f:
            f.write(ih)
        with open(os.path.join(DST, a.lng, "user_guide.xml"), "w", encoding="utf-8", newline="") as f:
            f.write(xm)
        print("index.html / user_guide.xml")


if __name__ == "__main__":
    main()
