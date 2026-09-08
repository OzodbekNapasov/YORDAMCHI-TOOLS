# ============================================================
#  services/youtube_service.py
#  ATLAS Platformasi — YouTube Shorts & Video Auto-Uploader
# ============================================================

import os
import sys
import json
import time
# YouTube Upload Scope
SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_FILE = os.path.join(BASE_DIR, "youtube_token.json")
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secrets.json")


def _get_raw_token_info():
    """Token ma'lumotlarini environment, baza yoki fayldan olish.

    Tartib muhim: Vercel'da atlas.db va youtube_token.json deploy'ga kirmaydi
    (.vercelignore), shuning uchun env var birinchi o'rinda turadi. Bu, shu
    bilan birga, bazada qolib ketgan eski tokenning yangisini bosib ketishiga
    ham yo'l qo'ymaydi.
    """
    # 1. Environment o'zgaruvchisidan tekshirish (Vercel / production)
    env_token = os.getenv("YOUTUBE_TOKEN_JSON")
    if env_token and env_token.strip().startswith("{"):
        try:
            return json.loads(env_token.strip())
        except Exception:
            pass

    # 2. DB dan tekshirish (lokal server, refresh'dan keyin yangilanadi)
    try:
        from services.insta_poster_service import get_setting
        db_val = get_setting("youtube_token_json", "")
        if db_val and db_val.strip().startswith("{"):
            return json.loads(db_val.strip())
    except Exception:
        pass

    # 3. Fayldan tekshirish
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

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
                print(f"[YouTube Refresh Token Err]: {e}")
                raise e
        else:
            raise ValueError("YouTube token muddati o'tgan va refresh_token mavjud emas!")

    return creds


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
        return {
            "success": False,
            "error": str(e)
        }
