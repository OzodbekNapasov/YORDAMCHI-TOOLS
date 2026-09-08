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

# DIQQAT: bu yerda ilgari _B64_FALLBACK_TOKEN bo'lgan — kodga base64 ko'rinishida
# yozilgan tirik refresh_token va client_secret. U olib tashlandi: manba kodiga
# yozilgan kalit repoga tushadi va git tarixida abadiy qoladi. Kalitlar faqat
# YOUTUBE_TOKEN_JSON env o'zgaruvchisi, Supabase yoki youtube_token.json orqali
# beriladi (quyidagi _iter_token_sources ga qarang).


def _mask(info, source):
    """Token manbasini xavfsiz ko'rinishda logga chiqarish (secret to'liq emas)"""
    try:
        # client_id maxfiy emas (har bir OAuth so'rovida ochiq yuboriladi), shuning
        # uchun uni to'liq ko'rsatsa bo'ladi. client_secret va refresh_token esa
        # loglarga (Vercel log'lari ham) hech qanday ko'rinishda tushmasligi kerak —
        # faqat mavjud/yo'qligini bildiramiz.
        cid = info.get("client_id") or "YO'Q"
        print(f"[YouTube Token] Manba: {source} | client_id: {cid} "
              f"| client_secret: {'bor' if info.get('client_secret') else 'YO`Q'} "
              f"| refresh_token: {'bor' if info.get('refresh_token') else 'YO`Q'}")
    except Exception:
        pass


def _iter_token_sources():
    """Mavjud barcha token manbalarini (nom, ma'lumot) ko'rinishida qaytarish.

    Bitta manbaga tayanish xavfli: Vercel'dagi eski YOUTUBE_TOKEN_JSON yoki
    bazada qolib ketgan eski token butun tizimni to'xtatib qo'yadi. Shuning
    uchun get_youtube_credentials() birinchi ISHLAYDIGANini tanlaydi.
    """
    env_token = os.getenv("YOUTUBE_TOKEN_JSON")
    if env_token and env_token.strip().startswith("{"):
        try:
            yield "ENV (YOUTUBE_TOKEN_JSON)", json.loads(env_token.strip())
        except Exception as e:
            print(f"[YouTube Token] ENV JSON parse xatosi: {e}")

    try:
        from services.insta_poster_service import get_setting
        db_val = get_setting("youtube_token_json", "")
        if db_val and db_val.strip().startswith("{"):
            yield "BAZA/Supabase (insta_settings)", json.loads(db_val.strip())
    except Exception as e:
        print(f"[YouTube Token] DB o'qish xatosi: {e}")

    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r", encoding="utf-8") as f:
                yield f"FAYL ({TOKEN_FILE})", json.load(f)
        except Exception as e:
            print(f"[YouTube Token] Fayl o'qish xatosi: {e}")


def _get_raw_token_info():
    """Birinchi mavjud token ma'lumotini qaytarish (yaroqliligini tekshirmasdan)"""
    for name, info in _iter_token_sources():
        _mask(info, name)
        return info
    print("[YouTube Token] HECH QAYERDA token topilmadi (ENV, baza, fayl — barchasi bo'sh/xato)")
    return None


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


def _persist_token(updated_json):
    """Yangilangan tokenni bazaga (Supabase) va faylga yozish"""
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


def get_youtube_credentials():
    """Ishlaydigan birinchi token manbasini topib, ruxsatnomani qaytarish.

    Manbalar ketma-ket sinaladi (env -> baza/Supabase -> fayl). Biri yaroqsiz
    bo'lsa (masalan Vercel'da eski YOUTUBE_TOKEN_JSON qolib ketgan bo'lsa),
    keyingisiga o'tiladi. Muvaffaqiyatli yangilangan token qolgan manbalarga
    ham yoziladi, shunda eski nusxa o'z-o'zidan tuzaladi.
    """
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
    except ImportError as e:
        raise ImportError("Google API kutubxonalari o'rnatilmagan") from e

    errors = []
    tried = 0

    for name, info in _iter_token_sources():
        tried += 1

        # Majburiy maydonlarni oldindan tekshirish — shu orqali 'invalid_grant'
        # kabi tushunarsiz xatolar o'rniga aniq sabab ko'rsatiladi
        missing = [f for f in ("refresh_token", "token_uri", "client_id", "client_secret")
                   if not info.get(f)]
        if missing:
            errors.append(f"{name}: quyidagi maydonlar yo'q — {', '.join(missing)}")
            continue

        try:
            creds = Credentials.from_authorized_user_info(info, SCOPES)
            if not creds.valid:
                creds.refresh(Request())
                _persist_token(creds.to_json())
            return creds
        except Exception as e:
            msg = str(e)
            errors.append(f"{name}: {msg[:120]}")
            print(f"[YouTube Token Manbasi Yaroqsiz] {name}: {msg[:160]}")
            continue

    if tried == 0:
        raise FileNotFoundError("YouTube token ma'lumotlari topilmadi!")

    detail = "Hech bir YouTube token manbasi ishlamadi:\n  " + "\n  ".join(errors)
    joined = " ".join(errors)

    if "invalid_grant" in joined:
        detail += (
            "\n\ninvalid_grant — Google refresh_token'ni rad etdi. Sabablari:\n"
            "  1) client_id/client_secret token olingan paytdagidan boshqa "
            "(masalan boshqa Google Cloud loyihasi client'i ishlatilmoqda);\n"
            "  2) OAuth consent screen 'Testing' rejimida va token 7 kunda eskirgan;\n"
            "  3) Ruxsat qo'lda bekor qilingan yoki akkaunt xavfsizligi o'zgargan.\n"
            "  Yechim: python setup_youtube.py — qaytadan avtorizatsiya qiling."
        )
    elif "deleted_client" in joined:
        detail += (
            "\n\ndeleted_client — OAuth client Google Cloud Console'da o'chirilgan.\n"
            "  Yechim: Console'da yangi OAuth client yarating, client_secrets.json "
            "ni almashtiring va python setup_youtube.py ni ishga tushiring."
        )

    raise ValueError(detail)


def upload_video_to_youtube(video_path, caption="", post_url="", privacy="public",
                            is_shorts=True, keep_caption=True):
    """
    Videoni YouTube (Shorts) ga avtomatik yuklash.

    :param video_path: Lokal .mp4 fayl manzili
    :param caption: Instagramdagi post matni
    :param post_url: Instagram post havolasi
    :param privacy: 'public', 'unlisted', yoki 'private'
    :param is_shorts: False bo'lsa havola /shorts/ o'rniga youtu.be ko'rinishida qaytadi
    :param keep_caption: True (standart) — izoh Instagramdagi holicha qoladi:
        sarlavhaga #Shorts, tavsifga havola yoki qo'shimcha teglar qo'shilmaydi.
        False — eski xatti-harakat (havola + doimiy teglar qo'shiladi).
    :return: dict {"success": bool, "video_id": str, "url": str, "error": str}
    """
    if not os.path.exists(video_path):
        return {"success": False, "error": f"Video fayl topilmadi: {video_path}"}

    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        creds = get_youtube_credentials()
        youtube = build('youtube', 'v3', credentials=creds)

        # 1. Sarlavha (Title) — YouTube cheklovi: maksimal 100 belgi
        first_line = caption.split('\n')[0].strip() if caption else "Shahrisabz Tibbiyot Texnikumi"

        if keep_caption:
            # Izoh o'zgarmaydi. Sarlavhada faqat YouTube taqiqlagan < va > tozalanadi
            # (aks holda API 400 qaytaradi) va 100 belgiga sig'diriladi.
            title = first_line.replace("<", "").replace(">", "").strip()
            if len(title) > 100:
                title = title[:97] + "..."
            description = caption
            tags = None
        else:
            clean_title = first_line.replace("#", "").strip()
            if len(clean_title) > 85:
                clean_title = clean_title[:82] + "..."

            if is_shorts and "#Shorts" not in clean_title:
                title = f"{clean_title} #Shorts"
            else:
                title = clean_title

            description_lines = []
            if caption:
                description_lines.append(caption)
            if post_url:
                description_lines.append(f"\n🔗 Instagram: {post_url}")
            description_lines.append("\n#Shahrisabz #Tibbiyot #Texnikum #Shorts #Hamshiralik #Talaba")
            description = "\n".join(description_lines)
            tags = ["Shahrisabz", "Tibbiyot", "Texnikum", "Hamshiralik", "Qabul", "Talabalar", "Shorts"]

        if not title:
            title = "Shahrisabz Tibbiyot Texnikumi"

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'categoryId': '27'  # 27: Education (Ta'lim)
            },
            'status': {
                'privacyStatus': privacy,
                'selfDeclaredMadeForKids': False
            }
        }
        if tags:
            body['snippet']['tags'] = tags

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
