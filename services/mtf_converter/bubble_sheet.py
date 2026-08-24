"""
bubble_sheet.py — Rasmiy DTM uslubidagi oq-qora professional Javoblar Varaqasi moduli.
"""

import os
import io
import re
import cv2
import qrcode
import numpy as np
import httpx
import logging
from fpdf import FPDF
from pathlib import Path
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger(__name__)

FONT_REGULAR = r"C:\Windows\Fonts\arial.ttf"
FONT_BOLD    = r"C:\Windows\Fonts\arialbd.ttf"

# Oq-qora printer uchun optimal ranglar (Monoxrom)
COLOR_BLACK        = (0, 0, 0)
COLOR_WHITE        = (255, 255, 255)
COLOR_LIGHT_GRAY   = (242, 242, 242)  # Oq-qora printerda tiniq chiquvchi och kulrang fon chizig'i
COLOR_DARK_TEXT    = (15, 23, 42)


def draw_bubble(pdf: FPDF, cx: float, cy: float, r: float, text: str = "", fill: bool = False, border_color=(0, 0, 0)) -> None:
    """
    Doiracha va ichidagi matnni geometrik 100% markazlashtirib chizadi.
    """
    pdf.set_draw_color(*border_color)
    pdf.set_line_width(0.35)
    
    if fill:
        pdf.set_fill_color(*border_color)
        pdf.circle(cx, cy, r, style="FD")
    else:
        pdf.circle(cx, cy, r, style="D")
        
    if text:
        # 2 xonali sonlar (masalan: 10-30) kichikroq shriftda chiziladi, A-D va 1-9 esa standart
        f_size = 7.2 if len(text) <= 1 else 5.4
        pdf.set_font("Arial", style="B", size=f_size)
        if fill:
            pdf.set_text_color(255, 255, 255)
        else:
            pdf.set_text_color(*border_color)
        
        t_w = pdf.get_string_width(text)
        y_off = 0.9 if len(text) <= 1 else 0.7
        pdf.text(cx - (t_w / 2.0), cy + y_off, text)
        pdf.set_text_color(0, 0, 0)


def generate_qr_code_image(data_text: str):
    qr = qrcode.QRCode(version=1, box_size=4, border=1)
    qr.add_data(data_text)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")


def generate_bubble_sheet_pdf(
    output_path: str,
    fan_name: str,
    num_questions: int = 30,
    test_id: str = "TEST-0000",
    variant_num: int = 1,
    num_variants: int = 1,
    prefill_variant: bool = False
) -> str:
    """
    Oq-qora printer uchun moslashtirilgan, variant raqami va Test ID DTM grid formatidagi A4 Javoblar Varaqasi PDF yaratadi.
    """
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(8, 8, 8)
    pdf.set_auto_page_break(auto=False)
    
    pdf.add_font("Arial", fname=FONT_REGULAR)
    pdf.add_font("Arial", style="B", fname=FONT_BOLD)
    
    v_start = 1
    v_end = num_variants
    
    if num_variants == 1:
        v_start = variant_num
        v_end = variant_num
        
    for v in range(v_start, v_end + 1):
        pdf.add_page()
        
        # ── 1. Alignment markerlar ──
        pdf.set_fill_color(0, 0, 0)
        pdf.rect(8, 8, 10, 10, style="F")
        pdf.rect(192, 8, 10, 10, style="F")
        pdf.rect(8, 279, 10, 10, style="F")
        pdf.rect(192, 279, 10, 10, style="F")
        
        # Chap tomonda bar-kod chiziqchalari
        for bar_y in range(25, 275, 5):
            pdf.rect(8, bar_y, 4, 2.5, style="F")
            
        # ── 2. Top Header Title Area ──
        pdf.set_font("Arial", style="B", size=16)
        pdf.set_text_color(*COLOR_BLACK)
        pdf.text(50, 15, "JAVOBLAR VARAQASI")
        
        pdf.set_font("Arial", style="B", size=9)
        pdf.set_text_color(*COLOR_BLACK)
        fan_disp = f"FAN: {fan_name.upper()}"
        if len(fan_disp) > 42:
            fan_disp = fan_disp[:40] + "..."
        pdf.text(50, 20, fan_disp)
        
        pdf.set_font("Arial", style="", size=8.5)
        pdf.set_text_color(*COLOR_BLACK)
        
        var_text = f"Variant: {v:02d}" if prefill_variant else "Variant: ____"
        pdf.text(50, 24.5, f"Test ID: {test_id}  |  {var_text}")
        
        try:
            qr_content = f"TEST_ID:{test_id}|VARIANT:{v}" if prefill_variant else f"TEST_ID:{test_id}"
            qr_img = generate_qr_code_image(qr_content)
            temp_dir = os.path.dirname(output_path) or "."
            temp_qr_path = os.path.join(temp_dir, f"temp_qr_{test_id}_{v}.png")
            qr_img.save(temp_qr_path)
            pdf.image(temp_qr_path, x=165, y=7, w=22)
            if os.path.exists(temp_qr_path):
                os.remove(temp_qr_path)
        except Exception as e:
            logger.warning(f"QR yaratishda xatolik: {e}")

        # Outer Frame
        pdf.set_draw_color(*COLOR_BLACK)
        pdf.set_line_width(0.6)
        pdf.rect(18, 30, 184, 245, style="D")

        # ── 3. Top Instruction Box (DIQQAT!) ──
        pdf.set_fill_color(*COLOR_WHITE)
        pdf.set_draw_color(*COLOR_BLACK)
        pdf.set_line_width(0.3)
        pdf.rect(22, 33, 176, 32, style="FD")
        
        pdf.set_font("Arial", style="B", size=8.5)
        pdf.set_text_color(*COLOR_BLACK)
        pdf.text(26, 38, "DIQQAT!")
        
        pdf.set_font("Arial", style="", size=7.5)
        pdf.set_text_color(*COLOR_BLACK)
        pdf.text(26, 43.5, "1. Moviy yoki qora sharikli ruchkadan foydalaning.")
        pdf.text(26, 49.0, "2. Har bir savol javoblaridan faqat bittasini doira ichiga to'liq bo'yang.")
        pdf.text(26, 54.5, "3. Doirachadan tashqariga chiqmang va varaqni buklamang.")

        # ── 5. Main Questions Grid (Kattalashtirilgan aylanalar!) ──
        q_max = min(num_questions, 45)
        cols = 2 if q_max <= 30 else 3
        rows_per_col = 15
        
        grid_width = 110
        col_w = grid_width / cols
        
        if cols == 2:
            line_x_offset = 12.0
            x_spacing = 9.6
            bubble_r = 2.9  # diametr 5.8 mm
        else:
            line_x_offset = 10.0
            x_spacing = 6.8
            bubble_r = 2.4  # diametr 4.8 mm
            
        opt_area_w = col_w - line_x_offset
        opt_center = line_x_offset + (opt_area_w / 2.0)
        
        cx_offsets = [
            opt_center - 1.5 * x_spacing,
            opt_center - 0.5 * x_spacing,
            opt_center + 0.5 * x_spacing,
            opt_center + 1.5 * x_spacing
        ]

        # Draw main box for grid (height adjusted to 143 to prevent overlap)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(*COLOR_BLACK)
        pdf.set_line_width(0.4)
        pdf.rect(22, 69, grid_width, 143, style="D")

        # Vertikal fon chiziqlarini chizish (Kulrang)
        for c in range(cols):
            c_x = 22 + c * col_w
            
            # Savol raqami va aylanalar orasidagi vertikal ajratuvchi chiziq
            pdf.set_draw_color(*COLOR_BLACK)
            pdf.set_line_width(0.45)
            pdf.line(c_x + line_x_offset, 77, c_x + line_x_offset, 212)
            
            # A va C variantlari ortida vertikal tekis kulrang fon chiziqlari
            pdf.set_fill_color(*COLOR_LIGHT_GRAY)
            pdf.rect(c_x + cx_offsets[0] - bubble_r - 1.2, 77.2, (bubble_r + 1.2) * 2, 134.5, style="F")
            pdf.rect(c_x + cx_offsets[2] - bubble_r - 1.2, 77.2, (bubble_r + 1.2) * 2, 134.5, style="F")

        # Ustunlar orasini vertikal ajratuvchi chiziq bilan ajratish
        pdf.set_draw_color(*COLOR_BLACK)
        pdf.set_line_width(0.5)
        for c in range(1, cols):
            c_x = 22 + c * col_w
            pdf.line(c_x, 69, c_x, 212)

        # Column Titles Header Box
        pdf.set_fill_color(*COLOR_BLACK)
        pdf.rect(22, 69, grid_width, 8, style="F")
        pdf.set_font("Arial", style="B", size=8)
        pdf.set_text_color(255, 255, 255)
        
        for c in range(cols):
            c_x = 22 + c * col_w
            start_q = c * rows_per_col + 1
            end_q = min((c + 1) * rows_per_col, q_max)
            
            title_text = f"SAVOLLAR ({start_q:02d}-{end_q:02d})"
            t_w = pdf.get_string_width(title_text)
            x_pos = c_x + (col_w - t_w) / 2.0
            pdf.text(x_pos, 74.5, title_text)

        # Sub-header row (№ A B C D)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(*COLOR_BLACK)
        pdf.rect(22, 77, grid_width, 6, style="FD")
        pdf.set_font("Arial", style="B", size=7.0)
        pdf.set_text_color(*COLOR_BLACK)
        
        for c in range(cols):
            c_x = 22 + c * col_w
            num_title_w = pdf.get_string_width("Nº")
            pdf.text(c_x + (line_x_offset / 2.0) - (num_title_w / 2.0), 81.2, "Nº")
            
            for opt_idx, letter in enumerate(["A", "B", "C", "D"]):
                opt_x = c_x + cx_offsets[opt_idx]
                let_w = pdf.get_string_width(letter)
                pdf.text(opt_x - (let_w / 2.0), 81.2, letter)

        # Questions Rows
        for q in range(1, q_max + 1):
            c = (q - 1) // rows_per_col
            r = (q - 1) % rows_per_col
            
            c_x = 22 + c * col_w
            r_baseline = 89.5 + r * 8.4  # Birinchi qator chiziqdan to'liq uzoqlashtirildi
            cy = r_baseline - 1.2

            # Savol raqami matni
            pdf.set_font("Arial", style="B", size=8.5)
            q_str = f"{q:02d}"
            t_w = pdf.get_string_width(q_str)
            pdf.text(c_x + (line_x_offset / 2.0) - (t_w / 2.0), r_baseline, q_str)

            # A, B, C, D doirachalari
            for opt_idx, letter in enumerate(["A", "B", "C", "D"]):
                cx = c_x + cx_offsets[opt_idx]
                draw_bubble(pdf, cx, cy, bubble_r, text=letter, fill=False)

        # ── 6. O'NG TARAFI: O'quvchi Ma'lumotlari Box ──
        right_x = 135
        right_w = 63
        info_y = 69
        info_h = 95
        
        pdf.set_fill_color(*COLOR_BLACK)
        pdf.set_draw_color(*COLOR_BLACK)
        pdf.rect(right_x, info_y, right_w, 6, style="F")
        
        pdf.set_font("Arial", style="B", size=7.5)
        pdf.set_text_color(255, 255, 255)
        pdf.text(right_x + 10, info_y + 4.2, "O'QUVCHI MA'LUMOTLARI")

        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(*COLOR_BLACK)
        pdf.set_line_width(0.35)
        pdf.rect(right_x, info_y, right_w, info_h, style="D")

        # 4 Input Fields
        field_y = info_y + 14
        pdf.set_font("Arial", style="B", size=7.5)
        pdf.set_text_color(*COLOR_BLACK)
        
        pdf.text(right_x + 4, field_y, "1. Familiyasi:")
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.25)
        pdf.line(right_x + 4, field_y + 9, right_x + right_w - 4, field_y + 9)

        field_y += 18
        pdf.text(right_x + 4, field_y, "2. Ismi:")
        pdf.line(right_x + 4, field_y + 9, right_x + right_w - 4, field_y + 9)

        field_y += 18
        pdf.text(right_x + 4, field_y, "3. Otasining ismi:")
        pdf.line(right_x + 4, field_y + 9, right_x + right_w - 4, field_y + 9)

        field_y += 18
        pdf.text(right_x + 4, field_y, "4. Imzosi:")
        pdf.line(right_x + 4, field_y + 9, right_x + right_w - 5, field_y + 9)

        # ── 7. O'NG TARAFI: Natija va Tekshiruv ──
        score_y = 168
        score_h = 44
        pdf.set_fill_color(*COLOR_WHITE)
        pdf.set_draw_color(*COLOR_BLACK)
        pdf.rect(right_x, score_y, right_w, score_h, style="FD")

        # Header
        pdf.set_fill_color(*COLOR_BLACK)
        pdf.rect(right_x, score_y, right_w, 6, style="F")
        pdf.set_font("Arial", style="B", size=7.5)
        pdf.set_text_color(255, 255, 255)
        pdf.text(right_x + 12, score_y + 4.2, "NATIJA VA TEKSHIRUV")

        pdf.set_font("Arial", style="B", size=7.5)
        pdf.set_text_color(*COLOR_BLACK)
        
        # 1. To'g'ri javoblar soni
        pdf.text(right_x + 4, score_y + 11.5, "1. To'g'ri javoblar soni:")
        box_sy = score_y + 14.5
        pdf.rect(right_x + 31.5 - 9.0, box_sy, 8.0, 7.0, style="D")
        pdf.rect(right_x + 31.5 + 1.0, box_sy, 8.0, 7.0, style="D")

        # 2. Yakuniy baho
        pdf.text(right_x + 4, score_y + 27.5, "2. Yakuniy baho:")
        pdf.rect(right_x + 31.5 - 9.0, score_y + 30.5, 18.0, 7.0, style="D")

        # ── 8. BOTTOM: Excel-Style Variant Box (100% to'liq to'rsimon chiziqlar) ──
        bottom_y = 216
        bottom_h = 48
        pdf.set_fill_color(*COLOR_WHITE)
        pdf.set_draw_color(*COLOR_BLACK)
        pdf.set_line_width(0.4)
        pdf.rect(22, bottom_y, 176, bottom_h, style="D")
        
        # Header
        pdf.set_fill_color(*COLOR_BLACK)
        pdf.rect(22, bottom_y, 176, 6, style="F")
        pdf.set_font("Arial", style="B", size=8.0)
        pdf.set_text_color(255, 255, 255)
        t_w = pdf.get_string_width("VARIANT RAQAMI")
        pdf.text(22 + (176 - t_w) / 2.0, bottom_y + 4.2, "VARIANT RAQAMI")
        
        # Sub-instruction
        pdf.set_font("Arial", style="B", size=6.5)
        pdf.set_text_color(*COLOR_BLACK)
        sub_text = "To'g'ri variant raqamini bo'yab belgilang."
        st_w = pdf.get_string_width(sub_text)
        pdf.text(22 + (176 - st_w) / 2.0, bottom_y + 11.5, sub_text)
        
        # Excel Grid o'lchamlari
        grid_x = 26
        grid_w = 168
        grid_y = 228
        grid_h = 36
        col_w_var = 11.2
        bubble_r_var = 2.9
        
        # Excel tashqi ramkasi
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(*COLOR_BLACK)
        pdf.set_line_width(0.35)
        pdf.rect(grid_x, grid_y, grid_w, grid_h, style="D")
        
        # Excel horizontal bo'luvchi chiziq (Row 1 va Row 2 orasida)
        pdf.line(grid_x, grid_y + 18, grid_x + grid_w, grid_y + 18)
        
        # Excel vertikal bo'luvchi chiziqlar (har bir ustun uchun)
        for i in range(1, 15):
            cx_line = grid_x + i * col_w_var
            pdf.line(cx_line, grid_y, cx_line, grid_y + grid_h)
            
        # Row 1 (1 to 15)
        y_row1_bub = grid_y + 9.0
        for col_idx in range(15):
            val = col_idx + 1
            cx = grid_x + 5.6 + col_idx * col_w_var
            is_filled = prefill_variant and (v == val)
            draw_bubble(pdf, cx, y_row1_bub, bubble_r_var, text=str(val), fill=is_filled)
            
        # Row 2 (16 to 30)
        y_row2_bub = grid_y + 27.0
        for col_idx in range(15):
            val = col_idx + 16
            cx = grid_x + 5.6 + col_idx * col_w_var
            is_filled = prefill_variant and (v == val)
            draw_bubble(pdf, cx, y_row2_bub, bubble_r_var, text=str(val), fill=is_filled)

        # ── 9. FOOTER: OMADINGIZNI BERSIN! ──
        pdf.set_font("Arial", style="B", size=8)
        foot_text = "OMADINGIZNI BERSIN!"
        t_w = pdf.get_string_width(foot_text)
        center_x = 22 + (176 - t_w) / 2.0
        
        pdf.line(center_x - 15, 271.5, center_x - 4, 271.5)
        pdf.text(center_x, 272.5, foot_text)
        pdf.line(center_x + t_w + 4, 271.5, center_x + t_w + 15, 271.5)

    pdf.output(output_path)
    return output_path


# ─── OMR Scanner implementation ───

def get_marker_centers(img: np.ndarray) -> list[tuple[int, int]]:
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []
    
    for c in contours:
        area = cv2.contourArea(c)
        if area < 100 or area > (w * h * 0.05):
            continue
            
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        
        rect = cv2.minAreaRect(c)
        bw, bh = rect[1]
        if bw == 0 or bh == 0:
            continue
        ar = bw / float(bh)
        
        if 0.7 <= ar <= 1.3:
            rect_area = bw * bh
            extent = area / rect_area
            if extent > 0.75:
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    candidates.append((cx, cy))
                    
    if len(candidates) < 4:
        return []
        
    tl = min(candidates, key=lambda p: p[0]**2 + p[1]**2)
    tr = min(candidates, key=lambda p: (p[0] - w)**2 + p[1]**2)
    bl = min(candidates, key=lambda p: p[0]**2 + (p[1] - h)**2)
    br = min(candidates, key=lambda p: (p[0] - w)**2 + (p[1] - h)**2)
    
    corners = [tl, tr, br, bl]
    if len(set(corners)) < 4:
        return []
        
    return corners


def warp_image(img: np.ndarray, corners: list[tuple[int, int]]) -> np.ndarray:
    tl, tr, br, bl = corners
    pts_src = np.float32([tl, tr, br, bl])
    pts_dst = np.float32([
        [50, 50],
        [950, 50],
        [950, 1385],
        [50, 1385]
    ])
    matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
    return cv2.warpPerspective(img, matrix, (1000, 1450))


def scan_answers(warped_gray: np.ndarray, num_questions: int = 30) -> tuple[str | None, int | None, dict[int, str]]:
    # QR koddan Test ID va Variantni o'qish (ustuvor)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(warped_gray)
    
    qr_test_id = None
    qr_variant = None
    if data:
        try:
            parts = dict(x.split(":") for x in data.split("|") if ":" in x)
            qr_test_id = parts.get("TEST_ID")
            if "VARIANT" in parts:
                qr_variant = int(parts.get("VARIANT"))
        except Exception:
            pass

    # Matematik jihatdan o'ta aniq millimeter-to-pixel masshtab koeffitsiyentlari
    scale_x = 900.0 / 184.0
    scale_y = 1335.0 / 271.0

    # Excel-Style variant doiralari koordinatalari
    grid_x = 26.0
    col_w_var = 11.2
    y_row1 = 237.0
    y_row2 = 255.0
    
    variant_means = []
    
    for v in range(1, 31):
        if v <= 15:
            cy_mm = y_row1
            col_idx = v - 1
        else:
            cy_mm = y_row2
            col_idx = v - 16
            
        cx_mm = grid_x + 5.6 + col_idx * col_w_var
        
        x_px = int(50.0 + (cx_mm - 13.0) * scale_x)
        y_px = int(50.0 + (cy_mm - 13.0) * scale_y)
        
        # Kattaroq doiralar uchun skanerlash darchasini 20x20 pikselga kattalashtiramiz
        crop = warped_gray[y_px - 10 : y_px + 10, x_px - 10 : x_px + 10]
        variant_means.append(np.mean(crop))
        
    min_v_idx = np.argmin(variant_means)
    sorted_means = sorted(variant_means)
    
    detected_variant = None
    if sorted_means[1] - sorted_means[0] > 12 and sorted_means[0] < 205:
        detected_variant = min_v_idx + 1
        
    final_variant = qr_variant if qr_variant is not None else detected_variant
    
    q_max = min(num_questions, 45)
    cols = 2 if q_max <= 30 else 3
    rows_per_col = 15
    grid_width = 110
    col_w = grid_width / cols
    
    if cols == 2:
        line_x_offset = 12.0
        x_spacing = 9.6
    else:
        line_x_offset = 10.0
        x_spacing = 6.8
        
    opt_area_w = col_w - line_x_offset
    opt_center = line_x_offset + (opt_area_w / 2.0)
    
    cx_offsets = [
        opt_center - 1.5 * x_spacing,
        opt_center - 0.5 * x_spacing,
        opt_center + 0.5 * x_spacing,
        opt_center + 1.5 * x_spacing
    ]
    
    answers = {}
    
    for q in range(1, q_max + 1):
        c = (q - 1) // rows_per_col
        r = (q - 1) % rows_per_col
        
        c_x_mm = 22.0 + c * col_w
        r_y_mm = 88.0 + r * 8.4  # generate_bubble_sheet_pdf dagi yangi baseline ga to'liq moslashtirildi
        
        opt_means = []
        for opt_idx in range(4):
            cx_mm = c_x_mm + cx_offsets[opt_idx]
            cy_mm = r_y_mm - 1.2
            
            x_px = int(50.0 + (cx_mm - 13.0) * scale_x)
            y_px = int(50.0 + (cy_mm - 13.0) * scale_y)
            
            crop = warped_gray[y_px - 10 : y_px + 10, x_px - 10 : x_px + 10]
            opt_means.append(np.mean(crop))
            
        min_opt_idx = np.argmin(opt_means)
        sorted_opt_means = sorted(opt_means)
        
        if sorted_opt_means[1] - sorted_opt_means[0] > 12 and sorted_opt_means[0] < 205:
            answers[q] = chr(ord("A") + min_opt_idx)
        else:
            answers[q] = None
            
    return qr_test_id, final_variant, answers


def get_optimal_warp(img: np.ndarray, corners: list[tuple[int, int]]) -> np.ndarray:
    tl_img, tr_img, br_img, bl_img = corners
    
    # 4 ta mumkin bo'lgan orientatsiya permutatsiyalari
    permutations = [
        ([tl_img, tr_img, br_img, bl_img], "Normal"),
        ([tr_img, br_img, bl_img, tl_img], "90 daraja o'ngga burilgan"),
        ([br_img, bl_img, tl_img, tr_img], "180 daraja burilgan"),
        ([bl_img, tl_img, tr_img, br_img], "90 daraja chapga burilgan")
    ]
    
    detector = cv2.QRCodeDetector()
    best_warped = None
    min_left_right_diff = 9999
    selected_desc = "Normal"
    
    # 1. QR kod orqali aniqlashga harakat qilamiz (eng ishonchli usul)
    for pts_src, desc in permutations:
        pts_src_np = np.float32(pts_src)
        pts_dst = np.float32([
            [50, 50],
            [950, 50],
            [950, 1385],
            [50, 1385]
        ])
        matrix = cv2.getPerspectiveTransform(pts_src_np, pts_dst)
        warped = cv2.warpPerspective(img, matrix, (1000, 1450))
        
        # QR kod joylashgan sohani tekshiramiz (tepa-o'ng burchak)
        qr_zone = warped[10:250, 700:980]
        qr_zone_gray = cv2.cvtColor(qr_zone, cv2.COLOR_BGR2GRAY)
        data, _, _ = detector.detectAndDecode(qr_zone_gray)
        if data:
            logger.info(f"Rasm orientatsiyasi QR kod orqali aniqlandi: {desc}")
            return warped
            
    # 2. Agar QR-kod topilmasa, chap tarafdagi qora bar-kod chiziqlar zichligi bo'yicha aniqlaymiz
    for pts_src, desc in permutations:
        pts_src_np = np.float32(pts_src)
        pts_dst = np.float32([
            [50, 50],
            [950, 50],
            [950, 1385],
            [50, 1385]
        ])
        matrix = cv2.getPerspectiveTransform(pts_src_np, pts_dst)
        warped = cv2.warpPerspective(img, matrix, (1000, 1450))
        warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        
        left_margin = np.mean(warped_gray[100:1300, 20:65])
        right_margin = np.mean(warped_gray[100:1300, 935:980])
        
        top_half = np.mean(warped_gray[50:400, 100:900])
        bottom_half = np.mean(warped_gray[1050:1400, 100:900])
        
        if left_margin < right_margin and bottom_half < top_half:
            diff = left_margin - right_margin
            if diff < min_left_right_diff:
                min_left_right_diff = diff
                best_warped = warped
                selected_desc = desc
                
    if best_warped is not None:
        logger.info(f"Rasm orientatsiyasi bar-kod zichligi bo'yicha aniqlandi: {selected_desc}")
        return best_warped
        
    # 3. Fallback: Normal permutatsiya
    logger.warning("Rasm orientatsiyasini aniqlab bo'lmadi, standart holatda davom etiladi.")
    pts_src_np = np.float32(permutations[0][0])
    pts_dst = np.float32([
        [50, 50],
        [950, 50],
        [950, 1385],
        [50, 1385]
    ])
    matrix = cv2.getPerspectiveTransform(pts_src_np, pts_dst)
    return cv2.warpPerspective(img, matrix, (1000, 1450))


async def process_bubble_sheet_image(
    image_path: str, 
    num_questions: int = 30,
) -> dict:
    img = cv2.imread(image_path)
    if img is None:
        return {"status": "error", "message": "Rasmni yuklab bo'lmadi."}
        
    corners = get_marker_centers(img)
    if not corners or len(corners) < 4:
        return {
            "status": "error", 
            "message": "Javoblar varaqasining 4 ta burchagidagi qora kvadratlar topilmadi. "
                       "Rasmni to'g'ri, yorug' va burchaklar ko'rinadigan qilib qayta yuboring."
        }
        
    try:
        # Avtomatik aylantirilgan to'g'ri rasm formatini olamiz
        warped = get_optimal_warp(img, corners)
        warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        test_id, variant, answers = scan_answers(warped_gray, num_questions)
        
        # Talabaning ismi yozilgan qismni qirqish
        student_info_crop = warped[325:794, 646:955]
        crop_path = os.path.splitext(image_path)[0] + "_student_info.jpg"
        cv2.imwrite(crop_path, student_info_crop)
        
        return {
            "status": "success",
            "test_id": test_id,
            "variant": variant,
            "answers": answers,
            "student_info_path": crop_path
        }
    except Exception as e:
        logger.exception(f"Skanerlashda xatolik: {e}")
        return {"status": "error", "message": f"Skanerlash jarayonida xatolik yuz berdi: {e}"}
