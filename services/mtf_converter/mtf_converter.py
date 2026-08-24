"""
mtf_converter.py — MTF test fayllarini XML ga o'girish moduli.

- Windows tizimlarida 001Mtf2Xml.exe utilitasini fonda (foydalanuvchiga ko'rinmasdan)
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
    """
    mtf_path = os.path.abspath(mtf_path)
    if not os.path.exists(mtf_path):
        raise FileNotFoundError(f".mtf fayl topilmadi: {mtf_path}")

    mtf_filename = os.path.basename(mtf_path)
    mtf_stem = Path(mtf_filename).stem

    target_dir = work_dir if work_dir else os.path.dirname(mtf_path)
    os.makedirs(target_dir, exist_ok=True)

    expected_xml = os.path.join(target_dir, f"{mtf_stem}_new.xml")

    # Mavjud tayyor XML ni tekshirish
    local_xml = os.path.join(os.path.dirname(mtf_path), f"{mtf_stem}_new.xml")
    if os.path.exists(local_xml) and os.path.getsize(local_xml) > 500:
        if local_xml != expected_xml:
            shutil.copy2(local_xml, expected_xml)
        logger.info(f"Mavjud XML fayldan foydalanilmoqda: {expected_xml}")
        return expected_xml

    actual_exe = exe_path if (exe_path and os.path.exists(exe_path)) else _find_exe()

    # EXE va Windows mavjud bo'lsa rasmiy Mtf2Xml orqali fonda ishlatamiz
    if actual_exe and os.path.exists(actual_exe) and os.name == 'nt':
        try:
            logger.info(f"Mtf2Xml.exe fonda ishga tushirilmoqda: {mtf_path}")
            return _run_gui_conversion(actual_exe, mtf_path, target_dir, expected_xml)
        except Exception as e:
            logger.warning(f"GUI konvertatsiyada xatolik: {e}. Nativ fallback ishga tushadi...")

    # Nativ Python fallback
    logger.info(f"Nativ Python MTF konvertor ishga tushmoqda: {mtf_path}")
    return _convert_mtf_native(mtf_path, expected_xml, mtf_stem)


def _run_gui_conversion(exe_path: str, mtf_path: str, target_dir: str, expected_xml: str, timeout: int = 45) -> str:
    """
    Fonda 001Mtf2Xml.exe utilitasi yordamida 100% to'g'ri va rasmli XML hosil qiladi.
    """
    import tempfile
    temp_dir = tempfile.mkdtemp(prefix="mtf_conv_")

    try:
        mtf_stem = Path(os.path.basename(mtf_path)).stem
        # Probeldan holi vaqtinchalik nom
        safe_mtf_name = "test_mtf.mtf"
        tmp_mtf = os.path.join(temp_dir, safe_mtf_name)
        tmp_exe = os.path.join(temp_dir, "001Mtf2Xml.exe")
        
        shutil.copy2(mtf_path, tmp_mtf)
        shutil.copy2(exe_path, tmp_exe)

        proc = subprocess.Popen([tmp_exe], cwd=temp_dir)
        time.sleep(2)

        form_hwnd = None
        for attempt in range(15):
            forms = _find_windows_by_pid_class(proc.pid, "TForm1")
            if forms:
                form_hwnd = forms[0]
                break
            time.sleep(0.5)

        if not form_hwnd:
            raise ConversionError("TForm1 oyna topilmadi")

        user32.ShowWindow(form_hwnd, SW_MINIMIZE)

        buttons_with_rect = []
        for ch in _find_all_children(form_hwnd):
            if _get_class_name(ch) == "TBitBtn":
                rect = ctypes.wintypes.RECT()
                user32.GetWindowRect(ch, ctypes.byref(rect))
                buttons_with_rect.append((rect.left, ch))

        buttons_with_rect.sort()
        if len(buttons_with_rect) < 2:
            raise ConversionError("BitBtn tugmalar topilmadi")

        open_btn = buttons_with_rect[0][1]
        convert_btn = buttons_with_rect[-1][1]

        _click_button(open_btn)
        time.sleep(1.5)

        dialog_found = False
        for attempt in range(10):
            dialogs = _find_windows_by_pid_class(proc.pid, "#32770")
            if dialogs:
                dlg_hwnd = dialogs[0]
                combo_ex = _find_child_by_class(dlg_hwnd, "ComboBoxEx32")
                if combo_ex:
                    combo_edit = _find_child_by_class(combo_ex[0], "Edit")
                    if combo_edit:
                        _set_edit_text(combo_edit[0], tmp_mtf)
                        time.sleep(0.5)

                for btn in _find_child_by_class(dlg_hwnd, "Button"):
                    txt = _get_window_text(btn)
                    if any(k in txt.lower() for k in ["ткрыть", "open"]) or txt in ("&О", "&O"):
                        _click_button(btn)
                        dialog_found = True
                        break
                if dialog_found:
                    break
            time.sleep(0.5)

        if not dialog_found:
            raise ConversionError("Fayl ochish muloqot oynasi topilmadi")

        time.sleep(1.5)
        _click_button(convert_btn)

        tmp_generated_xml = os.path.join(temp_dir, "test_mtf_new.xml")
        
        last_sz = -1
        stable_cnt = 0

        for i in range(timeout):
            time.sleep(1)
            if os.path.exists(tmp_generated_xml):
                sz = os.path.getsize(tmp_generated_xml)
                if sz == last_sz and sz > 1000:
                    stable_cnt += 1
                    if stable_cnt >= 3:
                        break
                else:
                    stable_cnt = 0
                    last_sz = sz

        if not os.path.exists(tmp_generated_xml) or os.path.getsize(tmp_generated_xml) < 500:
            raise ConversionError("XML konvertatsiya yakunlanmadi yoki natija bo'sh.")

        shutil.copy2(tmp_generated_xml, expected_xml)
        logger.info(f"XML fonda muvaffaqiyatli yaratildi: {expected_xml} ({os.path.getsize(expected_xml)} bytes)")
        return expected_xml

    finally:
        if 'proc' in locals() and proc:
            try:
                proc.terminate()
            except Exception:
                pass
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass


def _convert_mtf_native(mtf_path: str, expected_xml: str, title_stem: str) -> str:
    """Nativ Python fallback deshifrlagichi."""
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
    decomp = zlib.decompress(dec[34:])
    text_utf16 = decomp.decode("utf-16-le", errors="ignore")

    blocks = re.findall(r'\\fs\d+\s*([^\r\n\{\}\\]+)', text_utf16)
    
    clean_items = []
    ignore_set = {"Times New Roman", "Times New Roman CYR", "Segoe UI", "Symbol", "Arial", "Calibri"}
    
    for b in blocks:
        t = b.replace("rquote", "'").replace("lquote", "'").replace("ldblquote", '"').replace("rdblquote", '"')
        t = re.sub(r'\\\'[0-9a-fA-F]{2}', '', t)
        t = re.sub(r'\\[a-zA-Z0-9]+\s*', '', t)
        s = re.sub(r'[\{\}\\\r\n]', '', t).strip()
        if s and s not in ignore_set and len(s) >= 2:
            clean_items.append(s)

    root = ET.Element("MyTestX")
    version = ET.SubElement(root, "Version")
    version.text = "11.0"

    opts = ET.SubElement(root, "TestOptions")
    t_title = ET.SubElement(opts, "Title")
    t_title.text = title_stem

    groups = ET.SubElement(root, "Groups")
    group = ET.SubElement(groups, "Group")
    tasks = ET.SubElement(group, "Tasks")

    current_variants = None

    for item in clean_items:
        is_question = (
            item.endswith("?") or item.startswith("?") or
            "belgilang" in item.lower() or "ayting" in item.lower() or
            "ko'rsating" in item.lower() or len(item) > 50
        )

        if is_question or current_variants is None or len(current_variants) >= 6:
            task_node = ET.SubElement(tasks, "Task", Type="SINGLE_CHOICE", Score="1")
            q_text_node = ET.SubElement(task_node, "QuestionText")
            plain_text = ET.SubElement(q_text_node, "PlainText")
            plain_text.text = item
            current_variants = ET.SubElement(task_node, "Variants")
        else:
            v_node = ET.SubElement(current_variants, "VariantText", CorrectAnswer="True" if len(current_variants) == 0 else "False")
            v_plain = ET.SubElement(v_node, "PlainText")
            v_plain.text = item

    xml_bytes = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(xml_bytes)
    with open(expected_xml, "w", encoding="utf-8") as f:
        f.write(parsed.toprettyxml(indent="\t"))

    return expected_xml
