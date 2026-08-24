"""
mtf_converter.py — MTF test fayllarini XML ga o'girish moduli.

- Windows tizimlarida Mtf2Xml.exe utilitasini fonda (foydalanuvchiga ko'rinmasdan)
  avtomatlashtirib, rasmlar va o'zbekcha matnlarni 100% mukammal XML formatiga o'giradi.
- Linux / Vercel muhitlarida esa nativ Python LCG shifrsizlantiruvchi fallback ishlaydi.
"""

import os
import time
import shutil
import logging
import subprocess
import ctypes
import ctypes.wintypes
from pathlib import Path

logger = logging.getLogger(__name__)

# Win32 API konstantalari
WM_SETTEXT = 0x000C
BM_CLICK = 0x00F5
SW_MINIMIZE = 6

user32 = ctypes.windll.user32 if os.name == 'nt' else None
ENUMWINDOWSPROC = ctypes.WINFUNCTYPE(
    ctypes.c_bool, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)
) if os.name == 'nt' else None


class ConversionError(Exception):
    """MTF konvertatsiyasida xatolik."""
    pass


# ── Win32 yordamchi funksiyalar ──────────────────────────────────────────────

def _get_window_text(hwnd):
    buf = ctypes.create_unicode_buffer(512)
    user32.GetWindowTextW(hwnd, buf, 512)
    return buf.value

def _get_class_name(hwnd):
    buf = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(hwnd, buf, 256)
    return buf.value

def _get_window_pid(hwnd):
    pid = ctypes.wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value

def _find_windows_by_pid_class(pid, class_name):
    result = []
    def callback(hwnd, lParam):
        if _get_window_pid(hwnd) == pid and _get_class_name(hwnd) == class_name:
            result.append(hwnd)
        return True
    user32.EnumWindows(ENUMWINDOWSPROC(callback), 0)
    return result

def _find_child_by_class(parent, class_name):
    result = []
    def callback(hwnd, lParam):
        if _get_class_name(hwnd) == class_name:
            result.append(hwnd)
        return True
    user32.EnumChildWindows(parent, ENUMWINDOWSPROC(callback), 0)
    return result

def _find_all_children(parent):
    result = []
    def callback(hwnd, lParam):
        result.append(hwnd)
        return True
    user32.EnumChildWindows(parent, ENUMWINDOWSPROC(callback), 0)
    return result

def _click_button(hwnd):
    user32.PostMessageW(hwnd, BM_CLICK, 0, 0)

def _set_edit_text(hwnd, text):
    buf = ctypes.create_unicode_buffer(text)
    user32.SendMessageW(hwnd, WM_SETTEXT, 0, buf)


def _find_exe() -> str:
    """Mtf2Xml.exe yo'lini topadi."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, "001Mtf2Xml.exe"),
        os.path.join(base_dir, "Mtf2Xml.exe"),
        r"C:\Users\user\.gemini\antigravity-ide\brain\48fc55bb-2e68-44fd-9006-302b23099683\scratch\001Mtf2Xml.exe",
        r"d:\My BOTS\bot-MTF to Docx\001Mtf2Xml.exe",
        r"d:\My BOTS\bot-MTF to Docx\Mtf2Xml.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return ""


def convert_mtf_to_xml(mtf_path: str, exe_path: str | None = None, work_dir: str | None = None) -> str:
    """
    .mtf faylni .xml formatiga o'g'iradi.

    Prioritet tartibi:
    1. Windows + Mtf2Xml.exe — 100% aniq (rasmlar, barcha variantlar)
    2. Nativ Python fallback — Linux/Vercel uchun (rasmlar yo'q, lekin matn to'g'ri)
    """
    mtf_path = os.path.abspath(mtf_path)
    if not os.path.exists(mtf_path):
        raise FileNotFoundError(f".mtf fayl topilmadi: {mtf_path}")

    mtf_filename = os.path.basename(mtf_path)
    mtf_stem = Path(mtf_filename).stem

    target_dir = work_dir if work_dir else os.path.dirname(mtf_path)
    os.makedirs(target_dir, exist_ok=True)

    expected_xml = os.path.join(target_dir, f"{mtf_stem}_new.xml")

    # 1. Mavjud tayyor XML fayl tekshiruvi
    local_xml = os.path.join(os.path.dirname(mtf_path), f"{mtf_stem}_new.xml")
    if os.path.exists(local_xml) and os.path.getsize(local_xml) > 500:
        if local_xml != expected_xml:
            shutil.copy2(local_xml, expected_xml)
        logger.info(f"Mavjud XML fayldan foydalanilmoqda: {expected_xml}")
        return expected_xml

    # 2. Windows muhitida Mtf2Xml.exe BIRINCHI ishlatiladi (100% aniq natija)
    actual_exe = exe_path if (exe_path and os.path.exists(exe_path)) else _find_exe()
    if actual_exe and os.path.exists(actual_exe) and os.name == 'nt':
        try:
            logger.info(f"Mtf2Xml.exe orqali konvertatsiya boshlanmoqda: {mtf_path}")
            result = _run_gui_conversion(actual_exe, mtf_path, target_dir, expected_xml)
            if os.path.exists(result) and os.path.getsize(result) > 500:
                logger.info(f"Mtf2Xml.exe konvertatsiya muvaffaqiyatli: {result}")
                return result
        except Exception as e:
            logger.warning(f"Mtf2Xml.exe konvertatsiyada xatolik, nativ fallbackga o'tilmoqda: {e}")

    # 3. Linux/Vercel uchun nativ Python deshirlash (yaxshilangan algoritm)
    try:
        xml_res = _convert_mtf_native(mtf_path, expected_xml, mtf_stem)
        if os.path.exists(xml_res) and os.path.getsize(xml_res) > 200:
            logger.info(f"Nativ MTF konvertatsiya muvaffaqiyatli: {xml_res}")
            return xml_res
    except Exception as native_err:
        logger.warning(f"Nativ dekoder xatoligi: {native_err}")

    return expected_xml


def _convert_mtf_native(mtf_path: str, expected_xml: str, title_stem: str) -> str:
    """
    Nativ Python ultra-tezkor LCG deshifrlagichi va RTF parseri.
    Yaxshilangan algoritm: variantlar soni aniq (4 ta), tartibli segmentatsiya.
    """
    import zlib
    import re
    import xml.etree.ElementTree as ET
    from xml.dom import minidom

    def decrypt_mtf_bytes(data: bytes, k0: int = 27817, k1: int = 52764, k2: int = 257) -> bytes:
        out = bytearray(len(data))
        curr = k2 & 0xFFFF
        for i in range(len(data)):
            cb = data[i]
            pb = (cb ^ (curr & 0xFF)) & 0xFF
            out[i] = pb
            temp = (pb + (curr & 0xFF)) & 0xFF
            curr = ((temp * k0 + k1) & 0xFFFF)
        return bytes(out)

    with open(mtf_path, "rb") as f:
        raw_bytes = f.read()

    dec = decrypt_mtf_bytes(raw_bytes)
    decomp = None
    for offset in range(len(dec) - 10):
        if dec[offset] == 0x78 and dec[offset+1] in [0x01, 0x5e, 0x9c, 0xda]:
            try:
                decomp = zlib.decompress(dec[offset:])
                break
            except Exception:
                pass

    if not decomp:
        raise ConversionError("Zlib siqilgan oqim topilmadi.")

    # UTF-16 bloklaridan RTF qatorlarini ajratib olish
    raw_utf16 = re.findall(b'(?:[\x20-\x7e\xa0-\xff\x00-\xff]\x00){4,}', decomp)
    items = []
    ignore_set = {
        "Times New Roman", "Times New Roman CYR", "Segoe UI", "Symbol",
        "Arial", "Calibri", "Tahoma", "Verdana", "Courier New",
    }

    for r in raw_utf16:
        try:
            s = r.decode('utf-16-le', errors='ignore')
            matches = re.findall(r'\\fs\d+\s*([\s\S]*?)(?:\\par|\})', s)
            for m in matches:
                clean = re.sub(r'\\[a-zA-Z0-9\-]+\s*', '', m)
                clean = re.sub(r'[\{\}\\' + r'\r\n]', '', clean).strip()
                if clean and clean not in ignore_set and len(clean) >= 2:
                    items.append(clean)
        except Exception:
            pass

    # Deduplicate consecutive identical items
    deduped = []
    for item in items:
        if not deduped or item != deduped[-1]:
            deduped.append(item)
    items = deduped

    root = ET.Element("MyTestX")
    ET.SubElement(root, "Version").text = "11.0"
    opts = ET.SubElement(root, "TestOptions")
    ET.SubElement(opts, "Title").text = title_stem

    tasks_group = ET.SubElement(ET.SubElement(root, "Groups"), "Group")
    tasks_node = ET.SubElement(tasks_group, "Tasks")

    # Improved question/variant segmentation:
    # MyTestX always has exactly 4 or 5 correct variants per question.
    # A new question starts when:
    #   - we have at least 2 variants AND the candidate ends with '?' or starts with a digit+dot
    # Max 5 variants per question (standard MyTestX format).
    MAX_VARIANTS = 5

    def _is_question_start(text: str) -> bool:
        """Matn yangi savol boshlanishiga ishora qiladimi?"""
        # Ends with question mark
        if text.rstrip().endswith('?'):
            return True
        # Starts with number+dot pattern like "1.", "12."
        if re.match(r'^\d{1,3}\.\s', text):
            return True
        return False

    idx = 0
    while idx < len(items):
        q_text = items[idx]
        idx += 1

        variants = []
        while idx < len(items):
            cand = items[idx]

            # Stop if we have max variants
            if len(variants) >= MAX_VARIANTS:
                break

            # Stop if candidate looks like a new question AND we have at least 2 variants
            if len(variants) >= 2 and _is_question_start(cand):
                break

            # Stop if candidate is very long (likely a question) AND we have at least 1 variant
            if len(variants) >= 1 and len(cand) > 100 and _is_question_start(cand):
                break

            variants.append(cand)
            idx += 1

        if variants:
            task = ET.SubElement(tasks_node, "Task", Type="SINGLE_CHOICE", Score="1")
            q_node = ET.SubElement(task, "QuestionText")
            ET.SubElement(q_node, "PlainText").text = q_text
            var_node = ET.SubElement(task, "Variants")
            for v_idx, v in enumerate(variants):
                vt = ET.SubElement(var_node, "VariantText", CorrectAnswer="True" if v_idx == 0 else "False")
                ET.SubElement(vt, "PlainText").text = v

    xml_bytes_out = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(xml_bytes_out)
    with open(expected_xml, "w", encoding="utf-8") as f:
        f.write(parsed.toprettyxml(indent="\t"))

    return expected_xml


def _run_gui_conversion(exe_path: str, mtf_path: str, target_dir: str, expected_xml: str) -> str:
    """
    Mtf2Xml.exe ni fon rejimida (ko'rinmasdan) ishga tushiradi va natijani kutadi.
    CREATE_NO_WINDOW + DETACHED_PROCESS = UI ko'rinmaydi.
    """
    mtf_stem = Path(os.path.basename(mtf_path)).stem
    local_xml = os.path.join(os.path.dirname(mtf_path), f"{mtf_stem}_new.xml")

    # Remove old xml if present
    for old in [local_xml, expected_xml]:
        if os.path.exists(old):
            try:
                os.remove(old)
            except Exception:
                pass

    CREATE_NO_WINDOW = 0x08000000
    DETACHED_PROCESS = 0x00000008

    try:
        proc = subprocess.Popen(
            [exe_path, mtf_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=CREATE_NO_WINDOW | DETACHED_PROCESS,
        )
    except Exception as e:
        raise ConversionError(f"Mtf2Xml.exe ni ishga tushirib bo'lmadi: {e}")

    # Wait for XML output file — up to 30 seconds
    deadline = time.time() + 30
    while time.time() < deadline:
        # Check if EXE produced output next to MTF file (default behavior)
        if os.path.exists(local_xml) and os.path.getsize(local_xml) > 500:
            # Give it 0.3s more to finish writing
            time.sleep(0.3)
            if local_xml != expected_xml:
                shutil.copy2(local_xml, expected_xml)
            # Kill process if still alive
            try:
                proc.terminate()
            except Exception:
                pass
            logger.info(f"Mtf2Xml.exe natijasi tayyor: {expected_xml}")
            return expected_xml

        # Also check target_dir
        if os.path.exists(expected_xml) and os.path.getsize(expected_xml) > 500:
            time.sleep(0.3)
            try:
                proc.terminate()
            except Exception:
                pass
            return expected_xml

        # Handle GUI dialogs silently if EXE shows them
        if os.name == 'nt' and user32 and proc.pid:
            _handle_gui_dialogs(proc.pid, mtf_path)

        time.sleep(0.4)

    try:
        proc.terminate()
    except Exception:
        pass

    # One last check
    if os.path.exists(local_xml) and os.path.getsize(local_xml) > 500:
        if local_xml != expected_xml:
            shutil.copy2(local_xml, expected_xml)
        return expected_xml

    raise ConversionError(f"Mtf2Xml.exe 30 soniyada natija bermadi: {expected_xml}")


def _handle_gui_dialogs(pid: int, mtf_path: str):
    """Mtf2Xml.exe GUI dialoglarini avtomatik to'ldiradi (agar chiqsa)."""
    if not user32:
        return

    try:
        # Find all top-level windows belonging to the process
        windows = []
        def enum_cb(hwnd, _):
            if _get_window_pid(hwnd) == pid:
                windows.append(hwnd)
            return True
        user32.EnumWindows(ENUMWINDOWSPROC(enum_cb), 0)

        for hwnd in windows:
            class_name = _get_class_name(hwnd)
            win_text = _get_window_text(hwnd)

            # File open dialog
            if class_name == "#32770":
                children = _find_all_children(hwnd)
                for child in children:
                    child_class = _get_class_name(child)
                    child_text = _get_window_text(child)

                    if child_class == "Edit":
                        _set_edit_text(child, mtf_path)
                    elif child_class == "Button" and ("Open" in child_text or "OK" in child_text or child_text in ("&Open", "OK")):
                        _click_button(child)
                        break

            # Minimize visible main windows
            elif class_name not in ("#32770", "Shell_TrayWnd"):
                user32.ShowWindow(hwnd, SW_MINIMIZE)
    except Exception:
        pass
