"""
mtf_converter.py — MTF test fayllarini XML ga o'girish moduli.

- Windows tizimlarida Mtf2Xml.exe utilitasini fonda (foydalanuvchiga ko'rinmasdan)
  avtomatlashtirib, rasmlar va o'zbekcha matnlarni 100% mukammal XML formatiga o'giradi.
- Asosiy o'quvchi endi mtf_native.py (exe'siz, har qanday OS'da). Bu modul faqat
  native o'quvchi fayl versiyasini tanimagan holatlar uchun Windows'dagi zaxira.
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

    Faqat zaxira yo'l: Windows + Mtf2Xml.exe. Asosiy o'quvchi — mtf_native.parse_mtf_bytes.
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

    # Eski taxminiy dekoder olib tashlandi: u har doim birinchi variantni "to'g'ri" deb
    # belgilardi. Endi asosiy o'quvchi — mtf_native.py; bu funksiya faqat zaxira (Windows).
    raise ConversionError("Mtf2Xml.exe mavjud emas yoki natija bermadi.")


def _run_gui_conversion(exe_path: str, mtf_path: str, target_dir: str, expected_xml: str) -> str:
    """
    Mtf2Xml.exe ni fon rejimida (ko'rinmasdan) ishga tushiradi va natijani kutadi.
    CREATE_NO_WINDOW = GUI ko'rinmaydi. Timeout: 60 soniya.
    """
    mtf_stem = Path(os.path.basename(mtf_path)).stem
    # EXE always writes output next to the input MTF file
    local_xml = os.path.join(os.path.dirname(mtf_path), f"{mtf_stem}_new.xml")

    # Remove stale XML files before starting
    for old in [local_xml, expected_xml]:
        if os.path.exists(old):
            try:
                os.remove(old)
            except Exception:
                pass

    # CREATE_NO_WINDOW only — DETACHED_PROCESS can break file I/O on some systems
    CREATE_NO_WINDOW = 0x08000000

    try:
        proc = subprocess.Popen(
            [exe_path, mtf_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=CREATE_NO_WINDOW,
        )
    except Exception as e:
        raise ConversionError(f"Mtf2Xml.exe ni ishga tushirib bo'lmadi: {e}")

    def _xml_is_ready(path: str) -> bool:
        """XML fayl yozish tugaganiga ishonch hosil qilish: hajm barqaror bo'lsin."""
        if not os.path.exists(path):
            return False
        try:
            sz1 = os.path.getsize(path)
            if sz1 < 500:
                return False
            time.sleep(0.5)
            sz2 = os.path.getsize(path)
            return sz1 == sz2  # Fayl yozish to'xtagan
        except Exception:
            return False

    # Wait up to 60 seconds for XML output
    deadline = time.time() + 60
    while time.time() < deadline:
        # EXE writes XML next to the MTF (local_xml path)
        if _xml_is_ready(local_xml):
            if local_xml != expected_xml:
                shutil.copy2(local_xml, expected_xml)
            try:
                proc.terminate()
            except Exception:
                pass
            logger.info(f"Mtf2Xml.exe natijasi tayyor: {expected_xml}")
            return expected_xml

        # Also check target_dir in case EXE wrote there
        if _xml_is_ready(expected_xml):
            try:
                proc.terminate()
            except Exception:
                pass
            return expected_xml

        # Handle GUI dialogs silently if EXE shows them
        if os.name == 'nt' and user32 and proc.pid:
            _handle_gui_dialogs(proc.pid, mtf_path)

        time.sleep(0.5)

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
    """
    Mtf2Xml.exe GUI oynasini avtomatik boshqaradi.

    EXE TForm1 oynasini ko'rsatadi va 4 ta tugma bilan konvertatsiya turini so'raydi:
    - 'Папка и вложенные папки' (Papka va ichki)
    - 'Папка' (Papka)
    - 'Несколько файлов' (Bir nechta fayl)
    - 'Один файл' (Bitta fayl) ← BIZ SHUNI BOSAMIZ

    Shuningdek, eski MyTestX.exe uchun fayl tanlash (#32770) dialogini ham boshqaradi.
    """
    if not user32:
        return

    try:
        windows = []
        def enum_cb(hwnd, _):
            if _get_window_pid(hwnd) == pid:
                windows.append(hwnd)
            return True
        user32.EnumWindows(ENUMWINDOWSPROC(enum_cb), 0)

        for hwnd in windows:
            cls = _get_class_name(hwnd)
            txt = _get_window_text(hwnd)

            # Mtf2Xml.exe TForm1 — main conversion window
            # Has buttons: 'Папка и вложенные папки', 'Папка', 'Несколько файлов', 'Один файл'
            if cls == "TForm1":
                children = _find_all_children(hwnd)
                for child in children:
                    child_cls = _get_class_name(child)
                    child_txt = _get_window_text(child)
                    # Click 'Один файл' — single file conversion mode
                    if child_cls == "TBitBtn" and (
                        "\u041e\u0434\u0438\u043d" in child_txt or  # "Один"
                        "файл" in child_txt.lower() or
                        "file" in child_txt.lower()
                    ):
                        # Prefer 'Один файл' over other file-related buttons
                        if "папк" not in child_txt.lower() and "\u043d\u0435\u0441\u043a" not in child_txt.lower():
                            logger.info(f"TForm1 tugmasi bosilmoqda: {child_txt!r}")
                            _click_button(child)
                            return

                # Fallback: click last TBitBtn (usually 'Один файл')
                tbitbtns = [c for c in children if _get_class_name(c) == "TBitBtn"]
                if tbitbtns:
                    last_btn = tbitbtns[-1]
                    logger.info(f"TForm1 oxirgi tugma bosilmoqda: {_get_window_text(last_btn)!r}")
                    _click_button(last_btn)
                return

            # File open / save dialog (#32770 = DialogBox)
            elif cls == "#32770":
                children = _find_all_children(hwnd)
                for child in children:
                    child_cls = _get_class_name(child)
                    child_txt = _get_window_text(child)
                    if child_cls == "Edit" and not child_txt:
                        _set_edit_text(child, mtf_path)
                    elif child_cls == "Button" and any(
                        k in child_txt for k in ("Open", "OK", "&Open", "&OK", "\u041e\u041a", "\u041e\u0442\u043a\u0440")
                    ):
                        _click_button(child)
                        break

            # Minimize any other visible windows from this process
            elif cls not in ("TApplication", "TPUtilWindow", "Shell_TrayWnd",
                             "CiceroUIWndFrame", "MSCTFIME UI", "IME",
                             "Touch Tooltip Window", "UAC_InputIndicatorOverlayWnd",
                             "UAC Input Indicator", "CicLoaderWndClass"):
                if user32.IsWindowVisible(hwnd):
                    user32.ShowWindow(hwnd, SW_MINIMIZE)
    except Exception as e:
        logger.debug(f"_handle_gui_dialogs error: {e}")

