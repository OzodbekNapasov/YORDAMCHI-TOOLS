# ============================================================
#  services/app_secrets.py
#  Maxfiy kalitlarni (bot tokeni, webhook siri, sessiya kaliti) faqat
#  muhit o'zgaruvchilaridan (.env / Vercel Environment Variables) o'qish.
#  Kodga token yozib qo'yish taqiqlanadi: repozitoriy ochiq (public).
# ============================================================

import os
import hmac
import hashlib
import secrets

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# TeleBot bo'sh tokenni qabul qilmaydi (ValueError). Token qo'yilmagan bo'lsa ham
# veb-panel ishlab turishi uchun shu soxta qiymat ishlatiladi — Telegram uni rad etadi.
MISSING_TOKEN_PLACEHOLDER = "0:BOT_TOKEN_NOT_CONFIGURED"


def get_bot_token() -> str:
    """Asosiy Telegram bot tokeni (BOT_TOKEN yoki TOKEN). Topilmasa bo'sh satr."""
    return (os.environ.get("BOT_TOKEN") or os.environ.get("TOKEN") or "").strip()


def get_bot_token_or_placeholder() -> str:
    token = get_bot_token()
    if not token:
        print("[SECURITY WARN]: BOT_TOKEN muhit o'zgaruvchisi o'rnatilmagan! Bot ishlamaydi.")
        return MISSING_TOKEN_PLACEHOLDER
    return token


def redact_secrets(text) -> str:
    """Xato matnlaridan bot tokenini yashirish (requests xatolari URL'ni, ya'ni tokenni ham ko'rsatadi)."""
    text = str(text)
    for tok in {get_bot_token(), (os.environ.get("INSTA_BOT_TOKEN") or "").strip()}:
        if tok:
            text = text.replace(tok, "<BOT_TOKEN>")
    return text


def get_primary_admin_id() -> int:
    return int(os.environ.get("PRIMARY_ADMIN_ID") or os.environ.get("ADMIN_ID") or 8135594558)


def _derive(label: str) -> str:
    """Bot tokenidan (u maxfiy) barqaror yordamchi sir hosil qilish."""
    base = get_bot_token()
    if not base:
        return ""
    return hmac.new(base.encode("utf-8"), label.encode("utf-8"), hashlib.sha256).hexdigest()


def get_webhook_secret() -> str:
    """Telegram webhook so'rovlaridagi X-Telegram-Bot-Api-Secret-Token qiymati.

    Telegram faqat A-Z, a-z, 0-9, _ va - belgilarini (1-256) qabul qiladi;
    hex-digest shunga mos.
    """
    return (os.environ.get("TELEGRAM_WEBHOOK_SECRET") or "").strip() or _derive("atlas-telegram-webhook")[:64]


def get_session_secret() -> str:
    """Veb-panel sessiya tokenlarini imzolash kaliti."""
    global _PROCESS_SESSION_SECRET
    key = (os.environ.get("ATLAS_SECRET_KEY") or "").strip() or _derive("atlas-session-key")
    if key:
        return key
    # Hech qanday sir yo'q: taxmin qilib bo'lmaydigan, faqat shu jarayonga tegishli kalit
    if not _PROCESS_SESSION_SECRET:
        _PROCESS_SESSION_SECRET = secrets.token_hex(32)
    return _PROCESS_SESSION_SECRET


_PROCESS_SESSION_SECRET = ""
