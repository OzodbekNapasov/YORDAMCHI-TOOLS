import os
import re
import copy
import json
from datetime import datetime
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL

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


def fill_amaliyot_template(template_path: str, data: dict, output_path: str):
    """
    Amaliyot shabloni (.docx) ni to'liq to'ldirib, talabalar jadvalini dinamik kengaytiradi.
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

        # Keraksiz shablon qatorlarini tozalash
        while len(t.rows) > len(students) + 1:
            tr = t.rows[-1]._tr
            t._tbl.remove(tr)

        # Agar talabalar ko'proq bo'lsa yangi qatorlar qo'shish
        while len(t.rows) < len(students) + 1:
            new_tr = copy.deepcopy(t.rows[1]._tr)
            t._tbl.append(new_tr)

        # Qatorlarni to'ldirish
        for idx, st in enumerate(students):
            row = t.rows[idx + 1]
            st_fio = st.get("fio", "").strip()
            st_guruh = st.get("guruhi", "").strip() or (guruhlar[0] if guruhlar else "")
            st_start = st.get("start_date", "").strip() or start_date
            st_end = st.get("end_date", "").strip() or end_date

            # Cell 0: T/r
            if len(row.cells) > 0:
                row.cells[0].text = f"{idx + 1}."
                if row.cells[0].paragraphs:
                    row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            # Cell 1: Guruhi
            if len(row.cells) > 1:
                row.cells[1].text = st_guruh
                if row.cells[1].paragraphs:
                    row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            # Cell 2: F.I.SH
            if len(row.cells) > 2:
                row.cells[2].text = st_fio
                if row.cells[2].paragraphs:
                    row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
            # Cell 3: Amaliyot boshlanishi vaqti
            if len(row.cells) > 3:
                row.cells[3].text = st_start
                if row.cells[3].paragraphs:
                    row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            # Cell 4: Amaliyot tugash vaqti
            if len(row.cells) > 4:
                row.cells[4].text = st_end
                if row.cells[4].paragraphs:
                    row.cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            # Cell 5: Bahosi (Bo'sh)
            if len(row.cells) > 5:
                row.cells[5].text = ""
            # Cell 6: Imzo (Bo'sh)
            if len(row.cells) > 6:
                row.cells[6].text = ""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    return output_path
