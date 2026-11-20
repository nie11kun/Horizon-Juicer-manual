"""One-off importer: convert an existing (legacy) parameter help section HTML into the YAML source format,
keeping anchors, texts and configuration markers, so it can be reviewed/extended instead of rewritten.

Usage: python tools/hlp_capture/html2yaml.py section_26 [--rev <git-rev>]
"""
import argparse
import html
import os
import re
import subprocess

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer"


def clean(s):
    s = re.sub(r'<b class="highlight">(.*?)</b>', r"**\1**", s, flags=re.S)
    s = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', r"[\2](\1)", s, flags=re.S)
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return "\n".join(l.strip() for l in s.split("\n") if l.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--rev", default="655bef85")
    a = ap.parse_args()
    t = subprocess.run(["git", "-C", SRC, "show", f"{a.rev}:Source_Library/HMI/hlp/chs/UserGuide/{a.name}.html"],
                       capture_output=True).stdout.decode("utf-8-sig")
    title = re.search(r"<title>(.*?)</title>", t).group(1)
    head1 = re.search(r'class="head1"><a[^>]*>(.*?)</a>', t).group(1)
    tokens = re.finditer(r'<!--(ifIs\w+?)(Begin|End)-->|<div class="head2">([^<\n]*)|<div class="parameterCell">(.*?)</div>', t, re.S)
    marks, blocks, cur = [], [], None
    first_head2 = True
    for m in tokens:
        if m.group(1):
            if m.group(2) == "Begin":
                marks.append(m.group(1))
            elif marks and marks[-1] == m.group(1):
                marks.pop()
        elif m.group(3) is not None:
            if first_head2:
                first_head2 = False
                continue
            cur = {"h3": m.group(3).strip(), "body": [{"params": []}]}
            blocks.append(cur)
        else:
            cell = m.group(4)
            pid = re.search(r'name="(S\d+D\d+)"', cell).group(1)
            tds = [clean(x) for x in re.findall(r"<td>(.*?)</td>", cell, re.S)]
            exp = re.search(r'<p class="parameterExplain">(.*?)</p>', cell, re.S)
            p = {"id": pid, "name": tds[0] if tds else pid,
                 "rec": (tds[1].replace("推荐设置：", "") if len(tds) > 1 else "无") or "无",
                 "range": (tds[3] if len(tds) > 3 else "无") or "无",
                 "text": clean(exp.group(1)) + "\n" if exp else ""}
            if marks:
                p["marks"] = list(marks)
            if cur is None:
                cur = {"h3": title, "body": [{"params": []}]}
                blocks.append(cur)
            cur["body"][0]["params"].append(p)
    doc = {"title": title, "head1": head1, "blocks": blocks}
    out = os.path.join(HERE, "hlp_src", "chs", f"{a.name}.yaml")
    yaml.safe_dump(doc, open(out, "w", encoding="utf-8"), allow_unicode=True, sort_keys=False, width=200)
    print(out, sum(len(b["body"][0]["params"]) for b in blocks), "params")


if __name__ == "__main__":
    main()
