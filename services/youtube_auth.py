# ============================================================
#  services/youtube_auth.py
#  1 Martalik YouTube Ruxsatnomasini Olish (OAuth 2.0)
# ============================================================

import os
import sys
import glob
import json
from google_auth_oauthlib.flow import InstalledAppFlow

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_FILE = os.path.join(BASE_DIR, "youtube_token.json")
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secrets.json")

LOCAL_PORT = 8088
LOCAL_REDIRECT = f"http://localhost:{LOCAL_PORT}/"


def find_client_secrets():
    """client_secrets.json yoki Google Console'dan yuklangan client_secret_*.json ni topish"""
    if os.path.exists(CLIENT_SECRETS_FILE):
        return CLIENT_SECRETS_FILE
    matches = sorted(
        glob.glob(os.path.join(BASE_DIR, "client_secret_*.json")),
        key=os.path.getmtime,
        reverse=True,
    )
    return matches[0] if matches else None


def read_client_config(path):
    """Fayldan (web yoki installed) client konfiguratsiyasini o'qish"""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    key = "installed" if "installed" in data else "web"
    return key, data.get(key, {})


def save_token(creds):
    """Kalitni ham faylga, ham bazaga yozish.

    Baza qiymati youtube_service.py da fayldan ustun turadi — shuning uchun
    ikkalasini birga yangilamasak, eski token qayta ishlatilib qoladi.
    """
    updated_json = creds.to_json()
    with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
        f.write(updated_json)
    print(f"✅ Faylga saqlandi: {TOKEN_FILE}", flush=True)

    try:
        sys.path.insert(0, BASE_DIR)
        from services.insta_poster_service import set_setting
        set_setting("youtube_token_json", updated_json)
        print("✅ Bazaga (youtube_token_json) ham saqlandi.", flush=True)
    except Exception as e:
        print(f"⚠️  Bazaga saqlab bo'lmadi: {e}", flush=True)


if __name__ == "__main__":
    print("==================================================", flush=True)
    print("📺 YouTube Data API v3 — 1 Martalik Avtorizatsiya", flush=True)
    print("==================================================", flush=True)

    secrets_path = find_client_secrets()
    if not secrets_path:
        print(f"❌ client_secrets.json topilmadi: {BASE_DIR}", flush=True)
        sys.exit(1)

    client_type, cfg = read_client_config(secrets_path)
    redirect_uris = cfg.get("redirect_uris", [])
    print(f"📄 Fayl: {os.path.basename(secrets_path)}  (tur: {client_type})", flush=True)
    print(f"🆔 Client ID: {cfg.get('client_id', '?')}", flush=True)

    use_local = client_type == "installed" or any(
        u.startswith("http://localhost") for u in redirect_uris
    )

    if use_local:
        flow = InstalledAppFlow.from_client_secrets_file(
            secrets_path, scopes=SCOPES, redirect_uri=LOCAL_REDIRECT
        )
        # DIQQAT: bu yerda authorization_url() ni alohida chaqirmaslik kerak.
        # run_local_server() o'zi yangi 'state' bilan boshqa havola yasaydi va
        # foydalanuvchi birinchi havolani ochsa, MismatchingStateError (CSRF) chiqadi.
        # Shuning uchun havolani ham, brauzerni ham run_local_server o'zi boshqaradi.
        print(f"\n⏳ Brauzer ochilmoqda... (localhost:{LOCAL_PORT})", flush=True)
        print("   Ruxsat bergach, shu oynaga qayting.\n", flush=True)

        creds = flow.run_local_server(
            port=LOCAL_PORT,
            prompt='consent',
            access_type='offline',
            open_browser=True,
            authorization_prompt_message=(
                "🔗 Agar brauzer o'zi ochilmasa, shu havolani nusxalab oching:\n\n{url}\n"
            ),
            success_message=(
                "Tayyor! Bu oynani yopib, terminalga qayting."
            ),
        )
    else:
        # "web" turidagi client — localhost ruxsat etilmagan.
        # Ro'yxatdagi birinchi redirect_uri bilan qo'lda (kodni ko'chirib) tasdiqlaymiz.
        if not redirect_uris:
            print("❌ Faylda redirect_uris yo'q. Google Console'dan qayta yuklab oling.", flush=True)
            sys.exit(1)

        redirect_uri = redirect_uris[0]
        flow = InstalledAppFlow.from_client_secrets_file(
            secrets_path, scopes=SCOPES, redirect_uri=redirect_uri
        )
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')

        print(f"\n↩️  Redirect URI: {redirect_uri}", flush=True)
        print("\n🔗 QUYIDAGI HAVOLANI BRAUZERDA OCHING:\n", flush=True)
        print(auth_url, flush=True)
        print("\n--------------------------------------------------", flush=True)
        print("Ruxsat bergach, brauzer manzil qatoridagi ?code=... qiymatini nusxalang.", flush=True)
        print("--------------------------------------------------\n", flush=True)

        try:
            os.system(f'start "" "{auth_url}"')
        except Exception:
            pass

        code = input("📋 Kodni shu yerga qo'ying va Enter bosing: ").strip()
        if not code:
            print("❌ Kod kiritilmadi.", flush=True)
            sys.exit(1)

        flow.fetch_token(code=code)
        creds = flow.credentials

    if not creds.refresh_token:
        print("\n⚠️  DIQQAT: refresh_token qaytmadi! Avtomatik yuklash ishlamaydi.", flush=True)
        print("   myaccount.google.com/permissions dan ilovani o'chirib, qaytadan urinib ko'ring.", flush=True)

    save_token(creds)
    print("\n✅ TABRIKLAYMIZ! YouTube kanalingiz muvaffaqiyatli ulandi.", flush=True)
