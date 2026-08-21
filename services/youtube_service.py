# ============================================================
#  services/youtube_service.py
#  ATLAS Platformasi — YouTube Shorts & Video Auto-Uploader
# ============================================================

import os
import sys
import json
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# YouTube Upload Scope
SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_FILE = os.path.join(BASE_DIR, "youtube_token.json")
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secrets.json")


def is_youtube_ready():
    """YouTube ulanish va ruxsatnomasi mavjudligini tekshirish"""
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            if creds and (creds.valid or (creds.expired and creds.refresh_token)):
                return True
        except Exception:
            pass
    return False


def get_youtube_credentials():
    """OAuth 2.0 orqali ruxsat olingan ma'lumotlarni yuklash yoki yangilash"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            print(f"[YouTube Creds Load Err]: {e}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(TOKEN_FILE, 'w', encoding='utf-8') as token_f:
                    token_f.write(creds.to_json())
            except Exception as e:
                print(f"[YouTube Refresh Token Err]: {e}")
                creds = None
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                raise FileNotFoundError(
                    f"client_secrets.json fayli topilmadi! Iltimos, Google Cloud Console'dan yuklab olib {CLIENT_SECRETS_FILE} manziliga qo'ying."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=8088, prompt='consent')
            with open(TOKEN_FILE, 'w', encoding='utf-8') as token_f:
                token_f.write(creds.to_json())

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
        creds = get_youtube_credentials()
        youtube = build('youtube', 'v3', credentials=creds)

        # 1. Sarlavha (Title) tayyorlash (YouTube cheklovi: maksimal 100 belgi)
        first_line = caption.split('\n')[0].strip() if caption else "Shahrisabz Tibbiyot Texnikumi"
        # Belgilarni tozalash
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
                'categoryId': '27' # 27: Education (Ta'lim)
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
        return {
            "success": False,
            "error": str(e)
        }
