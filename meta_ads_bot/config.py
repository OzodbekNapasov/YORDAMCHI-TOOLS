import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file (prioritize local meta_ads_bot/.env then parent .env)
BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent

if (BASE_DIR / ".env").exists():
    load_dotenv(BASE_DIR / ".env")
elif (PARENT_DIR / ".env").exists():
    load_dotenv(PARENT_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("META_BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_USER_ID = int(os.getenv("PRIMARY_ADMIN_ID") or os.getenv("ALLOWED_USER_ID") or os.getenv("META_ADMIN_ID") or "8135594558")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID", "")

# Ensure AD_ACCOUNT_ID has 'act_' prefix
if AD_ACCOUNT_ID and not AD_ACCOUNT_ID.startswith("act_"):
    AD_ACCOUNT_ID = f"act_{AD_ACCOUNT_ID}"

META_API_VERSION = "v19.0"
META_GRAPH_URL = f"https://graph.facebook.com/{META_API_VERSION}"
