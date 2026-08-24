"""
xml_parser.py — MyTestX XML faylidan test savollari va rasmlarni o'qish moduli.
"""

import re
import base64
import logging
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class Variant:
    text: str
    is_correct: bool


@dataclass
class Question:
    index: int
    question_text: str
    question_type: str = "single"
    score: int = 1
    variants: List[Variant] = field(default_factory=list)
    image_base64: Optional[str] = None

    @property
    def correct_variants(self) -> List[Variant]:
        return [v for v in self.variants if v.is_correct]


def extract_jpeg_from_hex(hex_str: str) -> Optional[str]:
    """RTF FormattedText hex ma'lumotlaridan JPEG rasmini ajratib oladi."""
    if not hex_str:
        return None
    match = re.search(r'FFD8FF.*?FFD9', hex_str, re.IGNORECASE | re.DOTALL)
    if match:
        try:
            b = bytes.fromhex(match.group(0))
            if len(b) > 500:
                return base64.b64encode(b).decode('utf-8')
        except Exception:
            pass
    return None


def parse_xml(xml_path: str) -> List[Question]:
    """
    XML faylidan barcha savollar hamda ularning rasmlarini o'qiydi.
    """
    questions: List[Question] = []
    question_index = 1

    # Yirik XML (100MB+) fayllarni tez va xotirani tejab o'qish uchun iterparse
    context = ET.iterparse(xml_path, events=("end",))

    for event, elem in context:
        if elem.tag == "Task":
            q_text = _get_plain_text(elem, "QuestionText")
            if not q_text:
                elem.clear()
                continue

            q_type = elem.get("Type", "UNKNOWN")
            score = int(elem.get("Score", "1"))

            # 1. Rasm: QuestionImage node dan o'qish
            image_base64 = None
            img_node = elem.find("QuestionImage")
            if img_node is not None and img_node.text and len(img_node.text.strip()) > 50:
                image_base64 = img_node.text.strip()
            else:
                # 2. FormattedText hex ma'lumotlaridan qidirish
                q_text_el = elem.find("QuestionText")
                if q_text_el is not None:
                    fmt_el = q_text_el.find("FormattedText")
                    if fmt_el is not None and fmt_el.text:
                        image_base64 = extract_jpeg_from_hex(fmt_el.text)

            # Variantlarni o'qish
            variants: List[Variant] = []
            variants_node = elem.find("Variants")
            if variants_node is not None:
                for variant_node in variants_node.findall("VariantText"):
                    v_text = _get_plain_text(variant_node, None)
                    is_correct = variant_node.get("CorrectAnswer", "False").lower() == "true"
                    if v_text:
                        variants.append(Variant(text=v_text, is_correct=is_correct))

            questions.append(
                Question(
                    index=question_index,
                    question_text=q_text,
                    question_type=q_type,
                    score=score,
                    variants=variants,
                    image_base64=image_base64,
                )
            )
            question_index += 1
            elem.clear()

    return questions


def _get_plain_text(node: ET.Element, child_tag: Optional[str]) -> str:
    target = node.find(child_tag) if child_tag else node
    if target is None:
        return ""

    plain_text_el = target.find("PlainText")
    if plain_text_el is not None and plain_text_el.text:
        return plain_text_el.text.strip()

    plain_text2_el = target.find("PlainText2")
    if plain_text2_el is not None and plain_text2_el.text:
        return plain_text2_el.text.strip()

    return ""
