# ============================================================
#  services/youtube_auth.py
#  1 Martalik YouTube Ruxsatnomasini Olish (OAuth 2.0)
# ============================================================

import os
import sys
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_FILE = os.path.join(BASE_DIR, "youtube_token.json")
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secrets.json")

if __name__ == "__main__":
    print("==================================================", flush=True)
    print("📺 YouTube Data API v3 — 1 Martalik Avtorizatsiya", flush=True)
    print("==================================================", flush=True)
    
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print(f"❌ client_secrets.json topilmadi: {CLIENT_SECRETS_FILE}", flush=True)
        sys.exit(1)
        
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:8088/'
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    
    print("\n🔗 QUYIDAGI HAVOLANI BRAUZERDA OCHING:\n", flush=True)
    print(auth_url, flush=True)
    print("\n--------------------------------------------------\n", flush=True)
    
    # Brauzerni ochishga urinish
    try:
        os.system(f'start "" "{auth_url}"')
    except Exception as e:
        print(f"Brauzerni ochib bo'lmadi: {e}", flush=True)
        
    print("⏳ Ruxsat berishingiz kutilmoqda (localhost:8088)...", flush=True)
    
    creds = flow.run_local_server(port=8088, prompt='consent', open_browser=False)
    
    with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
        f.write(creds.to_json())
        
    print("\n✅ TABRIKLAYMIZ! YouTube kanalingiz muvaffaqiyatli ulandi.", flush=True)
    print(f"Kalit saqlandi: {TOKEN_FILE}", flush=True)
