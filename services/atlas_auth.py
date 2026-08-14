# ============================================================
#  services/atlas_auth.py
#  ATLAS Platformasi — Xavfsiz Autentifikatsiya va Session Tizimi
# ============================================================

import os
import time
import secrets
import hashlib
from functools import wraps
from flask import request, jsonify, session, make_response
from services.atlas_db import get_db_connection, log_audit

SECRET_KEY = os.environ.get("ATLAS_SECRET_KEY") or "atlas_production_secret_key_998_2026"
ACTIVE_SESSIONS = {}  # token -> {user_id, username, role, expires_at}
SESSION_DURATION_HOURS = 24


def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """PBKDF2-HMAC-SHA256 yordamida parolni xavfsiz heshlash"""
    if not salt:
        salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return pwd_hash, salt


def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    """Parol to'g'riligini doimiy vaqtli solishtirish orqali tekshirish"""
    computed_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(computed_hash, expected_hash)


def create_session(admin_id: int, username: str, full_name: str, role: str) -> str:
    """Yangi xavfsiz session token yaratish"""
    token = secrets.token_urlsafe(32)
    expires_at = time.time() + (SESSION_DURATION_HOURS * 3600)
    ACTIVE_SESSIONS[token] = {
        "id": admin_id,
        "username": username,
        "full_name": full_name,
        "role": role,
        "expires_at": expires_at
    }
    return token


def get_current_admin():
    """Joriy so'rovdan admin ma'lumotlarini olish (Header yoki Cookie orqali)"""
    auth_header = request.headers.get("Authorization", "")
    token = None

    if auth_header.startswith("Bearer "):
        token = auth_header[7:].strip()
    elif "atlas_token" in request.cookies:
        token = request.cookies.get("atlas_token")

    if not token or token not in ACTIVE_SESSIONS:
        return None

    sess = ACTIVE_SESSIONS[token]
    if time.time() > sess["expires_at"]:
        del ACTIVE_SESSIONS[token]
        return None

    return sess


def admin_required(f):
    """Faqat tizim ma'murlari kira oladigan API himoyalovchisi"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = get_current_admin()
        if not admin:
            return jsonify({
                "success": False,
                "error": "Autentifikatsiya talab qilinadi. Iltimos, qayta kiring."
            }), 401
        return f(*args, **kwargs)
    return decorated_function


def authenticate_admin(username, password, ip_address=""):
    """Administrator login tekshiruvi"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE username = ?", (username.strip(),))
    admin = cursor.fetchone()

    if not admin:
        log_audit(username, "auth", "login_failed", "warning", {"reason": "User not found"}, ip_address)
        conn.close()
        return None, "Foydalanuvchi nomi yoki parol noto'g'ri."

    if not verify_password(password, admin["salt"], admin["password_hash"]):
        log_audit(username, "auth", "login_failed", "warning", {"reason": "Invalid password"}, ip_address)
        conn.close()
        return None, "Foydalanuvchi nomi yoki parol noto'g'ri."

    cursor.execute("UPDATE admins SET last_login_at = CURRENT_TIMESTAMP WHERE id = ?", (admin["id"],))
    conn.commit()
    conn.close()

    token = create_session(admin["id"], admin["username"], admin["full_name"], admin["role"])
    log_audit(admin["username"], "auth", "login_success", "success", {"full_name": admin["full_name"]}, ip_address)

    return {
        "token": token,
        "user": {
            "id": admin["id"],
            "username": admin["username"],
            "full_name": admin["full_name"],
            "role": admin["role"]
        }
    }, None
