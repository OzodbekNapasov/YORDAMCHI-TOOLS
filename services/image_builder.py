# ============================================================
#  services/image_builder.py
#  Sizning asl Word shablonlaringizni 100% o'z holida
#  Ultra HD (300 DPI A4) formatida yaratuvchi universal renderer
# ============================================================

import os
import io
from PIL import Image, ImageDraw, ImageFont

try:
    from docbot_config import find_template_file
except ImportError:
    from config import find_template_file


def _get_font(font_type: str = "reg", px_size: int = 58):
    """Times New Roman shriftini loyiha papkasidan yoki tizimdan yuklash"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fonts_dir = os.path.join(base_dir, "fonts")

    if font_type == "bold":
        filenames = ["timesbd.ttf", "TimesNewRomanBold.ttf", "FreeSerifBold.ttf", "AppBoldFont.ttf"]
    elif font_type == "italic":
        filenames = ["timesi.ttf", "TimesNewRomanItalic.ttf", "FreeSerifItalic.ttf"]
    else:
        filenames = ["times.ttf", "TimesNewRoman.ttf", "FreeSerif.ttf"]

    for fn in filenames:
        candidates = [
            os.path.join(fonts_dir, fn),
            os.path.join(base_dir, "templates", "fonts", fn),
            os.path.join(r"C:\Windows\Fonts", fn),
            f"/usr/share/fonts/truetype/msttcorefonts/{fn}",
            f"/usr/share/fonts/truetype/freefont/{fn}",
        ]
        for p in candidates:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, px_size)
                except Exception:
                    pass

    return ImageFont.load_default(size=px_size)


def _render_qabul_1_kurs(data: dict, draw: ImageDraw.ImageDraw, img: Image.Image, f_reg, f_bold) -> int:
    """1-kursga qabul ma'lumotnomasi matnini chizish"""
    left_x = 355
    right_x = 2300
    content_w = right_x - left_x
    tab_indent_x = 503  # 1 abzas / Tab surilishi (1.25 cm)

    # 1. Kirish gapi (Abzas / Tab bilan boshlanib, o'ng tomongacha to'lib turishi)
    draw.rectangle([(0, 1350), (img.width, 1490)], fill=(255, 255, 255))
    intro_words = ["Ushbu", "ma’lumotnoma", "shuni", "tasdiqlaydiki,", "haqiqatdan", "ham"]
    intro_w = right_x - tab_indent_x
    words_w = sum(f_reg.getbbox(w)[2] - f_reg.getbbox(w)[0] for w in intro_words)
    gaps = len(intro_words) - 1
    gap_px = (intro_w - words_w) / gaps

    cur_x = float(tab_indent_x)
    intro_y = 1406
    for w in intro_words:
        draw.text((int(round(cur_x)), intro_y), w, fill=(0, 0, 0), font=f_reg)
        w_px = f_reg.getbbox(w)[2] - f_reg.getbbox(w)[0]
        cur_x += w_px + gap_px

    # 2. Dinamik Asosiy Matn (X: 355 dan 2300 gacha, Y=1541)
    fio = str(data.get("FIO", "")).strip()
    oquv_yili = str(data.get("OQUV_YILI", "2026/2027")).strip()
    yonalish = str(data.get("YONALISH", "")).strip()
    boshlash_yili = oquv_yili.split("/")[0] if "/" in oquv_yili else "2026"

    start_y = 1541
    line_h = 134

    tokens = []
    for w in fio.split():
        tokens.append((w, True))
    tokens.append((f"{oquv_yili}-o‘quv", False))
    tokens.append(("yilida", False))
    for w in yonalish.split():
        tokens.append((w, True))
    tokens.append(("yo‘nalishiga", False))
    tokens.append(("shartnoma", False))

    rest_phrase = f"asosida o‘qishga qabul qilindi. Talaba o‘qishni {boshlash_yili}-yil sentyabr oyidan boshlaydi."
    for w in rest_phrase.split():
        tokens.append((w, False))

    lines = []
    cur_line = []
    cur_w = 0
    space_w = f_reg.getbbox(" ")[2] - f_reg.getbbox(" ")[0]

    for word, is_bold in tokens:
        fnt = f_bold if is_bold else f_reg
        bb = fnt.getbbox(word)
        w_px = bb[2] - bb[0]

        max_w = (content_w - (tab_indent_x - left_x)) if not lines else content_w
        test_w = cur_w + (space_w if cur_line else 0) + w_px

        if test_w > max_w and cur_line:
            lines.append((cur_line, len(lines) == 0))
            cur_line = [(word, is_bold, w_px)]
            cur_w = w_px
        else:
            cur_line.append((word, is_bold, w_px))
            cur_w = test_w

    if cur_line:
        lines.append((cur_line, len(lines) == 0))

    cur_y = start_y
    for line_idx, (line, is_first_line) in enumerate(lines):
        is_last_line = (line_idx == len(lines) - 1)
        tot_w = sum(w for _, _, w in line)
        gaps = len(line) - 1
        line_start_x = tab_indent_x if is_first_line else left_x
        line_max_w = (right_x - tab_indent_x) if is_first_line else content_w

        if not is_last_line and gaps > 0:
            gap_px = (line_max_w - tot_w) / gaps
        else:
            gap_px = float(space_w)

        cur_x = float(line_start_x)
        for word, is_bold, w_px in line:
            fnt = f_bold if is_bold else f_reg
            draw.text((int(round(cur_x)), cur_y), word, fill=(0, 0, 0), font=fnt)
            cur_x += w_px + gap_px

        cur_y += line_h

    cur_y += 50
    return cur_y


def _render_oqiyapti(data: dict, draw: ImageDraw.ImageDraw, img: Image.Image, f_reg, f_bold) -> int:
    """O'qiyotganligi haqidagi ma'lumotnoma matnini chizish"""
    left_x = 355
    right_x = 2300
    content_w = right_x - left_x
    tab_indent_x = 503  # 1 abzas / Tab surilishi (1.25 cm)

    # 1. Kirish gapi (Abzas / Tab bilan boshlanib, o'ng tomongacha to'lib turishi)
    draw.rectangle([(0, 1350), (img.width, 1490)], fill=(255, 255, 255))
    intro_words = ["Ushbu", "ma’lumotnoma", "shuni", "tasdiqlaydiki,", "haqiqatdan", "ham"]
    intro_w = right_x - tab_indent_x
    words_w = sum(f_reg.getbbox(w)[2] - f_reg.getbbox(w)[0] for w in intro_words)
    gaps = len(intro_words) - 1
    gap_px = (intro_w - words_w) / gaps

    cur_x = float(tab_indent_x)
    intro_y = 1406
    for w in intro_words:
        draw.text((int(round(cur_x)), intro_y), w, fill=(0, 0, 0), font=f_reg)
        w_px = f_reg.getbbox(w)[2] - f_reg.getbbox(w)[0]
        cur_x += w_px + gap_px

    # 2. Dinamik Asosiy Matn (X: 355 dan 2300 gacha, Y=1541)
    fio = str(data.get("FIO", "")).strip()
    oquv_yili = str(data.get("OQUV_YILI", "2025/2026")).strip()
    yonalish = str(data.get("YONALISH", "")).strip()
    kurs = str(data.get("KURSI", "1")).strip()
    guruh = str(data.get("GURUHI", "")).strip()

    start_y = 1541
    line_h = 134

    tokens = []
    for w in fio.split():
        tokens.append((w, True))
    tokens.append((f"{oquv_yili}-o‘quv", False))
    tokens.append(("yilida", False))
    for w in yonalish.split():
        tokens.append((w, True))
    tokens.append(("yo‘nalishiga", False))
    tokens.append(("to‘lov-shartnoma", False))
    tokens.append(("asosida", False))
    tokens.append(("o‘qishga", False))
    tokens.append(("qabul", False))
    tokens.append(("qilingan.", False))
    tokens.append(("Hozirgi", False))
    tokens.append(("kunda", False))
    tokens.append((f"{kurs}-bosqich", False))
    tokens.append((f"{guruh}-guruhda", True))
    tokens.append(("taxsil", False))
    tokens.append(("olmoqda.", False))

    lines = []
    cur_line = []
    cur_w = 0
    space_w = f_reg.getbbox(" ")[2] - f_reg.getbbox(" ")[0]

    for word, is_bold in tokens:
        fnt = f_bold if is_bold else f_reg
        bb = fnt.getbbox(word)
        w_px = bb[2] - bb[0]

        max_w = (content_w - (tab_indent_x - left_x)) if not lines else content_w
        test_w = cur_w + (space_w if cur_line else 0) + w_px

        if test_w > max_w and cur_line:
            lines.append((cur_line, len(lines) == 0))
            cur_line = [(word, is_bold, w_px)]
            cur_w = w_px
        else:
            cur_line.append((word, is_bold, w_px))
            cur_w = test_w

    if cur_line:
        lines.append((cur_line, len(lines) == 0))

    cur_y = start_y
    for line_idx, (line, is_first_line) in enumerate(lines):
        is_last_line = (line_idx == len(lines) - 1)
        tot_w = sum(w for _, _, w in line)
        gaps = len(line) - 1
        line_start_x = tab_indent_x if is_first_line else left_x
        line_max_w = (right_x - tab_indent_x) if is_first_line else content_w

        if not is_last_line and gaps > 0:
            gap_px = (line_max_w - tot_w) / gaps
        else:
            gap_px = float(space_w)

        cur_x = float(line_start_x)
        for word, is_bold, w_px in line:
            fnt = f_bold if is_bold else f_reg
            draw.text((int(round(cur_x)), cur_y), word, fill=(0, 0, 0), font=fnt)
            cur_x += w_px + gap_px

        cur_y += line_h

    cur_y += 50
    return cur_y


def _render_buyruq(template_filename: str, data: dict, output_png_path: str) -> bool:
    """4 turdagi rasmiy buyruqlar Ultra HD (300 DPI A4) renderer"""
    img = Image.new("RGB", (2481, 3508), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_reg = _get_font("reg", 46)
    f_bold = _get_font("bold", 46)
    f_italic = _get_font("italic", 46)
    f_bold_italic = _get_font("bold", 48)
    f_hdr = _get_font("bold", 32)
    f_title = _get_font("bold", 42)

    left_margin = 250
    right_margin = 2231
    content_w = right_margin - left_margin
    tab_indent_x = 390  # 1.25 cm

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 1. HEADER (Bilingual + Emblem)
    hdr_y = 180
    logo_path = os.path.join(base_dir, "templates", "stamps", "buyruq_image1.png")
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path).convert("RGBA")
        logo_w, logo_h = logo_img.size
        target_w = 260
        target_h = int(logo_h * (target_w / logo_w))
        logo_resized = logo_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        logo_x = (2481 - target_w) // 2
        img.paste(logo_resized, (logo_x, hdr_y + 10), logo_resized if "A" in logo_resized.getbands() else None)

    # Left Uzbek Header
    uz_lines = [
        "O’ZBEKISTON RESPUBLIKASI",
        "QASHQADARYO VILOYATI",
        "“QARSHI TIBBIYOT TEXNIKUMI”",
        "NODAVLAT TA’LIM MUASSASASI"
    ]
    cur_hy = hdr_y
    for l in uz_lines:
        draw.text((left_margin, cur_hy), l, fill=(0, 0, 0), font=f_hdr)
        cur_hy += 52

    # Right Russian Header
    ru_lines = [
        "РЕСПУБЛИКА УЗБЕКИСТАН",
        "КАШКАДАРЬИНСКАЯ ОБЛАСТЬ",
        "НЕГОСУДАРСТВЕННОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ",
        "«КАРSHИНСКИЙ МЕДИЦИНСКИЙ ТЕХНИКУМ»"
    ]
    cur_hy = hdr_y
    for l in ru_lines:
        bb = f_hdr.getbbox(l)
        tw = bb[2] - bb[0]
        draw.text((right_margin - tw, cur_hy), l, fill=(0, 0, 0), font=f_hdr)
        cur_hy += 52

    # 2. TITLE BOX
    fn_lower = template_filename.lower()
    title_text = "Akademik ta’til berish to‘g‘risida"
    if "qayta_tiklash" in fn_lower or "tiklash" in fn_lower:
        title_text = "Akademik ta’til (o‘z kursida qolgan) o‘quvchini\no‘quvchilar safiga tiklash to‘g‘risida"
    elif "guruhdan" in fn_lower or "otkazish" in fn_lower or "o`tkazish" in fn_lower:
        title_text = "O‘quvchini guruhdan guruhga o’tkazish to‘g‘risida"
    elif "chiqarish" in fn_lower or "safidan" in fn_lower:
        title_text = "O‘quvchini o‘quvchilar safidan chiqarish to‘g‘risida"

    box_y = 480
    box_lines = title_text.split("\n")
    box_h = 100 + (len(box_lines) - 1) * 60
    draw.rectangle([(left_margin, box_y), (right_margin, box_y + box_h)], outline=(0, 0, 0), width=3)

    for i, bl in enumerate(box_lines):
        bb = f_title.getbbox(bl)
        tw = bb[2] - bb[0]
        tx = left_margin + (content_w - tw) // 2
        ty = box_y + 25 + i * 60
        draw.text((tx, ty), bl, fill=(0, 0, 0), font=f_title)

    # 3. BUYRUQ NUMBER AND DATE
    b_num = str(data.get("buyruq_raqami", "14-B")).strip()
    b_sana = str(data.get("sanasi") or data.get("SANA") or "14.08.2026").strip()
    num_y = box_y + box_h + 80

    draw.text((left_margin, num_y), f"BUYRUQ №  {b_num}_", fill=(0, 0, 0), font=f_bold_italic)

    bb_d = f_reg.getbbox(f"{b_sana}yil.")
    w_d = bb_d[2] - bb_d[0]
    draw.text((left_margin, num_y + 70), "Qarshi sh.", fill=(0, 0, 0), font=f_reg)
    draw.text((right_margin - w_d, num_y + 70), f"{b_sana}yil.", fill=(0, 0, 0), font=f_reg)

    # 4. PREAMBLE (Justified)
    preamble = "O‘zbekiston Respublikasi Vazirlar Mahkamasining 2020 yil 7-avgustdagi “O‘zbekiston Respublikasida uzluksiz boshlang‘ich, o‘rta va o‘rta maxsus professional ta’lim tizimini tartibga soluvchi normativ-huquqiy hujjatlarni tasdiqlash to‘g‘risida”gi 466-son qarori 1-ilovasi bilan tasdiqlangan “O‘zbekiston Respublikasida uzluksiz boshlang‘ich, o‘rta va o‘rta maxsus professional ta’lim to‘g‘risida” NIZOMga asosan"

    def draw_justified_paragraph(text, start_y, is_tab_indent=False, line_spacing=68):
        words = text.split()
        lines = []
        cur_line = []
        cur_w = 0
        space_w = f_reg.getbbox(" ")[2] - f_reg.getbbox(" ")[0]

        for w in words:
            bb = f_reg.getbbox(w)
            w_px = bb[2] - bb[0]
            max_w = (content_w - (tab_indent_x - left_margin)) if (not lines and is_tab_indent) else content_w
            test_w = cur_w + (space_w if cur_line else 0) + w_px
            if test_w > max_w and cur_line:
                lines.append((cur_line, len(lines) == 0 and is_tab_indent))
                cur_line = [(w, w_px)]
                cur_w = w_px
            else:
                cur_line.append((w, w_px))
                cur_w = test_w

        if cur_line:
            lines.append((cur_line, len(lines) == 0 and is_tab_indent))

        cur_y = start_y
        for line_idx, (line, has_tab) in enumerate(lines):
            is_last = (line_idx == len(lines) - 1)
            tot_w = sum(w for _, w in line)
            gaps = len(line) - 1
            line_start_x = tab_indent_x if has_tab else left_margin
            line_max_w = (right_margin - tab_indent_x) if has_tab else content_w

            gap_px = (line_max_w - tot_w) / gaps if (not is_last and gaps > 0) else float(space_w)
            cur_x = float(line_start_x)
            for word, w_px in line:
                draw.text((int(round(cur_x)), cur_y), word, fill=(0, 0, 0), font=f_reg)
                cur_x += w_px + gap_px
            cur_y += line_spacing

        return cur_y

    cur_y = draw_justified_paragraph(preamble, num_y + 160, is_tab_indent=False)

    # 5. BUYURAMAN:
    cur_y += 35
    bb_b = f_bold.getbbox("BUYURAMAN:")
    tw_b = bb_b[2] - bb_b[0]
    draw.text((left_margin + (content_w - tw_b) // 2, cur_y), "BUYURAMAN:", fill=(0, 0, 0), font=f_bold)
    cur_y += 85

    # 6. DECISION PARAGRAPH
    ifo = str(data.get("IFO") or data.get("FIO") or "").strip()
    kurs = str(data.get("kursi", "1")).strip()
    guruhi = str(data.get("guruhi") or data.get("avvalgi_guruhi") or "").strip()
    yangi_guruh = str(data.get("yangi_guruhi", "")).strip()
    yonalish = str(data.get("yonalishi", "")).strip()

    def draw_token_paragraph(tokens, start_y, is_tab_indent=True, line_spacing=68):
        lines = []
        cur_line = []
        cur_w = 0
        space_w = f_reg.getbbox(" ")[2] - f_reg.getbbox(" ")[0]

        for w, is_bold, is_it in tokens:
            fnt = f_bold if is_bold else (f_italic if is_it else f_reg)
            bb = fnt.getbbox(w)
            w_px = bb[2] - bb[0]
            max_w = (content_w - (tab_indent_x - left_margin)) if (not lines and is_tab_indent) else content_w
            test_w = cur_w + (space_w if cur_line else 0) + w_px
            if test_w > max_w and cur_line:
                lines.append((cur_line, len(lines) == 0 and is_tab_indent))
                cur_line = [(w, is_bold, is_it, w_px)]
                cur_w = w_px
            else:
                cur_line.append((w, is_bold, is_it, w_px))
                cur_w = test_w

        if cur_line:
            lines.append((cur_line, len(lines) == 0 and is_tab_indent))

        cur_y = start_y
        for line_idx, (line, has_tab) in enumerate(lines):
            is_last = (line_idx == len(lines) - 1)
            tot_w = sum(w for _, _, _, w in line)
            gaps = len(line) - 1
            line_start_x = tab_indent_x if has_tab else left_margin
            line_max_w = (right_margin - tab_indent_x) if has_tab else content_w

            gap_px = (line_max_w - tot_w) / gaps if (not is_last and gaps > 0) else float(space_w)
            cur_x = float(line_start_x)
            for word, is_b, is_i, w_px in line:
                fnt = f_bold if is_b else (f_italic if is_i else f_reg)
                draw.text((int(round(cur_x)), cur_y), word, fill=(0, 0, 0), font=fnt)
                cur_x += w_px + gap_px
            cur_y += line_spacing

        return cur_y

    if "akademik ta'til berish" in fn_lower or "akademik_tatil" in fn_lower:
        dec_tokens = [
            ("“O‘zbekiston", False, False), ("Respublikasida", False, False), ("uzluksiz", False, False),
            ("boshlang‘ich,", False, False), ("o‘rta", False, False), ("va", False, False), ("o‘rta", False, False),
            ("maxsus", False, False), ("professional", False, False), ("ta’lim", False, False),
            ("to‘g‘risida”", False, False), ("NIZOMga", False, False), ("asosan", False, False),
            (f"{kurs}-bosqich", False, False), (f"{guruhi}-guruh", True, False), ("talabasi", False, False)
        ]
        for w in ifo.split():
            dec_tokens.append((w, True, False))
        dec_tokens.extend([("ga", True, False), ("akademik", False, False), ("ta`til", False, False), ("berilsin.", False, False)])
        cur_y = draw_token_paragraph(dec_tokens, cur_y)

    elif "qayta_tiklash" in fn_lower or "tiklash" in fn_lower:
        avv_num = str(data.get("avvalgi_buyruq_raqami", "14-B")).strip()
        avv_sana = str(data.get("avvalgi_buyruq_sanasi", "10.02.2025")).strip()
        dec_tokens = [
            ("“O‘zbekiston", False, False), ("Respublikasida", False, False), ("uzluksiz", False, False),
            ("boshlang‘ich,", False, False), ("o‘rta", False, False), ("va", False, False), ("o‘rta", False, False),
            ("maxsus", False, False), ("professional", False, False), ("ta’lim", False, False),
            ("to‘g‘risida”", False, False), ("NIZOMga", False, False), ("asosan", False, False),
            ("texnikum", False, False), ("direktorining", False, False), (f"{avv_sana}", True, False),
            ("yil-dagi", False, False), (f"{avv_num}-sonli", True, False), ("buyrug`i", False, False),
            ("bilan", False, False), ("akademik", False, False), ("ta`til", False, False), ("berilgan", False, False),
            (f"{kurs}-bosqich", False, False), (f"{guruhi}-guruh", True, False), ("talabasi", False, False)
        ]
        for w in ifo.split():
            dec_tokens.append((w, True, False))
        dec_tokens.extend([
            ("ni", True, False), (f"{kurs}-bosqich", False, False), (f"{yangi_guruh}-guruhga", True, False),
            ("o’quv", False, False), ("jarayonlarini", False, False), ("davom", False, False),
            ("ettirishi", False, False), ("uchun", False, False), ("tiklansin.", False, False)
        ])
        cur_y = draw_token_paragraph(dec_tokens, cur_y)

    elif "guruhdan" in fn_lower or "otkazish" in fn_lower or "o`tkazish" in fn_lower:
        dec_tokens = [
            ("Ta`lim", False, False), ("yo`nalishi", False, False), ("va", False, False), ("o`quv", False, False),
            ("jarayoni", False, False), ("bir", False, False), ("xil", False, False), ("bo`lganligi", False, False),
            ("sababli", False, False), (f"{yonalish}", True, False), ("yo‘nalishining", False, False),
            ("quyidagi", False, False), ("o‘quvchilari", False, False), ("guruhdan-guruhga", False, False),
            ("o‘tkazilsin:", False, False)
        ]
        cur_y = draw_token_paragraph(dec_tokens, cur_y)

        # Draw Table
        cur_y += 30
        tbl_top = cur_y
        col_w = [180, 1000, 801]
        tbl_h = 170
        draw.rectangle([(left_margin, tbl_top), (right_margin, tbl_top + tbl_h)], outline=(0, 0, 0), width=2)
        draw.line([(left_margin + col_w[0], tbl_top), (left_margin + col_w[0], tbl_top + tbl_h)], fill=(0, 0, 0), width=2)
        draw.line([(left_margin + col_w[0] + col_w[1], tbl_top), (left_margin + col_w[0] + col_w[1], tbl_top + tbl_h)], fill=(0, 0, 0), width=2)
        draw.line([(left_margin, tbl_top + 75), (right_margin, tbl_top + 75)], fill=(0, 0, 0), width=2)

        draw.text((left_margin + 45, tbl_top + 15), "T/R", font=f_bold, fill=(0, 0, 0))
        draw.text((left_margin + col_w[0] + 180, tbl_top + 15), "O'quvchilarning I.F.Sh", font=f_bold, fill=(0, 0, 0))
        draw.text((left_margin + col_w[0] + col_w[1] + 160, tbl_top + 15), "Guruhdan almasishi", font=f_bold, fill=(0, 0, 0))

        draw.text((left_margin + 70, tbl_top + 95), "1", font=f_reg, fill=(0, 0, 0))
        draw.text((left_margin + col_w[0] + 40, tbl_top + 95), ifo, font=f_bold, fill=(0, 0, 0))
        transfer_str = f"{guruhi}guruhdan  {yangi_guruh}guruhga"
        draw.text((left_margin + col_w[0] + col_w[1] + 40, tbl_top + 95), transfer_str, font=f_reg, fill=(0, 0, 0))
        cur_y = tbl_top + tbl_h + 40

    else:
        # safidan chiqarish
        dec_tokens = [
            ("“O‘zbekiston", False, False), ("Respublikasida", False, False), ("uzluksiz", False, False),
            ("boshlang‘ich,", False, False), ("o‘rta", False, False), ("va", False, False), ("o‘rta", False, False),
            ("maxsus", False, False), ("professional", False, False), ("ta’lim", False, False),
            ("to‘g‘risida”", False, False), ("NIZOM", False, False), ("va", False, False),
            ("texnikum", False, False), ("ichki", False, False), ("tartib", False, False),
            ("qoidalariga", False, False), ("amal", False, False), ("qilmagan", False, False),
            (f"{kurs}-bosqich", False, False), (f"{guruhi}-guruh", True, False), ("talabasi", False, False)
        ]
        for w in ifo.split():
            dec_tokens.append((w, True, False))
        dec_tokens.extend([
            ("ni", True, False), ("o’quvchilar", False, False), ("safidan", False, False),
            ("chiqarilsin.", False, False)
        ])
        cur_y = draw_token_paragraph(dec_tokens, cur_y)

    # 7. SUB-PARAGRAPHS
    cur_y += 30
    sub_p1 = "Ushbu buyruq bilan O`IBDO`, KTBDO`, MMIBDO` hamda guruh rahbarlari tanishtirilsin." if ("chiqarish" in fn_lower or "safidan" in fn_lower) else "Ushbu buyruq bilan O`IBDO` hamda guruh rahbarlari tanishtirilsin."
    cur_y = draw_justified_paragraph(sub_p1, cur_y, is_tab_indent=False) + 20

    sub_p2 = "1 kun muddatda prof-emis.edu.uz platformasi administratoriga taqdim etilsin."
    cur_y = draw_justified_paragraph(sub_p2, cur_y, is_tab_indent=False) + 20

    sub_p3 = "Ushbu buyruq ijrosini taminlashni o`z  zimmamda qoldiraman."
    cur_y = draw_justified_paragraph(sub_p3, cur_y, is_tab_indent=False) + 35

    # 8. ASOS (Italic)
    asos_text = f"Asos: {ifo}ning arizasi va direktorning roziligi."
    if "chiqarish" in fn_lower or "safidan" in fn_lower:
        asos_turi = str(data.get("asos_turi", "Talaba arizasi")).strip()
        if "bildirgi" in asos_turi.lower() or "rahbar" in asos_turi.lower():
            asos_text = "Asos: Guruh rahbarining bildirgisi va ogohlantirish xatlari."
        else:
            asos_text = f"Asos: {ifo}ning arizasi va direktorning roziligi."
    elif "guruhdan" in fn_lower or "otkazish" in fn_lower or "o`tkazish" in fn_lower:
        asos_text = "Asos: Talabalarning arizasi va O`IBDO`ning roziligi."

    draw.text((tab_indent_x, cur_y), asos_text, fill=(0, 0, 0), font=f_italic)
    cur_y += 120

    # 9. FOOTER (DIRECTOR + STAMP)
    footer_banner_png = os.path.join(base_dir, "templates", "stamps", "word_footer_banner.png")
    footer_y = max(cur_y + 80, 2900)
    if os.path.exists(footer_banner_png):
        foot_img = Image.open(footer_banner_png).convert("RGBA")
        img.paste(foot_img, (445, footer_y), foot_img if "A" in foot_img.getbands() else None)

    img.save(output_png_path, "PNG", quality=100)
    return True


def render_docx_template_to_image(
    template_filename: str,
    output_png_path: str,
    data: dict,
    temp_dir: str = ""
) -> bool:
    """
    Sizning asl Word shabloningizni (Ma'lumotnoma yoki Buyruq) 100% asl dizaynda
    (300 DPI A4 Ultra HD rasm) shaklida yaratadi.
    """
    try:
        fn_lower = template_filename.lower()

        # Buyruqlar uchun maxsus renderer
        if "buyruq" in fn_lower or "tatil" in fn_lower or "tiklash" in fn_lower or "chiqarish" in fn_lower or "otkazish" in fn_lower or "o`tkazish" in fn_lower or "buyruq_raqami" in data:
            return _render_buyruq(template_filename, data, output_png_path)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 1. Asl Worddan olingan mukammal Yuqori andoza (Shapka, Chiziq, Qarshi shahri, MA'LUMOTNOMA)
        top_base_png = os.path.join(base_dir, "templates", "malumotnoma_top_base.png")
        footer_banner_png = os.path.join(base_dir, "templates", "stamps", "word_footer_banner.png")

        if os.path.exists(top_base_png):
            img = Image.open(top_base_png).convert("RGB")
        else:
            img = Image.new("RGB", (2481, 3508), color=(255, 255, 255))

        draw = ImageDraw.Draw(img)

        f_reg = _get_font("reg", 58)
        f_bold = _get_font("bold", 58)
        f_italic = _get_font("italic", 58)

        # 2. Sana: O'ng tomonga tekislangan (X=2339, Y=801)
        sana = str(data.get("SANA") or data.get("sanasi") or "14.08.2026").strip()
        sana_text = f"{sana} y." if not (sana.endswith("y.") or sana.endswith("y")) else sana
        bb = f_reg.getbbox(sana_text)
        tw = bb[2] - bb[0]
        draw.text((2339 - tw, 801), sana_text, fill=(0, 0, 0), font=f_reg)

        # 3. Shablon turiga qarab tegishli rendererni chaqirish
        if "o'qiyapti" in fn_lower or "oqiyapti" in fn_lower or "GURUHI" in data:
            cur_y = _render_oqiyapti(data, draw, img, f_reg, f_bold)
        else:
            cur_y = _render_qabul_1_kurs(data, draw, img, f_reg, f_bold)

        # 4. Izoh (Chap tomondan, 1 abzas surilgan X=503)
        tab_indent_x = 503
        note_str = "Ma’lumotnoma so‘ralgan joyga taqdim etish uchun berildi"
        draw.text((tab_indent_x, cur_y), note_str, fill=(0, 0, 0), font=f_italic)

        # 5. Footer (Asl Pechat, Muhr, Imzo va Sh.Raxmonov bloki)
        footer_y = max(cur_y + 265, 2208)
        if os.path.exists(footer_banner_png):
            foot_img = Image.open(footer_banner_png).convert("RGBA")
            img.paste(foot_img, (445, footer_y), foot_img if "A" in foot_img.getbands() else None)

        img.save(output_png_path, "PNG", quality=100)
        return True

    except Exception as e:
        print(f"Render error: {e}")
        return False
