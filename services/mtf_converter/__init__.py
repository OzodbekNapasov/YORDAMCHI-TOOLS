"""
MTF Converter Service Package for ATLAS Platform.
Provides full end-to-end conversion from MyTestX .mtf / .xml files to high-quality PDF, Word .docx, and JSON.
"""

import os
import io
import tempfile
from typing import List, Dict, Any, Optional

from .mtf_converter import convert_mtf_to_xml
from .xml_parser import parse_xml, Question, Variant
from .pdf_generator import generate_pdf, generate_variants_pdf
from .docx_generator import generate_docx


def process_mtf_to_pdf(
    mtf_bytes: bytes,
    filename: str,
    layout: str = "2col",
    with_answers: bool = True,
    with_bubble: bool = False,
    fan_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Bytes shaklidagi .mtf yoki .xml faylni qabul qilib, PDF va DOCX fayllarini generatsiya qiladi.
    """
    clean_stem = os.path.splitext(filename)[0]
    subject_title = fan_name or clean_stem.replace("_", " ").title()

    temp_dir = tempfile.mkdtemp(prefix="atlas_mtf_")
    try:
        temp_input = os.path.join(temp_dir, filename)
        with open(temp_input, "wb") as f:
            f.write(mtf_bytes)

        # 1. XML ga o'girish
        if filename.lower().endswith(".xml"):
            xml_path = temp_input
        else:
            xml_path = convert_mtf_to_xml(temp_input, work_dir=temp_dir)

        # 2. XML dan savollarni o'qish
        questions: List[Question] = parse_xml(xml_path)
        if not questions:
            raise ValueError(f"Fayldan hech qanday test savollari topilmadi: {filename}")

        # 3. PDF yaratish
        pdf_out_path = os.path.join(temp_dir, f"{clean_stem}.pdf")
        compact_mode = (layout == "2col" or layout == "compact")
        generate_pdf(
            questions=questions,
            fan_name=subject_title,
            with_answers=with_answers,
            output_path=pdf_out_path,
            compact=compact_mode
        )

        with open(pdf_out_path, "rb") as f:
            pdf_data = f.read()

        # 4. DOCX yaratish
        docx_out_path = os.path.join(temp_dir, f"{clean_stem}.docx")
        try:
            generate_docx(
                questions=questions,
                fan_name=subject_title,
                with_answers=with_answers,
                output_path=docx_out_path
            )
            with open(docx_out_path, "rb") as f:
                docx_data = f.read()
        except Exception:
            docx_data = None

        return {
            "success": True,
            "filename": filename,
            "title": subject_title,
            "questions_count": len(questions),
            "pdf_bytes": pdf_data,
            "docx_bytes": docx_data,
            "questions_summary": [
                {
                    "index": q.index,
                    "text": q.question_text[:120] + "..." if len(q.question_text) > 120 else q.question_text,
                    "variants_count": len(q.variants),
                    "has_image": bool(q.image_base64),
                    "correct_answers": [v.text for v in q.correct_variants]
                }
                for q in questions[:10]
            ]
        }
    finally:
        pass
