# ============================================================
#  services/image_builder.py
#  Sizning asl Word shabloningizni 100% o'z holida
#  Ultra HD (300 DPI A4) formatida yaratuvchi renderer
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


def render_docx_template_to_image(
    template_filename: str,
    output_png_path: str,
    data: dict,
    temp_dir: str = ""
) -> bool:
    """
    Sizning asl malumotnoma.docx shabloningizni 100% asl dizaynda
    (300 DPI A4 Ultra HD rasm) shaklida yaratadi.
    """
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 1. Asl Worddan olingan mukammal Yuqori andoza (Shapka, Chiziq, Qarshi shahri, MA'LUMOTNOMA, Ushbu...)
        top_base_png = os.path.join(base_dir, "templates", "malumotnoma_top_base.png")
        footer_banner_png = os.path.join(base_dir, "templates", "stamps", "word_footer_banner.png")
        
        if os.path.exists(top_base_png):
            img = Image.open(top_base_png).convert("RGB")
        else:
            # Fallback agar top_base_png topilmasa
            img = Image.new("RGB", (2481, 3508), color=(255, 255, 255))
            
        draw = ImageDraw.Draw(img)

        f_reg = _get_font("reg", 58)
        f_bold = _get_font("bold", 58)
        f_italic = _get_font("italic", 58)

        fio = str(data.get("FIO", "")).strip()
        oquv_yili = str(data.get("OQUV_YILI", "2026/2027")).strip()
        yonalish = str(data.get("YONALISH", "")).strip()
        sana = str(data.get("SANA", "14.08.2026")).strip()
        boshlash_yili = oquv_yili.split("/")[0] if "/" in oquv_yili else "2026"

        # 2. Sana: O'ng tomonga tekislangan (X=2339, Y=801)
        sana_text = f"{sana} y." if not (sana.endswith("y.") or sana.endswith("y")) else sana
        bb = f_reg.getbbox(sana_text)
        tw = bb[2] - bb[0]
        draw.text((2339 - tw, 801), sana_text, fill=(0, 0, 0), font=f_reg)

        left_x = 355
        right_x = 2300
        content_w = right_x - left_x

        # 3. Kirish gapi (Qatoriga to'lib turishi - Full Justified)
        draw.rectangle([(0, 1350), (img.width, 1490)], fill=(255, 255, 255))
        intro_words = ["Ushbu", "ma’lumotnoma", "shuni", "tasdiqlaydiki,", "haqiqatdan", "ham"]
        words_w = sum(f_reg.getbbox(w)[2] - f_reg.getbbox(w)[0] for w in intro_words)
        gaps = len(intro_words) - 1
        gap_px = (content_w - words_w) / gaps

        cur_x = float(left_x)
        intro_y = 1406
        for w in intro_words:
            draw.text((int(round(cur_x)), intro_y), w, fill=(0, 0, 0), font=f_reg)
            w_px = f_reg.getbbox(w)[2] - f_reg.getbbox(w)[0]
            cur_x += w_px + gap_px

        # 4. Dinamik Asosiy Matn (X: 355 dan 2300 gacha, Y=1541)
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
            test_w = cur_w + (space_w if cur_line else 0) + w_px
            if test_w > content_w and cur_line:
                lines.append(cur_line)
                cur_line = [(word, is_bold, w_px)]
                cur_w = w_px
            else:
                cur_line.append((word, is_bold, w_px))
                cur_w = test_w

        if cur_line:
            lines.append(cur_line)

        cur_y = start_y
        for line_idx, line in enumerate(lines):
            is_last = (line_idx == len(lines) - 1)
            tot_w = sum(w for _, _, w in line)
            gaps = len(line) - 1

            if not is_last and gaps > 0:
                gap_px = (content_w - tot_w) / gaps
            else:
                gap_px = float(space_w)

            cur_x = float(left_x)
            for word, is_bold, w_px in line:
                fnt = f_bold if is_bold else f_reg
                draw.text((int(round(cur_x)), cur_y), word, fill=(0, 0, 0), font=fnt)
                cur_x += w_px + gap_px

            cur_y += line_h

        # 4. Izoh (Chap tomondan, Ushbu... matni to'g'risidan X=503)
        cur_y = max(cur_y, 1809 + line_h)
        note_str = "Ma’lumotnoma so‘ralgan joyga taqdim etish uchun berildi"
        draw.text((503, cur_y), note_str, fill=(0, 0, 0), font=f_italic)

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
