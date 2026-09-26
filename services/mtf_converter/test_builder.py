"""
test_builder.py — bitta testdan turli hujjatlar yasash:
    * javobsiz / javobli PDF (va xohlasa Word);
    * "faqat A" varianti — har savolda to'g'ri javob A qatorida;
    * N ta savoldan iborat K ta aralash variant + alohida javoblar kaliti.
"""

from __future__ import annotations

import copy
import os
import random
import re
import tempfile
from datetime import datetime
from typing import List, Optional, Tuple

from fpdf import FPDF

from .xml_parser import Question, parse_xml
from .mtf_native import parse_mtf_bytes, to_questions
from .mtf_converter import convert_mtf_to_xml
from .pdf_generator import generate_pdf, generate_variants_pdf, _setup_pdf_fonts, clean_text_for_fpdf
from .docx_generator import generate_docx

# Aralashtirilganda ham o'z joyida qolishi kerak bo'lgan javoblar ("Barchasi to'g'ri" va h.k.)
_PINNED = re.compile(r"(barcha|hammasi|to.?g.?ri javob yo|javob yo.?q|all of|none of|все |нет правил|верны все)", re.I)


def load_questions(data: bytes, filename: str, with_answers: bool = True) -> Tuple[List[Question], str]:
    """(savollar, dvigatel) — avval native o'quvchi, bo'lmasa XML / Mtf2Xml.exe (Windows)."""
    native_error = None
    if not filename.lower().endswith(".xml"):
        try:
            qs = to_questions(parse_mtf_bytes(data), with_answers=with_answers)
            if qs:
                return qs, "native"
        except Exception as e:
            native_error = e
    with tempfile.TemporaryDirectory(prefix="atlas_mtf_") as tmp:
        src = os.path.join(tmp, os.path.basename(filename) or "test.mtf")
        with open(src, "wb") as f:
            f.write(data)
        try:
            xml_path = src if filename.lower().endswith(".xml") else convert_mtf_to_xml(src, work_dir=tmp)
            qs = parse_xml(xml_path) if xml_path and os.path.exists(xml_path) else []
        except Exception as e:
            native_error = native_error or e
            qs = []
    if not qs:
        reason = f" ({native_error})" if native_error else ""
        raise ValueError(f"Fayldan hech qanday test savollari topilmadi: {filename}{reason}")
    return qs, ("xml" if filename.lower().endswith(".xml") else "mtf2xml.exe")


def title_from_filename(filename: str) -> str:
    return os.path.splitext(os.path.basename(filename))[0].replace("_", " ").strip() or "Test"


def _renumber(questions: List[Question]) -> List[Question]:
    for i, q in enumerate(questions, 1):
        q.index = i
    return questions


def answers_first(questions: List[Question]) -> List[Question]:
    """Har savolda to'g'ri javob(lar) A (B...) qatoriga ko'chiriladi, qolganlari asl tartibda."""
    out = []
    for q in questions:
        q2 = copy.deepcopy(q)
        if q2.question_type in ("single", "multiple", "SINGLE_CHOICE", "MULTIPLE_CHOICE", "UNKNOWN") \
                and any(v.is_correct for v in q2.variants) and not all(v.is_correct for v in q2.variants):
            q2.variants = [v for v in q2.variants if v.is_correct] + [v for v in q2.variants if not v.is_correct]
        out.append(q2)
    return out


def _shuffle_options(q: Question, rng: random.Random) -> None:
    if q.question_type not in ("single", "multiple", "SINGLE_CHOICE", "MULTIPLE_CHOICE", "UNKNOWN"):
        return
    movable_idx = [i for i, v in enumerate(q.variants) if not _PINNED.search(v.text or "")]
    movable = [q.variants[i] for i in movable_idx]
    rng.shuffle(movable)
    new = list(q.variants)
    for i, v in zip(movable_idx, movable):
        new[i] = v
    q.variants = new


def unique_questions(questions: List[Question]) -> List[Question]:
    """Aynan takroriy savollarni (matn, rasm va javoblar bir xil) bittaga tushiradi."""
    seen, out = set(), []
    for q in questions:
        key = (re.sub(r"\s+", " ", q.question_text or "").strip().lower(), q.image_base64 or "",
               tuple(sorted((v.text or "").strip().lower() for v in q.variants)))
        if key not in seen:
            seen.add(key)
            out.append(q)
    return out


def make_variants(questions: List[Question], per_variant: int, count: int,
                  seed: Optional[int] = None) -> List[List[Question]]:
    """count ta variant: har biriga per_variant ta savol tasodifiy tanlanadi,
    savollar va javoblar tartibi aralashtiriladi. Savollar yetarli bo'lsa, variantlar
    imkon qadar turli savollardan tuziladi (hamma savol teng ishlatiladi)."""
    questions = unique_questions(questions)
    if not questions:
        raise ValueError("Savollar yo'q")
    per_variant = max(1, min(per_variant, len(questions)))
    count = max(1, count)
    rng = random.Random(seed)
    pool: List[int] = []
    variants = []
    for _ in range(count):
        chosen: List[int] = []
        while len(chosen) < per_variant:
            if not pool:
                pool = list(range(len(questions)))
                rng.shuffle(pool)
            idx = pool.pop()
            if idx not in chosen:
                chosen.append(idx)
            elif len(set(pool) - set(chosen)) == 0:
                pool = []  # qolgan hovuzda yangi savol yo'q — yangi aylana
        rng.shuffle(chosen)
        var = []
        for idx in chosen:
            q = copy.deepcopy(questions[idx])
            _shuffle_options(q, rng)
            var.append(q)
        variants.append(_renumber(var))
    return variants


def answer_letters(q: Question) -> str:
    if q.question_type in ("ordering", "matching", "image_mark"):
        return "—"  # harf bilan ifodalanmaydi (tartib / juftlik / rasmda belgilash)
    letters = "".join(chr(ord("A") + i) for i, v in enumerate(q.variants) if v.is_correct)
    return letters or "—"


# ---------------- PDF / Word baytlari ----------------

def _tmp_path(suffix: str) -> str:
    fd, path = tempfile.mkstemp(suffix=suffix, prefix="atlas_test_")
    os.close(fd)
    return path


def _read_and_remove(path: str) -> bytes:
    try:
        with open(path, "rb") as f:
            return f.read()
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def build_pdf(questions: List[Question], title: str, with_answers: bool) -> bytes:
    path = _tmp_path(".pdf")
    generate_pdf(questions=questions, fan_name=title, with_answers=with_answers, output_path=path, compact=True)
    return _read_and_remove(path)


def build_docx(questions: List[Question], title: str, with_answers: bool) -> bytes:
    path = _tmp_path(".docx")
    generate_docx(questions=questions, fan_name=title, with_answers=with_answers, output_path=path)
    return _read_and_remove(path)


def build_variants_pdf(variants: List[List[Question]], title: str) -> bytes:
    path = _tmp_path(".pdf")
    generate_variants_pdf(variants_questions=variants, fan_name=title, with_answers=False, output_path=path)
    return _read_and_remove(path)


def build_key_pdf(variants: List[List[Question]], title: str) -> bytes:
    """Javoblar kaliti: har variant uchun 10 ustunli jadval (savol raqami / to'g'ri javob)."""
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(12, 12, 12)
    pdf.set_auto_page_break(auto=True, margin=12)
    font = _setup_pdf_fonts(pdf)
    pdf.add_page()
    pdf.set_font(font, style="B", size=14)
    pdf.multi_cell(0, 8, clean_text_for_fpdf(f"{title.upper()} — JAVOBLAR KALITI"), align="C",
                   new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(font, size=9)
    pdf.multi_cell(0, 5, clean_text_for_fpdf(
        f"{len(variants)} ta variant × {len(variants[0]) if variants else 0} ta savol  |  "
        f"{datetime.now().strftime('%d.%m.%Y %H:%M')}  |  Faqat o'qituvchi uchun"),
        align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    cols = 10
    cell_w = (210 - 24) / cols
    for v_idx, var in enumerate(variants, 1):
        rows = (len(var) + cols - 1) // cols
        need = 8 + rows * 12 + 4
        if pdf.get_y() + need > 297 - 12:
            pdf.add_page()
        pdf.set_font(font, style="B", size=11)
        pdf.cell(0, 7, clean_text_for_fpdf(f"{v_idx}-variant"), new_x="LMARGIN", new_y="NEXT")
        for r in range(rows):
            chunk = var[r * cols:(r + 1) * cols]
            pdf.set_font(font, size=8)
            pdf.set_fill_color(235, 238, 242)
            for q in chunk:
                pdf.cell(cell_w, 5.5, str(q.index), border=1, align="C", fill=True)
            pdf.ln()
            pdf.set_font(font, style="B", size=10)
            for q in chunk:
                pdf.cell(cell_w, 6.5, answer_letters(q), border=1, align="C")
            pdf.ln()
        pdf.ln(4)
    return bytes(pdf.output())
