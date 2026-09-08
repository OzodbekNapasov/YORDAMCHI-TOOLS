# ============================================================
#  setup_youtube.py
#  YouTube ulanishini boshdan-oxir sozlash va tekshirish
#  Ishlatish:  python setup_youtube.py
# ============================================================

import os
import sys
import json
import subprocess

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

TOKEN_FILE = os.path.join(BASE_DIR, "youtube_token.json")

# Google Console'da o'chirilgan eski client — qayta ishlatilmasligi kerak
DELETED_CLIENT_ID = "694314262963-qcvacuejf00jj6n5fuafokologmeuqa6.apps.googleusercontent.com"


def line(ch="-"):
    print(ch * 60, flush=True)


def step(n, text):
    print(f"\n[{n}] {text}", flush=True)


def fail(msg, hint=""):
    print(f"\n❌ {msg}", flush=True)
    if hint:
        print(f"   → {hint}", flush=True)
    sys.exit(1)


def check_client_secrets():
    """client_secrets.json mavjudligi va eski o'chirilgan client emasligini tekshirish"""
    from services.youtube_auth import find_client_secrets, read_client_config

    path = find_client_secrets()
    if not path:
        fail(
            "client_secrets.json topilmadi.",
            "Google Cloud Console > Credentials > Create Credentials > "
            "OAuth client ID > Desktop app. Yuklab olib, client_secrets.json "
            "nomi bilan shu papkaga tashlang.",
        )

    kind, cfg = read_client_config(path)
    cid = cfg.get("client_id", "")
    print(f"    Fayl      : {os.path.basename(path)}", flush=True)
    print(f"    Tur       : {kind}", flush=True)
    print(f"    Client ID : {cid}", flush=True)

    if cid == DELETED_CLIENT_ID:
        fail(
            "Bu ESKI, Google'da O'CHIRILGAN client. U hech qachon ishlamaydi.",
            "Console'da yangi 'Desktop app' turidagi OAuth client yarating va "
            "shu fayl ustiga yozing.",
        )

    if kind != "installed":
        print(
            "    ⚠️  Bu 'Desktop app' emas ('web'). Avtorizatsiya qo'lda "
            "kod ko'chirishni talab qiladi.",
            flush=True,
        )
    return path


def check_token_alive():
    """Mavjud tokenni Google'ga yuborib, haqiqatan tirikligini tekshirish"""
    import requests

    from services.youtube_service import _get_raw_token_info

    info = _get_raw_token_info()
    if not info or not info.get("refresh_token"):
        return False, "token yo'q"

    r = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": info["client_id"],
            "client_secret": info["client_secret"],
            "refresh_token": info["refresh_token"],
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    if r.status_code == 200:
        return True, "ok"
    return False, r.json().get("error", f"HTTP {r.status_code}")


def run_auth():
    """youtube_auth.py ni interaktiv ishga tushirish"""
    print("\n    Brauzer ochiladi — Google akkauntingiz bilan ruxsat bering.\n", flush=True)
    res = subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, "services", "youtube_auth.py")],
        cwd=BASE_DIR,
    )
    if res.returncode != 0:
        fail("Avtorizatsiya bajarilmadi.")


def verify_channel():
    """API orqali kanalga ulanib, nomini qaytarish — yakuniy isbot"""
    from googleapiclient.discovery import build

    from services.youtube_service import get_youtube_credentials

    creds = get_youtube_credentials()
    yt = build("youtube", "v3", credentials=creds)
    resp = yt.channels().list(part="snippet,contentDetails", mine=True).execute()
    items = resp.get("items", [])
    if not items:
        fail(
            "Token ishladi, lekin bu akkauntga bog'langan YouTube kanal topilmadi.",
            "Ruxsat berishda YouTube kanali bor akkauntni tanlang.",
        )
    return items[0]["snippet"]["title"]


def print_vercel_env():
    """Vercel uchun env var qiymatini chiqarish"""
    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        raw = f.read().strip()

    line("=")
    print("VERCEL UCHUN (Settings > Environment Variables)", flush=True)
    line("=")
    print("Nomi   : YOUTUBE_TOKEN_JSON", flush=True)
    print("Qiymati: (quyidagi bitta qatorni to'liq nusxalang)\n", flush=True)
    print(json.dumps(json.loads(raw), ensure_ascii=False, separators=(",", ":")), flush=True)
    print("", flush=True)
    line("=")


if __name__ == "__main__":
    line("=")
    print("📺 YouTube avtomatik yuklashni sozlash", flush=True)
    line("=")

    step(1, "client_secrets.json tekshirilmoqda...")
    check_client_secrets()
    print("    ✅ Yaroqli", flush=True)

    step(2, "Mavjud token Google'da tirikmi?")
    alive, reason = check_token_alive()
    if alive:
        print("    ✅ Token tirik — qayta avtorizatsiya shart emas", flush=True)
    else:
        print(f"    ⚠️  Yaroqsiz ({reason}) — qayta avtorizatsiya kerak", flush=True)
        step(3, "Avtorizatsiya boshlanmoqda...")
        run_auth()

        alive, reason = check_token_alive()
        if not alive:
            fail(f"Avtorizatsiyadan keyin ham token yaroqsiz: {reason}")
        print("    ✅ Yangi token olindi", flush=True)

    step(4, "YouTube API orqali kanal tekshirilmoqda...")
    title = verify_channel()
    print(f"    ✅ Ulandi — kanal: «{title}»", flush=True)

    print("\n🎉 HAMMASI TAYYOR. Endi video yuklash ishlaydi.\n", flush=True)
    print_vercel_env()
