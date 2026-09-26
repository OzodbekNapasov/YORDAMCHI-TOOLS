"""
mtf_native.py — MyTestX .mtf fayllarini Mtf2Xml.exe'siz, sof Python'da o'qish.

Asos: Zahar tomonidan teskari muhandislik qilingan ochiq dekoder (MIT litsenziya):
    https://github.com/iamschmuck/MyTestStudentX-.MTF-Decoder
    (shifr, zlib, blok rollari, to'g'ri javob bayroqlari, moslashtirish/tartib turlari)

Bu yerda qo'shilganlar:
    * to'liq RTF → matn konvertori (shrift kodirovkasi \\fcharset, \\'xx va \\uN belgilari) —
      o'zbekcha o', g' va kirill harflari buzilmasligi uchun;
    * savol/javob ichidagi rasmlarni ({\\pict ...} guruhlari) ajratib olish;
    * natijani loyihadagi PDF/DOCX generatorlari tushunadigan Question obyektlariga o'girish.

Format (qisqacha):
    .mtf --XCrypt oqim shifri--> "MyTestX" + versiya + zlib --inflate--> UTF-16LE seriyalash
    Har bir savol/javob matni RTF, oldida u32 uzunlik; uzunlikdan oldingi u32 — blok roli
    (5 = savol, savol turi undan oldingi baytda; 10 = belgilangan element).
    To'g'ri javoblar oxirgi javobdan keyingi "0a 00 00 00" markeridan so'ng har bir javobga
    bittadan u32 (1 = to'g'ri, 0 = noto'g'ri) sifatida saqlanadi.
"""

from __future__ import annotations

import base64
import io
import re
import struct
import zlib
from typing import Any, Dict, List, Optional, Tuple

C1, C2, SEED = 0x6CA9, 0xCE1C, 0x0101

RTF_MARK = "{\\rtf1".encode("utf-16-le")
PICT_MARK = "\\pict".encode("utf-16-le")
FLAG_MARK = b"\x0a\x00\x00\x00"
GAP_MIN = 30

TYPE_NAME = {1: "single", 2: "multiple", 3: "ordering", 4: "matching", 8: "image_mark"}


class MtfNativeError(Exception):
    pass


# ---------------------------------------------------------------------------
# 1. Shifrni ochish va zlib
# ---------------------------------------------------------------------------

# Keyingi holat faqat fb (bir bayt) ga bog'liq: state = (fb*C1 + C2) & 0xFFFF.
# Shuning uchun keyingi kalit baytini 256 elementli jadvaldan olamiz — sikl ancha tezlashadi.
_NEXT_KEY = bytes(((fb * C1 + C2) & 0xFFFF) & 0xFF for fb in range(256))


def xcrypt_decrypt(data: bytes) -> bytes:
    out = bytearray(len(data))
    k = SEED & 0xFF
    nk = _NEXT_KEY
    for i, b in enumerate(data):
        x = b ^ k
        out[i] = x
        k = nk[(x + k) & 0xFF]
    return bytes(out)


def decode_body(data: bytes) -> Tuple[str, bytes]:
    """(versiya, zlib'dan ochilgan tana) qaytaradi."""
    dec = xcrypt_decrypt(data)
    magic = dec[:14].decode("utf-16-le", "replace")
    if not magic.startswith("MyTestX"):
        raise MtfNativeError("Fayl MyTestX .mtf emas yoki parol bilan himoyalangan.")
    vlen = struct.unpack_from("<I", dec, 14)[0]
    version = dec[18:18 + 2 * vlen].decode("utf-16-le", "replace") if vlen < 500 else ""
    start = 18 + 2 * vlen if vlen < 500 else 0
    candidates = []
    if dec[start:start + 1] == b"\x78":
        candidates.append(start)
    for h in (b"\x78\xda", b"\x78\x9c", b"\x78\x01", b"\x78\x5e"):
        pos = dec.find(h)
        if pos >= 0:
            candidates.append(pos)
    for pos in candidates:
        try:
            return version, zlib.decompressobj().decompress(dec[pos:])
        except zlib.error:
            continue
    raise MtfNativeError("Test ma'lumotlari (zlib oqimi) topilmadi.")


# ---------------------------------------------------------------------------
# 2. RTF → matn + rasmlar
# ---------------------------------------------------------------------------

_CHARSET_CODEPAGE = {
    0: "cp1252", 1: "cp1252", 2: "cp1252", 77: "mac_roman", 128: "cp932", 129: "cp949",
    134: "gbk", 136: "cp950", 161: "cp1253", 162: "cp1254", 163: "cp1258", 177: "cp1255",
    178: "cp1256", 186: "cp1257", 204: "cp1251", 238: "cp1250",
}
_SPECIAL = {
    "par": "\n", "line": "\n", "sect": "\n", "tab": "\t", "cell": "\t", "row": "\n",
    "ldblquote": "“", "rdblquote": "”", "lquote": "‘", "rquote": "’",
    "emdash": "—", "endash": "–", "bullet": "•", "emspace": " ", "enspace": " ", "qmspace": " ",
}
# Bu guruhlar matn emas (shriftlar, ranglar, stil jadvali, metama'lumot)
_SKIP_DESTS = {
    "fonttbl", "colortbl", "stylesheet", "info", "listtable", "listoverridetable",
    "rsidtbl", "generator", "themedata", "colorschememapping", "datastore", "latentstyles",
    "xmlnstbl", "mmathPr", "header", "footer", "object", "nonshppict", "fldinst",
}
_TOKEN = re.compile(r"\\([a-zA-Z]+)(-?\d+)? ?|\\'([0-9a-fA-F]{2})|\\([^a-zA-Z])|([{}])|([^\\{}]+)", re.S)


def _pict_to_image(pict_rtf: str) -> Optional[bytes]:
    """{\\pict ...} guruhidan rasm baytlarini olish (PNG/JPEG to'g'ridan-to'g'ri, qolganlari PNG'ga)."""
    kind = "png" if "\\pngblip" in pict_rtf else "jpeg" if "\\jpegblip" in pict_rtf else \
        "dib" if "\\dibitmap" in pict_rtf else "wmf" if "\\wmetafile" in pict_rtf else \
        "emf" if "\\emfblip" in pict_rtf else "other"
    # Boshqaruv so'zlarini olib tashlab, faqat hex ma'lumotni qoldiramiz
    body = re.sub(r"\\[a-zA-Z]+-?\d* ?", " ", pict_rtf)
    body = re.sub(r"[{}]", " ", body)
    hexdata = re.sub(r"[^0-9a-fA-F]", "", body)
    if len(hexdata) < 200:
        return None
    try:
        raw = bytes.fromhex(hexdata[: len(hexdata) - (len(hexdata) % 2)])
    except ValueError:
        return None
    if kind in ("png", "jpeg"):
        return raw
    if kind == "dib":
        # Device-independent bitmap: BMP fayl sarlavhasini qo'shamiz
        try:
            hdr_size = struct.unpack_from("<I", raw, 0)[0]
            bpp = struct.unpack_from("<H", raw, 14)[0]
            colors = struct.unpack_from("<I", raw, 32)[0] if hdr_size >= 36 else 0
            if bpp <= 8 and colors == 0:
                colors = 1 << bpp
            off = 14 + hdr_size + colors * 4
            raw = b"BM" + struct.pack("<IHHI", 14 + len(raw), 0, 0, off) + raw
        except struct.error:
            return None
    # BMP/WMF/EMF va boshqalar — PIL ochsa PNG'ga aylantiramiz, aks holda o'tkazib yuboramiz
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(raw))
        img.load()
        buf = io.BytesIO()
        img.convert("RGB" if img.mode not in ("RGB", "RGBA", "L") else img.mode).save(buf, "PNG")
        return buf.getvalue()
    except Exception:
        # Ma'lum sarlavhali rasm to'g'ridan-to'g'ri hex ichida bo'lishi mumkin
        for sig, end in ((b"\x89PNG", b"IEND\xaeB`\x82"), (b"\xff\xd8\xff", b"\xff\xd9")):
            s = raw.find(sig)
            if s >= 0:
                e = raw.rfind(end)
                if e > s:
                    return raw[s:e + len(end)]
        return None


def _group_end(rtf: str, start: int) -> int:
    """start dagi "{" guruhining yopiluvchi "}" dan keyingi indeks."""
    depth = 0
    i = start
    n = len(rtf)
    while i < n:
        c = rtf[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return n


def rtf_to_text_and_images(rtf: str) -> Tuple[str, List[bytes]]:
    """RTF matnini oddiy matnga o'giradi va ichidagi rasmlarni qaytaradi."""
    images: List[bytes] = []
    out: List[str] = []
    fonts: Dict[int, str] = {}
    default_cp = "cp1251"
    m = re.search(r"\\ansicpg(\d+)", rtf)
    if m:
        default_cp = "cp" + m.group(1)

    # Shrift jadvali: \fN ... \fcharsetM  (guruh chegarasi qavslarni sanab topiladi)
    ft_start = rtf.find("{\\fonttbl")
    if ft_start >= 0:
        ft_end = _group_end(rtf, ft_start)
        for fm in re.finditer(r"\\f(\d+)[^;]*?\\fcharset(\d+)", rtf[ft_start:ft_end]):
            fonts[int(fm.group(1))] = _CHARSET_CODEPAGE.get(int(fm.group(2)), default_cp)
    deff = re.search(r"\\deff(\d+)", rtf)

    # Holat steki: (skip, codepage, uc)
    stack: List[Tuple[bool, str, int]] = []
    skip, uc = False, 1
    cp = fonts.get(int(deff.group(1)), default_cp) if deff else default_cp
    nonshp_depth = -1  # {\nonshppict ...} — eski dasturlar uchun takroriy (WMF) rasm, olinmaydi
    pending_skip = 0  # \uN dan keyingi zaxira belgilar soni
    group_start_for_pict: Optional[int] = None
    depth = 0
    pict_depth = -1
    pos = 0
    n = len(rtf)
    raw_bytes = bytearray()

    def flush():
        if raw_bytes:
            out.append(bytes(raw_bytes).decode(cp, "replace"))
            raw_bytes.clear()

    while pos < n:
        mt = _TOKEN.match(rtf, pos)
        if not mt:
            pos += 1
            continue
        pos = mt.end()
        word, param, hexbyte, sym, brace, text = mt.groups()

        if brace == "{":
            flush()
            stack.append((skip, cp, uc))
            depth += 1
            # {\pict ...} guruhini to'liq ajratib olamiz
            if rtf.startswith("\\pict", pos) and pict_depth == -1 and nonshp_depth == -1:
                group_start_for_pict = mt.start()
                pict_depth = depth
            continue
        if brace == "}":
            flush()
            if pict_depth == depth and group_start_for_pict is not None:
                img = _pict_to_image(rtf[group_start_for_pict:pos])
                if img:
                    images.append(img)
                group_start_for_pict, pict_depth = None, -1
            if nonshp_depth == depth:
                nonshp_depth = -1
            depth -= 1
            if stack:
                skip, cp, uc = stack.pop()
            continue
        if pict_depth != -1:
            continue  # rasm ichidagi hex matn sifatida chiqmasin

        if word is not None:
            if word == "nonshppict" and nonshp_depth == -1:
                nonshp_depth = depth
            if word in _SKIP_DESTS or word == "pict":
                skip = True
                continue
            if skip:
                continue
            if word == "f" and param is not None:
                flush()
                cp = fonts.get(int(param), default_cp)
            elif word == "uc" and param is not None:
                uc = int(param)
            elif word == "u" and param is not None:
                flush()
                code = int(param)
                out.append(chr(code + 65536 if code < 0 else code))
                pending_skip = uc
            elif word in _SPECIAL:
                flush()
                out.append(_SPECIAL[word])
            continue
        if sym is not None:
            if sym == "*":
                skip = True  # \* — noma'lum qo'shimcha guruh
            elif skip:
                continue
            elif sym in "{}\\":
                flush()
                out.append(sym)
            elif sym == "~":
                flush()
                out.append(" ")
            elif sym == "_":
                flush()
                out.append("-")
            elif sym in "\r\n":
                flush()
                out.append("\n")  # "\" + qator oxiri = \par
            continue
        if skip:
            continue
        if hexbyte is not None:
            if pending_skip:
                pending_skip -= 1
                continue
            raw_bytes.append(int(hexbyte, 16))
            continue
        if text is not None:
            flush()
            t = text.replace("\r", "").replace("\n", "")
            if pending_skip and t:
                drop = min(pending_skip, len(t))
                t = t[drop:]
                pending_skip -= drop
            out.append(t)
    flush()

    txt = "".join(out)
    txt = re.sub(r"[ \t]+", " ", txt)
    txt = re.sub(r" *\n *", "\n", txt)
    txt = re.sub(r"\n{2,}", "\n", txt)
    return txt.strip(), images


# ---------------------------------------------------------------------------
# 3. Tuzilmani o'qish (asl dekoder mantiqi)
# ---------------------------------------------------------------------------

def _u32(b: bytes, o: int) -> int:
    return struct.unpack_from("<I", b, o)[0] if 0 <= o and o + 4 <= len(b) else -1


def _plain_strings(body: bytes, limit: int = 6) -> List[str]:
    out: List[str] = []
    i = 0
    while i + 4 <= len(body) and len(out) < limit:
        ln = _u32(body, i)
        if 0 < ln < 500 and i + 4 + 2 * ln <= len(body):
            try:
                s = body[i + 4:i + 4 + 2 * ln].decode("utf-16-le")
                if "rtf1" not in s and sum(1 for c in s if 0x20 <= ord(c) < 0x500) / len(s) > 0.9:
                    out.append(s)
                    i += 4 + 2 * ln
                    continue
            except UnicodeDecodeError:
                pass
        i += 1
    return out


# Rasm fayl nomi: "{GUID}.bmp" (UTF-16LE). Savol yozuvida — havola (keyingi u32 = 0),
# tana oxiridagi resurs jadvalida — "{GUID}.ext" + u32 hajm + rasm baytlari.
_RES_NAME = re.compile(rb"\{\x00(?:[0-9A-Fa-f]\x00|-\x00){36}\}\x00\.\x00(?:[A-Za-z0-9]\x00){3,4}")
_IMG_SIGS = (b"BM", b"\xff\xd8\xff", b"\x89PNG", b"GIF8", b"\xd7\xcd\xc6\x9a", b"\x01\x00\x00\x00")


def _resources(body: bytes) -> Dict[str, bytes]:
    """Tana ichidagi rasm resurslari: {"{GUID}.bmp": baytlar}."""
    out: Dict[str, bytes] = {}
    for m in _RES_NAME.finditer(body):
        size = _u32(body, m.end())
        if 0 < size < 60_000_000 and m.end() + 4 + size <= len(body):
            data = body[m.end() + 4:m.end() + 4 + size]
            if data.startswith(_IMG_SIGS):
                out[body[m.start():m.end()].decode("utf-16-le")] = data
    return out


def _to_web_image(data: bytes) -> Optional[bytes]:
    """BMP/WMF va boshqalarni PDF/Word uchun ixcham JPEG/PNG'ga o'giradi."""
    if data.startswith((b"\xff\xd8\xff", b"\x89PNG")):
        return data
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(data))
        img.load()
        buf = io.BytesIO()
        if img.mode in ("RGBA", "LA", "P"):
            img.convert("RGBA").save(buf, "PNG", optimize=True)
        else:
            img.convert("RGB").save(buf, "JPEG", quality=85, optimize=True)
        return buf.getvalue()
    except Exception:
        return None


def _blobs(body: bytes) -> List[Dict[str, Any]]:
    out = []
    i = 0
    n = len(body)
    while True:
        j = body.find(RTF_MARK, i)
        if j < 0:
            break
        i = j + 2
        if j < 9:
            continue
        ln = _u32(body, j - 4)
        if not (0 < ln < 4_000_000 and j + 2 * ln <= n):
            continue
        end = j + 2 * ln
        rtf = body[j:end].decode("utf-16-le", "replace")
        text, images = rtf_to_text_and_images(rtf)
        out.append({"off": j, "end": end, "text": text, "images": images,
                    "pre": _u32(body, j - 8), "type": body[j - 9]})
        i = end
    return out


def _read_flags(body: bytes, frm: int, to: int, n: int) -> Optional[List[bool]]:
    pos = frm
    while True:
        m = body.find(FLAG_MARK, pos, to)
        if m < 0:
            return None
        flags: List[bool] = []
        ok = True
        s = 0
        for k in range(n):
            v = _u32(body, m + 4 + 4 * k)
            if v == 1:
                flags.append(True)
                s += 1
            elif v == 0:
                flags.append(False)
            else:
                ok = False
                break
        if ok and s >= 1:
            return flags
        pos = m + 4


def _read_perm(body: bytes, frm: int, to: int, n: int, right_count: int) -> Optional[List[int]]:
    pos = frm
    while True:
        m = body.find(FLAG_MARK, pos, to)
        if m < 0:
            return None
        perm: List[int] = []
        ok = True
        for k in range(n):
            v = _u32(body, m + 4 + 4 * k)
            if 1 <= v <= right_count:
                perm.append(v)
            else:
                ok = False
                break
        if ok and len(set(perm)) == n:
            return perm
        pos = m + 4


def _read_polygon(body: bytes, lastend: int, nextoff: int) -> Optional[List[int]]:
    for c in range(1, 17):
        cp = nextoff - 18 - 8 * c
        if cp < lastend or cp < 0:
            break
        if _u32(body, cp) != c:
            continue
        xs, ys, ok = [], [], True
        for k in range(c):
            xx = _u32(body, cp + 4 + 8 * k)
            yy = _u32(body, cp + 8 + 8 * k)
            if not (0 <= xx <= 5000 and 0 <= yy <= 5000):
                ok = False
                break
            xs.append(xx)
            ys.append(yy)
        if ok and xs and max(xs) > min(xs):
            return [min(xs), min(ys), max(xs), max(ys)]
    return None


def parse_mtf_bytes(data: bytes) -> Dict[str, Any]:
    """.mtf baytlaridan test tuzilmasini qaytaradi: name, author, version, questions."""
    version, body = decode_body(data)
    resources = _resources(body)
    blobs = _blobs(body)
    converted: Dict[str, Optional[bytes]] = {}
    if resources:
        # Blokdan keyin (keyingi blokkacha) turgan "{GUID}.ext" havolasi — shu blokning rasmi
        for k, b in enumerate(blobs):
            limit = blobs[k + 1]["off"] - 4 if k + 1 < len(blobs) else min(len(body), b["end"] + 400)
            m = _RES_NAME.search(body, b["end"], limit)
            if m and _u32(body, m.end()) == 0:
                name = body[m.start():m.end()].decode("utf-16-le")
                if name in resources:
                    if name not in converted:
                        converted[name] = _to_web_image(resources[name])
                    if converted[name]:
                        b["images"] = b["images"] + [converted[name]]

    questions: List[Dict[str, Any]] = []
    cur: Optional[Dict[str, Any]] = None
    prev_end = 0
    for b in blobs:
        gap = (b["off"] - 4) - prev_end
        prev_end = b["end"]
        if not b["text"] and not b["images"]:
            continue
        if gap >= GAP_MIN and b["pre"] == 5:
            if questions:
                questions[-1]["nextoff"] = b["off"]
            cur = {"type": b["type"], "text": b["text"], "images": list(b["images"]), "items": [],
                   "lastend": b["end"], "nextoff": len(body)}
            questions.append(cur)
        elif cur is not None:
            cur["items"].append({"text": b["text"], "images": b["images"],
                                 "marked": gap >= GAP_MIN and b["pre"] == 10,
                                 "off": b["off"], "end": b["end"]})
            cur["lastend"] = b["end"]

    result = []
    for q in questions:
        items = q["items"]
        t = q["type"]
        entry: Dict[str, Any] = {"type": t, "kind": TYPE_NAME.get(t, "single"),
                                 "text": q["text"], "image": q["images"][0] if q["images"] else None}
        if t == 3:
            entry["order"] = [it["text"] or "(rasm)" for it in items]
            if len(entry["order"]) < 2:
                continue
        elif t == 4:
            marked_idx = [i for i, it in enumerate(items) if it["marked"]]
            split = marked_idx[1] if len(marked_idx) >= 2 else -1
            pairs = []
            if split > 0:
                left, right = items[:split], items[split:]
                perm = _read_perm(body, left[-1]["end"], right[0]["off"] - 4, len(left), len(right))
                for i in range(len(left)):
                    ri = (perm[i] if perm else i + 1) - 1
                    if 0 <= ri < len(right):
                        pairs.append([left[i]["text"], right[ri]["text"]])
            if len(pairs) < 2:
                continue
            entry["pairs"] = pairs
        elif t == 8:
            entry["mark"] = _read_polygon(body, q["lastend"], q["nextoff"])
        else:
            n = len(items)
            flags = _read_flags(body, q["lastend"], min(q["nextoff"], q["lastend"] + 512), n)
            if flags is None:
                flags = [it["marked"] for it in items]
            answers = [{"text": items[i]["text"] or "(rasm)", "correct": bool(flags[i]),
                        "image": items[i]["images"][0] if items[i]["images"] else None}
                       for i in range(n)]
            if len(answers) < 2 or not any(a["correct"] for a in answers):
                continue
            entry["multiple"] = t == 2 or sum(a["correct"] for a in answers) > 1
            entry["answers"] = answers
        if not entry["text"] and entry["image"]:
            entry["text"] = "Rasmga qarang:"
        result.append(entry)

    meta = _plain_strings(body)
    return {"name": meta[0] if meta else "", "author": meta[1] if len(meta) > 1 else "",
            "version": version, "questions": result}


# ---------------------------------------------------------------------------
# 4. Loyiha generatorlari uchun Question obyektlari
# ---------------------------------------------------------------------------

def to_questions(parsed: Dict[str, Any], with_answers: bool = True):
    """parse_mtf_bytes natijasini xml_parser.Question ro'yxatiga o'giradi."""
    from .xml_parser import Question, Variant

    out = []
    for idx, q in enumerate(parsed.get("questions", []), 1):
        text = q["text"]
        variants: List[Variant] = []
        kind = q["kind"]
        if kind in ("single", "multiple"):
            variants = [Variant(text=a["text"], is_correct=a["correct"]) for a in q["answers"]]
        elif kind == "ordering":
            text += "\n(To'g'ri ketma-ketlikni tiklang)"
            items = q["order"] if with_answers else sorted(q["order"], key=str.lower)
            variants = [Variant(text=(f"{i}) {s}" if with_answers else s), is_correct=with_answers)
                        for i, s in enumerate(items, 1)]
        elif kind == "matching":
            text += "\n(Mos juftliklarni toping)"
            if with_answers:
                variants = [Variant(text=f"{l} — {r}", is_correct=True) for l, r in q["pairs"]]
            else:
                rights = sorted((r for _, r in q["pairs"]), key=str.lower)
                text += "\n" + "\n".join(f"{i}) {l}" for i, (l, _) in enumerate(q["pairs"], 1))
                variants = [Variant(text=r, is_correct=False) for r in rights]
        elif kind == "image_mark":
            text += "\n(Rasmda to'g'ri joyni belgilang)"
            if with_answers and q.get("mark"):
                x0, y0, x1, y1 = q["mark"]
                variants = [Variant(text=f"To'g'ri hudud: x {x0}–{x1}, y {y0}–{y1} (piksel)", is_correct=True)]
        img_b64 = base64.b64encode(q["image"]).decode("ascii") if q.get("image") else None
        out.append(Question(index=idx, question_text=text, question_type=kind,
                            variants=variants, image_base64=img_b64))
    return out
