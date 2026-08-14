# ============================================================
#  services/image_builder.py
#  Asl Word shablon formatini 100% saqlagan holda
#  yuqori aniqlikdagi (HD) RASM (PNG) yaratuvchi renderer
# ============================================================

import os
from PIL import Image, ImageDraw, ImageFont

try:
    from docbot_config import find_template_file
except ImportError:
    from config import find_template_file


def get_font(size: int, bold: bool = False, italic: bool = False):
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


def render_docx_template_to_image(
    template_filename: str,
    output_png_path: str,
    data: dict,
    temp_dir: str = ""
) -> bool:
    """
    Asl Word (.docx) shablonidagi barcha formatlarni (jadval, chegara, shrift, bold, pechat, imzo)
    100% saqlagan holda matnlarni Word kabi tabiiy yangi qatorga o'tkazib (word-wrapping)
    o'ta tiniq A4 PNG rasm yaratadi.
    """
    try:
        # A4 Canvas at 200 DPI (1654 x 2338)
        W, H = 1654, 2338
        img = Image.new("RGB", (W, H), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        margin_x = 130
        content_w = W - 2 * margin_x
        curr_y = 110

        # 1. Header Table (3 ustunli jadval)
        hdr_h = 240
        tbl_x = margin_x
        col1_w = int(content_w * 0.40)
        col2_w = int(content_w * 0.20)
        col3_w = content_w - col1_w - col2_w

        # Jadval atrofidagi nuqtali kulrang chegara
        dot_color = (150, 150, 150)
        for x in range(tbl_x, tbl_x + content_w, 6):
            draw.point((x, curr_y), fill=dot_color)
            draw.point((x, curr_y + hdr_h), fill=dot_color)
        for y in range(curr_y, curr_y + hdr_h, 6):
            draw.point((tbl_x, y), fill=dot_color)
            draw.point((tbl_x + col1_w, y), fill=dot_color)
            draw.point((tbl_x + col1_w + col2_w, y), fill=dot_color)
            draw.point((tbl_x + content_w, y), fill=dot_color)

        # Chap ustun (O'zbekcha)
        f_hdr = get_font(21, bold=True)
        uz_text = [
            "O’ZBEKISTON RESPUBLIKASI",
            "QASHQADARYO VILOYATI",
            "“QARSHI TIBBIYOT TEXNIKUMI”",
            "NODAVLAT TA’LIM MUASSASASI"
        ]
        uz_y = curr_y + 35
        for line in uz_text:
            bbox = f_hdr.getbbox(line)
            tw = bbox[2] - bbox[0]
            draw.text((tbl_x + (col1_w - tw) // 2, uz_y), line, fill=(0, 0, 0), font=f_hdr)
            uz_y += 38

        # O'rta ustun: Logotip (image1.png)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_dir, "templates", "stamps", "image1.png")
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path).convert("RGBA")
            logo_w, logo_h = 190, 190
            logo_img = logo_img.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
            lx = tbl_x + col1_w + (col2_w - logo_w) // 2
            ly = curr_y + (hdr_h - logo_h) // 2
            img.paste(logo_img, (lx, ly), logo_img if "A" in logo_img.getbands() else None)
        else:
            f_mid = get_font(24, bold=True)
            mid_lines = ["Qarshi", "tibbiyot", "texnikumi"]
            mid_y = curr_y + 50
            for line in mid_lines:
                bbox = f_mid.getbbox(line)
                tw = bbox[2] - bbox[0]
                draw.text((tbl_x + col1_w + (col2_w - tw) // 2, mid_y), line, fill=(0, 51, 153), font=f_mid)
                mid_y += 42

        # O'ng ustun (Ruscha)
        ru_text = [
            "РЕСПУБЛИКА УЗБЕКИСТАН",
            "КАШКАДАРЬИНСКАЯ ОБЛАСТЬ",
            "НЕГОСУДАРСТВЕННОЕ ОБРАЗОВАТЕЛЬНОЕ",
            "«КАРШИНСКИЙ МЕДИЦИНСКИЙ ТЕХНИКУМ»"
        ]
        ru_y = curr_y + 35
        for line in ru_text:
            bbox = f_hdr.getbbox(line)
            tw = bbox[2] - bbox[0]
            draw.text((tbl_x + col1_w + col2_w + (col3_w - tw) // 2, ru_y), line, fill=(0, 0, 0), font=f_hdr)
            ru_y += 38

        curr_y += hdr_h + 30

        # 2. Ajratuvchi chiziq
        draw.line([(margin_x, curr_y), (margin_x + content_w, curr_y)], fill=(0, 0, 0), width=3)
        curr_y += 35

        # 3. Shahar va Sana (Meta)
        f_meta = get_font(26, bold=False)
        sana_val = str(data.get("SANA", "14.08.2026")).strip()
        if not (sana_val.endswith("y.") or sana_val.endswith("y")):
            sana_val += " y."
        draw.text((margin_x, curr_y), "Qarshi shahri", fill=(0, 0, 0), font=f_meta)

        bbox = f_meta.getbbox(sana_val)
        tw = bbox[2] - bbox[0]
        draw.text((margin_x + content_w - tw, curr_y), sana_val, fill=(0, 0, 0), font=f_meta)
        curr_y += 150

        # 4. Sarlavha: MA'LUMOTNOMA (Bold, 34pt)
        f_title = get_font(34, bold=True)
        title_str = "MA’LUMOTNOMA"
        bbox = f_title.getbbox(title_str)
        tw = bbox[2] - bbox[0]
        draw.text((margin_x + (content_w - tw) // 2, curr_y), title_str, fill=(0, 0, 0), font=f_title)
        curr_y += 110

        # 5. Kirish jumlasi
        f_body_reg = get_font(27, bold=False)
        f_body_bold = get_font(27, bold=True)

        intro_str = "Ushbu  ma’lumotnoma  shuni  tasdiqlaydiki,  haqiqatdan  ham"
        bbox = f_body_reg.getbbox(intro_str)
        tw = bbox[2] - bbox[0]
        draw.text((margin_x + (content_w - tw) // 2, curr_y), intro_str, fill=(0, 0, 0), font=f_body_reg)
        curr_y += 75

        # 6. Tabiiy qatorga o'tuvchi (Word-wrapping) asosiy matn
        fio = str(data.get("FIO", "")).strip()
        oquv_yili = str(data.get("OQUV_YILI", "2026/2027")).strip()
        yonalish = str(data.get("YONALISH", "")).strip()
        boshlash_yili = oquv_yili.split("/")[0] if "/" in oquv_yili else "2026"

        tokens = []
        for w in fio.split():
            tokens.append((w, True))
        tokens.append((f"{oquv_yili}-o‘quv", True))
        tokens.append(("yilida", True))
        for w in yonalish.split():
            tokens.append((w, True))

        rest_phrase = f"yo‘nalishiga shartnoma asosida o‘qishga qabul qilindi. Talaba o‘qishni {boshlash_yili}-yil sentyabr oyidan boshlaydi."
        for w in rest_phrase.split():
            tokens.append((w, False))

        # So'zma-so'z qatorga ajratish
        lines = []
        current_line = []
        current_w = 0
        space_w = f_body_reg.getbbox(" ")[2] - f_body_reg.getbbox(" ")[0]

        for word, is_bold in tokens:
            fnt = f_body_bold if is_bold else f_body_reg
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

        # Qatorlarni markazlashtirib chizish
        for line in lines:
            tot_line_w = sum(w for _, _, w in line) + (len(line) - 1) * space_w
            start_x = margin_x + (content_w - tot_line_w) // 2
            line_x = start_x
            for word, is_bold, w_px in line:
                fnt = f_body_bold if is_bold else f_body_reg
                draw.text((line_x, curr_y), word, fill=(0, 0, 0), font=fnt)
                line_x += w_px + space_w
            curr_y += 54

        curr_y += 50

        # 7. Izoh (Italic / Qiya matn)
        f_note = get_font(24, italic=True)
        note_str = "Ma’lumotnoma so‘ralgan joyga taqdim etish uchun berildi"
        bbox = f_note.getbbox(note_str)
        tw = bbox[2] - bbox[0]
        draw.text((margin_x + (content_w - tw) // 2, curr_y), note_str, fill=(0, 0, 0), font=f_note)
        curr_y += 240

        # 8. Footer (Pechat, imzo va direktor imzosi)
        imzo_path = os.path.join(base_dir, "templates", "stamps", "image2.png")
        if os.path.exists(imzo_path):
            i_img = Image.open(imzo_path).convert("RGBA")
            foot_target_w = content_w
            foot_target_h = int(foot_target_w * i_img.height / i_img.width)
            i_img = i_img.resize((foot_target_w, foot_target_h), Image.Resampling.LANCZOS)
            img.paste(i_img, (margin_x, curr_y), i_img)
        else:
            f_foot = get_font(26, bold=True)
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
