"""Generate 6 high-DPI custom technical diagrams into images/diagrams/ (2x supersampled)."""

import math
import os
from PIL import Image, ImageDraw, ImageFont

MANUAL_DIR = os.path.abspath(r"c:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer-manual")
OUT_DIR = os.path.join(MANUAL_DIR, "images", "diagrams")

FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

W2, H2 = 3200, 1520
W1, H1 = 1600, 760

C_BG = (248, 250, 252)
C_DARK = (15, 23, 42)
C_SLATE = (51, 65, 85)
C_MUTED = (100, 116, 139)
C_BORDER = (203, 213, 225)
C_CARD = (255, 255, 255)
C_BLUE = (37, 99, 235)
C_BLUE_BG = (239, 246, 255)
C_TEAL = (5, 150, 105)
C_TEAL_BG = (236, 253, 245)
C_AMBER = (217, 119, 6)
C_AMBER_BG = (255, 251, 235)
C_RED = (220, 38, 38)
C_RED_BG = (254, 242, 242)
C_PURPLE = (124, 58, 237)
C_PURPLE_BG = (245, 243, 255)


def f_reg(sz):
    return ImageFont.truetype(FONT_REG, sz)


def f_bold(sz):
    return ImageFont.truetype(FONT_BOLD, sz)


def f_mono(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, sz)


def new_canvas(title, subtitle):
    im = Image.new("RGB", (W2, H2), C_BG)
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W2, 136], fill=C_DARK)
    dr.rectangle([0, 136, W2, 144], fill=C_BLUE)
    dr.text((56, 24), title, font=f_bold(46), fill=(255, 255, 255))
    dr.text((58, 86), subtitle, font=f_reg(26), fill=(191, 219, 254))
    return im, dr


def rbox(dr, xy, radius=20, fill=C_CARD, outline=C_BORDER, width=3):
    dr.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def arrow(dr, x0, y0, x1, y1, color, width=5, head=18):
    dr.line([(x0, y0), (x1, y1)], fill=color, width=width)
    ang = math.atan2(y1 - y0, x1 - x0)
    a1 = ang + math.pi * 0.82
    a2 = ang - math.pi * 0.82
    p1 = (x1 + head * math.cos(a1), y1 + head * math.sin(a1))
    p2 = (x1 + head * math.cos(a2), y1 + head * math.sin(a2))
    dr.polygon([(x1, y1), p1, p2], fill=color)


def badge(dr, x, y, text, bg=C_BLUE, fg=(255, 255, 255), r=24):
    dr.ellipse([x - r, y - r, x + r, y + r], fill=bg)
    bb = dr.textbbox((0, 0), text, font=f_bold(26))
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    dr.text((x - tw / 2, y - th / 2 - 4), text, font=f_bold(26), fill=fg)


def wrap_text_px(dr, text, font, max_w):
    """Wrap mixed CJK/ASCII text cleanly without splitting ASCII identifiers or numbers mid-token."""
    tokens = []
    buf = ""
    for ch in text:
        if ch.isascii() and (ch.isalnum() or ch in "_[]/.-"):
            buf += ch
        else:
            if buf:
                tokens.append(buf)
                buf = ""
            tokens.append(ch)
    if buf:
        tokens.append(buf)

    lines = []
    cur = ""
    for tok in tokens:
        cand = cur + tok
        if dr.textbbox((0, 0), cand, font=font)[2] <= max_w or not cur:
            cur = cand
        else:
            lines.append(cur.rstrip())
            cur = tok.lstrip()
    if cur:
        lines.append(cur.rstrip())
    return lines


def save_downsampled(im, fname):
    out_path = os.path.join(OUT_DIR, fname)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    im.resize((W1, H1), Image.Resampling.LANCZOS).save(out_path, optimize=True)
    print(f"Generated diagram: {out_path}")


def draw_mcp_keys():
    im, dr = new_canvas(
        "图 4-1 / 5-1  SINUMERIK 操作面板（OP + MCP）关键功能键与权限层级映射",
        "依据 SINUMERIK Operate 权限等级（ac1~ac7）与 Horizon-Juicer 各画面软键配置绘制",
    )
    # Left panel: HMI OP Softkeys separated strictly by screen
    rbox(dr, [56, 176, 1584, 1470], fill=C_CARD, outline=C_BORDER)
    dr.text((88, 200), "一、SINUMERIK Operate 显示单元（OP）硬键与分画面软键区", font=f_bold(32), fill=C_DARK)

    # Card A: CUSTOM Welcome Page (a_custom.com)
    rbox(dr, [88, 258, 824, 648], radius=14, fill=C_BLUE_BG, outline=C_BLUE, width=3)
    dr.rectangle([88, 258, 824, 312], fill=(30, 64, 175))
    dr.text((108, 269), "A. CUSTOM 欢迎主页 (a_custom.com)", font=f_bold(23), fill=(255, 255, 255))
    custom_lines = [
        ("底栏 HS：仅设 HS7 用户界面 (ac7)", "HS1~6、HS8 在欢迎页为空", C_RED),
        ("VS1 出厂信息 (ac7)：", "查看机型与编号 (隐藏 VS3 改号需 ac3)", C_DARK),
        ("VS2 备份恢复 (ac3)：", "需用户口令及开关 TECHNOLOGY[56]=1", C_TEAL),
        ("VS3 配件寿命 (ac7)：", "需开启开关 TECHNOLOGY[368]=1", C_DARK),
        ("VS5 加工统计 (ac4)：", "需钥匙开关 3 档及 TECHNOLOGY[57]=1", C_PURPLE),
        ("VS8 扩展菜单 (ac3)：", "展开 MENU_1 -> VS1 机床配置 (ac3)", C_BLUE),
        ("VS4 / VS6 / VS7：", "主层留空（无按钮）", C_MUTED),
    ]
    for idx, (k, v, col) in enumerate(custom_lines):
        yy = 330 + idx * 43
        dr.text((108, yy), k, font=f_bold(19), fill=col)
        kw = dr.textbbox((0, 0), k, font=f_bold(19))[2]
        dr.text((108 + kw + 6, yy), v, font=f_reg(19), fill=C_SLATE)

    # Card B: Bottom HS Bar inside User Interface (config-dependent)
    rbox(dr, [844, 258, 1552, 648], radius=14, fill=C_TEAL_BG, outline=C_TEAL, width=3)
    dr.rectangle([844, 258, 1552, 312], fill=C_TEAL)
    dr.text((864, 269), "B. 进入「用户界面」后底栏 HS 导航（按配置显隐）", font=f_bold(23), fill=(255, 255, 255))

    hs_items = [
        ("HS1\n磨削", (219, 234, 254), C_BLUE),
        ("HS2\n工艺", (219, 234, 254), C_BLUE),
        ("HS3\n修整", (219, 234, 254), C_BLUE),
        ("HS4\n对刀*", (254, 243, 199), C_AMBER),
        ("HS5\n外圆†", (237, 233, 254), C_PURPLE),
        ("HS6\n端面†", (237, 233, 254), C_PURPLE),
        ("HS7\n选择†", (237, 233, 254), C_PURPLE),
        ("HS8\n返回", (219, 234, 254), C_BLUE),
    ]
    for i, (lbl, bgc, bd) in enumerate(hs_items):
        bx = 862 + i * 84
        rbox(dr, [bx, 330, bx + 78, 404], radius=8, fill=bgc, outline=bd, width=2)
        dr.multiline_text((bx + 12, 342), lbl, font=f_bold(18), fill=C_DARK, spacing=2)

    hs_notes = [
        ("• 蓝底 HS1~3/HS8：", "全机型常驻底栏菜单", C_BLUE),
        ("• * 橙底 HS4 自动对刀：", "未配置自动对刀时动态隐藏 (无此键)", C_AMBER),
        ("• † 紫底 HS5~HS7：", "仅内螺纹磨削中心 (;ifIsCenter) 存在，", C_PURPLE),
        ("  ", "普通外螺纹 / 纯内螺纹均无 HS5~HS7！", C_RED),
        ("• para_switch 锁：", "解锁黄/白底可输(ac4)；锁定灰底只读", C_TEAL),
        ("• 坐标与偏移：", "$AA_IM[X/Z] 实时坐标 / $AC_DRF 手轮增量", C_SLATE),
    ]
    for idx, (k, v, col) in enumerate(hs_notes):
        yy = 420 + idx * 36
        dr.text((864, yy), k, font=f_bold(18), fill=col)
        kw = dr.textbbox((0, 0), k, font=f_bold(18))[2]
        dr.text((864 + kw + 4, yy), v, font=f_reg(18), fill=C_DARK)

    # Card C: Per-screen VS Softkey Allocation
    rbox(dr, [88, 668, 1552, 1144], radius=14, fill=(248, 250, 252), outline=C_SLATE, width=3)
    dr.text((112, 686), "C. 各画面右侧 VS 软键归属速查（不同画面完全不同，受机型与 a_setting 开关显隐）", font=f_bold(23), fill=C_DARK)

    vs_rows = [
        ("HS1 磨削", C_BLUE,
         "VS1/2 机械手/模拟(仅非中心+机械手) · VS3 空运行 · VS4 分段补偿 · VS5 螺距变换 · VS6 自磨夹具(仅内螺纹) · VS7 反向孔倒角 · VS8 变径磨削"),
        ("HS2 工艺", (8, 145, 178),
         "VS1 批量 · VS2 单件 · VS4 附加配置(开关) · VS5 Y轴设置(开关) · VS6 挡块设置(仅 UW 修整器) · VS7 修整后空刀一次 (VS3/VS8 留空)"),
        ("HS3 修整", C_AMBER,
         "VS1/2 三角/梯形(全齿形) · VS3 双圆弧 · VS4/6 单/方滚轮 · VS5 双滚轮 · VS7 滚压轮 · VS8 扩展->行星齿(外磨全齿形+附加) / 滚轮页 VS8 摆缸(液压)"),
        ("HS4 对刀", C_TEAL,
         "Mask22 外螺纹无 VS；中心开关 Mask23：VS1 右端/VS2 跳动/VS3 左端；中心测头 Mask24：VS1 跳动/VS2 左端；Mask25~27 专项探测"),
        ("磨削中心", C_PURPLE,
         "HS7 加工选择：VS1/2 机械手(选配)、VS3~7 外圆/右端/左端/台阶/内螺纹；HS5 外圆：VS1~3、VS5/6 台阶；HS6 端面：VS1~3"),
        ("系统管理", C_RED,
         "a_setting 机床配置：Mask0 隐藏 VS3 取挑战码(ac3) / Mask1 VS3 重置数据(ac3) / Mask2 VS7/8；a_stats 统计：VS1/4 重置(ac4)、Mask3 VS1 滚轮"),
    ]
    for idx, (tag, col, desc) in enumerate(vs_rows):
        yy = 730 + idx * 67
        rbox(dr, [112, yy + 4, 246, yy + 52], radius=8, fill=col, outline=col)
        dr.text((126, yy + 15), tag, font=f_bold(19), fill=(255, 255, 255))
        wrapped = wrap_text_px(dr, desc, f_reg(18), 1265)
        if len(wrapped) == 1:
            dr.text((262, yy + 15), wrapped[0], font=f_reg(18), fill=C_DARK)
        else:
            for li, ln in enumerate(wrapped[:2]):
                dr.text((262, yy + 4 + li * 26), ln, font=f_reg(18), fill=C_DARK)

    # Card D: Physical OP Hardkeys
    rbox(dr, [88, 1166, 1552, 1442], radius=14, fill=C_AMBER_BG, outline=C_AMBER, width=3)
    dr.text((116, 1188), "D. OP 面板物理功能键导航速查：", font=f_bold(25), fill=C_AMBER)
    op_lines = [
        ("• [CUSTOM] / Shift+F8：任意界面一键直达 Horizon-Juicer 欢迎主页 (a_custom.com)", C_DARK),
        ("• [MENU SELECT] (F10)：打开底部主区域切换栏（加工 / 参数 / 程序 / 调试）", C_DARK),
        ("• [SELECT]：在下拉枚举框中切换选项（如 批量/单件、右旋/左旋、参数锁开关）", C_DARK),
        ("• [INPUT] / [ENTER]：写入当前输入框数值；未按 INPUT 确认前参数不生效", C_RED),
    ]
    for idx, (txt, col) in enumerate(op_lines):
        dr.text((116, 1236 + idx * 48), txt, font=f_reg(22), fill=col)

    # Right panel: MCP Machine Control Panel
    rbox(dr, [1608, 176, 3144, 1470], fill=C_CARD, outline=C_BORDER)
    dr.text((1644, 200), "二、MCP 机床控制面板权限等级、手轮与循环控制", font=f_bold(32), fill=C_DARK)

    # Keyswitch + Password levels (ac1..ac7 exact mapping)
    rbox(dr, [1644, 258, 3104, 728], radius=14, fill=C_RED_BG, outline=C_RED, width=3)
    badge(dr, 1694, 304, "1", bg=C_RED)
    dr.text((1736, 284), "SINUMERIK 权限等级（ac1~ac7）与钥匙开关映射（序号越小权限越高）", font=f_bold(25), fill=C_RED)
    levels = [
        ("ac1 制造商口令", "客户侧最高口令级：向下兼容全部 ac2~ac7 界面、软键与参数", C_PURPLE),
        ("ac2 服务口令", "调试/售后服务口令级：向下兼容全部 ac3~ac7 界面与软键", C_BLUE),
        ("ac3 用户口令", "解锁 VS2 备份恢复、VS8->VS1 机床配置、a_setting VS3 与 a_info VS3", C_TEAL),
        ("ac4 钥匙开关 3 档", "日常改参默认位！解锁磨削/工艺/修整/对刀/中心参数输入与加工统计", C_RED),
        ("ac5 钥匙开关 2 档", "中间操作级（权限低于 ac4，无法修改 ac4 参数）", C_AMBER),
        ("ac6 钥匙开关 1 档", "初级操作级（权限低于 ac4，无法修改 ac4 参数）", C_SLATE),
        ("ac7 钥匙开关 0 档", "最低级/无限制：操作 HS7 用户界面、VS1 出厂信息、VS3 配件寿命及常规导航", C_MUTED),
    ]
    for idx, (lv, desc, col) in enumerate(levels):
        yy = 348 + idx * 52
        rbox(dr, [1676, yy, 1948, yy + 41], radius=8, fill=col, outline=col)
        dr.text((1692, yy + 7), lv, font=f_bold(19), fill=(255, 255, 255))
        dr.text((1966, yy + 7), desc, font=f_reg(20), fill=C_DARK)

    # Mode + DRF block
    rbox(dr, [1644, 748, 2354, 1136], radius=14, fill=C_BLUE_BG, outline=C_BLUE, width=3)
    badge(dr, 1694, 796, "2", bg=C_BLUE)
    dr.text((1736, 774), "工作方式与 DRF 手轮补偿", font=f_bold(26), fill=C_BLUE)
    dr.text((1678, 844), "• [JOG] + [1/10/100]：手动点动对刀与找正", font=f_reg(22), fill=C_DARK)
    dr.text((1678, 890), "• [MDA]：手动输入执行单段 NC/复位指令", font=f_reg(22), fill=C_DARK)
    dr.text((1678, 936), "• [AUTO] + [DRF 有效]：关键调试技巧！", font=f_bold(22), fill=C_RED)
    dr.text((1698, 978), "在 AUTO 磨削循环期间打开手轮 DRF，", font=f_reg(21), fill=C_SLATE)
    dr.text((1698, 1012), "旋转手轮直接微调 X/Z（即画面上", font=f_reg(21), fill=C_SLATE)
    dr.text((1698, 1046), "红色 X_DRF / Z_DRF 实时增量，", font=f_reg(21), fill=C_SLATE)
    dr.text((1698, 1080), "磨削与对刀位置同步生效）。", font=f_reg(21), fill=C_SLATE)

    # Cycle Start / Feed Override
    rbox(dr, [2386, 748, 3104, 1136], radius=14, fill=C_TEAL_BG, outline=C_TEAL, width=3)
    badge(dr, 2436, 796, "3", bg=C_TEAL)
    dr.text((2478, 774), "循环控制与倍率安全规范", font=f_bold(26), fill=C_TEAL)
    dr.text((2420, 844), "• [CYCLE START] (绿键)：启动当前选定操作", font=f_reg(22), fill=C_DARK)
    dr.text((2420, 886), "  (由工作模式/GRIND[1]/TECH 等触发)", font=f_reg(21), fill=C_SLATE)
    dr.text((2420, 936), "• [CYCLE STOP] (红键) / [RESET]：暂停/复位", font=f_reg(22), fill=C_DARK)
    dr.text((2420, 984), "• [单段 SINGLE BLOCK]：首次试磨建议开启", font=f_reg(22), fill=C_DARK)
    dr.text((2420, 1032), "• [倍率旋钮]：对刀/首件校验时将进给与", font=f_bold(22), fill=C_RED)
    dr.text((2440, 1070), "快速倍率调至 20%~50% 确认无干涉！", font=f_reg(21), fill=C_SLATE)

    # Bottom signal summary (fixed INI[36]/INI[37]/INI[91])
    rbox(dr, [1644, 1158, 3104, 1442], radius=14, fill=C_PURPLE_BG, outline=C_PURPLE, width=3)
    badge(dr, 1694, 1206, "4", bg=C_PURPLE)
    dr.text((1736, 1184), "PLC 与 NC 变量核心联动点（调试必查）", font=f_bold(26), fill=C_PURPLE)
    dr.text((1680, 1248), "• 关键 PLC-NC 信号：$A_DBB[0]修整 / [1]手动对刀 / [5]自动对刀 / [2]退刀中断(PLCASUP1) / [80]侧门", font=f_reg(22), fill=C_DARK)
    dr.text((1680, 1294), "• 砂轮状态与驱动模式 INI[36]/INI[37]/INI[91]：必须执行一次 VS3->Mask2 重置才能与", font=f_reg(22), fill=C_DARK)
    dr.text((1700, 1332), "HorizonJuicerCreator 配置的 伺服(M1=3 S1=) / 变频器(R299+M13) 输出格式匹配！", font=f_bold(22), fill=C_RED)
    dr.text((1680, 1378), "• 急停 [EMERGENCY STOP]：任何碰撞风险下直接拍下，确认后先 RESET 再回参考点", font=f_reg(22), fill=C_DARK)

    save_downsampled(im, "diag_mcp_keys.png")


def draw_taper_convention():
    im, dr = new_canvas(
        "图 6-1  外螺纹与内螺纹锥度符号、左右端坐标及导程/锥度补偿方向图解",
        "依据 Source_Library GUD 变量 INI[1]/INI[2]（Z 端点）、INI[14]（单位锥度）与 INI[141]/INI[24]（全长补偿）绘制",
    )
    rbox(dr, [56, 184, 1570, 1180], fill=C_CARD, outline=C_BLUE, width=4)
    dr.text((92, 214), "一、外螺纹磨削（machineType=0）锥度与坐标约定", font=f_bold(32), fill=C_BLUE)

    arrow(dr, 220, 740, 1440, 740, C_SLATE, width=4)
    dr.text((1448, 722), "+Z", font=f_bold(28), fill=C_SLATE)
    arrow(dr, 260, 900, 260, 320, C_SLATE, width=4)
    dr.text((240, 276), "+X (砂轮退刀方向)", font=f_bold(26), fill=C_SLATE)

    pts_ext = [(420, 620), (1180, 520), (1180, 960), (420, 860)]
    dr.polygon(pts_ext, fill=(219, 234, 254), outline=C_BLUE, width=4)
    dr.line([(360, 740), (1240, 740)], fill=C_DARK, width=3)

    dr.line([(420, 410), (420, 990)], fill=C_RED, width=3)
    dr.text((340, 344), "工件左端 Z\nINI[1] (HMI: INI[2])", font=f_bold(22), fill=C_RED)
    dr.line([(1180, 410), (1180, 990)], fill=C_TEAL, width=3)
    dr.text((1090, 344), "工件右端 Z\nINI[2] (HMI: INI[3])", font=f_bold(22), fill=C_TEAL)

    dr.line([(420, 520), (1180, 520)], fill=C_AMBER, width=3)
    arrow(dr, 420, 620, 420, 520, C_AMBER, width=5)
    dr.text((444, 468), "ΔX = 单位长度锥度(INI[14]) × (Z右 - Z左)", font=f_bold(23), fill=C_AMBER)

    rbox(dr, [96, 1004, 1528, 1146], radius=12, fill=C_BLUE_BG, outline=C_BLUE, width=2)
    dr.text((120, 1020), "外螺纹符号判定（以砂轮架位于 +X 侧为例）：", font=f_bold(24), fill=C_DARK)
    dr.text((120, 1058), "• INI[14] / INI[141] 为半径方向增量(mm/mm)：左端相对右端外径越大，ΔX > 0（右端更粗则为负值）", font=f_reg(22), fill=C_SLATE)
    dr.text((120, 1094), "• 注意区分前置/后置布局与正反螺旋方向；实机首件建议先输小值 ±0.002 mm 试磨实测中径斜率！", font=f_bold(22), fill=C_RED)

    rbox(dr, [1630, 184, 3144, 1180], fill=C_CARD, outline=C_TEAL, width=4)
    dr.text((1666, 214), "二、内螺纹磨削（machineType=1）孔内锥度与退刀方向", font=f_bold(32), fill=C_TEAL)

    arrow(dr, 1790, 740, 3010, 740, C_SLATE, width=4)
    dr.text((3020, 722), "+Z", font=f_bold(28), fill=C_SLATE)
    arrow(dr, 1830, 900, 1830, 320, C_SLATE, width=4)
    dr.text((1810, 276), "+X (离开内孔壁方向)", font=f_bold(26), fill=C_SLATE)

    dr.polygon([(1980, 460), (2780, 460), (2780, 560), (1980, 620)], fill=(209, 250, 229), outline=C_TEAL, width=4)
    dr.polygon([(1980, 860), (2780, 920), (2780, 1020), (1980, 1020)], fill=(209, 250, 229), outline=C_TEAL, width=4)
    rbox(dr, [2120, 650, 2320, 720], radius=8, fill=(254, 215, 170), outline=C_AMBER, width=3)
    dr.text((2160, 668), "内磨砂轮", font=f_bold(22), fill=C_DARK)

    dr.line([(1980, 400), (1980, 1040)], fill=C_RED, width=3)
    dr.text((1920, 356), "Z左 INI[1]", font=f_bold(22), fill=C_RED)
    dr.line([(2780, 400), (2780, 1040)], fill=C_BLUE, width=3)
    dr.text((2710, 356), "Z右 INI[2]", font=f_bold(22), fill=C_BLUE)

    arrow(dr, 2220, 722, 2220, 800, C_RED, width=5)
    dr.text((2245, 738), "前/后置安全退刀 INI[23]\n(退回工件中心 INI[10])", font=f_bold(22), fill=C_RED)

    rbox(dr, [1670, 1004, 3102, 1146], radius=12, fill=C_TEAL_BG, outline=C_TEAL, width=2)
    dr.text((1694, 1020), "内螺纹符号判定要点（内孔磨削方向与外圆相反）：", font=f_bold(24), fill=C_DARK)
    dr.text((1694, 1058), "• 内螺纹磨削接刀方向及退刀方向取决于 U 轴配置与砂轮前/后置（X_CENTER = INI[10] 安全中心位）", font=f_reg(22), fill=C_SLATE)
    dr.text((1694, 1094), "• 全长锥度补偿 INI[141] (HMI: INI[142]) 直接叠加在 Z 左/右行程全长上，单位 mm（半径值）", font=f_bold(22), fill=C_TEAL)

    rbox(dr, [56, 1214, 3144, 1464], fill=C_AMBER_BG, outline=C_AMBER, width=3)
    dr.text((92, 1240), "关键参数索引对照表（切勿混淆「NC 0基数组下标」与「HMI 1基显示下标」）：", font=f_bold(28), fill=C_AMBER)
    dr.text((92, 1296), "• 工件左端 Z / 右端 Z：NC 程序读 INI[1] / INI[2]   <->   HMI 界面绑定 INI[2] / INI[3]", font=f_mono(24), fill=C_DARK)
    dr.text((92, 1340), "• 单位长度锥度(半径)：NC 程序读 INI[14] (mm/mm) <->   HMI 界面绑定 INI[15]   |   工件螺距：INI[4] <-> INI[5]", font=f_mono(24), fill=C_DARK)
    dr.text((92, 1384), "• 全长导程补偿 / 全长锥度补偿：NC 读 INI[24] / INI[141]   <->   HMI 绑定 INI[25] / INI[142]（总补偿值直接覆盖在全长斜率上）", font=f_mono(24), fill=C_DARK)

    save_downsampled(im, "diag_taper_convention.png")


def draw_var_dia_multipitch():
    im, dr = new_canvas(
        "图 6-2  Mask56 两端变径磨削曲线 与 Mask50 / Mask58 单/多段变螺距分段模型",
        "依据 a_grind.com Mask50 / Mask56 / Mask58 与 Source_Library 插补逻辑绘制",
    )
    rbox(dr, [56, 184, 1570, 1460], fill=C_CARD, outline=C_BLUE, width=4)
    dr.text((92, 214), "一、螺纹两端变径磨削（Mask56，开关 TECHNOLOGY[109]）", font=f_bold(32), fill=C_BLUE)

    rbox(dr, [96, 286, 1530, 820], radius=12, fill=C_BLUE_BG, outline=C_BORDER, width=2)
    arrow(dr, 140, 720, 1490, 720, C_SLATE, width=4)
    dr.text((1410, 738), "+Z (全长)", font=f_bold(22), fill=C_SLATE)
    arrow(dr, 180, 750, 180, 320, C_SLATE, width=4)
    dr.text((196, 310), "+X 退刀方向 (正值向后退刀/增大外径/内径扩展)", font=f_bold(22), fill=C_SLATE)

    pts = [
        (220, 440),
        (360, 440),
        (560, 600),
        (1060, 600),
        (1260, 440),
        (1400, 440),
    ]
    dr.line(pts, fill=C_RED, width=7)
    dr.line([(220, 490), (360, 440)], fill=C_TEAL, width=4)
    dr.line([(1260, 440), (1400, 490)], fill=C_TEAL, width=4)

    for vx, lbl in [
        (360, "左无效牙\nANG_LEFT_IGNORE"),
        (560, "左过渡角\nANG_LEFT"),
        (1060, "右过渡角\nANG_RIGHT"),
        (1260, "右无效牙\nANG_RIGHT_IGNORE"),
    ]:
        dr.line([(vx, 390), (vx, 730)], fill=C_MUTED, width=2)
        dr.text((vx - 80, 742), lbl, font=f_reg(18), fill=C_DARK)

    dr.line([(1400, 440), (1480, 440)], fill=C_AMBER, width=2)
    dr.line([(1400, 600), (1480, 600)], fill=C_AMBER, width=2)
    arrow(dr, 1450, 600, 1450, 440, C_AMBER, width=4)
    dr.text((1280, 504), "X_DIS_RIGHT\n[114/115]", font=f_bold(20), fill=C_AMBER)

    arrow(dr, 250, 600, 250, 440, C_PURPLE, width=4)
    dr.text((266, 514), "X_DIS_LEFT\n[116/117]", font=f_bold(20), fill=C_PURPLE)

    dr.text((710, 548), "标准等径工作段 (X = 0)", font=f_bold(24), fill=C_BLUE)

    rbox(dr, [96, 854, 1530, 1420], radius=12, fill=C_CARD, outline=C_BLUE, width=2)
    dr.text((124, 878), "Mask56 核心控制与首次调试要点：", font=f_bold(28), fill=C_BLUE)
    lines56 = [
        ("1. 使能与平滑曲线：", "CHANGE_DIA_ENABLE=TECHNOLOGY[109/110]；首次对位置时关闭 THREAD_SMOOTH[300/301]=0，待轨迹标定好后再开启平滑！", C_RED),
        ("2. 无效牙位置模式：", "ANG_IGNORE_MODE[154/155]：0=平顺加工（绿线平滑过渡），1=等大加工（红线平直保径）。", C_DARK),
        ("3. 四组核心几何参数：", "右端 X_DIS_RIGHT[114/115]、过渡角 ANG_RIGHT[115/116]、无效牙角 [138/139]；左端对应 [116/117]、[117/118]、[139/140]。", C_DARK),
        ("4. 独立变径模式：", "BIANJING_ONLY[378/379]=0 螺纹+变径同步磨；=1 变径单独修磨，可执行 BJ_ONLY_N[379/380] 次局部修正。", C_TEAL),
    ]
    for i, (h, t, col) in enumerate(lines56):
        yy = 944 + i * 112
        dr.text((124, yy), h, font=f_bold(23), fill=col)
        wrapped = wrap_text_px(dr, t, f_reg(21), 1340)
        for li, ln in enumerate(wrapped[:2]):
            dr.text((146, yy + 38 + li * 32), ln, font=f_reg(21), fill=C_SLATE)

    rbox(dr, [1630, 184, 3144, 1460], fill=C_CARD, outline=C_PURPLE, width=4)
    dr.text((1666, 214), "二、螺距变换：Mask50 单段 vs Mask58 五段分段变螺距", font=f_bold(32), fill=C_PURPLE)

    rbox(dr, [1670, 286, 3104, 820], radius=12, fill=C_PURPLE_BG, outline=C_BORDER, width=2)
    arrow(dr, 1730, 720, 3060, 720, C_SLATE, width=4)
    dr.text((3010, 738), "Z 位置", font=f_bold(22), fill=C_SLATE)
    arrow(dr, 1760, 750, 1760, 320, C_SLATE, width=4)
    dr.text((1780, 310), "局部螺距 P(z) / 变换增量", font=f_bold(22), fill=C_SLATE)

    seg_x = [1840, 2060, 2280, 2500, 2720, 2940]
    seg_y = [600, 560, 480, 420, 510, 610]
    seg_pts = list(zip(seg_x, seg_y))
    dr.line(seg_pts, fill=C_PURPLE, width=7)
    for i, (px, py) in enumerate(seg_pts):
        dr.ellipse([px - 10, py - 10, px + 10, py + 10], fill=C_AMBER, outline=C_DARK, width=2)
        dr.line([(px, py), (px, 720)], fill=C_MUTED, width=2)
        dr.text((px - 36, 736), f"POS_{i+1}", font=f_bold(20), fill=C_DARK)
    for i in range(5):
        mx = (seg_x[i] + seg_x[i + 1]) // 2 - 42
        my = min(seg_y[i], seg_y[i + 1]) - 54
        dr.text((mx, my), f"段{i+1}: P{i+1}\n(ANG_{i+1})", font=f_bold(18), fill=C_PURPLE)

    rbox(dr, [1670, 854, 2370, 1420], radius=12, fill=C_AMBER_BG, outline=C_AMBER, width=3)
    dr.text((1698, 882), "Mask50 单段变螺距\n(a_setting TOOL_SET[61/62]=1)", font=f_bold(25), fill=C_AMBER)
    dr.text((1698, 968), "• 使能：TOOL_SET[59/60]", font=f_mono(21), fill=C_DARK)
    dr.text((1698, 1006), "• 模式：TOOL_SET[60/61]", font=f_mono(21), fill=C_DARK)
    dr.text((1716, 1044), "0 = 给定角度 (TOOL_SET[67/68])", font=f_reg(20), fill=C_SLATE)
    dr.text((1716, 1078), "1 = 给定终点位置2 ([65/66])", font=f_reg(20), fill=C_SLATE)
    dr.text((1698, 1122), "• 起点位置1：TOOL_SET[64/65]", font=f_mono(21), fill=C_DARK)
    dr.text((1698, 1160), "• 变换目标螺距：TOOL_SET[66/67]", font=f_mono(21), fill=C_DARK)
    dr.text((1698, 1210), "• 同样受曲线平滑开关", font=f_bold(21), fill=C_RED)
    dr.text((1716, 1244), "TECHNOLOGY[301/302] 控制！", font=f_mono(21), fill=C_RED)

    rbox(dr, [2404, 854, 3104, 1420], radius=12, fill=C_TEAL_BG, outline=C_TEAL, width=3)
    dr.text((2432, 882), "Mask58 五段多段变螺距\n(a_setting TOOL_SET[61/62]=2)", font=f_bold(25), fill=C_TEAL)
    dr.text((2432, 968), "• 6 个Z节点定位 5 段螺距：", font=f_bold(22), fill=C_DARK)
    dr.text((2452, 1004), "POS_1: TOOL_SET[64/65]", font=f_mono(20), fill=C_DARK)
    dr.text((2452, 1038), "POS_2..5: TECH[417..420 / +1]", font=f_mono(20), fill=C_DARK)
    dr.text((2452, 1072), "POS_6: TOOL_SET[65/66]", font=f_mono(20), fill=C_DARK)
    dr.text((2432, 1118), "• 5 段对应角度与螺距变换值：", font=f_bold(22), fill=C_DARK)
    dr.text((2452, 1154), "ANGEL_1..5: TECH[421..425 / +1]", font=f_mono(20), fill=C_DARK)
    dr.text((2452, 1188), "PITCH_VAL1..5: TECH[426..430]", font=f_mono(20), fill=C_DARK)
    dr.text((2432, 1244), "• 适用于高精密非均匀变导程", font=f_reg(21), fill=C_SLATE)
    dr.text((2452, 1278), "丝杠及滚道补偿曲线。", font=f_reg(21), fill=C_SLATE)

    save_downsampled(im, "diag_var_dia_multipitch.png")


def draw_roller_calibration():
    im, dr = new_canvas(
        "图 7-1  砂轮与金刚石滚轮/金刚笔 三区块标定几何关系图",
        "对应 7.2 砂轮设定与修整器标定界面（V/VW/XZ/X 四种安装与 A/B/C 三类修整器）",
    )
    cols = [
        (56, 1040, "区块 A：砂轮尖端参考坐标 (V / XW / XZ)", C_BLUE, C_BLUE_BG),
        (1080, 2110, "区块 B：圆弧滚轮 vs 单边滚轮半径标定", C_TEAL, C_TEAL_BG),
        (2150, 3144, "区块 C：金刚笔 / 方片滚轮刃宽 L 标定", C_AMBER, C_AMBER_BG),
    ]
    for x0, x1, title, col, bg in cols:
        rbox(dr, [x0, 184, x1, 1460], fill=C_CARD, outline=col, width=4)
        dr.text((x0 + 30, 214), title, font=f_bold(28), fill=col)
        rbox(dr, [x0 + 30, 280, x1 - 30, 920], radius=12, fill=bg, outline=C_BORDER, width=2)

    dr.polygon([(360, 330), (740, 330), (740, 610), (550, 810), (360, 610)], fill=(203, 213, 225), outline=C_DARK, width=4)
    dr.ellipse([538, 798, 562, 822], fill=C_RED)
    arrow(dr, 550, 868, 550, 822, C_RED, width=4)
    dr.text((340, 868), "砂轮最外尖端参考点 (Z_tip, X_tip)", font=f_bold(22), fill=C_RED)
    dr.line([(550, 330), (550, 398)], fill=C_BLUE, width=3)
    dr.line([(550, 485), (550, 810)], fill=C_BLUE, width=3)
    dr.text((380, 410), "H: 新轮直径 DRESSER[23/24]\n   当前直径实时递减", font=f_bold(21), fill=C_BLUE)

    dr.ellipse([1260, 420, 1520, 680], fill=(167, 243, 208), outline=C_TEAL, width=4)
    dr.line([(1390, 550), (1490, 470)], fill=C_RED, width=4)
    dr.text((1340, 520), "R", font=f_bold(30), fill=C_RED)
    dr.text((1250, 710), "A 圆弧滚轮\n半径 R 补偿齿底圆弧", font=f_bold(22), fill=C_TEAL)
    dr.polygon([(1710, 420), (1950, 420), (1950, 680), (1830, 680), (1710, 520)], fill=(191, 219, 254), outline=C_BLUE, width=4)
    dr.ellipse([1818, 668, 1842, 692], fill=C_RED)
    dr.text((1700, 710), "B 单边滚轮\n仅单侧直壁接触修整", font=f_bold(22), fill=C_BLUE)

    dr.polygon([(2340, 380), (2640, 380), (2640, 560), (2490, 700), (2340, 560)], fill=(203, 213, 225), outline=C_DARK, width=4)
    dr.rectangle([2520, 700, 2760, 830], fill=(253, 230, 138), outline=C_AMBER, width=4)
    arrow(dr, 2520, 860, 2760, 860, C_RED, width=4)
    arrow(dr, 2760, 860, 2520, 860, C_RED, width=4)
    dr.text((2550, 874), "刃宽 L (方片/金刚笔)", font=f_bold(22), fill=C_RED)
    dr.text((2660, 460), "Z向平顶/侧翼\n偏置修整路径", font=f_reg(22), fill=C_DARK)

    texts = [
        (56, [
            "1. 修整坐标轴联动模式：",
            "• 立式/卧式插补(V/VW): U/V 轴或 Z/X 联控",
            "• 成型 X 修整(XZ/X): U 轴缺失时 X 轴直驱",
            "• 无U轴外磨位(后置0/前置1)及 DRESSER[37] 决定",
            "  修整进给符号与接触位正负方向。",
            "• 标定流程: 轻碰确定尖端 -> 写入",
            "  当前位置 -> 自动反算新砂轮补偿。",
        ]),
        (1080, [
            "2. 滚轮结构与修整方向匹配：",
            "• 双圆弧滚轮(A): 圆角半径 R 必须小于",
            "  齿槽最小圆弧；修整器DRESSER[0]，滚轮DRESSER[3]=0/1/2。",
            "• 单边滚轮(B): 左右侧接触角与",
            "  进刀侧壁分开标定，防单侧过切。",
            "• 滚轮转速线速度控制:",
            "  WHEEL_LINESPEED_DRESS[0..79]。",
        ]),
        (2150, [
            "3. 金刚笔/方片滚轮注意事项：",
            "• 方片滚轮刃宽 L 决定平顶切宽",
            "  与两侧翼退刀安全量；",
            "• 内螺纹无 U 轴成型修整时需注意",
            "  前/后置安全避让 (Mask17 vs Mask19)",
            "• 修整后实时同步 DRESSER[24]",
            "  当前直径并记录修整轮寿命台账。",
        ]),
    ]
    for x0, lines in texts:
        rbox(dr, [x0 + 30, 956, x0 + 960, 1424], radius=12, fill=C_BG, outline=C_BORDER, width=2)
        for i, ln in enumerate(lines):
            font_use = f_bold(22) if i == 0 else f_reg(21)
            col_use = C_DARK if i == 0 else C_SLATE
            dr.text((x0 + 54, 980 + i * 58), ln, font=font_use, fill=col_use)

    save_downsampled(im, "diag_roller_calibration.png")


def draw_tooth_profiles():
    im, dr = new_canvas(
        "图 7-2  四大标准齿形截面参数（TRI/TRAP/DARC/WORM）与 CAD 外部轮廓平面映射",
        "依据 Source_Library SHAPE_MODEL / TRI / TRAP / DARC / D_EXTERNE_SHAPE.SPF / D_LINE_TOOL_SHAPE.SPF 绘制",
    )
    cards = [
        (56, 790, "1. 三角齿形 (TRI)", C_BLUE, C_BLUE_BG),
        (824, 1558, "2. 梯形齿形 (TRAP)", C_TEAL, C_TEAL_BG),
        (1592, 2326, "3. 双圆弧 (DARC 哥特式)", C_PURPLE, C_PURPLE_BG),
        (2360, 3144, "4. 蜗杆齿形 (WORM)", C_AMBER, C_AMBER_BG),
    ]
    for x0, x1, title, col, bg in cards:
        rbox(dr, [x0, 184, x1, 950], fill=C_CARD, outline=col, width=4)
        dr.text((x0 + 24, 210), title, font=f_bold(27), fill=col)
        rbox(dr, [x0 + 24, 270, x1 - 24, 590], radius=10, fill=bg, outline=C_BORDER, width=2)

    # 1. TRI profile (text placed cleanly outside slope lines)
    dr.line([(120, 520), (270, 520), (420, 340), (570, 520), (720, 520)], fill=C_BLUE, width=6)
    dr.arc([394, 326, 446, 378], 200, 340, fill=C_RED, width=4)
    dr.text((130, 320), "牙型角 α\n(左右半角可调)", font=f_reg(20), fill=C_DARK)
    dr.text((516, 330), "齿底圆弧 R /\n凹槽选配", font=f_reg(20), fill=C_RED)

    # 2. TRAP profile
    dr.line([(890, 520), (1010, 520), (1090, 348), (1290, 348), (1370, 520), (1490, 520)], fill=C_TEAL, width=6)
    dr.text((1110, 300), "齿槽宽 W / 平顶", font=f_reg(20), fill=C_DARK)
    dr.text((1105, 420), "标准 6 项 /\n扩展多段圆角", font=f_reg(20), fill=C_TEAL)

    # 3. DARC Gothic arc profile (shifted arcs slightly downward to avoid overlapping text)
    dr.text((1820, 286), "哥特式双圆弧 (双偏心)", font=f_bold(20), fill=C_PURPLE)
    dr.arc([1770, 324, 2090, 520], 120, 230, fill=C_PURPLE, width=7)
    dr.arc([1830, 324, 2150, 520], 310, 60, fill=C_PURPLE, width=7)
    dr.ellipse([1946, 408, 1974, 436], fill=C_RED)
    dr.text((1660, 536), "左/右滚道半径与偏心 · 过切系数 1.07 / 1.11", font=f_bold(19), fill=C_RED)

    # 4. WORM profile
    dr.line([(2420, 520), (2540, 520), (2620, 348), (2840, 348), (2920, 520), (3060, 520)], fill=C_AMBER, width=6)
    dr.text((2590, 296), "模数 m · 压力角 α", font=f_reg(20), fill=C_DARK)
    dr.text((2625, 420), "法向/轴向齿厚\nC_DRESS_WORM_INIT(R3~R29)", font=f_bold(20), fill=C_RED)

    specs = [
        (56, ["• TRI[] + DRESSER[112]", "• 支持单圆弧齿顶 / 带", "  丝底凹槽 (Mask10)", "• 可控斜角 & 齿高修正"]),
        (824, ["• TRAP[] + SHAPE_MODEL", "• 支持左右偏心/牙底", "  圆弧/齿顶倒角", "• TIXING_TYPE 切标准/扩展"]),
        (1592, ["• DARC[] + SHAPE_MODEL[31..]", "• 行星齿 接触角 45~90°", "• DARC_CACL_REF 过切限制", "  范围 0.9~1.2 (默认 1.11)"]),
        (2360, ["• WORM_SHAPE 独立入口", "• ZA/ZN/ZK/ZI 等蜗杆齿形", "• M_OPEN/M_CLOSE OEM钩子(默认RET)", "  冷却/松夹: M8/28/38 · M35/36"]),
    ]
    for x0, lines in specs:
        for i, ln in enumerate(lines):
            dr.text((x0 + 30, 634 + i * 64), ln, font=f_reg(21), fill=C_DARK)

    rbox(dr, [56, 986, 1558, 1460], fill=C_BLUE_BG, outline=C_BLUE, width=4)
    dr.text((92, 1016), "D_EXTERNE_SHAPE.SPF —— 外部 CAD 左右分开修整", font=f_bold(30), fill=C_BLUE)
    dr.text((92, 1084), "• 适用场景：异形滚道、非标对称/不对称槽型直接导出 G 代码左右分边修整", font=f_reg(23), fill=C_DARK)
    dr.text((92, 1134), "• 插补平面与分边：DRESSER[56] 决定 G17(0) / G18(1) / G19(2)；DRESSER[44]=0右/1左", font=f_mono(22), fill=C_SLATE)
    dr.text((92, 1184), "• 外部路径位置：SHAPE_MODEL[0]（0内置 / 1后USB //DEV_3 / 2前USB / 3 CF卡）", font=f_reg(23), fill=C_DARK)
    dr.text((92, 1234), "• 提示：导入 CAD 轮廓前须在 shape/ 校验原点是否与砂轮尖端参考点重合！", font=f_bold(23), fill=C_RED)
    dr.text((92, 1294), "• 对应界面：通用齿形模块（a_shapecommon）外部轮廓名称 SHAPE_EXTERNAL", font=f_reg(23), fill=C_SLATE)

    rbox(dr, [1592, 986, 3144, 1460], fill=C_TEAL_BG, outline=C_TEAL, width=4)
    dr.text((1628, 1016), "D_LINE_TOOL_SHAPE.SPF —— 带刀补连续曲线（与通用积木区分）", font=f_bold(30), fill=C_TEAL)
    dr.text((1628, 1084), "• 适用场景：读取完整单段外部轨迹程序，并启用刀具半径补偿连续走刀", font=f_reg(23), fill=C_DARK)
    dr.text((1628, 1134), "• 刀补绑定：TOOL_INDEX=1, TOOL_EDGE_INDEX=1, TOOL_NAME=\"1\" ($TC_DP6[1,1]=DRESSER[32])", font=f_mono(21), fill=C_SLATE)
    dr.text((1628, 1184), "• 关键约束：通道须设 MD42480=0 防 EXTCALL+刀补报警（G41/G42放子程序内）；齿高 PROCESS[123]", font=f_reg(21), fill=C_DARK)
    dr.text((1628, 1234), "• 区分：参数化 10 线段积木(COMMON_LENGTH/ANG/RND)与平面修砂轮属 D_COMMON_SHAPE.SPF", font=f_reg(22), fill=C_SLATE)
    dr.text((1628, 1294), "• 注意：修整参数切换后必须在空行程下验证首轮空修防撞！", font=f_bold(23), fill=C_RED)

    save_downsampled(im, "diag_tooth_profiles.png")


def draw_probe_and_slot():
    im, dr = new_canvas(
        "图 8-1 / 9-1  内螺纹 4 种测头自动对刀模式 与 外圆在线测量 3 级进给控制",
        "依据 a_auto.com（Mask24~27）与 J_GRIND_ONLINE.SPF 逻辑绘制",
    )
    rbox(dr, [56, 184, 1660, 1460], fill=C_CARD, outline=C_BLUE, width=4)
    dr.text((92, 214), "一、内螺纹 4 种接触式测头自动对刀模式（a_auto.com）", font=f_bold(30), fill=C_BLUE)

    sub_modes = [
        (92, 286, "Mode 0 (Mask24): 测量反向孔（圆孔 / 腰型孔）", C_BLUE,
         "测头伸入反向孔内部摆扫，确定螺母反向孔中心 C0 与 Z 偏移；支持孔周探测搜索"),
        (92, 570, "Mode 1 (Mask25): 测量右端小台阶", C_TEAL,
         "需系统配置开放 TECHNOLOGY[128]=1：探测外圆右端小台阶端面以锁定工件基准"),
        (92, 854, "Mode 2 (Mask26): 测量右端定位孔", C_PURPLE,
         "通过工件右端面定位销孔（或端面基准孔）双侧探测确定 C 轴加工起始角"),
        (92, 1138, "Mode 3 (Mask27): 测量外圆直线及右端面内壁", C_AMBER,
         "在无反向孔时，复合探测外圆基准切面(.Z/.X)与右端面内壁(.Z/.X)完成定心定角"),
    ]
    for bx, by, t, col, desc in sub_modes:
        rbox(dr, [bx, by, 1624, by + 250], radius=12, fill=C_BG, outline=col, width=3)
        dr.text((bx + 26, by + 18), t, font=f_bold(25), fill=col)
        dr.text((bx + 26, by + 64), desc, font=f_reg(20), fill=C_DARK)
        rbox(dr, [bx + 26, by + 108, bx + 420, by + 226], radius=8, fill=C_CARD, outline=C_BORDER)
        if "Mask24" in t:
            # Slot / reverse hole schematic
            dr.line([(bx + 90, by + 140), (bx + 170, by + 140), (bx + 210, by + 206), (bx + 290, by + 140), (bx + 370, by + 140)], fill=C_BLUE, width=5)
            arrow(dr, bx + 210, by + 158, bx + 175, by + 172, C_RED, width=4)
            arrow(dr, bx + 210, by + 158, bx + 245, by + 172, C_RED, width=4)
            dr.text((bx + 448, by + 128), "支持圆形孔 / 腰型孔（角度/孔长/孔宽）\n可选「只测 C」同时折算端面 Z 偏刀", font=f_reg(21), fill=C_SLATE)
        elif "Mask25" in t:
            # Right step schematic
            dr.polygon([(bx + 110, by + 130), (bx + 260, by + 130), (bx + 260, by + 165), (bx + 310, by + 165), (bx + 310, by + 206), (bx + 110, by + 206)], fill=C_TEAL_BG, outline=C_TEAL, width=3)
            arrow(dr, bx + 365, by + 148, bx + 266, by + 148, C_RED, width=5)
            dr.text((bx + 448, by + 128), "适用于带右端定位小台阶的异形螺母\nprobePos = 0 向前 / 1 向后测量方向", font=f_reg(21), fill=C_SLATE)
        elif "Mask26" in t:
            # Pin hole on right face schematic
            dr.ellipse([bx + 170, by + 130, bx + 250, by + 206], fill=C_PURPLE_BG, outline=C_PURPLE, width=4)
            arrow(dr, bx + 210, by + 168, bx + 176, by + 168, C_RED, width=4)
            arrow(dr, bx + 210, by + 168, bx + 244, by + 168, C_RED, width=4)
            dr.text((bx + 448, by + 128), "可搭配磨削中心左右端面测量与跳动检校\n自动防碰退回安全中心位 PROCESS[53]", font=f_reg(21), fill=C_SLATE)
        else:
            # Outer diameter straight + inner endface wall schematic
            dr.line([(bx + 100, by + 200), (bx + 140, by + 142), (bx + 280, by + 142), (bx + 280, by + 204)], fill=C_AMBER, width=5)
            arrow(dr, bx + 210, by + 114, bx + 210, by + 140, C_RED, width=4)
            arrow(dr, bx + 340, by + 174, bx + 286, by + 174, C_RED, width=4)
            dr.text((bx + 448, by + 128), "核心参数：外圆找平 .Z/.X (TOOL_SET[71/72])\n与端反碰 .Z/.X (TOOL_SET[74/75])", font=f_reg(21), fill=C_SLATE)

    rbox(dr, [1700, 184, 3144, 1460], fill=C_CARD, outline=C_TEAL, width=4)
    dr.text((1736, 214), "二、磨削中心外圆在线量仪 3 级进给时序（J_GRIND_ONLINE.SPF）", font=f_bold(29), fill=C_TEAL)

    rbox(dr, [1736, 286, 3106, 940], radius=12, fill=C_TEAL_BG, outline=C_BORDER, width=2)
    arrow(dr, 1800, 860, 3050, 860, C_SLATE, width=4)
    dr.text((2940, 880), "余量 / 时间", font=f_bold(22), fill=C_SLATE)
    arrow(dr, 1820, 880, 1820, 320, C_SLATE, width=4)
    dr.text((1840, 310), "进给速度 F(mm/min) & X 坐标逼近", font=f_bold(22), fill=C_SLATE)

    steps = [
        (1820, 400), (2120, 400),
        (2120, 560), (2460, 560),
        (2460, 720), (2780, 720),
        (2780, 860), (2980, 860),
    ]
    dr.line(steps, fill=C_TEAL, width=7)
    dr.text((1850, 355), "阶段1: 粗磨进给 FA", font=f_bold(22), fill=C_BLUE)
    dr.text((2150, 490), "阶段2: 半精进给 FMA[3]\n(量仪第1信号触发切换)", font=f_bold(21), fill=C_AMBER)
    dr.text((2480, 650), "阶段3: 精磨进给 FMA[2]\n(量仪第2信号触发微进)", font=f_bold(21), fill=C_PURPLE)
    dr.text((2790, 756), "到达终尺寸 STA:\n光磨后 M93 撤回量仪", font=f_bold(20), fill=C_RED)

    rbox(dr, [1736, 976, 3106, 1424], radius=12, fill=C_BG, outline=C_TEAL, width=2)
    dr.text((1764, 1004), "J_GRIND_ONLINE.SPF 关键 NC 指令与系统机床数据要求：", font=f_bold(26), fill=C_TEAL)
    notes = [
        "1. SYN / 高速开关量切换：依赖 MD21220 ($MC_MULTFEED_ASSIGN_FASTIN)",
        "   与 MD21230 关联数字量高速输入字节，实现毫秒级不停顿变进给（FMA）。",
        "2. 量仪就位与撤回 M 代码：M92 伸出量仪气缸抱合外圆，到寸后发 M93 自动缩回量仪，",
        "   同时置 $A_OUT[3]=0 结束测量、砂轮退回安全位（PROCESS[46]）。",
        "3. 测量使能绑定：主览界面 Mask23 打开 [在线测量使能] (TECHNOLOGY[295/296])",
        "   且机床配置 INI[149/150] 允许显示时生效，避免空跑报量仪未就位报警。",
    ]
    for i, ln in enumerate(notes):
        col = C_DARK if i % 2 == 0 else C_SLATE
        dr.text((1764, 1068 + i * 54), ln, font=f_reg(22), fill=col)

    save_downsampled(im, "diag_probe_and_slot.png")


def main():
    draw_mcp_keys()
    draw_taper_convention()
    draw_var_dia_multipitch()
    draw_roller_calibration()
    draw_tooth_profiles()
    draw_probe_and_slot()
    print("All 6 technical diagrams generated cleanly.")


if __name__ == "__main__":
    main()
