#!/usr/bin/env python3
"""
从 Horizon-Juicer 与 HorizonJuicerCreator 源码直接生成第 10 章全量索引小节：
- 10.2 m_codes_and_signals.md (M0~M99 全量 M 代码 + PLC-NC 46 项 + 快速 I/O 14 项)
- 10.3 config_ui_variables.md (a_setting.com 93+1+9 项 + SUB(UP1..UP9) + Creator 31 项 JSON)
- 10.4 full_variable_index.md (MGUD.DEF 60 项 + Parameter_Index.md 1,561 项 + 补充 22 项)
- 10.5 replace_markers.md (66 项 ifIs 条件编译标记 + 占位/文本替换规则 + oneReplace.json 47 项)
"""

import json
import os
import re
import sys
import xml.etree.ElementTree as ET

MANUAL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HJ_ROOT = r"c:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer"
SRC_LIB = os.path.join(HJ_ROOT, "Source_Library")
CREATOR_ROOT = r"c:\Users\Marco Nie\Development\WorkProgram\HorizonJuicerCreator"

OUT_DIR = os.path.join(MANUAL_ROOT, "10_appendix_and_troubleshooting")


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def escape_dollar_vars(text):
    """Replace $VAR[...] or $VAR with <code>&#36;...</code> safely outside existing tags."""
    if not text:
        return text

    def _repl(m):
        return f"<code>&#36;{m.group(1)}</code>"

    # Match $A_DBB[12], $MN_HW_SERIAL_NUMBER, $AC_MEA[1], etc.
    text = re.sub(r"\$([A-Za-z][A-Za-z0-9_]*(?:\[\d+\])?)", _repl, text)
    # Any leftover lone '$' -> &#36;
    text = text.replace("$", "&#36;")
    return text


def sanitize_cell(text, is_var_context=False):
    """Clean cell text for HonKit Markdown tables and audit_manual rules."""
    if text is None:
        return ""
    s = str(text).strip()
    s = s.replace("|", " / ")
    # Normalize whitespace
    s = re.sub(r"\s+", " ", s).strip()
    # Fix bare parenthesized numbers/shorthands that could clash with audit_manual
    # e.g. 前(0)/后(1) -> 0=前 / 1=后
    s = s.replace("前(0)/后(1)", "0=前 / 1=后")
    s = s.replace("(0:当前c起始角/1:0度对刀)", "（0=当前 C 起始角 / 1=0° 对刀）")
    s = s.replace("(0.9-1.2)", "（标准 0.9 / 1.2 切换）")
    s = s.replace("(1-24)", "（范围 1～24）")
    s = s.replace("(0:G17-12几何轴/1:G18-13几何轴/2:G19-23几何轴)",
                  "（0=G17 1-2几何轴 / 1=G18 1-3几何轴 / 2=G19 2-3几何轴）")
    s = s.replace("(45-90)", "（范围 45°～90°）")
    s = s.replace("(1工件后/-1工件前)", "（1=工件后 / -1=工件前）")
    # Convert standalone (0否1是) or (0否/1是) etc. nicely if needed; keep clear
    s = escape_dollar_vars(s)
    # Prevent unescaped markdown delimiters inside normal table prose
    s = s.replace("`", "")
    # Escape asterisks only if not paired cleanly
    if "*" in s:
        s = s.replace("*", "×")
    return s


def fmt_code(token):
    """Format a non-$ identifier or value as inline code, or <code>&#36;...</code> if $."""
    t = token.strip()
    if "$" in t:
        return escape_dollar_vars(t)
    t = t.replace("|", "/")
    return f"`{t}`"


def make_hmi_var(nc_var):
    """Compute 1-based HMI ACX variable name from 0-based NC variable name."""
    m = re.match(r"^([A-Z0-9_]+)\[(\d+)\]$", nc_var.strip())
    if m:
        return f"{m.group(1)}[{int(m.group(2)) + 1}]"
    return nc_var.strip()


# ---------------------------------------------------------------------------
# 10.2 m_codes_and_signals.md
# ---------------------------------------------------------------------------
def build_m_codes_and_signals():
    ms_text = read_text(os.path.join(SRC_LIB, "M-sympol_Index.md"))
    pi_text = read_text(os.path.join(SRC_LIB, "Parameter_Index.md"))

    # Parse M-sympol_Index.md
    m_raw = {}
    for line in ms_text.splitlines():
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if parts and re.match(r"^M\d+$", parts[0]):
            m_raw[int(parts[0][1:])] = parts[1] if len(parts) > 1 else ""

    # Scope & remark overrides based on verified NC source inspection
    sys_codes = {0, 1, 2, 3, 4, 5, 6, 17, 19, 30, 32, 40, 41, 42, 43, 44, 45, 70}
    jxs_codes = {80, 81, 82, 83, 84, 85, 86, 87, 88, 89}

    m_rows = []
    for n in range(100):
        code = f"M{n}"
        raw_desc = m_raw.get(n, "").strip()

        # Classify scope
        if n in sys_codes:
            scope = "西门子系统"
        elif n in jxs_codes:
            scope = "机械手握手"
        elif n in {92, 93, 94, 95, 96, 97}:
            scope = "复用定制（机械手/量仪/防护罩/测头）"
        elif raw_desc == "":
            scope = "未分配 / 预留"
        else:
            scope = "Horizon-Juicer 定制"

        # Refined verified definitions & notes
        note = "—"
        if n == 38:
            desc = "淋浴冷却 / 外磨冷却（冷却泵 3）启动"
            note = "用于磨削中心外圆/端面磨削及修整冷却控制"
        elif n == 39:
            desc = "淋浴冷却 / 外磨冷却（冷却泵 3）停止"
            note = "与 `M38` 成对使用"
        elif n == 75:
            desc = "液压卡盘夹紧"
            note = "与 `M76` 成对使用"
        elif n == 88:
            desc = "尾架顶尖伸出到位信号置 1（有效）"
            note = "置位 <code>&#36;A_DBB[64]</code> / `DB4900.DBX64.0`"
        elif n == 89:
            desc = "尾架顶尖伸出到位信号置 0（复位）"
            note = "复位 <code>&#36;A_DBB[64]</code> / `DB4900.DBX64.0`"
        elif n == 92:
            desc = "机械手：液压卡盘松开到位信号置 1（有效）；磨削中心：外圆在线测量气缸伸出"
            note = "机械手置位 <code>&#36;A_DBB[65]</code>；在线测量见 `I_CYCLE.SPF`"
        elif n == 93:
            desc = "机械手：液压卡盘松开到位信号置 0（复位）；磨削中心：外圆在线测量气缸缩回"
            note = "机械手复位 <code>&#36;A_DBB[65]</code>；退回见 `J_GRIND_ONLINE.SPF`"
        elif n == 94:
            desc = "机械手：液压卡盘夹紧到位信号置 1（有效）；内螺纹：头架防护罩壳伸出"
            note = "机械手置位 <code>&#36;A_DBB[66]</code>；防护罩见 `F_SHIELD_CONTROL.SPF`"
        elif n == 95:
            desc = "机械手：液压卡盘夹紧到位信号置 0（复位）；内螺纹：头架防护罩壳缩回"
            note = "机械手复位 <code>&#36;A_DBB[66]</code>；防护罩见 `F_SHIELD_CONTROL.SPF`"
        elif n == 96:
            desc = "机械手：吹气旋转头架复位 / 吹气完成回位信号；自动对刀：`E_PROBE_DISABLE.SPF` 测头信号无效"
            note = "索引表标注 <code>&#36;A_DBB[67]</code> 置 0；`B_JXS_ZJ.SPF` 实际以 `M96` 发吹气完成有效信号"
        elif n == 97:
            desc = "机械手：吹气旋转头架有效 / 信号复位；自动对刀：`E_PROBE_ENABLE.SPF` 测头信号有效"
            note = "索引表标注 <code>&#36;A_DBB[67]</code> 置 1；`A_JXS_MAIN.SPF`/`B_JXS_ZJ.SPF` 用 `M97` 复位该信号"
        elif n == 98:
            desc = "未分配 / 预留（源码 `M-sympol_Index.md` 未定义）"
            note = "—"
        elif raw_desc == "":
            desc = "未分配 / 预留"
        else:
            desc = sanitize_cell(raw_desc)
            if n == 80 or n == 81:
                note = f"{'置位' if n == 80 else '复位'} <code>&#36;A_DBB[60]</code> / `DB4900.DBX60.0`（备妥信号）"
            elif n == 82 or n == 83:
                note = f"{'置位' if n == 82 else '复位'} <code>&#36;A_DBB[61]</code> / `DB4900.DBX61.0`（预完成信号）"
            elif n == 84 or n == 85:
                note = f"{'置位' if n == 84 else '复位'} <code>&#36;A_DBB[62]</code> / `DB4900.DBX62.0`（故障信号）"
            elif n == 86 or n == 87:
                note = f"{'置位' if n == 86 else '复位'} <code>&#36;A_DBB[63]</code> / `DB4900.DBX63.0`"
            elif n == 70:
                note = "过渡到进给轴运行，常用于 `PLCASUP2.SPF` C 轴回零前"
            elif n == 19:
                note = "依据设定数据 `SD43240` 执行主轴准停定向"

        m_rows.append((code, scope, desc, note))

    # Parse PLC_NC & Robot & Fast I/O & Probe sections from Parameter_Index.md
    pi_lines = pi_text.splitlines()
    plc_nc_rows = []
    robot_sig_rows = []
    fast_io_rows = []
    probe_sig_rows = []
    cur_sec = None
    for line in pi_lines:
        s = line.strip()
        if s.startswith("|**"):
            cur_sec = re.findall(r"\*\*(.*?)\*\*", s)[0]
            continue
        if not s or s == "#" or s.startswith("|:---") or s == "|变量名|变量含义|备注" or s in ("|", "||", "|||"):
            continue
        parts = [p.strip() for p in s.strip("|").split("|")]
        if cur_sec == "PLC_NC交换变量":
            plc_nc_rows.append((parts[0], parts[1] if len(parts) > 1 else "", parts[2] if len(parts) > 2 else ""))
        elif cur_sec == "与桁架机器人交互相关的信号":
            robot_sig_rows.append((parts[0], parts[1] if len(parts) > 1 else "", parts[2] if len(parts) > 2 else ""))
        elif cur_sec == "快速输入输出信号":
            fast_io_rows.append((parts[0], parts[1] if len(parts) > 1 else "", parts[2] if len(parts) > 2 else ""))
        elif cur_sec == "自动测量信号":
            probe_sig_rows.append((parts[0], parts[1] if len(parts) > 1 else "", parts[2] if len(parts) > 2 else ""))
        elif cur_sec == "修整主参数(DRESSER)":
            break

    out = []
    out.append("# 10.2 全量 M 代码表与 PLC-NC 交互信号")
    out.append("")
    out.append("本节依据上游 `M-sympol_Index.md`、`Parameter_Index.md` 及 `CMA/**/*.SPF` 实际调用源码，完整列出 `M0`～`M99` 全量 M 代码、全部 46 项 PLC-NC 交换字节（<code>&#36;A_DBB</code> ↔ `DB4900`）以及全部 14 项快速 I/O 与测头硬件信号。")
    out.append("")
    out.append("## 1. 全系统 M 代码标准索引表（`M0` ～ `M99`）")
    out.append("")
    out.append("| M 代码 | 分类 / 作用域 | 含义与功能定义 | 关联信号 / 备注 |")
    out.append("| :---: | :--- | :--- | :--- |")
    for code, scope, desc, note in m_rows:
        out.append(f"| `{code}` | {scope} | {desc} | {note} |")

    out.append("")
    out.append("> **源码扩展 M 代码补充**（`M0`～`M99` 之外）：<br>• **`M206`**：外部连续轨迹曲线修整子程序 `D_LINE_TOOL_SHAPE.SPF` 中用于执行带刀补刀具调用（`T=TOOL_NAME D=TOOL_EDGE_INDEX M206`）；<br>• **`M03` / `M04`**：与 `M3` / `M4` 等效的主轴顺/逆时针旋转指令（见于 `E_DOUBLE_ARC_DRESS.SPF` 与 `C_CYCLE_CENTER.SPF`）。")
    out.append("")
    out.append("## 2. 桁架机械手专控握手 M 代码速查（`M80` ～ `M97`）")
    out.append("")
    out.append("当 `HorizonJuicerCreator` 勾选 `机械手 = 1 有`（`;ifIsHasLoadingArm`）并在机床配置开启 `TOOL_SET[16] = 1`（HMI：`TOOL_SET[17]`）时，系统通过以下专控 M 代码向桁架机械手发送到位与状态信号：")
    out.append("")
    out.append("| M 代码 | 置位 / 复位 NC-PLC 位 | 物理定义与机械手含义 |")
    out.append("| :---: | :--- | :--- |")
    out.append("| `M80` / `M81` | <code>&#36;A_DBB[60]</code>（`DB4900.DBX60.0`）= `1` / `0` | 罩壳顶部门已打开（**备妥信号**有效 / 复位） |")
    out.append("| `M82` / `M83` | <code>&#36;A_DBB[61]</code>（`DB4900.DBX61.0`）= `1` / `0` | **预完成**，提前通知机械手准备抓放料 / 复位 |")
    out.append("| `M84` / `M85` | <code>&#36;A_DBB[62]</code>（`DB4900.DBX62.0`）= `1` / `0` | **机床故障**信号有效 / 清除 |")
    out.append("| `M86` / `M87` | <code>&#36;A_DBB[63]</code>（`DB4900.DBX63.0`）= `1` / `0` | **尾架顶尖缩回到位**信号置 `1` / 置 `0` |")
    out.append("| `M88` / `M89` | <code>&#36;A_DBB[64]</code>（`DB4900.DBX64.0`）= `1` / `0` | **尾架顶尖伸出到位**信号置 `1` / 置 `0` |")
    out.append("| `M92` / `M93` | <code>&#36;A_DBB[65]</code>（`DB4900.DBX65.0`）= `1` / `0` | **液压卡盘松开到位**信号置 `1` / 置 `0`（磨削中心复用为外圆量仪气缸伸出/缩回） |")
    out.append("| `M94` / `M95` | <code>&#36;A_DBB[66]</code>（`DB4900.DBX66.0`）= `1` / `0` | **液压卡盘夹紧到位**信号置 `1` / 置 `0`（内螺纹无机械手时复用为头架防护罩壳伸出/缩回） |")
    out.append("| `M96` / `M97` | <code>&#36;A_DBB[67]</code>（`DB4900.DBX67.0`）= `0` / `1` | 机床吹气旋转头架复位（`M96`）/ 有效（`M97`）；子程序 `B_JXS_ZJ.SPF` 实际以 `M96` 发吹气完成信号、`M97` 复位 |")
    out.append("")
    out.append("## 3. PLC-NC 交换变量全量表（<code>&#36;A_DBB</code> ↔ `DB4900`，共 46 项）")
    out.append("")
    out.append("> **Sinumerik ONE 跨平台说明**：当 `HorizonJuicerCreator` 选择 **数控系统 = `2 Sinumerik ONE`** 时，生成器依据 `oneReplace.json` 自动将老式 <code>&#36;A_DBB[...]</code>、`aDbb[...]` 与 `DB2700` 信号替换为 ONE 平台的 <code>&#36;A_IN[...]</code>、`digitInpVal[...]` 与 `DB10.DBX107.0` / `DB10.DBX107.1`，全量映射对照表见 [10.5 条件编译与字符替换标记全表](replace_markers.md)。")
    out.append("")
    out.append("### 3.1 常规机床互锁与状态交换信号（33 项）")
    out.append("")
    out.append("| NC 变量 | PLC 地址 | 功能含义与说明 |")
    out.append("| :--- | :--- | :--- |")
    for v, plc, desc in plc_nc_rows:
        out.append(f"| {fmt_code(v)} | {fmt_code(plc)} | {sanitize_cell(desc)} |")
    out.append("")
    out.append("### 3.2 桁架机器人专控交互信号（13 项）")
    out.append("")
    out.append("> **地址修正说明**：标准西门子 NCK ↔ PLC 交换字节遵循 <code>&#36;A_DBB[n]</code> ↔ `DB4900.DBXn.0` 1:1 映射。上游 `Parameter_Index.md` 原表存在少量复制笔误（将 <code>&#36;A_DBB[34]</code> 误写为 `DB4900.DBX33.0`、将 <code>&#36;A_DBB[65]</code> 误写为 `DB4900.DBX63.0`、将 <code>&#36;A_DBB[66]</code> 与 <code>&#36;A_DBB[67]</code> 误写为 `DB4900.DBX64.0`），下表已按真实字节偏移核正并在备注注明。")
    out.append("")
    out.append("| NC 变量 | PLC 地址（按 1:1 映射核正） | 信号方向与功能含义 |")
    out.append("| :--- | :--- | :--- |")
    plc_fix = {
        "$A_DBB[34]": ("DB4900.DBX34.0", "（原索引笔误写为 DB4900.DBX33.0）"),
        "$A_DBB[65]": ("DB4900.DBX65.0", "（原索引笔误写为 DB4900.DBX63.0）"),
        "$A_DBB[66]": ("DB4900.DBX66.0", "（原索引笔误写为 DB4900.DBX64.0）"),
        "$A_DBB[67]": ("DB4900.DBX67.0", "（原索引笔误写为 DB4900.DBX64.0）"),
    }
    for v, plc, desc in robot_sig_rows:
        real_plc, fix_note = plc_fix.get(v, (plc, ""))
        out.append(f"| {fmt_code(v)} | {fmt_code(real_plc)} | {sanitize_cell(desc)}{fix_note} |")
    out.append("")
    out.append("## 4. 快速 I/O 量仪与自动测量硬件信号（共 14 项）")
    out.append("")
    out.append("| 变量接口 | 分类 | 信号用途与状态定义 |")
    out.append("| :--- | :--- | :--- |")
    for v, d, n in fast_io_rows:
        detail = sanitize_cell(d) + (f"（{sanitize_cell(n)}）" if n else "")
        out.append(f"| {fmt_code(v)} | 快速 I/O | {detail} |")
    for v, d, n in probe_sig_rows:
        detail = sanitize_cell(d) + (f"：{sanitize_cell(n)}" if n else "")
        out.append(f"| {fmt_code(v)} | 自动测量探头 | {detail} |")

    content = "\n".join(out) + "\n"
    return os.path.join(OUT_DIR, "m_codes_and_signals.md"), content, {
        "m_codes": len(m_rows),
        "plc_nc": len(plc_nc_rows) + len(robot_sig_rows),
        "fast_io_probe": len(fast_io_rows) + len(probe_sig_rows),
    }


# ---------------------------------------------------------------------------
# 10.3 config_ui_variables.md
# ---------------------------------------------------------------------------
def load_almc_chs():
    txt = read_text(os.path.join(SRC_LIB, "HMI", "lng", "almc_chs.txt"))
    kv = {}
    for line in txt.splitlines():
        m = re.match(r'^(\d+)\s+0\s+0\s+"(.*)"', line.strip())
        if m:
            kv[m.group(1)] = m.group(2)
    return kv


def format_up6_preset(items):
    if not items:
        return "无（保持持久值）"
    guard_map = {
        "ifIsHasA": "有A轴时",
        "ifIsNotHasA": "无A轴时",
        "ifIsSiFuInGrindWheel": "变频砂轮",
        "ifIsNotSiFuInGrindWheel": "伺服砂轮",
        "ifIsSiFuInExGrindWheel": "变频外磨",
        "ifIsNotSiFuInExGrindWheel": "伺服外磨",
        "ifIsSiFuInDressWheel": "变频修整",
        "ifIsNotSiFuInDressWheel": "伺服修整",
        "ifIsExternal": "外螺纹",
        "ifIsInternal": "内螺纹",
        "ifIsAuto": "有自动对刀",
        "ifIsNotAuto": "无自动对刀",
        "ifIsHasReOperate": "有二次对刀",
        "ifIsNotHasReOperate": "无二次对刀",
        "ifIsHasU": "磨削中心有U轴",
        "ifIsNotHasUBack": "无U轴后置",
        "ifIsNotHasUFront": "无U轴前置",
        "ifIsHasLoadingArm": "有机械手",
        "ifIsCenter": "磨削中心",
        "ifIsProbeFront": "前向测量",
        "ifIsNotProbeFront": "后向测量",
        "ifIsKaiGuanCeLiang": "开关测量",
        "ifIsCeTouCeLiang": "测头测量",
    }
    parts = []
    for val, cmt in items:
        v_clean = "Creator 机床编号 `machineIndex`" if val == "machineIndex" else f"`{val}`"
        guards = re.findall(r"ifIs[A-Za-z0-9_]+", cmt)
        if guards:
            g_str = "+".join(guard_map.get(g, g) for g in guards)
            parts.append(f"{v_clean}（{g_str}）")
        else:
            parts.append(v_clean)
    return "<br>".join(parts)


def build_config_ui_variables():
    kv = load_almc_chs()
    aset = read_text(os.path.join(SRC_LIB, "HMI", "proj", "a_setting.com"))

    up6_block = re.search(r"SUB\(UP6\)(.*?)END_SUB", aset, re.S).group(1)
    up6_defs = {}
    for line in up6_block.splitlines():
        m = re.match(r"\s*([A-Z0-9_]+)\.VAL\s*=\s*([^;]+);?(.*)", line)
        if m:
            up6_defs.setdefault(m.group(1), []).append((m.group(2).strip(), m.group(3).strip()))

    # Also parse SUB(UP1..UP5, UP7..UP9)
    sub_blocks = {}
    for m in re.finditer(r"SUB\((UP\d+)\)(.*?)END_SUB", aset, re.S):
        sub_blocks[m.group(1)] = m.group(2)

    sections = []
    hidden_vars = []
    cur_sec = None
    in_center = False
    in_hidden = False

    def resolve_label(lbl):
        return re.sub(r"\s+", " ", lbl.lstrip("-").strip())

    # Also check README.md for PROCESS[122]
    for line in aset.splitlines():
        s = line.strip()
        if ";ifIsCenterBegin" in s:
            in_center = True
            continue
        if ";ifIsCenterEnd" in s:
            in_center = False
            continue
        if ";****************隐藏设置参数" in s:
            in_hidden = True
            continue
        if s.startswith("DEF MSG_"):
            ids = re.findall(r"\$(\d+)", s)
            sec_title = kv.get(ids[0], s).rstrip(":").strip()
            cur_sec = {"title": sec_title, "rows": []}
            sections.append(cur_sec)
            continue

        m = re.match(r"DEF\s+(\w+)=\((.*?)\);?(.*)", s)
        if not m:
            continue
        vname, body, comment = m.group(1), m.group(2), m.group(3).strip()
        acxm = re.search(r"/NC/_N_NC_GD2_ACX/([A-Z_]+)\[(\d+)\]", body)
        if not acxm:
            continue
        arr, hmi_i = acxm.group(1), int(acxm.group(2))
        nc_var = f"{arr}[{hmi_i - 1}]"
        hmi_var = f"{arr}[{hmi_i}]"
        guards = re.findall(r"ifIs[A-Za-z0-9_]+", comment)
        if in_center and "ifIsCenter" not in guards:
            guards = ["ifIsCenter"] + guards
        guard_str = " ".join(f"`;{g}`" for g in guards) if guards else "通用（无裁剪）"

        opts = []
        optm = re.search(r"/\*([^/]+)/", body)
        if optm:
            for om in re.finditer(r"(-?\d+)=\$(\d+)", optm.group(1)):
                opts.append(f"`{om.group(1)}`={kv.get(om.group(2), om.group(2))}")

        ids = re.findall(r"\$(\d+)", body)
        label = resolve_label(kv.get(ids[-1], "")) if ids else ""
        wr_m = re.search(r"WR(\d)", body)
        wr_s = f"WR{wr_m.group(1)}" if wr_m else ""
        ac_m = re.search(r"ac(\d)", body)
        ac_s = f"ac{ac_m.group(1)}" if ac_m else ""

        if cur_sec is None or in_hidden:
            hidden_vars.append({
                "mask": "Mask0" if cur_sec is None else "Mask1（隐藏区）",
                "vname": vname,
                "nc_var": nc_var,
                "hmi_var": hmi_var,
                "wr": f"{wr_s}/{ac_s}".strip("/"),
                "guards": guard_str,
                "up6": format_up6_preset(up6_defs.get(vname, [])),
                "desc": comment,
            })
        else:
            # Build detail text
            detail_parts = []
            if opts:
                detail_parts.append("选项：" + " / ".join(opts))
            if guard_str != "通用（无裁剪）":
                detail_parts.append("条件编译：" + guard_str)
            # Clean comment description if useful and safe
            clean_cmt = comment
            for g in guards:
                clean_cmt = clean_cmt.replace(f";{g}", "").replace(g, "")
            clean_cmt = clean_cmt.strip(" ;")
            if clean_cmt:
                clean_cmt = sanitize_cell(clean_cmt)
                detail_parts.append("源码备注：" + clean_cmt)
            cur_sec["rows"].append({
                "label": label,
                "vname": vname,
                "nc_var": nc_var,
                "hmi_var": hmi_var,
                "up6": format_up6_preset(up6_defs.get(vname, [])),
                "detail": "<br>".join(detail_parts) if detail_parts else "—",
            })

    # Manual-variable note for PROCESS[122] (from Horizon-Juicer/README.md & A_JXS_MAIN.SPF)
    process122_row = {
        "label": "机械手吹气清洁卡盘检测（后台变量表配置）",
        "vname": "无 HMI 控件",
        "nc_var": "PROCESS[122]",
        "hmi_var": "PROCESS[123]",
        "up6": "未在 `UP6` 覆盖（默认 `0`）",
        "detail": "选项：`0`=不检测 / `1`=检测<br>条件编译：`;ifIsHasLoadingArm`（需在 NC 变量表手动赋值；配合 `R100` 转速与 `R101` 保持时间）",
    }

    # Parse CHANGE(VAR_*) -> SUB(UP*)
    change_triggers = {}
    for cm in re.finditer(r"CHANGE\((\w+)\)\s+call\(\"(\w+)\"\)\s+END_CHANGE", aset, re.S):
        change_triggers[cm.group(2)] = cm.group(1)

    # Map vname -> (label, nc_var)
    vname_info = {}
    for sec in sections:
        for r in sec["rows"]:
            vname_info[r["vname"]] = (r["label"], r["nc_var"], r["hmi_var"])

    up_rows = []
    for up_name in ["UP1", "UP2", "UP3", "UP4", "UP5", "UP6", "UP7", "UP8", "UP9"]:
        if up_name == "UP6":
            up_rows.append((
                "`SUB(UP6)`",
                "`VS3 重置数据` → `Mask2 VS8 确认`",
                "全量初始化所有配置位（含隐藏配置与 `INI[130]` 出厂编号），并依次触发 `UP1`/`UP3`/`UP2`/`UP4`/`UP5`/`UP7`/`UP9`",
                "首次导入程序包或升级 `MGUD.DEF` 后必做",
            ))
            continue
        blk = sub_blocks.get(up_name, "")
        trig = change_triggers.get(up_name, "")
        t_lbl, t_nc, t_hmi = vname_info.get(trig, (trig, trig, trig))
        cond_m = re.search(r"IF\s+([^\n]+)", blk)
        cond = cond_m.group(1).strip() if cond_m else ""
        targets = []
        for tm in re.findall(r"(\w+)\.WR=2", blk):
            if tm in vname_info:
                tl, tnc, thmi = vname_info[tm]
                targets.append(f"`{tm}`（{tl}：`{tnc}` / `{thmi}`）")
            else:
                targets.append(f"`{tm}`")
        # Readable condition
        cond_desc = cond.replace(f"{trig}.VAL==", "值 == ").replace(f"{trig}.VAL<>", "值 != ")
        up_rows.append((
            f"`SUB({up_name})`",
            f"`{trig}`（{t_lbl}：`{t_nc}` / `{t_hmi}`）<br>条件：`{cond_desc}`",
            "<br>".join(targets),
            "条件满足时置 `WR=2`（允许编辑），否则置 `WR=1`（只读灰显）",
        ))

    # Creator JSON mapping (all 31 keys from generatepro.cpp::getJsonValue + creatorwindow.ui)
    creator_rows = [
        ("路径与版本", "软件版本号（内部写入）", "`version`", "如 `V3.29.0`；替换程序 `softwareVersion` 占位符"),
        ("路径与版本", "源仓库目录", "`programDir.sourceDir`", "指向 `Horizon-Juicer` 仓库根目录（需包含 `Source_Library`）"),
        ("路径与版本", "程序生成目录", "`programDir.destDir`", "输出根路径；最终生成 `<destDir>/<machineName>(#<machineIndex>-<customInfo>)`"),
        ("机床信息", "机床型号", "`machineName`", "自动转大写，`×`/`*` → `x`、`/` → `_`；重命名 `INFO_INIT.MPF` 并匹配专属欢迎图"),
        ("机床信息", "机床名称", "`machineNameLng`", "替换 `machineCHS`，写入主程序与 HMI 设备信息文本"),
        ("机床信息", "机床编号", "`machineIndex`", "替换 `machineIndex`（同步写入 `a_setting.com` `INI[130]` / HMI `INI[131]`）与输出目录名"),
        ("机床信息", "用户名称", "`customInfo`", "替换 `customInfo` 与输出目录后缀（支持 UTF-8 转 GBK 文件夹命名）"),
        ("机床信息", "机床语言", "`lng`", "`0` 中文（裁剪 `;ifIsENG`，仅拷贝 `hlp/chs`）/ `1` 多语言（裁剪 `;ifIsCHS`，切换英文面板图）"),
        ("机床配置", "机床类型", "`machineType`", "`0` 外螺纹（拷贝 `SW` 子程序、保留 `;ifIsExternal`）/ `1` 内螺纹（拷贝 `SN` 子程序、保留 `;ifIsInternal`）"),
        ("机床配置", "是否磨丝锥", "`ifHasScrewTap`", "**反向极性**：`0` 是（拷贝 `SCREW_TAP`、保留 `;ifIsScrewTap`）/ `1` 否；仅 `machineType=0` 可见"),
        ("机床配置", "修整器类型", "`wareType`", "`0` VW / `1` V / `2` XZ / `3` X_Back（外磨隐藏）/ `4` 液压 / `5` XW / `6` UW（外磨隐藏）"),
        ("机床配置", "是否磨蜗杆", "`ifHasWorm`", "`0` 否 / `1` 是（拷贝 `Worm` 目录、保留 `;ifIsHasWorm`）；仅外螺纹且插补修整器可选"),
        ("机床配置", "修整轮类型", "`wheelType`", "`0` 单/方滚轮 / `1` 双滚轮；仅 `wareType` 为 `0` / `2` / `5` / `6` 时生效"),
        ("机床配置", "齿形选择", "`shapeType`", "`0` 全套齿形 / `1` 双圆弧；仅 `wareType` 为 `0` / `2` / `5` / `6` 时生效"),
        ("机床配置", "二次对刀", "`ifHasReOp`", "**反向极性**：`0` 有（保留 `;ifIsHasReOperate`，预设 `INI[78]=1`）/ `1` 无；仅外螺纹可见"),
        ("机床配置", "自动对刀", "`ifOperation`", "**反向极性**：`0` 有（拷贝 `auto_operation` 与 `a_auto.com`，预设 `INI[69]=1`）/ `1` 无"),
        ("机床配置", "对刀机构", "`measureMethord`", "`0` 开关（外/内可用）/ `1` 测头（仅内螺纹）/ `2` 开关和测头（仅外螺纹）；仅 `ifOperation=0` 可见"),
        ("机床配置", "测量方向", "`probePos`", "`0` 向前测量（预设 `TOOL_SET[43]=1`）/ `1` 向后测量（预设 `TOOL_SET[43]=-1`）；仅内螺纹且 `ifOperation=0` 可见"),
        ("机床配置", "磨削中心", "`ifCenter`", "**反向极性**：`0` 是（拷贝 `GRIND_CENTER` 与 `a_center*.com`）/ `1` 不是；仅 `machineType=1` 内螺纹可见"),
        ("机床配置", "U 轴", "`ifHasU`", "**反向极性**：`0` 有独立 U 轴（保留 `;ifIsHasU`）/ `1` 无独立 U 轴（共用 X 轴）；仅磨削中心可见"),
        ("机床配置", "外磨位置", "`ifNotHasUExternalPos`", "`0` 后置（保留 `;ifIsNotHasUBack`）/ `1` 前置（保留 `;ifIsNotHasUFront`）；仅磨削中心且 `ifHasU=1` 可见"),
        ("机床配置", "A 轴", "`ifHasA`", "**反向极性**：`0` 有（预设 `INI[16]=1`、`INI[158]=1`，开放螺旋升角与修整 A 角）/ `1` 无"),
        ("机床配置", "砂轮驱动", "`grindWheelType`", "`0` 伺服（预设 `INI[36]=1`）/ `1` 变频器（预设 `INI[36]=0`）"),
        ("机床配置", "外磨砂轮驱动", "`exGrindWheelType`", "`0` 伺服（预设 `INI[91]=1`）/ `1` 变频器（预设 `INI[91]=0`）；仅磨削中心可见"),
        ("机床配置", "修整轮驱动", "`dressWheelType`", "`0` 伺服（预设 `INI[37]=1`）/ `1` 变频器（预设 `INI[37]=0`）"),
        ("其他设置", "删除注释", "`ifRemoveComments`", "**反向极性**：`0` 是（剥离 `.com`/`.spf`/`.mpf` 普通注释）/ `1` 否（保留全部注释）"),
        ("其他设置", "界面模式", "`hmiMode`", "`0` 标准（保留图标路径与 `,pa0`/`,ac` 属性）/ `1` 兼容（剥离图片与修饰属性）"),
        ("其他设置", "数控系统", "`systemMode`", "`0` 老版 828D（`siemens` + `ico800`）/ `1` 新版 828D（`oem` + `ico1024`）/ `2` Sinumerik ONE（`oem` + `ico1024` + `oneReplace.json`）"),
        ("其他设置", "机械手", "`ifHasLoadingArm`", "`0` 无 / `1` 有（拷贝 `JiXieShouRelative` 并保留 `M80`～`M97` 与 `;ifIsHasLoadingArm`）"),
        ("其他设置", "后期加密程序", "`ifHasEncryption`", "`0` 否 / `1` 是（保留 `;ifIsHasEncryption` CF 卡硬件序列号授权校验）"),
        ("其他设置", "删除厂商标识图", "`ifHasNoneTradeMark`", "`0` 否 / `1` 是（改用 `Repository/0_NoneTradeMark` 无品牌底图）"),
    ]

    out = []
    out.append("# 10.3 全量配置界面对应变量表")
    out.append("")
    out.append("本节对照 `Source_Library/HMI/proj/a_setting.com`、`almc_chs.txt`、`Horizon-Juicer/README.md` 与 `HorizonJuicerCreator` 源码（`creatorwindow.ui`、`generatepro.cpp`），提供 **机床端配置界面（`a_setting.com`）** 与 **PC 端生成软件（`HorizonJuicerCreator`）** 的全量变量映射与重置预设清单。")
    out.append("")
    out.append("> **索引基准换算铁律**：<br>• `NC 变量` 列为 `.SPF` 与 `MGUD.DEF` 使用的 **0-based** 数组下标（如 `INI[36]`）；<br>• `HMI 引用` 列为 `a_setting.com` 绑定的 `/NC/_N_NC_GD2_ACX/...` **1-based** 下标（**HMI 下标 = NC 下标 + 1**，如 `INI[37]`）；<br>• 新机首次导入程序包或重新激活 `MGUD.DEF` 后，必须进入 `CUSTOM → 扩展菜单 → 机床配置` 解锁并点击 **`VS3 重置数据 → Mask2 VS8 确认`** 执行 `SUB(UP6)`，将全部出厂预设写入 NC 全局变量。")
    out.append("")
    out.append("## 1. 机床端 `a_setting.com`（`Mask1`）全量可见配置变量表")
    out.append("")

    total_visible = 0
    for idx, sec in enumerate(sections, 1):
        sec_title_note = f"{len(sec['rows'])} 项 HMI 开关 + 1 项后台变量" if idx == 5 else f"{len(sec['rows'])} 项"
        out.append(f"### 1.{idx} {sec['title']}（{sec_title_note}）")
        out.append("")
        out.append("| HMI 配置项（控件名） | NC 变量（0-based） | HMI 引用（1-based） | 重置预设（`UP6`） | 可选值、条件裁剪与说明 |")
        out.append("| :--- | :--- | :--- | :--- | :--- |")
        for r in sec["rows"]:
            total_visible += 1
            out.append(
                f"| **{r['label']}**（`{r['vname']}`） | `{r['nc_var']}` | `{r['hmi_var']}` | {r['up6']} | {r['detail']} |"
            )
        if idx == 5:
            out.append(
                f"| **{process122_row['label']}**（{process122_row['vname']}） | `{process122_row['nc_var']}` | `{process122_row['hmi_var']}` | {process122_row['up6']} | {process122_row['detail']} |"
            )
        out.append("")

    out.append("## 2. 配置界面后台隐藏与系统持久化变量（`Mask0` + `Mask1` 隐藏区，共 9 项）")
    out.append("")
    out.append("以下变量不直接在 `Mask1` 可视区域显示，但由 `a_setting.com` 在口令挑战滚动或 `SUB(UP6)` 重置时读写（按生成选配决定是否保留隐藏初始化分支）：")
    out.append("")
    out.append("| 画面 / 控件名 | NC 变量（0-based） | HMI 引用（1-based） | 属性 / 条件裁剪 | 重置预设（`UP6`）与用途说明 |")
    out.append("| :--- | :--- | :--- | :--- | :--- |")
    for hv in hidden_vars:
        raw_desc = hv["desc"]
        for g in re.findall(r"ifIs[A-Za-z0-9_]+", raw_desc):
            raw_desc = raw_desc.replace(f";{g}", "").replace(g, "")
        desc_s = sanitize_cell(raw_desc.strip(" ;")) if raw_desc.strip(" ;") else "—"
        if hv["vname"] == "SEED_VAR":
            desc_s = "口令验证页（`Mask0`）SRAM 持久化挑战码种子变量（不设默认值 0 防止覆盖清零）"
        out.append(
            f"| {hv['mask']} `{hv['vname']}` | `{hv['nc_var']}` | `{hv['hmi_var']}` | {hv['wr']} / {hv['guards']} | 预设：{hv['up6']}<br>{desc_s} |"
        )

    out.append("")
    out.append("## 3. `a_setting.com` 动态读写联动子程序表（`SUB(UP1)` ～ `SUB(UP9)`）")
    out.append("")
    out.append("在 `Mask1` 修改父开关参数时，EasyScreen 的 `CHANGE(...)` 事件与 `SUB(UP6)` 重置结束阶段会调用下列子程序动态切换从属输入框的读写权限（`WR=2` 可读写 / `WR=1` 只读锁定）：")
    out.append("")
    out.append("| 子程序 | 触发源控件与激活条件 | 受控目标控件（`WR=2` 解锁项） | 联动逻辑说明 |")
    out.append("| :--- | :--- | :--- | :--- |")
    for upn, trig, targs, note in up_rows:
        out.append(f"| {upn} | {trig} | {targs} | {note} |")

    out.append("")
    out.append("## 4. PC 端 `HorizonJuicerCreator` 配置界面与 JSON 字段全量对照（共 31 项）")
    out.append("")
    out.append("下表列出 `HorizonJuicerCreator` 写入 `~/HorizonJuicerCreator.json` 并由 `GeneratePro::getJsonValue()` 读取的全部 31 个配置键。请特别注意标注为 **反向极性** 的开关（`0` 代表启用/有/是）：")
    out.append("")
    out.append("| 配置分组 | 界面字段名称 | JSON 键名 | 枚举值、极性与代码生成作用 |")
    out.append("| :--- | :--- | :--- | :--- |")
    for grp, lbl, jkey, desc in creator_rows:
        out.append(f"| {grp} | **{lbl}** | {jkey} | {desc} |")

    content = "\n".join(out) + "\n"
    return os.path.join(OUT_DIR, "config_ui_variables.md"), content, {
        "visible_setting": total_visible,
        "hidden_setting": len(hidden_vars),
        "creator_json": len(creator_rows),
    }


# ---------------------------------------------------------------------------
# 10.4 full_variable_index.md
# ---------------------------------------------------------------------------
def build_full_variable_index():
    mgud_text = read_text(os.path.join(SRC_LIB, "DEF", "MGUD.DEF"))
    pi_text = read_text(os.path.join(SRC_LIB, "Parameter_Index.md"))

    # 1. Parse MGUD.DEF (60 declarations)
    mgud_rows = []
    cur_cmt = ""
    for line in mgud_text.splitlines():
        s = line.strip()
        if not s or s == "M30" or s.startswith(";*"):
            continue
        if s.startswith(";"):
            cur_cmt = s.lstrip(";").strip()
            continue
        m = re.match(r"DEF\s+NCK\s+(STRING\[\d+\]|REAL|INT)\s+([A-Z0-9_]+(?:\[\d+\])?)\s*(?:;(.*))?$", s)
        if m:
            dtype, sym, inline_cmt = m.group(1), m.group(2), (m.group(3) or "").strip()
            # Determine storage & index rule
            am = re.match(r"^([A-Z0-9_]+)\[(\d+)\]$", sym)
            if am:
                arr_name, arr_len = am.group(1), int(am.group(2))
                # Check if 1-based in NC code or 0-based
                if arr_name.startswith("COMMON_") and arr_name not in ("COMMON_STATUS_CACU", "COMMON_LENGTH_ADD"):
                    idx_rule = f"NC `{arr_name}[1]`～`{arr_name}[{arr_len}]`<br>HMI `{arr_name}[1]`～`{arr_name}[{arr_len}]`"
                elif arr_name in ("COMMON_STATUS_CACU", "COMMON_LENGTH_ADD"):
                    idx_rule = f"NC `{arr_name}[0]`～`{arr_name}[10]`<br>HMI `{arr_name}[1]`～`{arr_name}[11]`"
                else:
                    idx_rule = f"NC `{arr_name}[0]`～`{arr_name}[{arr_len - 1}]`<br>HMI `{arr_name}[1]`～`{arr_name}[{arr_len}]`"
            else:
                idx_rule = "标量（无下标）"
            desc = inline_cmt if inline_cmt else cur_cmt
            if not desc:
                desc = "全局变量"
            mgud_rows.append((sym, dtype, idx_rule, sanitize_cell(desc)))

    # Refine MGUD descriptions where inline comments in MGUD.DEF are shared/terse
    mgud_desc_overrides = {
        "CUR_WHEEL": "当前砂轮更换记录序号（`1～99` 索引 `WHEEL_GRIND_CUMU` 与 `WHEEL_CHANGED_DATA`）",
        "WHEEL_GRIND_CUMU[100]": "99 组更换砂轮周期对应的工件加工产量累计数组",
        "WHEEL_CHANGED_DATA[100]": "99 组更换砂轮操作的时间戳记录数组",
        "DRESS_WHEEL_NUM[100]": "100 组金刚石滚轮编号档案数组",
        "DRESS_WHEEL_DATE[100]": "100 组金刚石滚轮上线启用日期档案数组",
        "CHOICE": "参数备份恢复运行模式（`0` 加工 / `1` 备份 / `2` 恢复）",
        "BACKUP_TYPE": "备份模式（`0` 备份全部 MGUD 变量 / `1` 按自定义列表备份）",
        "BACKUP_POS": "备份目标存储位置（`0` 内置 / `1` 后 USB / `2` 前 USB / `3` CF 卡）",
        "RESTORE_POS": "恢复源存储位置（`0` 内置 / `1` 后 USB / `2` 前 USB / `3` CF 卡）",
        "FILE_LINE_COUNT": "自定义参数列表文件的总行数（含空行与分号注释行）",
        "BR_MSG": "备份/恢复执行状态与多语言提示消息",
        "WORM_SHAPE": "蜗杆专用齿形子程序名称",
        "AXIS_EW": "磨削中心外圆砂轮切入轴名（有 U 轴时为 `U`，共用轴时为 `X`）",
        "PARA_LOCK_SWITCH[30]": "界面参数锁定开关状态预留数组",
    }

    # 2. Parse Parameter_Index.md into sections & subtables
    pi_sections = []
    cur_sec = None
    cur_sub = None
    for line in pi_text.splitlines():
        s = line.strip()
        if not s or s == "#" or s.startswith("|:---") or s == "|变量名|变量含义|备注" or s in ("|", "||", "|||"):
            continue
        hm = re.match(r"^\|\*\*(.+?)\*\*\|?$", s)
        if hm:
            cur_sec = {
                "title": hm.group(1).strip(),
                "groups": [{"subtitle": None, "rows": []}],
            }
            pi_sections.append(cur_sec)
            cur_sub = cur_sec["groups"][0]
            continue
        parts = [p.strip() for p in s.strip("|").split("|")]
        v = parts[0] if len(parts) > 0 else ""
        d = parts[1] if len(parts) > 1 else ""
        n = parts[2] if len(parts) > 2 else ""
        if cur_sec is None:
            continue
        if v in ("磨削中心相关", "修整参数", "不需要修改的参数", "双圆弧", "梯形", "三角") and not d and not n:
            cur_sub = {"subtitle": v, "rows": []}
            cur_sec["groups"].append(cur_sub)
            continue
        cur_sub["rows"].append((v, d, n))

    # Fix known upstream DB4900 copy-paste typos in 与桁架机器人交互相关的信号
    plc_fix = {
        "$A_DBB[34]": ("DB4900.DBX34.0", "（原索引笔误写为 DB4900.DBX33.0）"),
        "$A_DBB[65]": ("DB4900.DBX65.0", "（原索引笔误写为 DB4900.DBX63.0）"),
        "$A_DBB[66]": ("DB4900.DBX66.0", "（原索引笔误写为 DB4900.DBX64.0）"),
        "$A_DBB[67]": ("DB4900.DBX67.0", "（原索引笔误写为 DB4900.DBX64.0）"),
    }

    # Categories by schema type
    sig_titles = {"PLC_NC交换变量", "与桁架机器人交互相关的信号", "快速输入输出信号", "自动测量信号"}
    r_titles = {"R参数使用情况", "内螺纹反相孔倒角参数", "内螺纹夹具自磨R参数版程序参数", "蜗杆用R参数"}

    # Build anchor slugs & TOC
    toc_links = []
    sec_anchors = []
    for idx, sec in enumerate(pi_sections, 1):
        anchor = f"pi-sec-{idx}"
        row_total = sum(len(g["rows"]) for g in sec["groups"])
        sec_anchors.append((anchor, row_total))
        toc_links.append(f"[{sec['title']}（{row_total} 项）](#{anchor})")

    pi_total_items = sum(rt for _, rt in sec_anchors)
    out = []
    out.append("# 10.4 全量全局变量与 R 参数索引表")
    out.append("")
    out.append(f"本节汇集 `MGUD.DEF` 全部 60 条自定义全局变量声明、`Parameter_Index.md` 全部 30 个分类共 {pi_total_items:,} 条变量明细（对应 `Parameter_Index.md` 全部 1,561 个非空表格行中的 8 个子分组标题与 {pi_total_items:,} 个独立条目），以及 `Parameter_Index.md` 未展开的 22 项系统/备份统计变量。")
    out.append("")
    out.append("> **0-based（NC）与 1-based（HMI ACX）下标偏移铁律**：<br>• `.SPF` / `.MPF` 子程序、`MGUD.DEF` 与 `Parameter_Index.md` 使用 **0-based** 下标（例如 `DRESSER[0]`、`INI[36]`）；<br>• EasyScreen `.com` 界面脚本（`/NC/_N_NC_GD2_ACX/...`）使用 **1-based** 下标（**HMI 下标 = NC 下标 + 1**，例如 `DRESSER[1]`、`INI[37]`）；<br>• `MGUD.DEF` 自定义变量名超过 60 个，激活前必须确保通用机床数据 **`MD18120 >= 70`**。若将早期 `TECHNOLOGY[420]` 控制器升级至 `TECHNOLOGY[500]` 新版 `MGUD.DEF`，激活前务必先备份原 GUD 数据，激活后执行 `VS3 重置数据` 并恢复业务参数。")
    out.append("")
    out.append("### 快速分类导航目录")
    out.append("")
    out.append("- [1. `MGUD.DEF` 全局变量声明总表（60 项）](#mgud-def-list)")
    out.append(f"- **2. `Parameter_Index.md` 全量明细（30 类 / {pi_total_items:,} 项）**：" + " · ".join(toc_links))
    out.append("- [3. `MGUD.DEF` 补充系统与备份变量表（22 项）](#mgud-extra-vars)")
    out.append("")
    out.append('<a id="mgud-def-list"></a>')
    out.append("")
    out.append("## 1. `MGUD.DEF` 全局变量声明全量清单（60 项）")
    out.append("")
    out.append("| 变量 / 数组声明 | 数据类型 | 存储与下标基准 | 用途说明 |")
    out.append("| :--- | :--- | :--- | :--- |")
    for sym, dtype, idx_rule, desc in mgud_rows:
        final_desc = mgud_desc_overrides.get(sym, desc)
        out.append(f"| `{sym}` | `{dtype}` | {idx_rule} | {final_desc} |")

    out.append("")
    out.append(f"## 2. `Parameter_Index.md` 全量变量明细表（30 类 / {pi_total_items:,} 项）")
    out.append("")

    total_pi_rows = 0
    for idx, sec in enumerate(pi_sections, 1):
        title = sec["title"]
        anchor, row_total = sec_anchors[idx - 1]
        out.append(f'<a id="{anchor}"></a>')
        out.append("")
        out.append(f"### 2.{idx} {title}（{row_total} 项）")
        out.append("")

        for grp in sec["groups"]:
            if not grp["rows"]:
                continue
            if grp["subtitle"]:
                out.append(f"#### {grp['subtitle']}")
                out.append("")

            if title in sig_titles:
                out.append("| NC 信号变量 | PLC 地址 / 通道映射 | 含义与备注 |")
                out.append("| :--- | :--- | :--- |")
                for v, d, n in grp["rows"]:
                    total_pi_rows += 1
                    if title == "PLC_NC交换变量":
                        plc_s = fmt_code(d)
                        meaning_s = sanitize_cell(n) if n else "预留 / 暂未使用"
                    elif title == "与桁架机器人交互相关的信号":
                        real_plc, fix_note = plc_fix.get(v, (d, ""))
                        plc_s = fmt_code(real_plc)
                        meaning_s = sanitize_cell(n) + fix_note
                    else:
                        plc_s = "快速 I/O / 测头硬件接口"
                        meaning_s = sanitize_cell(d) + (f"（{sanitize_cell(n)}）" if n else "")
                    out.append(f"| {fmt_code(v)} | {plc_s} | {meaning_s} |")
            elif title in r_titles:
                out.append("| `R` 参数 | 变量含义 | 备注 |")
                out.append("| :--- | :--- | :--- |")
                for v, d, n in grp["rows"]:
                    total_pi_rows += 1
                    desc_s = sanitize_cell(d) if d else "预留 / 暂未使用"
                    note_s = sanitize_cell(n) if n else "—"
                    out.append(f"| `{v}` | {desc_s} | {note_s} |")
            else:
                out.append("| NC 变量（0-based） | HMI 引用（1-based） | 变量含义 | 备注 |")
                out.append("| :--- | :--- | :--- | :--- |")
                for v, d, n in grp["rows"]:
                    total_pi_rows += 1
                    # Note: COMMON_* arrays COMMON_LENGTH..COMMON_POINT_REF_HORI are 1-based in MGUD [1..10], keep HMI identical or mark
                    if re.match(r"^COMMON_(?:LENGTH|ANG|RND|POINT_REF_VER|POINT_REF_HORI)\[\d+\]$", v):
                        hmi_v = v
                        extra_n = "通用齿形 `1～10` 段同下标引用"
                        note_s = sanitize_cell(n) + (f"；{extra_n}" if n else extra_n)
                    else:
                        hmi_v = make_hmi_var(v)
                        note_s = sanitize_cell(n) if n else "—"
                    desc_s = sanitize_cell(d) if d else "预留 / 暂未使用"
                    out.append(f"| `{v}` | `{hmi_v}` | {desc_s} | {note_s} |")
            out.append("")

    # 3. Supplementary 22 MGUD symbols not listed in Parameter_Index.md
    extra_vars = [
        ("AXIS_EW", "AXIS_EW", "STRING[1]", "磨削中心外圆砂轮切入轴名称（有 U 轴时为 `U`，共用轴时为 `X`，见 `C_PAR_INI.SPF` / `A_GRIND_CENTER.SPF`）"),
        ("WORM_SHAPE", "WORM_SHAPE", "STRING[20]", "蜗杆专用齿形子程序名（初始化时写入 `SHAPE`）"),
        ("INI[257]", "INI[258]", "REAL", "`a_setting.com` `Mask0` SRAM 持久化随机挑战码种子变量（仅底层安全验证滚动更新）"),
        ("TRI[0]～TRI[19]", "TRI[1]～TRI[20]", "REAL[20]", "三角齿形历史兼容参数数组（已逐步迁移至 `SHAPE_MODEL`，保留于整机备份表）"),
        ("TRAP[0]～TRAP[19]", "TRAP[1]～TRAP[20]", "REAL[20]", "梯形齿形历史兼容参数数组（已逐步迁移至 `SHAPE_MODEL`，保留于整机备份表）"),
        ("DARC[0]～DARC[29]", "DARC[1]～DARC[30]", "REAL[30]", "双圆弧齿形历史兼容参数数组（已逐步迁移至 `SHAPE_MODEL`，保留于整机备份表）"),
        ("PARA_LOCK_SWITCH[0]～PARA_LOCK_SWITCH[29]", "PARA_LOCK_SWITCH[1]～PARA_LOCK_SWITCH[30]", "INT[30]", "HMI 界面参数读写锁定开关预留数组（纳入 `D_BACKUP_ALL_PARA.SPF` 备份）"),
        ("CHOICE", "CHOICE", "REAL", "`a_backup_restore.com` 运行模式选择（`0` 正常加工 / `1` 备份数据 / `2` 恢复数据）"),
        ("BACKUP_TYPE", "BACKUP_TYPE", "REAL", "备份范围模式（`0` 全量备份 MGUD / `1` 按自定义清单文件备份）"),
        ("BACKUP_POS", "BACKUP_POS", "REAL", "备份目标介质位置（`0` 内置 / `1` 后 USB（不可写）/ `2` 前 USB / `3` CF 卡）"),
        ("RESTORE_POS", "RESTORE_POS", "REAL", "恢复源介质位置（`0` 内置 / `1` 后 USB / `2` 前 USB / `3` CF 卡）"),
        ("FILE_LINE_COUNT", "FILE_LINE_COUNT", "REAL", "自定义变量列表文件的总行数（含空行与 `;` 注释行）"),
        ("LIST_NAME", "LIST_NAME", "STRING[30]", "自定义备份参数列表文件名（默认 `.TXT` 文档，不含扩展名）"),
        ("LIST_DIR", "LIST_DIR", "STRING[30]", "自定义备份参数列表所在文件夹名（位于 `_N_SPF_DIR` 内）"),
        ("BACKUP_NAME", "BACKUP_NAME", "STRING[30]", "生成的备份数据文件名"),
        ("BACKUP_DIR", "BACKUP_DIR", "STRING[30]", "生成的备份目标文件夹名"),
        ("RESTORE_NAME", "RESTORE_NAME", "STRING[30]", "待恢复的数据文件名"),
        ("RESTORE_DIR", "RESTORE_DIR", "STRING[30]", "待恢复的数据源文件夹名"),
        ("BR_MSG", "BR_MSG", "STRING[150]", "`a_backup_restore.com` 备份/恢复执行状态与多语言提示消息"),
        ("CUR_WHEEL", "CUR_WHEEL", "INT", "当前砂轮更换记录序号（换轮后在 `B_DRESS.SPF` 中自增，范围 `1～99`）"),
        ("WHEEL_GRIND_CUMU[0]～WHEEL_GRIND_CUMU[99]", "WHEEL_GRIND_CUMU[1]～WHEEL_GRIND_CUMU[100]", "INT[100]", "各期砂轮累计磨削工件计数台账（新轮切换时 `WHEEL_GRIND_CUMU[CUR_WHEEL]=0`）"),
        ("WHEEL_CHANGED_DATA[0]～WHEEL_CHANGED_DATA[99]", "WHEEL_CHANGED_DATA[1]～WHEEL_CHANGED_DATA[100]", "STRING[30][100]", "各期砂轮更换日期时间戳台账（格式 `YYYY-MM-DD HH:MM`）"),
    ]

    out.append('<a id="mgud-extra-vars"></a>')
    out.append("")
    out.append("## 3. `MGUD.DEF` 补充系统与备份变量表（22 项）")
    out.append("")
    out.append("以下 22 项变量在 `MGUD.DEF` 中声明且被 `a_setting.com`、`a_backup_restore.com`、`a_stats.com`、`B_DRESS.SPF` 或 `D_BACKUP_ALL_PARA.SPF` 实际读写，但未在 `Parameter_Index.md` 中单独列出：")
    out.append("")
    out.append("| NC 变量 / 范围（0-based） | HMI 引用 / 范围（1-based） | 类型 | 功能含义与来源 |")
    out.append("| :--- | :--- | :--- | :--- |")
    for nc_v, hmi_v, dtype, desc in extra_vars:
        out.append(f"| `{nc_v}` | `{hmi_v}` | `{dtype}` | {desc} |")

    content = "\n".join(out) + "\n"
    return os.path.join(OUT_DIR, "full_variable_index.md"), content, {
        "mgud_decls": len(mgud_rows),
        "pi_categories": len(pi_sections),
        "pi_rows": total_pi_rows,
        "extra_vars": len(extra_vars),
    }


# ---------------------------------------------------------------------------
# 10.5 replace_markers.md
# ---------------------------------------------------------------------------
def build_replace_markers():
    rm_text = read_text(os.path.join(SRC_LIB, "ReplaceMarker.md"))
    one_json = json.loads(read_text(os.path.join(CREATOR_ROOT, "oneReplace.json")))

    # Parse ReplaceMarker.md (66 markers)
    rm_list = []
    for line in rm_text.splitlines():
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) == 2 and parts[1].startswith("ifIs"):
            rm_list.append((parts[1], parts[0]))

    # Exact retention condition & scope verified from generatepro.cpp
    marker_meta = {
        "ifIsCHS": ("语言与平台", "`lng == 0`（中文）", "`CMA`、`.MPF` 源码"),
        "ifIsENG": ("语言与平台", "`lng == 1`（多语言）", "`CMA`、`.MPF` 源码"),
        "ifIsOneSystem": ("语言与平台", "`systemMode == 1`（新版 828D）或 `systemMode == 2`（Sinumerik ONE）", "`HMI/lng`、`CMA`"),
        "ifIsNotOneSystem": ("语言与平台", "`systemMode == 0`（老版 828D）", "`HMI/lng`、`CMA`"),

        "ifIsHasEncryption": ("授权与机械手", "`ifHasEncryption == 1`（启用后期加密）", "`CMA`（校验序列号授权）"),
        "ifIsNotHasEncryption": ("授权与机械手", "`ifHasEncryption == 0`（无加密）", "`CMA`"),
        "ifIsHasLoadingArm": ("授权与机械手", "`ifHasLoadingArm == 1`（有机械手）", "`MPF`、`CMA`、`HMI/proj`"),
        "ifIsNotHasLoadingArm": ("授权与机械手", "`ifHasLoadingArm == 0`（无机械手）", "`MPF`、`CMA`、`HMI/proj`"),

        "ifIsExternal": ("机型与复合功能", "`machineType == 0`（外螺纹）", "`CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp`"),
        "ifIsInternal": ("机型与复合功能", "`machineType == 1`（内螺纹）", "`CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp`"),
        "ifIsHasWorm": ("机型与复合功能", "`machineType == 0` 且 `wareType in {0,2}` 且 `ifHasWorm == 1`", "`CMA`、`HMI/proj`"),
        "ifIsNotHasWorm": ("机型与复合功能", "除 `ifIsHasWorm` 成立外的所有配置（注意：`wareType!=0 && !=2` 或 `machineType==1` 时源码未删此反转块，主要与 `ifIsHasWorm` 成对在插补外磨下使用）", "`CMA`、`HMI/proj`"),
        "ifIsScrewTap": ("机型与复合功能", "`machineType == 0` 且 `ifHasScrewTap == 0`（外螺纹丝锥）", "`MPF`、`CMA`、`HMI/proj`、`HMI/hlp`"),
        "ifIsNotScrewTap": ("机型与复合功能", "`machineType == 1` 或 `ifHasScrewTap == 1`（非丝锥）", "`MPF`、`CMA`、`HMI/proj`、`HMI/hlp`"),
        "ifIsCenter": ("机型与复合功能", "`machineType == 1` 且 `ifCenter == 0`（内螺纹磨削中心）", "`CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp`"),
        "ifIsNotCenter": ("机型与复合功能", "`machineType == 0` 或 `ifCenter == 1`（非磨削中心）", "`CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp`"),
        "ifIsInternalOnly": ("机型与复合功能", "`machineType == 1` 且 `ifCenter == 1`（纯内螺纹非磨削中心）", "`HMI/proj`（`a_setting` 等）"),

        "ifIsHasU": ("磨削中心 U 轴与外圆", "`machineType == 1` 且 `ifCenter == 0` 且 `ifHasU == 0`（有 U 轴）", "`CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp`"),
        "ifIsNotHasU": ("磨削中心 U 轴与外圆", "`machineType == 1` 且 `ifCenter == 0` 且 `ifHasU == 1`；或 `machineType == 0`（注意 `ifCenter==1` 时源码亦会删除 `ifIsNotHasU` 中的 `proj/lng/hlp`）", "`CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp`"),
        "ifIsNotHasUBack": ("磨削中心 U 轴与外圆", "内螺纹磨削中心、`ifHasU == 1`（无 U 轴）且 `ifNotHasUExternalPos == 0`（外磨后置）", "`CMA`、`HMI/proj`、`HMI/hlp`"),
        "ifIsNotHasUFront": ("磨削中心 U 轴与外圆", "内螺纹磨削中心、`ifHasU == 1`（无 U 轴）且 `ifNotHasUExternalPos == 1`（外磨前置）", "`CMA`、`HMI/proj`、`HMI/hlp`"),

        "ifIsHasReOperate": ("对刀与测量硬件", "`machineType == 0` 且 `ifHasReOp == 0`（外螺纹有二次对刀）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsNotHasReOperate": ("对刀与测量硬件", "`machineType == 1` 或 `ifHasReOp == 1`（无二次对刀）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsAuto": ("对刀与测量硬件", "`ifOperation == 0`（有自动对刀）", "`CMA`、`HMI/proj`、`HMI/hlp`"),
        "ifIsNotAuto": ("对刀与测量硬件", "`ifOperation == 1`（无自动对刀）", "`CMA`、`HMI/proj`、`HMI/hlp`"),
        "ifIsKaiGuanCeLiang": ("对刀与测量硬件", "`ifOperation == 0` 且 `measureMethord == 0`（仅开关测量）", "`CMA`、`HMI/proj`、`HMI/hlp`"),
        "ifIsCeTouCeLiang": ("对刀与测量硬件", "`ifOperation == 0` 且 `measureMethord == 1`（仅测头测量）", "`CMA`、`HMI/proj`、`HMI/hlp`"),
        "ifIsKaiGuanAndCeTouCeLiang": ("对刀与测量硬件", "`ifOperation == 0` 且 `measureMethord == 2`（开关和测头同时配置）", "`CMA`、`HMI/proj`、`HMI/hlp`"),
        "ifIsProbeFront": ("对刀与测量硬件", "`machineType == 1` 且 `ifOperation == 0` 且 `probePos == 0`（内螺纹自动对刀向前测量）", "`a_setting.com` 专属初始赋值预设"),
        "ifIsNotProbeFront": ("对刀与测量硬件", "`machineType == 1` 且 `ifOperation == 0` 且 `probePos == 1`（内螺纹自动对刀向后测量）", "`a_setting.com` 专属初始赋值预设"),

        "ifIsXW": ("修整器构型组合", "`wareType == 5`（XW 修整器）", "`MPF`、`CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp`"),
        "ifIsNotXW": ("修整器构型组合", "`wareType != 5`（非 XW 修整器）", "`MPF`、`CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp`"),
        "ifIsUW": ("修整器构型组合", "`wareType == 6`（UW 修整器，仅内螺纹）", "`MPF`、`CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp`"),
        "ifIsNotUW": ("修整器构型组合", "`wareType != 6`（非 UW 修整器）", "`MPF`、`CMA`、`HMI/proj`、`HMI/lng`、`HMI/hlp`"),
        "ifIsDressWare1": ("修整器构型组合", "`wareType in {0, 2, 5, 6}`（VW、XZ、XW、UW 两轴插补系）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsDressWare2": ("修整器构型组合", "`wareType == 1`（V 单轴成型）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsDressWare3": ("修整器构型组合", "`wareType == 2` 或 `wareType == 5`（XZ / XW）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsDressWare4": ("修整器构型组合", "`wareType == 3`（X_Back 内后置成型）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsDressWare5": ("修整器构型组合", "`wareType == 4`（液压摆缸成型）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsExternalVW": ("修整器构型组合", "（`machineType == 0` 且 `wareType in {0, 1}`）或（`machineType == 1` 且 `wareType == 6`）", "`CMA`、`HMI/hlp`（独立 V/W 或 U/W 轴控制段）"),
        "ifIsFrontDress": ("修整器构型组合", "`wareType != 3`（非 X_Back 后置修整的常规前向修整）", "`CMA`、`HMI/proj`、`HMI/hlp`"),
        "ifIsBackDress": ("修整器构型组合", "`wareType == 3`（X_Back 后置修整）", "`CMA`、`HMI/proj`、`HMI/hlp`"),
        "ifIsVW": ("修整器构型组合", "`wareType in {0, 2, 3, 4, 5, 6}`（即非纯 `V` 成型）；当 `wareType == 1` 时删除", "`CMA`、`HMI/proj`、`HMI/hlp`"),
        "ifIsVWSR": ("修整器构型组合", "`wareType == 0` 且 `wheelType == 0`（VW 单/方滚轮）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsVWSide": ("修整器构型组合", "`wareType == 0` 且 `wheelType == 1`（VW 双滚轮）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsV": ("修整器构型组合", "`wareType == 1`（V 单轴修整器）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsXZSR": ("修整器构型组合", "`wareType in {2, 5, 6}` 且 `wheelType == 0`（XZ/XW/UW 单/方滚轮）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsXZSide": ("修整器构型组合", "`wareType in {2, 5, 6}` 且 `wheelType == 1`（XZ/XW/UW 双滚轮）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsXWai": ("修整器构型组合", "`machineType == 0` 且 `wareType in {2, 5}`（外螺纹 X 轴向修整）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsXNeiFront": ("修整器构型组合", "`machineType == 1` 且 `wareType in {2, 5, 6}`（内螺纹前向修整）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsXNeiBack": ("修整器构型组合", "`wareType == 3`（内螺纹 X_Back 向后修整）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsVH": ("修整器构型组合", "`wareType == 4`（液压修整器）", "`HMI/proj`、`HMI/hlp`"),

        "ifIsSingleAndRound": ("滚轮与齿形细分", "`wareType in {0, 2, 5, 6}` 且 `wheelType == 0`（单/方滚轮）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsSide": ("滚轮与齿形细分", "`wareType in {0, 2, 5, 6}` 且 `wheelType == 1`（双滚轮）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsAllShape": ("滚轮与齿形细分", "`wareType in {0, 2, 5, 6}` 且 `shapeType == 0`（全套齿形）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsArc": ("滚轮与齿形细分", "`wareType in {0, 2, 5, 6}` 且 `shapeType in {0, 1}`（含双圆弧）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsOnlyArc": ("滚轮与齿形细分", "`wareType in {0, 2, 5, 6}` 且 `shapeType == 1`（仅双圆弧）", "`HMI/proj`、`HMI/hlp`"),
        "ifIsHasOtherCommonShape": ("滚轮与齿形细分", "`wareType in {0, 2, 5, 6}` 且 `shapeType == 0`（含通用扩展齿形）", "`HMI/proj`、`HMI/hlp`"),

        "ifIsHasA": ("A 轴与电主轴驱动", "`ifHasA == 0`（有机床 A 轴）", "`a_setting.com`（可见开关与预设）"),
        "ifIsNotHasA": ("A 轴与电主轴驱动", "`ifHasA == 1`（无机床 A 轴）", "`a_setting.com`（隐藏清零预设）"),
        "ifIsSiFuInGrindWheel": ("A 轴与电主轴驱动", "`grindWheelType == 1`（**注意**：源码内 `0=伺服 / 1=变频`，此处实控写入 `INI[36]=0` 模拟量/变频分支）", "`a_setting.com` `SUB(UP6)`"),
        "ifIsNotSiFuInGrindWheel": ("A 轴与电主轴驱动", "`grindWheelType == 0`（写入 `INI[36]=1` 西门子伺服分支）", "`a_setting.com` `SUB(UP6)`"),
        "ifIsSiFuInExGrindWheel": ("A 轴与电主轴驱动", "`machineType == 1 && ifCenter == 0 && exGrindWheelType == 1`（写入 `INI[91]=0` 模拟量/变频分支）", "`a_setting.com` `SUB(UP6)`"),
        "ifIsNotSiFuInExGrindWheel": ("A 轴与电主轴驱动", "`machineType == 1 && ifCenter == 0 && exGrindWheelType == 0`（写入 `INI[91]=1` 西门子伺服分支）", "`a_setting.com` `SUB(UP6)`"),
        "ifIsSiFuInDressWheel": ("A 轴与电主轴驱动", "`dressWheelType == 1`（写入 `INI[37]=0` 模拟量/变频分支）", "`a_setting.com` `SUB(UP6)`"),
        "ifIsNotSiFuInDressWheel": ("A 轴与电主轴驱动", "`dressWheelType == 0`（写入 `INI[37]=1` 西门子伺服分支）", "`a_setting.com` `SUB(UP6)`"),
    }

    # Check completeness against ReplaceMarker.md (66)
    missing = set(m for m, _ in rm_list) - set(marker_meta)
    assert not missing, f"Missing markers: {missing}"

    groups_order = [
        "语言与平台",
        "授权与机械手",
        "机型与复合功能",
        "磨削中心 U 轴与外圆",
        "对刀与测量硬件",
        "修整器构型组合",
        "滚轮与齿形细分",
        "A 轴与电主轴驱动",
    ]

    # Non-ifIs text/placeholder rules from generatepro.cpp
    placeholder_rows = [
        ("`machineName`", "替换字符串", "规范化后的机床型号（大写、`×`/`*` → `x`、`_` 还原 `/`）", "`INFO_INIT.MPF`、`HMI/lng/*`、`hlp/**/index.html`"),
        ("`machineCHS`", "替换字符串", "`machineNameLng` 设备中文/多语言描述名", "`INFO_INIT.MPF`、`HMI/lng/*`、`hlp/**/index.html`"),
        ("`machineIndex`", "替换字符串", "`machineIndex` 设备出厂编号", "`INFO_INIT.MPF`、`HMI/proj/*.com`（含 `a_setting.com` `INI[130]`）"),
        ("`customInfo`", "替换字符串", "`customInfo` 客户简称/项目代号", "`INFO_INIT.MPF`"),
        ("`debugDate`", "替换字符串", "程序包生成的系统时间戳", "`INFO_INIT.MPF`"),
        ("`softwareVersion`", "替换字符串", "`HorizonJuicerCreator` 当前版本号（如 `V3.29.0`）", "`INFO_INIT.MPF`、`hlp/**/index.html`"),
        ("`specificationInfo`", "替换字符串", "配置规格编码数字串（由 `machineType`..`ifHasNoneTradeMark` 依次拼接）", "`INFO_INIT.MPF`"),
        ("`passwordSource`", "替换字符串", "6 位随机模板占位符（由 `a_setting.com` 动态口令机制接管）", "`a_setting.com`（旧版占位兼容）"),
        ("`chs.png`", "替换为 `eng.png`", "当 `lng == 1` 多语言模式时自动替换图标文件名引用", "`HMI/proj/*.com`、`HMI/cfg/*.ini`"),
        ("`[\"\\\\图标.png\",` / `],ac`", "兼容剥离", "当 `hmiMode == 1`（兼容模式）时剥离图标引用与 `,ac` 修饰符", "`HMI/proj/*.com`"),
        ("`;...` 行末/单行注释", "正则删除为 `;`", "当 `ifRemoveComments == 0` 时保留 `;*` 与 `;\"`、删除普通注释", "`.com` / `.spf` / `.mpf`"),
        ("文件名 `INFO_INIT.MPF`", "重命名主程序", "重命名为 `<规范化 machineName>.MPF`（`×`/`*` → `x`、`/` → `_`）", "`NC-Data/MPF/`"),
    ]

    out = []
    out.append("# 10.5 条件编译与字符替换标记全表")
    out.append("")
    out.append("本节对照 `Source_Library/ReplaceMarker.md`、`HorizonJuicerCreator/generatepro.cpp` 与 `oneReplace.json`，完整列出代码生成器执行的全部 **66 项条件编译标记（`;ifIs...`）**、**4 种源码书写语法**、**12 项文本占位/剥离规则** 以及 **47 项 Sinumerik ONE 跨平台替换映射**。")
    out.append("")
    out.append("## 1. 替换标记编写规范（4 种语法形式）")
    out.append("")
    out.append("当 `HorizonJuicerCreator` 判定某项特性 **不适用** 于当前配置时，会按正则匹配并把整行或整块替换为保留占位符（NC/HMI 文件替换为分号 `;`，在线帮助 HTML 替换为 `<!--removed-->`）：")
    out.append("")
    out.append("| 适用文件类型 | 作用粒度 | 编写语法格式 | 裁剪后输出 |")
    out.append("| :--- | :--- | :--- | :--- |")
    out.append("| `.SPF` / `.MPF` / `.com` / `.ini` / `.txt` | **行级标记** | `<有效语句> ;ifIsXXX`（行末词边界匹配） | `;`（整行删除并留空注释符） |")
    out.append("| `.SPF` / `.MPF` / `.com` / `.ini` / `.txt` | **块级标记** | `;ifIsXXXBegin` … 多行代码 … `;ifIsXXXEnd` | `;`（跨行整块删除） |")
    out.append("| `HMI/hlp/**/*.html`（在线帮助） | **行级标记** | `<HTML 行><!--ifIsXXXLine-->` | `<!--removed-->` |")
    out.append("| `HMI/hlp/**/*.html`（在线帮助） | **块级标记** | `<!--ifIsXXXBegin-->` … 多行 HTML … `<!--ifIsXXXEnd-->` | `<!--removed-->` |")
    out.append("")
    out.append("## 2. 全量 66 项 `;ifIs...` 条件编译标记索引表")
    out.append("")
    out.append("> **驱动标记极性特别提醒**：在 `creatorwindow.ui` 中，`grindWheelType`、`exGrindWheelType`、`dressWheelType` 的下拉第 `0` 项为 **伺服**、第 `1` 项为 **变频器**。`generatepro.cpp` 在裁剪 `a_setting.com` 时：`0=伺服` 保留 `;ifIsNotSiFuIn...`（向 `INI[36]`/`INI[37]`/`INI[91]` 写入 `1`）；`1=变频器` 保留 `;ifIsSiFuIn...`（写入 `0`）。切勿仅凭英文名称字面误判。")
    out.append("")

    total_markers = 0
    for grp_idx, grp_name in enumerate(groups_order, 1):
        items = [(m, desc) for m, desc in rm_list if marker_meta[m][0] == grp_name]
        out.append(f"### 2.{grp_idx} {grp_name}（{len(items)} 项）")
        out.append("")
        out.append("| 条件编译标记（`ReplaceMarker.md`） | 源码中文含义 | 保留条件（`generatepro.cpp`） | 作用目录 / 备注 |")
        out.append("| :--- | :--- | :--- | :--- |")
        for m, desc in items:
            total_markers += 1
            _, cond, scope = marker_meta[m]
            out.append(f"| `{m}` | {sanitize_cell(desc)} | {cond} | {scope} |")
        out.append("")

    out.append("## 3. 项目元数据占位符与自动文本替换规则（12 项）")
    out.append("")
    out.append("| 源码标记 / 匹配目标 | 替换行为 | 替换内容 / 触发条件 | 作用目标文件 |")
    out.append("| :--- | :--- | :--- | :--- |")
    for tgt, act, val, scope in placeholder_rows:
        out.append(f"| {tgt} | {act} | {val} | {scope} |")

    out.append("")
    out.append("## 4. Sinumerik ONE 跨平台信号替换全表（`oneReplace.json`，共 47 项）")
    out.append("")
    out.append("当 `HorizonJuicerCreator` 选择 **数控系统 = `2 Sinumerik ONE`** 时，系统自动遍历 `MPF`、`CMA`、`HMI/proj` 与 `System-CF-Card/user`，执行下列 47 项精准文本替换（`CF 卡序列号` 模板测试项已做脱敏处理）：")
    out.append("")
    out.append("| 类别 | 原 828D / 840D sl 符号 | 替换为 Sinumerik ONE 符号 | 说明 |")
    out.append("| :--- | :--- | :--- | :--- |")

    one_count = 0
    for k, v in one_json.items():
        one_count += 1
        if k.startswith("$A_DBB"):
            cat = "NC 快速交换位"
            src_s = escape_dollar_vars(k)
            dst_s = escape_dollar_vars(v)
            note = "映射 ONE 高速输入通道"
        elif k.startswith("aDbb"):
            cat = "HMI XML / 状态变量"
            src_s = f"`{k}`"
            dst_s = f"`{v}`"
            note = "映射 `digitInpVal` 数组"
        elif k.startswith("DB2700"):
            cat = "测头接口 PLC 地址"
            src_s = f"`{k}`"
            dst_s = f"`{v}`"
            note = "ONE 测头实时状态位"
        else:
            cat = "CF 卡硬件序列号模板"
            src_s = "`<828D 测试 CF 卡序列号（已脱敏）>`"
            dst_s = "`<ONE 测试 CF 卡序列号（已脱敏）>`"
            note = "仅用于出厂模板匹配替换"
        out.append(f"| {cat} | {src_s} | {dst_s} | {note} |")

    content = "\n".join(out) + "\n"
    return os.path.join(OUT_DIR, "replace_markers.md"), content, {
        "markers": total_markers,
        "placeholders": len(placeholder_rows),
        "one_replace": one_count,
    }


def self_audit(files_and_contents):
    sys.path.insert(0, os.path.join(MANUAL_ROOT, "tools"))
    try:
        import audit_manual
    except ImportError:
        print("WARN: tools/audit_manual.py not found; skipping self_audit")
        return

    all_errors = []
    for path, txt in files_and_contents:
        rel = os.path.relpath(path, MANUAL_ROOT)
        for sec in audit_manual.FORBIDDEN_SECRETS:
            if sec.lower() in txt.lower():
                all_errors.append(f"Secret '{sec}' in {rel}")
        cleaned = re.sub(r"```.*?```", "", txt, flags=re.S)
        cleaned = re.sub(r"`[^`\n]+`", "", cleaned)
        cleaned = re.sub(r"\$\$[\s\S]*?\$\$", "", cleaned)
        for li, line in enumerate(cleaned.splitlines(), 1):
            lno = re.sub(r"\$[^$\n]+\$", "", line).replace(r"\$", "")
            if "$" in lno:
                all_errors.append(f"Stray $ in {rel}:{li}: {line[:80]}")
        audit_manual._check_markdown_tables(txt, rel, all_errors)
        audit_manual._check_bare_numeric_shorthands(txt, rel, all_errors)

    if all_errors:
        print(f"SELF-AUDIT ERRORS ({len(all_errors)}):")
        for e in all_errors:
            print(" -", e)
        raise SystemExit(1)
    print("Self-audit passed (0 errors across all generated files).")


def main():
    builders = [
        build_m_codes_and_signals,
        build_config_ui_variables,
        build_full_variable_index,
        build_replace_markers,
    ]
    written = []
    for fn in builders:
        path, content, stats = fn()
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"Wrote {os.path.relpath(path, MANUAL_ROOT)}: {stats}")
        written.append((path, content))

    self_audit(written)


if __name__ == "__main__":
    main()
