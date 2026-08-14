# ============================================================
#  services/pdf_maker.py
#  .docx → .pdf va pechat/imzoni PDF ustiga qo'yish
# ============================================================

import os
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

def add_stamp_to_pdf(
    pdf_path: str,
    output_path: str,
    pechat_img_path: str | None,
    imzo_img_path:   str | None,
    stamp_config: dict,
    page_index: int = -1,        # -1 = oxirgi sahifa
) -> None:
    try:
        import fitz  # PyMuPDF
    except Exception as ie:
        print(f"PyMuPDF fitz not available: {ie}")
        return

    doc = fitz.open(pdf_path)
    page_idx = page_index if page_index >= 0 else len(doc) - 1
    page = doc[page_idx]

    mm = 2.8346  # 1 mm = 2.8346 pt (PDF birlik)

    def place_image(img_path: str, cfg: dict) -> None:
        if not img_path or not os.path.exists(img_path):
            return
        x0 = cfg["x_mm"] * mm
        y0 = cfg["y_mm"] * mm
        x1 = x0 + cfg["w_mm"] * mm
        y1 = y0 + cfg["h_mm"] * mm
        rect = fitz.Rect(x0, y0, x1, y1)

        # PNG ni to'g'ri o'qib, alpha kanalini saqlaymiz
        img = Image.open(img_path).convert("RGBA")
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img.save(tmp.name)
        tmp.close()

        page.insert_image(rect, filename=tmp.name, overlay=True)
        os.unlink(tmp.name)

    if pechat_img_path:
        place_image(pechat_img_path, stamp_config.get("pechat", {}))
    if imzo_img_path:
        place_image(imzo_img_path,   stamp_config.get("imzo",   {}))

    doc.save(output_path, deflate=True)
    doc.close()
