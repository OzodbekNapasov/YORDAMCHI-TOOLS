# ============================================================
#  services/atlas_db.py
#  ATLAS Platformasi — SQLite Database va Ma'lumotlar Boshqaruvi
# ============================================================

import os
import sqlite3
import json
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
is_serverless = os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME") or os.path.exists("/tmp")
if is_serverless:
    DB_PATH = "/tmp/atlas.db"
else:
    DB_PATH = os.path.join(BASE_DIR, "atlas.db")


def get_db_connection():
    """Ma'lumotlar bazasiga ulanish (dictionary cursor bilan)"""
    if is_serverless and not os.path.exists(DB_PATH):
        try:
            init_db()
        except Exception:
            pass
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Barcha jadvallarni va boshlang'ich ma'lumotlarni yaratish"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Foydalanuvchilar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE NOT NULL,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        phone TEXT,
        status TEXT DEFAULT 'active', -- active, blocked
        role TEXT DEFAULT 'user',     -- admin, accountant, user
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_active_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_requests INTEGER DEFAULT 0,
        notes TEXT
    )
    """)

    # 2. Guruhlar va Kanallar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE NOT NULL,
        title TEXT NOT NULL,
        username TEXT,
        type TEXT DEFAULT 'group',    -- group, supergroup, channel
        members_count INTEGER DEFAULT 0,
        status TEXT DEFAULT 'active', -- active, left, restricted
        bot_is_admin INTEGER DEFAULT 1,
        last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 3. Yuborilgan xabarlar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipient_type TEXT NOT NULL, -- user, group, channel, broadcast
        recipient_id TEXT NOT NULL,
        message_type TEXT DEFAULT 'text', -- text, photo, document, video
        content TEXT,
        media_path TEXT,
        status TEXT DEFAULT 'sent',   -- pending, sent, failed
        error_msg TEXT,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 4. Ommaviy xabarlar (Broadcasts) jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS broadcasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        target TEXT DEFAULT 'all_users', -- all_users, groups, channels, custom
        message_type TEXT DEFAULT 'text',
        content TEXT NOT NULL,
        media_path TEXT,
        total_recipients INTEGER DEFAULT 0,
        sent_count INTEGER DEFAULT 0,
        delivered_count INTEGER DEFAULT 0,
        failed_count INTEGER DEFAULT 0,
        status TEXT DEFAULT 'draft',    -- draft, running, completed, cancelled
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP
    )
    """)

    # 5. Avtomatlashtirish qoidalari (Automations) jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS automations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        trigger_type TEXT NOT NULL,     -- user_join, command, keyword, schedule
        trigger_value TEXT NOT NULL,
        condition_json TEXT,
        action_type TEXT NOT NULL,      -- send_message, alert_admin, generate_doc
        action_payload_json TEXT NOT NULL,
        is_active INTEGER DEFAULT 1,
        execution_count INTEGER DEFAULT 0,
        last_executed_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 6. Fon vazifalari (Tasks) jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        task_type TEXT NOT NULL,
        status TEXT DEFAULT 'queued',   -- queued, running, completed, failed
        started_at TIMESTAMP,
        ended_at TIMESTAMP,
        duration_seconds REAL DEFAULT 0,
        result_json TEXT,
        error_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 7. Audit loglar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        actor TEXT NOT NULL,            -- admin, bot, system, user_id
        module TEXT NOT NULL,           -- auth, users, messages, contracts, documents, settings
        action TEXT NOT NULL,
        status TEXT DEFAULT 'success',  -- success, warning, error, info
        details_json TEXT,
        ip_address TEXT
    )
    """)

    # 8. Tizim sozlamalari jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        category TEXT DEFAULT 'general',
        description TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 9. Modullar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS modules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        is_enabled INTEGER DEFAULT 1,
        settings_json TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 10. Yaratilgan rasmiy hujjatlar tarixi
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS generated_docs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        template_id TEXT NOT NULL,
        template_name TEXT NOT NULL,
        recipient_fio TEXT NOT NULL,
        data_json TEXT NOT NULL,
        file_type TEXT DEFAULT 'png',   -- png, docx, pdf
        file_path TEXT,
        created_by TEXT DEFAULT 'bot',  -- bot, web_admin
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 11. Administrator hisob jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT DEFAULT 'superadmin',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login_at TIMESTAMP
    )
    """)

    # Boshlang'ich tizim sozlamalari
    default_settings = [
        ("bot_name", "Qarshi Tibbiyot Texnikumi Bot", "general", "Botning rasmiy nomi"),
        ("bot_username", "@qarshi_tibbiyot_bot", "general", "Bot username"),
        ("mode", "webhook", "bot", "Ishlash rejimi (webhook yoki polling)"),
        ("primary_admin_id", "8135594558", "security", "Bosh administrator Telegram ID"),
        ("allowed_users", "[\"8135594558\"]", "security", "Ruxsat etilgan foydalanuvchilar ro'yxati"),
        ("version", "2.1.0", "system", "ATLAS Platforma versiyasi"),
        ("maintenance_mode", "0", "system", "Texnik profilaktika rejimi")
    ]
    for k, v, cat, desc in default_settings:
        cursor.execute("""
        INSERT OR IGNORE INTO system_settings (key, value, category, description)
        VALUES (?, ?, ?, ?)
        """, (k, v, cat, desc))

    # Boshlang'ich modullar
    default_modules = [
        ("contracts", "Kontraktlar va Debitorlik", "Talabalar to'lov kontraktlarini yangilash va debitorlik hisobotlari", 1, "{}"),
        ("documents", "Ma'lumotnomalar Generatori", "1-kursga qabul va o'qiyotganligi haqida 300 DPI rasmiy ma'lumotnomalar", 1, "{}"),
        ("screenshots", "Guruh Screenshotlari", "Guruhlar bo'yicha to'lov ro'yxati grafik screenshotlari", 1, "{}"),
        ("broadcast", "Ommaviy Xabarlar", "Foydalanuvchilar va guruhlarga mass broadcast yuborish tizimi", 1, "{}"),
        ("automation", "Avtomatlashtirish Dvigateli", "Triggers, shartlar va avtomatik reaksiyalar", 1, "{}"),
        ("audit_logs", "Audit va Monitoring", "Barcha operatsiyalar va so'rovlarni xavfsiz qayd qilish", 1, "{}")
    ]
    for key, name, desc, en, s_json in default_modules:
        cursor.execute("""
        INSERT OR IGNORE INTO modules (key, name, description, is_enabled, settings_json)
        VALUES (?, ?, ?, ?, ?)
        """, (key, name, desc, en, s_json))

    # Boshlang'ich avtomatlashtirish qoidalari
    default_automations = [
        ("Yangi foydalanuvchini kutib olish", "command", "/start", "{}", "send_message", json.dumps({"text": "Assalomu alaykum! Qarshi tibbiyot texnikumi botiga xush kelibsiz."}), 1),
        ("Guruhga yangi a'zo qo'shilganda", "user_join", "any", "{}", "send_message", json.dumps({"text": "Guruhga xush kelibsiz! Qoidalar bilan tanishib chiqing."}), 1)
    ]
    for name, t_type, t_val, cond, a_type, a_payload, act in default_automations:
        cursor.execute("""
        INSERT OR IGNORE INTO automations (name, trigger_type, trigger_value, condition_json, action_type, action_payload_json, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, t_type, t_val, cond, a_type, a_payload, act))

    # Standart birlamchi administrator (admin / atlas2026)
    # Hashlash atlas_auth da tekshiriladi
    from hashlib import pbkdf2_hmac
    salt = "atlas_secure_salt_2026"
    pwd_hash = pbkdf2_hmac('sha256', "atlas2026".encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    
    cursor.execute("""
    INSERT OR IGNORE INTO admins (username, password_hash, salt, full_name, role)
    VALUES (?, ?, ?, ?, ?)
    """, ("admin", pwd_hash, salt, "Bosh Administrator", "superadmin"))

    # Boshlang'ich administratorni users jadvaliga kiritish
    cursor.execute("""
    INSERT OR IGNORE INTO users (telegram_id, username, first_name, last_name, role, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (8135594558, "BoshBuxgalter", "Bosh", "Buxgalter", "admin", "active"))

    conn.commit()
    conn.close()


def _sync_supabase_async(endpoint: str, payload: dict):
    """Supabase Cloud bazasiga fonda avtomatik sinxronlash"""
    import threading
    def _worker():
        try:
            import requests
            supa_url = os.environ.get("SUPABASE_URL", "https://rsrrrkkpvfjyfnzikiiy.supabase.co")
            supa_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY") or os.environ.get("NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY", "")
            if supa_url and supa_key:
                headers = {
                    "apikey": supa_key,
                    "Authorization": f"Bearer {supa_key}",
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal"
                }
                requests.post(f"{supa_url}/rest/v1/{endpoint}", headers=headers, json=payload, timeout=5)
        except Exception:
            pass
    threading.Thread(target=_worker, daemon=True).start()


# Yordamchi DB Funksiyalari
def log_audit(actor: str, module: str, action: str, status: str = "success", details: dict = None, ip: str = None):
    """Audit log qayd qilish (Mahalliy SQLite + Supabase Cloud)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO audit_logs (actor, module, action, status, details_json, ip_address)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (actor, module, action, status, json.dumps(details or {}), ip or ""))
        conn.commit()
        conn.close()

        # Supabase Cloud ga fonda yuborish
        _sync_supabase_async("atlas_audit_logs", {
            "actor": actor,
            "module": module,
            "action": action,
            "status": status,
            "details_json": details or {},
            "ip_address": ip or ""
        })
    except Exception as e:
        print(f"Audit log error: {e}")


def track_user_activity(telegram_id: int, username: str = "", first_name: str = "", last_name: str = ""):
    """Foydalanuvchi faolligini qayd qilish va yangilash (Mahalliy SQLite + Supabase Cloud)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO users (telegram_id, username, first_name, last_name, last_active_at, total_requests)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, 1)
        ON CONFLICT(telegram_id) DO UPDATE SET
            username = CASE WHEN ? != '' THEN ? ELSE username END,
            first_name = CASE WHEN ? != '' THEN ? ELSE first_name END,
            last_name = CASE WHEN ? != '' THEN ? ELSE last_name END,
            last_active_at = CURRENT_TIMESTAMP,
            total_requests = total_requests + 1
        """, (
            telegram_id, username, first_name, last_name,
            username, username,
            first_name, first_name,
            last_name, last_name
        ))
        conn.commit()
        conn.close()

        # Supabase Cloud ga fonda yuborish
        _sync_supabase_async("atlas_users", {
            "telegram_id": telegram_id,
            "username": username or "",
            "first_name": first_name or "",
            "last_name": last_name or "",
            "role": "user",
            "status": "active"
        })
    except Exception as e:
        print(f"Track user error: {e}")


def track_group_activity(telegram_id: int, title: str, username: str = "", group_type: str = "group", members_count: int = 0):
    """Guruh yoki kanal faolligini qayd qilish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO groups (telegram_id, title, username, type, members_count, last_activity_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(telegram_id) DO UPDATE SET
            title = ?,
            username = CASE WHEN ? != '' THEN ? ELSE username END,
            members_count = CASE WHEN ? > 0 THEN ? ELSE members_count END,
            last_activity_at = CURRENT_TIMESTAMP
        """, (
            telegram_id, title, username, group_type, members_count,
            title,
            username, username,
            members_count, members_count
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Track group error: {e}")


def log_generated_document(template_id: str, template_name: str, recipient_fio: str, data: dict, file_type: str = "png", file_path: str = "", created_by: str = "bot"):
    """Yaratilgan hujjatni arxivga qo'shish (Mahalliy SQLite + Supabase Cloud)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO generated_docs (template_id, template_name, recipient_fio, data_json, file_type, file_path, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (template_id, template_name, recipient_fio, json.dumps(data), file_type, file_path, created_by))
        conn.commit()
        conn.close()

        # Supabase Cloud ga fonda yuborish
        _sync_supabase_async("atlas_generated_docs", {
            "template_id": template_id,
            "template_name": template_name,
            "recipient_fio": recipient_fio,
            "data_json": data,
            "file_type": file_type,
            "storage_path": file_path,
            "created_by": created_by
        })
    except Exception as e:
        print(f"Log doc error: {e}")


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
