"""
mtf_native_tekshiruv.py — yangi native MTF o'quvchini Mtf2Xml.exe natijasi bilan solishtirish.

Windows kompyuterda (Mtf2Xml.exe ishlaydigan joyda) ishga tushiring:

    python mtf_native_tekshiruv.py "D:\\MyTestX\\tests"

Har bir .mtf fayl uchun ikkala usul natijasini taqqoslaydi: savollar soni, savol matni va
to'g'ri javoblar. Oxirida umumiy hisobot chiqadi. Hammasi mos kelsa, Mtf2Xml.exe endi kerak emas.
"""

import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.mtf_converter.mtf_native import parse_mtf_bytes, to_questions  # noqa: E402
from services.mtf_converter.mtf_converter import convert_mtf_to_xml  # noqa: E402
from services.mtf_converter.xml_parser import parse_xml  # noqa: E402


def norm(t: str) -> str:
    t = (t or "").lower().replace("‘", "'").replace("’", "'").replace("ʻ", "'").replace("`", "'")
    return re.sub(r"\s+", " ", t).strip()


def compare(path: str):
    data = open(path, "rb").read()
    native = to_questions(parse_mtf_bytes(data), with_answers=True)
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, os.path.basename(path))
        with open(src, "wb") as f:
            f.write(data)
        exe = parse_xml(convert_mtf_to_xml(src, work_dir=tmp))

    problems = []
    if len(native) != len(exe):
        problems.append(f"savollar soni: native {len(native)} ≠ exe {len(exe)}")
    for i, (a, b) in enumerate(zip(native, exe), 1):
        if a.question_type not in ("single", "multiple"):
            continue  # tartiblash/moslashtirish exe XML'da boshqacha ifodalanadi
        if norm(a.question_text)[:60] != norm(b.question_text)[:60]:
            problems.append(f"#{i} savol matni farq qiladi: «{a.question_text[:50]}» / «{b.question_text[:50]}»")
            continue
        ca = sorted(norm(v.text) for v in a.variants if v.is_correct)
        cb = sorted(norm(v.text) for v in b.variants if v.is_correct)
        if ca != cb:
            problems.append(f"#{i} to'g'ri javob farq qiladi: native {ca} / exe {cb}")
        if bool(a.image_base64) != bool(b.image_base64):
            problems.append(f"#{i} rasm: native {'bor' if a.image_base64 else 'yo‘q'}, exe {'bor' if b.image_base64 else 'yo‘q'}")
    return len(native), problems


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else r"D:\MyTestX\tests"
    files = [os.path.join(r, f) for r, _, fs in os.walk(folder) for f in fs if f.lower().endswith(".mtf")]
    if not files:
        print(f"{folder} ichida .mtf fayl topilmadi.")
        return
    ok = bad = 0
    for path in sorted(files):
        try:
            count, problems = compare(path)
        except Exception as e:
            count, problems = 0, [f"xatolik: {e}"]
        name = os.path.relpath(path, folder)
        if problems:
            bad += 1
            print(f"❌ {name} ({count} savol)")
            for p in problems[:10]:
                print(f"     - {p}")
        else:
            ok += 1
            print(f"✅ {name} ({count} savol) — to'liq mos")
    print(f"\nJami: {len(files)} ta fayl | mos: {ok} | farqli: {bad}")


if __name__ == "__main__":
    main()
