# ============================================================
#  services/image_builder.py
#  Sizning asl Word shabloningizni 100% o'z holida
#  Ultra HD (A4 PNG) formatida yaratuvchi renderer
# ============================================================

import os
import io
import zipfile
from PIL import Image, ImageDraw, ImageFont

try:
    from docbot_config import find_template_file
except ImportError:
    from config import find_template_file


def _get_font(size: int, bold: bool = False, italic: bool = False):
    """Times New Roman shriftini tizimdan yoki loyiha papkasidan yuklash"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bundled_tnr = os.path.join(base_dir, "fonts", "TimesNewRomanBold.ttf")
    bundled_fallback = os.path.join(base_dir, "fonts", "AppBoldFont.ttf")

    font_paths = [
        r"C:\Windows\Fonts\timesbd.ttf" if bold else (r"C:\Windows\Fonts\timesi.ttf" if italic else r"C:\Windows\Fonts\times.ttf"),
        "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf" if bold else ("/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf" if italic else "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"),
        "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman_Bold.ttf" if bold else "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf",
    ]
    if bold and os.path.exists(bundled_tnr):
        font_paths.insert(0, bundled_tnr)
    if os.path.exists(bundled_fallback):
        font_paths.append(bundled_fallback)

    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    if os.path.exists(bundled_tnr):
        try:
            return ImageFont.truetype(bundled_tnr, size)
        except Exception:
            pass
    return ImageFont.load_default(size=size)


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
    (logotip, matnlar, shahar/sana, imzo va pechat) A4 tiniq rasm shaklida hosil qiladi.
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

        # 2. A4 Canvas (1654 x 2338 px)
        W, H = 1654, 2338
        img = Image.new("RGB", (W, H), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        margin_x = 100
        content_w = W - 2 * margin_x
        curr_y = 120

        # 3. Header (3 ustun: O'zbekcha | Logotip | Ruscha)
        col1_w = int(content_w * 0.38)
        col2_w = int(content_w * 0.24)
        col3_w = content_w - col1_w - col2_w

        f_hdr = _get_font(26, bold=True)

        # Chap ustun: O'zbekcha matn
        uz_lines = [
            "O’ZBEKISTON",
            "RESPUBLIKASI",
            "QASHQADARYO VILOYATI",
            "“QARSHI TIBBIYOT",
            "TEXNIKUMI”",
            "NODAVLAT TA’LIM",
            "MUASSASASI"
        ]
        uz_y = curr_y + 10
        for line in uz_lines:
            bbox = f_hdr.getbbox(line)
            tw = bbox[2] - bbox[0]
            draw.text((margin_x + (col1_w - tw) // 2, uz_y), line, fill=(0, 0, 0), font=f_hdr)
            uz_y += 36

        # Markaziy ustun: Asl Logotip (image1.png)
        if logo_img:
            logo_w, logo_h = 240, 240
            logo_resized = logo_img.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
            lx = margin_x + col1_w + (col2_w - logo_w) // 2
            ly = curr_y + 15
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
        ru_y = curr_y + 10
        for line in ru_lines:
            bbox = f_hdr.getbbox(line)
            tw = bbox[2] - bbox[0]
            draw.text((margin_x + col1_w + col2_w + (col3_w - tw) // 2, ru_y), line, fill=(0, 0, 0), font=f_hdr)
            ru_y += 36

        curr_y = max(uz_y, ru_y, curr_y + 270) + 25

        # 4. Qalin Ajratuvchi Chiziq
        draw.line([(margin_x, curr_y), (margin_x + content_w, curr_y)], fill=(0, 0, 0), width=4)
        curr_y += 30

        # 5. Shahar va Sana
        f_meta_bold = _get_font(28, bold=True)
        f_meta_reg = _get_font(28, bold=False)
        draw.text((margin_x, curr_y), "Qarshi shahri", fill=(0, 0, 0), font=f_meta_bold)

        sana_val = str(data.get("SANA", "13.08.2026")).strip()
        if not (sana_val.endswith("y.") or sana_val.endswith("y")):
            sana_val += " y."
        bbox = f_meta_reg.getbbox(sana_val)
        tw = bbox[2] - bbox[0]
        draw.text((margin_x + content_w - tw, curr_y), sana_val, fill=(0, 0, 0), font=f_meta_reg)
        curr_y += 180

        # 6. Sarlavha: MA'LUMOTNOMA (Bold, 38pt)
        f_title = _get_font(38, bold=True)
        title_str = "MA’LUMOTNOMA"
        bbox = f_title.getbbox(title_str)
        tw = bbox[2] - bbox[0]
        draw.text((margin_x + (content_w - tw) // 2, curr_y), title_str, fill=(0, 0, 0), font=f_title)
        curr_y += 130

        # 7. Kirish jumlasi
        f_body = _get_font(28, bold=False)
        intro_str = "Ushbu     ma’lumotnoma     shuni     tasdiqlaydiki,     haqiqatdan     ham"
        bbox = f_body.getbbox(intro_str)
        tw = bbox[2] - bbox[0]
        draw.text((margin_x + (content_w - tw) // 2, curr_y), intro_str, fill=(0, 0, 0), font=f_body)
        curr_y += 85

        # 8. Asosiy Matn (Word-wrapping)
        fio = str(data.get("FIO", "")).strip()
        oquv_yili = str(data.get("OQUV_YILI", "2026/2027")).strip()
        yonalish = str(data.get("YONALISH", "")).strip()
        boshlash_yili = oquv_yili.split("/")[0] if "/" in oquv_yili else "2026"

        full_text = f"{fio} {oquv_yili}-o‘quv yilida {yonalish} yo‘nalishiga shartnoma asosida o‘qishga qabul qilindi. Talaba o‘qishni {boshlash_yili}-yil sentyabr oyidan boshlaydi."

        words = full_text.split()
        lines = []
        current_line = []
        current_w = 0
        space_w = f_body.getbbox(" ")[2] - f_body.getbbox(" ")[0]

        for word in words:
            bb = f_body.getbbox(word)
            w_px = bb[2] - bb[0]
            test_w = current_w + (space_w if current_line else 0) + w_px
            if test_w > content_w and current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_w = w_px
            else:
                current_line.append(word)
                current_w = test_w

        if current_line:
            lines.append(" ".join(current_line))

        for line in lines:
            bb = f_body.getbbox(line)
            tw = bb[2] - bb[0]
            draw.text((margin_x + (content_w - tw) // 2, curr_y), line, fill=(0, 0, 0), font=f_body)
            curr_y += 60

        curr_y += 50

        # 9. Izoh (Italic)
        f_note = _get_font(26, italic=True)
        note_str = "Ma’lumotnoma so‘ralgan joyga taqdim etish uchun berildi"
        bbox = f_note.getbbox(note_str)
        tw = bbox[2] - bbox[0]
        draw.text((margin_x + (content_w - tw) // 2, curr_y), note_str, fill=(0, 0, 0), font=f_note)
        curr_y += 240

        # 10. Footer Banner (Asl Pechat, Muhr, Imzo va Matn)
        if imzo_img:
            foot_w = content_w
            foot_h = int(foot_w * imzo_img.height / imzo_img.width)
            imzo_resized = imzo_img.resize((foot_w, foot_h), Image.Resampling.LANCZOS)
            img.paste(imzo_resized, (margin_x, curr_y), imzo_resized if "A" in imzo_resized.getbands() else None)
        else:
            f_foot = _get_font(26, bold=True)
            foot_l1 = "“Qarshi tibbiyot texnikumi”"
            foot_l2 = "ijrochi direktori:"
            draw.text((margin_x, curr_y), foot_l1, fill=(0, 0, 0), font=f_foot)
            draw.text((margin_x, curr_y + 36), foot_l2, fill=(0, 0, 0), font=f_foot)
            dir_name = "Sh.Raxmonov"
            bb = f_foot.getbbox(dir_name)
            tw = bb[2] - bb[0]
            draw.text((margin_x + content_w - tw, curr_y + 18), dir_name, fill=(0, 0, 0), font=f_foot)

        img.save(output_png_path, "PNG", quality=100)
        return True

    except Exception as e:
        print(f"Render docx error: {e}")
        return False
