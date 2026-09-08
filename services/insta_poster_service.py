# ============================================================
#  services/insta_poster_service.py
#  ATLAS Platformasi — Instagram to Telegram & YouTube AutoPoster Moduli
# ============================================================

import os
import sys
import re
import json
import time
import asyncio
import tempfile
import threading
import traceback
import subprocess
import requests
import telebot
from datetime import datetime, timezone, timedelta
from services.atlas_db import get_db_connection

UZB_TZ = timezone(timedelta(hours=5))

def get_uzb_now():
    """Toshkent (O'zbekiston, UTC+5) bo'yicha joriy vaqtni olish"""
    return datetime.now(timezone.utc).astimezone(UZB_TZ).replace(tzinfo=None)


# ------------------------------------------------------------
# 1.1. Supabase Cloud State Sync (Vercel Serverless Persistent Sync)
# ------------------------------------------------------------

def _get_supabase_headers():
    from services.atlas_db import _get_supabase_credentials
    supa_url, supa_key = _get_supabase_credentials()
    if not supa_url or not supa_key:
        return None, None
    headers = {
        "apikey": supa_key,
        "Authorization": f"Bearer {supa_key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }
    return supa_url, headers


def load_insta_cloud_state():
    """Supabase Cloud dan yuborilgan postlar va YouTube yuklanganlar holatini olish"""
    try:
        supa_url, headers = _get_supabase_headers()
        if supa_url and headers:
            r = requests.get(f"{supa_url}/rest/v1/atlas_settings?key=eq.insta_poster_state", headers=headers, timeout=5)
            if r.status_code == 200 and r.json():
                raw_val = r.json()[0].get("value")
                if raw_val:
                    return json.loads(raw_val)
    except Exception as e:
        print(f"[Supabase Load Insta State Info]: {e}")
        
    # Local fallback
    try:
        val = get_setting("insta_poster_state_local", "")
        if val:
            return json.loads(val)
    except Exception:
        pass
    return {"sent_shortcodes": {}, "yt_uploaded_shortcodes": {}, "last_post_time": ""}


def save_insta_cloud_state(state: dict):
    """Supabase Cloud ga holatni saqlash (Rekursiyasiz: to'g'ridan-to'g'ri DB ga yozish)"""
    # LOCAL: to'g'ridan-to'g'ri SQLite ga yozamiz (set_setting orqali EMAS!)
    # set_setting → save_insta_cloud_state → set_setting cheksiz siklini oldini olish uchun
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO insta_settings (key, value) VALUES (?, ?)",
                       ("insta_poster_state_local", json.dumps(state)))
        conn.commit()
        conn.close()
    except Exception as _db_e:
        print(f"[Cloud State Local Save Err]: {_db_e}")

    # CLOUD: Supabase ga yuborish
    try:
        supa_url, headers = _get_supabase_headers()
        if supa_url and headers:
            payload = {
                "key": "insta_poster_state",
                "value": json.dumps(state),
                "category": "instagram",
                "description": "Instagram & YouTube AutoPoster persistent cloud state"
            }
            requests.post(f"{supa_url}/rest/v1/atlas_settings", headers=headers, json=payload, timeout=5)
    except Exception as e:
        print(f"[Supabase Save Insta State Err]: {e}")


def mark_post_sent_in_cloud(shortcode: str, sent_at_str: str):
    """Post Telegramga yuborilganda bulut holatiga yozish (set_setting CHAQIRILMAYDI - tez)"""
    try:
        state = load_insta_cloud_state()
        if "sent_shortcodes" not in state:
            state["sent_shortcodes"] = {}
        state["sent_shortcodes"][shortcode] = sent_at_str
        state["last_post_time"] = sent_at_str
        if "settings" not in state:
            state["settings"] = {}
        state["settings"]["last_post_time"] = sent_at_str
        save_insta_cloud_state(state)  # 1 ta Supabase so'rovi
    except Exception as e:
        print(f"[Cloud Mark Sent Err]: {e}")


def mark_youtube_uploaded_in_cloud(shortcode: str, yt_url: str):
    """Post YouTubega yuklanganda bulut holatiga yozish"""
    try:
        state = load_insta_cloud_state()
        if "yt_uploaded_shortcodes" not in state:
            state["yt_uploaded_shortcodes"] = {}
        state["yt_uploaded_shortcodes"][shortcode] = yt_url
        save_insta_cloud_state(state)
    except Exception as e:
        print(f"[Cloud Mark YT Err]: {e}")


def notify_admin_post_published(platform, item_info):
    """Post Telegram yoki YouTube ga chiqqanda adminga (ID: 8135594558) avtomatik inline tugmali bildirishnoma yuborish"""
    try:
        admin_id = 8135594558
        bot_tokens = [
            "8937819411:AAHrCwLyr_Ob3bM0ypwNFYP-SKb1weL97fs",
            get_setting("bot_token", DEFAULT_BOT_TOKEN)
        ]
        
        now_formatted = get_uzb_now().strftime("%H:%M:%S (%d.%m.%Y)")
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        
        if platform == "telegram":
            caption_preview = (item_info.get("caption") or "").strip()
            if len(caption_preview) > 200:
                caption_preview = caption_preview[:197] + "..."
            
            text = (
                f"🚀 <b>Telegram Kanalga Yangi Post Joylandi!</b>\n\n"
                f"🎬 <b>Reels:</b> <code>{item_info.get('shortcode', '')}</code>\n"
                f"📝 <b>Matn:</b> {caption_preview if caption_preview else '(Matnsiz)'}\n"
                f"🔗 <b>Instagram:</b> {item_info.get('post_url', '')}\n"
                f"⏰ <b>Vaqt:</b> {now_formatted}\n\n"
                f"<i>Quyidagi inline tugmalar orqali to‘g‘ridan-to‘g‘ri postni ko‘rishingiz mumkin:</i>"
            )
            
            tg_msg_id = item_info.get("msg_id") or item_info.get("telegram_msg_id")
            target_chat = str(item_info.get("target_chat_id") or get_setting("target_chat_id", DEFAULT_TARGET_CHAT_ID))
            if tg_msg_id:
                if target_chat.startswith("@"):
                    tg_link = f"https://t.me/{target_chat.lstrip('@')}/{tg_msg_id}"
                else:
                    cid_clean = target_chat.replace("-100", "").replace("-", "")
                    tg_link = f"https://t.me/c/{cid_clean}/{tg_msg_id}"
                markup.add(telebot.types.InlineKeyboardButton("🔵 Telegram Kanalda Ko‘rish ↗️", url=tg_link))
                
            if item_info.get("post_url"):
                markup.add(telebot.types.InlineKeyboardButton("📸 Instagram Postini Ochish ↗️", url=item_info.get("post_url")))
            markup.add(telebot.types.InlineKeyboardButton("🌐 ATLAS Boshqaruv Paneli ↗️", url="https://atlas-my-tools.vercel.app"))
            
        elif platform == "youtube":
            text = (
                f"🎬 <b>YouTube Shorts ga Yangi Video Yuklandi!</b>\n\n"
                f"📌 <b>Sarlavha:</b> {item_info.get('title', '')}\n"
                f"🔗 <b>YouTube:</b> {item_info.get('url', '')}\n"
                f"📸 <b>Instagram:</b> {item_info.get('post_url', '')}\n"
                f"⏰ <b>Vaqt:</b> {now_formatted}\n\n"
                f"<i>Quyidagi inline tugmalar orqali Shorts videoni tomosha qilishingiz mumkin:</i>"
            )
            if item_info.get("url"):
                markup.add(telebot.types.InlineKeyboardButton("🔴 YouTubeda Ko‘rish (Shorts) ↗️", url=item_info.get("url")))
            if item_info.get("post_url"):
                markup.add(telebot.types.InlineKeyboardButton("📸 Instagram Asl Posti ↗️", url=item_info.get("post_url")))
            markup.add(telebot.types.InlineKeyboardButton("🌐 ATLAS Boshqaruv Paneli ↗️", url="https://atlas-my-tools.vercel.app"))
        else:
            return
            
        for tok in bot_tokens:
            if not tok: continue
            try:
                t_bot = telebot.TeleBot(tok)
                t_bot.send_message(admin_id, text, parse_mode="HTML", reply_markup=markup)
                break
            except Exception as _e:
                print(f"[Notify Admin Err with tok {tok[:10]}]: {_e}")
    except Exception as e:
        print(f"[Notify Admin Post Published General Error]: {e}")


DEFAULT_BOT_TOKEN = "8818017813:AAEJTzJ97jCPIYy5exZSjFNHOcSvcHkjDJk"
DEFAULT_TARGET_CHAT_ID = "-1004295470034"
DEFAULT_INSTA_USERNAME = "shahrisabz_t_t_uz"

# Barcha 74 ta Video Reels postlar (DTHudhLiEJT dan keyingi yangi postlar, eskisidan yangisiga qarab)
DEFAULT_SEEDED_POSTS = [
    {
        "shortcode": "DTNEIiLCBPn",
        "post_url": "https://www.instagram.com/reel/DTNEIiLCBPn",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nHammada shunaqami?🤦🏻‍♀️\n\n#top #trendy #rek #top #sh_t_t\nView all 59 comments",
        "media_url": "",
        "post_date": ""
    }
]


_INIT_INSTA_DONE = False
_LAST_CLOUD_SYNC_TS = 0

def init_insta_tables(force=False):
    """Instagram jadvallarini yaratish va videolarni bazaga sinxronlash (Ultra-fast cached)"""
    global _INIT_INSTA_DONE, _LAST_CLOUD_SYNC_TS
    now_ts = time.time()
    if _INIT_INSTA_DONE and not force and (now_ts - _LAST_CLOUD_SYNC_TS < 180):
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Navbat jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insta_posts_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shortcode TEXT UNIQUE,
        post_url TEXT NOT NULL,
        media_type TEXT DEFAULT 'reel',
        caption TEXT,
        media_url TEXT,
        post_date TEXT,
        status TEXT DEFAULT 'PENDING',
        scheduled_at TIMESTAMP,
        sent_at TIMESTAMP,
        error_msg TEXT,
        likes_count INTEGER DEFAULT 0,
        telegram_msg_id INTEGER,
        youtube_uploaded INTEGER DEFAULT 0,
        youtube_url TEXT,
        youtube_uploaded_at TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Migration ustunlar
    cursor.execute("PRAGMA table_info(insta_posts_queue)")
    cols = [row["name"] for row in cursor.fetchall()]
    if "likes_count" not in cols:
        try: cursor.execute("ALTER TABLE insta_posts_queue ADD COLUMN likes_count INTEGER DEFAULT 0")
        except Exception: pass
    if "telegram_msg_id" not in cols:
        try: cursor.execute("ALTER TABLE insta_posts_queue ADD COLUMN telegram_msg_id INTEGER")
        except Exception: pass
    if "youtube_uploaded" not in cols:
        try: cursor.execute("ALTER TABLE insta_posts_queue ADD COLUMN youtube_uploaded INTEGER DEFAULT 0")
        except Exception: pass
    if "youtube_url" not in cols:
        try: cursor.execute("ALTER TABLE insta_posts_queue ADD COLUMN youtube_url TEXT")
        except Exception: pass
    if "youtube_uploaded_at" not in cols:
        try: cursor.execute("ALTER TABLE insta_posts_queue ADD COLUMN youtube_uploaded_at TEXT")
        except Exception: pass
    
    # 2. Layklar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insta_post_likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(post_id, user_id)
    )
    """)
    
    # 3. Sozlamalar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insta_settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    
    defaults = {
        "bot_token": DEFAULT_BOT_TOKEN,
        "target_chat_id": DEFAULT_TARGET_CHAT_ID,
        "insta_username": DEFAULT_INSTA_USERNAME,
        "auto_schedule_enabled": "1",
        "interval_minutes": "60",
        "last_post_time": "",
        "is_scanning": "0",
        "last_scan_time": "",
        "last_scan_count": "74",
        "night_mode_enabled": "1",
        "night_mode_start": "00:00",
        "night_mode_end": "07:00",
        # DIQQAT: Bu sessionid ESKIRGAN bo'lishi mumkin!
        # Yangilash uchun: brauzerda instagram.com ga kiring -> DevTools -> Application ->
        # Cookies -> instagram.com -> "sessionid" qiymatini shu yerga qo'ying.
        "insta_session_id": "61835138797%3AzWTgfIiOPBUkVE%3A13%3AAYiLE6mFSW2M7qmjat3MGNfyqvWPPoaneRmr-c__Gg",
        "insta_ds_user_id": "",
        "insta_csrftoken": "",
        "youtube_token_json": "",
        "youtube_auto_upload": "1",
        "youtube_schedule_enabled": "1",
        "youtube_schedule_times": "09:00,12:00,15:00,18:30,21:00",
        "youtube_last_posted_slot": ""
    }
    
    for k, v in defaults.items():
        cursor.execute("INSERT OR IGNORE INTO insta_settings (key, value) VALUES (?, ?)", (k, v))
        
    # Eski yuklangan postlarni tozalash (DTHudhLiEJT gacha bo'lgan)
    cursor.execute("""
    DELETE FROM insta_posts_queue 
    WHERE shortcode IN (
        'DRjbVIVCKY4', 'DRodxW9iPAr', 'DRtp7ONiAtK', 'DRy5jtWiId5', 'DR6hnfsCFyT',
        'DSE-3rGiKBm', 'DSJ8o_MCK6L', 'DSPNK1QiLHZ', 'DSUShSniPWi', 'DSZZK5-iGaQ',
        'DSem0aaiO5s', 'DSjq4LCCB4l', 'DSo84-gCD7E', 'DSuH3e7iD4N', 'DSzWzXdiB5t',
        'DS4nL3iiIdL', 'DTB-Fz7iJ4A', 'DTHudhLiEJT', 'DTKl4neiIGi', 'DTKl2WlCFbP',
        'DTKlzm8CJ5N', 'Db0U9ivIcwC'
    ) OR media_type = 'post'
    """)
    
    # 4. Agar navbat kam bo'lsa, barcha videolarni eskisidan yangisiga qarab qayta joylash
    cursor.execute("SELECT COUNT(*) as cnt FROM insta_posts_queue")
    cnt_val = cursor.fetchone()["cnt"]
    if cnt_val < 1:
        for p in DEFAULT_SEEDED_POSTS:
            sc = p.get("shortcode") or ""
            p_url = p.get("post_url") or p.get("url") or f"https://www.instagram.com/reel/{sc}"
            m_type = p.get("media_type") or "reel"
            cap = p.get("caption") or ""
            m_url = p.get("media_url") or ""
            p_date = p.get("post_date") or ""
            cursor.execute("""
            INSERT OR IGNORE INTO insta_posts_queue (shortcode, post_url, media_type, caption, media_url, post_date, status)
            VALUES (?, ?, ?, ?, ?, ?, 'PENDING')
            """, (sc, p_url, m_type, cap, m_url, p_date))
    else:
        for p in DEFAULT_SEEDED_POSTS:
            sc = p.get("shortcode") or ""
            p_url = p.get("post_url") or p.get("url") or f"https://www.instagram.com/reel/{sc}"
            cap = p.get("caption") or ""
            p_date = p.get("post_date") or ""
            m_url = p.get("media_url") or ""
            cursor.execute("""
            UPDATE insta_posts_queue 
            SET caption = CASE WHEN caption IS NULL OR caption = '' THEN ? ELSE caption END,
                post_date = CASE WHEN post_date IS NULL OR post_date = '' THEN ? ELSE post_date END,
                media_type = 'reel',
                post_url = CASE WHEN post_url IS NULL OR post_url = '' THEN ? ELSE post_url END,
                media_url = CASE WHEN media_url IS NULL OR media_url = '' THEN ? ELSE media_url END
            WHERE shortcode = ?
            """, (cap, p_date, p_url, m_url, sc))

    # 5. Supabase Cloud holatidan allaqachon yuborilgan, qo'shilgan va o'chirilganlarni sinxronlash
    try:
        cloud_state = load_insta_cloud_state()
        
        # 5.1 O'chirilgan postlarni tozalash
        deleted_list = cloud_state.get("deleted_shortcodes", [])
        if deleted_list:
            for dsc in deleted_list:
                cursor.execute("DELETE FROM insta_posts_queue WHERE shortcode = ?", (dsc,))
                
        # 5.2 Foydalanuvchi qo'shgan maxsus postlarni tiklash
        for cp in cloud_state.get("custom_posts", []):
            sc = cp.get("shortcode")
            if sc and sc not in deleted_list:
                cursor.execute("SELECT id FROM insta_posts_queue WHERE shortcode = ?", (sc,))
                if not cursor.fetchone():
                    cursor.execute("""
                    INSERT INTO insta_posts_queue (shortcode, post_url, media_type, caption, media_url, post_date, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'PENDING')
                    """, (sc, cp.get("post_url", f"https://www.instagram.com/reel/{sc}"), cp.get("media_type", "reel"), cp.get("caption", ""), cp.get("media_url", ""), cp.get("post_date", "")))

        # 5.3 Yuborilganlar holati
        sent_dict = cloud_state.get("sent_shortcodes", {})
        for sc, sent_date in sent_dict.items():
            cursor.execute("UPDATE insta_posts_queue SET status = 'SENT', sent_at = ? WHERE shortcode = ?", (sent_date, sc))
            
        # 5.4 YouTube yuklanganlar holati
        yt_dict = cloud_state.get("yt_uploaded_shortcodes", {})
        for sc, yt_url in yt_dict.items():
            cursor.execute("UPDATE insta_posts_queue SET youtube_uploaded = 1, youtube_url = ? WHERE shortcode = ?", (yt_url, sc))

        # 5.6 Sozlamalar va slot holatlarini sinxronlash
        cloud_settings = cloud_state.get("settings", {})
        for sk, sv in cloud_settings.items():
            if sv is not None:
                cursor.execute("INSERT OR REPLACE INTO insta_settings (key, value) VALUES (?, ?)", (sk, str(sv)))
    except Exception as _ce:
        print(f"[Init Cloud Sync Err]: {_ce}")

    conn.commit()
    conn.close()
    _INIT_INSTA_DONE = True
    _LAST_CLOUD_SYNC_TS = time.time()


def get_setting(key, default=""):
    """Sozlamani olish (Supabase Cloud + Local SQLite)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM insta_settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        if row and row["value"] is not None:
            return row["value"]
    except Exception:
        pass
        
    try:
        cloud_state = load_insta_cloud_state()
        cloud_settings = cloud_state.get("settings", {})
        if key in cloud_settings and cloud_settings[key] is not None:
            return cloud_settings[key]
    except Exception:
        pass
        
    return default


def set_setting(key, value):
    """Sozlamani yangilash (Local SQLite + Supabase Cloud, rekursiyasiz)"""
    val_str = str(value) if value is not None else ""

    # 1. Local SQLite ga yozish
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO insta_settings (key, value) VALUES (?, ?)", (key, val_str))
        conn.commit()
        conn.close()
    except Exception as _db_e:
        print(f"[Set Setting DB Error]: {_db_e}")

    # 2. Supabase cloud_state.settings ga to'g'ridan-to'g'ri yuborish
    # save_insta_cloud_state CHAQIRILMAYDI — rekursiyadan himoya
    try:
        supa_url, headers = _get_supabase_headers()
        if supa_url and headers:
            # Avval mavjud holatni olish
            r = requests.get(
                f"{supa_url}/rest/v1/atlas_settings?key=eq.insta_poster_state",
                headers=headers, timeout=4
            )
            if r.status_code == 200 and r.json():
                try:
                    cloud_state = json.loads(r.json()[0].get("value") or "{}")
                except Exception:
                    cloud_state = {}
            else:
                cloud_state = {}

            if "settings" not in cloud_state:
                cloud_state["settings"] = {}
            cloud_state["settings"][key] = val_str

            # Yangilangan holatni saqlash
            payload = {
                "key": "insta_poster_state",
                "value": json.dumps(cloud_state),
                "category": "instagram",
                "description": "Instagram & YouTube AutoPoster persistent cloud state"
            }
            requests.post(
                f"{supa_url}/rest/v1/atlas_settings",
                headers=headers, json=payload, timeout=4
            )
        return True
    except Exception as e:
        print(f"[Set Setting Cloud Error]: {e}")
        return False


def set_settings_batch(updates: dict):
    """Bir vaqtda bir nechta sozlamalarni yangilash (1 ta Supabase so'rovi bilan, tez va rekursiyasiz)"""
    if not updates:
        return True

    # 1. Local SQLite - hammasi birga
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for k, v in updates.items():
            val_str = str(v) if v is not None else ""
            cursor.execute("INSERT OR REPLACE INTO insta_settings (key, value) VALUES (?, ?)", (k, val_str))
        conn.commit()
        conn.close()
    except Exception as _db_e:
        print(f"[Batch Set Setting DB Error]: {_db_e}")

    # 2. Supabase - faqat 1 ta GET + 1 ta POST (ko'p set_setting emas!)
    try:
        supa_url, headers = _get_supabase_headers()
        if supa_url and headers:
            r = requests.get(
                f"{supa_url}/rest/v1/atlas_settings?key=eq.insta_poster_state",
                headers=headers, timeout=4
            )
            if r.status_code == 200 and r.json():
                try:
                    cloud_state = json.loads(r.json()[0].get("value") or "{}")
                except Exception:
                    cloud_state = {}
            else:
                cloud_state = {}

            if "settings" not in cloud_state:
                cloud_state["settings"] = {}
            for k, v in updates.items():
                cloud_state["settings"][k] = str(v) if v is not None else ""

            payload = {
                "key": "insta_poster_state",
                "value": json.dumps(cloud_state),
                "category": "instagram",
                "description": "Instagram & YouTube AutoPoster persistent cloud state"
            }
            requests.post(
                f"{supa_url}/rest/v1/atlas_settings",
                headers=headers, json=payload, timeout=4
            )
        return True
    except Exception as e:
        print(f"[Batch Set Setting Cloud Error]: {e}")
        return False

def get_all_settings():
    """Barcha sozlamalarni lug'at ko'rinishida olish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM insta_settings")
        rows = cursor.fetchall()
        conn.close()
        res = {r["key"]: r["value"] for r in rows}
        
        # Bulut sozlamalari bilan birlashtirish
        try:
            cloud_state = load_insta_cloud_state()
            for ck, cv in cloud_state.get("settings", {}).items():
                if ck not in res:
                    res[ck] = cv
        except Exception:
            pass
        return res
    except Exception as e:
        print(f"[Insta Get All Settings Error]: {e}")
        return {}

# ------------------------------------------------------------
# 2. Like Boshqaruvi va Inline Tugmalar
# ------------------------------------------------------------

def get_post_inline_keyboard(post_id, post_url, likes_count=0):
    """Post tagidagi Like va Instagramga o'tish inline tugmalari (Alohida-alohida qatorlarda)"""
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn_link = telebot.types.InlineKeyboardButton("🔗 Instagramda ko‘rish", url=post_url)
    btn_like = telebot.types.InlineKeyboardButton(f"❤️ {likes_count}", callback_data=f"insta_like_{post_id}")
    markup.add(btn_link)
    markup.add(btn_like)
    return markup


def toggle_post_like(post_id, user_id):
    """Foydalanuvchi like bosganda layklar sonini yangilash (Toggle)"""
    init_insta_tables()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM insta_post_likes WHERE post_id = ? AND user_id = ?", (post_id, user_id))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute("DELETE FROM insta_post_likes WHERE post_id = ? AND user_id = ?", (post_id, user_id))
        is_liked = False
    else:
        cursor.execute("INSERT OR IGNORE INTO insta_post_likes (post_id, user_id) VALUES (?, ?)", (post_id, user_id))
        is_liked = True
        
    cursor.execute("SELECT COUNT(*) as cnt FROM insta_post_likes WHERE post_id = ?", (post_id,))
    total_likes = cursor.fetchone()["cnt"]
    
    cursor.execute("UPDATE insta_posts_queue SET likes_count = ? WHERE id = ?", (total_likes, post_id))
    conn.commit()
    
    cursor.execute("SELECT post_url, telegram_msg_id FROM insta_posts_queue WHERE id = ?", (post_id,))
    post_data = cursor.fetchone()
    conn.close()
    
    return {
        "is_liked": is_liked,
        "likes_count": total_likes,
        "post_url": post_data["post_url"] if post_data else "https://instagram.com",
        "telegram_msg_id": post_data["telegram_msg_id"] if post_data else None
    }


def clean_caption_text(raw_caption, username=None):
    """Instagram caption matnini tozalash (username prefiksi, izohlar va ortiqcha matnlarni olib tashlash)"""
    if not raw_caption:
        return ""
    text = str(raw_caption).strip()
    
    usernames = ["shahrisabz_t_t_uz", "shahrisabz.t.t.uz", "shahrisabz_tt_uz"]
    if username:
        usernames.insert(0, str(username).lstrip("@").strip())
        
    for u in set(usernames):
        if not u:
            continue
        pattern = rf"^(?:@)?{re.escape(u)}[:\s\-\n\r]*"
        text = re.sub(pattern, "", text, flags=re.IGNORECASE).strip()
        
    patterns = [
        r'View all \d+ comments.*',
        r'View \d+ more comments.*',
        r'View more on Instagram.*',
        r'Add a comment\.\.\..*',
        r'Log in to like or comment.*',
        r'\d+\s+likes\s*$',
        r'View profile.*',
    ]
    for p in patterns:
        text = re.sub(p, '', text, flags=re.IGNORECASE | re.DOTALL).strip()
        
    return text.strip()

# ------------------------------------------------------------
# 3. YouTube Shorts Jadval Boshqaruvi
# ------------------------------------------------------------

DEFAULT_YOUTUBE_SCHEDULE_TIMES = "09:00,12:00,15:00,18:30,21:00"

def get_youtube_schedule_times():
    """Sozlangan YouTube vaqtlarini ro'yxat ko'rinishida olish"""
    raw = get_setting("youtube_schedule_times", DEFAULT_YOUTUBE_SCHEDULE_TIMES)
    times = [t.strip() for t in raw.split(",") if t.strip()]
    # Normalize times to HH:MM format
    normalized = []
    for t in times:
        m = re.match(r"^([01]?\d|2[0-3]):([0-5]\d)$", t)
        if m:
            normalized.append(f"{int(m.group(1)):02d}:{int(m.group(2)):02d}")
    return sorted(list(set(normalized)))


def add_youtube_schedule_time(time_str):
    """Yangi vaqt qo'shish (Format: HH:MM)"""
    time_str = str(time_str).strip()
    match = re.match(r"^([01]?\d|2[0-3]):([0-5]\d)$", time_str)
    if not match:
        return False, "Noto'g'ri format! Vaqtni '14:30' yoki '20:00' formatida kiriting."
    
    hh, mm = match.groups()
    formatted = f"{int(hh):02d}:{int(mm):02d}"
    
    current_times = get_youtube_schedule_times()
    if formatted in current_times:
        return False, f"Ushbu vaqt ({formatted}) allaqachon jadvalda mavjud!"
        
    current_times.append(formatted)
    current_times = sorted(list(set(current_times)))
    set_setting("youtube_schedule_times", ",".join(current_times))
    return True, formatted


def remove_youtube_schedule_time(time_str):
    """Vaqtni jadvaldan o'chirish"""
    current_times = get_youtube_schedule_times()
    time_str = str(time_str).strip()
    
    m = re.match(r"^([01]?\d|2[0-3]):([0-5]\d)$", time_str)
    formatted = f"{int(m.group(1)):02d}:{int(m.group(2)):02d}" if m else time_str
    
    if formatted in current_times:
        current_times.remove(formatted)
        set_setting("youtube_schedule_times", ",".join(current_times))
        return True
    return False


def reset_youtube_schedule_times():
    """Standart 5 ta YouTube vaqtlariga qaytarish (09:00, 12:00, 15:00, 18:30, 21:00)"""
    set_setting("youtube_schedule_times", DEFAULT_YOUTUBE_SCHEDULE_TIMES)
    return ["09:00", "12:00", "15:00", "18:30", "21:00"]

# ------------------------------------------------------------
# 4. Instagram Profile Scraper (Playwright)
# ------------------------------------------------------------

async def _scrape_instagram_profile_async(username, max_posts=150):
    """Playwright orqali profil postlarini skanerlash"""
    try:
        from playwright.async_api import async_playwright
    except ImportError as e:
        raise ImportError("Playwright kutubxonasi o'rnatilmagan.") from e
    
    collected_links = []
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 900}
            )
            page = await context.new_page()
            
            url = f"https://www.instagram.com/{username}/"
            print(f"[Insta Scraper]: Sahifa ochilmoqda: {url}")
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(3)
            
            seen_codes = set()
            scroll_attempts = 0
            max_scrolls = 25
            stagnant_count = 0
            
            while scroll_attempts < max_scrolls and len(seen_codes) < max_posts:
                links = await page.evaluate('''() => {
                    const anchors = Array.from(document.querySelectorAll('a'));
                    return anchors.map(a => a.href).filter(h => h.includes('/reel/'));
                }''')
                
                initial_len = len(seen_codes)
                for l in links:
                    parts = l.split('?')[0].rstrip('/')
                    code = parts.split('/')[-1]
                    if code and code not in seen_codes:
                        seen_codes.add(code)
                        collected_links.append({
                            "shortcode": code,
                            "url": parts,
                            "is_reel": True
                        })
                        
                if len(seen_codes) == initial_len:
                    stagnant_count += 1
                    if stagnant_count >= 4:
                        break
                else:
                    stagnant_count = 0
                    
                await page.evaluate("window.scrollBy(0, 1600)")
                await asyncio.sleep(2)
                scroll_attempts += 1
                
            await browser.close()
    except Exception as be:
        print(f"[Playwright Launch/Scrape Error]: {be}")
        raise be
        
    return collected_links


def scan_and_enqueue_posts(username=None, max_posts=150):
    """Instagram profilini skanerlab, barcha postlarni eskisidan yangisiga tartibda bazaga qo'shish"""
    init_insta_tables()
    if not username:
        username = get_setting("insta_username", DEFAULT_INSTA_USERNAME)
        
    set_setting("is_scanning", "1")
    set_setting("last_scan_error", "")
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        links = loop.run_until_complete(_scrape_instagram_profile_async(username, max_posts=max_posts))
        loop.close()
        
        links_chronological = list(reversed(links))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        added_count = 0
        for item in links_chronological:
            try:
                cursor.execute("""
                INSERT OR IGNORE INTO insta_posts_queue (shortcode, post_url, media_type, status)
                VALUES (?, ?, ?, 'PENDING')
                """, (item["shortcode"], item["url"], "reel" if item["is_reel"] else "post"))
                if cursor.rowcount > 0:
                    added_count += 1
            except Exception as _e:
                print(f"[Enqueue Error]: {_e}")
                
        conn.commit()
        conn.close()
        
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        set_setting("last_scan_time", now_str)
        set_setting("last_scan_count", str(len(links)))
        set_setting("is_scanning", "0")
        
        return {
            "success": True,
            "total_found": len(links),
            "new_added": added_count,
            "username": username
        }
    except Exception as e:
        err_msg = str(e)
        set_setting("is_scanning", "0")
        set_setting("last_scan_error", err_msg)
        print(f"[Scan Instagram Error]: {e}")
        return {
            "success": False,
            "error": err_msg
        }


def add_posts_by_urls(urls_text):
    """Foydalanuvchi kiritgan Instagram post/reel havolalarini tahlil qilib, matni (caption) bilan navbatga qo'shish"""
    init_insta_tables()
    if not urls_text:
        return {"success": False, "error": "Hech qanday havola kiritilmadi."}
        
    # Extract shortcodes cleanly (ignoring query parameters like ?igsh=...)
    clean_pattern = r'instagram\.com/(?:reel|p|tv)/([A-Za-z0-9_-]+)'
    raw_lines = urls_text.splitlines()
    extracted_shortcodes = []
    
    for line in raw_lines:
        line_str = line.strip()
        if not line_str:
            continue
        m = re.findall(clean_pattern, line_str)
        if m:
            for code in m:
                if code and code not in extracted_shortcodes:
                    extracted_shortcodes.append(code)
        else:
            token = line_str.rstrip('/').split('/')[-1].split('?')[0].strip()
            if len(token) >= 9 and len(token) <= 15 and re.match(r'^[A-Za-z0-9_-]+$', token):
                if token not in extracted_shortcodes:
                    extracted_shortcodes.append(token)
                    
    if not extracted_shortcodes:
        return {"success": False, "error": "Instagram havolalari aniqlanmadi. Format: https://www.instagram.com/reel/DTNEIiLCBPn/"}
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    added_count = 0
    existing_count = 0
    new_custom_posts = []
    now_str = get_uzb_now().strftime("%Y-%m-%d %H:%M:%S")
    
    for sc in extracted_shortcodes:
        cursor.execute("SELECT id FROM insta_posts_queue WHERE shortcode = ?", (sc,))
        if cursor.fetchone():
            existing_count += 1
            continue
            
        post_url = f"https://www.instagram.com/reel/{sc}"
        caption = ""
        media_url = ""
        
        # Sarlavha va rasmni avtomatik tortib olish
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            content = loop.run_until_complete(_fetch_post_content_async(post_url))
            loop.close()
            if content:
                caption = content.get("caption") or ""
                media_url = content.get("img_url") or content.get("video_url") or ""
        except Exception as fe:
            print(f"[Fetch info for {sc}]: {fe}")
            
        cursor.execute("""
        INSERT INTO insta_posts_queue (shortcode, post_url, media_type, caption, media_url, post_date, status)
        VALUES (?, ?, 'reel', ?, ?, ?, 'PENDING')
        """, (sc, post_url, caption, media_url, now_str))
        added_count += 1
        
        new_custom_posts.append({
            "shortcode": sc,
            "post_url": post_url,
            "media_type": "reel",
            "caption": caption,
            "media_url": media_url,
            "post_date": now_str
        })
        
    conn.commit()
    conn.close()
    
    # Supabase Cloud holatida saqlash
    try:
        if new_custom_posts:
            cloud_state = load_insta_cloud_state()
            cust = cloud_state.get("custom_posts", [])
            for ncp in new_custom_posts:
                if not any(c.get("shortcode") == ncp["shortcode"] for c in cust):
                    cust.append(ncp)
            del_list = cloud_state.get("deleted_shortcodes", [])
            del_list = [d for d in del_list if not any(ncp["shortcode"] == d for ncp in new_custom_posts)]
            cloud_state["custom_posts"] = cust
            cloud_state["deleted_shortcodes"] = del_list
            save_insta_cloud_state(cloud_state)
    except Exception as _ce:
        print(f"[Save Custom Posts Cloud Err]: {_ce}")
        
    return {
        "success": True,
        "total_parsed": len(extracted_shortcodes),
        "new_added": added_count,
        "existing_skipped": existing_count,
        "message": f"{added_count} ta yangi post matni bilan navbatga qo'shildi! ({existing_count} ta avvaldan bor)"
    }


def scan_in_background(username=None, callback_notify=None):
    """Fon rejimida skanerlash"""
    def _task():
        res = scan_and_enqueue_posts(username)
        if callback_notify:
            try:
                callback_notify(res)
            except Exception as e:
                print(f"[Scan Callback Error]: {e}")
                
    th = threading.Thread(target=_task, daemon=True)
    th.start()
    return th

# ------------------------------------------------------------
# 5. HD Video yuklash va Telegram / YouTube ga yuborish
# ------------------------------------------------------------

_INSTA_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"


def _build_insta_cookiefile():
    """
    Instagram sessiya cookie'laridan Netscape formatidagi vaqtinchalik cookie fayl yaratadi.
    yt-dlp shu faylni ishlatib login qilingandek so'rov yuboradi — bu ko'pgina
    "video yuklab bo'lmadi / login required / rate-limited" xatolarini hal qiladi.

    Sozlamalarda (insta_settings) quyidagilarni to'ldiring:
      - insta_session_id  (majburiy)
      - insta_ds_user_id  (ixtiyoriy, lekin tavsiya etiladi)
      - insta_csrftoken   (ixtiyoriy, lekin tavsiya etiladi)
    """
    session_id = (get_setting("insta_session_id", "") or "").strip()
    if not session_id:
        return None

    ds_user_id = (get_setting("insta_ds_user_id", "") or "").strip()
    csrftoken = (get_setting("insta_csrftoken", "") or "").strip()

    temp_dir = tempfile.gettempdir()
    cookie_path = os.path.join(temp_dir, f"insta_cookies_{int(time.time()*1000)}_{os.getpid()}.txt")

    lines = ["# Netscape HTTP Cookie File"]
    expiry = "2147483647"  # 2038 yilgacha amal qiladi

    def _cookie_line(name, value):
        # domain, include_subdomains, path, secure, expiry, name, value
        return f".instagram.com\tTRUE\t/\tTRUE\t{expiry}\t{name}\t{value}"

    lines.append(_cookie_line("sessionid", session_id))
    if ds_user_id:
        lines.append(_cookie_line("ds_user_id", ds_user_id))
    if csrftoken:
        lines.append(_cookie_line("csrftoken", csrftoken))

    try:
        with open(cookie_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return cookie_path
    except Exception as e:
        print(f"[Cookie File Yaratish Xatosi]: {e}")
        return None


def _download_hd_video_ytdlp(post_url, use_cookies=True):
    """
    yt-dlp yordamida videoni to'g'ridan-to'g'ri yuklab olish.
    Avval cookie bilan (agar mavjud bo'lsa), muvaffaqiyatsiz bo'lsa cookie'siz qayta urinadi.
    """
    cookie_path = None
    try:
        import yt_dlp

        temp_dir = tempfile.gettempdir()
        out_filename = os.path.join(temp_dir, f"insta_hd_{int(time.time()*1000)}_{os.getpid()}.mp4")

        ydl_opts = {
            "outtmpl": out_filename,
            "format": "best[ext=mp4]/best",
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": 30,
            "retries": 3,
            "http_headers": {
                "User-Agent": _INSTA_UA,
                "Accept-Language": "en-US,en;q=0.9",
            },
        }

        if use_cookies:
            cookie_path = _build_insta_cookiefile()
            if cookie_path:
                ydl_opts["cookiefile"] = cookie_path
            else:
                print("[yt-dlp]: insta_session_id topilmadi — cookie'siz urinilmoqda (login talab qilinishi mumkin).")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([post_url])

        if os.path.exists(out_filename) and os.path.getsize(out_filename) > 10000:
            return out_filename

        base_prefix = out_filename.replace(".mp4", "")
        for ext in [".mp4", ".mkv", ".webm"]:
            cand = base_prefix + ext
            if os.path.exists(cand) and os.path.getsize(cand) > 10000:
                return cand

        print(f"[yt-dlp]: Video yuklandi deb hisoblandi, lekin fayl topilmadi yoki juda kichik: {post_url}")

    except Exception as e:
        print(f"[yt-dlp Python Module Error] ({post_url}): {e}")
        print(traceback.format_exc())

        # Agar cookie bilan urinish muvaffaqiyatsiz bo'lsa va biz hali cookie'siz urinmagan bo'lsak,
        # cookie'siz (ba'zi hollarda cookie eskirgan/noto'g'ri bo'lsa bu yordam beradi) qayta urinib ko'ramiz.
        if use_cookies:
            print("[yt-dlp]: Cookie bilan urinish muvaffaqiyatsiz. Cookie'siz qayta urinib ko'rilmoqda...")
            if cookie_path and os.path.exists(cookie_path):
                try:
                    os.remove(cookie_path)
                except Exception:
                    pass
            return _download_hd_video_ytdlp(post_url, use_cookies=False)

    finally:
        if cookie_path and os.path.exists(cookie_path):
            try:
                os.remove(cookie_path)
            except Exception:
                pass

    return None


async def _fetch_post_content_async(post_url):
    """Postning to'liq ma'lumotlarini olish (yt-dlp orqali tezkor va xavfsiz, keyin Playwright fallback)"""
    cookie_path = None
    try:
        import yt_dlp
        cookie_path = _build_insta_cookiefile()
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "socket_timeout": 15,
            "http_headers": {"User-Agent": _INSTA_UA},
        }
        if cookie_path:
            ydl_opts["cookiefile"] = cookie_path

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(post_url, download=False)
            if info:
                desc = info.get("description") or info.get("title") or ""
                v_url = info.get("url")
                t_url = info.get("thumbnail")
                return {
                    "caption": desc,
                    "video_url": v_url,
                    "img_url": t_url,
                    "all_imgs": [t_url] if t_url else []
                }
    except Exception as yte:
        print(f"[yt-dlp info error] ({post_url}): {yte}")
    finally:
        if cookie_path and os.path.exists(cookie_path):
            try:
                os.remove(cookie_path)
            except Exception:
                pass

    try:
        from playwright.async_api import async_playwright
        parts = post_url.rstrip('/').split('/')
        code = parts[-1]
        is_reel = "/reel/" in post_url
        embed_url = f"https://www.instagram.com/{'reel' if is_reel else 'p'}/{code}/embed/captioned/"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=_INSTA_UA
            )
            page = await context.new_page()
            await page.goto(embed_url, wait_until="domcontentloaded", timeout=15000)
            await asyncio.sleep(1)
            
            data = await page.evaluate('''() => {
                const captionEl = document.querySelector('.Caption') || document.querySelector('.CaptionComments');
                let cap = captionEl ? captionEl.innerText : "";
                const videoEl = document.querySelector('video');
                const imgEl = document.querySelector('.EmbeddedMediaImage') || document.querySelector('img.EmbeddedMedia');
                let allImgs = Array.from(document.querySelectorAll('img')).map(i => i.src).filter(s => s && (s.includes('cdninstagram') || s.includes('fbcdn')));
                return {
                    caption: cap,
                    video_url: videoEl ? videoEl.src : null,
                    img_url: imgEl ? imgEl.src : (allImgs.length > 0 ? allImgs[0] : null),
                    all_imgs: allImgs
                };
            }''')
            await browser.close()
            return data
    except Exception as pe:
        print(f"[Playwright skipped] ({post_url}): {pe}")
        
    return {"caption": "", "video_url": None, "img_url": None, "all_imgs": []}


def post_next_queued_item(chat_id=None, bot_token=None):
    """Navbatdagi eng eski 1 ta postni olib Telegramga yuborish"""
    init_insta_tables()
    
    if not bot_token:
        bot_token = get_setting("bot_token", DEFAULT_BOT_TOKEN)
    if not chat_id:
        chat_id = get_setting("target_chat_id", DEFAULT_TARGET_CHAT_ID)
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT * FROM insta_posts_queue 
    WHERE status = 'PENDING' 
    ORDER BY id ASC 
    LIMIT 1
    """)
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return {
            "success": False,
            "empty": True,
            "message": "Navbatda yuborilmagan postlar qolmadi!"
        }
        
    post_id = row["id"]
    shortcode = row["shortcode"]
    post_url = row["post_url"]
    
    # ATOMIC CLAIM: Bir vaqtning o'zida ikkita jarayon bitta postni yuborib qo'ymasligi uchun darhol statusni 'PROCESSING' qilish
    now_claim_str = get_uzb_now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE insta_posts_queue SET status = 'PROCESSING', sent_at = ? WHERE id = ? AND status = 'PENDING'", (now_claim_str, post_id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return {"success": False, "message": "Post ayni vaqtda boshqa so'rov orqali yuborilmoqda."}
        
    # Local DB ga yozish (Supabase ga YUKLAMAYDI - mark_post_sent_in_cloud da yoziladi)
    try:
        _conn = get_db_connection()
        _conn.execute("INSERT OR REPLACE INTO insta_settings (key, value) VALUES (?, ?)", ("last_post_time", now_claim_str))
        _conn.commit()
        _conn.close()
    except Exception:
        pass
    
    bot = telebot.TeleBot(bot_token)
    
    try:
        username = get_setting("insta_username", DEFAULT_INSTA_USERNAME)
        
        raw_caption = row["caption"] or ""
        video_direct_url = None
        
        if not raw_caption:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            content = loop.run_until_complete(_fetch_post_content_async(post_url))
            loop.close()
            raw_caption = content.get("caption") or ""
            video_direct_url = content.get("video_url")
            
        clean_caption = clean_caption_text(raw_caption, username)
        
        if len(clean_caption) > 1000:
            telegram_caption = clean_caption[:997] + "..."
        else:
            telegram_caption = clean_caption
            
        inline_kb = get_post_inline_keyboard(post_id, post_url, likes_count=0)
        
        media_sent = False
        sent_msg = None
        
        # 1. HD Video yuklash (Reels/Video postlar uchun)
        if row["media_type"] in ("reel", "video") or "/reel/" in post_url:
            hd_video_path = _download_hd_video_ytdlp(post_url)
            if hd_video_path and os.path.exists(hd_video_path):
                try:
                    with open(hd_video_path, 'rb') as v_file:
                        sent_msg = bot.send_video(
                            chat_id,
                            v_file,
                            caption=telegram_caption,
                            parse_mode="HTML" if telegram_caption else None,
                            reply_markup=inline_kb,
                            supports_streaming=True
                        )
                    media_sent = True
                finally:
                    if os.path.exists(hd_video_path):
                        os.remove(hd_video_path)
                        
            if not media_sent and video_direct_url:
                v_res = requests.get(video_direct_url, timeout=40, headers={"User-Agent": _INSTA_UA})
                if v_res.status_code == 200:
                    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
                        f.write(v_res.content)
                        temp_v_path = f.name
                    try:
                        with open(temp_v_path, 'rb') as v_file:
                            sent_msg = bot.send_video(
                                chat_id,
                                v_file,
                                caption=telegram_caption,
                                parse_mode="HTML" if telegram_caption else None,
                                reply_markup=inline_kb,
                                supports_streaming=True
                            )
                        media_sent = True
                    finally:
                        if os.path.exists(temp_v_path):
                            os.remove(temp_v_path)
                            
        # 2. Rasm jo'natish (Statik rasm postlari uchun)
        if not media_sent and (row["media_url"] or row["img_url"] if "img_url" in row.keys() else row["media_url"]):
            img_url = row["media_url"]
            try:
                p_res = requests.get(img_url, timeout=30, headers={"User-Agent": _INSTA_UA})
                if p_res.status_code == 200:
                    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
                        f.write(p_res.content)
                        temp_p_path = f.name
                    try:
                        with open(temp_p_path, 'rb') as p_file:
                            sent_msg = bot.send_photo(
                                chat_id,
                                p_file,
                                caption=telegram_caption,
                                parse_mode="HTML" if telegram_caption else None,
                                reply_markup=inline_kb
                            )
                        media_sent = True
                    finally:
                        if os.path.exists(temp_p_path):
                            os.remove(temp_p_path)
            except Exception as _pe:
                print(f"[Photo Send Err]: {_pe}")
                
        # 3. Matnli xabar orqali jo'natish (oxirgi zaxira)
        if not media_sent:
            sent_msg = bot.send_message(
                chat_id,
                telegram_caption or f"📢 Instagram: {post_url}",
                reply_markup=inline_kb,
                parse_mode="HTML" if telegram_caption else None
            )
            media_sent = True
            
        now_str = get_uzb_now().strftime("%Y-%m-%d %H:%M:%S")
        msg_id_val = sent_msg.message_id if sent_msg else None
        cursor.execute("""
        UPDATE insta_posts_queue 
        SET status = 'SENT', sent_at = ?, caption = ?, error_msg = NULL, telegram_msg_id = ?
        WHERE id = ?
        """, (now_str, clean_caption, msg_id_val, post_id))
        conn.commit()
        
        mark_post_sent_in_cloud(shortcode, now_str)  # Bu last_post_time ni ham cloud ga yozadi
        conn.close()

        
        notify_admin_post_published("telegram", {
            "post_id": post_id,
            "shortcode": shortcode,
            "post_url": post_url,
            "caption": clean_caption,
            "msg_id": msg_id_val,
            "target_chat_id": chat_id
        })
        
        return {
            "success": True,
            "post_id": post_id,
            "shortcode": shortcode,
            "post_url": post_url,
            "caption": clean_caption[:80]
        }
        
    except Exception as e:
        err_msg = str(e)
        print(f"[Post Next Error] ({post_url}): {e}")
        print(traceback.format_exc())
        cursor.execute("""
        UPDATE insta_posts_queue 
        SET status = 'FAILED', error_msg = ?
        WHERE id = ?
        """, (err_msg, post_id))
        conn.commit()
        conn.close()
        return {
            "success": False,
            "post_id": post_id,
            "error": err_msg
        }


def post_next_youtube_video():
    """Navbatdagi eng eski 1 ta videoni olib YouTube Shorts ga yuklash"""
    init_insta_tables()
    from services.youtube_service import is_youtube_ready, upload_video_to_youtube
    
    if not is_youtube_ready():
        return {
            "success": False,
            "error": "YouTube avtorizatsiyasi mavjud emas! (youtube_token.json)"
        }
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Hali YouTubega yuklanmagan eng eski video yoki reelni topish
    cursor.execute("""
    SELECT * FROM insta_posts_queue 
    WHERE (media_type IN ('reel', 'video', 'unknown') OR post_url LIKE '%/reel/%')
      AND youtube_uploaded = 0
    ORDER BY id ASC 
    LIMIT 1
    """)
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return {
            "success": False,
            "empty": True,
            "message": "YouTubega yuklash uchun navbatda yangi videolar qolmadi!"
        }
        
    post_id = row["id"]
    shortcode = row["shortcode"]
    post_url = row["post_url"]
    
    username = get_setting("insta_username", DEFAULT_INSTA_USERNAME)
    
    try:
        # 1. Post matnini olish
        caption = row["caption"]
        if not caption:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            content = loop.run_until_complete(_fetch_post_content_async(post_url))
            loop.close()
            raw_caption = content.get("caption") or ""
            caption = clean_caption_text(raw_caption, username)
            
        # 2. HD Videoni yuklab olish
        vpath = _download_hd_video_ytdlp(post_url)
        if not vpath or not os.path.exists(vpath):
            err_text = f"Videoni yuklab bo'lmadi: {post_url}"
            cursor.execute("UPDATE insta_posts_queue SET error_msg = ? WHERE id = ?", (err_text, post_id))
            conn.commit()
            conn.close()
            return {
                "success": False,
                "error": err_text
            }
            
        # 3. YouTube Shorts ga yuklash
        yt_res = upload_video_to_youtube(
            vpath,
            caption=caption,
            post_url=post_url,
            privacy="public",
            is_shorts=True
        )
        
        if os.path.exists(vpath):
            os.remove(vpath)
            
        if yt_res.get("success"):
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
            UPDATE insta_posts_queue 
            SET youtube_uploaded = 1, youtube_url = ?, youtube_uploaded_at = ?, caption = ?
            WHERE id = ?
            """, (yt_res.get("url"), now_str, caption, post_id))
            conn.commit()
            conn.close()
            mark_youtube_uploaded_in_cloud(shortcode, yt_res.get("url") or "")
            
            notify_admin_post_published("youtube", {
                "post_id": post_id,
                "shortcode": shortcode,
                "post_url": post_url,
                "url": yt_res.get("url"),
                "title": yt_res.get("title")
            })
            
            return {
                "success": True,
                "post_id": post_id,
                "shortcode": shortcode,
                "url": yt_res.get("url"),
                "title": yt_res.get("title")
            }
        else:
            cursor.execute("UPDATE insta_posts_queue SET error_msg = ? WHERE id = ?", (yt_res.get("error", ""), post_id))
            conn.commit()
            conn.close()
            return {
                "success": False,
                "error": yt_res.get("error")
            }
    except Exception as e:
        print(f"[YouTube Upload Queue Error] ({post_url}): {e}")
        print(traceback.format_exc())
        try:
            cursor.execute("UPDATE insta_posts_queue SET error_msg = ? WHERE id = ?", (str(e), post_id))
            conn.commit()
        except Exception:
            pass
        conn.close()
        return {
            "success": False,
            "error": str(e)
        }


def post_single_youtube_item(post_id):
    """Aniq tanlangan bitta videoni YouTube Shorts ga yuklash"""
    init_insta_tables()
    from services.youtube_service import is_youtube_ready, upload_video_to_youtube
    
    if not is_youtube_ready():
        return {
            "success": False,
            "error": "YouTube avtorizatsiyasi mavjud emas! (youtube_token.json)"
        }
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM insta_posts_queue WHERE id = ?", (post_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return {"success": False, "error": f"Post topilmadi (ID: {post_id})"}
        
    shortcode = row["shortcode"]
    post_url = row["post_url"]
    
    username = get_setting("insta_username", DEFAULT_INSTA_USERNAME)
    
    try:
        # 1. Post matnini olish
        caption = row["caption"] or ""
        if not caption:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            content = loop.run_until_complete(_fetch_post_content_async(post_url))
            loop.close()
            raw_caption = content.get("caption") or ""
            caption = clean_caption_text(raw_caption, username)
            
        # 2. HD Videoni yuklab olish
        vpath = _download_hd_video_ytdlp(post_url)
        if not vpath or not os.path.exists(vpath):
            err_text = f"Videoni yuklab bo'lmadi: {post_url}"
            cursor.execute("UPDATE insta_posts_queue SET error_msg = ? WHERE id = ?", (err_text, post_id))
            conn.commit()
            conn.close()
            return {
                "success": False,
                "error": err_text
            }
            
        # 3. YouTube Shorts ga yuklash
        yt_res = upload_video_to_youtube(
            vpath,
            caption=caption,
            post_url=post_url,
            privacy="public",
            is_shorts=True
        )
        
        if os.path.exists(vpath):
            os.remove(vpath)
            
        if yt_res.get("success"):
            now_str = get_uzb_now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
            UPDATE insta_posts_queue 
            SET youtube_uploaded = 1, youtube_url = ?, youtube_uploaded_at = ?, caption = ?
            WHERE id = ?
            """, (yt_res.get("url"), now_str, caption, post_id))
            conn.commit()
            conn.close()
            mark_youtube_uploaded_in_cloud(shortcode, yt_res.get("url") or "")
            
            notify_admin_post_published("youtube", {
                "post_id": post_id,
                "shortcode": shortcode,
                "post_url": post_url,
                "url": yt_res.get("url"),
                "title": yt_res.get("title")
            })
            
            return {
                "success": True,
                "post_id": post_id,
                "shortcode": shortcode,
                "url": yt_res.get("url"),
                "title": yt_res.get("title")
            }
        else:
            cursor.execute("UPDATE insta_posts_queue SET error_msg = ? WHERE id = ?", (yt_res.get("error", ""), post_id))
            conn.commit()
            conn.close()
            return {
                "success": False,
                "error": yt_res.get("error")
            }
    except Exception as e:
        print(f"[YouTube Upload Single Error] ({post_url}): {e}")
        print(traceback.format_exc())
        try:
            cursor.execute("UPDATE insta_posts_queue SET error_msg = ? WHERE id = ?", (str(e), post_id))
            conn.commit()
        except Exception:
            pass
        conn.close()
        return {
            "success": False,
            "error": str(e)
        }


# ------------------------------------------------------------
# 6. Statistics & Queue Control
# ------------------------------------------------------------

def get_queue_stats():
    """Navbat holati va hisoboti"""
    init_insta_tables()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM insta_posts_queue")
    total = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) as pending FROM insta_posts_queue WHERE status = 'PENDING'")
    pending = cursor.fetchone()["pending"]
    
    cursor.execute("SELECT COUNT(*) as sent FROM insta_posts_queue WHERE status = 'SENT'")
    sent = cursor.fetchone()["sent"]
    
    cursor.execute("SELECT COUNT(*) as failed FROM insta_posts_queue WHERE status = 'FAILED'")
    failed = cursor.fetchone()["failed"]
    
    cursor.execute("SELECT COUNT(*) as yt_uploaded FROM insta_posts_queue WHERE youtube_uploaded = 1")
    yt_uploaded = cursor.fetchone()["yt_uploaded"]
    
    cursor.execute("SELECT * FROM insta_posts_queue WHERE status = 'PENDING' ORDER BY id ASC LIMIT 1")
    next_post = cursor.fetchone()
    
    cursor.execute("SELECT * FROM insta_posts_queue WHERE status = 'SENT' ORDER BY sent_at DESC LIMIT 1")
    last_sent = cursor.fetchone()
    
    conn.close()
    settings = get_all_settings()
    
    next_post_dict = dict(next_post) if next_post else None
    last_sent_dict = dict(last_sent) if last_sent else None
    
    # Calculate next scheduled post time and status
    interval_min = int(settings.get("interval_minutes") or 60)
    last_post_str = settings.get("last_post_time", "")
    
    next_time_str = "Hozir (Navbatdagi siklda)"
    is_night_now = False
    
    now = get_uzb_now()
    now_hm = now.strftime("%H:%M")
    
    night_on = settings.get("night_mode_enabled", "1") == "1"
    night_start = settings.get("night_mode_start", "00:00")
    night_end = settings.get("night_mode_end", "07:00")
    
    if night_on:
        if night_start <= night_end:
            is_night_now = (night_start <= now_hm < night_end)
        else:
            is_night_now = (now_hm >= night_start or now_hm < night_end)
            
    if is_night_now:
        next_time_str = f"Ertalab soat {night_end} da (Tungi rejim faol)"
    else:
        if now.minute > 0 or now.second > 0:
            next_top_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        else:
            next_top_hour = now.replace(minute=0, second=0, microsecond=0)
        next_time_str = f"{next_top_hour.strftime('%H:00')} da (Soat boshida)"
        
    yt_times = get_youtube_schedule_times()
    next_yt_time_str = "—"
    if yt_times:
        upcoming_yt = [t for t in yt_times if t > now_hm]
        if upcoming_yt:
            next_yt_time_str = f"Bugun {upcoming_yt[0]} da"
        else:
            next_yt_time_str = f"Ertaga {yt_times[0]} da"
            
    return {
        "total": total,
        "pending": pending,
        "sent": sent,
        "failed": failed,
        "yt_uploaded": yt_uploaded,
        "next_post": next_post_dict,
        "last_sent": last_sent_dict,
        "next_time_estimate": next_time_str,
        "next_yt_time_estimate": next_yt_time_str,
        "is_night_mode_active": is_night_now,
        "settings": settings
    }


def reset_queue_status():
    """Barcha FAILED postlarni qayta PENDING qilish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE insta_posts_queue SET status = 'PENDING' WHERE status = 'FAILED'")
    count = cursor.rowcount
    conn.commit()
    conn.close()
    return count


def clear_all_queue():
    """Barcha navbatni tozalash"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM insta_posts_queue")
    conn.commit()
    conn.close()
    return True

def delete_queue_item(post_id):
    """Bitta postni navbatdan o'chirish va bulutda saqlash"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT shortcode FROM insta_posts_queue WHERE id = ?", (post_id,))
        row = cursor.fetchone()
        sc = row["shortcode"] if row else None

        cursor.execute("DELETE FROM insta_posts_queue WHERE id = ?", (post_id,))
        cursor.execute("DELETE FROM insta_post_likes WHERE post_id = ?", (post_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()

        if sc:
            try:
                cloud_state = load_insta_cloud_state()
                del_list = cloud_state.get("deleted_shortcodes", [])
                if sc not in del_list:
                    del_list.append(sc)
                cloud_state["deleted_shortcodes"] = del_list
                # Remove from custom_posts if exists
                if "custom_posts" in cloud_state:
                    cloud_state["custom_posts"] = [cp for cp in cloud_state["custom_posts"] if cp.get("shortcode") != sc]
                save_insta_cloud_state(cloud_state)
            except Exception as _ce:
                print(f"[Delete Cloud Sync Err]: {_ce}")

        return deleted
    except Exception as e:
        print(f"[Delete Queue Item Error]: {e}")
        return False


def get_queue_items(page=1, limit=500, status=None, search=None):
    """Navbatdagi postlarni Toshkent vaqti bo'yicha aniq rejalashtirilgan vaqtlar va qidiruv bilan olish"""
    init_insta_tables()
    page = max(1, int(page))
    limit = max(1, min(1000, int(limit)))
    offset = (page - 1) * limit
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    where_clauses = []
    params = []
    
    if status and status.upper() not in ("ALL", ""):
        if status.upper() == "YOUTUBE":
            where_clauses.append("youtube_uploaded = 1")
        else:
            where_clauses.append("status = ?")
            params.append(status.upper())
            
    if search:
        s_term = f"%{search.strip()}%"
        where_clauses.append("(shortcode LIKE ? OR caption LIKE ?)")
        params.extend([s_term, s_term])
        
    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
    
    # Count total matching
    count_sql = f"SELECT COUNT(*) as cnt FROM insta_posts_queue {where_sql}"
    cursor.execute(count_sql, params)
    total_count = cursor.fetchone()["cnt"]
    
    # Order: If status == 'SENT', sent_at DESC, else id ASC (xronologik eng eskisidan yangisiga)
    order_sql = "ORDER BY sent_at DESC" if status and status.upper() == "SENT" else "ORDER BY id ASC"
    
    query_sql = f"""
    SELECT id, shortcode, post_url, media_type, caption, media_url, post_date,
           status, sent_at, error_msg, likes_count, telegram_msg_id,
           youtube_uploaded, youtube_url, youtube_uploaded_at, created_at
    FROM insta_posts_queue
    {where_sql}
    {order_sql}
    LIMIT ? OFFSET ?
    """
    cursor.execute(query_sql, params + [limit, offset])
    raw_rows = cursor.fetchall()
    rows = []
    for r in raw_rows:
        d = dict(r)
        d["caption"] = clean_caption_text(d.get("caption") or "")
        rows.append(d)
    
    # Barcha PENDING / PROCESSING postlar uchun rejalashtirilgan kelgusi vaqtlarni hisoblash
    cursor.execute("SELECT id FROM insta_posts_queue WHERE status IN ('PENDING', 'PROCESSING') ORDER BY id ASC")
    all_pending_ids = [r["id"] for r in cursor.fetchall()]
    conn.close()
    
    settings = get_all_settings()
    interval_min = int(settings.get("interval_minutes") or 60)
    night_on = settings.get("night_mode_enabled", "1") == "1"
    night_start_str = settings.get("night_mode_start", "00:00")
    night_end_str = settings.get("night_mode_end", "07:00")
    
    now = get_uzb_now()
    
    # Har bir kutilayotgan postga Toshkent vaqti bo'yicha aniq soat boshidagi sana va soat belgilash (:00 da)
    if now.minute > 0 or now.second > 0:
        curr_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        curr_time = now.replace(minute=0, second=0, microsecond=0)
        
    schedule_map = {}
    for pid in all_pending_ids:
        if night_on:
            hm_str = curr_time.strftime("%H:%M")
            if night_start_str <= hm_str < night_end_str:
                end_parts = night_end_str.split(":")
                curr_time = curr_time.replace(hour=int(end_parts[0]), minute=int(end_parts[1]), second=0)
                if curr_time < now:
                    curr_time += timedelta(days=1)
        schedule_map[pid] = curr_time.strftime("%d.%m.%Y %H:%M")
        curr_time += timedelta(minutes=interval_min)
        
    for r in rows:
        if r.get("status") == 'SENT':
            r["scheduled_time"] = r.get("sent_at") or "Yuborildi"
        elif r.get("status") == 'FAILED':
            r["scheduled_time"] = "Xatolik"
        else:
            r["scheduled_time"] = schedule_map.get(r["id"]) or now.strftime("%d.%m.%Y %H:%M")
        
    return {
        "success": True,
        "items": rows,
        "total": total_count,
        "page": page,
        "limit": limit,
        "total_pages": (total_count + limit - 1) // limit if limit > 0 else 1
    }


def post_single_item(post_id, chat_id=None, bot_token=None):
    """Bitta aniq tanlangan postni Telegramga yuborish"""
    init_insta_tables()
    
    if not bot_token:
        bot_token = get_setting("bot_token", DEFAULT_BOT_TOKEN)
    if not chat_id:
        chat_id = get_setting("target_chat_id", DEFAULT_TARGET_CHAT_ID)
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM insta_posts_queue WHERE id = ?", (post_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return {"success": False, "error": f"Post topilmadi (ID: {post_id})"}
        
    shortcode = row["shortcode"]
    post_url = row["post_url"]
    
    # ATOMIC CLAIM
    now_claim_str = get_uzb_now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE insta_posts_queue SET status = 'PROCESSING', sent_at = ? WHERE id = ? AND status = 'PENDING'", (now_claim_str, post_id))
    conn.commit()
    if cursor.rowcount == 0 and row["status"] != 'FAILED':
        conn.close()
        return {"success": False, "message": "Ushbu post ayni paytda yuborilmoqda yoki allaqachon yuborilgan."}
        
    set_setting("last_post_time", now_claim_str)
    
    bot = telebot.TeleBot(bot_token)
    
    try:
        username = get_setting("insta_username", DEFAULT_INSTA_USERNAME)
        
        raw_caption = row["caption"] or ""
        video_direct_url = None
        if not raw_caption:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            content = loop.run_until_complete(_fetch_post_content_async(post_url))
            loop.close()
            raw_caption = content.get("caption") or ""
            video_direct_url = content.get("video_url")
            
        clean_caption = clean_caption_text(raw_caption, username)
        
        if len(clean_caption) > 1000:
            telegram_caption = clean_caption[:997] + "..."
        else:
            telegram_caption = clean_caption
            
        inline_kb = get_post_inline_keyboard(post_id, post_url, likes_count=row["likes_count"] or 0)
        
        media_sent = False
        sent_msg = None
        
        # 1. HD Video yuklash (Reels/Video postlar uchun)
        if row["media_type"] in ("reel", "video") or "/reel/" in post_url:
            hd_video_path = _download_hd_video_ytdlp(post_url)
            if hd_video_path and os.path.exists(hd_video_path):
                try:
                    with open(hd_video_path, 'rb') as v_file:
                        sent_msg = bot.send_video(
                            chat_id,
                            v_file,
                            caption=telegram_caption,
                            parse_mode="HTML" if telegram_caption else None,
                            reply_markup=inline_kb,
                            supports_streaming=True
                        )
                    media_sent = True
                finally:
                    if os.path.exists(hd_video_path):
                        os.remove(hd_video_path)
                        
            if not media_sent and video_direct_url:
                v_res = requests.get(video_direct_url, timeout=40, headers={"User-Agent": _INSTA_UA})
                if v_res.status_code == 200:
                    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
                        f.write(v_res.content)
                        temp_v_path = f.name
                    try:
                        with open(temp_v_path, 'rb') as v_file:
                            sent_msg = bot.send_video(
                                chat_id,
                                v_file,
                                caption=telegram_caption,
                                parse_mode="HTML" if telegram_caption else None,
                                reply_markup=inline_kb,
                                supports_streaming=True
                            )
                        media_sent = True
                    finally:
                        if os.path.exists(temp_v_path):
                            os.remove(temp_v_path)
                            
        # 2. Rasm jo'natish (Statik rasm postlari uchun)
        if not media_sent and row["media_url"]:
            img_url = row["media_url"]
            try:
                p_res = requests.get(img_url, timeout=30, headers={"User-Agent": _INSTA_UA})
                if p_res.status_code == 200:
                    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
                        f.write(p_res.content)
                        temp_p_path = f.name
                    try:
                        with open(temp_p_path, 'rb') as p_file:
                            sent_msg = bot.send_photo(
                                chat_id,
                                p_file,
                                caption=telegram_caption,
                                parse_mode="HTML" if telegram_caption else None,
                                reply_markup=inline_kb
                            )
                        media_sent = True
                    finally:
                        if os.path.exists(temp_p_path):
                            os.remove(temp_p_path)
            except Exception as _pe:
                print(f"[Photo Send Err]: {_pe}")
                
        # 3. Matnli xabar orqali jo'natish (oxirgi zaxira)
        if not media_sent:
            sent_msg = bot.send_message(
                chat_id,
                telegram_caption or f"📢 Instagram: {post_url}",
                reply_markup=inline_kb,
                parse_mode="HTML" if telegram_caption else None
            )
            media_sent = True
            
        now_str = get_uzb_now().strftime("%Y-%m-%d %H:%M:%S")
        msg_id_val = sent_msg.message_id if sent_msg else None
        cursor.execute("""
        UPDATE insta_posts_queue 
        SET status = 'SENT', sent_at = ?, caption = ?, error_msg = NULL, telegram_msg_id = ?
        WHERE id = ?
        """, (now_str, clean_caption, msg_id_val, post_id))
        conn.commit()
        
        mark_post_sent_in_cloud(shortcode, now_str)
        set_setting("last_post_time", now_str)
        conn.close()
        
        notify_admin_post_published("telegram", {
            "post_id": post_id,
            "shortcode": shortcode,
            "post_url": post_url,
            "caption": clean_caption,
            "msg_id": msg_id_val,
            "target_chat_id": chat_id
        })
        
        return {
            "success": True,
            "post_id": post_id,
            "shortcode": shortcode,
            "post_url": post_url,
            "caption": clean_caption[:80]
        }
    except Exception as e:
        err_msg = str(e)
        print(f"[Post Single Error] ({post_url}): {e}")
        print(traceback.format_exc())
        cursor.execute("""
        UPDATE insta_posts_queue 
        SET status = 'FAILED', error_msg = ?
        WHERE id = ?
        """, (err_msg, post_id))
        conn.commit()
        conn.close()
        return {
            "success": False,
            "post_id": post_id,
            "error": err_msg
        }
