# ============================================================
#  services/atlas_auth.py
#  ATLAS Platformasi — Xavfsiz Autentifikatsiya va Stateless Session Tizimi
#  Vercel Serverless & Multi-Instance Muammosiz 100% Stateless HMAC Tokenlar
# ============================================================

import os
import time
import json
import base64
import hmac
import hashlib
import secrets
from functools import wraps
from flask import request, jsonify, make_response
from services.atlas_db import get_db_connection, log_audit

SECRET_KEY = os.environ.get("ATLAS_SECRET_KEY") or "atlas_production_secret_key_998_2026_super_secure"
SESSION_DURATION_HOURS = 24 * 7  # 7 kunlik doimiy session


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
    """
    Stateless HMAC-SHA256 Signed Token yaratish.
    Vercel serverless lambda muhitlarida har bir so'rov turli instansiyalarga tushganda ham
    sessiya hech qachon yo'qolmaydi va chiqib ketmaydi.
    """
    payload = {
        "id": admin_id,
        "username": username,
        "full_name": full_name,
        "role": role,
        "exp": int(time.time()) + (SESSION_DURATION_HOURS * 3600)
    }
    payload_json = json.dumps(payload, separators=(',', ':'))
    payload_b64 = base64.urlsafe_b64encode(payload_json.encode('utf-8')).decode('utf-8').rstrip('=')
    sig = hmac.new(SECRET_KEY.encode('utf-8'), payload_b64.encode('utf-8'), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{sig}"


def get_current_admin():
    """Joriy so'rovdan admin ma'lumotlarini olish va HMAC imzosini tekshirish"""
    auth_header = request.headers.get("Authorization", "")
    token = None

    if auth_header.startswith("Bearer "):
        token = auth_header[7:].strip()
    elif "atlas_token" in request.cookies:
        token = request.cookies.get("atlas_token")

    if not token or "." not in token:
        return None

    try:
        payload_b64, sig = token.split(".", 1)
        expected_sig = hmac.new(SECRET_KEY.encode('utf-8'), payload_b64.encode('utf-8'), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None

        # Base64 padding
        rem = len(payload_b64) % 4
        if rem > 0:
            payload_b64 += '=' * (4 - rem)

        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode('utf-8')).decode('utf-8'))
        if time.time() > payload.get("exp", 0):
            return None

        return {
            "id": payload.get("id", 1),
            "username": payload.get("username", "Ozodbek"),
            "full_name": payload.get("full_name", "Ozodbek Napasov"),
            "role": payload.get("role", "superadmin")
        }
    except Exception:
        return None


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

    # Zaxira tekshiruv: agar DB da bo'lmasa yoki yangilanmagan bo'lsa
    if not admin and username.strip().lower() == "ozodbek" and password == "Eua5gd007":
        from hashlib import pbkdf2_hmac
        salt = "atlas_secure_salt_2026"
        pwd_hash = pbkdf2_hmac('sha256', "Eua5gd007".encode('utf-8'), salt.encode('utf-8'), 100000).hex()
        cursor.execute("""
        INSERT OR REPLACE INTO admins (id, username, password_hash, salt, full_name, role)
        VALUES (1, 'Ozodbek', ?, ?, 'Ozodbek Napasov', 'superadmin')
        """, (pwd_hash, salt))
        conn.commit()
        cursor.execute("SELECT * FROM admins WHERE username = 'Ozodbek'")
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
