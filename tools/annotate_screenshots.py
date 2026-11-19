"""Annotate all Creator (7) and SinuTrain HMI (44) raw screenshots with pixel-aligned callout boxes and legend footers."""

import os
from PIL import Image, ImageDraw, ImageFont

MANUAL_DIR = os.path.abspath(r"c:\Users\Marco Nie\Development\WorkProgram\Horizon-Juicer-manual")
SCRATCH_RAW = r"C:\Users\Marco Nie\.gemini\antigravity\brain\4170654c-8b49-4f7b-996b-4304aec2104a\scratch\raw_captures"
RAW_CREATOR = os.path.join(SCRATCH_RAW, "creator")
RAW_HMI = os.path.join(SCRATCH_RAW, "hmi")
RAW_OVERRIDES = os.path.join(MANUAL_DIR, "tools", "raw_overrides")
CUR_SCRATCH = r"C:\Users\Marco Nie\.gemini\antigravity\brain\091b2f29-df9d-4eba-9126-5ef79d7fbda4\scratch"

FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

PALETTE = [
    (239, 68, 68),    # 1 Red
    (37, 99, 235),    # 2 Blue
    (16, 185, 129),   # 3 Emerald
    (245, 158, 11),   # 4 Amber
    (139, 92, 246),   # 5 Violet
    (6, 182, 212),    # 6 Cyan
]


def font_r(sz):
    return ImageFont.truetype(FONT_REG, sz)


def font_b(sz):
    return ImageFont.truetype(FONT_BOLD, sz)


def draw_badge(dr, cx, cy, num, color, r=14, fsz=16):
    dr.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=(255, 255, 255))
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    txt = str(num)
    f = font_b(fsz)
    bb = dr.textbbox((0, 0), txt, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    dr.text((cx - tw / 2, cy - th / 2 - 2), txt, font=f, fill=(255, 255, 255))


def annotate_image(src_path, dest_path, callouts, erase_rects=None):
    """
    callouts: list of tuples (rect_xyxy, badge_pos_mode_or_xy, label)
      badge_pos_mode:
        'tl'|'tr'|'bl'|'br'  - inside corner
        'vleft'|'htop'       - outside left of VS / top of HS
        'out_l'|'out_r'      - outside left/right edge vertically centered
        'out_tl'|'out_tr'|'out_bl'|'out_br' - outside corner
        'top_l'|'top_r'|'bot_l'|'bot_r' - straddling top/bottom border
        'mid_l'|'mid_r'      - straddling left/right border vertically centered
        (bx, by)             - explicit center pixel coordinates
    """
    base = Image.open(src_path).convert("RGBA")
    w, h = base.size
    scale = max(1.0, w / 800.0)

    if erase_rects:
        base_rgb = base.convert("RGB")
        dr_clean = ImageDraw.Draw(base_rgb)
        for rect, sample_xy in erase_rects:
            col = base_rgb.getpixel(sample_xy)
            dr_clean.rectangle(rect, fill=col)
        base = base_rgb.convert("RGBA")

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr_ov = ImageDraw.Draw(overlay)
    line_w = max(2, int(round(3 * scale)))
    rad = max(6, int(round(8 * scale)))
    badge_r = int(round(13 * scale))
    badge_fsz = int(round(15 * scale))

    for idx, (rect, _, _) in enumerate(callouts):
        col = PALETTE[idx % len(PALETTE)]
        x0, y0, x1, y1 = rect
        dr_ov.rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=col + (28,), outline=col + (235,), width=line_w)

    merged = Image.alpha_composite(base, overlay).convert("RGB")
    dr_img = ImageDraw.Draw(merged)

    gap = int(round(5 * scale))
    for idx, (rect, bpos, _) in enumerate(callouts):
        col = PALETTE[idx % len(PALETTE)]
        x0, y0, x1, y1 = rect
        if isinstance(bpos, tuple):
            bx, by = bpos
        elif bpos == "vleft":
            bx, by = x0 - int(round(6 * scale)), (y0 + y1) // 2
        elif bpos == "htop":
            bx, by = (x0 + x1) // 2, y0 - int(round(4 * scale))
        elif bpos == "out_l":
            bx, by = x0 - badge_r - gap, (y0 + y1) // 2
        elif bpos == "out_r":
            bx, by = x1 + badge_r + gap, (y0 + y1) // 2
        elif bpos == "out_tl":
            bx, by = x0 - badge_r - gap, y0 + badge_r
        elif bpos == "out_tr":
            bx, by = x1 + badge_r + gap, y0 + badge_r
        elif bpos == "out_bl":
            bx, by = x0 - badge_r - gap, y1 - badge_r
        elif bpos == "out_br":
            bx, by = x1 + badge_r + gap, y1 - badge_r
        elif bpos == "top_l":
            bx, by = x0 + badge_r + gap, y0
        elif bpos == "top_r":
            bx, by = x1 - badge_r - gap, y0
        elif bpos == "bot_l":
            bx, by = x0 + badge_r + gap, y1
        elif bpos == "bot_r":
            bx, by = x1 - badge_r - gap, y1
        elif bpos == "mid_l":
            bx, by = x0, (y0 + y1) // 2
        elif bpos == "mid_r":
            bx, by = x1, (y0 + y1) // 2
        elif bpos == "tr":
            bx, by = x1 - badge_r - 2, y0 + badge_r + 2
        elif bpos == "bl":
            bx, by = x0 + badge_r + 2, y1 - badge_r - 2
        elif bpos == "br":
            bx, by = x1 - badge_r - 2, y1 - badge_r - 2
        else:  # 'tl'
            bx, by = x0 + badge_r + 2, y0 + badge_r + 2
        bx = max(badge_r + 4, min(w - badge_r - 4, bx))
        by = max(badge_r + 4, min(h - badge_r - 4, by))
        draw_badge(dr_img, bx, by, idx + 1, col, r=badge_r, fsz=badge_fsz)

    # Bottom Legend Strip
    pad_x = int(round(14 * scale))
    pad_y = int(round(10 * scale))
    leg_fsz = int(round(14 * scale))
    f_leg = font_r(leg_fsz)
    col_w = (w - 3 * pad_x) // 2

    def wrap_text(txt, max_px):
        if dr_img.textbbox((0, 0), txt, font=f_leg)[2] <= max_px:
            return [txt]
        lines, cur = [], ""
        for ch in txt:
            if dr_img.textbbox((0, 0), cur + ch, font=f_leg)[2] > max_px and cur:
                lines.append(cur)
                cur = ch
            else:
                cur += ch
        if cur:
            lines.append(cur)
        return lines

    badge_leg_r = int(round(10 * scale))
    text_offset = badge_leg_r * 2 + int(round(8 * scale))
    wrapped_items = []
    for idx, (_, _, label) in enumerate(callouts):
        lines = wrap_text(label, col_w - text_offset)
        wrapped_items.append((idx + 1, PALETTE[idx % len(PALETTE)], lines))

    line_h = int(round(leg_fsz * 1.38))
    rows_pair = []
    for i in range(0, len(wrapped_items), 2):
        left = wrapped_items[i]
        right = wrapped_items[i + 1] if i + 1 < len(wrapped_items) else None
        max_lines = max(len(left[2]), len(right[2]) if right else 1)
        rows_pair.append((left, right, max_lines))

    footer_h = pad_y * 2 + sum(r[2] * line_h + int(round(6 * scale)) for r in rows_pair)
    out = Image.new("RGB", (w, h + footer_h), (15, 23, 42))
    out.paste(merged, (0, 0))
    dr_out = ImageDraw.Draw(out)
    dr_out.rectangle([0, h, w, h + max(2, int(round(3 * scale)))], fill=(59, 130, 246))

    cur_y = h + pad_y
    for left, right, max_lines in rows_pair:
        for side_idx, item in enumerate((left, right)):
            if item is None:
                continue
            num, col, lines = item
            x_base = pad_x + side_idx * (col_w + pad_x)
            draw_badge(
                dr_out,
                x_base + badge_leg_r,
                cur_y + badge_leg_r + int(round(1 * scale)),
                num,
                col,
                r=badge_leg_r,
                fsz=int(round(12 * scale)),
            )
            for li, ln in enumerate(lines):
                dr_out.text((x_base + text_offset, cur_y + li * line_h), ln, font=f_leg, fill=(241, 245, 249))
        cur_y += max_lines * line_h + int(round(6 * scale))

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    out.save(dest_path, optimize=True)


CREATOR_SPECS = {
    "creator_main_workbench.png": [
        ([12, 74, 212, 152], "out_r", "顶部菜单栏：打开（系统工作路径配置）/ 帮助（版本历史）"),
        ([160, 810, 698, 1252], "tl", "机床配置入口：配置设备结构与生成 Sinumerik 程序包"),
        ([748, 810, 1286, 1252], "tl", "口令计算工具：秒算 6 位机床解锁响应口令"),
        ([1336, 810, 1874, 1252], "tl", "批量删除注释：清理生成包内 .COM/.SPF/.MPF 开发注释"),
        ([1330, 1468, 1446, 1540], "out_r", "关于我：查看版本演进与 V3.29.0 / V3.28.0 更新日志"),
    ],
    "creator_settings_dialog.png": [
        ([74, 322, 1656, 444], "top_r", "源仓库目录：须选到包含 Source_Library 的 Horizon-Juicer 根目录"),
        ([74, 452, 1656, 574], "bot_r", "程序生成目录：输出按 <型号>(#<编号>-<客户>) 归档的文件夹"),
        ([1114, 784, 1676, 886], "top_l", "操作按钮区：取消修改或点击「保存配置」写入 HorizonJuicerCreator.json"),
    ],
    "creator_config_center.png": [
        ([34, 174, 756, 766], "top_r", "机床信息：型号/名称/编号/用户及语言（0=中文, 1=多语言）"),
        ([34, 778, 756, 1398], "top_r", "其他设置：删注释、界面模式、数控系统(老/新828D/ONE)、机械手等"),
        ([770, 174, 1372, 1398], "top_r", "机床配置联动区：类型、XZ/VW 修整、齿形、测头/开关及中心/U/A轴"),
        ([1386, 174, 1996, 1398], "top_r", "生成状态监视区：校验配置、显示输出路径并自动打开文件夹"),
        ([34, 1412, 1996, 1556], "top_l", "底部操作栏：返回主菜单 / 保存 JSON 设置 / 一键生成程序"),
    ],
    "creator_config_external.png": [
        ([34, 174, 756, 766], "top_r", "外螺纹机型信息：SK7420 命名及多语言/中文输出模式选择"),
        ([770, 174, 1372, 704], "top_r", "外螺纹专有选配：丝锥、VW/X 等修整器、蜗杆与修整轮类型"),
        ([770, 710, 1372, 1398], "bot_r", "齿形与对刀驱动配置：齿形选择、二次对刀、测量机构及伺服/变频驱动"),
        ([1386, 174, 1996, 1556], "top_r", "状态与生成区：就绪后点击「程序生成」按条件编译裁剪并打包"),
    ],
    "creator_password_calc.png": [
        ([240, 326, 1792, 560], "top_r", "版本算法选择：V3.29.0+ 默认使用新版算法，老版本请切旧版"),
        ([240, 582, 1792, 768], "top_r", "6 位挑战码输入：支持手动输入、剪贴板自动识别粘贴与一键清空"),
        ([240, 796, 1792, 1274], "bot_l", "解锁口令结果区：输入 6 位即秒算，支持一键复制或 Enter 复制"),
    ],
    "creator_remove_comments.png": [
        ([256, 300, 1776, 526], "top_r", "目标目录选择：务必指向已生成的交付副本，严禁直选 Source_Library"),
        ([256, 566, 1776, 882], "bot_r", "格式与安全规则：递归扫描 .COM/.SPF/.MPF，保留 ;* 与 ;\" 标记"),
        ([256, 912, 1776, 1044], "top_l", "执行清理：就地剥离开发分号注释，精简代码体积"),
    ],
    "creator_about_history.png": [
        ([24, 74, 1958, 562], "top_r", "V3.29.0 新增特性：新版口令算法、去厂商标识图、M/DBB 及机械手更新"),
        ([24, 574, 1958, 1446], "top_r", "V3.28.0 历史版本：磨削中心分屏、多段变螺距、寿命/滚轮台账等演进"),
    ],
}


# Exact measured SINUMERIK 800x600 softkey geometry:
# VS1..8: step=66px, height=47px (y=39+(m-1)*66 .. 86+(m-1)*66), x=700..798
# HS1..8: width=98px (x=(k-1)*100+1 .. k*100-1), y=553..598
def hs_rect(k0, k1=None):
    k1 = k0 if k1 is None else k1
    return [(k0 - 1) * 100 + 1, 553, k1 * 100 - 1, 598]


def vs_rect(m0, m1=None):
    m1 = m0 if m1 is None else m1
    return [700, 39 + (m0 - 1) * 66, 798, 86 + (m1 - 1) * 66]


STATUS_ERASE = [([25, 534, 260, 550], (400, 540))]

HMI_SPECS = {
    "hmi_setup_main.png": {
        "callouts": [
            ([6, 72, 694, 482], "bot_r", "调试(Setup)主表：机床轴与驱动配置一览"),
            (vs_rect(3), "vleft", "第2步【关键】：直接点击右侧垂直软键 VS3 Change language"),
            (hs_rect(5), "htop", "切勿误点 HS5 HMI！HMI 子菜单内无 Change language 按钮"),
        ]
    },
    "hmi_setup_lang_popup.png": {
        "callouts": [
            ([226, 140, 572, 218], "bot_r", "语言列表：先选中 English - English 触发切换，再切回 Simplified Chinese"),
            (vs_rect(8), "vleft", "点击 VS8 确认生效：系统重读 alsc_*.qm / .com 文本，刷新全部界面中文"),
        ]
    },
    "hmi_custom_home.png": {
        "callouts": [
            ([4, 70, 696, 533], "tl", "定制主入口画布（如勾选删除厂商标识图则使用通用灰色无标识底图）"),
            (vs_rect(1, 3), "out_l", "VS1 出厂信息(ac7) / VS2 参数备份恢复(需 ac3 用户口令+开关) / VS3 配件寿命(ac7+开关)"),
            (vs_rect(5), "out_l", "VS5 加工统计与滚轮寿命记录（需 ac4 钥匙开关 3 档+开关）"),
            (vs_rect(8), (682, 518), "VS8 扩展菜单(MENU_1, 需 ac3 用户口令)：点击展开右侧顶部 VS1「机床配置」入口"),
            (hs_rect(7), "out_l", "HS7 用户界面(ac7)：进入主加工参数选择画面（外/内螺纹或磨削中心总览）"),
        ]
    },
    "hmi_device_info.png": {
        "callouts": [
            ([140, 250, 456, 368], "top_r", "显示机床型号及出厂编号（INI[130]；ac3 用户口令下连续点击隐藏 VS3 8次可解锁编辑）"),
            (hs_rect(8), "htop", "HS8 返回：退出出厂信息页回到 CUSTOM 主界面"),
        ]
    },
    "hmi_setting_challenge.png": {
        "callouts": [
            ([10, 74, 384, 110], "out_r", "6 位解码输入框：填入口令计算器生成的对应密码后按 INPUT 确认"),
            ([614, 496, 696, 532], "out_l", "6 位随机挑战码：ac3 用户口令下按隐藏 VS3 显示并动态更新"),
            (hs_rect(8), "htop", "HS8 返回：取消解锁并返回扩展菜单"),
        ]
    },
    "hmi_setting_mask1_top.png": {
        "callouts": [
            ([8, 68, 472, 333], "out_r", "驱动与动作开关：砂轮驱动(伺服/变频)、不关液压、多头补偿、恒转速等"),
            ([8, 336, 360, 520], "out_r", "功能开放总闸：扩展工艺、环形槽、三线测量、修整补偿及防护罩开关"),
            (vs_rect(3), "vleft", "【新机必做】VS3 重置数据(ac3)：导入程序包后必须执行一次以初始化硬件标志！"),
        ]
    },
    "hmi_setting_mask1_mid.png": {
        "erase": STATUS_ERASE,
        "callouts": [
            ([8, 68, 472, 306], "out_r", "自动对刀配置：一次/两次检测、测头方向(前/后)及内滚道测量 mode 选择"),
            ([8, 326, 546, 516], "out_r", "磨削中心专项开关：外圆砂轮驱动类型、外圆/端面头架旋向与修整器控制"),
            (vs_rect(3), "vleft", "VS3 重置数据(ac3)：根据生成包条件标签重置底层 INI / TECHNOLOGY 参数"),
        ]
    },
    "hmi_setting_mask1_bottom.png": {
        "erase": STATUS_ERASE,
        "callouts": [
            ([8, 66, 360, 302], "out_r", "特殊页面开关（Mask53~57/Y轴/配件寿命）：开启后对应画面垂直软键生效"),
            ([8, 324, 472, 514], "out_r", "第6类输入保护限值：安全Z最小距(默认30)、中径(±1)、进给(±0.1)、转速(60)"),
            (vs_rect(3), "vleft", "VS3 重置数据(ac3)：执行 SUB(UP6) 并弹出 Mask2 二次确认弹窗"),
        ]
    },
    "hmi_setting_reset_confirm.png": {
        "callouts": [
            ([122, 206, 578, 356], "top_r", "确认重置弹窗（Mask2）：执行后按 Creator 编译标签重写全部默认值与读写权限"),
            (vs_rect(7, 8), "vleft", "VS8 确认执行 SUB(UP6) 完成初始化（新机首装必点！）；VS7 取消操作"),
        ]
    },
    "hmi_stats_wheel.png": {
        "callouts": [
            ([8, 70, 415, 532], "bot_r", "左侧 99 组砂轮记录表：序号、累计已磨件数(WHEEL_GRIND_CUMU)及换轮日期"),
            ([424, 96, 680, 360], "bot_r", "当前砂轮索引及右侧「修整轮生命周期管理」（额定次数/已修次数/修整量）"),
            (vs_rect(1), "vleft", "VS1 重置统计：清零当前砂轮及 99 组换轮计数台账（需 ac4 钥匙开关 3 档）"),
            (vs_rect(4), "vleft", "VS4 重置修整轮计数：更换新金刚石滚轮后清零次数与累计量（需 ac4 钥匙开关 3 档）"),
        ]
    },
    "hmi_stats_life.png": {
        "callouts": [
            ([18, 100, 666, 238], "bot_r", "核心易损件寿命监控表（滚轮 / 夹具 / 外圆金刚笔 / 端面金刚笔：设定、已用、报警限与重置）"),
            ([18, 250, 310, 400], "out_r", "滚轮编号/夹具编号绑定输入框及「报警提示信息」总开关"),
            (vs_rect(1), "vleft", "VS1 进入滚轮台账：查看最近 100 次滚轮更换编号与日期履历"),
        ]
    },
    "hmi_stats_wheel_id.png": {
        "callouts": [
            ([8, 70, 476, 532], "bot_r", "99 行滚轮更换履历表：DRESS_WHEEL_NUM 与 DRESS_WHEEL_DATE 自动追加"),
            ([482, 98, 650, 136], "bot_r", "当前激活滚轮记录指针位置(INI[161/162])"),
            (hs_rect(8), "htop", "HS8 返回上一级配件寿命主界面"),
        ]
    },
    "hmi_backup_restore.png": {
        "callouts": [
            ([406, 79, 692, 196], "out_l", "模式选择(0加工/1备份/2恢复)、存储路径(内部SPF / 后USB //DEV_3)与文件名"),
            ([406, 202, 692, 232], "out_l", "备份模式：所有变量全量备份 / 指定列表文件中挑选关键数组备份"),
            ([406, 314, 508, 344], "out_l", "执行状态反馈栏（点击启动后执行；用完务必将模式改回「0 加工」！）"),
        ]
    },
    "hmi_external_grind.png": {
        "callouts": [
            ([6, 74, 430, 172], (280, 172), "实时监控与对刀控制：X/Z 与 DRF 手轮增量、丝锥开关、首次/二次与对刀点"),
            ([442, 74, 692, 232], "out_l", "核心螺纹特征：单件/批量、右/左旋、头数、螺距、锥度与螺旋升角"),
            ([442, 248, 668, 334], "out_l", "行程与安全坐标：工件左右端Z、对刀起始位.X"),
            ([442, 348, 692, 532], "out_l", "安全位置与现场微调区：安全X/C/退刀、导程/锥度全长补偿、中径（黄框）与偏刀"),
            ([6, 450, 356, 532], "top_r", "起始角 C、当前/初始接触 X 与首件切换（影响自动对刀后首次走刀逻辑）"),
        ]
    },
    "hmi_internal_grind.png": {
        "callouts": [
            ([6, 74, 294, 134], "out_r", "实时坐标与手轮 DRF：X/Z 当前位置与手轮动态微调量 ($AC_DRF)"),
            ([442, 74, 692, 232], "out_l", "内螺纹基本几何参数：加工模式、旋向、头数、螺距、半径锥度与螺旋升角"),
            ([442, 248, 676, 408], "out_l", "孔内安全与中心定义：工件左右端 Z、工件中心 X(INI[10]) 及安全位置 Z/X/C"),
            ([442, 424, 692, 532], "out_l", "全长导程/锥度补偿及中径/偏刀微调（带小锁受右侧开关联动控制）"),
            ([6, 450, 356, 532], "top_r", "起始角 C、当前/初始接触 X 及退刀方式（直接退出 / 螺旋退出 INI[84]）"),
        ]
    },
    "hmi_external_process.png": {
        "callouts": [
            ([4, 66, 386, 118], "out_r", "累计磨削总量/设定磨削总量与已加工/修整件数统计"),
            ([28, 128, 672, 434], "bot_l", "粗磨/半精磨/精磨/终磨 4 阶段工艺表：单双向、次数、切深、速度与转速"),
            (vs_rect(1, 2), "vleft", "VS1 批量工艺 / VS2 单件工艺（或切换为扩展多段修整工艺表格）"),
            (vs_rect(7), "vleft", "VS7 修整后空刀一次开关：开启后每次修整完紧跟一刀无进给光磨防烧伤"),
        ]
    },
    "hmi_process_extended.png": {
        "callouts": [
            ([14, 115, 682, 321], "top_r", "磨削阶段主表：单双磨削、循环次数、进给深度、磨削速度与砂轮线速度"),
            ([14, 324, 682, 441], "bot_r", "独立阶段修整行：可为粗/半精/精/终磨单独设定不同修整次数、余量与转速"),
            ([14, 444, 682, 532], "bot_r", "头架转速、磨削砂轮转速与修整砂轮转速折算实时监控"),
            (vs_rect(4, 5), "vleft", "VS4 附加配置(阶梯切深+6头偏置) / VS5 Y轴设置（需系统配置开启显示）"),
        ]
    },
    "hmi_process_addon.png": {
        "callouts": [
            ([8, 74, 400, 156], "out_r", "阶梯渐变进给控制：开启粗磨/半精磨进刀量梯度变化并设定首末刀差值"),
            ([8, 174, 668, 384], "bot_r", "单头位置独立补偿（最多支持第 1~6 头进刀位置 X、起始角 C 与锥度补偿 X）"),
            (vs_rect(8), "vleft", "VS8 返回上一级工艺主界面"),
        ]
    },
    "hmi_process_yaxis.png": {
        "callouts": [
            ([8, 74, 574, 272], "bot_r", "Y 轴参数区：有Y轴总开关、自动计算中心距、当前中心距及修整后实际 Y 位置"),
            (vs_rect(8), "vleft", "VS8 返回工艺参数主页面（需在 a_setting 中开启 Y 轴显示方能进入）"),
        ]
    },
    "hmi_tap_grind.png": {
        "callouts": [
            ([6, 136, 392, 174], "out_r", "丝锥模式与磨削类型切换：可切回「螺纹」普通模式或保持「丝锥」铲磨"),
            ([6, 181, 392, 306], "tr", "槽数、直槽/螺旋槽、螺旋槽旋向及螺旋槽升角定义"),
            ([6, 314, 392, 530], "tr", "跳齿铲磨选项（C/角度调整）、B/C 起始角、粗磨铲磨开关及接触位"),
            ([442, 74, 692, 532], "out_l", "右侧共用标准外螺纹几何区（左/右端Z、安全位及中径/偏刀补偿）"),
        ]
    },
    "hmi_ring_groove.png": {
        "erase": STATUS_ERASE,
        "callouts": [
            ([6, 74, 294, 339], "out_tr", "环形槽总览与当前位置：单/批量、总槽数、需加工/已加工槽及当前槽 Z/X"),
            ([442, 74, 688, 339], "out_l", "起止磨削槽范围(SLOT_INIT~END)、工件中心 X 与安全位置 X/Z"),
            ([30, 342, 668, 528], "bot_r", "分组(第一~四组)批量参数：各组槽数、槽距、槽宽(升量)与水平/垂直偏移"),
        ],
    },
    "hmi_adv_dryrun.png": {
        "callouts": [
            ([390, 72, 656, 334], "out_l", "空运行热机设定：总使能开关、自动卡爪、冷开与正向/负向 Z/X 行程终点"),
            ([390, 338, 656, 398], "out_l", "热机运行转速设定：砂轮主轴转速与Z-X联动空跑进给速度(mm/min)"),
            (hs_rect(1), "htop", "HS1 磨削参数：切回主磨削界面（加工前务必先关闭空运行使能！）"),
        ]
    },
    "hmi_adv_seg_comp.png": {
        "callouts": [
            ([24, 74, 456, 108], "out_r", "分段补偿总使能（TECHNOLOGY[310/311]）与补偿分段数上限设置"),
            ([24, 122, 612, 460], "bot_r", "10 段局部补偿表：各段边界起点/终点 Z 与局部中径补偿 X(半径)、导程补偿"),
            (hs_rect(1), "htop", "HS1 返回主磨削页；各段Z值需按工件左端到右端顺序连续分布"),
        ]
    },
    "hmi_adv_single_pitch.png": {
        "callouts": [
            ([390, 72, 668, 184], "out_l", "单段变螺距核心：使能开关、平滑轨迹、目标螺距与方式(给定角度/给定终点位置)"),
            ([390, 188, 668, 298], "out_l", "变螺距角度及分段起点位置 1 (TOOL_SET[64/65]) / 终点位置 2 坐标设定"),
        ]
    },
    "hmi_adv_multi_pitch.png": {
        "callouts": [
            ([390, 74, 616, 148], "out_l", "多段变螺距使能与「平滑轨迹」控制（首次校位务必先关闭平滑！）"),
            ([280, 154, 692, 344], "bot_r", "位置 1~6 与 5 段对应角度 / 螺距变换值表（TOOL_SET & TECHNOLOGY[417..430]）"),
        ]
    },
    "hmi_adv_jiaju.png": {
        "callouts": [
            ([6, 74, 160, 150], "out_r", "X/Z/C 机床实时坐标监控（便于对刀夹具找正读取当前值）"),
            ([6, 156, 234, 448], "out_r", "左侧夹具磨削参数：左右端Z、接触X、次数、进刀、速度、头架/砂轮转速"),
            ([390, 74, 640, 448], "out_l", "自磨夹具总使能、Z安全起始位及右侧夹具砂轮修整全部参数"),
        ]
    },
    "hmi_adv_chamfer.png": {
        "callouts": [
            ([6, 74, 308, 530], "top_r", "单滚道最多 24 孔孔间距偏移表与可选 X 向终补偿（DISTANCE_Z & TECH[271..290]）"),
            ([316, 74, 693, 234], "bot_l", "反向孔倒角总使能、补偿模式(直接/渐变)、精磨不倒角、平滑及过渡角/深度"),
            ([316, 240, 693, 400], "bot_l", "模式设置、单双滚道及孔距自动计算与倒角基准偏移量"),
        ]
    },
    "hmi_adv_var_dia.png": {
        "callouts": [
            ([390, 72, 670, 234], "out_l", "变径使能、轨迹平滑、无效牙位置模式（0=平顺加工 / 1=等大加工）及无效牙角"),
            ([390, 238, 670, 358], "out_l", "左右端变径量（正值向后退刀/扩径）及左右端变径过渡角度设定"),
            ([390, 362, 670, 400], "out_l", "变径磨削模式（0=螺纹+变径同步磨削 / 1=变径单独局部磨削及次数）"),
        ]
    },
    "hmi_external_dress.png": {
        "callouts": [
            ([408, 76, 636, 132], "out_l", "修整器结构(VW/XZ)、当前齿形/滚轮选择及新/旧砂轮状态切换"),
            ([402, 138, 694, 311], "tr", "粗修/精修主参数：次数（新轮首次由系统计算可调）、单次切深与进给速度"),
            ([382, 316, 694, 484], "out_l", "砂轮几何与安全限位：宽度、新轮/当前直径、线速度/转速自动计算与最小直径"),
            (vs_rect(1, 3), "vleft", "右侧齿形快速跳转入口：VS1 三角 / VS2 梯形 / VS3 双圆弧"),
            (vs_rect(4, 6), "vleft", "右侧滚轮标定入口：VS4 单滚轮 / VS6 方滚轮（双滚轮机型显示 VS5，按配置动态裁剪）"),
        ]
    },
    "hmi_dress_plane.png": {
        "callouts": [
            ([408, 76, 636, 132], "out_r", "齿形选择「平面」(DRESSER[4]=4)：需在系统配置开启 TECHNOLOGY[431]=1 后追加显示"),
            ([208, 127, 421, 160], "out_l", "平面锥度(DRESSER[141], mm)：正值表示修整后砂轮左大右小；对刀须砂轮左端对准滚轮中心"),
            ([406, 316, 658, 343], "out_r", "砂轮宽度(DRESSER[22], mm)：决定单向平面修整行程长度及微锥度斜角换算"),
        ]
    },
    "hmi_external_wheel.png": {
        "callouts": [
            ([6, 74, 124, 130], "out_r", "V/W（UW 机型为 U/W）修整器实时轴坐标监视（含滚轮中心偏移几何示意图）"),
            ([404, 110, 692, 336], "out_l", "单圆弧滚轮核心参数：修整中心 W、圆弧半径 R、初始接触 V(U) 与当前接触 V(U)"),
            ([404, 360, 682, 448], "out_l", "修整轮直径及修整轮线速度/转速（WHEEL_LINESPEED_DRESS）"),
        ]
    },
    "hmi_wheel_square.png": {
        "callouts": [
            ([404, 110, 682, 234], "out_l", "方片/金刚笔核心参数：修整中心 W、方滚轮厚度 L、左/右倒角圆弧"),
            ([404, 238, 692, 448], "out_l", "修整初始接触 V(U) / 当前接触 V(U) 及修整轮直径/线速度/转速设定"),
            (vs_rect(6), "vleft", "VS6 方滚轮激活态（VS7 滚压轮未配置时自动灰显禁用）"),
        ]
    },
    "hmi_external_shape.png": {
        "callouts": [
            ([8, 74, 699, 156], "bl", "圆弧角度、自动计算钢球直径及哥特式标准参数/斜角过切切换"),
            ([78, 159, 602, 351], "out_r", "双圆弧滚道参数表：左/右初始圆弧半径、微调量与水平偏心（分初始/调整/当前）"),
            ([8, 364, 270, 452], "bot_r", "齿形旋转补偿角、右侧高低微调与延长斜线角度（防边缘干涉）"),
        ]
    },
    "hmi_shape_triangle.png": {
        "callouts": [
            ([396, 72, 676, 234], "out_l", "三角齿形定义：齿底圆弧半径、左/右斜面角度及左/右齿根圆弧半径"),
            ([396, 238, 676, 348], "out_l", "齿高、锥度修正与延长线角度（支持标准单圆弧及带丝底凹槽模式）"),
        ]
    },
    "hmi_shape_trapezoid.png": {
        "callouts": [
            ([396, 72, 676, 448], "out_l", "梯形齿形参数：齿底长/圆弧半径、左右斜面角度、齿高、平顶/锥顶模式与延长角"),
            (vs_rect(2), "vleft", "VS2 梯形模块激活态（如开启扩展梯形，下方显示多段倒角/偏心参数）"),
        ]
    },
    "hmi_external_auto.png": {
        "callouts": [
            ([6, 74, 145, 108], "out_r", "测头信号灯：实时指示接近开关/测头触发状态 (DB2700.DBX1.0)"),
            ([390, 74, 668, 148], "out_l", "对刀结果微调及接近开关与砂轮物理重合位标定 (TOOL_SET[41] / INI[42])"),
            ([390, 502, 692, 532], "out_l", "X / Z / C 三轴当前坐标参考（方便手动寻找初始采样基准位）"),
        ]
    },
    "hmi_internal_auto.png": {
        "callouts": [
            ([6, 74, 378, 108], (188, 108), "测头信号灯及对刀结构模式（反向孔 / 标准孔 / 测头1·2号）"),
            ([396, 74, 664, 328], "out_l", "对刀中心与特征区：结果调整、测头水平/中心位、起始位Z、半径与反向孔测量角"),
            ([396, 331, 697, 496], "out_l", "孔形与周向探测：孔缺口深、常规圆孔/腰型孔尺寸及孔周探测参数"),
            (vs_rect(1, 2), "vleft", "VS1 外圆跳动 / VS2 左端测量（磨削中心自动对刀辅助复检页面切换）"),
        ]
    },
    "hmi_center_main.png": {
        "callouts": [
            ([4, 72, 227, 530], "tr", "左栏全轴监控：X/Z/C/U 坐标、DRF 手轮增量与内磨/外圆/端面初始及当前接触位"),
            ([233, 72, 695, 270], "tr", "上区「内螺纹」状态面板：已加工数、中径/偏刀、砂轮直径、粗修次数与工艺模式"),
            ([233, 274, 695, 399], "tr", "中区「外圆磨削」状态面板：批量/单件、累计/设定总量与粗修次数"),
            ([233, 403, 695, 531], "tr", "下区「端面磨削」状态面板：左右端独立累计/设定磨削量与粗修计数"),
            (vs_rect(3, 7), "vleft", "右侧多工序组合选择（绿灯亮起表示执行）：外圆 / 右端 / 左端 / 台阶 / 内螺纹"),
        ]
    },
    "hmi_center_cylindrical.png": {
        "callouts": [
            ([6, 74, 244, 132], (266, 84), "外圆轴 U / Z 实时机床坐标（无 U 轴配置时自动切换显示共用 X 轴）"),
            ([416, 79, 686, 282], "out_l", "加工模式、磨削起点/终点 Z 与终点补偿/退刀槽长度设定"),
            ([416, 288, 664, 484], "out_l", "初始/当前磨削接触 X(U)、尺寸补偿及外磨安全位置 X/Z/C 设定"),
            (vs_rect(1, 6), "vleft", "外圆分支：VS2 工艺参数 / VS3 外圆修整 / VS5 台阶一 / VS6 台阶二 (VS4 留空)"),
        ]
    },
    "hmi_center_cyl_process.png": {
        "callouts": [
            ([32, 72, 692, 124], "out_l", "外圆磨削总量统计与「保持分段」/ 已加工 / 修整设定监控"),
            ([28, 128, 674, 430], "bot_r", "外圆 4 阶段工艺表：粗磨/半精磨/精磨/终磨 磨削方式、次数、切深、速度与转速"),
            ([28, 430, 260, 482], "out_r", "直接靠磨左端与同修端面联动开关（开启后外磨前顺带完成左端面修磨）"),
        ]
    },
    "hmi_center_cyl_dress.png": {
        "callouts": [
            ([6, 72, 360, 186], "bot_l", "外圆轮 U/Z 坐标、累计修整量与外圆斜修整偏转补偿角（支持锥度微调）"),
            ([392, 72, 692, 346], "out_l", "外圆砂轮状态（新/旧）、粗修/精修次数·余量·速度及修整起止点 Z"),
            ([392, 352, 676, 524], "out_l", "新/当前外圆砂轮直径、砂轮线速度/转速及当前/初始修整接触 U"),
        ]
    },
    "hmi_center_step1.png": {
        "callouts": [
            ([4, 72, 249, 386], "bot_r", "外圆台阶一使能、初始接触模式、距左端面、起点/终点 Z 与当前/初始接触 U"),
            ([254, 86, 693, 464], "bot_r", "台阶磨削独立工艺表：单段/保持分段策略、往复方式与粗/精磨切深及转速"),
            (vs_rect(5, 6), "vleft", "VS5 台阶一 / VS6 台阶二：支持双台阶轴肩连续自动磨削"),
        ]
    },
    "hmi_center_endface.png": {
        "callouts": [
            ([6, 74, 694, 324], "bot_l", "左/右端面独立参数卡：耳高/壁厚、磨削起点/终点 X、初始/当前接触 Z 与补偿"),
            (vs_rect(2, 3), "vleft", "端面分支跳转：VS2 端面工艺参数(4列) / VS3 端面砂轮修整(双向联动)"),
        ]
    },
    "hmi_center_end_process.png": {
        "callouts": [
            ([32, 72, 688, 124], "out_l", "左/右端面累计及设定磨削量、已加工与修整设定独立监控"),
            ([28, 128, 674, 464], "bot_r", "左/右端面各自独立的粗/精磨工艺表（4列独立设定进刀、方式、速度与转速）"),
        ]
    },
    "hmi_center_end_dress.png": {
        "callouts": [
            ([404, 72, 692, 346], "out_l", "端面砂轮修整参数（U(X) 向起终点、粗/精修余量与速度，支持左/右翼修整）"),
            ([404, 352, 680, 474], "out_l", "外圆-端面修整坐标双向联动与当前/初始修整接触 Z 显示"),
        ]
    },
}


def build_sheet(paths, dest_path, cols=4, tw=360):
    thumbs = []
    font = font_r(12)
    for p in paths:
        im = Image.open(p).convert("RGB")
        th = int(round(tw * im.height / im.width))
        thumbs.append((os.path.basename(p), im.resize((tw, th), Image.Resampling.LANCZOS), th))
    max_h = max(t[2] for t in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 10, rows * (max_h + 26) + 10), (24, 28, 36))
    dr = ImageDraw.Draw(sheet)
    for i, (name, im, _) in enumerate(thumbs):
        r, c = divmod(i, cols)
        x = 10 + c * (tw + 10)
        y = 10 + r * (max_h + 26)
        sheet.paste(im, (x, y))
        dr.text((x + 4, y + max_h + 4), name, fill=(240, 245, 255), font=font)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    sheet.save(dest_path)
    print(f"Saved contact sheet: {dest_path}")


def main():
    creator_out = []
    for name, callouts in CREATOR_SPECS.items():
        src = os.path.join(RAW_CREATOR, name)
        dst = os.path.join(MANUAL_DIR, "images", name)
        assert os.path.exists(src), f"Missing raw creator file: {src}"
        annotate_image(src, dst, callouts)
        creator_out.append(dst)
    print(f"Annotated {len(creator_out)} Creator screenshots.")

    hmi_out = []
    for name, spec in HMI_SPECS.items():
        override_src = os.path.join(RAW_OVERRIDES, name)
        src = override_src if os.path.exists(override_src) else os.path.join(RAW_HMI, name)
        dst = os.path.join(MANUAL_DIR, "images", "sinutrain", name)
        assert os.path.exists(src), f"Missing raw HMI file: {src}"
        annotate_image(src, dst, spec["callouts"], erase_rects=spec.get("erase"))
        hmi_out.append(dst)
    print(f"Annotated {len(hmi_out)} SinuTrain HMI screenshots.")

    build_sheet(creator_out, os.path.join(CUR_SCRATCH, "_contact_annotated_creator.png"), cols=4)
    build_sheet(hmi_out, os.path.join(CUR_SCRATCH, "_contact_annotated_hmi.png"), cols=4)


if __name__ == "__main__":
    main()
