# ============================================================
#  services/youtube_service.py
#  ATLAS Platformasi — YouTube Shorts & Video Auto-Uploader
# ============================================================

import os
import sys
import json
import time
import base64
import traceback

# YouTube Upload Scope
SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_FILE = os.path.join(BASE_DIR, "youtube_token.json")
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secrets.json")

# Yangi OAuth 2.0 Web Client va Production Refresh Token (Doimiy zaxira)
# DIQQAT: Bu qiymat to'g'ridan-to'g'ri JSON matnidan yasalgan (eski buzilgan
# base64 o'rniga). Agar tokenni yangilasangiz, quyidagi _rebuild_fallback_b64()
# yordam funksiyasi bilan yangi base64 hosil qilishingiz mumkin.
_B64_FALLBACK_TOKEN = "eyJyZWZyZXNoX3Rva2VuIjogIjEvLzA0LVZGem51UERjeWFDZ1lJQVJBQUdBUVNOd0YtTDlJcmlrYzZGRTEwRkxxb1hXVzRJcDhJaWtJWV9oREhzdkE2SGtWTmJXdUt4WFpnYUVwZHA3TFN3R2xfNk0zeDRwNko4TW8iLCAidG9rZW5fdXJpIjogImh0dHBzOi8vb2F1dGgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwgImNsaWVudF9pZCI6ICI2OTQzMTQyNjI5NjMtOGRscjdhcGUzYXZnc2x2ajA1amZkYmI3bW5tNDJjMmkuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCAiY2xpZW50X3NlY3JldCI6ICJHT0NTUFgtampUazBISkFjNmQ2WG81Z2dWQ1l0dmNiWXhqRCIsICJzY29wZXMiOiBbImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL2F1dGgveW91dHViZS51cGxvYWQiLCAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vYXV0aC95b3V0dWJlIl19"


def _rebuild_fallback_b64(refresh_token, client_id, client_secret,
                            token_uri="https://oauth2.googleapis.com/token"):
    """
    Yordamchi funksiya: agar tokenni yangilash kerak bo'lsa, shu funksiyani
    Python konsolida chaqirib to'g'ri base64 string hosil qiling va uni
    yuqoridagi _B64_FALLBACK_TOKEN ga qo'ying.

    Masalan:
        from services.youtube_service import _rebuild_fallback_b64
        print(_rebuild_fallback_b64("1//...", "xxx.apps.googleusercontent.com", "GOCSPX-..."))
    """
    info = {
        "refresh_token": refresh_token,
        "token_uri": token_uri,
        "client_id": client_id,
        "client_secret": client_secret,
        "scopes": SCOPES
    }
    return base64.b64encode(json.dumps(info).encode("utf-8")).decode("utf-8")


def _get_raw_token_info():
    """Token ma'lumotlarini o'qish (Environment > Fayl > Base64 Fallback > Baza)"""
    source = None
    info = None

    # 1. Eng birinchi Vercel Environment o'zgaruvchisidan tekshirish
    env_token = os.getenv("YOUTUBE_TOKEN_JSON")
    if env_token and env_token.strip().startswith("{"):
        try:
            info = json.loads(env_token.strip())
            source = "ENV (YOUTUBE_TOKEN_JSON)"
        except Exception as e:
            print(f"[YouTube Token] ENV JSON parse xatosi: {e}")

    # 2. Lokal fayldan tekshirish
    if info is None and os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r", encoding="utf-8") as f:
                info = json.load(f)
                source = f"FAYL ({TOKEN_FILE})"
        except Exception as e:
            print(f"[YouTube Token] Fayl o'qish xatosi: {e}")

    # 3. Base64 zaxira sozlamadan o'qish
    if info is None:
        try:
            raw_json = base64.b64decode(_B64_FALLBACK_TOKEN.encode('utf-8')).decode('utf-8')
            info = json.loads(raw_json)
            source = "BASE64 FALLBACK"
        except Exception as e:
            print(f"[YouTube Token] Base64 fallback decode xatosi: {e}")

    # 4. DB dan tekshirish (oxirgi variant)
    if info is None:
        try:
            from services.insta_poster_service import get_setting
            db_val = get_setting("youtube_token_json", "")
            if db_val and db_val.strip().startswith("{"):
                info = json.loads(db_val.strip())
                source = "DATABASE (insta_settings)"
        except Exception as e:
            print(f"[YouTube Token] DB o'qish xatosi: {e}")

    if info:
        # Xavfsizlik uchun to'liq secret'ni emas, faqat manba va qisqartirilgan
        # ma'lumotni chiqaramiz - lekin muammoni aniqlash uchun juda foydali.
        masked_secret = (info.get("client_secret", "")[:10] + "...") if info.get("client_secret") else "YO'Q"
        masked_refresh = (info.get("refresh_token", "")[:15] + "...") if info.get("refresh_token") else "YO'Q"
        print(f"[YouTube Token] Manba: {source} | client_id: {info.get('client_id', 'YO`Q')[:20]}... "
              f"| client_secret: {masked_secret} | refresh_token: {masked_refresh}")
    else:
        print("[YouTube Token] HECH QAYERDA token topilmadi (ENV, fayl, base64, DB barchasi bo'sh/xato)")

    return info


def is_youtube_ready():
    """YouTube ulanish va ruxsatnomasi mavjudligini tekshirish"""
    try:
        from google.oauth2.credentials import Credentials
        info = _get_raw_token_info()
        if not info or not info.get("refresh_token"):
            return False
        creds = Credentials.from_authorized_user_info(info, SCOPES)
        return bool(creds and (creds.valid or creds.refresh_token))
    except Exception as e:
        print(f"[YouTube Check Info]: {e}")
        return False


def get_youtube_credentials():
    """OAuth 2.0 orqali ruxsat olingan ma'lumotlarni yuklash yoki yangilash"""
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
    except ImportError as e:
        raise ImportError("Google API kutubxonalari o'rnatilmagan") from e

    info = _get_raw_token_info()
    if not info:
        raise FileNotFoundError("YouTube token ma'lumotlari topilmadi!")

    # Majburiy maydonlarni tekshirish - shu orqali 'invalid_grant' kabi
    # tushunarsiz xatolar o'rniga aniq xabar beramiz
    required_fields = ["refresh_token", "token_uri", "client_id", "client_secret"]
    missing = [f for f in required_fields if not info.get(f)]
    if missing:
        raise ValueError(
            f"YouTube token ma'lumotlarida quyidagi maydonlar yo'q yoki bo'sh: {missing}. "
            f"Token JSON to'liq va to'g'ri ekanligini tekshiring."
        )

    creds = Credentials.from_authorized_user_info(info, SCOPES)

    if not creds.valid:
        if creds.refresh_token:
            try:
                creds.refresh(Request())
                updated_json = creds.to_json()
                try:
                    from services.insta_poster_service import set_setting
                    set_setting("youtube_token_json", updated_json)
                except Exception:
                    pass
                try:
                    with open(TOKEN_FILE, 'w', encoding='utf-8') as token_f:
                        token_f.write(updated_json)
                except Exception:
                    pass
            except Exception as e:
                err_str = str(e)
                print(f"[YouTube Refresh Token Err]: {err_str}")
                print(traceback.format_exc())

                # invalid_grant uchun tushunarli tushuntirish qo'shamiz
                if "invalid_grant" in err_str:
                    raise RuntimeError(
                        "YouTube refresh_token Google tomonidan rad etildi (invalid_grant). "
                        "Bu odatda quyidagi sabablarga ko'ra yuz beradi:\n"
                        "1) client_id/client_secret token olingan paytdagi bilan mos kelmayapti "
                        "(masalan, boshqa Google Cloud loyihasi client'i bilan olingan token ishlatilmoqda);\n"
                        "2) OAuth consent screen 'Testing' rejimida va token 7 kunda eskirgan;\n"
                        "3) Google akkaunt xavfsizlik sozlamalari o'zgargan yoki token qo'lda bekor qilingan;\n"
                        "4) Token boshqa loyiha/环境 uchun yaratilgan.\n"
                        "Yechim: YouTube OAuth flow'ni qaytadan o'tib, yangi refresh_token oling va "
                        "uni ATLAS environment (YOUTUBE_TOKEN_JSON) ga to'liq to'g'ri JSON sifatida joylang."
                    ) from e
                raise e
        else:
            raise ValueError("YouTube token muddati o'tgan va refresh_token mavjud emas!")

    return creds


def upload_video_to_youtube(video_path, caption="", post_url="", privacy="public", is_shorts=True):
    """
    Videoni YouTube (Shorts) ga avtomatik yuklash.
    
    :param video_path: Lokal .mp4 fayl manzili
    :param caption: Instagramdagi post matni
    :param post_url: Instagram post havolasi
    :param privacy: 'public', 'unlisted', yoki 'private'
    :param is_shorts: True bo'lsa sarlavhaga #Shorts qo'shadi
    :return: dict {"success": bool, "video_id": str, "url": str, "error": str}
    """
    if not os.path.exists(video_path):
        return {"success": False, "error": f"Video fayl topilmadi: {video_path}"}

    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        creds = get_youtube_credentials()
        youtube = build('youtube', 'v3', credentials=creds)

        # 1. Sarlavha (Title) tayyorlash (YouTube cheklovi: maksimal 100 belgi)
        first_line = caption.split('\n')[0].strip() if caption else "Shahrisabz Tibbiyot Texnikumi"
        clean_title = first_line.replace("#", "").strip()
        if len(clean_title) > 85:
            clean_title = clean_title[:82] + "..."
            
        if is_shorts and "#Shorts" not in clean_title:
            title = f"{clean_title} #Shorts"
        else:
            title = clean_title

        # 2. Tavsif (Description) tayyorlash
        description_lines = []
        if caption:
            description_lines.append(caption)
        if post_url:
            description_lines.append(f"\n🔗 Instagram: {post_url}")
        description_lines.append("\n#Shahrisabz #Tibbiyot #Texnikum #Shorts #Hamshiralik #Talaba")
        
        description = "\n".join(description_lines)

        # 3. Teglar
        tags = ["Shahrisabz", "Tibbiyot", "Texnikum", "Hamshiralik", "Qabul", "Talabalar", "Shorts"]

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '27'  # 27: Education (Ta'lim)
            },
            'status': {
                'privacyStatus': privacy,
                'selfDeclaredMadeForKids': False
            }
        }

        # 4. Resumable Upload orqali yuklash
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"[YouTube Uploading]: {int(status.progress() * 100)}%")

        video_id = response.get("id")
        yt_url = f"https://youtube.com/shorts/{video_id}" if is_shorts else f"https://youtu.be/{video_id}"
        
        print(f"[YouTube Success]: Video muvaffaqiyatli yuklandi: {yt_url}")
        return {
            "success": True,
            "video_id": video_id,
            "url": yt_url,
            "title": title
        }

    except Exception as e:
        print(f"[YouTube Upload Error]: {e}")
        print(traceback.format_exc())
        return {
            "success": False,
            "error": str(e)
        }
