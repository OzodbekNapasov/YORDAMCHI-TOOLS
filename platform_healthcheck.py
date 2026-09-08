# ============================================================
#  platform_healthcheck.py
#  ATLAS platformasining barcha qismlarini tekshirish.
#  Hech narsani o'zgartirmaydi — faqat o'qiydi va hisobot beradi.
#
#  Ishlatish:  python platform_healthcheck.py
# ============================================================

import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

OK, WARN, BAD = "[ OK ]", "[OGOH]", "[XATO]"
results = []


def check(name, fn):
    try:
        status, detail = fn()
    except Exception as e:
        status, detail = BAD, f"{type(e).__name__}: {e}"
    results.append((status, name, detail))
    print(f"{status} {name}")
    for line in str(detail).split("\n"):
        if line.strip():
            print(f"       {line}")


def section(title):
    print("\n" + "=" * 62)
    print(f"  {title}")
    print("=" * 62)


# ---------------- 1. Kutubxonalar ----------------
def c_deps():
    import importlib
    need = ["flask", "telebot", "yt_dlp", "googleapiclient", "google_auth_oauthlib",
            "requests", "supabase", "PIL", "docx", "openpyxl", "reportlab", "fpdf"]
    missing = []
    for m in need:
        try:
            importlib.import_module(m)
        except Exception:
            missing.append(m)
    if missing:
        return WARN, "O'rnatilmagan: " + ", ".join(missing)
    return OK, f"{len(need)} ta asosiy kutubxona joyida"


def c_playwright():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return BAD, "playwright o'rnatilmagan -> Instagram skanerlash ishlamaydi"
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            b.close()
        return OK, "Chromium ishga tushdi (Instagram skaneri tayyor)"
    except Exception as e:
        return BAD, f"Chromium yo'q: {str(e)[:120]}\nTuzatish: python -m playwright install chromium"


# ---------------- 2. Ma'lumotlar bazasi ----------------
def c_sqlite():
    from services.insta_poster_service import get_db_connection
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM insta_posts_queue")
    n = c.fetchone()[0]
    db_path = os.path.join(BASE_DIR, "atlas.db")
    size = os.path.getsize(db_path) / 1024 / 1024 if os.path.exists(db_path) else 0
    conn.close()
    return OK, f"atlas.db {size:.0f} MB, navbatda {n} ta post"


def c_supabase():
    import requests
    from services.atlas_db import _get_supabase_credentials
    url, key = _get_supabase_credentials()
    if not url or not key:
        return BAD, "SUPABASE_URL / SUPABASE_KEY topilmadi"
    r = requests.get(f"{url}/rest/v1/atlas_settings?select=key&limit=1",
                     headers={"apikey": key, "Authorization": f"Bearer {key}"}, timeout=10)
    if r.status_code == 200:
        return OK, f"Ulandi ({url.split('//')[-1][:32]}...)"
    return BAD, f"HTTP {r.status_code}: {r.text[:120]}"


# ---------------- 3. YouTube ----------------
def c_youtube():
    from services.youtube_service import get_youtube_credentials
    from googleapiclient.discovery import build
    yt = build("youtube", "v3", credentials=get_youtube_credentials())
    ch = yt.channels().list(part="snippet,statistics", mine=True).execute()["items"][0]
    return OK, (f"Kanal: {ch['snippet']['title']} | "
                f"{ch['statistics'].get('videoCount','?')} video, "
                f"{ch['statistics'].get('subscriberCount','?')} obunachi")


def c_youtube_quota():
    from services.insta_poster_service import get_db_connection
    from datetime import datetime
    conn = get_db_connection()
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT COUNT(*) FROM insta_posts_queue WHERE youtube_uploaded_at LIKE ?", (today + "%",))
    used = c.fetchone()[0]
    c.execute("""SELECT COUNT(*) FROM insta_posts_queue WHERE youtube_uploaded = 0
                 AND (media_type IN ('reel','video','unknown') OR post_url LIKE '%/reel/%')""")
    left = c.fetchone()[0]
    conn.close()
    msg = f"Bugun {used} ta yuklangan (kunlik limit ~6). Navbatda {left} ta kutmoqda."
    return (WARN if used >= 6 else OK), msg


# ---------------- 4. Telegram ----------------
def c_telegram():
    import requests
    tok = os.getenv("BOT_TOKEN")
    if not tok:
        return BAD, "BOT_TOKEN yo'q"
    r = requests.get(f"https://api.telegram.org/bot{tok}/getMe", timeout=10)
    if r.status_code == 200 and r.json().get("ok"):
        u = r.json()["result"]
        return OK, f"@{u.get('username')} ({u.get('first_name')})"
    return BAD, f"HTTP {r.status_code}: {r.text[:120]}"


# ---------------- 5. Instagram ----------------
def c_instagram():
    import yt_dlp
    url = "https://www.instagram.com/shahrisabz_t_t_uz/reel/DXzVIPBIVdy/"
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True,
                           "skip_download": True, "socket_timeout": 20}) as y:
        info = y.extract_info(url, download=False)
    if info:
        return OK, "yt-dlp Instagram'dan ma'lumot oldi (IP bloklanmagan)"
    return BAD, "Ma'lumot olinmadi"


# ---------------- 6. Jadval / Scheduler ----------------
def c_schedule():
    from services.insta_poster_service import get_setting, get_youtube_schedule_times
    times = get_youtube_schedule_times()
    yt_on = get_setting("youtube_schedule_enabled", "1") == "1"
    yt_auto = get_setting("youtube_auto_upload", "1") == "1"
    tg_on = get_setting("auto_schedule_enabled", "1") == "1"
    times_str = ", ".join(times) if times else "(belgilanmagan)"
    lines = [f"YouTube vaqtlari: {times_str}",
             f"youtube_schedule_enabled={yt_on}  youtube_auto_upload={yt_auto}",
             f"Telegram avto-jadval: {tg_on}"]
    st = OK if (yt_on and yt_auto and times) else WARN
    return st, "\n".join(lines)


def c_scheduler_running():
    import subprocess
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
             "Select-Object -ExpandProperty CommandLine"],
            capture_output=True, text=True, timeout=25).stdout
    except Exception as e:
        return WARN, f"Jarayonlarni tekshirib bo'lmadi: {e}"

    lines = [l.strip() for l in (out or "").split("\n") if l.strip()]
    bot = [l for l in lines if "bot.py" in l]
    worker = [l for l in lines if "run_insta_worker" in l]
    bridge = [l for l in lines if "run_pc_bridge" in l]

    msg = []
    msg.append(("ISHLAMOQDA" if bot else "TO'XTAGAN") + "  bot.py (scheduler shu yerda)")
    msg.append(("ISHLAMOQDA" if worker else "to'xtagan") + "  run_insta_worker.py (muqobil)")
    msg.append(("ISHLAMOQDA" if bridge else "TO'XTAGAN") + "  run_pc_bridge.py (Vercel tugmalari uchun)")
    st = OK if (bot or worker) else BAD
    if not bridge:
        st = WARN if st == OK else st
    return st, "\n".join(msg)


def c_vercel_cron():
    p = os.path.join(BASE_DIR, "vercel.json")
    cfg = json.load(open(p, encoding="utf-8"))
    if "crons" in cfg:
        return OK, f"Vercel cron sozlangan: {cfg['crons']}"
    return WARN, ("vercel.json da 'crons' yo'q.\n"
                  "/instagram/cron_tick endpoint bor, lekin uni hech kim chaqirmaydi.\n"
                  "Jadval faqat shu kompyuterda bot.py ishlab turganda bajariladi.")


# ---------------- 7. PC Bridge ----------------
def c_bridge():
    from services.pc_control.bridge import get_bridge_pc_status
    st = get_bridge_pc_status()
    online = st.get("online") or st.get("is_online")
    return (OK if online else WARN), f"Bridge holati: {json.dumps(st, ensure_ascii=False)[:200]}"


def c_bridge_actions():
    from services.pc_control.bridge import _execute_command_locally
    import inspect
    src = inspect.getsource(_execute_command_locally)
    acts = sorted(set(__import__("re").findall(r'action == "([a-z_]+)"', src)))
    has_yt = "youtube_upload" in acts
    return (OK if has_yt else BAD), f"{len(acts)} ta buyruq: {', '.join(acts)}"


def c_startup():
    startup = os.path.join(os.getenv("APPDATA", ""),
                           r"Microsoft\Windows\Start Menu\Programs\Startup")
    if not os.path.isdir(startup):
        return WARN, "Startup papkasi topilmadi"
    files = os.listdir(startup)
    has_bridge = any("bridge" in f.lower() or "atlas" in f.lower() for f in files)
    if has_bridge:
        return OK, "Bridge avtoishga tushirishga qo'yilgan"
    files_str = ", ".join(files) if files else "(bo'sh)"
    return WARN, ("PC Bridge Startup papkasida YO'Q -> kompyuter yonganda o'zi ishga tushmaydi.\n"
                  f"Mavjud: {files_str}\n"
                  "Tuzatish: Win+R -> shell:startup -> AUTORUN_BRIDGE_FONDA.vbs yorlig'ini tashlang")


def c_task_scheduler():
    import subprocess
    try:
        r = subprocess.run(["schtasks", "/query", "/tn", "ATLAS YouTube kunlik"],
                           capture_output=True, text=True, timeout=20)
        if r.returncode == 0:
            return OK, "Windows vazifasi ro'yxatdan o'tgan"
    except Exception:
        pass
    return WARN, ("'ATLAS YouTube kunlik' vazifasi yo'q (ixtiyoriy — jadval bot.py orqali ham ishlaydi)")


# ---------------- 8. Vercel ----------------
def c_vercel_live():
    import requests
    r = requests.get("https://atlas-my-tools.vercel.app", timeout=20, allow_redirects=True)
    return (OK if r.status_code < 500 else BAD), f"HTTP {r.status_code} — sayt javob bermoqda"


# ---------------- 9. Fayl/konfiguratsiya ----------------
def c_secrets_ignored():
    import subprocess
    risky = ["client_secrets.json", "youtube_token.json", ".env", "atlas.db"]
    leaked = []
    for f in risky:
        r = subprocess.run(["git", "check-ignore", f], cwd=BASE_DIR,
                           capture_output=True, text=True)
        if r.returncode != 0 and os.path.exists(os.path.join(BASE_DIR, f)):
            leaked.append(f)
    if leaked:
        return BAD, "GIT'GA TUSHISHI MUMKIN: " + ", ".join(leaked)
    return OK, "Barcha maxfiy fayllar .gitignore bilan himoyalangan"


if __name__ == "__main__":
    print("=" * 62)
    print("  ATLAS PLATFORMASI — TO'LIQ TEKSHIRUV")
    print("=" * 62)

    section("1. Muhit va kutubxonalar")
    check("Python kutubxonalari", c_deps)
    check("Playwright / Chromium (Instagram skaneri)", c_playwright)

    section("2. Ma'lumotlar bazasi")
    check("SQLite (atlas.db)", c_sqlite)
    check("Supabase bulut", c_supabase)

    section("3. Tashqi xizmatlar")
    check("YouTube API", c_youtube)
    check("YouTube kunlik kvota", c_youtube_quota)
    check("Telegram bot", c_telegram)
    check("Instagram (yt-dlp)", c_instagram)

    section("4. Jadval (avtomatik joylash)")
    check("Jadval sozlamalari", c_schedule)
    check("Scheduler jarayoni", c_scheduler_running)
    check("Vercel cron", c_vercel_cron)
    check("Windows kunlik vazifa", c_task_scheduler)

    section("5. PC Bridge (Vercel <-> kompyuter)")
    check("Bridge buyruqlari", c_bridge_actions)
    check("Bridge holati", c_bridge)
    check("Avtoishga tushirish (Startup)", c_startup)

    section("6. Veb platforma")
    check("Vercel sayti", c_vercel_live)

    section("7. Xavfsizlik")
    check("Maxfiy fayllar himoyasi", c_secrets_ignored)

    # ---- Yakuniy hisobot ----
    print("\n" + "=" * 62)
    print("  YAKUN")
    print("=" * 62)
    n_ok = sum(1 for s, _, _ in results if s == OK)
    n_warn = sum(1 for s, _, _ in results if s == WARN)
    n_bad = sum(1 for s, _, _ in results if s == BAD)
    print(f"  OK: {n_ok}   Ogohlantirish: {n_warn}   Xato: {n_bad}\n")

    for s, name, detail in results:
        if s != OK:
            print(f"{s} {name}")
            for line in str(detail).split("\n"):
                if line.strip():
                    print(f"       {line}")
    if n_bad == 0 and n_warn == 0:
        print("  Hammasi joyida.")
