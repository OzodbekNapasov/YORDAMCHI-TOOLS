import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict

# Telegram 64-byte callback_data cheklovini aylanib o'tish uchun yo'llar kesh-xotirasi (PATH_CACHE)
PATH_CACHE: Dict[int, str] = {}
REVERSE_PATH_CACHE: Dict[str, int] = {}
CACHE_COUNTER = 0

def get_path_id(path: str) -> int:
    global CACHE_COUNTER
    norm_path = os.path.abspath(path)
    if norm_path in REVERSE_PATH_CACHE:
        return REVERSE_PATH_CACHE[norm_path]
    CACHE_COUNTER += 1
    PATH_CACHE[CACHE_COUNTER] = norm_path
    REVERSE_PATH_CACHE[norm_path] = CACHE_COUNTER
    return CACHE_COUNTER

def get_path_by_id(path_id: int) -> str:
    return PATH_CACHE.get(path_id)


def get_pc_control_keyboard():
    """2-DARAJALI PAPKA: Kompyuter Boshqaruvi Asosiy Menyusi"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_status = KeyboardButton("📊 Tizim Holati")
    btn_shot = KeyboardButton("🖼 Skrinshot")
    btn_cam = KeyboardButton("📷 Veb-kamera")
    btn_files = KeyboardButton("📁 Papka va Fayllar")
    btn_apps = KeyboardButton("🎮 Dasturlar (TOP-20)")
    btn_cmd = KeyboardButton("📝 CMD Buyruq")
    btn_power = KeyboardButton("⚡ Quvvat Boshqaruvi")
    btn_media = KeyboardButton("🔊 Ovoz & Yorqinlik")
    btn_clean = KeyboardButton("🧹 Kesh & Korzina Tozalash")
    btn_ai = KeyboardButton("🧠 AI Yordamchi (PC Agent)")
    btn_back = KeyboardButton("🔙 Asosiy menyuga qaytish")

    markup.add(btn_status, btn_shot)
    markup.add(btn_cam, btn_files)
    markup.add(btn_apps, btn_cmd)
    markup.add(btn_power, btn_media)
    markup.add(btn_clean, btn_ai)
    markup.add(btn_back)
    return markup


def get_power_inline_keyboard():
    """Quvvat boshqaruvi Inline menyusi"""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("⚡ O'chirish (Shutdown)", callback_data="pc_power_ask:shutdown"),
        InlineKeyboardButton("🔄 Qayta yuklash (Restart)", callback_data="pc_power_ask:restart"),
        InlineKeyboardButton("🌙 Uyqu rejimi (Sleep)", callback_data="pc_power_do:sleep"),
        InlineKeyboardButton("🔒 Ekranni qulflash (Lock)", callback_data="pc_power_do:lock"),
        InlineKeyboardButton("❌ O'chirishni bekor qilish", callback_data="pc_power_do:cancel")
    )
    return markup


def get_confirmation_inline(action: str):
    """O'chirish yoki qayta yuklashni tasdiqlash tugmalari"""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✅ Ha, bajaring", callback_data=f"pc_power_do:{action}"),
        InlineKeyboardButton("❌ Bekor qilish", callback_data="pc_power_cancel")
    )
    return markup


def get_volume_inline():
    """Ovoz sozlamalari inline klaviaturasi"""
    markup = InlineKeyboardMarkup(row_width=4)
    markup.add(
        InlineKeyboardButton("🔇 Mute", callback_data="pc_vol_mute"),
        InlineKeyboardButton("🔈 25%", callback_data="pc_vol:25"),
        InlineKeyboardButton("🔉 50%", callback_data="pc_vol:50"),
        InlineKeyboardButton("🔊 100%", callback_data="pc_vol:100")
    )
    return markup


def get_brightness_inline():
    """Ekran yorqinligi inline klaviaturasi"""
    markup = InlineKeyboardMarkup(row_width=4)
    markup.add(
        InlineKeyboardButton("🌙 25%", callback_data="pc_bright:25"),
        InlineKeyboardButton("⛅ 50%", callback_data="pc_bright:50"),
        InlineKeyboardButton("🌤 75%", callback_data="pc_bright:75"),
        InlineKeyboardButton("☀️ 100%", callback_data="pc_bright:100")
    )
    return markup


def get_cleanup_inline():
    """Tozalash inline klaviaturasi"""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🗑 Korzinani tozalash", callback_data="pc_clean_recycle"),
        InlineKeyboardButton("🧹 Temp keshni tozalash", callback_data="pc_clean_temp")
    )
    return markup


def get_ai_mode_keyboard():
    """AI Agent rejimida chiqish klaviaturasi"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_clear = KeyboardButton("🧹 Chat xotirasini tozalash")
    btn_exit = KeyboardButton("❌ AI Rejimidan chiqish")
    markup.add(btn_clear, btn_exit)
    return markup


ITEMS_PER_PAGE = 8

def make_explorer_markup(dir_path: str, parent_dir: str, dirs: list, files: list, page: int = 0):
    """File Explorer uchun Inline sahifalangan klaviatura"""
    markup = InlineKeyboardMarkup(row_width=1)
    dir_id = get_path_id(dir_path)

    # 1. Yuqoriga (Orqaga)
    if parent_dir and parent_dir != dir_path:
        parent_id = get_path_id(parent_dir)
        markup.add(InlineKeyboardButton("⬆️ Yuqoriga (Orqaga)", callback_data=f"exp_op:{parent_id}:0"))

    # 2. ZIP Arxivlash tugmasi
    markup.add(InlineKeyboardButton("📦 Ushbu papkani ZIP qilib yuklab olish", callback_data=f"exp_zp:{dir_id}"))

    # Barcha elementlar (papkalar va fayllar)
    all_items = []
    for d in dirs:
        all_items.append({"type": "dir", "name": d, "path": os.path.join(dir_path, d)})
    for f in files:
        all_items.append({"type": "file", "name": f, "path": os.path.join(dir_path, f)})

    total_items = len(all_items)
    total_pages = max(1, (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
    page = max(0, min(page, total_pages - 1))

    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_items = all_items[start_idx:end_idx]

    # Elementlar tugmalari
    for item in page_items:
        item_id = get_path_id(item["path"])
        name = item["name"]
        if item["type"] == "dir":
            markup.add(InlineKeyboardButton(f"📁 {name[:24]}", callback_data=f"exp_op:{item_id}:0"))
        else:
            icon = "🔗" if name.lower().endswith(".lnk") else "📄"
            markup.add(InlineKeyboardButton(f"{icon} {name[:24]}", callback_data=f"exp_fl:{item_id}"))

    # Pagination (Sahifalash)
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Avvalgi", callback_data=f"exp_op:{dir_id}:{page - 1}"))
    if total_pages > 1:
        nav_row.append(InlineKeyboardButton(f"📄 {page + 1}/{total_pages}", callback_data="exp_noop"))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("Keyingi ➡️", callback_data=f"exp_op:{dir_id}:{page + 1}"))

    if nav_row:
        markup.row(*nav_row)

    return markup, page, total_pages
