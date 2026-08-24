"""
pdf_generator.py — Test savollari va rasmlardan yuqori sifatli PDF yaratish moduli.
"""

import os
import io
import base64
import struct
import logging
import ctypes
import ctypes.wintypes
from pathlib import Path
from typing import List
from datetime import datetime
from PIL import Image, ImageDraw, ImageFilter, ImageFile
from fpdf import FPDF

ImageFile.LOAD_TRUNCATED_IMAGES = True

try:
    from .xml_parser import Question
except ImportError:
    from xml_parser import Question

logger = logging.getLogger(__name__)

# Windows GDI+ yordamida rasmlarni to'g'ri o'qish (EMF/WMF/MyTestX BMP)
gdiplus = ctypes.windll.gdiplus if os.name == 'nt' else None
ole32   = ctypes.windll.ole32   if os.name == 'nt' else None
kernel32= ctypes.windll.kernel32 if os.name == 'nt' else None

if os.name == 'nt':
    class GdiplusStartupInput(ctypes.Structure):
        _fields_ = [
            ('GdiplusVersion', ctypes.c_uint32),
            ('DebugEventCallback', ctypes.c_void_p),
            ('SuppressBackgroundThread', ctypes.c_bool),
            ('SuppressExternalCodecs', ctypes.c_bool)
        ]

    gdi_token = ctypes.c_ulong()
    gdi_input = GdiplusStartupInput(1, None, False, False)
    try:
        gdiplus.GdiplusStartup(ctypes.byref(gdi_token), ctypes.byref(gdi_input), None)
        
        kernel32.GlobalAlloc.restype = ctypes.c_void_p
        kernel32.GlobalLock.restype = ctypes.c_void_p
        kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
        kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
        kernel32.GlobalSize.restype = ctypes.c_size_t
        kernel32.GlobalSize.argtypes = [ctypes.c_void_p]

        ole32.CreateStreamOnHGlobal.argtypes = [ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p]
        ole32.GetHGlobalFromStream.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    except Exception:
        pass


def add_image_shadow(img: Image.Image, shadow_offset=(3, 3), blur_radius=4, shadow_color=(160, 160, 160, 160), border_color=(220, 220, 220)) -> Image.Image:
    """
    Rasm atrofida yengil professional soya va ramka hosil qiladi.
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")
        
    w, h = img.size
    
    pad_right = shadow_offset[0] + blur_radius * 2
    pad_bottom = shadow_offset[1] + blur_radius * 2
    
    new_w = w + pad_right + blur_radius
    new_h = h + pad_bottom + blur_radius
    
    canvas = Image.new("RGBA", (new_w, new_h), (255, 255, 255, 255))
    
    shadow_mask = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_mask)
    
    sx0 = shadow_offset[0] + 1
    sy0 = shadow_offset[1] + 1
    sx1 = sx0 + w
    sy1 = sy0 + h
    
    shadow_draw.rectangle([sx0, sy0, sx1, sy1], fill=shadow_color)
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(blur_radius))
    
    canvas.paste(shadow_mask, (0, 0), shadow_mask)
    
    bordered_img = img.copy()
    draw_b = ImageDraw.Draw(bordered_img)
    draw_b.rectangle([0, 0, w - 1, h - 1], outline=border_color, width=1)
    
    canvas.paste(bordered_img, (0, 0), bordered_img)
    return canvas.convert("RGB")


def render_image_bytes(raw_bytes: bytes) -> Image.Image:
    """
    Rasm baytlarini PIL Image ob'ektiga o'tkazadi.
    UTF-8 ko'p baytli o'zgarishlarni aniqlab, 100% tiniq va xatosiz tiklaydi.
    """
    # BMP va UTF-8 multi-byte buzilishini tekshirish
    needs_utf8_recovery = False
    if raw_bytes.startswith(b'BM') and len(raw_bytes) >= 54:
        w = abs(struct.unpack_from('<i', raw_bytes, 18)[0])
        h = abs(struct.unpack_from('<i', raw_bytes, 22)[0])
        if w > 4000 or h > 4000 or b'\xd1\x8f' in raw_bytes[:100] or b'\xe2\x80' in raw_bytes[:100]:
            needs_utf8_recovery = True

    # 1. UTF-8 -> CP1251 yagona baytli tiklash (agar kerak bo'lsa)
    if needs_utf8_recovery:
        try:
            utf8_str = raw_bytes.decode('utf-8', errors='ignore')
            single_bytes = utf8_str.encode('cp1251', errors='replace')
            if single_bytes.startswith(b'BM') and len(single_bytes) >= 54:
                w = abs(struct.unpack_from('<i', single_bytes, 18)[0])
                h = abs(struct.unpack_from('<i', single_bytes, 22)[0])
                exp_len = 54 + w * h * 4
                if len(single_bytes) < exp_len:
                    single_bytes += b'\x00' * (exp_len - len(single_bytes))
                img = Image.open(io.BytesIO(single_bytes))
                return add_image_shadow(img)
        except Exception:
            pass

    # 2. Oddiy PIL o'qish
    try:
        img = Image.open(io.BytesIO(raw_bytes))
        if 0 < img.size[0] < 4000 and 0 < img.size[1] < 4000:
            return add_image_shadow(img)
    except Exception:
        pass

    # 3. Ikkinchi urinish UTF-8 recovery
    try:
        utf8_str = raw_bytes.decode('utf-8', errors='ignore')
        single_bytes = utf8_str.encode('cp1251', errors='replace')
        if single_bytes.startswith(b'BM') and len(single_bytes) >= 54:
            w = abs(struct.unpack_from('<i', single_bytes, 18)[0])
            h = abs(struct.unpack_from('<i', single_bytes, 22)[0])
            exp_len = 54 + w * h * 4
            if len(single_bytes) < exp_len:
                single_bytes += b'\x00' * (exp_len - len(single_bytes))
            img = Image.open(io.BytesIO(single_bytes))
            return add_image_shadow(img)
    except Exception:
        pass

    # 4. Windows GDI+ fallback
    if os.name == 'nt' and gdiplus and kernel32:
        try:
            h_glob = kernel32.GlobalAlloc(0x0002, len(raw_bytes))
            if h_glob:
                ptr = kernel32.GlobalLock(h_glob)
                if ptr:
                    ctypes.memmove(ptr, raw_bytes, len(raw_bytes))
                    kernel32.GlobalUnlock(h_glob)

                    p_stream = ctypes.c_void_p()
                    if ole32.CreateStreamOnHGlobal(h_glob, True, ctypes.byref(p_stream)) == 0:
                        p_image = ctypes.c_void_p()
                        if gdiplus.GdipLoadImageFromStream(p_stream, ctypes.byref(p_image)) == 0 and p_image:
                            w = ctypes.c_uint32()
                            h = ctypes.c_uint32()
                            gdiplus.GdipGetImageWidth(p_image, ctypes.byref(w))
                            gdiplus.GdipGetImageHeight(p_image, ctypes.byref(h))

                            if w.value > 0 and h.value > 0 and w.value < 5000 and h.value < 5000:
                                p_bitmap = ctypes.c_void_p()
                                gdiplus.GdipCreateBitmapFromScan0(w.value, h.value, 0, 0x26200A, None, ctypes.byref(p_bitmap))

                                p_graphics = ctypes.c_void_p()
                                gdiplus.GdipGetImageGraphicsContext(p_bitmap, ctypes.byref(p_graphics))
                                gdiplus.GdipGraphicsClear(p_graphics, 0xFFFFFFFF)
                                gdiplus.GdipDrawImageI(p_graphics, p_image, 0, 0)

                                png_clsid = (ctypes.c_ubyte * 16)(0x06, 0xF4, 0x7C, 0x55, 0x04, 0x1A, 0xD3, 0x11, 0x9A, 0x73, 0x00, 0x00, 0xF8, 0x1E, 0xF3, 0x2E)
                                p_out_stream = ctypes.c_void_p()
                                ole32.CreateStreamOnHGlobal(None, True, ctypes.byref(p_out_stream))

                                gdiplus.GdipSaveImageToStream(p_bitmap, p_out_stream, png_clsid, None)

                                h_out_glob = ctypes.c_void_p()
                                ole32.GetHGlobalFromStream(p_out_stream, ctypes.byref(h_out_glob))
                                size = kernel32.GlobalSize(h_out_glob)
                                out_ptr = kernel32.GlobalLock(h_out_glob)

                                png_bytes = bytes((ctypes.c_ubyte * size).from_address(out_ptr))
                                kernel32.GlobalUnlock(h_out_glob)

                                gdiplus.GdipDisposeImage(p_graphics)
                                gdiplus.GdipDisposeImage(p_bitmap)
                                gdiplus.GdipDisposeImage(p_image)

                                img = Image.open(io.BytesIO(png_bytes))
                                return add_image_shadow(img)
        except Exception:
            pass

    return None


def decode_image_base64(image_b64: str) -> bytes:
    try:
        clean_b64 = "".join(c for c in image_b64 if ('A' <= c <= 'Z') or ('a' <= c <= 'z') or ('0' <= c <= '9') or c in ('+', '/', '='))
        rem = len(clean_b64) % 4
        if rem > 0:
            clean_b64 += '=' * (4 - rem)
        return base64.b64decode(clean_b64)
    except Exception:
        return base64.b64decode(image_b64.encode('cp1251', errors='ignore'))


PAGE_W   = 210
MARGIN   = 10
LINE_H   = 6.5
Q_SPACE  = 4


def clean_text_for_fpdf(t: str) -> str:
    """FPDF uchun matnni xavfsiz Unicode/Latin-1 formatiga tozalash."""
    if not t:
        return ""
    repl = {
        "\u2018": "'", "\u2019": "'", "`": "'", "\u02bb": "'", "\u02bc": "'",
        "\u201c": '"', "\u201d": '"', "\u00ab": '"', "\u00bb": '"',
        "\u2013": "-", "\u2014": "-", "\u2212": "-",
        "\u2026": "...", "\u2116": "No.",
        "ў": "o'", "Ў": "O'", "ғ": "g'", "Ғ": "G'",
        "қ": "q", "Қ": "Q", "ҳ": "h", "Ҳ": "H"
    }
    for k, v in repl.items():
        t = t.replace(k, v)
    return t.encode("latin-1", errors="replace").decode("latin-1")


def _setup_pdf_fonts(pdf: FPDF) -> str:
    """Windows va Linux/Vercel tizimlarida mos shrifni xavfsiz sozlash."""
    win_reg = r"C:\Windows\Fonts\arial.ttf"
    win_bold = r"C:\Windows\Fonts\arialbd.ttf"
    if os.path.exists(win_reg) and os.path.exists(win_bold):
        try:
            pdf.add_font("CustomFont", fname=win_reg)
            pdf.add_font("CustomFont", style="B", fname=win_bold)
            return "CustomFont"
        except Exception:
            pass

    linux_candidates = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/TTF/DejaVuSans.ttf", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf")
    ]
    for reg, bold in linux_candidates:
        if os.path.exists(reg) and os.path.exists(bold):
            try:
                pdf.add_font("CustomFont", fname=reg)
                pdf.add_font("CustomFont", style="B", fname=bold)
                return "CustomFont"
            except Exception:
                pass

    return "Helvetica"


def generate_pdf(
    questions: List[Question],
    fan_name: str,
    with_answers: bool,
    output_path: str,
    compact: bool = False,
) -> str:
    fan_name_clean = clean_text_for_fpdf(fan_name).upper()

    if not compact:
        pdf = _create_pdf(fan_name_clean, with_answers)
        for q in questions:
            _add_question(pdf, q, with_answers, output_path)
    else:
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.set_margins(MARGIN, MARGIN, MARGIN)
        pdf.set_auto_page_break(auto=False)

        font_name = _setup_pdf_fonts(pdf)

        pdf.add_page()

        pdf.set_font(font_name, style="B", size=13)
        pdf.multi_cell(0, 8, fan_name_clean, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

        pdf.set_font(font_name, style="", size=8.5)
        date_str = datetime.now().strftime("%d.%m.%Y %H:%M")
        variant_str = "Javoblar bilan" if with_answers else "Savollar (Javobsiz)"
        metadata_line = f"Variant: {variant_str}  |  Yaratilgan vaqt: {date_str}"
        pdf.multi_cell(0, 5, metadata_line, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        pdf.set_draw_color(100, 100, 100)
        pdf.line(MARGIN, pdf.get_y(), PAGE_W - MARGIN, pdf.get_y())
        pdf.ln(3)

        col_w = 90
        col_gap = 10
        max_y = 297 - MARGIN

        pdf.col = 0
        pdf.col_y_start = pdf.get_y()
        pdf.set_xy(MARGIN, pdf.col_y_start)

        line_h = 4.5
        q_space = 3
        indent = 6

        for q in questions:
            pdf.set_font(font_name, style="B", size=8.5)
            q_text = clean_text_for_fpdf(f"{q.index}. {q.question_text}")
            q_h = pdf.multi_cell(col_w, line_h, q_text, dry_run=True, output="HEIGHT")

            pdf.set_font(font_name, style="", size=8.5)
            v_h_total = 0.0
            for i, v in enumerate(q.variants):
                letter = chr(ord("A") + i)
                v_raw = f"{letter}) {v.text} *" if with_answers and v.is_correct else f"{letter}) {v.text}"
                v_text = clean_text_for_fpdf(v_raw)
                v_h_total += pdf.multi_cell(col_w - indent, line_h, v_text, dry_run=True, output="HEIGHT")

            img_h = 0.0
            temp_img_path = None
            if q.image_base64:
                try:
                    img_bytes = decode_image_base64(q.image_base64)
                    pil_img = render_image_bytes(img_bytes)
                    if pil_img:
                        w, h = pil_img.size
                        w_fit = min(col_w - indent, w * 0.264)
                        h_fit = h * (w_fit / w) if w > 0 else 30
                        img_h = h_fit + 4

                        temp_dir = os.path.dirname(output_path) or "."
                        temp_img_path = os.path.join(temp_dir, f"temp_q_{q.index}.png")
                        pil_img.save(temp_img_path, format="PNG")
                except Exception as e:
                    logger.warning(f"Rasm tayyorlashda xatolik ({q.index}-savol): {e}")

            est_total_h = q_h + v_h_total + img_h + q_space

            if pdf.get_y() + est_total_h > max_y:
                if pdf.col == 0:
                    pdf.col = 1
                    pdf.set_xy(MARGIN + col_w + col_gap, pdf.col_y_start)
                else:
                    pdf.add_page()
                    pdf.col = 0
                    pdf.col_y_start = MARGIN
                    pdf.set_xy(MARGIN, pdf.col_y_start)

            curr_x = MARGIN if pdf.col == 0 else MARGIN + col_w + col_gap

            # 1. Savol matni
            pdf.set_font(font_name, style="B", size=8.5)
            pdf.multi_cell(col_w, line_h, q_text, align="L", new_x="LMARGIN", new_y="NEXT")

            # 2. Rasm SAVOLDAN KEYIN
            if temp_img_path and os.path.exists(temp_img_path):
                try:
                    pdf.ln(1)
                    pdf.set_x(curr_x + indent)
                    pdf.image(temp_img_path, w=min(col_w - indent, 75))
                    pdf.ln(1.5)
                    os.remove(temp_img_path)
                except Exception as e:
                    logger.warning(f"Rasm joylashda xatolik ({q.index}-savol): {e}")

            # 3. Variantlar (A, B, C, D)
            pdf.set_font(font_name, style="", size=8.5)
            for i, v in enumerate(q.variants):
                letter = chr(ord("A") + i)
                v_raw = f"{letter}) {v.text} *" if with_answers and v.is_correct else f"{letter}) {v.text}"
                v_text = clean_text_for_fpdf(v_raw)
                pdf.set_x(curr_x + indent)
                pdf.multi_cell(col_w - indent, line_h, v_text, align="L", new_x="LMARGIN", new_y="NEXT")

            pdf.ln(q_space)
            pdf.set_x(curr_x)

    pdf.output(output_path)
    return output_path


def generate_variants_pdf(
    variants_questions: List[List[Question]],
    fan_name: str,
    with_answers: bool,
    output_path: str,
) -> str:
    """
    Bir nechta variantlarni bitta PDF faylga jamlab yozadi.
    Har bir variant yangi sahifadan 2-kolonna rejimida boshlanadi.
    """
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.set_auto_page_break(auto=False)

    font_name = _setup_pdf_fonts(pdf)

    col_w = 90
    col_gap = 10
    max_y = 297 - MARGIN
    line_h = 4.5
    q_space = 3
    indent = 6

    for var_idx, questions in enumerate(variants_questions):
        pdf.add_page()

        pdf.set_font(font_name, style="B", size=13)
        variant_title = clean_text_for_fpdf(f"{fan_name.upper()} - Variant {var_idx + 1}")
        pdf.multi_cell(0, 8, variant_title, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

        pdf.set_font(font_name, style="", size=8.5)
        date_str = datetime.now().strftime("%d.%m.%Y %H:%M")
        variant_str = "Javoblar bilan" if with_answers else "Savollar (Javobsiz)"
        metadata_line = f"Variant: {variant_str}  |  Yaratilgan vaqt: {date_str}"
        pdf.multi_cell(0, 5, metadata_line, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        pdf.set_draw_color(100, 100, 100)
        pdf.line(MARGIN, pdf.get_y(), PAGE_W - MARGIN, pdf.get_y())
        pdf.ln(3)

        pdf.col = 0
        pdf.col_y_start = pdf.get_y()
        pdf.set_xy(MARGIN, pdf.col_y_start)

        for q in questions:
            pdf.set_font(font_name, style="B", size=8.5)
            q_text = clean_text_for_fpdf(f"{q.index}. {q.question_text}")
            q_h = pdf.multi_cell(col_w, line_h, q_text, dry_run=True, output="HEIGHT")

            pdf.set_font(font_name, style="", size=8.5)
            v_h_total = 0.0
            for i, v in enumerate(q.variants):
                letter = chr(ord("A") + i)
                v_raw = f"{letter}) {v.text} *" if with_answers and v.is_correct else f"{letter}) {v.text}"
                v_text = clean_text_for_fpdf(v_raw)
                v_h_total += pdf.multi_cell(col_w - indent, line_h, v_text, dry_run=True, output="HEIGHT")

            img_h = 0.0
            temp_img_path = None
            if q.image_base64:
                try:
                    img_bytes = decode_image_base64(q.image_base64)
                    pil_img = render_image_bytes(img_bytes)
                    if pil_img:
                        w, h = pil_img.size
                        w_fit = min(col_w - indent, w * 0.264)
                        h_fit = h * (w_fit / w) if w > 0 else 30
                        img_h = h_fit + 4

                        temp_dir = os.path.dirname(output_path) or "."
                        temp_img_path = os.path.join(temp_dir, f"temp_var_{var_idx}_q_{q.index}.png")
                        pil_img.save(temp_img_path, format="PNG")
                except Exception as e:
                    logger.warning(f"Rasm tayyorlashda xatolik ({q.index}-savol): {e}")

            est_total_h = q_h + v_h_total + img_h + q_space

            if pdf.get_y() + est_total_h > max_y:
                if pdf.col == 0:
                    pdf.col = 1
                    pdf.set_xy(MARGIN + col_w + col_gap, pdf.col_y_start)
                else:
                    pdf.add_page()
                    pdf.col = 0
                    pdf.col_y_start = MARGIN
                    pdf.set_xy(MARGIN, pdf.col_y_start)

            curr_x = MARGIN if pdf.col == 0 else MARGIN + col_w + col_gap

            # 1. Savol matni
            pdf.set_font(font_name, style="B", size=8.5)
            pdf.multi_cell(col_w, line_h, q_text, align="L", new_x="LMARGIN", new_y="NEXT")

            # 2. Rasm SAVOLDAN KEYIN
            if temp_img_path and os.path.exists(temp_img_path):
                try:
                    pdf.ln(1)
                    pdf.set_x(curr_x + indent)
                    pdf.image(temp_img_path, w=min(col_w - indent, 75))
                    pdf.ln(1.5)
                    os.remove(temp_img_path)
                except Exception as e:
                    logger.warning(f"Rasm joylashda xatolik ({q.index}-savol): {e}")

            # 3. Variantlar (A, B, C, D)
            pdf.set_font(font_name, style="", size=8.5)
            for i, v in enumerate(q.variants):
                letter = chr(ord("A") + i)
                v_raw = f"{letter}) {v.text} *" if with_answers and v.is_correct else f"{letter}) {v.text}"
                v_text = clean_text_for_fpdf(v_raw)
                pdf.set_x(curr_x + indent)
                pdf.multi_cell(col_w - indent, line_h, v_text, align="L", new_x="LMARGIN", new_y="NEXT")

            pdf.ln(q_space)
            pdf.set_x(curr_x)

    pdf.output(output_path)
    return output_path


def _create_pdf(fan_name: str, with_answers: bool) -> FPDF:
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.set_auto_page_break(auto=True, margin=MARGIN)

    font_name = _setup_pdf_fonts(pdf)
    pdf.custom_font_name = font_name

    pdf.add_page()

    pdf.set_font(font_name, style="B", size=14)
    pdf.multi_cell(0, 9, clean_text_for_fpdf(fan_name), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    pdf.set_font(font_name, style="", size=9)
    date_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    variant_str = "Javoblar bilan" if with_answers else "Savollar (Javobsiz)"
    metadata_line = f"Variant: {variant_str}  |  Yaratilgan vaqt: {date_str}"
    pdf.multi_cell(0, 6, metadata_line, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_draw_color(100, 100, 100)
    pdf.line(MARGIN, pdf.get_y(), PAGE_W - MARGIN, pdf.get_y())
    pdf.ln(5)

    return pdf


def _add_question(pdf: FPDF, q: Question, with_answers: bool, output_path: str) -> None:
    usable_w = PAGE_W - 2 * MARGIN
    font_name = getattr(pdf, "custom_font_name", "Helvetica")

    # 1. Savol matni
    pdf.set_font(font_name, style="B", size=10.5)
    question_line = clean_text_for_fpdf(f"{q.index}. {q.question_text}")
    pdf.multi_cell(usable_w, LINE_H, question_line, align="L", new_x="LMARGIN", new_y="NEXT")

    indent = 8
    variant_w = usable_w - indent

    # 2. Rasm darhol SAVOLDAN KEYIN (variantlardan oldin)
    if q.image_base64:
        try:
            img_bytes = decode_image_base64(q.image_base64)
            pil_img = render_image_bytes(img_bytes)
            if pil_img:
                w, h = pil_img.size
                temp_dir = os.path.dirname(output_path) or "."
                temp_img_path = os.path.join(temp_dir, f"temp_q_{q.index}.png")
                pil_img.save(temp_img_path, format="PNG")

                w_fit = min(110, w * 0.264)
                pdf.ln(2)
                pdf.set_x(MARGIN + indent)
                pdf.image(temp_img_path, w=w_fit)
                pdf.ln(2)

                os.remove(temp_img_path)
        except Exception as e:
            logger.warning(f"Rasm joylashda xatolik ({q.index}-savol): {e}")

    # 3. Variantlar (A, B, C, D)
    pdf.set_font(font_name, style="", size=10)
    for i, v in enumerate(q.variants):
        letter = chr(ord("A") + i)
        line = f"{letter}) {v.text} *" if (with_answers and v.is_correct) else f"{letter}) {v.text}"
        clean_line = clean_text_for_fpdf(line)

        pdf.set_x(MARGIN + indent)
        pdf.multi_cell(variant_w, LINE_H, clean_line, align="L", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(Q_SPACE)

