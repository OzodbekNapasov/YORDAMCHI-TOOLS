# ============================================================
#  services/image_builder.py
#  Sizning asl Word shabloningizni 100% o'z holida
#  Ultra HD (300 DPI A4) formatida yaratuvchi universal renderer
# ============================================================

import os
import io
import zipfile
from PIL import Image, ImageDraw, ImageFont

try:
    from docbot_config import find_template_file
except ImportError:
    from config import find_template_file


def _get_font(size_pt: float, bold: bool = False, italic: bool = False):
    """Times New Roman shriftini 300 DPI o'lchamda yuklash (1 pt = ~4.166 px)"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fonts_dir = os.path.join(base_dir, "fonts")
    
    # 300 DPI uchun pt -> px konvertatsiyasi: size_pt * (300 / 72)
    px_size = int(round(size_pt * (300.0 / 72.0)))
    
    if bold and italic:
        font_names = ["timesbi.ttf", "TimesNewRomanBoldItalic.ttf", "FreeSerifBoldItalic.ttf"]
    elif bold:
        font_names = ["timesbd.ttf", "TimesNewRomanBold.ttf", "FreeSerifBold.ttf", "AppBoldFont.ttf"]
    elif italic:
        font_names = ["timesi.ttf", "TimesNewRomanItalic.ttf", "FreeSerifItalic.ttf"]
    else:
        font_names = ["times.ttf", "TimesNewRoman.ttf", "FreeSerif.ttf"]

    font_paths = []
    for fn in font_names:
        font_paths.append(os.path.join(fonts_dir, fn))
        font_paths.append(os.path.join(base_dir, "templates", "fonts", fn))
        font_paths.append(os.path.join(r"C:\Windows\Fonts", fn))
        font_paths.append(f"/usr/share/fonts/truetype/msttcorefonts/{fn}")
        font_paths.append(f"/usr/share/fonts/truetype/freefont/{fn}")

    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, px_size)
            except Exception:
                pass

    return ImageFont.load_default(size=px_size)


def _extract_media_from_docx(docx_path: str, media_name: str) -> Image.Image | None:
    """Word (.docx) fayli ichidagi o'z logotip yoki pechat rasmini to'g'ridan-to'g'ri o'qib olish"""
    try:
        if not os.path.exists(docx_path):
            return None
        with zipfile.ZipFile(docx_path, 'r') as z:
            target = f"word/media/{media_name}"
            if target in z.namelist():
                img_data = z.read(target)
                return Image.open(io.BytesIO(img_data)).convert("RGBA")
    except Exception as e:
        print(f"Extract media error ({media_name}): {e}")
    return None


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
        template_path = find_template_file(template_filename)

        # 1. Logotip va Pechat/Imzo rasmlarini olish
        logo_img = None
        imzo_img = None

        local_logo = os.path.join(base_dir, "templates", "stamps", "image1.png")
        if os.path.exists(local_logo):
            try: logo_img = Image.open(local_logo).convert("RGBA")
            except Exception: pass
        if logo_img is None and os.path.exists(template_path):
            logo_img = _extract_media_from_docx(template_path, "image1.png")

        local_imzo = os.path.join(base_dir, "templates", "stamps", "image2.png")
        if os.path.exists(local_imzo):
            try: imzo_img = Image.open(local_imzo).convert("RGBA")
            except Exception: pass
        if imzo_img is None and os.path.exists(template_path):
            imzo_img = _extract_media_from_docx(template_path, "image2.png")

        # 2. 300 DPI A4 Canvas (2481 x 3508 px)
        W, H = 2481, 3508
        img = Image.new("RGB", (W, H), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        margin_x = 142
        content_w = W - 2 * margin_x  # ~2197 px
        curr_y = 240

        # 3. Header (3 ustun: O'zbekcha (12pt Bold) | Logotip | Ruscha (12pt Bold))
        col1_w = int(content_w * 0.40)
        col2_w = int(content_w * 0.20)
        col3_w = content_w - col1_w - col2_w

        f_hdr = _get_font(12, bold=True)

        uz_lines = [
            "O’ZBEKISTON",
            "RESPUBLIKASI",
            "QASHQADARYO VILOYATI",
            "“QARSHI TIBBIYOT",
            "TEXNIKUMI”",
            "NODAVLAT TA’LIM",
            "MUASSASASI"
        ]
        uz_y = curr_y
        for line in uz_lines:
            bbox = f_hdr.getbbox(line)
            tw = bbox[2] - bbox[0]
            draw.text((margin_x + (col1_w - tw) // 2, uz_y), line, fill=(0, 0, 0), font=f_hdr)
            uz_y += 58

        # Markaziy ustun: Asl Logotip (image1.png)
        if logo_img:
            logo_w, logo_h = 360, 360
            logo_resized = logo_img.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
            lx = margin_x + col1_w + (col2_w - logo_w) // 2
            ly = curr_y + 20
            img.paste(logo_resized, (lx, ly), logo_resized if "A" in logo_resized.getbands() else None)

        # O'ng ustun: Ruscha matn
        ru_lines = [
            "РЕСПУБЛИКА УЗБЕКИСТАН",
            "КАШКАДАРЬИНСКАЯ ОБЛАСТЬ",
            "НЕГОСУДАРСТВЕННОЕ",
            "ОБРАЗОВАТЕЛЬНОЕ",
            "УЧРЕЖДЕНИЕ",
            "«КАРШИНСКИЙ",
            "МЕДИЦИНСКИЙ ТЕХНИКУМ»"
        ]
        ru_y = curr_y
        for line in ru_lines:
            bbox = f_hdr.getbbox(line)
            tw = bbox[2] - bbox[0]
            draw.text((margin_x + col1_w + col2_w + (col3_w - tw) // 2, ru_y), line, fill=(0, 0, 0), font=f_hdr)
            ru_y += 58

        curr_y = max(uz_y, ru_y, curr_y + 400) + 40

        # 4. Qalin Ajratuvchi Chiziq
        draw.line([(margin_x, curr_y), (margin_x + content_w, curr_y)], fill=(0, 0, 0), width=6)
        curr_y += 35

        # 5. Shahar va Sana (14pt Regular)
        f_14 = _get_font(14, bold=False)
        f_14_b = _get_font(14, bold=True)
        f_14_i = _get_font(14, italic=True)

        draw.text((margin_x, curr_y), "Qarshi shahri", fill=(0, 0, 0), font=f_14)

        sana_val = str(data.get("SANA", "14.08.2026")).strip()
        if not (sana_val.endswith("y.") or sana_val.endswith("y")):
            sana_val += " y."
        bbox = f_14.getbbox(sana_val)
        tw = bbox[2] - bbox[0]
        draw.text((margin_x + content_w - tw, curr_y), sana_val, fill=(0, 0, 0), font=f_14)
        curr_y += 400

        # 6. Sarlavha: MA'LUMOTNOMA (16pt Bold)
        f_title = _get_font(16, bold=True)
        title_str = "MA’LUMOTNOMA"
        bbox = f_title.getbbox(title_str)
        tw = bbox[2] - bbox[0]
        draw.text((margin_x + (content_w - tw) // 2, curr_y), title_str, fill=(0, 0, 0), font=f_title)
        curr_y += 180

        # 7. Kirish jumlasi (14pt Regular, Justified)
        intro_words = ["Ushbu", "ma’lumotnoma", "shuni", "tasdiqlaydiki,", "haqiqatdan", "ham"]
        words_w = sum(f_14.getbbox(w)[2] - f_14.getbbox(w)[0] for w in intro_words)
        total_gaps = len(intro_words) - 1
        gap_w = (content_w - words_w) / total_gaps if total_gaps > 0 else 0

        cur_x = float(margin_x)
        for i, w in enumerate(intro_words):
            draw.text((int(round(cur_x)), curr_y), w, fill=(0, 0, 0), font=f_14)
            w_px = f_14.getbbox(w)[2] - f_14.getbbox(w)[0]
            cur_x += w_px + gap_w

        curr_y += 135

        # 8. Asosiy Matn (14pt, FIO va YONALISH Bold, avtomatik qatorlash)
        fio = str(data.get("FIO", "")).strip()
        oquv_yili = str(data.get("OQUV_YILI", "2026/2027")).strip()
        yonalish = str(data.get("YONALISH", "")).strip()
        boshlash_yili = oquv_yili.split("/")[0] if "/" in oquv_yili else "2026"

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
        current_line = []
        current_w = 0
        space_w = f_14.getbbox(" ")[2] - f_14.getbbox(" ")[0]

        for word, is_bold in tokens:
            fnt = f_14_b if is_bold else f_14
            bb = fnt.getbbox(word)
            w_px = bb[2] - bb[0]
            test_w = current_w + (space_w if current_line else 0) + w_px
            if test_w > content_w and current_line:
                lines.append(current_line)
                current_line = [(word, is_bold, w_px)]
                current_w = w_px
            else:
                current_line.append((word, is_bold, w_px))
                current_w = test_w

        if current_line:
            lines.append(current_line)

        for line_idx, line in enumerate(lines):
            is_last_line = (line_idx == len(lines) - 1)
            line_words_w = sum(w for _, _, w in line)
            gaps = len(line) - 1

            if not is_last_line and gaps > 0:
                # Justified qator
                line_gap = (content_w - line_words_w) / gaps
            else:
                # Oxirgi qator chapdan
                line_gap = float(space_w)

            cur_x = float(margin_x)
            for word, is_bold, w_px in line:
                fnt = f_14_b if is_bold else f_14
                draw.text((int(round(cur_x)), curr_y), word, fill=(0, 0, 0), font=fnt)
                cur_x += w_px + line_gap

            curr_y += 135

        curr_y += 90

        # 9. Izoh (14pt Kursiv/Italic, Chapdan / LEFT ALIGNED!)
        note_str = "Ma’lumotnoma so‘ralgan joyga taqdim etish uchun berildi"
        draw.text((margin_x, curr_y), note_str, fill=(0, 0, 0), font=f_14_i)
        curr_y += 280

        # 10. Footer Banner (Asl Pechat, Muhr, Imzo va Matn)
        if imzo_img:
            foot_w = int(content_w * 0.85)
            foot_h = int(foot_w * imzo_img.height / imzo_img.width)
            imzo_resized = imzo_img.resize((foot_w, foot_h), Image.Resampling.LANCZOS)
            fx = margin_x + (content_w - foot_w) // 2
            img.paste(imzo_resized, (fx, curr_y), imzo_resized if "A" in imzo_resized.getbands() else None)
        else:
            foot_l1 = "“Qarshi tibbiyot texnikumi”"
            foot_l2 = "ijrochi direktori:"
            draw.text((margin_x, curr_y), foot_l1, fill=(0, 0, 0), font=f_14_b)
            draw.text((margin_x, curr_y + 55), foot_l2, fill=(0, 0, 0), font=f_14_b)
            dir_name = "Sh.Raxmonov"
            bb = f_14_b.getbbox(dir_name)
            tw = bb[2] - bb[0]
            draw.text((margin_x + content_w - tw, curr_y + 25), dir_name, fill=(0, 0, 0), font=f_14_b)

        img.save(output_png_path, "PNG", quality=100)
        return True

    except Exception as e:
        print(f"Render docx error: {e}")
        return False
