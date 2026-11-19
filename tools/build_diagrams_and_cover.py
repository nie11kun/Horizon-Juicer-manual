"""
Generate HonKit cover images (cover.jpg, cover_small.jpg), engineering architecture
diagrams (arch_ecosystem_flow.png, creator_option_tree.png, hmi_navigation_map.png),
and copy curated HMI schematic illustrations from Source_Library into images/schematics/.
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont

MANUAL_DIR = r"c:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer-manual"
IMG_DIR = os.path.join(MANUAL_DIR, "images")
SCHEM_DIR = os.path.join(IMG_DIR, "schematics")
SRC_HLP_IMG = r"C:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer\Source_Library\HMI\hlp\chs\UserGuide\resources\img"
SRC_ICO_CHS = r"C:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer\Source_Library\HMI\ico\ico800\default\chs"

os.makedirs(IMG_DIR, exist_ok=True)


def load_font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf" if bold else r"C:\Windows\Fonts\simsun.ttc",
        r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def build_cover():
    W, H = 1600, 2260
    img = Image.new("RGB", (W, H), "#0b1324")
    draw = ImageDraw.Draw(img)

    # Subtle vertical gradient
    for y in range(H):
        t = y / H
        r = int(11 + t * 8)
        g = int(19 + t * 14)
        b = int(36 + t * 24)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Tech grid lines
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=(26, 42, 74), width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=(26, 42, 74), width=1)

    # Left accent bar & top badge
    draw.rectangle([(0, 0), (32, H)], fill="#2563eb")
    draw.rectangle([(120, 140), (760, 206)], fill="#172554", outline="#3b82f6", width=2)
    f_badge = load_font(30, bold=True)
    draw.text((155, 154), "SINUMERIK 828D / 840D sl / ONE", fill="#60a5fa", font=f_badge)

    # Main Title
    f_title = load_font(96, bold=True)
    f_sub = load_font(48, bold=True)
    f_desc = load_font(34, bold=False)
    f_small = load_font(30, bold=False)

    draw.text((120, 300), "Horizon-Juicer", fill="#f8fafc", font=f_title)
    draw.text((120, 420), "& HorizonJuicerCreator", fill="#38bdf8", font=load_font(76, bold=True))
    draw.line([(120, 540), (1480, 540)], fill="#334155", width=3)

    draw.text((120, 585), "西门子数控螺纹磨削程序库与定制工作台完全指南", fill="#e2e8f0", font=f_sub)
    draw.text((120, 670), "涵盖外螺纹 / 内螺纹 / 丝锥 / 蜗杆 / 环形槽 / 磨削中心全流程配置与实操", fill="#94a3b8", font=f_desc)

    # Center schematic cards visual
    cards = [
        ("01", "Creator 工程裁剪", "23 项机床结构动态联动\n828D / ONE / 中英俄多语言\n口令计算与注释批量清理", "#3b82f6"),
        ("02", "加工与工艺体系", "标准 / 扩展 / DIY 三模工艺\n螺距变换 / 变径 / 分段补偿\n反向孔倒角与自磨夹具", "#10b981"),
        ("03", "修整与自动对刀", "VW/UW/XZ/XW/V/X_Back/液压\n三角 / 梯形 / 双圆弧 / 行星齿\n接近开关 & 测头全自动测量", "#f59e0b"),
        ("04", "内螺纹磨削中心", "有/无 U 轴砂轮架控制\n外圆 / 台阶 / 左右端面联磨\n在线测量与加工选择总控", "#a855f7"),
    ]
    cw, ch = 640, 290
    positions = [(120, 820), (840, 820), (120, 1160), (840, 1160)]
    f_num = load_font(32, bold=True)
    f_ct = load_font(38, bold=True)
    f_cb = load_font(28, bold=False)
    for (num, title, body, accent), (cx, cy) in zip(cards, positions):
        draw.rounded_rectangle([(cx, cy), (cx + cw, cy + ch)], radius=18, fill="#111c33", outline="#283a5e", width=2)
        draw.rounded_rectangle([(cx, cy), (cx + 12, cy + ch)], radius=6, fill=accent)
        draw.text((cx + 38, cy + 28), f"PART {num}", fill=accent, font=f_num)
        draw.text((cx + 38, cy + 78), title, fill="#f8fafc", font=f_ct)
        draw.multiline_text((cx + 38, cy + 145), body, fill="#cbd5e1", font=f_cb, spacing=10)

    # Bottom bar
    draw.rounded_rectangle([(120, 1580), (1480, 1890)], radius=18, fill="#0f172a", outline="#1e3a8a", width=2)
    draw.text((165, 1625), "适用版本与部署平台", fill="#38bdf8", font=load_font(34, bold=True))
    specs = (
        "• 配置工作台版本：HorizonJuicerCreator v3.29.0\n"
        "• 适配数控系统：SINUMERIK 828D (老版/新版) / 840D sl / SINUMERIK ONE\n"
        "• 仿真验证平台：SinuTrain for SINUMERIK Operate 4.8 SP4\n"
        "• 交付范围：配置生成指南 · 实机与 SinuTrain 部署 · HMI 画面与 NC 工艺全书"
    )
    draw.multiline_text((165, 1690), specs, fill="#cbd5e1", font=load_font(29), spacing=14)

    draw.line([(120, 2040), (1480, 2040)], fill="#1e293b", width=2)
    draw.text((120, 2080), "HorizonJuicer Engineering Documentation", fill="#64748b", font=f_small)
    draw.text((1120, 2080), "Author: Nie Kun", fill="#94a3b8", font=f_small)

    cover_path = os.path.join(MANUAL_DIR, "cover.jpg")
    cover_small_path = os.path.join(MANUAL_DIR, "cover_small.jpg")
    img.save(cover_path, quality=95)
    img.resize((400, 565), Image.Resampling.LANCZOS).save(cover_small_path, quality=92)
    print("Generated cover.jpg and cover_small.jpg")


def draw_box(draw, x, y, w, h, title, lines, border="#3b82f6", fill="#f8fafc", header_fill="#1e3a8a", title_size=19, body_size=16):
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=12, fill=fill, outline=border, width=3)
    draw.rounded_rectangle([(x, y), (x + w, y + 46)], radius=12, fill=header_fill)
    draw.rectangle([(x, y + 30), (x + w, y + 46)], fill=header_fill)
    f_t = load_font(title_size, bold=True)
    f_b = load_font(body_size, bold=False)
    draw.text((x + 14, y + 10), title, fill="#ffffff", font=f_t)
    draw.multiline_text((x + 14, y + 58), "\n".join(lines), fill="#1e293b", font=f_b, spacing=6)


def draw_arrow(draw, x1, y1, x2, y2, color="#2563eb", label=None, label_offset=(0, 0)):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=4)
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    L = 13
    a1 = ang + math.pi * 0.82
    a2 = ang - math.pi * 0.82
    p1 = (x2 + L * math.cos(a1), y2 + L * math.sin(a1))
    p2 = (x2 + L * math.cos(a2), y2 + L * math.sin(a2))
    draw.polygon([(x2, y2), p1, p2], fill=color)
    if label:
        f_l = load_font(15, bold=True)
        bbox = draw.textbbox((0, 0), label, font=f_l)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        mx = (x1 + x2) // 2 - tw // 2 + label_offset[0]
        my = (y1 + y2) // 2 - th // 2 - 14 + label_offset[1]
        draw.rounded_rectangle([(mx - 5, my - 3), (mx + tw + 5, my + th + 3)], radius=4, fill="#ffffff")
        draw.text((mx, my), label, fill=color, font=f_l)


def build_arch_diagram():
    W, H = 1600, 820
    img = Image.new("RGB", (W, H), "#ffffff")
    draw = ImageDraw.Draw(img)

    f_h1 = load_font(30, bold=True)
    f_sub = load_font(18)
    draw.text((50, 28), "Horizon-Juicer 全流程工程架构：从源码库裁剪定制到实机 / SinuTrain 部署", fill="#0f172a", font=f_h1)
    draw.text((50, 72), "Source_Library -> HorizonJuicerCreator (v3.29.0) -> NC-Data + System-CF-Card -> SINUMERIK / SinuTrain", fill="#64748b", font=f_sub)

    draw_box(
        draw, 40, 140, 340, 320,
        "1. 源程序代码库 (Source_Library)",
        [
            "• CMA/：工艺、修整、对刀、丝锥、",
            "  磨削中心、夹具、机械手、备份恢复",
            "• MPF/：INFO_INIT.MPF 主控入口",
            "• DEF/：MGUD.DEF 全局变量定义",
            "• HMI/：proj(*.com)、lng、hlp、ico、",
            "  cfg 与 Repository 机型专用图",
            "• user/：VNC、USB、NC/PLC变量表、",
            "  machine_sec.ini 安全配置文件",
        ],
        border="#2563eb", header_fill="#1e3a8a", title_size=17, body_size=16,
    )

    draw_arrow(draw, 380, 300, 455, 300, color="#2563eb", label="读取模板")

    draw_box(
        draw, 455, 130, 345, 340,
        "2. HorizonJuicerCreator 工作台",
        [
            "• 机床信息：型号/名称/编号/语言",
            "• 结构配置：外/内螺纹、丝锥、蜗杆、",
            "  7种修整器、滚轮、齿形、自动对刀、",
            "  磨削中心(U轴)、A轴、电机驱动",
            "• 系统适配：老版828D / 新版828D /",
            "  Sinumerik ONE (oneReplace.json)",
            "• 智能裁剪：按 ;ifIs... 与 HTML 标记",
            "  剔除无效分支，重采样图标与图片",
            "• 辅助工具：口令计算、批量删注释",
        ],
        border="#0891b2", header_fill="#0e7490", title_size=18, body_size=16,
    )

    draw_arrow(draw, 800, 235, 910, 210, color="#059669", label="NC 输出")
    draw_arrow(draw, 800, 370, 910, 395, color="#7c3aed", label="HMI 输出")

    draw_box(
        draw, 910, 120, 320, 200,
        "3A. NC-Data 输出包",
        [
            "• CMA/*.SPF：定制后工艺子程序",
            "• MPF/<型号>.MPF：重命名主程序",
            "• DEF/MGUD.DEF：全局数组定义",
            "• 注：导入后须激活 DEF 并重启 NC",
        ],
        border="#059669", header_fill="#047857", title_size=18, body_size=16,
    )

    draw_box(
        draw, 910, 345, 320, 230,
        "3B. System-CF-Card 输出包",
        [
            "• user/：变量表、extdev、VNC、",
            "  machine_sec.ini 一机一密配置",
            "• oem/：cfg、lng、hlp、ico",
            "  (新版828D/ONE 含 proj 与 ico1024)",
            "• siemens/：老版828D proj 界面目录",
        ],
        border="#7c3aed", header_fill="#6d28d9", title_size=18, body_size=16,
    )

    draw_arrow(draw, 1230, 215, 1290, 260, color="#059669")
    draw_arrow(draw, 1230, 450, 1290, 400, color="#7c3aed")

    draw_box(
        draw, 1290, 150, 275, 395,
        "4. 部署与仿真验证",
        [
            "[真实机床部署]",
            "1) 拷入 NC-Data & CF卡",
            "2) 激活 MGUD.DEF",
            "3) 载入 NC_PLC-variates.xml",
            "4) CUSTOM->机床配置->重置",
            "",
            "[SinuTrain 仿真验证]",
            "1) System-CF-Card 拷入",
            "   4.8 SP4\\hmi 目录",
            "2) 调试->VS3切换语言刷新",
        ],
        border="#d97706", header_fill="#b45309", title_size=18, body_size=16,
    )

    # Bottom note strip
    draw.rounded_rectangle([(40, 610), (1560, 770)], radius=12, fill="#f1f5f9", outline="#cbd5e1", width=2)
    draw.text((65, 630), "闭环调试与二次加工提示", fill="#0f172a", font=load_font(21, bold=True))
    tips = (
        "• 解锁闭环：进入实机/SinuTrain「机床配置」时通过 VS3 获取动态滚动 6 位挑战码 -> 在 Creator「口令计算」获取 6 位解锁口令。\n"
        "• 目录对齐：设置中「源仓库目录」必须指向 Horizon-Juicer 根目录（其下需包含 Source_Library 子目录）；生成包自动归档为 <型号>(#<编号>-<用户>)。\n"
        "• 缓存清理：若修改了在线帮助 hlp 文档，必须删除 siemens/sinumerik/sys_cache/hmi/hlp 目录并重启 HMI，新帮助才会生效。"
    )
    draw.multiline_text((65, 672), tips, fill="#334155", font=load_font(17), spacing=9)

    out = os.path.join(IMG_DIR, "arch_ecosystem_flow.png")
    img.save(out)
    print("Generated", out)


def build_option_tree():
    W, H = 1600, 900
    img = Image.new("RGB", (W, H), "#ffffff")
    draw = ImageDraw.Draw(img)

    draw.text((50, 28), "HorizonJuicerCreator 机床配置动态联动与分支约束图", fill="#0f172a", font=load_font(30, bold=True))
    draw.text((50, 72), "选择不同「机床类型」与「修整器 / 自动对刀 / 磨削中心」选项时，界面控件自动显隐联动规则", fill="#64748b", font=load_font(18))

    draw_box(
        draw, 40, 340, 250, 150,
        "核心主分支：机床类型",
        [
            "comboBoxMachineType",
            "• 索引 0：外螺纹",
            "• 索引 1：内螺纹",
        ],
        border="#1d4ed8", header_fill="#1e3a8a", title_size=18, body_size=16,
    )

    draw_arrow(draw, 290, 390, 380, 240, color="#2563eb", label="外螺纹 (0)")
    draw_arrow(draw, 290, 440, 380, 620, color="#059669", label="内螺纹 (1)")

    draw_box(
        draw, 380, 120, 560, 290,
        "外螺纹专属与可选分支",
        [
            "• 是否磨丝锥：开放显示（选择「是」导入 CMA/SCREW_TAP）",
            "• 修整器类型：VW / V / XZ / 液压 / XW（隐藏 X_Back、UW）",
            "• 是否磨蜗杆：仅外螺纹且修整器为 VW 或 XZ 时显示",
            "• 二次对刀：仅外螺纹显示（有 / 无）",
            "• 自动对刀机构：开关 / 开关和测头（隐藏单「测头」）",
            "• 隐藏项：测头测量方向、磨削中心、U轴、外磨位置、外磨驱动",
        ],
        border="#2563eb", header_fill="#1d4ed8", title_size=18, body_size=16,
    )

    draw_box(
        draw, 380, 470, 560, 350,
        "内螺纹专属与磨削中心分支",
        [
            "• 修整器类型：XZ / X_Back / XW / UW（隐藏 VW、V、液压）",
            "• 自动对刀机构：开关 / 测头（隐藏「开关和测头」）",
            "• 测头测量方向：自动对刀=「有」时显示（向前测量 / 向后测量）",
            "• 磨削中心：仅内螺纹显示（是 / 不是）",
            "  ├─ 选「是」：显示 U轴（有/无）与 外磨砂轮驱动（伺服/变频）",
            "  └─ U轴=「无」时：显示 外磨位置（后置 / 前置）",
            "• 隐藏项：是否磨丝锥、是否磨蜗杆、二次对刀",
        ],
        border="#059669", header_fill="#047857", title_size=18, body_size=16,
    )

    draw_box(
        draw, 1020, 120, 535, 320,
        "修整轮与齿形联动规则",
        [
            "• 成型修整器（V / X_Back / 液压）时：",
            "  └─ 自动隐藏「修整轮类型」与「齿形选择」",
            "• 插补修整器（VW / XZ / XW / UW）时：",
            "  ├─ 修整轮类型：单/方滚轮 或 双滚轮",
            "  └─ 齿形选择：全套齿形（三角/梯形/双圆弧",
            "     /行星齿） 或 仅双圆弧",
        ],
        border="#d97706", header_fill="#b45309", title_size=18, body_size=16,
    )

    draw_box(
        draw, 1020, 480, 535, 340,
        "通用配置与系统输出模式",
        [
            "• A 轴配置：有 / 无（控制螺旋升角及修整 A 轴）",
            "• 砂轮 & 修整轮驱动：伺服 / 变频器",
            "• 语言：中文（仅 chs）或 多语言（中/英/俄）",
            "• 界面模式：标准（图标按钮）/ 兼容（文本按钮）",
            "• 数控系统：",
            "  ├─ 老版 828D：proj->siemens, ico800",
            "  ├─ 新版 828D：proj->oem, ico1024",
            "  └─ Sinumerik ONE：oneReplace 替换+$A_IN",
            "• 附加项：机械手、后期加密、删除厂商标识图",
        ],
        border="#7c3aed", header_fill="#6d28d9", title_size=18, body_size=16,
    )

    draw_arrow(draw, 940, 260, 1020, 260, color="#d97706")
    draw_arrow(draw, 940, 640, 1020, 640, color="#7c3aed")

    out = os.path.join(IMG_DIR, "creator_option_tree.png")
    img.save(out)
    print("Generated", out)


def build_hmi_nav_map():
    W, H = 1600, 980
    img = Image.new("RGB", (W, H), "#ffffff")
    draw = ImageDraw.Draw(img)

    draw.text((40, 28), "Horizon-Juicer SINUMERIK Operate HMI 全界面导航拓扑图", fill="#0f172a", font=load_font(30, bold=True))
    draw.text((40, 72), "按 CUSTOM 键进入欢迎页，通过底栏水平软键 (HS1~HS8) 与右侧垂直软键 (VS1~VS8) 调度全部功能画面", fill="#64748b", font=load_font(18))

    draw_box(
        draw, 40, 135, 345, 325,
        "CUSTOM 欢迎页 (a_custom)",
        [
            "• 底栏仅设 HS7 用户界面 (ac7)：",
            "  - 外螺纹->磨削(1) / 纯内->磨削(18)",
            "  - 磨削中心 -> 加工选择 (Mask23)",
            "• VS1 出厂信息 (ac7, 改号VS3:ac3)",
            "• VS2 备份恢复 (ac3, TECH[56]=1)",
            "• VS3 配件寿命 (ac7, TECH[368]=1)",
            "• VS5 加工统计 (ac4, TECH[57]=1)",
            "• VS8 扩展(ac3) -> VS1 机床配置(ac3)",
        ],
        border="#1e3a8a", header_fill="#1e3a8a", title_size=18, body_size=15,
    )

    draw_box(
        draw, 445, 135, 330, 325,
        "HS1 磨削参数 (a_grind)",
        [
            "• 主磨削：外(Mask1)/内(Mask18)",
            "• 特殊工艺：丝锥(52) / 环形槽(51)",
            "• 右侧 VS（受 a_setting 开关显隐）：",
            "  - VS1/2 机械手/模拟(非中心选配)",
            "  - VS3 空运行(55)·VS4 分段(57)",
            "  - VS5 螺距变换(Mask50单/58多)",
            "  - VS6 自磨夹具(53, 仅内螺纹)",
            "  - VS7 倒角(54)·VS8 变径(56)",
        ],
        border="#2563eb", header_fill="#2563eb", title_size=18, body_size=15,
    )

    draw_box(
        draw, 835, 135, 330, 325,
        "HS2 工艺参数 (a_process)",
        [
            "• 批量 / 单件工艺主表格：",
            "  - 精简工艺 (Mask2批量 / Mask29单件)",
            "  - 扩展工艺 (Mask20批量 / Mask30单件)",
            "• 粗磨 / 半精磨 / 精磨 / 终磨 / DIY",
            "• VS 子界面：",
            "  - VS4 附加配置 (Mask3)",
            "    (单头补偿、进刀量梯度)",
            "  - VS5 Y轴设置 (Mask4)",
            "  - VS6 挡块设置 (Mask5, UW)",
            "  - VS7 修整后空刀一次",
        ],
        border="#0891b2", header_fill="#0891b2", title_size=18, body_size=15,
    )

    draw_box(
        draw, 1225, 135, 335, 325,
        "HS3 修整参数 (dress/shape)",
        [
            "• Mask3 修整主界面：",
            "  - 新砂轮 / 旧砂轮 / 外部程序",
            "• 右侧 VS1~VS6 按选配动态显隐：",
            "  - 齿形：三角/梯形/双圆弧/行星齿/平面(选配)",
            "  - 滚轮：单/方/双滚轮、VS7 滚压轮",
            "  - 滚轮子页 VS8 摆缸(仅液压)",
        ],
        border="#d97706", header_fill="#d97706", title_size=18, body_size=15,
    )

    draw_box(
        draw, 40, 530, 345, 290,
        "HS4 自动对刀 (a_auto)",
        [
            "• 外螺纹开关/双机构 (Mask22)",
            "• 内螺纹开关测内滚道 (Mask23)",
            "• 内螺纹测头 4 模式 (Mask21 路由)：",
            "  - Mode0 测量反向孔 (Mask24)",
            "  - Mode1 测量右端小台阶 (Mask25)",
            "  - Mode2 测量右端定位孔 (Mask26)",
            "  - Mode3 外圆及右端内壁 (Mask27)",
            "• 磨削中心 VS1~3 跳动/端面复检",
        ],
        border="#059669", header_fill="#059669", title_size=18, body_size=15,
    )

    draw_box(
        draw, 445, 530, 545, 290,
        "HS5 外圆 / HS6 端面 / HS7 加工选择 (磨削中心)",
        [
            "• HS7 加工选择 (a_centermain Mask23)：",
            "  - 实时显示 X/Z/C/U/DRF 及内磨/外圆/端面加工状态",
            "  - VS3~VS7 勾选执行：外圆/右端面/左端面/外圆台阶/内螺纹",
            "• HS5 外圆参数 (a_centerwaiyuan)：",
            "  - VS1 磨削(Mask31) · VS2 工艺(Mask24) · VS3 修整(Mask26)",
            "  - VS5 台阶一(Mask33) · VS6 台阶二(Mask34)",
            "• HS6 端面参数 (a_centerduanmian)：",
            "  - VS1 磨削(Mask32) · VS2 工艺(Mask25) · VS3 修整(Mask27)",
        ],
        border="#7c3aed", header_fill="#7c3aed", title_size=18, body_size=15,
    )

    draw_box(
        draw, 1045, 530, 515, 290,
        "系统管理与运维界面",
        [
            "• 机床配置 (a_setting Mask0 -> Mask1)：",
            "  - VS3 显示动态挑战码(ac3) -> 解锁改 80+ 后台开关",
            "  - VS3 重置数据(ac3，按出厂预设恢复所有配置)",
            "• 加工统计 (a_stats Mask1)：99组砂轮累计件数 & 滚轮寿命",
            "• 配件寿命 (a_stats Mask3/4)：滚轮/夹具/金刚笔预警",
            "• 备份恢复 (a_backup_restore)：内部SPF / 前后USB / CF卡",
        ],
        border="#dc2626", header_fill="#b91c1c", title_size=18, body_size=15,
    )

    draw_arrow(draw, 385, 250, 445, 250, color="#2563eb", label="HS7")
    draw_arrow(draw, 775, 250, 835, 250, color="#0891b2", label="HS2")
    draw_arrow(draw, 1165, 250, 1225, 250, color="#d97706", label="HS3")
    draw_arrow(draw, 515, 460, 290, 530, color="#059669", label="HS4(配自动对刀)", label_offset=(-78, 0))
    draw_arrow(draw, 670, 460, 670, 530, color="#7c3aed", label="HS5~7(仅磨削中心)")

    draw.rounded_rectangle([(40, 850), (1560, 945)], radius=10, fill="#f8fafc", outline="#cbd5e1", width=2)
    draw.multiline_text(
        (65, 868),
        "提示：底栏水平软键 HS1~HS4 在螺纹加工画面统一；未启用「自动对刀」时 HS4 隐藏；仅「磨削中心」具备 HS5~HS7，普通外/内螺纹无此三键。\n"
        "访问权限：ac1 制造商 / ac2 服务 / ac3 用户口令（备份/配置）；ac4 钥匙开关 3 档（改参/统计重置）；ac5/6/7 对应钥匙 2/1/0 档。",
        fill="#334155",
        font=load_font(16),
        spacing=8,
    )

    out = os.path.join(IMG_DIR, "hmi_navigation_map.png")
    img.save(out)
    print("Generated", out)


def copy_curated_schematics():
    # Copy key existing HMI panel illustrations & UserGuide illustrations into images/schematics/
    hlp_picks = [f"pic{i}.png" for i in range(1, 56)]
    copied = 0
    for name in hlp_picks:
        src = os.path.join(SRC_HLP_IMG, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(SCHEM_DIR, f"hlp_{name}"))
            copied += 1

    panel_picks = [
        "panel_1_1_chs.png",
        "panel_18_4_chs.png",
        "panel_2_0_chs.png",
        "panel_3_4_chs.png",
        "panel_4_1_chs.png",
        "panel_5_1_chs.png",
        "panel_6_1_chs.png",
        "panel_7_7_chs.png",
        "panel_7_12_chs.png",
        "panel_8_10_chs.png",
        "panel_8_17_chs.png",
        "panel_8_45_chs.png",
        "panel_9_16_chs.png",
        "panel_10_0_chs.png",
        "panel_11_1_chs.png",
        "panel_12_1_chs.png",
        "panel_14_1_chs.png",
        "panel_16_1_chs.png",
        "panel_17_1_chs.png",
        "panel_19_1_chs.png",
        "panel_20_0_chs.png",
        "panel_21_2_chs.png",
        "panel_23_1_chs.png",
        "panel_23_2_chs.png",
        "panel_23_3_chs.png",
        "panel_23_4_chs.png",
        "panel_23_5_chs.png",
        "panel_23_6_chs.png",
        "panel_24_0_chs.png",
        "panel_25_0_chs.png",
        "panel_26_1_chs.png",
        "panel_27_1_chs.png",
        "panel_31_1_chs.png",
        "panel_32_1_chs.png",
        "panel_33_0_chs.png",
        "panel_50_0_chs.png",
        "panel_51_0_chs.png",
        "panel_52_0_chs.png",
        "panel_56_0_chs.png",
    ]
    for name in panel_picks:
        src = os.path.join(SRC_ICO_CHS, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(SCHEM_DIR, name))
            copied += 1
    print(f"Copied {copied} schematic images into {SCHEM_DIR}")


if __name__ == "__main__":
    build_cover()
    build_arch_diagram()
    build_option_tree()
    build_hmi_nav_map()
