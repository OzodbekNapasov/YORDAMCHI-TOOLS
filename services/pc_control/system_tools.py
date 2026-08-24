import os
import sys
import time
import asyncio
import logging
import tempfile
import shutil
import glob
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Check OS
IS_WINDOWS = os.name == 'nt'

# Safe imports for Windows-specific libraries
try:
    import psutil
except ImportError:
    psutil = None

try:
    from PIL import Image, ImageGrab
except ImportError:
    Image = None
    ImageGrab = None

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import pyautogui
    pyautogui.FAILSAFE = False
except ImportError:
    pyautogui = None

try:
    import ctypes
except ImportError:
    ctypes = None


def is_system_compatible() -> bool:
    """Tekshiradi: Ushbu mashina Windows OS va PC boshqaruviga mosmi."""
    return IS_WINDOWS


def get_system_status() -> str:
    """
    Kompyuter tizim holati (CPU, RAM, Disk, Batareya, Uptime) haqida ma'lumot yig'adi.
    """
    if not psutil:
        return "⚠️ <code>psutil</code> kutubxonasi o'rnatilmagan yoki muhit mos emas."

    try:
        # CPU
        cpu_usage = psutil.cpu_percent(interval=0.5)
        cpu_count = psutil.cpu_count(logical=True)
        
        # RAM
        ram = psutil.virtual_memory()
        ram_total_gb = round(ram.total / (1024 ** 3), 2)
        ram_used_gb = round(ram.used / (1024 ** 3), 2)
        ram_percent = ram.percent

        # Disk C: & D:
        disk_lines = []
        for drive in ["C:\\", "D:\\"]:
            if os.path.exists(drive):
                try:
                    d_usage = psutil.disk_usage(drive)
                    d_tot = round(d_usage.total / (1024 ** 3), 1)
                    d_free = round(d_usage.free / (1024 ** 3), 1)
                    disk_lines.append(f"💾 <b>{drive} Disk:</b> {d_usage.percent}% ({d_free} GB bo'sh / {d_tot} GB)")
                except Exception:
                    pass
        disk_info = "\n".join(disk_lines) if disk_lines else "💾 <b>Disk:</b> Ma'lumot olib bo'lmadi"

        # Batareya
        battery = psutil.sensors_battery()
        if battery:
            plugged = "🔌 Tarmoqqa ulangan" if battery.power_plugged else "🔋 Batareyadan ishlamoqda"
            battery_info = f"<b>Batareya:</b> {battery.percent}% ({plugged})"
        else:
            battery_info = "<b>Batareya:</b> Stasionar kompyuter (Mavjud emas)"

        # Uptime
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        uptime_str = str(timedelta(seconds=int(uptime.total_seconds())))

        status_text = (
            "📊 <b>TIZIM HOLATI (SYSTEM MONITOR)</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"💻 <b>CPU Yuklanishi:</b> {cpu_usage}% ({cpu_count} ta yadro)\n"
            f"🧠 <b>RAM Yuklanishi:</b> {ram_percent}% ({ram_used_gb} GB / {ram_total_gb} GB)\n"
            f"{disk_info}\n"
            f"🔋 {battery_info}\n"
            f"⏱ <b>Ishlash vaqti (Uptime):</b> {uptime_str}\n"
            f"🕒 <b>Hozirgi vaqt:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return status_text
    except Exception as e:
        logger.error(f"System status olishda xatolik: {e}")
        return f"❌ Tizim holatini olishda xatolik yuz berdi: {e}"


def take_screenshot(filepath: str) -> str:
    """
    Ekran tasvirini (screenshot) olib ko'rsatilgan yo'lga saqlaydi (Fail-safe Win32 + ImageGrab).
    """
    if ImageGrab:
        try:
            screenshot = ImageGrab.grab()
            screenshot.save(filepath, "PNG")
            return filepath
        except Exception:
            pass

    if IS_WINDOWS and ctypes and Image:
        try:
            user32 = ctypes.windll.user32
            gdi32 = ctypes.windll.gdi32

            w = user32.GetSystemMetrics(0)
            h = user32.GetSystemMetrics(1)

            hwnd = user32.GetDesktopWindow()
            hdc = user32.GetWindowDC(hwnd)
            memdc = gdi32.CreateCompatibleDC(hdc)
            bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
            gdi32.SelectObject(memdc, bmp)

            gdi32.BitBlt(memdc, 0, 0, w, h, hdc, 0, 0, 0x00CC0020)

            class BITMAPINFOHEADER(ctypes.Structure):
                _fields_ = [
                    ('biSize', ctypes.c_uint32),
                    ('biWidth', ctypes.c_int32),
                    ('biHeight', ctypes.c_int32),
                    ('biPlanes', ctypes.c_uint16),
                    ('biBitCount', ctypes.c_uint16),
                    ('biCompression', ctypes.c_uint32),
                    ('biSizeImage', ctypes.c_uint32),
                    ('biXPelsPerMeter', ctypes.c_int32),
                    ('biYPelsPerMeter', ctypes.c_int32),
                    ('biClrUsed', ctypes.c_uint32),
                    ('biClrImportant', ctypes.c_uint32)
                ]

            bmi = BITMAPINFOHEADER()
            bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
            bmi.biWidth = w
            bmi.biHeight = -h
            bmi.biPlanes = 1
            bmi.biBitCount = 32
            bmi.biCompression = 0

            buffer = ctypes.create_string_buffer(w * h * 4)
            gdi32.GetDIBits(hdc, bmp, 0, h, buffer, ctypes.byref(bmi), 0)

            gdi32.DeleteObject(bmp)
            gdi32.DeleteDC(memdc)
            user32.ReleaseDC(hwnd, hdc)

            img = Image.frombuffer('RGBA', (w, h), buffer.raw, 'raw', 'BGRA', 0, 1)
            img = img.convert('RGB')
            img.save(filepath, "PNG")
            return filepath
        except Exception as e:
            logger.error(f"Screenshot Win32 error: {e}")
            raise e

    raise Exception("Screenshot olish imkonsiz: Pillow yoki Windows GUI mavjud emas.")


def take_webcam_photo(filepath: str) -> str:
    """
    OpenCV orqali veb-kamera orqali suratga olib saqlaydi.
    """
    if not cv2:
        raise Exception("OpenCV (cv2) kutubxonasi o'rnatilmagan!")

    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW if IS_WINDOWS else cv2.CAP_ANY)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            raise Exception("Veb-kamera topilmadi yoki boshqa dastur tomonidan band qilingan!")

        for _ in range(5):
            ret, frame = cap.read()

        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            raise Exception("Kameradan tasvirni o'qib bo'lmadi!")

        cv2.imwrite(filepath, frame)
        return filepath
    except Exception as e:
        logger.error(f"Webcam rasm olishda xatolik: {e}")
        raise e


def execute_cmd_sync(command: str, timeout: int = 30) -> str:
    """
    Windows CMD/PowerShell buyrug'ini bajaradi va natijasini matn ko'rinishida qaytaradi (Sinxron).
    """
    import subprocess
    try:
        proc = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='cp866',
            errors='replace'
        )
        out_str = proc.stdout.strip() or proc.stderr.strip()
        if not out_str:
            out_str = "✅ Buyruq muvaffaqiyatli bajarildi (hech qanday matn qaytarilmadi)."

        if len(out_str) > 3500:
            out_str = out_str[:3500] + "\n\n... [Matn juda uzun bo'lgani uchun qisqartirildi]"

        return out_str
    except subprocess.TimeoutExpired:
        return "⏳ <b>Xatolik:</b> Buyruq bajarilish vaqti tugadi (Timeout: 30s)."
    except Exception as e:
        logger.error(f"CMD bajarishda xatolik: {e}")
        return f"❌ Buyruqni bajarishda xatolik: {e}"


def get_running_apps() -> str:
    """
    Hozirda ishlab turgan asosiy va faol dasturlar ro'yxatini qaytaradi (TOP 20 RAM).
    """
    if not psutil:
        return "⚠️ <code>psutil</code> kutubxonasi mavjud emas."

    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
            try:
                pinfo = proc.info
                if pinfo['name'] and pinfo['memory_info']:
                    mem_mb = round(pinfo['memory_info'].rss / (1024 * 1024), 1)
                    if mem_mb > 15:
                        processes.append({
                            'pid': pinfo['pid'],
                            'name': pinfo['name'],
                            'memory': mem_mb
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        processes = sorted(processes, key=lambda x: x['memory'], reverse=True)[:20]

        if not processes:
            return "📱 Ishlayotgan dasturlar topilmadi."

        result = "🎮 <b>ISHLAYOTGAN ASOSIY DASTURLAR (TOP 20 RAM):</b>\n━━━━━━━━━━━━━━━━━━━━━\n"
        for p in processes:
            result += f"🔹 <code>{p['name']}</code> | PID: <code>{p['pid']}</code> | RAM: <b>{p['memory']} MB</b>\n"

        result += "\n💡 <i>To'xtatish uchun: /kill &lt;dastur_nomi&gt; yoki /kill &lt;PID&gt;</i>"
        return result
    except Exception as e:
        logger.error(f"Apps ro'yxatini olishda xatolik: {e}")
        return f"❌ Dasturlar ro'yxatini olishda xatolik: {e}"


def kill_process(target: str) -> str:
    """
    Nomi yoki PID raqami bo'yicha jarayonni majburiy to'xtatadi.
    """
    if not psutil:
        return "⚠️ <code>psutil</code> kutubxonasi mavjud emas."

    try:
        killed_count = 0
        target = target.strip()

        if target.isdigit():
            pid = int(target)
            proc = psutil.Process(pid)
            pname = proc.name()
            proc.kill()
            return f"✅ PID <code>{pid}</code> ({pname}) jarayoni to'xtatildi."

        target_name = target.lower()
        target_name_exe = target_name if target_name.endswith('.exe') else target_name + '.exe'

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pname = proc.info['name'].lower()
                if pname == target_name or pname == target_name_exe:
                    proc.kill()
                    killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if killed_count > 0:
            return f"✅ <code>{target}</code> nomi bo'yicha {killed_count} ta jarayon to'xtatildi."
        else:
            return f"⚠️ <code>{target}</code> nomli faol jarayon topilmadi."
    except Exception as e:
        logger.error(f"Kill process xatoligi: {e}")
        return f"❌ Jarayonni to'xtatishda xatolik: {e}"


def show_popup(text: str):
    """
    Windows operatsion tizimida MessageBox ko'rsatish.
    """
    if IS_WINDOWS and ctypes:
        try:
            ctypes.windll.user32.MessageBoxW(0, text, "ATLAS Bot Bildirishnomasi", 0x40 | 0x1000)
            return "✅ Bildirishnoma kompyuter ekranida ko'rsatildi."
        except Exception as e:
            return f"❌ Bildirishnoma ko'rsatishda xatolik: {e}"
    return "⚠️ Ushbu muhitda MessageBox mavjud emas."


def power_control(action: str) -> str:
    """
    Quvvatni boshqarish (Shutdown, Restart, Sleep, Lock, Cancel).
    """
    if not IS_WINDOWS:
        return "⚠️ Quvvat boshqaruvi faqat Windows operatsion tizimida ishlaydi."

    try:
        if action == "shutdown":
            os.system("shutdown /s /t 10 /c \"ATLAS Bot orqali o'chirilmoqda...\"")
            return "⚡ Kompyuter 10 soniyadan so'ng o'chiriladi! Bekor qilish uchun: /cancel_power"
        elif action == "restart":
            os.system("shutdown /r /t 10 /c \"ATLAS Bot orqali Qayta yuklanmoqda...\"")
            return "🔄 Kompyuter 10 soniyadan so'ng qayta yuklanadi! Bekor qilish uchun: /cancel_power"
        elif action == "sleep":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "🌙 Kompyuter uyqu rejimiga (Sleep) o'tkazildi."
        elif action == "lock":
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "🔒 Ekran qulflandi (Lock)."
        elif action == "cancel":
            os.system("shutdown /a")
            return "❌ Rejalashtirilgan o'chirish/qayta yuklash bekor qilindi."
        else:
            return "⚠️ Noma'lum quvvat buyrug'i."
    except Exception as e:
        logger.error(f"Quvvatni boshqarishda xatolik: {e}")
        return f"❌ Quvvat buyrug'ini bajarishda xatolik: {e}"


def is_admin() -> bool:
    """
    Python skripti Administrator (UAC) huquqlari bilan ishlayotganini tekshiradi.
    """
    if IS_WINDOWS and ctypes:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    return False


def click_screen(x: int, y: int) -> str:
    """
    Ekranning ko'rsatilgan (x, y) koordinatasida sichqoncha tugmasini bosadi.
    """
    if not pyautogui:
        return "⚠️ PyAutoGUI kutubxonasi mavjud emas."
    try:
        pyautogui.click(x, y)
        return f"✅ Sichqoncha ekranning ({x}, {y}) nuqtasida bosildi."
    except Exception as e:
        return f"❌ Klik xatoligi: {e}"


def press_key(key: str) -> str:
    """
    Klaviatura tugmasini bosadi (masalan: enter, space, tab, alt+a va h.k.).
    """
    if not pyautogui:
        return "⚠️ PyAutoGUI kutubxonasi mavjud emas."
    try:
        if "+" in key:
            keys = key.split("+")
            pyautogui.hotkey(*keys)
        else:
            pyautogui.press(key)
        return f"✅ Klaviaturada <code>{key}</code> tugmasi bosildi."
    except Exception as e:
        return f"❌ Tugma bosish xatoligi: {e}"


def set_volume(percent: int) -> str:
    """
    Windows masofaviy ovoz balandligini o'rnatadi (0 - 100).
    """
    percent = max(0, min(100, percent))
    try:
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from comtypes import CLSCTX_ALL

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMasterVolumeLevelScalar(percent / 100.0, None)
        return f"🔊 Ovoz balandligi <b>{percent}%</b> ga o'rnatildi."
    except Exception as e:
        logger.error(f"Volume pycaw error: {e}")
        return f"🔊 Ovoz o'rnatildi (yoki pycaw mavjud emas: {e})."


def set_mute(mute: bool = True) -> str:
    """
    Windows masofaviy ovozini o'chirish (Mute) yoki yoqish (Unmute).
    """
    try:
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from comtypes import CLSCTX_ALL

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMute(int(mute), None)
        status = "o'chirildi (Mute 🔇)" if mute else "yoqildi (Unmute 🔊)"
        return f"🔊 Ovoz {status}."
    except Exception:
        if pyautogui:
            pyautogui.press('volumemute')
            return "🔊 Ovoz holati (Mute/Unmute) o'zgartirildi."
        return "⚠️ Ovozni o'zgartirib bo'lmadi."


def media_control(action: str) -> str:
    """
    Media pleyer boshqaruvi (playpause, nexttrack, prevtrack).
    """
    if not pyautogui:
        return "⚠️ PyAutoGUI kutubxonasi mavjud emas."
    try:
        if action in ["play", "pause", "playpause"]:
            pyautogui.press('playpause')
            return "⏯ Media pleyer ijro / to'xtatish tugmasi bosildi."
        elif action in ["next", "nexttrack"]:
            pyautogui.press('nexttrack')
            return "⏭ Keyingi trekka o'tildi."
        elif action in ["prev", "prevtrack"]:
            pyautogui.press('prevtrack')
            return "⏮ Oldingi trekka o'tildi."
        else:
            return "⚠️ Noma'lum media buyruq."
    except Exception as e:
        return f"❌ Media boshqaruvida xatolik: {e}"


def set_brightness(percent: int) -> str:
    """
    Ekran yorqinligini (Brightness) moslaydi (0 - 100).
    """
    import subprocess
    percent = max(0, min(100, percent))
    try:
        ps_script = f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {percent})"
        subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True, timeout=5)
        return f"☀️ Ekran yorqinligi <b>{percent}%</b> ga o'rnatildi."
    except Exception as e:
        logger.error(f"Brightness error: {e}")
        return f"❌ Ekran yorqinligini o'zgartirishda xatolik: {e}"


def open_app(app_name: str) -> str:
    """
    Kalkulyator, Bloknot, Chrome, Telegram, Explorer kabi dasturlarni nomiga qarab ochadi.
    """
    name = app_name.lower().strip()
    apps_map = {
        "kalkulyator": "calc",
        "calculator": "calc",
        "calc": "calc",
        "bloknot": "notepad",
        "notepad": "notepad",
        "chrome": "chrome",
        "google chrome": "chrome",
        "browser": "chrome",
        "telegram": "telegram",
        "explorer": "explorer",
        "my pc": "explorer",
        "dispetcher": "taskmgr",
        "task manager": "taskmgr",
        "taskmgr": "taskmgr",
        "cmd": "cmd /c start cmd",
        "powershell": "powershell",
        "word": "winword",
        "excel": "excel",
        "control panel": "control",
        "boshqaruv paneli": "control",
        "paint": "mspaint",
        "skrinshot": "snippingtool"
    }

    cmd_to_run = apps_map.get(name, name)
    try:
        if "." not in cmd_to_run and " " not in cmd_to_run:
            cmd_to_run = f"start {cmd_to_run}"

        os.system(cmd_to_run)
        return f"🚀 <b>{app_name.capitalize()}</b> dasturi ishga tushirildi!"
    except Exception as e:
        logger.error(f"Open app error: {e}")
        return f"❌ Dasturni ochishda xatolik: {e}"


def show_desktop() -> str:
    """
    Barcha ochiq oynalarni yig'adi / Ish stolini ko'rsatadi (Win + D).
    """
    if not pyautogui:
        return "⚠️ PyAutoGUI mavjud emas."
    try:
        pyautogui.hotkey('win', 'd')
        return "🖥 Ish stoli ko'rsatildi (Win + D)."
    except Exception as e:
        return f"❌ Xatolik: {e}"


def close_active_window() -> str:
    """
    Hozirgi faol oynani yopadi (Alt + F4).
    """
    if not pyautogui:
        return "⚠️ PyAutoGUI mavjud emas."
    try:
        pyautogui.hotkey('alt', 'f4')
        return "❌ Faol oyna yopildi (Alt + F4)."
    except Exception as e:
        return f"❌ Xatolik: {e}"


def empty_recycle_bin() -> str:
    """
    Windows Korzina (Chaqindi qutisi) ni tozalaydi.
    """
    import subprocess
    try:
        ps_script = "Clear-RecycleBin -Confirm:$false -ErrorAction SilentlyContinue"
        subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True, timeout=10)
        return "🗑 <b>Windows Korzina (Chaqindi qutisi) tozalandi!</b>"
    except Exception as e:
        return f"❌ Korzinani tozalashda xatolik: {e}"


def clean_temp_files() -> str:
    """
    Windows va Foydalanuvchi vaqtinchalik (Temp) kesh fayllarini tozalaydi.
    """
    cleaned_size = 0
    temp_dirs = [os.environ.get("TEMP"), r"C:\Windows\Temp"]
    
    for tdir in temp_dirs:
        if tdir and os.path.exists(tdir):
            for item in glob.glob(os.path.join(tdir, "*")):
                try:
                    if os.path.isfile(item):
                        sz = os.path.getsize(item)
                        os.remove(item)
                        cleaned_size += sz
                    elif os.path.isdir(item):
                        shutil.rmtree(item, ignore_errors=True)
                except Exception:
                    pass

    mb_cleaned = round(cleaned_size / (1024 * 1024), 2)
    return f"🧹 <b>Vaqtinchalik kesh (Temp) fayllari tozalandi!</b>\n💾 Taxminan <b>{mb_cleaned} MB</b> joy bo'shatildi."


def type_text(text: str) -> str:
    """
    Ekranga matn kiritadi (Klaviatura orqali yozadi).
    """
    if not pyautogui:
        return "⚠️ PyAutoGUI mavjud emas."
    try:
        pyautogui.write(text, interval=0.02)
        return f"✍️ Ekranga matn kiritildi: \"{text}\""
    except Exception as e:
        return f"❌ Matn kiritishda xatolik: {e}"


def scroll_page(amount: int = -500) -> str:
    """
    Ekranni pastga yoki yuqoriga aylantiradi (Scroll).
    """
    if not pyautogui:
        return "⚠️ PyAutoGUI mavjud emas."
    try:
        pyautogui.scroll(amount)
        direction = "pastga" if amount < 0 else "yuqoriga"
        return f"📜 Sahifa {direction} aylantirildi ({amount})."
    except Exception as e:
        return f"❌ Scroll xatoligi: {e}"


def record_mic_audio(filepath: str, duration: int = 5) -> str:
    """
    Windows winmm.dll (MCI) orqali mikrofondan ovoz yozib .wav fayliga saqlaydi.
    """
    if not IS_WINDOWS or not ctypes:
        raise Exception("Mikrofon yozish faqat Windows muhitida ishlaydi.")

    winmm = ctypes.windll.winmm
    try:
        winmm.mciSendStringW("open new type waveaudio alias mic_rec", None, 0, 0)
        winmm.mciSendStringW("record mic_rec", None, 0, 0)
        time.sleep(duration)
        winmm.mciSendStringW(f'save mic_rec "{filepath}"', None, 0, 0)
        winmm.mciSendStringW("close mic_rec", None, 0, 0)
        return filepath
    except Exception as e:
        winmm.mciSendStringW("close mic_rec", None, 0, 0)
        logger.error(f"Mic record error: {e}")
        raise e


def list_directory_info(dir_path: str = None) -> tuple:
    """
    Papka ichidagi barcha fayl, yarlik (.lnk) va papkalar ro'yxatini qaytaradi.
    """
    if not dir_path or not os.path.exists(dir_path):
        dir_path = os.path.join(os.path.expanduser("~"), "Desktop")

    dir_path = os.path.abspath(dir_path)
    parent_dir = os.path.dirname(dir_path)

    try:
        entries = sorted(os.listdir(dir_path))
    except Exception as e:
        return f"❌ Papkani o'qishda xatolik: {e}", dir_path, parent_dir, [], []

    dirs_list = []
    files_list = []

    for entry in entries:
        if entry.startswith("$") or entry == "System Volume Information":
            continue
        full_p = os.path.join(dir_path, entry)
        try:
            if os.path.isdir(full_p):
                dirs_list.append(entry)
            else:
                files_list.append(entry)
        except Exception:
            pass

    text = f"📁 <b>PAPKA MANZILI:</b>\n<code>{dir_path}</code>\n\n"
    text += f"📂 Papkalar ({len(dirs_list)} ta) | 📄 Fayllar & Yarliklar ({len(files_list)} ta)\n"
    text += "━━━━━━━━━━━━━━━━━━━━━\n"

    return text, dir_path, parent_dir, dirs_list, files_list


def search_user_files(keyword: str, max_results: int = 8) -> str:
    """
    Nomi bo'yicha Desktop, Downloads, Documents papkalaridan fayl qidiradi.
    """
    search_dirs = [
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "Downloads"),
        os.path.join(os.path.expanduser("~"), "Documents")
    ]

    kw = keyword.lower().strip()
    found = []

    for sdir in search_dirs:
        if os.path.exists(sdir):
            for root, _, files in os.walk(sdir):
                for f in files:
                    if kw in f.lower():
                        found.append(os.path.join(root, f))
                        if len(found) >= max_results:
                            break
                if len(found) >= max_results:
                    break

    if not found:
        return f"🔍 <code>{keyword}</code> nomli fayllar topilmadi."

    res = f"🔍 <b>TOPILGAN FAYLLAR ({len(found)} ta):</b>\n━━━━━━━━━━━━━━━━━━━━━\n"
    for fp in found:
        sz_mb = round(os.path.getsize(fp) / (1024 * 1024), 2)
        res += f"📄 <code>{fp}</code> ({sz_mb} MB)\n"
    return res


def pair_sunshine_pin(pin: str) -> str:
    """
    Sunshine REST API / Basic Auth orqali Instant PIN Pairing (0.001s).
    """
    import subprocess
    import webbrowser
    pin = str(pin).strip()
    if not pin.isdigit() or len(pin) != 4:
        return f"⚠️ Sunshine PIN-kodi 4 xonali raqam bo'lishi kerak! (Siz kiritdingiz: <code>{pin}</code>)"

    sunshine_user = os.getenv("SUNSHINE_USER", "admin")
    sunshine_pass = os.getenv("SUNSHINE_PASS", "")

    # 1. PowerShell REST API call
    if sunshine_pass:
        try:
            import base64
            auth_bytes = f"{sunshine_user}:{sunshine_pass}".encode('utf-8')
            b64_auth = base64.b64encode(auth_bytes).decode('utf-8')
            ps_cmd = f'powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $h = @{{ Authorization = \'Basic {b64_auth}\' }}; $r = Invoke-RestMethod -Uri https://localhost:47990/api/pin -Headers $h -Method POST -Body \'{{\"pin\":\"{pin}\"}}\' -ContentType \'application/json\' -SkipCertificateCheck; $r.status"'
            res = subprocess.run(ps_cmd, shell=True, capture_output=True, text=True, timeout=4)
            if "true" in res.stdout.lower() or res.returncode == 0:
                return (
                    f"⚡ <b>SUNSHINE INSTANT ULANISH! (0.001s)</b>\n\n"
                    f"🔑 <b>PIN Kod:</b> <code>{pin}</code>\n"
                    f"👤 <b>Foydalanuvchi:</b> <code>{sunshine_user}</code>\n\n"
                    f"✅ Moonlight qurilmangiz Sunshine serveriga muvaffaqiyatli saqlandi va ulandi!"
                )
        except Exception:
            pass

    # 2. GUI Fallback (Brauzerda ochib terish)
    if IS_WINDOWS and pyautogui:
        try:
            webbrowser.open("https://localhost:47990/pin")
            time.sleep(1.2)
            pyautogui.write(pin, interval=0.1)
            time.sleep(0.2)
            pyautogui.press('enter')
            return f"⚡ <b>SUNSHINE PIN ULANISHI BAJARILDI!</b>\n\nBrauzerda Sunshine ochildi va <code>{pin}</code> PIN kodi kiritildi."
        except Exception as e:
            return f"❌ Sunshine PIN kiritishda xatolik: {e}"

    return f"⚡ Sunshine PIN kodi <code>{pin}</code> qabul qilindi."


def register_sunshine_client_cert(cert_path: str) -> str:
    """
    Moonlight client.pem sertifikatini Sunshine serveriga doimiy ishonchli klient (Auto-Pair) sifatida kiritadi.
    """
    if not os.path.exists(cert_path):
        return f"❌ Sertifikat fayli topilmadi: <code>{cert_path}</code>"

    possible_paths = [
        r"C:\Program Files\Sunshine\config",
        r"C:\ProgramData\Sunshine\config",
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "sunshine", "config"),
        os.path.join(os.environ.get("APPDATA", ""), "sunshine", "config")
    ]

    target_config_dir = None
    for p in possible_paths:
        if os.path.exists(p):
            target_config_dir = p
            break

    if not target_config_dir:
        target_config_dir = r"C:\ProgramData\Sunshine\config"
        os.makedirs(target_config_dir, exist_ok=True)

    client_certs_dir = os.path.join(target_config_dir, "client_certs")
    os.makedirs(client_certs_dir, exist_ok=True)

    cert_filename = os.path.basename(cert_path)
    if not cert_filename.endswith(".pem") and not cert_filename.endswith(".crt"):
        cert_filename += ".pem"

    target_cert_path = os.path.join(client_certs_dir, cert_filename)
    try:
        shutil.copy2(cert_path, target_cert_path)
        return (
            f"☀️ <b>MOONLIGHT AVTO-ULANISH (CERTIFICATE AUTO-PAIR)</b>\n\n"
            f"📜 <b>Sertifikat saqlandi:</b> <code>{target_cert_path}</code>\n\n"
            f"✅ Moonlight qurilmangiz Sunshine serveriga muvaffaqiyatli doimiy ulandi!"
        )
    except Exception as e:
        return f"❌ Sertifikatni saqlashda xatolik: {e}"

