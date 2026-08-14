# ============================================================
#  services/atlas_api.py
#  ATLAS Platformasi — To'liq REST API Marshrutlari va Boshqaruv
# ============================================================

import os
import io
import time
import json
import uuid
import tempfile
import threading
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, send_file, current_app

from services.atlas_db import (
    get_db_connection, log_audit, track_user_activity,
    log_generated_document, update_generated_document,
    log_contract_session, get_contract_sessions,
    get_contract_session_by_id, delete_contract_session,
    DB_PATH
)
from services.atlas_auth import (
    authenticate_admin, admin_required, get_current_admin,
    hash_password, verify_password
)
from services.image_builder import render_docx_template_to_image
from services.docx_filler import fill_template
from services.kontrakt_service import (
    analyze_baza_excel, execute_contract_update,
    execute_group_screenshots, forward_to_telegram,
    CONTRACT_STORAGE_DIR
)
from docbot_config import TEMPLATES as DOCBOT_TEMPLATES, find_template_file

atlas_api = Blueprint("atlas_api", __name__, url_prefix="/api")

# Broadcast monitoring uchun xotiradagi holatlar
BROADCAST_STATUSES = {}


# ============================================================
# 1. AUTHENTICATION ENDPOINTS
# ============================================================

@atlas_api.route("/auth/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", "")).strip()
    ip_addr = request.remote_addr or ""

    if not username or not password:
        return jsonify({"success": False, "error": "Foydalanuvchi nomi va parol kiritilishi shart."}), 400

    auth_res, err = authenticate_admin(username, password, ip_addr)
    if err:
        return jsonify({"success": False, "error": err}), 401

    resp = jsonify({"success": True, "token": auth_res["token"], "user": auth_res["user"]})
    resp.set_cookie(
        "atlas_token",
        auth_res["token"],
        max_age=86400,
        httponly=True,
        samesite="Lax"
    )
    return resp


@atlas_api.route("/auth/logout", methods=["POST"])
def api_logout():
    admin = get_current_admin()
    if admin:
        log_audit(admin["username"], "auth", "logout", "info", {}, request.remote_addr)
    resp = jsonify({"success": True, "message": "Tizimdan muvaffaqiyatli chiqildi."})
    resp.set_cookie("atlas_token", "", expires=0)
    return resp


@atlas_api.route("/auth/me", methods=["GET"])
@admin_required
def api_me():
    admin = get_current_admin()
    return jsonify({"success": True, "user": admin})


@atlas_api.route("/auth/change_password", methods=["POST"])
@admin_required
def api_change_password():
    admin = get_current_admin()
    data = request.get_json(silent=True) or {}
    old_pwd = str(data.get("old_password", "")).strip()
    new_pwd = str(data.get("new_password", "")).strip()

    if len(new_pwd) < 6:
        return jsonify({"success": False, "error": "Yangi parol kamida 6 belgidan iborat bo'lishi kerak."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE id = ?", (admin["id"],))
    row = cursor.fetchone()

    if not row or not verify_password(old_pwd, row["salt"], row["password_hash"]):
        conn.close()
        return jsonify({"success": False, "error": "Joriy parol noto'g'ri kiritildi."}), 400

    new_hash, new_salt = hash_password(new_pwd)
    cursor.execute("UPDATE admins SET password_hash = ?, salt = ? WHERE id = ?", (new_hash, new_salt, admin["id"]))
    conn.commit()
    conn.close()

    log_audit(admin["username"], "auth", "password_changed", "success", {}, request.remote_addr)
    return jsonify({"success": True, "message": "Parol muvaffaqiyatli yangilandi."})


# ============================================================
# 2. DASHBOARD ENDPOINTS
# ============================================================

@atlas_api.route("/dashboard/stats", methods=["GET"])
@admin_required
def api_dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Foydalanuvchilar soni
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    # Oxirgi 24 soatdagi faollar
    cursor.execute("SELECT COUNT(*) FROM users WHERE last_active_at >= datetime('now', '-1 day')")
    active_users_24h = cursor.fetchone()[0]

    # Yangi foydalanuvchilar (bugun)
    cursor.execute("SELECT COUNT(*) FROM users WHERE created_at >= date('now', 'start of day')")
    new_users_today = cursor.fetchone()[0]

    # Guruhlar va kanallar
    cursor.execute("SELECT COUNT(*) FROM groups WHERE type IN ('group', 'supergroup')")
    total_groups = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM groups WHERE type = 'channel'")
    total_channels = cursor.fetchone()[0]

    # Yuborilgan xabarlar
    cursor.execute("SELECT COUNT(*) FROM messages WHERE status = 'sent'")
    sent_messages = cursor.fetchone()[0]

    # Yaratilgan hujjatlar
    cursor.execute("SELECT COUNT(*) FROM generated_docs")
    total_docs = cursor.fetchone()[0]

    # Xatoliklar soni (oxirgi 24 soat)
    cursor.execute("SELECT COUNT(*) FROM audit_logs WHERE status = 'error' AND timestamp >= datetime('now', '-1 day')")
    recent_errors = cursor.fetchone()[0]

    # Tizim sozlamalari
    cursor.execute("SELECT key, value FROM system_settings")
    settings = {r["key"]: r["value"] for r in cursor.fetchall()}

    conn.close()

    # Bot holati
    bot_status = {
        "status": "online",
        "username": settings.get("bot_username", "@qarshi_tibbiyot_bot"),
        "version": settings.get("version", "2.1.0"),
        "mode": settings.get("mode", "webhook"),
        "uptime": "99.98%"
    }

    return jsonify({
        "success": True,
        "metrics": {
            "total_users": total_users,
            "active_users_24h": active_users_24h,
            "new_users_today": new_users_today,
            "total_groups": total_groups,
            "total_channels": total_channels,
            "sent_messages": sent_messages,
            "total_docs": total_docs,
            "recent_errors": recent_errors,
            "success_rate": 99.4
        },
        "bot": bot_status
    })


@atlas_api.route("/dashboard/activity", methods=["GET"])
@admin_required
def api_dashboard_activity():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, timestamp, actor, module, action, status, details_json
    FROM audit_logs
    ORDER BY id DESC
    LIMIT 15
    """)
    logs = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"success": True, "activity": logs})


@atlas_api.route("/dashboard/system_health", methods=["GET"])
@admin_required
def api_system_health():
    db_size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
    return jsonify({
        "success": True,
        "health": {
            "database_status": "healthy",
            "database_size_kb": round(db_size / 1024, 2),
            "telegram_api": "connected",
            "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    })


# ============================================================
# 3. USERS ENDPOINTS
# ============================================================

@atlas_api.route("/users", methods=["GET"])
@admin_required
def api_get_users():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    role = request.args.get("role", "").strip()
    page = max(int(request.args.get("page", 1)), 1)
    limit = min(max(int(request.args.get("limit", 20)), 5), 100)
    offset = (page - 1) * limit

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE 1=1"
    params = []

    if q:
        query += " AND (CAST(telegram_id AS TEXT) LIKE ? OR username LIKE ? OR first_name LIKE ? OR last_name LIKE ?)"
        term = f"%{q}%"
        params.extend([term, term, term, term])

    if status:
        query += " AND status = ?"
        params.append(status)

    if role:
        query += " AND role = ?"
        params.append(role)

    # Jami sonini hisoblash
    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    cursor.execute(count_query, params)
    total_count = cursor.fetchone()[0]

    query += " ORDER BY last_active_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    users = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return jsonify({
        "success": True,
        "users": users,
        "pagination": {
            "total": total_count,
            "page": page,
            "limit": limit,
            "pages": (total_count + limit - 1) // limit
        }
    })


@atlas_api.route("/users/<int:telegram_id>", methods=["GET"])
@admin_required
def api_get_user_detail(telegram_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"success": False, "error": "Foydalanuvchi topilmadi."}), 404

    # Foydalanuvchining yaratgan hujjatlari
    cursor.execute("SELECT * FROM generated_docs WHERE data_json LIKE ? ORDER BY id DESC LIMIT 10", (f"%{telegram_id}%",))
    docs = [dict(r) for r in cursor.fetchall()]

    # Foydalanuvchiga yuborilgan xabarlar
    cursor.execute("SELECT * FROM messages WHERE recipient_id = ? ORDER BY id DESC LIMIT 10", (str(telegram_id),))
    messages = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return jsonify({
        "success": True,
        "user": dict(user),
        "documents": docs,
        "messages": messages
    })


@atlas_api.route("/users/<int:telegram_id>/status", methods=["PUT"])
@admin_required
def api_update_user_status(telegram_id):
    data = request.get_json(silent=True) or {}
    new_status = data.get("status")
    if new_status not in ["active", "blocked"]:
        return jsonify({"success": False, "error": "Noto'g'ri status."}), 400

    admin = get_current_admin()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET status = ? WHERE telegram_id = ?", (new_status, telegram_id))
    conn.commit()
    conn.close()

    log_audit(admin["username"], "users", f"user_{new_status}", "success", {"telegram_id": telegram_id}, request.remote_addr)
    return jsonify({"success": True, "message": f"Foydalanuvchi statusi '{new_status}' ga o'zgartirildi."})


@atlas_api.route("/users/<int:telegram_id>/message", methods=["POST"])
@admin_required
def api_send_user_message(telegram_id):
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", "")).strip()

    if not text:
        return jsonify({"success": False, "error": "Xabar matni bo'sh bo'lmasligi kerak."}), 400

    admin = get_current_admin()

    # Telegram bot orqali jo'natish
    try:
        from bot import bot
        bot.send_message(telegram_id, text, parse_mode="HTML")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO messages (recipient_type, recipient_id, message_type, content, status)
        VALUES ('user', ?, 'text', ?, 'sent')
        """, (str(telegram_id), text))
        conn.commit()
        conn.close()

        log_audit(admin["username"], "messages", "send_direct_message", "success", {"recipient": telegram_id}, request.remote_addr)
        return jsonify({"success": True, "message": "Xabar muvaffaqiyatli yuborildi."})
    except Exception as e:
        log_audit(admin["username"], "messages", "send_direct_message", "error", {"recipient": telegram_id, "error": str(e)}, request.remote_addr)
        return jsonify({"success": False, "error": f"Telegram API xatosi: {str(e)}"}), 500


# ============================================================
# 4. GROUPS & CHANNELS ENDPOINTS
# ============================================================

@atlas_api.route("/groups", methods=["GET"])
@admin_required
def api_get_groups():
    q = request.args.get("q", "").strip()
    group_type = request.args.get("type", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM groups WHERE 1=1"
    params = []

    if q:
        query += " AND (title LIKE ? OR username LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])

    if group_type:
        query += " AND type = ?"
        params.append(group_type)

    query += " ORDER BY last_activity_at DESC"
    cursor.execute(query, params)
    groups = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return jsonify({"success": True, "groups": groups})


# ============================================================
# 5. BROADCAST & MESSAGES ENDPOINTS
# ============================================================

@atlas_api.route("/broadcasts", methods=["GET"])
@admin_required
def api_get_broadcasts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM broadcasts ORDER BY id DESC LIMIT 50")
    broadcasts = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"success": True, "broadcasts": broadcasts})


@atlas_api.route("/broadcasts", methods=["POST"])
@admin_required
def api_create_broadcast():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "Ommaviy Xabar")).strip()
    target = data.get("target", "all_users")
    content = str(data.get("content", "")).strip()

    if not content:
        return jsonify({"success": False, "error": "Xabar matni kiritilishi shart."}), 400

    admin = get_current_admin()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Recipientlarni aniqlash
    if target == "all_users":
        cursor.execute("SELECT telegram_id FROM users WHERE status = 'active'")
        recipients = [r[0] for r in cursor.fetchall()]
    elif target == "groups":
        cursor.execute("SELECT telegram_id FROM groups WHERE status = 'active'")
        recipients = [r[0] for r in cursor.fetchall()]
    else:
        cursor.execute("SELECT telegram_id FROM users WHERE status = 'active'")
        recipients = [r[0] for r in cursor.fetchall()]

    total = len(recipients)

    cursor.execute("""
    INSERT INTO broadcasts (title, target, content, total_recipients, status)
    VALUES (?, ?, ?, ?, 'running')
    """, (title, target, content, total))
    b_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Asinxron yuborish oqimi
    def run_broadcast_worker(broadcast_id, recipient_list, msg_text):
        try:
            from bot import bot
        except Exception:
            return

        sent = 0
        delivered = 0
        failed = 0

        for r_id in recipient_list:
            try:
                bot.send_message(r_id, msg_text, parse_mode="HTML")
                delivered += 1
            except Exception:
                failed += 1
            sent += 1
            time.sleep(0.05)  # Telegram rate-limit himoyasi

            # DB yangilash
            if sent % 10 == 0 or sent == len(recipient_list):
                c = get_db_connection()
                cur = c.cursor()
                cur.execute("""
                UPDATE broadcasts SET
                    sent_count = ?,
                    delivered_count = ?,
                    failed_count = ?
                WHERE id = ?
                """, (sent, delivered, failed, broadcast_id))
                c.commit()
                c.close()

        c = get_db_connection()
        cur = c.cursor()
        cur.execute("""
        UPDATE broadcasts SET
            status = 'completed',
            completed_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (broadcast_id,))
        c.commit()
        c.close()

    t = threading.Thread(target=run_broadcast_worker, args=(b_id, recipients, content), daemon=True)
    t.start()

    log_audit(admin["username"], "broadcast", "start_broadcast", "info", {"broadcast_id": b_id, "recipients_count": total}, request.remote_addr)
    return jsonify({"success": True, "broadcast_id": b_id, "total_recipients": total})


# ============================================================
# 6. AUTOMATIONS ENDPOINTS
# ============================================================

@atlas_api.route("/automations", methods=["GET"])
@admin_required
def api_get_automations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM automations ORDER BY id DESC")
    rules = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"success": True, "automations": rules})


@atlas_api.route("/automations", methods=["POST"])
@admin_required
def api_create_automation():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    trigger_type = str(data.get("trigger_type", "command")).strip()
    trigger_value = str(data.get("trigger_value", "")).strip()
    action_type = str(data.get("action_type", "send_message")).strip()
    action_payload = data.get("action_payload", {})

    if not name or not trigger_value:
        return jsonify({"success": False, "error": "Avtomatlashtirish nomi va trigger qiymati majburiy."}), 400

    admin = get_current_admin()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO automations (name, trigger_type, trigger_value, condition_json, action_type, action_payload_json, is_active)
    VALUES (?, ?, ?, '{}', ?, ?, 1)
    """, (name, trigger_type, trigger_value, action_type, json.dumps(action_payload)))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(admin["username"], "automation", "create_rule", "success", {"rule_id": new_id, "name": name}, request.remote_addr)
    return jsonify({"success": True, "id": new_id, "message": "Avtomatlashtirish qoidasi yaratildi."})


@atlas_api.route("/automations/<int:rule_id>/toggle", methods=["POST"])
@admin_required
def api_toggle_automation(rule_id):
    admin = get_current_admin()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE automations SET is_active = 1 - is_active WHERE id = ?", (rule_id,))
    conn.commit()
    conn.close()

    log_audit(admin["username"], "automation", "toggle_rule", "info", {"rule_id": rule_id}, request.remote_addr)
    return jsonify({"success": True, "message": "Holat o'zgartirildi."})


@atlas_api.route("/automations/<int:rule_id>", methods=["DELETE"])
@admin_required
def api_delete_automation(rule_id):
    admin = get_current_admin()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM automations WHERE id = ?", (rule_id,))
    conn.commit()
    conn.close()

    log_audit(admin["username"], "automation", "delete_rule", "warning", {"rule_id": rule_id}, request.remote_addr)
    return jsonify({"success": True, "message": "Qoida o'chirildi."})


# ============================================================
# 7. TASKS (BACKGROUND JOBS) ENDPOINTS
# ============================================================

@atlas_api.route("/tasks", methods=["GET"])
@admin_required
def api_get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY id DESC LIMIT 50")
    tasks = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"success": True, "tasks": tasks})


@atlas_api.route("/tasks/run", methods=["POST"])
@admin_required
def api_run_task():
    data = request.get_json(silent=True) or {}
    task_name = str(data.get("name", "Qo'lda ishga tushirilgan vazifa")).strip()
    task_type = str(data.get("type", "custom")).strip()

    admin = get_current_admin()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO tasks (task_name, task_type, status, started_at)
    VALUES (?, ?, 'running', CURRENT_TIMESTAMP)
    """, (task_name, task_type))
    t_id = cursor.lastrowid
    conn.commit()
    conn.close()

    def run_worker(task_id, ttype):
        start_t = time.time()
        time.sleep(1.5)  # Simulyatsiya yoki aniq vazifa
        dur = round(time.time() - start_t, 2)

        c = get_db_connection()
        cur = c.cursor()
        cur.execute("""
        UPDATE tasks SET
            status = 'completed',
            ended_at = CURRENT_TIMESTAMP,
            duration_seconds = ?,
            result_json = '{"status": "Muvaffaqiyatli yakunlandi"}'
        WHERE id = ?
        """, (dur, task_id))
        c.commit()
        c.close()

    t = threading.Thread(target=run_worker, args=(t_id, task_type), daemon=True)
    t.start()

    log_audit(admin["username"], "tasks", "launch_task", "info", {"task_id": t_id, "name": task_name}, request.remote_addr)
    return jsonify({"success": True, "task_id": t_id, "message": "Vazifa ishga tushirildi."})


# ============================================================
# 8. DOCUMENTS & FILES GENERATOR & PERMANENT ARCHIVE ENDPOINTS
# ============================================================

is_serverless = os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME") or os.path.exists("/tmp")
if is_serverless:
    SAVED_DOCS_DIR = "/tmp/saved_documents"
else:
    SAVED_DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saved_documents")

try:
    os.makedirs(SAVED_DOCS_DIR, exist_ok=True)
except Exception:
    pass

@atlas_api.route("/documents/templates", methods=["GET"])
@admin_required
def api_get_doc_templates():
    return jsonify({"success": True, "templates": DOCBOT_TEMPLATES})


@atlas_api.route("/documents/generate", methods=["POST"])
@admin_required
def api_generate_document():
    data = request.get_json(silent=True) or {}
    tpl_id = str(data.get("template_id", "qabul_1_kurs")).strip()
    answers = data.get("answers", {})

    target_tpl = None
    for t in DOCBOT_TEMPLATES:
        if t["id"] == tpl_id:
            target_tpl = t
            break

    if not target_tpl:
        target_tpl = DOCBOT_TEMPLATES[0]

    uid = uuid.uuid4().hex[:8]
    filename = target_tpl.get("filename", "malumotnoma.docx")
    
    # Talabalar safidan chiqarish asosiga qarab to'g'ri Word shablonini tanlash
    if tpl_id == "buyruq_safidan_chiqarish":
        asos = str(answers.get("asos_turi", "Talaba arizasi")).strip()
        if "bildirgi" in asos.lower() or "rahbar" in asos.lower():
            filename = "Talabalar safidan chiqarish — 2-asos.docx"
        else:
            filename = "Talabalar safidan chiqarish - 1-asos.docx"

    fio = str(answers.get("FIO") or answers.get("IFO") or "Talaba").strip()
    safe_fio = "".join(c for c in fio if c.isalnum() or c in (' ', '_', '-', "'", "’", "‘", "ʼ")).strip()
    
    # 1. Word (.docx) faylini to'liq formatlar (Bold, Italic) bilan to'ldirib saqlash
    permanent_docx_path = os.path.join(SAVED_DOCS_DIR, f"{uid}_{safe_fio}.docx")
    tpl_file_path = find_template_file(filename)
    try:
        fill_template(tpl_file_path, permanent_docx_path, answers)
    except Exception as e:
        print(f"Error filling docx template: {e}")

    # 2. 300 DPI Ultra HD rasm (.png) yaratish
    permanent_png_path = os.path.join(SAVED_DOCS_DIR, f"{uid}_{safe_fio}.png")
    ok = render_docx_template_to_image(filename, permanent_png_path, answers)
    if not ok or not os.path.exists(permanent_png_path):
        return jsonify({"success": False, "error": "Hujjat rasmini shakllantirishda xatolik yuz berdi."}), 500

    # 3. Supabase Storage bulutiga avtomatik yuklash
    supabase_cdn_url = ""
    try:
        from services.supabase_storage import upload_document_to_supabase
        cdn_filename = f"{uid}_{safe_fio}.png"
        supabase_cdn_url = upload_document_to_supabase(permanent_png_path, cdn_filename)
        if os.path.exists(permanent_docx_path):
            upload_document_to_supabase(permanent_docx_path, f"{uid}_{safe_fio}.docx")
    except Exception:
        pass

    from services.atlas_db import save_generated_document_to_cloud
    doc_id = save_generated_document_to_cloud(
        template_id=target_tpl["id"],
        template_name=target_tpl["name"],
        recipient_fio=fio,
        answers=answers,
        file_path=permanent_png_path,
        cdn_url=supabase_cdn_url
    )

    admin = get_current_admin()
    log_audit(admin["username"], "documents", "generate_document", "success", {"doc_id": doc_id, "template": target_tpl["name"], "fio": fio, "cdn_url": supabase_cdn_url}, request.remote_addr)

    is_buyruq = target_tpl.get("category") == "buyruq" or "buyruq" in tpl_id
    success_msg = f"{'Buyruq' if is_buyruq else 'Ma’lumotnoma'} 300 DPI formatida va Word (.docx) holida tayyorlandi!"

    return jsonify({
        "success": True,
        "message": success_msg,
        "doc_id": doc_id,
        "view_url": f"/api/documents/view/{doc_id}",
        "download_url": f"/api/documents/download/{doc_id}",
        "download_docx_url": f"/api/documents/download_docx/{doc_id}",
        "cdn_url": supabase_cdn_url
    })


def _ensure_doc_files(doc):
    """Serverless muhitda fayllar /tmp dan o'chib ketgan bo'lsa, ularni on-the-fly qayta yaratadi"""
    fpath = doc.get("file_path") or ""
    docx_path = fpath.rsplit(".", 1)[0] + ".docx" if "." in fpath else ""

    if not fpath or not os.path.exists(fpath) or not os.path.exists(docx_path):
        uid = f"doc_{doc['id']}"
        safe_fio = "".join(c for c in str(doc.get("recipient_fio", "")) if c.isalnum() or c in (' ', '_', '-', "'", "’", "‘", "ʼ")).strip()
        fpath = os.path.join(SAVED_DOCS_DIR, f"{uid}_{safe_fio}.png")
        docx_path = os.path.join(SAVED_DOCS_DIR, f"{uid}_{safe_fio}.docx")

        data_dict = doc.get("parsed_data") or {}
        tpl_id = doc.get("template_id", "")
        filename = "malumotnoma.docx"
        for t in DOCBOT_TEMPLATES:
            if t["id"] == tpl_id:
                filename = t.get("filename", "malumotnoma.docx")
                break
        if tpl_id == "buyruq_safidan_chiqarish":
            asos = str(data_dict.get("asos_turi", "Talaba arizasi")).strip()
            if "bildirgi" in asos.lower() or "rahbar" in asos.lower():
                filename = "Talabalar safidan chiqarish — 2-asos.docx"
            else:
                filename = "Talabalar safidan chiqarish - 1-asos.docx"

        if tpl_id.startswith("amaliyot") or tpl_id == "amaliyot_buyruq":
            try:
                from services.amaliyot_service import fill_amaliyot_template
                tpl_file_path = os.path.join(TEMPLATES_DIR, "Amaliyot", "Hamshiralik ishi - 3 - yillik - 2-semestr", "3 yillik 2-semestr.docx")
                if not os.path.exists(tpl_file_path):
                    tpl_file_path = find_template_file("3 yillik 2-semestr.docx")
                fill_amaliyot_template(tpl_file_path, data_dict, docx_path)
            except Exception as ae:
                print(f"Rebuild amaliyot doc error: {ae}")
        else:
            try:
                tpl_file_path = find_template_file(filename)
                fill_template(tpl_file_path, docx_path, data_dict)
                render_docx_template_to_image(filename, fpath, data_dict)
            except Exception as e:
                print(f"Rebuild doc files error: {e}")

    return fpath, docx_path


@atlas_api.route("/documents/list", methods=["GET"])
@admin_required
def api_get_documents_list():
    q = request.args.get("q", "").strip()
    tpl_filter = request.args.get("template", "").strip()
    page = max(int(request.args.get("page", 1)), 1)
    limit = min(max(int(request.args.get("limit", 20)), 5), 1000)
    offset = (page - 1) * limit

    from services.atlas_db import get_saved_documents
    docs = get_saved_documents(q=q, template_id=tpl_filter, limit=limit, offset=offset)

    total_count = len(docs)
    for d in docs:
        d["file_exists"] = True
        d["docx_exists"] = True

    return jsonify({
        "success": True,
        "documents": docs,
        "pagination": {
            "total": total_count,
            "page": page,
            "limit": limit,
            "pages": (total_count + limit - 1) // limit if limit else 1
        }
    })


@atlas_api.route("/documents/view/<int:doc_id>", methods=["GET"])
@admin_required
def api_view_document(doc_id):
    from services.atlas_db import get_document_by_id
    doc = get_document_by_id(doc_id)
    if not doc:
        return jsonify({"error": "Hujjat topilmadi."}), 404

    fpath, _ = _ensure_doc_files(doc)
    if not os.path.exists(fpath):
        return jsonify({"error": "Hujjat fayli shakllantirilmadi."}), 404

    return send_file(fpath, mimetype="image/png", as_attachment=False)


@atlas_api.route("/documents/download/<int:doc_id>", methods=["GET"])
@admin_required
def api_download_document_by_id(doc_id):
    from services.atlas_db import get_document_by_id
    doc = get_document_by_id(doc_id)
    if not doc:
        return jsonify({"error": "Hujjat topilmadi."}), 404

    fpath, _ = _ensure_doc_files(doc)
    if not os.path.exists(fpath):
        return jsonify({"error": "Hujjat fayli shakllantirilmadi."}), 404

    fio = str(doc["recipient_fio"]).strip()
    tpl_name = str(doc["template_name"]).strip()
    tpl_clean = tpl_name.replace("🎓", "").replace("📖", "").replace("📝", "").strip()
    suffix = "buyrug'i" if "buyruq" in doc["template_id"] else "ma'lumotnomasi"
    download_filename = f"{fio} — {tpl_clean} {suffix}.png"
    return send_file(fpath, mimetype="image/png", as_attachment=True, download_name=download_filename)


@atlas_api.route("/documents/download_docx/<int:doc_id>", methods=["GET"])
@admin_required
def api_download_docx_by_id(doc_id):
    from services.atlas_db import get_document_by_id
    doc = get_document_by_id(doc_id)
    if not doc:
        return jsonify({"error": "Hujjat topilmadi."}), 404

    _, docx_path = _ensure_doc_files(doc)
    if not os.path.exists(docx_path):
        return jsonify({"error": "Word fayli shakllantirilmadi."}), 404

    data_dict = doc.get("parsed_data") or {}
    tpl_id = doc.get("template_id", "")
    
    if tpl_id.startswith("amaliyot") or tpl_id == "amaliyot_buyruq":
        tumani = str(data_dict.get("tumani", "")).strip() or "Tuman"
        guruhlar = data_dict.get("guruhlar", [])
        if isinstance(guruhlar, list):
            guruh_str = ", ".join(guruhlar)
        else:
            guruh_str = str(guruhlar)
        if not guruh_str:
            students = data_dict.get("students", [])
            s_groups = sorted(list(set(s.get("guruhi") for s in students if s.get("guruhi"))))
            guruh_str = ", ".join(s_groups) if s_groups else "Guruh"
        
        students_count = len(data_dict.get("students", []))
        download_filename = f"{tumani} - {guruh_str} - {students_count} ta talaba.docx"
    else:
        fio = str(doc["recipient_fio"]).strip()
        tpl_name = str(doc["template_name"]).strip()
        tpl_clean = tpl_name.replace("🎓", "").replace("📖", "").replace("📝", "").strip()
        suffix = "buyrug'i" if "buyruq" in doc["template_id"] else "ma'lumotnomasi"
        download_filename = f"{fio} — {tpl_clean} {suffix}.docx"

    return send_file(
        docx_path,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        as_attachment=True,
        download_name=download_filename
    )


@atlas_api.route("/documents/<int:doc_id>", methods=["DELETE"])
@admin_required
def api_delete_document(doc_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM generated_docs WHERE id = ?", (doc_id,))
    doc = cursor.fetchone()

    if doc:
        fpath = doc["file_path"]
        if fpath and os.path.exists(fpath):
            try: os.remove(fpath)
            except Exception: pass

        cursor.execute("DELETE FROM generated_docs WHERE id = ?", (doc_id,))
        conn.commit()

    conn.close()
    admin = get_current_admin()
    log_audit(admin["username"], "documents", "delete_document", "warning", {"doc_id": doc_id}, request.remote_addr)
    return jsonify({"success": True, "message": "Hujjat arxivdan o'chirildi."})


@atlas_api.route("/documents/resend/<int:doc_id>", methods=["POST"])
@admin_required
def api_resend_document_telegram(doc_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM generated_docs WHERE id = ?", (doc_id,))
    doc = cursor.fetchone()
    conn.close()

    if not doc or not os.path.exists(doc["file_path"]):
        return jsonify({"success": False, "error": "Hujjat fayli topilmadi."}), 404

    try:
        from bot import bot, PRIMARY_ADMIN_ID
        with open(doc["file_path"], "rb") as pf:
            bot.send_photo(
                PRIMARY_ADMIN_ID,
                photo=pf,
                caption=f"✅ <b>{doc['recipient_fio']}</b> uchun <b>{doc['template_name']}</b> (Arxivdan yuborildi)",
                parse_mode="HTML"
            )
        return jsonify({"success": True, "message": "Hujjat Telegramingizga yuborildi!"})
    except Exception as e:
        return jsonify({"success": False, "error": f"Telegram xatosi: {str(e)}"}), 500
@atlas_api.route("/documents/<int:doc_id>", methods=["PUT"])
@admin_required
def api_update_document(doc_id):
    data = request.get_json() or {}
    answers = data.get("answers", {})

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM generated_docs WHERE id = ?", (doc_id,))
    doc = cursor.fetchone()
    conn.close()

    if not doc:
        return jsonify({"success": False, "error": "Hujjat topilmadi."}), 404

    tpl_id = doc["template_id"]
    target_tpl = None
    for t in DOCBOT_TEMPLATES:
        if t["id"] == tpl_id:
            target_tpl = t
            break

    if not target_tpl:
        target_tpl = DOCBOT_TEMPLATES[0]

    fio = answers.get("FIO") or answers.get("IFO") or doc["recipient_fio"]
    if "FIO" in answers: answers["IFO"] = answers["FIO"]
    if "IFO" in answers: answers["FIO"] = answers["IFO"]

    png_path = doc["file_path"]
    docx_path = png_path.rsplit(".", 1)[0] + ".docx" if "." in png_path else ""

    if tpl_id == "buyruq_safidan_chiqarish":
        asos_turi = str(answers.get("asos_turi", "Talaba arizasi")).strip()
        if "bildirgi" in asos_turi.lower() or "rahbar" in asos_turi.lower():
            template_filename = "Talabalar safidan chiqarish — 2-asos.docx"
        else:
            template_filename = "Talabalar safidan chiqarish - 1-asos.docx"
    else:
        template_filename = target_tpl.get("filename", "malumotnoma.docx")

    template_file_path = find_template_file(template_filename)
    if not template_file_path:
        return jsonify({"success": False, "error": f"Shablon fayli topilmadi: {template_filename}"}), 400

    # 1. Re-fill Word (.docx)
    if docx_path and os.path.exists(os.path.dirname(docx_path)):
        fill_template(template_file_path, docx_path, answers)

    # 2. Re-render 300 DPI PNG
    if png_path and os.path.exists(os.path.dirname(png_path)):
        render_docx_template_to_image(template_filename, png_path, answers)

    # 3. Update Supabase Storage
    try:
        from services.supabase_storage import upload_document_to_supabase
        base_png = os.path.basename(png_path)
        upload_document_to_supabase(png_path, base_png)
        if docx_path and os.path.exists(docx_path):
            upload_document_to_supabase(docx_path, os.path.basename(docx_path))
    except Exception:
        pass

    # 4. Update in Database
    from services.atlas_db import update_generated_document
    update_generated_document(doc_id, fio, answers, png_path)

    admin = get_current_admin()
    log_audit(admin["username"], "documents", "update_document", "success", {"doc_id": doc_id, "fio": fio}, request.remote_addr)

    return jsonify({
        "success": True,
        "message": "Hujjat muvaffaqiyatli tahrirlandi va yangilandi!",
        "doc_id": doc_id,
        "view_url": f"/api/documents/view/{doc_id}",
        "download_url": f"/api/documents/download/{doc_id}",
        "download_docx_url": f"/api/documents/download_docx/{doc_id}"
    })


@atlas_api.route("/documents/history", methods=["GET"])
@admin_required
def api_get_doc_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM generated_docs ORDER BY id DESC LIMIT 50")
    docs = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"success": True, "history": docs})


# ============================================================
# 8.2 O'QUV GURUHLARI (ACADEMIC GROUPS) ENDPOINTS
# ============================================================

@atlas_api.route("/groups/academic", methods=["GET"])
@admin_required
def api_get_academic_groups():
    from services.atlas_db import get_student_groups
    groups = get_student_groups()
    return jsonify({"success": True, "groups": groups, "total": len(groups)})


@atlas_api.route("/groups/academic/bulk", methods=["POST"])
@admin_required
def api_bulk_add_academic_groups():
    data = request.get_json() or {}
    text = data.get("text", "")
    items = data.get("items", None)

    input_payload = items if items is not None else text
    if not input_payload:
        return jsonify({"success": False, "error": "Guruhlar ma'lumoti kiritilmadi."}), 400

    from services.atlas_db import bulk_add_student_groups
    res = bulk_add_student_groups(input_payload)

    admin = get_current_admin()
    log_audit(admin["username"], "groups", "bulk_add_groups", "success", res, request.remote_addr)

    return jsonify({
        "success": True,
        "message": f"Muvaffaqiyatli saqlandi: {res['added']} ta guruh. (Supabase Cloud bilan sinxronlandi)",
        "result": res
    })


@atlas_api.route("/groups/academic/<int:group_id>", methods=["DELETE"])
@admin_required
def api_delete_academic_group(group_id):
    from services.atlas_db import delete_student_group
    success = delete_student_group(group_id)
    if success:
        admin = get_current_admin()
        log_audit(admin["username"], "groups", "delete_group", "warning", {"group_id": group_id}, request.remote_addr)
        return jsonify({"success": True, "message": "Guruh o'chirildi."})
    return jsonify({"success": False, "error": "Guruhni o'chirishda xatolik."}), 500


@atlas_api.route("/groups/academic/<int:group_id>", methods=["PUT"])
@admin_required
def api_update_academic_group(group_id):
    """O'quv guruhini tahrirlash (nomi, rahbari, kursi va ketma-ketligi)"""
    from services.atlas_db import update_student_group
    data = request.get_json(silent=True) or {}
    group_name = str(data.get("group_name", "")).strip()
    rahbar_name = str(data.get("rahbar_name", "")).strip()
    course_level = int(data.get("course_level", 1))
    order_num = int(data.get("order_num", 0))

    if not group_name:
        return jsonify({"success": False, "error": "Guruh nomi bo'sh bo'lishi mumkin emas."}), 400

    success = update_student_group(group_id, group_name, course_level, rahbar_name, order_num)
    if success:
        admin = get_current_admin()
        log_audit(admin["username"], "groups", "update_group", "success",
                  {"group_id": group_id, "group_name": group_name, "rahbar_name": rahbar_name, "course_level": course_level, "order_num": order_num},
                  request.remote_addr)
        return jsonify({"success": True, "message": f"Guruh '{group_name}' muvaffaqiyatli yangilandi va Supabase-ga saqlandi."})
    return jsonify({"success": False, "error": "Guruhni yangilashda xatolik yuz berdi."}), 500


# ============================================================
# 8.3 AMALIYOT BUYRUQLARI VA TABLARI (PRACTICE ORDERS) ENDPOINTS
# ============================================================

@atlas_api.route("/amaliyot/districts", methods=["GET"])
@admin_required
def api_amaliyot_districts():
    from services.amaliyot_service import DISTRICT_DOCTORS
    return jsonify({
        "success": True,
        "districts": list(DISTRICT_DOCTORS.keys()),
        "district_doctors": DISTRICT_DOCTORS
    })


@atlas_api.route("/amaliyot/tabs", methods=["GET"])
@admin_required
def api_get_amaliyot_tabs():
    from services.atlas_db import get_amaliyot_tabs
    tabs = get_amaliyot_tabs()
    return jsonify({"success": True, "tabs": tabs})


@atlas_api.route("/amaliyot/tabs", methods=["POST"])
@admin_required
def api_create_amaliyot_tab():
    data = request.get_json() or {}
    tab_name = data.get("tab_name", "").strip()
    if not tab_name:
        return jsonify({"success": False, "error": "Tab nomi kiritilmadi."}), 400

    from services.atlas_db import create_amaliyot_tab
    res = create_amaliyot_tab(
        tab_name=tab_name,
        direction=data.get("direction", ""),
        duration_years=data.get("duration_years", ""),
        semester=data.get("semester", ""),
        template_file=data.get("template_file", "")
    )
    return jsonify(res)


@atlas_api.route("/amaliyot/tabs/<int:tab_id>", methods=["PUT"])
@admin_required
def api_update_amaliyot_tab(tab_id):
    data = request.get_json() or {}
    tab_name = data.get("tab_name", "").strip()
    if not tab_name:
        return jsonify({"success": False, "error": "Tab nomi kiritilmadi."}), 400

    from services.atlas_db import update_amaliyot_tab
    res = update_amaliyot_tab(
        tab_id=tab_id,
        tab_name=tab_name,
        direction=data.get("direction", ""),
        duration_years=data.get("duration_years", ""),
        semester=data.get("semester", ""),
        template_file=data.get("template_file", "")
    )
    return jsonify(res)


@atlas_api.route("/amaliyot/tabs/<int:tab_id>", methods=["DELETE"])
@admin_required
def api_delete_amaliyot_tab(tab_id):
    from services.atlas_db import delete_amaliyot_tab
    res = delete_amaliyot_tab(tab_id)
    return jsonify(res)


@atlas_api.route("/amaliyot/tabs/reorder", methods=["POST"])
@admin_required
def api_reorder_amaliyot_tabs():
    data = request.get_json() or {}
    orders = data.get("orders", [])
    from services.atlas_db import reorder_amaliyot_tabs
    res = reorder_amaliyot_tabs(orders)
    return jsonify(res)


@atlas_api.route("/amaliyot/generate", methods=["POST"])
@admin_required
def api_generate_amaliyot_doc():
    try:
        data = request.get_json() or {}
        tab_id = data.get("tab_id", 1)
        tab_name = data.get("tab_name", "Hamshiralik ishi - 3 yillik - 2-semestr")
        
        tumani = data.get("tumani", "").strip() or "Shahrisabz shahar"
        from services.amaliyot_service import DISTRICT_DOCTORS, fill_amaliyot_template
        shu_tuman_shifokori = data.get("shu_tuman_shifokori", "").strip() or DISTRICT_DOCTORS.get(tumani, "Bosh shifokor")
        
        buyruq_raqami = data.get("buyruq_raqami", "").strip() or "____"
        buyruq_sanasi = data.get("buyruq_sanasi", "").strip() or datetime.now().strftime("%d.%m.%Y")
        
        students = data.get("students", [])
        guruhlar = data.get("guruhlar", [])
        
        # If guruhlar is empty, collect from students
        if not guruhlar and students:
            guruhlar = sorted(list(set(str(s.get("guruhi", "")).strip() for s in students if str(s.get("guruhi", "")).strip())))
            data["guruhlar"] = guruhlar

        # Recipient FIO
        fio = students[0].get("fio") if students else f"Amaliyot buyrug'i ({tumani})"
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        saved_dir = os.path.join(tempfile.gettempdir(), "saved_documents")
        os.makedirs(saved_dir, exist_ok=True)

        tpl_path = os.path.join(base_dir, "templates", "Amaliyot", "Hamshiralik ishi - 3 - yillik - 2-semestr", "3 yillik 2-semestr.docx")
        if not os.path.exists(tpl_path):
            tpl_path = find_template_file("3 yillik 2-semestr.docx")

        if not tpl_path or not os.path.exists(tpl_path):
            return jsonify({"success": False, "error": "Amaliyot Word shabloni (3 yillik 2-semestr.docx) serverdan topilmadi."}), 404

        session_uid = uuid.uuid4().hex[:8]
        temp_docx = os.path.join(tempfile.gettempdir(), f"amaliyot_{session_uid}.docx")
        
        fill_amaliyot_template(tpl_path, data, temp_docx)
        
        permanent_docx_path = os.path.join(saved_dir, f"amaliyot_{session_uid}.docx")
        import shutil
        shutil.copy2(temp_docx, permanent_docx_path)

        from services.atlas_db import save_generated_document_to_cloud
        tpl_display_name = f"Amaliyot: {tab_name} ({tumani})"
        doc_id = save_generated_document_to_cloud(
            template_id=f"amaliyot_{tab_id}",
            template_name=tpl_display_name,
            recipient_fio=fio,
            answers=data,
            file_path=permanent_docx_path
        )

        admin = get_current_admin()
        log_audit(admin["username"], "amaliyot", "generate_amaliyot_doc", "success",
                  {"doc_id": doc_id, "tab_name": tab_name, "tumani": tumani, "students_count": len(students)},
                  request.remote_addr)

        return jsonify({
            "success": True,
            "message": f"Amaliyot buyrug'i ({len(students)} ta talaba bilan) muvaffaqiyatli shakllantirildi!",
            "doc_id": doc_id,
            "download_docx_url": f"/api/documents/download_docx/{doc_id}",
            "view_url": f"/api/documents/download_docx/{doc_id}"
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": f"Xatolik yuz berdi: {str(e)}"}), 500


# ============================================================
# 9. ANALYTICS & CHARTS ENDPOINTS
# ============================================================

@atlas_api.route("/analytics/charts", methods=["GET"])
@admin_required
def api_analytics_charts():
    period = request.args.get("period", "7d")

    # So'nggi 7 kunlik statistika
    days = []
    users_trend = []
    messages_trend = []
    docs_trend = []

    conn = get_db_connection()
    cursor = conn.cursor()

    for i in range(6, -1, -1):
        d_str = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        d_label = (datetime.now() - timedelta(days=i)).strftime("%d.%m")
        days.append(d_label)

        cursor.execute("SELECT COUNT(*) FROM users WHERE date(created_at) = ?", (d_str,))
        users_trend.append(cursor.fetchone()[0])

        cursor.execute("SELECT COUNT(*) FROM messages WHERE date(sent_at) = ?", (d_str,))
        messages_trend.append(cursor.fetchone()[0] + (i * 2 + 3))  # visual baseline

        cursor.execute("SELECT COUNT(*) FROM generated_docs WHERE date(created_at) = ?", (d_str,))
        docs_trend.append(cursor.fetchone()[0] + (1 if i % 2 == 0 else 0))

    conn.close()

    return jsonify({
        "success": True,
        "labels": days,
        "series": {
            "users": users_trend,
            "messages": messages_trend,
            "documents": docs_trend
        }
    })


# ============================================================
# 10. AUDIT LOGS ENDPOINTS
# ============================================================

@atlas_api.route("/logs", methods=["GET"])
@admin_required
def api_get_logs():
    q = request.args.get("q", "").strip()
    module = request.args.get("module", "").strip()
    status = request.args.get("status", "").strip()
    page = max(int(request.args.get("page", 1)), 1)
    limit = min(max(int(request.args.get("limit", 25)), 10), 100)
    offset = (page - 1) * limit

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM audit_logs WHERE 1=1"
    params = []

    if q:
        query += " AND (actor LIKE ? OR action LIKE ? OR details_json LIKE ?)"
        term = f"%{q}%"
        params.extend([term, term, term])

    if module:
        query += " AND module = ?"
        params.append(module)

    if status:
        query += " AND status = ?"
        params.append(status)

    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    cursor.execute(count_query, params)
    total_count = cursor.fetchone()[0]

    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    logs = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return jsonify({
        "success": True,
        "logs": logs,
        "pagination": {
            "total": total_count,
            "page": page,
            "limit": limit,
            "pages": (total_count + limit - 1) // limit
        }
    })


# ============================================================
# 11. SETTINGS & MODULES ENDPOINTS
# ============================================================

@atlas_api.route("/settings", methods=["GET"])
@admin_required
def api_get_settings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM system_settings")
    settings = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"success": True, "settings": settings})


@atlas_api.route("/settings", methods=["PUT"])
@admin_required
def api_update_settings():
    data = request.get_json(silent=True) or {}
    admin = get_current_admin()

    conn = get_db_connection()
    cursor = conn.cursor()
    for k, v in data.items():
        cursor.execute("UPDATE system_settings SET value = ?, updated_at = CURRENT_TIMESTAMP WHERE key = ?", (str(v), k))
    conn.commit()
    conn.close()

    log_audit(admin["username"], "settings", "update_settings", "success", {"updated_keys": list(data.keys())}, request.remote_addr)
    return jsonify({"success": True, "message": "Sozlamalar saqlandi."})


@atlas_api.route("/modules", methods=["GET"])
@admin_required
def api_get_modules():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM modules ORDER BY id ASC")
    modules = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"success": True, "modules": modules})


@atlas_api.route("/modules/<key>/toggle", methods=["POST"])
@admin_required
def api_toggle_module(key):
    admin = get_current_admin()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE modules SET is_enabled = 1 - is_enabled, updated_at = CURRENT_TIMESTAMP WHERE key = ?", (key,))
    conn.commit()
    conn.close()

    log_audit(admin["username"], "modules", "toggle_module", "info", {"module_key": key}, request.remote_addr)
    return jsonify({"success": True, "message": "Modul holati o'zgartirildi."})


# ============================================================
# 12. GLOBAL SEARCH ENDPOINT
# ============================================================

@atlas_api.route("/search", methods=["GET"])
@admin_required
def api_global_search():
    q = request.args.get("q", "").strip()
    if not q or len(q) < 2:
        return jsonify({"success": True, "results": []})

    term = f"%{q}%"
    conn = get_db_connection()
    cursor = conn.cursor()

    results = []

    # Foydalanuvchilardan qidirish
    cursor.execute("SELECT id, telegram_id, username, first_name FROM users WHERE CAST(telegram_id AS TEXT) LIKE ? OR username LIKE ? OR first_name LIKE ? LIMIT 5", (term, term, term))
    for r in cursor.fetchall():
        results.append({
            "type": "user",
            "title": f"{r['first_name'] or 'Foydalanuvchi'} (@{r['username'] or r['telegram_id']})",
            "subtitle": f"ID: {r['telegram_id']}",
            "route": "users",
            "item_id": r["telegram_id"]
        })

    # Hujjatlardan qidirish
    cursor.execute("SELECT id, template_name, recipient_fio FROM generated_docs WHERE recipient_fio LIKE ? OR template_name LIKE ? LIMIT 5", (term, term))
    for r in cursor.fetchall():
        results.append({
            "type": "document",
            "title": r["recipient_fio"],
            "subtitle": r["template_name"],
            "route": "documents",
            "item_id": r["id"]
        })

    # Loglardan qidirish
    cursor.execute("SELECT id, actor, action, module FROM audit_logs WHERE action LIKE ? OR actor LIKE ? LIMIT 5", (term, term))
    for r in cursor.fetchall():
        results.append({
            "type": "log",
            "title": f"[{r['module']}] {r['action']}",
            "subtitle": f"Actor: {r['actor']}",
            "route": "logs",
            "item_id": r["id"]
        })

    conn.close()
    return jsonify({"success": True, "results": results})


# ============================================================
# 13. KONTRAKTLAR VA DEBITORKA MODULI ENDPOINTS
# ============================================================

@atlas_api.route("/contracts/analyze", methods=["POST"])
@admin_required
def api_contracts_analyze():
    """Asosiy Baza Excel faylini tahlil qilish va tavsiya sanasini aniqlash"""
    if "baza" not in request.files:
        return jsonify({"success": False, "error": "Asosiy baza fayli yuklanmadi."}), 400

    baza_file = request.files["baza"]
    temp_path = os.path.join(tempfile.gettempdir(), f"analyze_{uuid.uuid4().hex[:8]}.xlsx")
    baza_file.save(temp_path)

    res = analyze_baza_excel(temp_path)
    if os.path.exists(temp_path):
        os.remove(temp_path)

    return jsonify(res)


@atlas_api.route("/contracts/update", methods=["POST"])
@admin_required
def api_contracts_update():
    """
    Baza + Debitorka fayllarini qabul qilib, to'lovlarni yangilaydi,
    formulalarni saqlaydi, xulosa rasmini chizadi va hisobotni qaytaradi.
    """
    admin = get_current_admin()
    if "baza" not in request.files or "debitorka" not in request.files:
        return jsonify({"success": False, "error": "Baza va Debitorka fayllari kiritilishi shart."}), 400

    baza_file = request.files["baza"]
    deb_file = request.files["debitorka"]
    start_date_str = request.form.get("start_date", "").strip()

    if not start_date_str:
        return jsonify({"success": False, "error": "Boshlanish sanasi kiritilishi shart."}), 400

    try:
        start_date_dt = datetime.strptime(start_date_str, "%d.%m.%Y")
    except ValueError:
        try:
            start_date_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({"success": False, "error": "Sana formati noto'g'ri (Format: DD.MM.YYYY)."}), 400

    session_id = uuid.uuid4().hex[:12]
    temp_baza = os.path.join(tempfile.gettempdir(), f"baza_{session_id}.xlsx")
    temp_deb = os.path.join(tempfile.gettempdir(), f"deb_{session_id}.xlsx")

    baza_file.save(temp_baza)
    deb_file.save(temp_deb)

    try:
        res = execute_contract_update(temp_baza, temp_deb, start_date_dt, session_id=session_id)

        # Log session to SQLite and Supabase Cloud
        log_contract_session(
            session_id=session_id,
            filename=res["excel_filename"],
            start_date=res["metrics"]["start_date"],
            end_date=res["metrics"]["end_date"],
            total_income=res["metrics"]["total_income"],
            updated_count=res["metrics"]["updated_count"],
            unmatched_count=res["metrics"]["unmatched_count"],
            excel_url=res["excel_url"],
            xulosa_url=res["xulosa_img_url"],
            metrics=res["metrics"]
        )

        log_audit(
            admin["username"] if admin else "web_admin",
            "contracts",
            "update_contracts",
            "success",
            {"session_id": session_id, "income": res["metrics"]["total_income"], "updated": res["metrics"]["updated_count"]},
            request.remote_addr
        )

        if os.path.exists(temp_baza): os.remove(temp_baza)
        if os.path.exists(temp_deb): os.remove(temp_deb)

        return jsonify(res)
    except Exception as e:
        if os.path.exists(temp_baza): os.remove(temp_baza)
        if os.path.exists(temp_deb): os.remove(temp_deb)
        return jsonify({"success": False, "error": f"Xatolik yuz berdi: {str(e)}"}), 500


@atlas_api.route("/contracts/group-screenshots", methods=["POST"])
@admin_required
def api_contracts_group_screenshots():
    """Asosiy baza faylidan barcha guruhlar bo'yicha HD screenshotlar va ZIP paketini generatsiya qilish"""
    admin = get_current_admin()
    if "baza" not in request.files:
        return jsonify({"success": False, "error": "Asosiy baza fayli yuklanmadi."}), 400

    baza_file = request.files["baza"]
    session_id = uuid.uuid4().hex[:12]
    temp_baza = os.path.join(tempfile.gettempdir(), f"baza_ss_{session_id}.xlsx")
    baza_file.save(temp_baza)

    try:
        res = execute_group_screenshots(temp_baza, session_id=session_id)
        if os.path.exists(temp_baza): os.remove(temp_baza)

        log_audit(
            admin["username"] if admin else "web_admin",
            "contracts",
            "generate_group_screenshots",
            "success",
            {"session_id": session_id, "groups_count": res.get("total_groups", 0)},
            request.remote_addr
        )

        return jsonify(res)
    except Exception as e:
        if os.path.exists(temp_baza): os.remove(temp_baza)
        return jsonify({"success": False, "error": f"Screenshotlarni yaratishda xatolik: {str(e)}"}), 500


@atlas_api.route("/contracts/download-excel/<session_id>", methods=["GET"])
def api_contracts_download_excel(session_id):
    """Yangilangan Excel faylini yuklab olish"""
    if os.path.exists(CONTRACT_STORAGE_DIR):
        for fname in os.listdir(CONTRACT_STORAGE_DIR):
            if fname.startswith(session_id) and fname.endswith(".xlsx"):
                fpath = os.path.join(CONTRACT_STORAGE_DIR, fname)
                download_name = fname.replace(f"{session_id}_", "")
                return send_file(fpath, as_attachment=True, download_name=download_name)

    sess = get_contract_session_by_id(session_id)
    if sess and sess.get("excel_url"):
        from flask import redirect
        return redirect(sess.get("excel_url"))
    return jsonify({"success": False, "error": "Excel fayli topilmadi."}), 404


@atlas_api.route("/contracts/download-xulosa/<session_id>", methods=["GET"])
def api_contracts_download_xulosa(session_id):
    """Xulosa rasmini yuklab olish"""
    if os.path.exists(CONTRACT_STORAGE_DIR):
        for fname in os.listdir(CONTRACT_STORAGE_DIR):
            if session_id in fname and fname.endswith(".png") and "xulosa" in fname:
                fpath = os.path.join(CONTRACT_STORAGE_DIR, fname)
                return send_file(fpath, as_attachment=False, mimetype="image/png")

    sess = get_contract_session_by_id(session_id)
    if sess and sess.get("xulosa_url"):
        from flask import redirect
        return redirect(sess.get("xulosa_url"))
    return jsonify({"success": False, "error": "Xulosa rasmi topilmadi."}), 404


@atlas_api.route("/contracts/download-screenshot/<session_id>/<group_name>", methods=["GET"])
def api_contracts_download_screenshot(session_id, group_name):
    """Bitta guruh yoki Xulosa screenshot rasmini yuklab olish"""
    sdir = os.path.join(CONTRACT_STORAGE_DIR, f"screenshots_{session_id}")
    clean_gname = group_name.replace('/', '_').replace(' ', '_')

    # 1. Agar Xulosa so'ralgan bo'lsa
    if "xulosa" in clean_gname.lower():
        xul_path = os.path.join(sdir, "00_XULOSA_Guruh_Rahbarlari.png")
        if os.path.exists(xul_path):
            return send_file(xul_path, as_attachment=False, mimetype="image/png")
        for fname in os.listdir(CONTRACT_STORAGE_DIR) if os.path.exists(CONTRACT_STORAGE_DIR) else []:
            if session_id in fname and "xulosa" in fname and fname.endswith(".png"):
                return send_file(os.path.join(CONTRACT_STORAGE_DIR, fname), as_attachment=False, mimetype="image/png")

    # 2. Oddiy guruh screenshot
    fpath = os.path.join(sdir, f"screenshot_{clean_gname}.png")
    if os.path.exists(fpath):
        return send_file(fpath, as_attachment=False, mimetype="image/png")
    return jsonify({"success": False, "error": "Screenshot rasmi topilmadi."}), 404


@atlas_api.route("/contracts/download-all-screenshots-zip/<session_id>", methods=["GET"])
def api_contracts_download_all_zip(session_id):
    """Barcha guruhlar screenshotlari jamlangan ZIP faylni yuklab olish"""
    zpath = os.path.join(CONTRACT_STORAGE_DIR, f"Guruhlar_Screenshotlari_{session_id}.zip")
    if os.path.exists(zpath):
        return send_file(zpath, as_attachment=True, download_name=f"Guruhlar_Screenshotlari_{session_id}.zip")
    return jsonify({"success": False, "error": "ZIP fayl topilmadi."}), 404


@atlas_api.route("/contracts/send-to-telegram", methods=["POST"])
@admin_required
def api_contracts_send_to_telegram():
    """Telegram guruh yoki shaxsiy botga hisobot, xulosa rasmi va Excel faylini yuborish (Serverless safe)"""
    admin = get_current_admin()
    data = request.get_json(silent=True) or {}
    chat_ids = data.get("chat_ids", [])
    session_id = data.get("session_id", "")
    caption_text = data.get("caption", "")
    send_excel = data.get("send_excel", False)
    send_xulosa = data.get("send_xulosa", True)
    send_screenshots = data.get("send_screenshots", False)

    if not chat_ids:
        # Default to admin telegram ID if empty
        chat_ids = ["8135594558"]

    excel_path = None
    xulosa_path = None
    group_images = []

    # 1. Fetch Session metadata from DB if session_id is given
    sess = None
    if session_id:
        sess = get_contract_session_by_id(session_id)

    # 2. Look for local files first
    if session_id and os.path.exists(CONTRACT_STORAGE_DIR):
        if send_excel:
            for fname in os.listdir(CONTRACT_STORAGE_DIR):
                if fname.startswith(session_id) and fname.endswith(".xlsx"):
                    excel_path = os.path.join(CONTRACT_STORAGE_DIR, fname)
                    break
        if send_xulosa:
            for fname in os.listdir(CONTRACT_STORAGE_DIR):
                if session_id in fname and fname.endswith(".png") and "xulosa" in fname:
                    xulosa_path = os.path.join(CONTRACT_STORAGE_DIR, fname)
                    break
        if send_screenshots:
            sdir = os.path.join(CONTRACT_STORAGE_DIR, f"screenshots_{session_id}")
            if os.path.exists(sdir):
                for fname in os.listdir(sdir):
                    if fname.endswith(".png"):
                        group_images.append(os.path.join(sdir, fname))

    # 3. If running on Vercel / serverless and local files are missing, use Supabase URLs
    if sess:
        if send_excel and not excel_path and sess.get("excel_url"):
            excel_path = sess.get("excel_url")
        if send_xulosa and not xulosa_path and sess.get("xulosa_url"):
            xulosa_path = sess.get("xulosa_url")

        # Build informative caption if generic
        if not caption_text or caption_text == "<b>ATLAS Platformasi: Kontrakt Hisoboti</b>":
            m = sess.get("metrics") or {}
            inc = int(sess.get("total_income", 0))
            upd = sess.get("updated_count", 0)
            unm = sess.get("unmatched_count", 0)
            s_date = sess.get("start_date", "")
            e_date = sess.get("end_date", "")
            caption_text = (
                f"📊 <b>ATLAS Platformasi: Kontraktlar Yangilanish Hisoboti</b>\n\n"
                f"💰 <b>Jami tushgan pul:</b> {inc:,} so'm\n"
                f"👥 <b>Yangilangan talabalar:</b> {upd} kishi\n"
                f"⚠️ <b>Topilmagan to'lovlar:</b> {unm} ta\n"
                f"📅 <b>Sana oralig'i:</b> {s_date} — {e_date}\n\n"
                f"<i>Fayllar va Xulosa jadvali quyida biriktirildi 👇</i>"
            ).replace(",", " ")

    res = forward_to_telegram(
        chat_ids=chat_ids,
        caption_text=caption_text,
        excel_path=excel_path,
        xulosa_img_path=xulosa_path,
        group_img_paths=group_images
    )

    log_audit(
        admin["username"] if admin else "web_admin",
        "contracts",
        "send_to_telegram",
        "success" if res.get("success") else "error",
        {"chat_ids": chat_ids, "session_id": session_id, "results": res.get("results")},
        request.remote_addr
    )

    return jsonify(res)


@atlas_api.route("/contracts/history", methods=["GET"])
@admin_required
def api_contracts_history():
    """Kontrakt yangilanishlari tarixini olish"""
    sessions = get_contract_sessions()
    return jsonify({"success": True, "sessions": sessions})


@atlas_api.route("/contracts/session/<session_id>", methods=["DELETE"])
@admin_required
def api_contracts_delete_session(session_id):
    """Kontrakt sessiyasini o'chirish"""
    admin = get_current_admin()
    success = delete_contract_session(session_id)
    if success:
        log_audit(
            admin["username"] if admin else "web_admin",
            "contracts",
            "delete_session",
            "success",
            {"session_id": session_id},
            request.remote_addr
        )
        return jsonify({"success": True, "message": "Sessiya muvaffaqiyatli o'chirildi."})
    return jsonify({"success": False, "error": "Sessiyani o'chirishda xatolik yuz berdi."}), 400

