"""按 Mask 打印可见控件紧凑布局：行号 位置 文字 变量 枚举 标记 帮助。
用法: python tools/hlp_capture/masks.py a_grind.com [Mask1 ...]"""
import json, os, sys
inv = json.load(open(os.path.join(os.path.dirname(__file__), "out", "inventory.json"), encoding="utf-8"))
fn, masks = sys.argv[1], set(sys.argv[2:])
for it in inv:
    if it["file"] != fn or not it["visible"] or (masks and it["mask"] not in masks):
        continue
    v = it["var"].replace("/NC/_N_NC_GD2_ACX/", "")
    print(f'{it["mask"]:7} L{it["line"]:<5} [{it["pos"]:>13}] {it["long"] or it["name"]}|{it["short"]} '
          f'{v} WR{it["wr"]}ac{it["ac"]} {it["limits"][:40]} {it["unit"]} <{" ".join(it["marks"])}> {it["help"]}')
