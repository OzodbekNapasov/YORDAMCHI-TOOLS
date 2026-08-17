import os
import re
import copy
import json
from datetime import datetime
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL

from docbot_config import TEMPLATES as DOCBOT_TEMPLATES, find_template_file
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

DISTRICT_DOCTORS = {
    "Shahrisabz shahar": "O.Norboyev",
    "Kitob tuman": "A.Hasanov",
    "Yakkabog' tuman": "S.B.Jo’rayev",
    "Shahrisabz tuman": "Z.Esanov",
    "Chiroqchi tuman": "Sh.Ro'ziqulov",
    "Qamashi tuman": "Avazov Shuxrat Shukullayevich"
}


def format_amaliyot_muddati(start_date_str: str, end_date_str: str) -> str:
    """Sanani '2026-yil 08-iyunidan  2026-yil 06-iyuligacha' formatiga o'tkazish"""
    uzbek_months = {
        1: ("yanvar", "yanvaridan", "yanvarigacha"),
        2: ("fevral", "fevralidan", "fevraligacha"),
        3: ("mart", "martidan", "martigacha"),
        4: ("aprel", "aprelidan", "apreligacha"),
        5: ("may", "mayidan", "mayigacha"),
        6: ("iyun", "iyunidan", "iyunigacha"),
        7: ("iyul", "iyulidan", "iyuligacha"),
        8: ("avgust", "avgustidan", "avgustigacha"),
        9: ("sentabr", "sentabridan", "sentabrigacha"),
        10: ("oktabr", "oktabridan", "oktabrigacha"),
        11: ("noyabr", "noyabridan", "noyabrigacha"),
        12: ("dekabr", "dekabridan", "dekabrigacha")
    }

    try:
        s_dt = datetime.strptime(start_date_str.strip(), "%d.%m.%Y")
        e_dt = datetime.strptime(end_date_str.strip(), "%d.%m.%Y")

        s_m_str = uzbek_months[s_dt.month][1]  # -dan
        e_m_str = uzbek_months[e_dt.month][2]  # -gacha

        s_day = f"{s_dt.day:02d}"
        e_day = f"{e_dt.day:02d}"

        return f"{s_dt.year}-yil {s_day}-{s_m_str}  {e_dt.year}-yil {e_day}-{e_m_str}"
    except Exception:
        return f"{start_date_str} dan {end_date_str} gacha"


def set_cell_formatted(cell, text, font_name="Times New Roman", font_size=10.5, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, width=None):
    """Jadval katakchasiga Times New Roman shriftida ixcham va tekis matn joylash"""
    cell.text = ""
    p = cell.paragraphs[0] if cell.paragraphs else cell.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(0.5)
    p.paragraph_format.space_after = Pt(0.5)
    p.paragraph_format.line_spacing = 1.0

    run = p.add_run(str(text))
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)

    # Windows va Word uchun Times New Roman rFonts xususiyatini o'rnatish
    rPr = run._r.get_or_add_rPr()
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>')
    rPr.append(rFonts)

    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    if width:
        cell.width = width


def fill_amaliyot_template(template_path: str, data: dict, output_path: str):
    """
    Amaliyot shabloni (.docx) ni to'liq to'ldirib, talabalar jadvalini dinamik kengaytiradi.
    Times New Roman shrifti, qat'iy ustun kengliklari va ixcham qatorlar bilan formatlaydi.
    """
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Amaliyot shabloni topilmadi: {template_path}")

    doc = docx.Document(template_path)

    buyruq_raqami = data.get("buyruq_raqami", "").strip() or "____"
    buyruq_sanasi = data.get("buyruq_sanasi", "").strip() or datetime.now().strftime("%d.%m.%Y")
    tumani = data.get("tumani", "").strip() or "Shahrisabz shahar"
    shu_tuman_shifokori = data.get("shu_tuman_shifokori", "").strip() or DISTRICT_DOCTORS.get(tumani, "Bosh shifokor")
    oquv_yili = data.get("oquv_yili", "").strip() or "2025/2026"
    kursi = str(data.get("kursi", "1")).strip()
    
    # Guruhlar ro'yxatini shakllantirish
    raw_guruhlar = data.get("guruhlar", [])
    if isinstance(raw_guruhlar, str):
        guruhlar = [g.strip() for g in re.split(r'[,; ]+', raw_guruhlar) if g.strip()]
    elif isinstance(raw_guruhlar, list):
        guruhlar = [str(g).strip() for g in raw_guruhlar if str(g).strip()]
    else:
        guruhlar = []

    guruhlar_str = ", ".join(guruhlar) if guruhlar else "101, 102"

    start_date = data.get("start_date", "").strip() or "08.06.2026"
    end_date = data.get("end_date", "").strip() or "06.07.2026"

    amaliyot_muddati = data.get("amaliyot_muddati", "").strip()
    if not amaliyot_muddati and start_date and end_date:
        amaliyot_muddati = format_amaliyot_muddati(start_date, end_date)
    if not amaliyot_muddati:
        amaliyot_muddati = "2026-yil 08-iyunidan  2026-yil 06-iyuligacha"

    replacements = {
        "{{buyruq_raqami}}": buyruq_raqami,
        "{{buyruq_sanasi}}": buyruq_sanasi,
        "{{tumani}}": tumani,
        "{{shu_tuman_shifokori}}": shu_tuman_shifokori,
        "{{oquv_yili}}": oquv_yili,
        "{{kursi}}": kursi,
        "{{guruh_1}}, {{guruh_2}}, {{guruh_3}}": guruhlar_str,
        "{{guruh_1}},{{guruh_2}},{{guruh_3}}": guruhlar_str,
        "{{guruh_1}}": guruhlar[0] if len(guruhlar) > 0 else "",
        "{{guruh_2}}": guruhlar[1] if len(guruhlar) > 1 else "",
        "{{guruh_3}}": guruhlar[2] if len(guruhlar) > 2 else "",
        "{{amaliyot_muddati}}": amaliyot_muddati,
        "{{amaliyot_boshlanish_sanasi}}": start_date,
        "{{amaliyot_tugash_sanasi}}": end_date
    }

    def _replace_in_p(p):
        full_text = p.text
        has_match = False
        for k, v in replacements.items():
            if k in full_text:
                full_text = full_text.replace(k, v)
                has_match = True
        if has_match:
            if p.runs:
                p.runs[0].text = full_text
                for r in p.runs[1:]:
                    r.text = ""
            else:
                p.text = full_text

    # Paragraf matnlarini almashtirish
    for p in doc.paragraphs:
        _replace_in_p(p)

    # 1 va 2-jadvallardagi matnlarni almashtirish
    for t_idx, table in enumerate(doc.tables):
        if t_idx < 2:
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        _replace_in_p(p)

    # 3-Jadval: Talabalar ro'yxati jadvali (Table 2)
    students = data.get("students", [])
    if len(doc.tables) >= 3 and students:
        t = doc.tables[2]

        # 7 ta ustun uchun qat'iy va optimal kengliklar (A4 sahifaga to'liq va tekis sig'ish uchun)
        col_widths = [
            Inches(0.42),  # 0: T/r
            Inches(0.72),  # 1: Guruhi
            Inches(2.55),  # 2: F.I.SH (Keng va 1 qatorga sig'adigan)
            Inches(0.92),  # 3: Boshlanishi
            Inches(0.92),  # 4: Tugashi
            Inches(0.68),  # 5: Bahosi
            Inches(0.68)   # 6: Imzo
        ]

        # Keraksiz shablon qatorlarini tozalash
        while len(t.rows) > len(students) + 1:
            tr = t.rows[-1]._tr
            t._tbl.remove(tr)

        # Agar talabalar ko'proq bo'lsa yangi qatorlar qo'shish
        while len(t.rows) < len(students) + 1:
            new_tr = copy.deepcopy(t.rows[1]._tr)
            t._tbl.append(new_tr)

        # 1. Sarlavha qatorini (Row 0) chiroyli Times New Roman Bold formatlash
        header_titles = [
            "T/r", "Guruhi", "F.I.SH", 
            "Amaliyot boshlanishi vaqti", "Amaliyot tugash vaqti", 
            "Amaliyot bahosi", "Rahbar imzosi"
        ]
        if len(t.rows) > 0:
            for c_idx, cell in enumerate(t.rows[0].cells):
                title = header_titles[c_idx] if c_idx < len(header_titles) else cell.text
                set_cell_formatted(
                    cell, title, 
                    font_name="Times New Roman", font_size=10.0, bold=True, 
                    align=WD_ALIGN_PARAGRAPH.CENTER, width=col_widths[c_idx] if c_idx < len(col_widths) else None
                )

        # 2. Talabalar qatorlarini (Row 1..N) to'ldirish va Times New Roman formatlash
        for idx, st in enumerate(students):
            row = t.rows[idx + 1]
            st_fio = st.get("fio", "").strip()
            st_guruh = st.get("guruhi", "").strip() or (guruhlar[0] if guruhlar else "")
            st_start = st.get("start_date", "").strip() or start_date
            st_end = st.get("end_date", "").strip() or end_date

            # Agar FIO juda uzun bo'lsa 1 qatorda chiroyli sig'ishi uchun 9.5pt, oddiy bo'lsa 10.5pt
            fio_font_size = 9.5 if len(st_fio) > 30 else 10.5

            # Cell 0: T/r
            if len(row.cells) > 0:
                set_cell_formatted(row.cells[0], f"{idx + 1}.", "Times New Roman", 10.5, False, WD_ALIGN_PARAGRAPH.CENTER, col_widths[0])
            # Cell 1: Guruhi
            if len(row.cells) > 1:
                set_cell_formatted(row.cells[1], st_guruh, "Times New Roman", 10.5, False, WD_ALIGN_PARAGRAPH.CENTER, col_widths[1])
            # Cell 2: F.I.SH (Chapdan tekis, 1 qatorda)
            if len(row.cells) > 2:
                set_cell_formatted(row.cells[2], st_fio, "Times New Roman", fio_font_size, False, WD_ALIGN_PARAGRAPH.LEFT, col_widths[2])
            # Cell 3: Amaliyot boshlanishi vaqti
            if len(row.cells) > 3:
                set_cell_formatted(row.cells[3], st_start, "Times New Roman", 10.5, False, WD_ALIGN_PARAGRAPH.CENTER, col_widths[3])
            # Cell 4: Amaliyot tugash vaqti
            if len(row.cells) > 4:
                set_cell_formatted(row.cells[4], st_end, "Times New Roman", 10.5, False, WD_ALIGN_PARAGRAPH.CENTER, col_widths[4])
            # Cell 5: Bahosi (Bo'sh)
            if len(row.cells) > 5:
                set_cell_formatted(row.cells[5], "", "Times New Roman", 10.5, False, WD_ALIGN_PARAGRAPH.CENTER, col_widths[5])
            # Cell 6: Imzo (Bo'sh)
            if len(row.cells) > 6:
                set_cell_formatted(row.cells[6], "", "Times New Roman", 10.5, False, WD_ALIGN_PARAGRAPH.CENTER, col_widths[6])

        # Barcha qatorlar va ustunlar kengligini takroran mustahkamlash
        for r in t.rows:
            for c_i, c in enumerate(r.cells):
                if c_i < len(col_widths):
                    c.width = col_widths[c_i]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    return output_path
