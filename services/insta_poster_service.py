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
import subprocess
import requests
import telebot
from datetime import datetime, timezone, timedelta
from services.atlas_db import get_db_connection

UZB_TZ = timezone(timedelta(hours=5))

def get_uzb_now():
    """Toshkent (O'zbekiston, UTC+5) bo'yicha joriy vaqtni olish"""
    return datetime.now(timezone.utc).astimezone(UZB_TZ).replace(tzinfo=None)

DEFAULT_BOT_TOKEN = "8818017813:AAEJTzJ97jCPIYy5exZSjFNHOcSvcHkjDJk"
DEFAULT_TARGET_CHAT_ID = "-1004295470034"
DEFAULT_INSTA_USERNAME = "shahrisabz_t_t_uz"

# Barcha 12 ta post (Kanal boshlangan dastlabki kunlardan to hozirgi kungacha xronologik tartibda)
DEFAULT_SEEDED_POSTS = [
    {
        "shortcode": "DTKl4neiIGi",
        "url": "https://www.instagram.com/p/DTKl4neiIGi",
        "media_type": "post",
        "post_date": "2024-01-20",
        "caption": "🎓 Shahrisabz tibbiyot texnikumi — rasmiy axborot va qabul sahifasi.\n\n📍 Shahrisabz shahar\n☎️ 88 260 20 73",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/611243991_17854198077603794_8141413038807599667_n.heic?stp=dst-jpg_e35_tt6&_nc_cat=107&_nc_map=urlgen_bucketless&ig_cache_key=MzgwNDAxOTQ1MzY2NzYwNjk0Ng%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkZFRUQueHBpZHMuMTA4MC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=7pSI3-_Pc-cQ7kNvwEneT1q&_nc_oc=AdrtdIbWBsE78EMouREb3QS-9JC3WF7ZRYJZWGsNxFMPy3ughxkO86aYSuFvcK2V6m8&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=QEXrn4rzV57_hezr1f_ABA&_nc_ss=7ea8c&oh=00_AQEvJxD_Uzw3hlU6bqcsSur9paMbfNHJ_gaf-cShbjSpCw&oe=6A8DD7FA"
    },
    {
        "shortcode": "DTKl2WlCFbP",
        "url": "https://www.instagram.com/p/DTKl2WlCFbP",
        "media_type": "post",
        "post_date": "2024-01-20",
        "caption": "🏥 Zamonaviy tibbiy ta'lim va amaliyot maskani.\n\n📍 Shahrisabz tibbiyot texnikumi",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/611276333_17854198053603794_4631092453008533657_n.heic?stp=dst-jpg_e35_tt6&_nc_cat=106&_nc_map=urlgen_bucketless&ig_cache_key=MzgwNDAxOTI5ODA4NDA4MzQwNw%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkZFRUQueHBpZHMuMTQ0MC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=WRFpBdaCtusQ7kNvwFqqHcN&_nc_oc=AdoM1OdcwT8ITNZBz7401pEMznFxeC7soCX1ofSnTLUrAckxPTt8cLa5t9E3qumfRN8&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=zo4Uz_WYYs7DLt2XxB1MDQ&_nc_ss=7ea8c&oh=00_AQGkuyjL2eeKpcCl_T9LvaQ6eL6IE-lJKZlMvL9GNM-9Kw&oe=6A8DD489"
    },
    {
        "shortcode": "DTKlzm8CJ5N",
        "url": "https://www.instagram.com/p/DTKlzm8CJ5N",
        "media_type": "post",
        "post_date": "2024-01-20",
        "caption": "🩺 Malakali ustozlar va amaliy laboratoriyalar.\n\n📍 Shahrisabz tibbiyot texnikumi",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/612116905_17854198023603794_5331005024687690903_n.heic?stp=dst-jpg_e35_tt6&_nc_cat=105&_nc_map=urlgen_bucketless&ig_cache_key=MzgwNDAxOTEwOTQ5MTQxNjY1Mw%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkZFRUQueHBpZHMuMTA4MC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=zddiMk2qPogQ7kNvwHpBAth&_nc_oc=AdpY3YAPdluDBAOp7-STkH443s_tJc8lT4Pi8SQE0y_9EXvPgoTXguPVZyO4qkW-Sfc&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=7eVuoKPXPYmGinTZusWG9w&_nc_ss=7ea8c&oh=00_AQEpr9wKXvY5Nym4EjE_bzkLMHD3aEW-sK4XfmT6h_nOdw&oe=6A8DF77F"
    },
    {
        "shortcode": "DbsKZ2qICdh",
        "url": "https://www.instagram.com/reel/DbsKZ2qICdh",
        "media_type": "reel",
        "post_date": "2026-08-06",
        "caption": "🎓 Kelajagingizni bugundan boshlang!\n\n👩‍⚕️ Davlat namunasidagi diplom asosida zamonaviy tibbiy kasbni egallang.\n\n✅ Hamshiralik\n✅ Feldsherlik\n✅ Farmatsiya\n\n📚 Qulay to’lov imkoniyatlari\n👨‍🏫 Tajribali ustozlar\n💼 Bitirgach ish topish imkoniyatini oshiruvchi amaliy ta’lim\n\n📍 Shahrisabz tibbiyot texnikumi\n\n📞 Batafsil ma’lumot va ro’yxatdan o’tish:\n☎️ 88 260 20 73\n☎️ 97 266 20 73\n\n⏳ Qabul davom etmoqda. Joylar cheklangan — hoziroq murojaat qiling!"
    },
    {
        "shortcode": "DbyU4H_oLZr",
        "url": "https://www.instagram.com/reel/DbyU4H_oLZr",
        "media_type": "reel",
        "post_date": "2026-08-08",
        "caption": "🎓 SHAHRISABZ TIBBIYOT TEXNIKUMI\n\n📢 QABUL DAVOM ETMOQDA!\n\nKelajagingizni tibbiyot sohasi bilan bog‘lashni istaysizmi? 🩺\nUnda bizning texnikumimizga hujjat topshirishga shoshiling!\n\n👩🏻‍⚕️Hamshiralik ishi\n🩺Davolash ishi\n💊Farmatsiya\n\n📞 Murojaat uchun telefon raqamlari:\n☎️ 88 260 20 73\n☎️ 97 266 20 73\n\n✨ Sifatli ta’lim — yorqin kelajak sari birinchi qadam!"
    },
    {
        "shortcode": "Db0U9ivIcwC",
        "url": "https://www.instagram.com/p/Db0U9ivIcwC",
        "media_type": "post",
        "post_date": "2026-08-09",
        "caption": "🩺 SHAHRISABZ TIBBIYOT TEXNIKUMI\n🎓 3 OYLIK HAMSHIRALIK KURSI\n📚 Nazariy bilimlar • Amaliy ko‘nikmalar • Tajribali ustozlar\n\n💙 Tibbiyot sohasiga ilk qadamingizni biz bilan boshlang!\n\n👩‍⚕️ Yo‘nalishlar:\n• Hamshiralik ishi\n• Davolash ishi\n• Farmasevtika\n\n📢 Qabul davom etmoqda!\n\n📞 Murojaat uchun:\n88 260 20 73\n97 266 20 73\n📍 Shahrisabz tibbiyot texnikumi\n✨ Kelajagingizni bugundan boshlang!",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/768604174_17889330708603794_2515257640581746909_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=102&_nc_map=urlgen_bucketless&ig_cache_key=Mzk1OTg4MjE2MjQ4MTc3NzY2Ng%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkZFRUQueHBpZHMuMTI1NC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=Lf_Gs-HboeUQ7kNvwE5nXLq&_nc_oc=AdrGFx6YasSpN79YkPmcmmv4UQ12HmXce5_whufzGubjE5kjTPhXeO2mTHyPHYAngYk&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=8S0WoXyNOEm2_F52LgqR1w&_nc_ss=7ea8c&oh=00_AQEz_VB3NGRydzG5-sWRAyqnqC0K6n3XfgyqrWg6Mue-3w&oe=6A8DCFC9"
    },
    {
        "shortcode": "Db-ssJeIyZh",
        "url": "https://www.instagram.com/reel/Db-ssJeIyZh",
        "media_type": "reel",
        "post_date": "2026-08-13",
        "caption": "🎓 SHAHRISABZ TIBBIYOT TEXNIKUMIDA QABUL DAVOM ETMOQDA! 🩺\n\nKelajakdagi kasbingizni bugundan tanlang! 💙\nSifatli ta’lim, zamonaviy bilim va tibbiyot sohasida mustahkam kelajak sari bir qadam! 👩‍⚕️👨‍⚕️\n\n📞 Murojaat uchun:\n☎️ 77 088 20 73\n☎️ 88 260 20 73\n☎️ 97 266 20 73\n\n📍 Shahrisabz tibbiyot texnikumi\n✨ Qabul davom etmoqda! Shoshiling, o‘z o‘rningizni band qiling!"
    },
    {
        "shortcode": "DcBekL6Omao",
        "url": "https://www.instagram.com/reel/DcBekL6Omao",
        "media_type": "reel",
        "post_date": "2026-08-14",
        "caption": "📚 3 OYLIK HAMSHIRALIK KURSI\n\n🩺 Shahrisabz tibbiyot texnikumida 3 oylik hamshiralik kursiga qabul davom etmoqda!\n\n🎓 Zamonaviy bilim va amaliy ko‘nikmalar\n👩‍⚕️ Tajribali mutaxassislardan ta’lim\n📜 Kurs yakunida rasmiy sertifikat\n\n📞 Murojaat uchun:\n☎️ 77 088 20 73\n☎️ 88 260 20 73\n☎️ 97 266 20 73\n\n📍 Shahrisabz tibbiyot texnikumi\n\nJoylar soni cheklangan! Hoziroq ro'yxatdan o'ting."
    },
    {
        "shortcode": "DcDX1cOoIoX",
        "url": "https://www.instagram.com/reel/DcDX1cOoIoX",
        "media_type": "reel",
        "post_date": "2026-08-15",
        "caption": "📚 Shahrisabz tibbiyot texnikumi — kelajagingiz uchun mustahkam qadam! 🩺\n\n🎓 Zamonaviy ta’lim\n👩‍⚕️ Amaliy mashg‘ulotlar\n📚 Sifatli bilim va tajriba\n\n📞 Batafsil ma’lumot uchun:\n+998 77 088 20 73\n+998 97 266 20 73\n+998 88 260 20 73\n\n📍 Shahrisabz tibbiyot texnikumi"
    },
    {
        "shortcode": "DcIsWQ5IT8b",
        "url": "https://www.instagram.com/reel/DcIsWQ5IT8b",
        "media_type": "reel",
        "post_date": "2026-08-17",
        "caption": "📚 Shahrisabz tibbiyot texnikumi — kelajagingiz uchun mustahkam qadam! 🩺\n\n🎓 Zamonaviy ta’lim\n👩‍⚕️ Amaliy mashg‘ulotlar\n📚 Sifatli bilim va tajriba\n\n📞 Batafsil ma’lumot uchun:\n+998 77 088 20 73\n+998 88 260 20 73\n+998 97 266 20 73\n\n📍 Shahrisabz tibbiyot texnikumi"
    },
    {
        "shortcode": "DcLj3zwqODC",
        "url": "https://www.instagram.com/reel/DcLj3zwqODC",
        "media_type": "reel",
        "post_date": "2026-08-18",
        "caption": "📚 Tibbiyotda o‘qishni xohlayapsizmi? 🩺\nUnda bu video aynan siz uchun! ❤️\n\n📍 Shahrisabz tibbiyot texnikumi — kelajakdagi kasbingiz sari ishonchli qadam! 🎓\n\n📲 Batafsil ma’lumot uchun:\n☎️ 88 260 20 73\n☎️ 77 088 20 73\n☎️ 97 266 20 73\n\n❤️ Bu videoni tibbiyotda o‘qishni xohlayotgan do‘stingizga yuboring!"
    },
    {
        "shortcode": "DcLkGzAqbz9",
        "url": "https://www.instagram.com/reel/DcLkGzAqbz9",
        "media_type": "reel",
        "post_date": "2026-08-18",
        "caption": "🩺 Bugun kasb tanlaysiz — ertaga shu kasb bilan daromad topasiz! 🎓✨\n\nKelajagingiz uchun to‘g‘ri tanlov qiling!\n🏥 Shahrisabz tibbiyot texnikumi — bilim, kasb va kelajak sari ishonchli qadam! ❤️\n\n📲 Batafsil ma’lumot uchun:\n☎️ 88 260 20 73\n☎️ 77 088 20 73\n☎️ 97 266 20 73"
    }
]

# ------------------------------------------------------------
# 1. Database Initialization & Settings
# ------------------------------------------------------------

def init_insta_tables():
    """Instagram navbati, sozlamalari, layklar va YouTube jadvallarini yaratish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Postlar navbati jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insta_posts_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shortcode TEXT UNIQUE NOT NULL,
        post_url TEXT NOT NULL,
        media_type TEXT DEFAULT 'unknown', -- 'photo', 'video', 'carousel', 'reel'
        caption TEXT,
        media_url TEXT,
        post_date TEXT,
        status TEXT DEFAULT 'PENDING',    -- 'PENDING', 'SENT', 'FAILED'
        sent_at TEXT,
        error_msg TEXT,
        likes_count INTEGER DEFAULT 0,
        telegram_msg_id INTEGER,
        youtube_uploaded INTEGER DEFAULT 0,
        youtube_url TEXT,
        youtube_uploaded_at TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Ustunlar mavjudligini tekshirib, kerak bo'lsa qo'shish (Migration)
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
    
    # 2. Layklar jadvali (Har bir foydalanuvchining 1 ta layk bosishini nazorat qilish)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insta_post_likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(post_id, user_id)
    )
    """)
    
    # 3. Modul sozlamalari jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insta_settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    
    # Boshlang'ich sozlamalarni kiritish
    defaults = {
        "bot_token": DEFAULT_BOT_TOKEN,
        "target_chat_id": DEFAULT_TARGET_CHAT_ID,
        "insta_username": DEFAULT_INSTA_USERNAME,
        "auto_schedule_enabled": "0",       # 0: O'chirilgan, 1: Yoqilgan (Telegram)
        "interval_minutes": "60",           # Har 60 daqiqada (Telegram uchun)
        "last_post_time": "",
        "is_scanning": "0",
        "last_scan_time": "",
        "last_scan_count": "12",
        "night_mode_enabled": "1",          # 0: O'chirilgan, 1: Yoqilgan (00:00 - 07:00)
        "night_mode_start": "00:00",
        "night_mode_end": "07:00",
        "youtube_auto_upload": "1",         # 0: O'chirilgan, 1: Yoqilgan
        "youtube_schedule_enabled": "1",    # YouTube jadvali faolmi?
        "youtube_schedule_times": "09:00,12:00,15:00,18:30,21:00",  # 5 ta Rek vaqtlari
        "youtube_last_posted_slot": ""      # Oxirgi yuborilgan slot
    }
    
    for k, v in defaults.items():
        cursor.execute("INSERT OR IGNORE INTO insta_settings (key, value) VALUES (?, ?)", (k, v))

    # 4. Barcha 12 ta postni bazaga kiritish / yangilash (Eskisidan yangisiga qarab)
    for p in DEFAULT_SEEDED_POSTS:
        cursor.execute("""
        INSERT OR IGNORE INTO insta_posts_queue (shortcode, post_url, media_type, caption, media_url, post_date, status)
        VALUES (?, ?, ?, ?, ?, ?, 'PENDING')
        """, (p["shortcode"], p["url"], p["media_type"], p["caption"], p.get("media_url") or "", p["post_date"]))
        
        cursor.execute("""
        UPDATE insta_posts_queue 
        SET caption = CASE WHEN caption IS NULL OR caption = '' THEN ? ELSE caption END,
            post_date = CASE WHEN post_date IS NULL OR post_date = '' THEN ? ELSE post_date END,
            media_type = ?,
            media_url = CASE WHEN media_url IS NULL OR media_url = '' THEN ? ELSE media_url END
        WHERE shortcode = ?
        """, (p["caption"], p["post_date"], p["media_type"], p.get("media_url") or "", p["shortcode"]))
        
    conn.commit()
    conn.close()


def get_setting(key, default=""):
    """Sozlamani olish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM insta_settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row["value"]
    except Exception as e:
        print(f"[Insta Settings Error]: {e}")
    return default


def set_setting(key, value):
    """Sozlamani yangilash"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO insta_settings (key, value) VALUES (?, ?)", (key, str(value)))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[Insta Set Setting Error]: {e}")
        return False


def get_all_settings():
    """Barcha sozlamalarni lug'at ko'rinishida olish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM insta_settings")
        rows = cursor.fetchall()
        conn.close()
        return {r["key"]: r["value"] for r in rows}
    except Exception as e:
        print(f"[Insta Get All Settings Error]: {e}")
        return {}

# ------------------------------------------------------------
# 2. Like Boshqaruvi va Inline Tugmalar
# ------------------------------------------------------------

def get_post_inline_keyboard(post_id, post_url, likes_count=0):
    """Post tagidagi Like va Instagramga o'tish inline tugmalari"""
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn_like = telebot.types.InlineKeyboardButton(f"❤️ {likes_count}", callback_data=f"insta_like_{post_id}")
    btn_link = telebot.types.InlineKeyboardButton("🔗 Instagramda ko‘rish", url=post_url)
    markup.add(btn_like, btn_link)
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
    """Instagram caption matnini tozalash"""
    if not raw_caption:
        return ""
    text = raw_caption.strip()
    
    if username and text.lower().startswith(username.lower()):
        text = text[len(username):].strip()
        
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
        
    return text

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


def add_posts_by_urls(urls_text):
    """Foydalanuvchi kiritgan Instagram havolalari yoki shortcode'larini navbatga qo'shish"""
    init_insta_tables()
    if not urls_text or not str(urls_text).strip():
        return {"success": False, "error": "Havolalar kiritilmadi"}
    
    text = str(urls_text).strip()
    codes = []
    
    # 1. URL pattern orqali topish (masalan: instagram.com/reel/CODE yoki instagram.com/p/CODE)
    url_matches = re.findall(r'instagram\.com/(?:[a-zA-Z0-9_\.]+/)?(?:reel|p)/([A-Za-z0-9_-]+)', text, re.IGNORECASE)
    for c in url_matches:
        c = c.strip('/')
        if c and c not in codes:
            codes.append(c)
            
    # 2. Qatorlar bo'yicha ajratish
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        cleaned = line.split('?')[0].rstrip('/')
        parts = cleaned.split('/')
        last_part = parts[-1].strip()
        if len(last_part) >= 9 and len(last_part) <= 15 and re.match(r'^[A-Za-z0-9_-]+$', last_part):
            if last_part not in codes:
                codes.append(last_part)
                
    if not codes:
        return {"success": False, "error": "Birorta ham to'g'ri Instagram post/reel havolasi yoki kodi topilmadi"}
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    added_count = 0
    for code in codes:
        is_reel = True
        post_url = f"https://www.instagram.com/reel/{code}"
        try:
            cursor.execute("""
            INSERT OR IGNORE INTO insta_posts_queue (shortcode, post_url, media_type, status)
            VALUES (?, ?, ?, 'PENDING')
            """, (code, post_url, "reel" if is_reel else "post"))
            if cursor.rowcount > 0:
                added_count += 1
        except Exception as e:
            print(f"[Manual Add Error]: {e}")
            
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "total_parsed": len(codes),
        "new_added": added_count,
        "codes": codes,
        "message": f"{len(codes)} ta postdan {added_count} tasi navbatga muvaffaqiyatli qo'shildi."
    }


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

def _download_hd_video_ytdlp(post_url):
    """yt-dlp Python moduli yordamida videoni to'g'ridan-to'g'ri yuklab olish (Vercel va barcha tizimlarda 100% ishlaydi)"""
    try:
        import yt_dlp
        temp_dir = tempfile.gettempdir()
        out_filename = os.path.join(temp_dir, f"insta_hd_{int(time.time()*1000)}.mp4")
        
        ydl_opts = {
            "outtmpl": out_filename,
            "format": "best[ext=mp4]/best",
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": 30
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([post_url])
            
        if os.path.exists(out_filename) and os.path.getsize(out_filename) > 10000:
            return out_filename
            
        base_prefix = out_filename.replace(".mp4", "")
        for ext in [".mp4", ".mkv", ".webm"]:
            cand = base_prefix + ext
            if os.path.exists(cand) and os.path.getsize(cand) > 10000:
                return cand
    except Exception as e:
        print(f"[yt-dlp Python Module Error]: {e}")
        
    return None


async def _fetch_post_content_async(post_url):
    """Postning to'liq ma'lumotlarini olish (yt-dlp orqali tezkor va xavfsiz)"""
    try:
        import yt_dlp
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "socket_timeout": 15
        }
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
        print(f"[yt-dlp info error]: {yte}")

    try:
        from playwright.async_api import async_playwright
        parts = post_url.rstrip('/').split('/')
        code = parts[-1]
        is_reel = "/reel/" in post_url
        embed_url = f"https://www.instagram.com/{'reel' if is_reel else 'p'}/{code}/embed/captioned/"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
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
        print(f"[Playwright skipped]: {pe}")
        
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
                v_res = requests.get(video_direct_url, timeout=40)
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
        if not media_sent and (row.get("media_url") or row.get("img_url")):
            img_url = row.get("media_url") or row.get("img_url")
            try:
                p_res = requests.get(img_url, timeout=30)
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
        
        set_setting("last_post_time", now_str)
        conn.close()
        
        return {
            "success": True,
            "post_id": post_id,
            "shortcode": shortcode,
            "post_url": post_url,
            "caption": clean_caption[:80]
        }
        
    except Exception as e:
        err_msg = str(e)
        cursor.execute("""
        UPDATE insta_posts_queue 
        SET status = 'FAILED', error_msg = ?
        WHERE id = ?
        """, (err_msg, post_id))
        conn.commit()
        conn.close()
        print(f"[Post Next Error]: {e}")
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
            conn.close()
            return {
                "success": False,
                "error": f"Videoni yuklab bo'lmadi: {post_url}"
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
            
            return {
                "success": True,
                "post_id": post_id,
                "shortcode": shortcode,
                "url": yt_res.get("url"),
                "title": yt_res.get("title")
            }
        else:
            conn.close()
            return {
                "success": False,
                "error": yt_res.get("error")
            }
    except Exception as e:
        conn.close()
        print(f"[YouTube Upload Queue Error]: {e}")
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
    elif last_post_str:
        try:
            last_dt = datetime.strptime(last_post_str, "%Y-%m-%d %H:%M:%S")
            target_dt = last_dt + timedelta(minutes=interval_min)
            if target_dt > now:
                next_time_str = target_dt.strftime("%H:%M")
            else:
                next_time_str = "Hozir (Navbatdagi siklda)"
        except Exception:
            next_time_str = "Hozir"
            
    return {
        "total": total,
        "pending": pending,
        "sent": sent,
        "failed": failed,
        "yt_uploaded": yt_uploaded,
        "next_post": next_post_dict,
        "last_sent": last_sent_dict,
        "next_time_estimate": next_time_str,
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
    """Bitta postni navbatdan o'chirish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM insta_posts_queue WHERE id = ?", (post_id,))
        cursor.execute("DELETE FROM insta_post_likes WHERE post_id = ?", (post_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted
    except Exception as e:
        print(f"[Delete Queue Item Error]: {e}")
        return False


def get_queue_items(page=1, limit=50, status=None, search=None):
    """Navbatdagi postlarni sahifalash, Toshkent vaqti bo'yicha aniq rejalashtirilgan vaqtlar va qidiruv bilan olish"""
    init_insta_tables()
    page = max(1, int(page))
    limit = max(1, min(200, int(limit)))
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
    rows = [dict(r) for r in cursor.fetchall()]
    
    # Barcha PENDING postlar uchun rejalashtirilgan kelgusi vaqtlarni hisoblash
    cursor.execute("SELECT id FROM insta_posts_queue WHERE status = 'PENDING' ORDER BY id ASC")
    all_pending_ids = [r["id"] for r in cursor.fetchall()]
    conn.close()
    
    settings = get_all_settings()
    interval_min = int(settings.get("interval_minutes") or 60)
    last_post_str = settings.get("last_post_time", "")
    night_on = settings.get("night_mode_enabled", "1") == "1"
    night_start_str = settings.get("night_mode_start", "00:00")
    night_end_str = settings.get("night_mode_end", "07:00")
    
    now = get_uzb_now()
    
    start_dt = now
    if last_post_str:
        try:
            last_dt = datetime.strptime(last_post_str, "%Y-%m-%d %H:%M:%S")
            cand = last_dt + timedelta(minutes=interval_min)
            if cand > now:
                start_dt = cand
            else:
                start_dt = now
        except Exception:
            start_dt = now
            
    # Har bir kutilayotgan postga Toshkent vaqti bo'yicha sana va soat belgilash
    curr_time = start_dt
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
        r["scheduled_time"] = schedule_map.get(r["id"]) or "—"
        
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
                v_res = requests.get(video_direct_url, timeout=40)
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
        if not media_sent and (row.get("media_url") or row.get("img_url")):
            img_url = row.get("media_url") or row.get("img_url")
            try:
                p_res = requests.get(img_url, timeout=30)
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
        
        set_setting("last_post_time", now_str)
        conn.close()
        
        return {
            "success": True,
            "post_id": post_id,
            "shortcode": shortcode,
            "post_url": post_url,
            "caption": clean_caption[:80]
        }
    except Exception as e:
        err_msg = str(e)
        cursor.execute("""
        UPDATE insta_posts_queue 
        SET status = 'FAILED', error_msg = ?
        WHERE id = ?
        """, (err_msg, post_id))
        conn.commit()
        conn.close()
        print(f"[Post Single Error]: {e}")
        return {
            "success": False,
            "post_id": post_id,
            "error": err_msg
        }


