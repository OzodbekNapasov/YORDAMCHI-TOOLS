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
is_serverless = bool(os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME") or (os.name != 'nt' and os.path.exists("/tmp")))
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

    # 11. O'quv guruhlari (Academic student groups) jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT UNIQUE NOT NULL,
        rahbar_name TEXT,
        course_level INTEGER DEFAULT 1,
        direction TEXT,
        order_num INTEGER DEFAULT 0,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    # Mavjud jadval ustunlarini yangilash
    try: cursor.execute("ALTER TABLE student_groups ADD COLUMN rahbar_name TEXT")
    except: pass
    try: cursor.execute("ALTER TABLE student_groups ADD COLUMN order_num INTEGER DEFAULT 0")
    except: pass

    # 12. Administrator hisob jadvali
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

    # 13. Kontrakt yangilanish sessiyalari jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contract_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT UNIQUE NOT NULL,
        filename TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT,
        total_income REAL DEFAULT 0,
        updated_count INTEGER DEFAULT 0,
        unmatched_count INTEGER DEFAULT 0,
        excel_url TEXT,
        xulosa_url TEXT,
        metrics_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_contract_sessions_created ON contract_sessions(created_at DESC)")

    # Amaliyot Yo'nalishlari Tablari Jadvali (Legacy support)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS amaliyot_tabs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tab_name TEXT NOT NULL,
        direction TEXT,
        duration_years TEXT,
        semester TEXT,
        template_file TEXT,
        order_num INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_amaliyot_tabs_order ON amaliyot_tabs(order_num ASC)")

    # 1. Amaliyot Papkalar Ierarxiyasi (Folders Hierarchy)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS amaliyot_folders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        parent_id INTEGER DEFAULT NULL,
        folder_type TEXT NOT NULL, -- 'year', 'direction', 'groups', 'semester'
        name TEXT NOT NULL,
        extra_data TEXT,           -- JSON: {"duration": "3 yillik", "template_file": "...", "start_date": "...", "end_date": "..."}
        order_num INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (parent_id) REFERENCES amaliyot_folders(id) ON DELETE CASCADE
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_amaliyot_folders_parent ON amaliyot_folders(parent_id, order_num ASC)")

    # 2. Amaliyot So'rovnomasi (Surveys / Student District Distribution)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS amaliyot_surveys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        folder_id INTEGER NOT NULL, -- Semester folder ID
        guruhi TEXT,
        fio TEXT NOT NULL,
        tumani TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT,
        phone TEXT,
        organization TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (folder_id) REFERENCES amaliyot_folders(id) ON DELETE CASCADE
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_amaliyot_surveys_folder ON amaliyot_surveys(folder_id)")

    # 3. Amaliyot Buyruqlari Arxivi (Generated District Orders)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS amaliyot_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        folder_id INTEGER NOT NULL, -- Semester folder ID
        tumani TEXT NOT NULL,
        buyruq_raqami TEXT,
        buyruq_sanasi TEXT,
        shu_tuman_shifokori TEXT,
        oquv_yili TEXT,
        kursi TEXT,
        guruhlar TEXT,
        amaliyot_muddati TEXT,
        start_date TEXT,
        end_date TEXT,
        docx_path TEXT,
        students_count INTEGER DEFAULT 0,
        students_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (folder_id) REFERENCES amaliyot_folders(id) ON DELETE CASCADE
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_amaliyot_orders_folder ON amaliyot_orders(folder_id)")

    # Boshlang'ich Namunaviy Papkalar Ierarxiyasini tekshirish va yaratish
    cursor.execute("SELECT COUNT(*) as cnt FROM amaliyot_folders")
    f_cnt_row = cursor.fetchone()
    if f_cnt_row and f_cnt_row["cnt"] == 0:
        # Level 1: O'quv yili
        cursor.execute("""
        INSERT INTO amaliyot_folders (id, parent_id, folder_type, name, extra_data, order_num)
        VALUES (1, NULL, 'year', '2025/2026', '{}', 1)
        """)
        # Level 2: Yo'nalish
        cursor.execute("""
        INSERT INTO amaliyot_folders (id, parent_id, folder_type, name, extra_data, order_num)
        VALUES (2, 1, 'direction', 'Hamshiralik ishi (3 yillik)', '{"duration":"3 yillik"}', 1)
        """)
        # Level 3: Guruhlar to'plami
        cursor.execute("""
        INSERT INTO amaliyot_folders (id, parent_id, folder_type, name, extra_data, order_num)
        VALUES (3, 2, 'groups', '201-204 guruhlar', '{"groups":["201","202","203","204"]}', 1)
        """)
        cursor.execute("""
        INSERT INTO amaliyot_folders (id, parent_id, folder_type, name, extra_data, order_num)
        VALUES (4, 2, 'groups', '205-guruh', '{"groups":["205"]}', 2)
        """)
        cursor.execute("""
        INSERT INTO amaliyot_folders (id, parent_id, folder_type, name, extra_data, order_num)
        VALUES (5, 2, 'groups', '206-guruh', '{"groups":["206"]}', 3)
        """)
        # Level 4: Semestrlar (201-204 ichida)
        cursor.execute("""
        INSERT INTO amaliyot_folders (id, parent_id, folder_type, name, extra_data, order_num)
        VALUES (6, 3, 'semester', '2-semestr', '{"template_file":"Amaliyot/Hamshiralik ishi - 3 - yillik - 2-semestr/3 yillik 2-semestr.docx","start_date":"08.06.2026","end_date":"06.07.2026","amaliyot_muddati":"2026-yil 08-iyunidan  2026-yil 06-iyuligacha","kursi":"1"}', 1)
        """)
        cursor.execute("""
        INSERT INTO amaliyot_folders (id, parent_id, folder_type, name, extra_data, order_num)
        VALUES (7, 3, 'semester', '3-semestr', '{"kursi":"2"}', 2)
        """)
        cursor.execute("""
        INSERT INTO amaliyot_folders (id, parent_id, folder_type, name, extra_data, order_num)
        VALUES (8, 3, 'semester', '4-semestr', '{"kursi":"2"}', 3)
        """)

        # 2-semestr uchun namunaviy talabalar so'rovnomasi (folder_id = 6)
        demo_survey = [
            ("201", "Rahmatova Shaxnoza Sherzod qizi", "Shahrisabz shahar", "08.06.2026", "06.07.2026", "+998901234567", "Shahrisabz ShTTB Markaziy Shifoxonasi"),
            ("201", "Botirova Gulbahor Olimovna", "Shahrisabz shahar", "08.06.2026", "06.07.2026", "+998912345678", "Shahrisabz ShTTB 1-sonli Poliklinika"),
            ("202", "Asraliyev Asilbek Bekmurod o'g'li", "Kitob tuman", "08.06.2026", "06.07.2026", "+998933456789", "Kitob TTB Markaziy Shifoxonasi"),
            ("202", "Meyliyev Ruslan Rustam o'g'li", "Kitob tuman", "08.06.2026", "06.07.2026", "+998974567890", "Kitob TTB Shoshilinch Bo'limi"),
            ("203", "Nazarova Dilnoza Farxod qizi", "Yakkabog' tuman", "08.06.2026", "06.07.2026", "+998995678901", "Yakkabog' TTB Markaziy Poliklinikasi"),
            ("203", "Qodirov Jasur Anvar o'g'li", "Yakkabog' tuman", "08.06.2026", "06.07.2026", "+998906789012", "Yakkabog' TTB 2-sonli Shifoxonasi"),
            ("204", "Eshmurodov Bobur Shavkat o'g'li", "Chiroqchi tuman", "08.06.2026", "06.07.2026", "+998917890123", "Chiroqchi TTB Markaziy Shifoxonasi"),
            ("204", "Xoliqova Madina Zafar qizi", "Qamashi tuman", "08.06.2026", "06.07.2026", "+998988901234", "Qamashi TTB Markaziy Shifoxonasi"),
            ("204", "Jumanov Sardor Bahodir o'g'li", "Shahrisabz tuman", "08.06.2026", "06.07.2026", "+998909012345", "Shahrisabz Tuman TTB Shifoxonasi")
        ]
        for s_grp, s_fio, s_tum, s_st, s_en, s_ph, s_org in demo_survey:
            cursor.execute("""
            INSERT INTO amaliyot_surveys (folder_id, guruhi, fio, tumani, start_date, end_date, phone, organization)
            VALUES (6, ?, ?, ?, ?, ?, ?, ?)
            """, (s_grp, s_fio, s_tum, s_st, s_en, s_ph, s_org))

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

    # Standart administrator (Ozodbek / Eua5gd007)
    from hashlib import pbkdf2_hmac
    salt = "atlas_secure_salt_2026"
    pwd_hash = pbkdf2_hmac('sha256', "Eua5gd007".encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    
    cursor.execute("""
    INSERT OR REPLACE INTO admins (id, username, password_hash, salt, full_name, role)
    VALUES (1, ?, ?, ?, ?, ?)
    """, ("Ozodbek", pwd_hash, salt, "Ozodbek Napasov", "superadmin"))

    # Boshlang'ich administratorni users jadvaliga kiritish
    cursor.execute("""
    INSERT OR IGNORE INTO users (telegram_id, username, first_name, last_name, role, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (8135594558, "BoshBuxgalter", "Bosh", "Buxgalter", "admin", "active"))

    conn.commit()
    conn.close()


def _get_supabase_credentials():
    supa_url = os.environ.get("SUPABASE_URL", "https://rsrrrkkpvfjyfnzikiiy.supabase.co")
    supa_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY") or os.environ.get("NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY", "")
    if not supa_key:
        env_paths = [".env", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")]
        for ep in env_paths:
            if os.path.exists(ep):
                try:
                    with open(ep, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith("SUPABASE_SERVICE_ROLE_KEY="):
                                supa_key = line.split("=", 1)[1].strip()
                            elif not supa_key and line.startswith("SUPABASE_KEY="):
                                supa_key = line.split("=", 1)[1].strip()
                            elif line.startswith("SUPABASE_URL=") and not os.environ.get("SUPABASE_URL"):
                                supa_url = line.split("=", 1)[1].strip()
                except Exception:
                    pass
    return supa_url, supa_key


def _sync_supabase_async(endpoint: str, payload: dict, method: str = "POST", params: str = ""):
    """Supabase Cloud bazasiga ishonchli sinxronlash (POST, PATCH, DELETE)"""
    try:
        import requests
        supa_url, supa_key = _get_supabase_credentials()
        if supa_url and supa_key:
            headers = {
                "apikey": supa_key,
                "Authorization": f"Bearer {supa_key}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates"
            }
            url = f"{supa_url}/rest/v1/{endpoint}{params}"
            if method.upper() == "POST":
                requests.post(url, headers=headers, json=payload, timeout=4)
            elif method.upper() == "PATCH":
                requests.patch(url, headers=headers, json=payload, timeout=4)
            elif method.upper() == "DELETE":
                requests.delete(url, headers=headers, timeout=4)
    except Exception as e:
        print(f"Supabase sync error for {endpoint}: {e}")


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
    """Telegram guruh yoki kanal faolligini qayd qilish"""
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
def save_generated_document_to_cloud(template_id: str, template_name: str, recipient_fio: str, answers: dict, file_path: str, cdn_url: str = "") -> int:
    """Hujjatni Supabase Cloud bazasiga saqlab, uning haqiqiy global ID raqamini oladi"""
    supa_url, supa_key = _get_supabase_credentials()
    cloud_id = None
    if supa_url and supa_key:
        try:
            import requests
            headers = {
                "apikey": supa_key,
                "Authorization": f"Bearer {supa_key}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
            payload = {
                "template_id": template_id,
                "template_name": template_name,
                "recipient_fio": recipient_fio,
                "data_json": answers,
                "file_type": "png",
                "file_url": cdn_url,
                "storage_path": file_path,
                "created_by": "web_admin"
            }
            res = requests.post(f"{supa_url}/rest/v1/atlas_generated_docs", headers=headers, json=payload, timeout=6)
            if res.status_code in [200, 201]:
                data = res.json()
                if data and isinstance(data, list) and len(data) > 0:
                    cloud_id = data[0].get("id")
        except Exception as se:
            print(f"Supabase create doc error: {se}")

    conn = get_db_connection()
    cursor = conn.cursor()
    if cloud_id:
        cursor.execute("""
        INSERT OR REPLACE INTO generated_docs (id, template_id, template_name, recipient_fio, data_json, file_type, file_path, created_by)
        VALUES (?, ?, ?, ?, ?, 'png', ?, 'web_admin')
        """, (cloud_id, template_id, template_name, recipient_fio, json.dumps(answers), file_path))
        doc_id = cloud_id
    else:
        cursor.execute("""
        INSERT INTO generated_docs (template_id, template_name, recipient_fio, data_json, file_type, file_path, created_by)
        VALUES (?, ?, ?, ?, 'png', ?, 'web_admin')
        """, (template_id, template_name, recipient_fio, json.dumps(answers), file_path))
        doc_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return doc_id


def log_generated_document(template_id: str, template_name: str, recipient_fio: str, data: dict, file_type: str = "png", file_path: str = "", created_by: str = "bot"):
    """Yaratilgan hujjatni arxivga qo'shish"""
    return save_generated_document_to_cloud(template_id, template_name, recipient_fio, data, file_path, "")


def update_generated_document(doc_id: int, recipient_fio: str, data: dict, file_path: str = ""):
    """Tahrirlangan hujjatni arxivda yangilash (Mahalliy SQLite + Supabase Cloud)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE generated_docs
        SET recipient_fio = ?, data_json = ?, file_path = CASE WHEN ? != '' THEN ? ELSE file_path END
        WHERE id = ?
        """, (recipient_fio, json.dumps(data), file_path, file_path, doc_id))
        conn.commit()
        conn.close()

        # Supabase Cloud-da yangilash
        _sync_supabase_async("atlas_generated_docs", {
            "recipient_fio": recipient_fio,
            "data_json": data,
            "storage_path": file_path
        }, method="PATCH", params=f"?id=eq.{doc_id}")
        return True
    except Exception as e:
        print(f"Update doc error: {e}")
        return False


def get_saved_documents(q: str = "", template_id: str = "", limit: int = 100, offset: int = 0):
    """Barcha saqlangan hujjatlarni olish (SQLite + Supabase Cloud avtomatik yuklash)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM generated_docs WHERE 1=1"
        params = []
        if q:
            query += " AND (recipient_fio LIKE ? OR data_json LIKE ?)"
            params.extend([f"%{q}%", f"%{q}%"])
        if template_id:
            query += " AND template_id = ?"
            params.append(template_id)
        query += " ORDER BY id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        cursor.execute(query, params)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        if rows:
            for r in rows:
                try:
                    r["parsed_data"] = json.loads(r.get("data_json") or "{}") if isinstance(r.get("data_json"), str) else r.get("data_json") or {}
                except Exception:
                    r["parsed_data"] = {}
            return rows
    except Exception as e:
        print(f"Sqlite get docs error: {e}")

    # Agar SQLite bo'sh bo'lsa (Serverless konteyner yangilanganda), Supabase Cloud'dan yuklash
    try:
        import requests
        supa_url, supa_key = _get_supabase_credentials()
        if supa_url and supa_key:
            headers = {
                "apikey": supa_key,
                "Authorization": f"Bearer {supa_key}"
            }
            url = f"{supa_url}/rest/v1/atlas_generated_docs?select=*&order=id.desc&limit={limit}&offset={offset}"
            if template_id:
                url += f"&template_id=eq.{template_id}"
            if q:
                url += f"&recipient_fio=ilike.*{q}*"
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                cloud_docs = resp.json()
                if cloud_docs:
                    try:
                        conn = get_db_connection()
                        c = conn.cursor()
                        for d in cloud_docs:
                            d_json = json.dumps(d.get("data_json") or {}) if isinstance(d.get("data_json"), dict) else str(d.get("data_json") or "{}")
                            c.execute("""
                            INSERT OR REPLACE INTO generated_docs (id, template_id, template_name, recipient_fio, data_json, file_type, file_path, created_by, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                d.get("id"),
                                d.get("template_id"),
                                d.get("template_name"),
                                d.get("recipient_fio"),
                                d_json,
                                d.get("file_type", "png"),
                                d.get("storage_path") or d.get("file_url") or "",
                                d.get("created_by", "web_admin"),
                                d.get("created_at")
                            ))
                        conn.commit()
                        conn.close()
                    except Exception as cache_err:
                        print(f"Cache docs error: {cache_err}")

                    for cd in cloud_docs:
                        cd["parsed_data"] = cd.get("data_json") or {}
                    return cloud_docs
    except Exception as se:
        print(f"Supabase fetch docs error: {se}")

    return []


def get_document_by_id(doc_id: int):
    """Bitta hujjatni ID bo'yicha olish (SQLite + Supabase Cloud fallback)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM generated_docs WHERE id = ?", (doc_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            d = dict(row)
            try:
                d["parsed_data"] = json.loads(d.get("data_json") or "{}") if isinstance(d.get("data_json"), str) else d.get("data_json") or {}
            except Exception:
                d["parsed_data"] = {}
            return d
    except Exception as e:
        print(f"Get doc by id sqlite error: {e}")

    try:
        import requests
        supa_url, supa_key = _get_supabase_credentials()
        if supa_url and supa_key:
            headers = {
                "apikey": supa_key,
                "Authorization": f"Bearer {supa_key}"
            }
            resp = requests.get(f"{supa_url}/rest/v1/atlas_generated_docs?id=eq.{doc_id}&select=*", headers=headers, timeout=5)
            if resp.status_code == 200:
                results = resp.json()
                if results:
                    d = results[0]
                    d["parsed_data"] = d.get("data_json") or {}
                    return d
    except Exception as se:
        print(f"Get doc by id supabase error: {se}")

    return None


# O'quv Guruhlari (Academic Student Groups) Boshqaruvi
def get_student_groups():
    """Barcha o'quv guruhlarini tartib bo'yicha olish (SQLite + Supabase Cloud fallback)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student_groups ORDER BY order_num ASC, group_name ASC")
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        if rows:
            return rows
    except Exception as e:
        print(f"Get student groups sqlite error: {e}")

    # Agar SQLite bo'sh bo'lsa (Serverless / Yangi konteynerda), Supabase Cloud'dan o'qib kelish:
    try:
        import requests
        supa_url, supa_key = _get_supabase_credentials()
        if supa_url and supa_key:
            headers = {
                "apikey": supa_key,
                "Authorization": f"Bearer {supa_key}"
            }
            resp = requests.get(f"{supa_url}/rest/v1/atlas_student_groups?select=*", headers=headers, timeout=5)
            if resp.status_code == 200:
                cloud_groups = resp.json()
                if cloud_groups:
                    for g in cloud_groups:
                        notes_val = g.get('notes')
                        if notes_val:
                            try:
                                n_dict = json.loads(notes_val) if isinstance(notes_val, str) else notes_val
                                if isinstance(n_dict, dict):
                                    if not g.get('rahbar_name'):
                                        g['rahbar_name'] = n_dict.get('rahbar', '')
                                    if not g.get('order_num'):
                                        g['order_num'] = int(n_dict.get('order', 0))
                            except Exception:
                                if not g.get('rahbar_name'):
                                    g['rahbar_name'] = str(notes_val)
                        if not g.get('order_num'):
                            g['order_num'] = 0
                        if not g.get('rahbar_name'):
                            g['rahbar_name'] = ''

                    cloud_groups.sort(key=lambda x: (int(x.get('order_num') or 0), int(x.get('course_level') or 1), str(x.get('group_name') or '')))

                    # Local SQLite ga keshlab qo'yish
                    try:
                        conn = get_db_connection()
                        c = conn.cursor()
                        for g in cloud_groups:
                            c.execute("""
                            INSERT OR REPLACE INTO student_groups (id, group_name, rahbar_name, course_level, direction, order_num)
                            VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                g.get('id'),
                                g.get('group_name'),
                                g.get('rahbar_name', ''),
                                g.get('course_level', 1),
                                g.get('direction', ''),
                                g.get('order_num', 0)
                            ))
                        conn.commit()
                        conn.close()
                    except Exception:
                        pass
                return cloud_groups
    except Exception as se:
        print(f"Supabase fetch groups error: {se}")

    return []


def bulk_add_student_groups(items_data):
    """
    Foydalanuvchi tomonidan kiritilgan guruhlarni (Guruh nomi, Rahbari, Kursi va Ketma-ketligi)
    tahlil qilib, SQLite va Supabase Cloud bazasiga to'liq saqlaydi.
    """
    if not items_data:
        return {"added": 0, "skipped": 0, "total": 0}

    import re
    parsed_items = []

    if isinstance(items_data, list):
        for idx, itm in enumerate(items_data):
            if isinstance(itm, dict) and itm.get('group_name'):
                parsed_items.append({
                    "group_name": str(itm.get('group_name')).strip(),
                    "rahbar_name": str(itm.get('rahbar_name', '')).strip(),
                    "course_level": int(itm.get('course_level') or 1),
                    "direction": str(itm.get('direction', '')).strip(),
                    "order_num": int(itm.get('order_num') or (idx + 1))
                })
    elif isinstance(items_data, str):
        lines = [line.strip() for line in items_data.splitlines() if line.strip()]
        for idx, line in enumerate(lines):
            parts = []
            if "\t" in line:
                parts = [p.strip() for p in line.split("\t") if p.strip()]
            elif "," in line:
                parts = [p.strip() for p in line.split(",") if p.strip()]
            elif " - " in line or " – " in line:
                parts = [p.strip() for p in re.split(r'\s+[-–—]\s+', line) if p.strip()]
            else:
                parts = line.split()

            if not parts: continue
            g_name = parts[0].strip()
            if g_name.endswith('.0'): g_name = g_name[:-2]

            rahbar = ""
            course = 1

            m = re.search(r'([1-4])\d{2}', g_name)
            if m:
                course = int(m.group(1))
            elif g_name.startswith('24-'):
                course = 2
            elif g_name.startswith('25-'):
                course = 1

            if len(parts) >= 2:
                p2 = parts[1].replace("-kurs", "").replace("kurs", "").strip()
                if p2.isdigit():
                    course = int(p2)
                    if len(parts) >= 3:
                        rahbar = " ".join(parts[2:])
                else:
                    rahbar = parts[1]
                    if len(parts) >= 3:
                        p3 = parts[2].replace("-kurs", "").replace("kurs", "").strip()
                        if p3.isdigit():
                            course = int(p3)

            parsed_items.append({
                "group_name": g_name,
                "rahbar_name": rahbar,
                "course_level": course,
                "direction": "",
                "order_num": idx + 1
            })

    added = 0
    skipped = 0

    conn = get_db_connection()
    cursor = conn.cursor()

    for item in parsed_items:
        g_name = item["group_name"]
        rahbar = item["rahbar_name"]
        course = item["course_level"]
        order_num = item["order_num"]
        direction = item["direction"]

        try:
            cursor.execute("""
            INSERT INTO student_groups (group_name, rahbar_name, course_level, direction, order_num)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(group_name) DO UPDATE SET
                rahbar_name = excluded.rahbar_name,
                course_level = excluded.course_level,
                order_num = excluded.order_num
            """, (g_name, rahbar, course, direction, order_num))
            added += 1

            # Supabase Cloud ga saqlash
            notes_json = json.dumps({"rahbar": rahbar, "order": order_num})
            _sync_supabase_async("atlas_student_groups", {
                "group_name": g_name,
                "course_level": course,
                "direction": direction,
                "notes": notes_json
            }, method="POST", params="?on_conflict=group_name")
        except Exception as e:
            print(f"Error inserting group {g_name}: {e}")
            skipped += 1

    conn.commit()
    conn.close()
    return {"added": added, "skipped": skipped, "total": len(parsed_items)}


def delete_student_group(group_id: int):
    """O'quv guruhini o'chirish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student_groups WHERE id = ?", (group_id,))
        conn.commit()
        conn.close()

        # Supabase-dan o'chirish
        _sync_supabase_async("atlas_student_groups", {}, method="DELETE", params=f"?id=eq.{group_id}")
        return True
    except Exception as e:
        print(f"Delete group error: {e}")
        return False


def update_student_group(group_id: int, group_name: str, course_level: int, rahbar_name: str = "", order_num: int = 0):
    """O'quv guruhini tahrirlash (nomi, rahbari, kursi va ketma-ketligi)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE student_groups
               SET group_name = ?, course_level = ?, rahbar_name = ?, order_num = ?
               WHERE id = ?""",
            (group_name, course_level, rahbar_name, order_num, group_id)
        )
        conn.commit()
        conn.close()

        # Supabase-ga sinxronlash
        notes_json = json.dumps({"rahbar": rahbar_name, "order": order_num})
        _sync_supabase_async("atlas_student_groups", {
            "group_name": group_name,
            "course_level": course_level,
            "notes": notes_json
        }, method="PATCH", params=f"?id=eq.{group_id}")
        return True
    except Exception as e:
        print(f"Update group error: {e}")
        return False



# Kontrakt Yangilanish Sessiyalari Boshqaruvi
def log_contract_session(session_id: str, filename: str, start_date: str, end_date: str, total_income: float, updated_count: int, unmatched_count: int, excel_url: str = "", xulosa_url: str = "", metrics: dict = None):
    """Kontrakt yangilanish sessiyasini bazaga va Supabase Cloud-ga qayd qilish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO contract_sessions (session_id, filename, start_date, end_date, total_income, updated_count, unmatched_count, excel_url, xulosa_url, metrics_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (session_id, filename, start_date, end_date, total_income, updated_count, unmatched_count, excel_url, xulosa_url, json.dumps(metrics or {})))
        conn.commit()
        conn.close()

        # Supabase Cloud ga sinxronlash
        _sync_supabase_async("atlas_contract_sessions", {
            "session_id": session_id,
            "filename": filename,
            "start_date": start_date,
            "end_date": end_date,
            "total_income": total_income,
            "updated_count": updated_count,
            "unmatched_count": unmatched_count,
            "excel_url": excel_url,
            "xulosa_url": xulosa_url,
            "metrics_json": metrics or {}
        })
        return True
    except Exception as e:
        print(f"Log contract session error: {e}")
        return False


def get_contract_sessions():
    """Barcha kontrakt yangilanish sessiyalari tarixini olish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contract_sessions ORDER BY created_at DESC LIMIT 100")
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        for r in rows:
            if r.get("metrics_json"):
                try:
                    r["metrics"] = json.loads(r["metrics_json"])
                except:
                    r["metrics"] = {}
        return rows
    except Exception as e:
        print(f"Get contract sessions error: {e}")
        return []


def get_contract_session_by_id(session_id: str):
    """Sessiya ID bo'yicha ma'lumot olish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contract_sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            res = dict(row)
            if res.get("metrics_json"):
                try:
                    res["metrics"] = json.loads(res["metrics_json"])
                except:
                    res["metrics"] = {}
            return res
        return None
    except Exception as e:
        print(f"Get contract session by id error: {e}")
        return None


def delete_contract_session(session_id: str):
    """Kontrakt sessiyasini o'chirish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contract_sessions WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()

        # Supabase Cloud-dan o'chirish
        _sync_supabase_async("atlas_contract_sessions", {}, method="DELETE", params=f"?session_id=eq.{session_id}")
        return True
    except Exception as e:
        print(f"Delete contract session error: {e}")
        return False


# ============================================================
# AMALIYOT TABLARI VA BUYRUQLARI BOSHQARUVI
# ============================================================

def get_amaliyot_tabs():
    """Barcha amaliyot tablarini tartiblangan holda olish (SQLite + Supabase Cloud fallback)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM amaliyot_tabs ORDER BY order_num ASC, id ASC")
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        if rows:
            return rows
    except Exception as e:
        print(f"Get amaliyot tabs sqlite error: {e}")

    try:
        import requests
        supa_url, supa_key = _get_supabase_credentials()
        if supa_url and supa_key:
            headers = {
                "apikey": supa_key,
                "Authorization": f"Bearer {supa_key}"
            }
            resp = requests.get(f"{supa_url}/rest/v1/atlas_amaliyot_tabs?select=*&order=order_num.asc,id.asc", headers=headers, timeout=5)
            if resp.status_code == 200:
                cloud_tabs = resp.json()
                if cloud_tabs:
                    try:
                        conn = get_db_connection()
                        c = conn.cursor()
                        for t in cloud_tabs:
                            c.execute("""
                            INSERT OR REPLACE INTO amaliyot_tabs (id, tab_name, direction, duration_years, semester, template_file, order_num)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (
                                t.get("id"),
                                t.get("tab_name"),
                                t.get("direction", ""),
                                t.get("duration_years", ""),
                                t.get("semester", ""),
                                t.get("template_file", ""),
                                t.get("order_num", 0)
                            ))
                        conn.commit()
                        conn.close()
                    except Exception:
                        pass
                    return cloud_tabs
    except Exception as se:
        print(f"Supabase fetch amaliyot tabs error: {se}")

    # Standart boshlang'ich tab
    return [{
        "id": 1,
        "tab_name": "Hamshiralik ishi - 3 yillik - 2-semestr",
        "direction": "Hamshiralik ishi",
        "duration_years": "3 yillik",
        "semester": "2-semestr",
        "template_file": "Amaliyot/Hamshiralik ishi - 3 - yillik - 2-semestr/3 yillik 2-semestr.docx",
        "order_num": 1
    }]


def create_amaliyot_tab(tab_name: str, direction: str = "", duration_years: str = "", semester: str = "", template_file: str = "", order_num: int = 0):
    """Yangi amaliyot tabini qo'shish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if order_num == 0:
            cursor.execute("SELECT COALESCE(MAX(order_num), 0) + 1 FROM amaliyot_tabs")
            order_num = cursor.fetchone()[0]

        cursor.execute("""
        INSERT INTO amaliyot_tabs (tab_name, direction, duration_years, semester, template_file, order_num)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (tab_name, direction, duration_years, semester, template_file, order_num))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Supabase Cloud-ga saqlash
        _sync_supabase_async("atlas_amaliyot_tabs", {
            "id": new_id,
            "tab_name": tab_name,
            "direction": direction,
            "duration_years": duration_years,
            "semester": semester,
            "template_file": template_file,
            "order_num": order_num
        }, method="POST", params="?on_conflict=id")

        return {"success": True, "id": new_id, "tab_name": tab_name}
    except Exception as e:
        print(f"Create amaliyot tab error: {e}")
        return {"success": False, "error": str(e)}


def update_amaliyot_tab(tab_id: int, tab_name: str, direction: str = "", duration_years: str = "", semester: str = "", template_file: str = ""):
    """Amaliyot tabini tahrirlash"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE amaliyot_tabs
        SET tab_name = ?, direction = ?, duration_years = ?, semester = ?, template_file = CASE WHEN ? != '' THEN ? ELSE template_file END
        WHERE id = ?
        """, (tab_name, direction, duration_years, semester, template_file, template_file, tab_id))
        conn.commit()
        conn.close()

        # Supabase Cloud-da yangilash
        _sync_supabase_async("atlas_amaliyot_tabs", {
            "tab_name": tab_name,
            "direction": direction,
            "duration_years": duration_years,
            "semester": semester
        }, method="PATCH", params=f"?id=eq.{tab_id}")

        return {"success": True}
    except Exception as e:
        print(f"Update amaliyot tab error: {e}")
        return {"success": False, "error": str(e)}


def delete_amaliyot_tab(tab_id: int):
    """Amaliyot tabini o'chirish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM amaliyot_tabs WHERE id = ?", (tab_id,))
        conn.commit()
        conn.close()

        # Supabase Cloud-dan o'chirish
        _sync_supabase_async("atlas_amaliyot_tabs", {}, method="DELETE", params=f"?id=eq.{tab_id}")
        return {"success": True}
    except Exception as e:
        print(f"Delete amaliyot tab error: {e}")
        return {"success": False, "error": str(e)}


def reorder_amaliyot_tabs(tab_orders: list):
    """Amaliyot tablari tartibini yangilash (Drag & Drop / O'rin almashtirish)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for item in tab_orders:
            t_id = item.get("id")
            o_num = item.get("order_num")
            if t_id is not None and o_num is not None:
                cursor.execute("UPDATE amaliyot_tabs SET order_num = ? WHERE id = ?", (o_num, t_id))
                _sync_supabase_async("atlas_amaliyot_tabs", {"order_num": o_num}, method="PATCH", params=f"?id=eq.{t_id}")
        conn.commit()
        conn.close()
        return {"success": True}
    except Exception as e:
        print(f"Reorder amaliyot tabs error: {e}")
        return {"success": False, "error": str(e)}


# ============================================================
# AMALIYOT PAPKALAR IERARXIYASI (FOLDERS HIERARCHY)
# ============================================================

def get_amaliyot_folder_contents(parent_id=None):
    """Berilgan parent_id ostidagi barcha papkalar ro'yxatini qaytaradi"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if parent_id is None or parent_id == 0:
            cursor.execute("SELECT * FROM amaliyot_folders WHERE parent_id IS NULL ORDER BY order_num ASC, id ASC")
        else:
            cursor.execute("SELECT * FROM amaliyot_folders WHERE parent_id = ? ORDER BY order_num ASC, id ASC", (parent_id,))

        rows = cursor.fetchall()
        folders = []
        for r in rows:
            f = dict(r)
            try:
                f["extra_data"] = json.loads(f["extra_data"]) if f.get("extra_data") else {}
            except Exception:
                f["extra_data"] = {}

            # Bolalar sonini yoki semestr statistikasini hisoblash
            if f.get("folder_type") == "semester":
                cursor.execute("SELECT COUNT(*) as cnt FROM amaliyot_surveys WHERE folder_id = ?", (f["id"],))
                f["survey_count"] = cursor.fetchone()["cnt"]
                cursor.execute("SELECT COUNT(*) as cnt FROM amaliyot_orders WHERE folder_id = ?", (f["id"],))
                f["orders_count"] = cursor.fetchone()["cnt"]
            else:
                cursor.execute("SELECT COUNT(*) as cnt FROM amaliyot_folders WHERE parent_id = ?", (f["id"],))
                f["children_count"] = cursor.fetchone()["cnt"]

            folders.append(f)

        conn.close()
        return {"success": True, "folders": folders}
    except Exception as e:
        print(f"Get amaliyot folder contents error: {e}")
        return {"success": False, "error": str(e), "folders": []}


def get_amaliyot_folder_path(folder_id: int):
    """Papkaning ildizidan to o'zigacha bo'lgan yo'lini (Breadcrumb) qaytaradi"""
    if not folder_id:
        return {"success": True, "path": []}

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        path = []
        current_id = folder_id

        while current_id:
            cursor.execute("SELECT id, parent_id, folder_type, name, extra_data FROM amaliyot_folders WHERE id = ?", (current_id,))
            row = cursor.fetchone()
            if not row:
                break
            f_dict = dict(row)
            try:
                f_dict["extra_data"] = json.loads(f_dict["extra_data"]) if f_dict.get("extra_data") else {}
            except Exception:
                f_dict["extra_data"] = {}

            path.insert(0, f_dict)
            current_id = f_dict.get("parent_id")

        conn.close()
        return {"success": True, "path": path}
    except Exception as e:
        print(f"Get amaliyot folder path error: {e}")
        return {"success": False, "error": str(e), "path": []}


def get_amaliyot_folder(folder_id: int):
    """Bitta papka ma'lumotlarini olish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM amaliyot_folders WHERE id = ?", (folder_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            f = dict(row)
            try:
                f["extra_data"] = json.loads(f["extra_data"]) if f.get("extra_data") else {}
            except Exception:
                f["extra_data"] = {}
            return f
        return None
    except Exception as e:
        print(f"Get amaliyot folder error: {e}")
        return None


def create_amaliyot_folder(parent_id, folder_type: str, name: str, extra_data: dict = None):
    """Yangi papka yaratish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if parent_id is None or parent_id == 0:
            cursor.execute("SELECT COALESCE(MAX(order_num), 0) + 1 FROM amaliyot_folders WHERE parent_id IS NULL")
            p_val = None
        else:
            cursor.execute("SELECT COALESCE(MAX(order_num), 0) + 1 FROM amaliyot_folders WHERE parent_id = ?", (parent_id,))
            p_val = parent_id

        next_order = cursor.fetchone()[0]
        extra_json = json.dumps(extra_data or {}, ensure_ascii=False)

        cursor.execute("""
        INSERT INTO amaliyot_folders (parent_id, folder_type, name, extra_data, order_num)
        VALUES (?, ?, ?, ?, ?)
        """, (p_val, folder_type, name, extra_json, next_order))
        new_id = cursor.lastrowid

        conn.commit()
        conn.close()
        return {"success": True, "id": new_id}
    except Exception as e:
        print(f"Create amaliyot folder error: {e}")
        return {"success": False, "error": str(e)}


def update_amaliyot_folder(folder_id: int, name: str, extra_data: dict = None):
    """Papka nomi yoki qo'shimcha parametrlarini yangilash"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if extra_data is not None:
            extra_json = json.dumps(extra_data, ensure_ascii=False)
            cursor.execute("UPDATE amaliyot_folders SET name = ?, extra_data = ? WHERE id = ?", (name, extra_json, folder_id))
        else:
            cursor.execute("UPDATE amaliyot_folders SET name = ? WHERE id = ?", (name, folder_id))

        conn.commit()
        conn.close()
        return {"success": True}
    except Exception as e:
        print(f"Update amaliyot folder error: {e}")
        return {"success": False, "error": str(e)}


def delete_amaliyot_folder(folder_id: int):
    """Papka va uning barcha ichki bolalari, so'rovnomalari va buyruqlarini rekursiv o'chirish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Rekursiv barcha bolalar ID larini yig'ish
        to_delete_ids = [folder_id]
        idx = 0
        while idx < len(to_delete_ids):
            cur_p = to_delete_ids[idx]
            cursor.execute("SELECT id FROM amaliyot_folders WHERE parent_id = ?", (cur_p,))
            children = cursor.fetchall()
            for ch in children:
                to_delete_ids.append(ch["id"])
            idx += 1

        for fid in to_delete_ids:
            cursor.execute("DELETE FROM amaliyot_surveys WHERE folder_id = ?", (fid,))
            cursor.execute("DELETE FROM amaliyot_orders WHERE folder_id = ?", (fid,))
            cursor.execute("DELETE FROM amaliyot_folders WHERE id = ?", (fid,))

        conn.commit()
        conn.close()
        return {"success": True, "deleted_count": len(to_delete_ids)}
    except Exception as e:
        print(f"Delete amaliyot folder error: {e}")
        return {"success": False, "error": str(e)}


# ============================================================
# AMALIYOT SO'ROVNOMASI (SURVEYS) BOSHQARUVI
# ============================================================

def get_amaliyot_surveys(folder_id: int):
    """Semestr papkasi bo'yicha talabalar so'rovnomasi ro'yxatini olish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM amaliyot_surveys
        WHERE folder_id = ?
        ORDER BY id ASC
        """, (folder_id,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return {"success": True, "surveys": rows}
    except Exception as e:
        print(f"Get amaliyot surveys error: {e}")
        return {"success": False, "error": str(e), "surveys": []}


def save_amaliyot_surveys(folder_id: int, students_list: list, replace_all: bool = True):
    """Talabalar so'rovnomasini ommaviy saqlash"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if replace_all:
            cursor.execute("DELETE FROM amaliyot_surveys WHERE folder_id = ?", (folder_id,))

        for st in students_list:
            fio = st.get("fio", "").strip()
            if not fio:
                continue
            guruhi = st.get("guruhi", "").strip()
            tumani = st.get("tumani", "").strip() or "Shahrisabz shahar"
            start_date = st.get("start_date", "").strip() or "08.06.2026"
            end_date = st.get("end_date", "").strip() or "06.07.2026"
            phone = st.get("phone", "").strip()
            organization = st.get("organization", "").strip()
            notes = st.get("notes", "").strip()

            cursor.execute("""
            INSERT INTO amaliyot_surveys (folder_id, guruhi, fio, tumani, start_date, end_date, phone, organization, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (folder_id, guruhi, fio, tumani, start_date, end_date, phone, organization, notes))

        conn.commit()
        conn.close()
        return {"success": True, "count": len(students_list)}
    except Exception as e:
        print(f"Save amaliyot surveys error: {e}")
        return {"success": False, "error": str(e)}


def add_amaliyot_survey_item(folder_id: int, st: dict):
    """Bitta so'rovnoma qatorini qo'shish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO amaliyot_surveys (folder_id, guruhi, fio, tumani, start_date, end_date, phone, organization, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            folder_id,
            st.get("guruhi", "").strip(),
            st.get("fio", "").strip(),
            st.get("tumani", "").strip() or "Shahrisabz shahar",
            st.get("start_date", "08.06.2026").strip(),
            st.get("end_date", "06.07.2026").strip(),
            st.get("phone", "").strip(),
            st.get("organization", "").strip(),
            st.get("notes", "").strip()
        ))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return {"success": True, "id": new_id}
    except Exception as e:
        print(f"Add amaliyot survey item error: {e}")
        return {"success": False, "error": str(e)}


def delete_amaliyot_survey_item(survey_id: int):
    """Bitta so'rovnoma qatorini o'chirish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM amaliyot_surveys WHERE id = ?", (survey_id,))
        conn.commit()
        conn.close()
        return {"success": True}
    except Exception as e:
        print(f"Delete amaliyot survey item error: {e}")
        return {"success": False, "error": str(e)}


# ============================================================
# AMALIYOT BUYRUQLARI (ORDERS) BOSHQARUVI
# ============================================================

def get_amaliyot_orders(folder_id: int):
    """Semestr papkasi bo'yicha shakllantirilgan buyruqlar ro'yxatini olish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM amaliyot_orders
        WHERE folder_id = ?
        ORDER BY created_at DESC, id DESC
        """, (folder_id,))
        rows = []
        for r in cursor.fetchall():
            item = dict(r)
            try:
                item["students"] = json.loads(item["students_json"]) if item.get("students_json") else []
            except Exception:
                item["students"] = []
            rows.append(item)
        conn.close()
        return {"success": True, "orders": rows}
    except Exception as e:
        print(f"Get amaliyot orders error: {e}")
        return {"success": False, "error": str(e), "orders": []}


def save_amaliyot_order_record(folder_id: int, data: dict):
    """Shakllantirilgan buyruqni arxivga yozish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        students = data.get("students", [])
        students_json = json.dumps(students, ensure_ascii=False)
        raw_guruhlar = data.get("guruhlar", [])
        guruhlar_str = ", ".join(raw_guruhlar) if isinstance(raw_guruhlar, list) else str(raw_guruhlar)

        cursor.execute("""
        INSERT INTO amaliyot_orders (
            folder_id, tumani, buyruq_raqami, buyruq_sanasi, shu_tuman_shifokori,
            oquv_yili, kursi, guruhlar, amaliyot_muddati, start_date, end_date,
            docx_path, students_count, students_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            folder_id,
            data.get("tumani", "").strip(),
            data.get("buyruq_raqami", "").strip(),
            data.get("buyruq_sanasi", "").strip(),
            data.get("shu_tuman_shifokori", "").strip(),
            data.get("oquv_yili", "2025/2026").strip(),
            str(data.get("kursi", "1")).strip(),
            guruhlar_str,
            data.get("amaliyot_muddati", "").strip(),
            data.get("start_date", "").strip(),
            data.get("end_date", "").strip(),
            data.get("docx_path", "").strip(),
            len(students),
            students_json
        ))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return {"success": True, "id": new_id}
    except Exception as e:
        print(f"Save amaliyot order record error: {e}")
        return {"success": False, "error": str(e)}


def delete_amaliyot_order_record(order_id: int):
    """Arxivdagi buyruqni o'chirish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM amaliyot_orders WHERE id = ?", (order_id,))
        conn.commit()
        conn.close()
        return {"success": True}
    except Exception as e:
        print(f"Delete amaliyot order record error: {e}")
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)

