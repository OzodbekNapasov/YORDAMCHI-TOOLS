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

    if font_type == "bolditalic":
        filenames = ["timesbi.ttf", "TimesNewRomanBoldItalic.ttf", "FreeSerifBoldItalic.ttf",
                     "timesbd.ttf", "TimesNewRomanBold.ttf"]
    elif font_type == "bold":
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


# ============================================================
#  BUYRUQ RENDERI — o'lchamlar Word etalonidan olingan (300 DPI A4)
#
#  Etalon qanday olingan: shablon Word (COM) orqali PDF ga o'girilib,
#  PyMuPDF bilan har bir matn bo'lagining x/y/pt qiymati o'lchangan.
#  Quyidagi raqamlar — o'sha o'lchovlar, taxmin emas.
# ============================================================

# Sahifa va chetlar (300 DPI: 1cm = 118.11px, 1pt = 4.167px)
_PG_W, _PG_H = 2481, 3508
_LEFT, _RIGHT = 355, 2340          # docx: chap 3.00cm, o'ng 1.25cm
_CONTENT_W = _RIGHT - _LEFT        # 1985 px

# Shrift o'lchamlari (docx dagi punktlardan)
_SZ_BODY = 58                      # 14 pt — asosiy matn
_SZ_HDR = 42                       # 10 pt — yuqoridagi ikki tilli sarlavha
_SZ_ORDER = 67                     # 16 pt — "BUYRUQ №"

_LINE_H = 67                       # qatorlar orasi
_PARA_GAP = 49                     # xatboshilar orasidagi qo'shimcha bo'shliq
_IND_PRE = 118                     # 1.00 cm — muqaddima xatboshisi
_IND_ITEM = 125                    # 1.06 cm — ro'yxat bandlari

# Aniq o'lchangan vertikal joylar
_Y_HDR = 203                       # sarlavha birinchi qatori
_HDR_STEP = 48
_X_HDR_L, _X_HDR_R = 700, 1940     # chap va o'ng katak markazlari
_EMB_X, _EMB_Y, _EMB_W = 1112, 201, 345   # gerb
_Y_RULE = 650                      # sarlavha ostidagi gorizontal chiziq
_Y_ORDER = 700                     # BUYRUQ №
_Y_CITY = 776                      # "Qarshi sh." va sana
_X_DATE = 1855                     # sana tab to'xtash joyi
_Y_TITLE = 921                     # hujjat sarlavhasi
_X_CENTER = 1410                   # markazlashtirilgan matnlar markazi
_Y_BODY = 999                      # muqaddima boshlanishi


def _render_buyruq(template_filename: str, data: dict, output_png_path: str) -> bool:
    """Rasmiy buyruqlarni Word shablonining aynan o'zidek chizadi (300 DPI A4)"""
    img = Image.new("RGB", (_PG_W, _PG_H), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    F = {
        "reg": _get_font("reg", _SZ_BODY),
        "bold": _get_font("bold", _SZ_BODY),
        "italic": _get_font("italic", _SZ_BODY),
        "bolditalic": _get_font("bolditalic", _SZ_BODY),
    }
    f_hdr = _get_font("bold", _SZ_HDR)
    f_order = _get_font("bolditalic", _SZ_ORDER)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fn_lower = template_filename.lower()

    def tw(text, font):
        bb = font.getbbox(text)
        return bb[2] - bb[0]

    def draw_centered(text, y, font, center_x=_X_CENTER):
        draw.text((int(center_x - tw(text, font) / 2), y), text, fill=(0, 0, 0), font=font)

    # ---------- 1. Ikki tilli sarlavha ----------
    # Word kataklar ichida matnni markazga tekislaydi va o'z-o'zidan o'raydi
    uz_lines = [
        "O’ZBEKISTON RESPUBLIKASI", "QASHQADARYO VILOYATI",
        "“QARSHI TIBBIYOT", "TEXNIKUMI”",
        "NODAVLAT TA’LIM", "MUASSASASI",
    ]
    ru_lines = [
        "РЕСПУБЛИКА УЗБЕКИСТАН",
        "КАШКАДАРЬИНСКАЯ ОБЛАСТЬ",
        "НЕГОСУДАРСТВЕННОЕ",
        "ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ",
        "«КАРШИНСКИЙ МЕДИЦИНСКИЙ",
        "ТЕХНИКУМ»",
    ]
    for i, line in enumerate(uz_lines):
        draw_centered(line, _Y_HDR + i * _HDR_STEP, f_hdr, _X_HDR_L)
    for i, line in enumerate(ru_lines):
        draw_centered(line, _Y_HDR + i * _HDR_STEP, f_hdr, _X_HDR_R)

    # Gerb
    logo_path = os.path.join(base_dir, "templates", "stamps", "buyruq_image1.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        h = int(logo.size[1] * (_EMB_W / logo.size[0]))
        logo = logo.resize((_EMB_W, h), Image.Resampling.LANCZOS)
        img.paste(logo, (_EMB_X, _EMB_Y), logo)

    # Sarlavha ostidagi chiziq
    draw.rectangle([(349, _Y_RULE), (_RIGHT, _Y_RULE + 5)], fill=(0, 0, 0))

    # ---------- 2. BUYRUQ raqami, shahar va sana ----------
    b_num = str(data.get("buyruq_raqami", "")).strip()
    b_sana = str(data.get("sanasi") or data.get("SANA") or "").strip()
    draw_centered(f"BUYRUQ №  {b_num}_", _Y_ORDER, f_order, (_LEFT + _RIGHT) // 2)
    draw.text((_LEFT, _Y_CITY), "Qarshi sh.", fill=(0, 0, 0), font=F["reg"])
    draw.text((_X_DATE, _Y_CITY), f"{b_sana}yil.", fill=(0, 0, 0), font=F["reg"])

    # ---------- 3. Hujjat sarlavhasi (ramkasiz, markazda) ----------
    title = "Akademik ta’til berish to‘g‘risida"
    if "qayta_tiklash" in fn_lower or "tiklash" in fn_lower:
        title = ("Akademik ta’til (o‘z kursida qolgan) o‘quvchini\n"
                 "o‘quvchilar safiga tiklash to‘g‘risida")
    elif "guruhdan" in fn_lower or "otkazish" in fn_lower or "o`tkazish" in fn_lower:
        title = "O‘quvchini guruhdan guruhga o’tkazish to‘g‘risida"
    elif "chiqarish" in fn_lower or "safidan" in fn_lower:
        title = "O‘quvchini o‘quvchilar safidan chiqarish to‘g‘risida"

    ty = _Y_TITLE
    for tline in title.split("\n"):
        draw_centered(tline, ty, F["bold"])
        ty += _LINE_H

    # Muqaddima sarlavha ostidan boshlanadi. Qat'iy _Y_BODY ga bog'lab qo'yilsa,
    # ikki qatorli sarlavhali shablonlarda matn sarlavha ustiga chiqib ketardi.
    body_y = max(_Y_BODY, ty + 11)

    # ---------- Matn oqimi uchun yordamchilar ----------
    space_w = tw(" ", F["reg"])

    def layout(tokens, first_indent):
        """So'zlarni qatorlarga bo'lish. token = (matn, uslub)"""
        lines, cur, cur_w = [], [], 0
        for text, st in tokens:
            w = tw(text, F[st])
            avail = _CONTENT_W - (first_indent if not lines else 0)
            if cur and cur_w + space_w + w > avail:
                lines.append(cur)
                cur, cur_w = [(text, st, w)], w
            else:
                cur_w = cur_w + (space_w if cur else 0) + w
                cur.append((text, st, w))
        if cur:
            lines.append(cur)
        return lines

    def render(lines, y, first_indent):
        """Word kabi: oxirgi qatordan boshqasi ikki chetga tekislanadi"""
        for i, line in enumerate(lines):
            indent = first_indent if i == 0 else 0
            x0, avail = _LEFT + indent, _CONTENT_W - indent
            total = sum(w for _, _, w in line)
            gaps = len(line) - 1
            gap = ((avail - total) / gaps) if (i < len(lines) - 1 and gaps > 0) else space_w
            x = float(x0)
            for text, st, w in line:
                draw.text((int(round(x)), y), text, fill=(0, 0, 0), font=F[st])
                x += w + gap
            y += _LINE_H
        return y

    def para(tokens, y, first_indent=0):
        return render(layout(tokens, first_indent), y, first_indent) + _PARA_GAP

    def words(text, style="reg"):
        return [(w, style) for w in text.split()]

    # ---------- 4. Muqaddima ----------
    preamble = (
        "O‘zbekiston Respublikasi Vazirlar Mahkamasining 2020 yil 7-avgustdagi "
        "“O‘zbekiston Respublikasida uzluksiz boshlang‘ich, o‘rta va "
        "o‘rta maxsus professional ta’lim tizimini tartibga soluvchi "
        "normativ-huquqiy hujjatlarni tasdiqlash to‘g‘risida”gi 466-son "
        "qarori 1-ilovasi bilan tasdiqlangan “O‘zbekiston Respublikasida "
        "uzluksiz boshlang‘ich, o‘rta va o‘rta maxsus professional "
        "ta’lim to‘g‘risida” NIZOMga asosan"
    )
    # Muqaddimadan keyin xatboshi bo'shlig'i QO'YILMAYDI: etalonda oxirgi qator
    # 1347 da, BUYURAMAN esa 1414 da — orasi roppa-rosa bitta qator balandligi.
    cur_y = render(layout(words(preamble), _IND_PRE), body_y, _IND_PRE)

    # ---------- 5. BUYURAMAN: ----------
    draw_centered("BUYURAMAN:", cur_y, F["bold"])
    cur_y += _LINE_H + _PARA_GAP

    # ---------- 6. Ro'yxat bandlari ----------
    ifo = str(data.get("IFO") or data.get("FIO") or "").strip()
    kurs = str(data.get("kursi", "")).strip()
    guruhi = str(data.get("guruhi") or data.get("avvalgi_guruhi") or "").strip()
    yangi_guruh = str(data.get("yangi_guruhi", "")).strip()

    # Shablondagi {{IFO}}ga — qo'shimcha ismga YOPISHIB yozilishi kerak,
    # shuning uchun oxirgi so'z bilan birga bitta token qilinadi
    def ifo_tokens(suffix):
        parts = ifo.split()
        if not parts:
            return [(suffix.lstrip(), "bold")] if suffix.strip() else []
        out = [(w, "bold") for w in parts[:-1]]
        out.append((parts[-1] + suffix, "bold"))
        return out

    base = words(
        "“O‘zbekiston Respublikasida uzluksiz boshlang‘ich, o‘rta va "
        "o‘rta maxsus professional ta’lim to‘g‘risida” NIZOMga asosan"
    )

    if "qayta_tiklash" in fn_lower or "tiklash" in fn_lower:
        avv_num = str(data.get("avvalgi_buyruq_raqami", "")).strip()
        avv_sana = str(data.get("avvalgi_buyruq_sanasi", "")).strip()
        item1 = (base + words("texnikum direktorining")
                 + [(avv_sana, "bold")] + words("yil-dagi")
                 + [(f"{avv_num}-sonli", "bold")]
                 + words("buyrug`i bilan akademik ta`til berilgan")
                 + [(f"{kurs}-bosqich", "reg"), (f"{guruhi}-guruh", "bold")]
                 + words("talabasi") + ifo_tokens("ni")
                 + [(f"{kurs}-bosqich", "reg"), (f"{yangi_guruh}-guruhga", "bold")]
                 + words("o’quv jarayonlarini davom ettirishi uchun tiklansin."))
    elif "guruhdan" in fn_lower or "otkazish" in fn_lower or "o`tkazish" in fn_lower:
        item1 = (base + [(f"{kurs}-bosqich", "reg"), (f"{guruhi}-guruh", "bold")]
                 + words("talabasi") + ifo_tokens("ni")
                 + [(f"{yangi_guruh}-guruhga", "bold")]
                 + words("o‘tkazilsin."))
    elif "chiqarish" in fn_lower or "safidan" in fn_lower:
        item1 = (base + words("texnikum ichki tartib qoidalariga amal qilmagan")
                 + [(f"{kurs}-bosqich", "reg"), (f"{guruhi}-guruh", "bold")]
                 + words("talabasi") + ifo_tokens("ni")
                 + words("o’quvchilar safidan chiqarilsin."))
    else:
        item1 = (base + [(f"{kurs}-bosqich", "reg"), (f"{guruhi}-guruh", "bold")]
                 + words("talabasi") + ifo_tokens("ga")
                 + words("akademik ta`til berilsin."))

    is_expel = "chiqarish" in fn_lower or "safidan" in fn_lower
    item2 = ("Ushbu buyruq bilan O`IBDO`, KTBDO`, MMIBDO` hamda guruh tutorlari tanishtirilsin."
             if is_expel else
             "Ushbu buyruq bilan O`IBDO` hamda guruh tutorlari tanishtirilsin.")

    items = [
        item1,
        words(item2),
        words("1 kun muddatda prof-emis.edu.uz platformasi administratoriga taqdim etilsin."),
        words("Ushbu buyruq ijrosini taminlashni o`z  zimmamda qoldiraman."),
    ]

    for n, toks in enumerate(items, start=1):
        numbered = list(toks)
        if numbered:
            first_text, first_st = numbered[0][0], numbered[0][1]
            numbered[0] = (f"{n}.{first_text}", first_st)
        cur_y = para(numbered, cur_y, _IND_ITEM)

    # ---------- 7. Asos ----------
    asos_tail = f"{ifo}ning arizasi va direktorning roziligi."
    if is_expel:
        turi = str(data.get("asos_turi", "")).strip().lower()
        if "bildirgi" in turi or "rahbar" in turi:
            asos_tail = "Guruh rahbarining bildirgisi va ogohlantirish xatlari."
    elif "guruhdan" in fn_lower or "otkazish" in fn_lower or "o`tkazish" in fn_lower:
        asos_tail = "Talabalarning arizasi va O`IBDO`ning roziligi."

    cur_y = render(layout([("Asos:", "bolditalic")] + words(asos_tail, "italic"), 0),
                   cur_y, 0)

    # ---------- 8. Imzo ----------
    foot_y = max(cur_y + 200, 2432)
    draw.text((502, foot_y), "“Qarshi tibbiyot texnikumi”", fill=(0, 0, 0), font=F["bold"])
    draw.text((_LEFT, foot_y + _LINE_H), "ijrochi direktori:", fill=(0, 0, 0), font=F["bold"])
    name = "Sh.Raxmonov"
    draw.text((_RIGHT - tw(name, F["bold"]), foot_y + _LINE_H), name, fill=(0, 0, 0), font=F["bold"])

    img.save(output_png_path, "PNG")
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
