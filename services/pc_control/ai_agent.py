import os
import sys
import json
import logging
import requests
import base64
from typing import Dict, List

from .system_tools import (
    execute_cmd_sync,
    get_system_status,
    take_screenshot,
    show_popup,
    kill_process,
    click_screen,
    press_key,
    set_brightness,
    open_app,
    show_desktop,
    close_active_window,
    empty_recycle_bin,
    clean_temp_files,
    type_text,
    scroll_page,
    set_volume,
    set_mute,
    media_control
)

logger = logging.getLogger(__name__)

def _get_openrouter_key():
    k = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not k:
        env_paths = [".env", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")]
        for ep in env_paths:
            if os.path.exists(ep):
                try:
                    with open(ep, "r", encoding="utf-8") as f:
                        for line in f:
                            if line.strip().startswith("OPENROUTER_API_KEY="):
                                k = line.strip().split("=", 1)[1].strip()
                                break
                except Exception:
                    pass
            if k:
                break
    return k

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# OpenRouter uchun eng optimal, arzon va o'zbek tilida aniq ishlovchi modellar:
# 1. deepseek/deepseek-chat (DeepSeek V3: $0.14/M token - eng aqlli va o'ta arzon)
# 2. meta-llama/llama-3.1-8b-instruct ($0.05/M token - eng tezkor)
# 3. openai/gpt-4o-mini ($0.15/M token - barqaror zaxira)
# 4. meta-llama/llama-3.3-70b-instruct ($0.12/M token - chuqur mantiqiy)
OPENROUTER_MODELS = [
    "deepseek/deepseek-chat",
    "meta-llama/llama-3.1-8b-instruct",
    "openai/gpt-4o-mini",
    "meta-llama/llama-3.3-70b-instruct",
]

# Foydalanuvchilar chat tarixini saqlash uchun xotira
CHAT_HISTORIES: Dict[int, List[Dict[str, str]]] = {}

def clear_user_history(user_id: int):
    CHAT_HISTORIES.pop(user_id, None)

AGENT_SYSTEM_PROMPT = """Siz Windows kompyuterini masofadan turib to'liq boshqaruvchi va barcha topshiriqlarni avtomatik bajaruvchi aqlli Sun'iy Intellekt Agentisiz (ATLAS PC Agent).
Siz foydalanuvchi bilan o'zbek tilida muloqot qilasiz va avvalgi xabarlar tarixini eslab qolasiz.

Siz har doim yagona to'g'ri JSON obyektini qaytarishingiz shart!

JSON Formati:
{
  "action": "ACTION_TYPE",
  "params": { ... },
  "message": "Foydalanuvchiga yuboriladigan qisqa tushuntirish matni"
}

ACTION_TYPE turlari:
1. "open_app": Dasturni ochish (kalkulyator, bloknot, chrome, telegram, explorer, word, excel, va h.k.).
   params: {"app_name": "calc"}
2. "open_url": Brauzerda sayt ochish.
   params: {"url": "https://youtube.com"}
3. "click": Ekranning (x, y) nuqtasida sichqonchani bosish.
   params: {"x": 500, "y": 400}
4. "press_key": Klaviaturada tugma bosish (enter, space, tab, alt+f4, win+d va h.k.).
   params: {"key": "enter"}
5. "cmd": Windows CMD/PowerShell buyrug'i.
   params: {"command": "dir"}
6. "screenshot": Ekrandan rasm olish.
   params: {}
7. "status": CPU, RAM, Disk holati.
   params: {}
8. "popup": Ekran bildirishnomasi.
   params: {"text": "Matn"}
9. "brightness": Ekran yorqinligini o'zgartirish (0-100%).
   params: {"percent": 80}
10. "volume": Ovoz balandligini o'rnatish (0-100%).
   params: {"percent": 50}
11. "mute": Ovozni o'chirish/yoqish.
   params: {"mute": true}
12. "media": Media ijro boshqaruvi (playpause, next, prev).
   params: {"action": "playpause"}
13. "show_desktop": Ish stolini ko'rsatish (Win + D).
   params: {}
14. "close_window": Faol oynani yopish (Alt + F4).
   params: {}
15. "empty_recycle_bin": Windows Korzinani tozalash.
   params: {}
16. "clean_temp": Vaqtinchalik kesh fayllarini tozalash.
   params: {}
17. "type_text": Ekranga matn kiritish.
   params: {"text": "salom dunyo"}
18. "scroll": Sahifani aylantirish.
   params: {"amount": -500}
19. "kill": Jarayonni to'xtatish.
   params: {"target": "chrome.exe"}
20. "chat": Kompyuterda hech narsa bajarmasdan, shunchaki foydalanuvchi savoliga o'zbek tilida javob berish.
   params: {}
"""

def call_gemini_api_sync(messages: list, api_key: str) -> str | None:
    """
    Google Gemini REST API (gemini-2.0-flash / gemini-1.5-flash) orqali so'rov yuborish.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    system_text = ""
    contents = []

    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "system":
            system_text = content
        else:
            g_role = "user" if role == "user" else "model"
            contents.append({
                "role": g_role,
                "parts": [{"text": content}]
            })

    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json"
        }
    }
    if system_text:
        payload["system_instruction"] = {
            "parts": [{"text": system_text}]
        }

    try:
        resp = requests.post(url, json=payload, timeout=30)
        data = resp.json()
        if resp.status_code == 200 and "candidates" in data and len(data["candidates"]) > 0:
            parts = data["candidates"][0]["content"]["parts"]
            if parts:
                return parts[0]["text"].strip()
        else:
            logger.warning(f"Gemini API status {resp.status_code}: {data}")
    except Exception as e:
        logger.error(f"Gemini API xatoligi: {e}")
    return None


def call_openrouter_api_sync(messages: list, api_key: str, model: str = None) -> str | None:
    """OpenRouter API orqali so'rov yuborish (model avtomatik tanlanadi)"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://atlas-my-tools.vercel.app",
        "X-Title": "ATLAS PC AI Agent"
    }

    # Model tanlov: birinchi bepul modellarni sinab ko'radi
    models_to_try = [model] if model else OPENROUTER_MODELS

    for m in models_to_try:
        payload = {
            "model": m,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 512,
            "response_format": {"type": "json_object"}
        }
        try:
            resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=25)
            data = resp.json()
            if resp.status_code == 200 and "choices" in data and data["choices"]:
                content = data["choices"][0]["message"]["content"]
                if content and content.strip():
                    logger.info(f"[OpenRouter] Model: {m} -> OK")
                    return content.strip()
            # Model mavjud emas yoki kredit yetarli emas -> keyingisiga o'tish
            err = data.get("error", {}).get("message", "")
            logger.warning(f"[OpenRouter] Model {m} failed: {err}")
        except Exception as e:
            logger.warning(f"[OpenRouter] {m} exception: {e}")

    return None


def process_ai_agent_request(user_id: int, user_prompt: str) -> dict:
    """
    Foydalanuvchi so'rovini AI orqali tahlil qilib kompyuterda bajaradi.
    """
    api_key_openrouter = _get_openrouter_key()
    api_key_gemini = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key_openrouter and not api_key_gemini:
        return {
            "status": "error",
            "message": "OPENROUTER_API_KEY topilmadi! .env faylida API kalitni ko'rsating."
        }

    # Tarixni tayyorlash
    if user_id not in CHAT_HISTORIES:
        CHAT_HISTORIES[user_id] = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}]

    CHAT_HISTORIES[user_id].append({"role": "user", "content": user_prompt})

    # AI javobini olish (OpenRouter avval, keyin Gemini)
    ai_raw = None
    if api_key_openrouter:
        ai_raw = call_openrouter_api_sync(CHAT_HISTORIES[user_id], api_key_openrouter)
    if not ai_raw and api_key_gemini:
        ai_raw = call_gemini_api_sync(CHAT_HISTORIES[user_id], api_key_gemini)

    if not ai_raw:
        return {
            "status": "error",
            "message": "❌ AI serveridan javob olib bo'lmadi. Internet yoki API kalitni tekshiring."
        }

    # JSON parse qilish
    try:
        ai_clean = ai_raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(ai_clean)
    except Exception:
        data = {
            "action": "chat",
            "params": {},
            "message": ai_raw
        }

    action = data.get("action", "chat")
    params = data.get("params", {})
    bot_msg = data.get("message", "Topshiriq bajarilmoqda...")

    CHAT_HISTORIES[user_id].append({"role": "assistant", "content": json.dumps(data, ensure_ascii=False)})

    # Tarix hajmini nazorat qilish (oxirgi 15 ta xabar)
    if len(CHAT_HISTORIES[user_id]) > 15:
        CHAT_HISTORIES[user_id] = [CHAT_HISTORIES[user_id][0]] + CHAT_HISTORIES[user_id][-14:]

    # Amallarni bajarish
    exec_result = ""
    screenshot_file = None

    try:
        if action == "open_app":
            app = params.get("app_name", "")
            exec_result = open_app(app)
        elif action == "open_url":
            import webbrowser
            url = params.get("url", "https://google.com")
            webbrowser.open(url)
            exec_result = f"🌐 Brauzerda havola ochildi: <code>{url}</code>"
        elif action == "click":
            x = int(params.get("x", 0))
            y = int(params.get("y", 0))
            exec_result = click_screen(x, y)
        elif action == "press_key":
            key = params.get("key", "enter")
            exec_result = press_key(key)
        elif action == "cmd":
            cmd = params.get("command", "")
            out = execute_cmd_sync(cmd)
            exec_result = f"💻 <b>CMD Natijasi:</b>\n<code>{out}</code>"
        elif action == "screenshot":
            import tempfile
            temp_dir = tempfile.gettempdir()
            screenshot_file = os.path.join(temp_dir, f"ai_shot_{user_id}.png")
            take_screenshot(screenshot_file)
            exec_result = "🖼 Ekran tasviri olindi."
        elif action == "status":
            exec_result = get_system_status()
        elif action == "popup":
            txt = params.get("text", "Salom!")
            show_popup(txt)
            exec_result = f"💬 Bildirishnoma ko'rsatildi: \"{txt}\""
        elif action == "brightness":
            pct = int(params.get("percent", 50))
            exec_result = set_brightness(pct)
        elif action == "volume":
            pct = int(params.get("percent", 50))
            exec_result = set_volume(pct)
        elif action == "mute":
            m = bool(params.get("mute", True))
            exec_result = set_mute(m)
        elif action == "media":
            act = params.get("action", "playpause")
            exec_result = media_control(act)
        elif action == "show_desktop":
            exec_result = show_desktop()
        elif action == "close_window":
            exec_result = close_active_window()
        elif action == "empty_recycle_bin":
            exec_result = empty_recycle_bin()
        elif action == "clean_temp":
            exec_result = clean_temp_files()
        elif action == "type_text":
            txt = params.get("text", "")
            exec_result = type_text(txt)
        elif action == "scroll":
            amt = int(params.get("amount", -500))
            exec_result = scroll_page(amt)
        elif action == "kill":
            tgt = params.get("target", "")
            exec_result = kill_process(tgt)
        elif action == "chat":
            exec_result = ""
        else:
            exec_result = f"⚠️ Noma'lum amal: {action}"
    except Exception as e:
        exec_result = f"❌ Amalni bajarishda xatolik: {e}"

    return {
        "status": "ok",
        "action": action,
        "message": bot_msg,
        "exec_result": exec_result,
        "screenshot_file": screenshot_file
    }
