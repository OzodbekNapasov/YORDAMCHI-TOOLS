# ============================================================
#  docbot_config.py — Shablonlar, Buyruqlar va Maydonlar Sozlamalari
# ============================================================

import os
import json
from datetime import datetime
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_template_file(filename="malumotnoma.docx"):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(curr_dir, "templates", filename),
        os.path.join(curr_dir, "templates", "Buyruqlar", filename),
        os.path.join(curr_dir, "..", "templates", filename),
        os.path.join(curr_dir, "..", "templates", "Buyruqlar", filename),
        os.path.join(os.getcwd(), "templates", filename),
        os.path.join(os.getcwd(), "templates", "Buyruqlar", filename),
        os.path.join(os.getcwd(), filename),
        f"/var/task/templates/{filename}",
        f"/var/task/templates/Buyruqlar/{filename}",
        f"/var/task/{filename}",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]

today_str = datetime.now().strftime("%d.%m.%Y")

# ============================================================
# 1. MA'LUMOTNOMALAR SHABLONLARI
# ============================================================
MALUMOTNOMA_TEMPLATES = [
    {
        "id": "qabul_1_kurs",
        "category": "malumotnoma",
        "name": "🎓 1-kursga qabul",
        "file": find_template_file("malumotnoma.docx"),
        "filename": "malumotnoma.docx",
        "steps": [
            {
                "field": "FIO",
                "question": "👤 Talabaning F.I.O ni kiriting:\n<i>(Masalan: Napasov Ozodbek Zafar o’g’li)</i>",
                "buttons": None
            },
            {
                "field": "YONALISH",
                "question": "📚 Yo'nalishni tanlang yoki kiriting:",
                "buttons": [
                    ["Hamshiralik ishi"],
                    ["Davolash ishi (Feldsherlik)"],
                    ["Farmatsiya"],
                    ["Stomatologiya ishi"]
                ]
            },
            {
                "field": "OQUV_YILI",
                "question": "📅 O'quv yilini tanlang yoki kiriting:",
                "buttons": [
                    ["2026/2027", "2025/2026"]
                ]
            },
            {
                "field": "SANA",
                "question": "📆 Berilgan sanani tanlang yoki qo'lda kiriting:",
                "buttons": [
                    [today_str]
                ]
            }
        ]
    },
    {
        "id": "oqiyapti",
        "category": "malumotnoma",
        "name": "📖 O'qiyotganligi haqida",
        "file": find_template_file("malumotnoma — O'qiyapti degan.docx"),
        "filename": "malumotnoma — O'qiyapti degan.docx",
        "steps": [
            {
                "field": "FIO",
                "question": "👤 Talabaning F.I.O ni kiriting:\n<i>(Masalan: Napasov Ozodbek Zafar o’g’li)</i>",
                "buttons": None
            },
            {
                "field": "YONALISH",
                "question": "📚 Yo'nalishni tanlang yoki kiriting:",
                "buttons": [
                    ["Hamshiralik ishi"],
                    ["Davolash ishi (Feldsherlik)"],
                    ["Farmatsiya"],
                    ["Stomatologiya ishi"]
                ]
            },
            {
                "field": "OQUV_YILI",
                "question": "📅 Qaysi o'quv yilida qabul qilingan:\n<i>(Masalan: 2024/2025)</i>",
                "buttons": [
                    ["2025/2026", "2024/2025"],
                    ["2023/2024", "2026/2027"]
                ]
            },
            {
                "field": "KURSI",
                "question": "🎯 Nechanchi kursda o'qimoqda?",
                "buttons": [
                    ["1", "2"],
                    ["3", "4"]
                ]
            },
            {
                "field": "GURUHI",
                "question": "👥 Guruh raqami yoki nomini kiriting:\n<i>(Masalan: 201 yoki 102)</i>",
                "buttons": None
            },
            {
                "field": "SANA",
                "question": "📆 Berilgan sanani tanlang yoki qo'lda kiriting:",
                "buttons": [
                    [today_str]
                ]
            }
        ]
    }
]

# ============================================================
# 2. RASMIY BUYRUQLAR SHABLONLARI (4 TURDAGI)
# ============================================================
BUYRUQ_TEMPLATES = [
    {
        "id": "buyruq_akademik_tatil",
        "category": "buyruq",
        "name": "📝 Akademik ta'til berish",
        "file": find_template_file("Akademik ta'til berish.docx"),
        "filename": "Akademik ta'til berish.docx",
        "steps": [
            {
                "field": "buyruq_raqami",
                "question": "🔢 Buyruq raqamini kiriting:\n<i>(Masalan: 14-B yoki 104)</i>",
                "buttons": None
            },
            {
                "field": "sanasi",
                "question": "📆 Buyruq sanasini tanlang yoki kiriting:",
                "buttons": [
                    [today_str]
                ]
            },
            {
                "field": "kursi",
                "question": "🎯 Talabaning bosqichi (kursi):",
                "buttons": [
                    ["1", "2"],
                    ["3", "4"]
                ]
            },
            {
                "field": "guruhi",
                "question": "👥 Guruh raqamini kiriting:\n<i>(Masalan: 204)</i>",
                "buttons": None
            },
            {
                "field": "IFO",
                "question": "👤 Talabaning F.I.O ni kiriting:\n<i>(Masalan: Napasov Ozodbek Zafar o’g’li)</i>",
                "buttons": None
            }
        ]
    },
    {
        "id": "buyruq_qayta_tiklash",
        "category": "buyruq",
        "name": "📝 Akademik ta'tildan qayta tiklash",
        "file": find_template_file("Akademik ta'tildan qayta tiklash.docx"),
        "filename": "Akademik ta'tildan qayta tiklash.docx",
        "steps": [
            {
                "field": "buyruq_raqami",
                "question": "🔢 Yangi buyruq raqamini kiriting:\n<i>(Masalan: 18-B)</i>",
                "buttons": None
            },
            {
                "field": "sanasi",
                "question": "📆 Buyruq sanasini tanlang yoki kiriting:",
                "buttons": [
                    [today_str]
                ]
            },
            {
                "field": "avvalgi_buyruq_raqami",
                "question": "📄 Avvalgi buyruq raqami:\n<i>(Masalan: 14-B)</i>",
                "buttons": None
            },
            {
                "field": "avvalgi_buyruq_sanasi",
                "question": "📅 Avvalgi buyruq sanasi:\n<i>(Masalan: 10.02.2025)</i>",
                "buttons": None
            },
            {
                "field": "kursi",
                "question": "🎯 Kursini tanlang:",
                "buttons": [
                    ["1", "2"],
                    ["3", "4"]
                ]
            },
            {
                "field": "avvalgi_guruhi",
                "question": "👥 Avvalgi guruhi:\n<i>(Masalan: 204)</i>",
                "buttons": None
            },
            {
                "field": "yangi_guruhi",
                "question": "👥 Yangi tiklanayotgan guruhi:\n<i>(Masalan: 205)</i>",
                "buttons": None
            },
            {
                "field": "IFO",
                "question": "👤 Talabaning F.I.O ni kiriting:\n<i>(Masalan: Napasov Ozodbek Zafar o’g’li)</i>",
                "buttons": None
            }
        ]
    },
    {
        "id": "buyruq_guruhdan_guruhga",
        "category": "buyruq",
        "name": "📝 Guruhdan guruhga o'tkazish",
        "file": find_template_file("Guruhdan guruhga o`tkazish.docx"),
        "filename": "Guruhdan guruhga o`tkazish.docx",
        "steps": [
            {
                "field": "buyruq_raqami",
                "question": "🔢 Buyruq raqamini kiriting:\n<i>(Masalan: 22-B)</i>",
                "buttons": None
            },
            {
                "field": "sanasi",
                "question": "📆 Buyruq sanasini tanlang yoki kiriting:",
                "buttons": [
                    [today_str]
                ]
            },
            {
                "field": "yonalishi",
                "question": "📚 Ta'lim yo'nalishini tanlang:",
                "buttons": [
                    ["Hamshiralik ishi"],
                    ["Davolash ishi (Feldsherlik)"],
                    ["Farmatsiya"],
                    ["Stomatologiya ishi"]
                ]
            },
            {
                "field": "IFO",
                "question": "👤 Talabaning F.I.O ni kiriting:\n<i>(Masalan: Napasov Ozodbek Zafar o’g’li)</i>",
                "buttons": None
            },
            {
                "field": "avvalgi_guruhi",
                "question": "👥 Qaysi guruhdan o'tkazilmoqda:\n<i>(Masalan: 102)</i>",
                "buttons": None
            },
            {
                "field": "yangi_guruhi",
                "question": "👥 Qaysi guruhga o'tkazilmoqda:\n<i>(Masalan: 105)</i>",
                "buttons": None
            }
        ]
    },
    {
        "id": "buyruq_safidan_chiqarish",
        "category": "buyruq",
        "name": "📝 Talabalar safidan chiqarish",
        "file": find_template_file("Talabalar safidan chiqarish - 1-asos.docx"),
        "filename": "Talabalar safidan chiqarish - 1-asos.docx",
        "steps": [
            {
                "field": "asos_turi",
                "question": "⚖️ Chiqarish asosini tanlang:",
                "buttons": [
                    ["Talaba arizasi"],
                    ["Rahbarini bildirgisi"]
                ]
            },
            {
                "field": "buyruq_raqami",
                "question": "🔢 Buyruq raqamini kiriting:\n<i>(Masalan: 35-B)</i>",
                "buttons": None
            },
            {
                "field": "sanasi",
                "question": "📆 Buyruq sanasini tanlang yoki kiriting:",
                "buttons": [
                    [today_str]
                ]
            },
            {
                "field": "kursi",
                "question": "🎯 Kursini tanlang:",
                "buttons": [
                    ["1", "2"],
                    ["3", "4"]
                ]
            },
            {
                "field": "avvalgi_guruhi",
                "question": "👥 Guruhi:\n<i>(Masalan: 101)</i>",
                "buttons": None
            },
            {
                "field": "IFO",
                "question": "👤 Talabaning F.I.O ni kiriting:\n<i>(Masalan: Napasov Ozodbek Zafar o’g’li)</i>",
                "buttons": None
            }
        ]
    }
]

# Barcha birlashtirilgan shablonlar
TEMPLATES = MALUMOTNOMA_TEMPLATES + BUYRUQ_TEMPLATES

is_serverless = os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME") or os.path.exists("/tmp")
TEMP_DIR = "/tmp" if is_serverless else os.path.join(BASE_DIR, "temp")
try:
    os.makedirs(TEMP_DIR, exist_ok=True)
except Exception:
    pass
