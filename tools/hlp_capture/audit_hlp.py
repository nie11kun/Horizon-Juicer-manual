"""Self-review audit for the HMI help (chs).

Checks:
  1. every .com help link points to an existing section file + anchor
  2. every <a href="section_x.html#Sy"> inside the help points to an existing anchor
  3. ReplaceMarker comments are valid names and balanced Begin/End in every HTML/XML file
  4. every referenced image exists; lists unreferenced images (orphans)
  5. no internal variable names (ARRAY[n]) or NC/HMI index talk leaks into the end-user pages
  6. index.html / user_guide.xml entries point to existing files
Usage: python tools/hlp_capture/audit_hlp.py [--delete-orphans]
"""
import argparse
import glob
import os
import re

import inventory

SL = os.path.join(inventory.ROOT, "Source_Library")
HLP = os.path.join(SL, "HMI", "hlp", "chs")
UG = os.path.join(HLP, "UserGuide")
IMG = os.path.join(UG, "resources", "img")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--delete-orphans", action="store_true")
    a = ap.parse_args()
    errors = []
    valid_marks = set(re.findall(r"\|(ifIs\w+)", open(os.path.join(SL, "ReplaceMarker.md"), encoding="utf-8").read()))
    pages = {os.path.basename(p): open(p, encoding="utf-8-sig").read() for p in glob.glob(os.path.join(UG, "*.html"))}
    anchors = {f: set(re.findall(r'name="(S\d+D\d+)"', t)) for f, t in pages.items()}
    # 1 .com links
    n = 0
    for fp in glob.glob(os.path.join(SL, "HMI", "proj", "*.com")):
        for k, line in enumerate(open(fp, encoding="utf-8-sig"), 1):
            for sec, aid in re.findall(r'"UserGuide/(section_\d+\.html)"\s*,\s*"(S\d+D\d+)"', line):
                n += 1
                if aid not in anchors.get(sec, set()):
                    errors.append(f"[com-link] {os.path.basename(fp)}:{k} -> {sec}#{aid} missing")
    print(f"com help links checked: {n}")
    # 2 internal links, 3 markers, 4 images, 5 leaks
    used_imgs = set()
    for f, t in list(pages.items()) + [("user_guide.xml", open(os.path.join(HLP, "user_guide.xml"), encoding="utf-8").read())]:
        for href, aid in re.findall(r'href="(section_\d+\.html)(?:#(S\d+D\d+))?"', t):
            if href not in pages:
                errors.append(f"[link] {f} -> {href} missing")
            elif aid and aid not in anchors[href]:
                errors.append(f"[link] {f} -> {href}#{aid} missing")
        for ref in re.findall(r'ref ?="(section_\d+\.html)"', t):
            if ref not in pages:
                errors.append(f"[toc] {f} -> {ref} missing")
        stack = []
        for name, kind in re.findall(r"<!--(ifIs\w+?)(Begin|End|Line)-->", t):
            if name not in valid_marks:
                errors.append(f"[marker] {f}: unknown {name}")
            if kind == "Begin":
                stack.append(name)
            elif kind == "End":
                if not stack or stack[-1] != name:
                    errors.append(f"[marker] {f}: unbalanced {name}End")
                else:
                    stack.pop()
        if stack:
            errors.append(f"[marker] {f}: unclosed {stack}")
        for src in re.findall(r'<img src="resources/img/([^"]+)"', t):
            used_imgs.add(src)
            if not os.path.exists(os.path.join(IMG, src)):
                errors.append(f"[img] {f}: missing {src}")
        body = re.sub(r"<!--.*?-->", "", t, flags=re.S)
        body = re.sub(r"<[^>]+>", " ", body)
        for leak in re.findall(r"\b(?:INI|TECHNOLOGY|PROCESS|DRESSER|TOOL_SET|SHAPE_MODEL|GRIND|RING|WORK|WHEEL|SCREW_TAP|SERVICE_LIFE)\[\d+\]|HMI ?= ?NC|NC 程序中为", body):
            errors.append(f"[leak] {f}: {leak}")
    orphans = sorted(set(os.listdir(IMG)) - used_imgs)
    print(f"images referenced: {len(used_imgs)}, orphans: {len(orphans)}")
    if a.delete_orphans:
        for o in orphans:
            os.remove(os.path.join(IMG, o))
        print("deleted orphans")
    for e in errors:
        print(e)
    print("ALL HLP AUDITS PASSED" if not errors else f"{len(errors)} problems")


if __name__ == "__main__":
    main()
