import html
from datetime import datetime
import requests
try:
    from meta_ads_bot.config import BOT_TOKEN, ALLOWED_USER_ID
except ImportError:
    from config import BOT_TOKEN, ALLOWED_USER_ID

def format_lead_message(data):
    """
    Saytdan kelgan lid ma'lumotlarini Telegram uchun chiroyli HTML formatga keltiradi
    """
    name = html.escape(str(data.get("name") or "Ko'rsatilmagan"))
    phone = html.escape(str(data.get("phone") or "Ko'rsatilmagan"))
    telegram = html.escape(str(data.get("telegram") or "Ko'rsatilmagan"))
    goal = html.escape(str(data.get("goal") or data.get("service") or data.get("program") or "Umumiy ariza"))
    experience = html.escape(str(data.get("experience") or "Ko'rsatilmagan"))
    days = html.escape(str(data.get("daysPerWeek") or data.get("days") or "Ko'rsatilmagan"))
    injuries = html.escape(str(data.get("injuries") or data.get("comment") or data.get("notes") or "Mavjud emas"))
    
    # Sana va vaqt
    created_at = data.get("created_at") or data.get("date") or datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    # UTM Parametrlari
    utm_source = html.escape(str(data.get("utm_source") or ""))
    utm_campaign = html.escape(str(data.get("utm_campaign") or ""))
    utm_medium = html.escape(str(data.get("utm_medium") or ""))
    utm_term = html.escape(str(data.get("utm_term") or ""))
    utm_content = html.escape(str(data.get("utm_content") or ""))

    msg = (
        "🔥 <b>YANGI ARIZA / LID KELDI!</b> 🔥\n"
        "────────────────────\n"
        f"👤 <b>Ism:</b> {name}\n"
        f"📞 <b>Telefon:</b> <code>{phone}</code>\n"
        f"💬 <b>Telegram:</b> {telegram}\n"
        f"🎯 <b>Tanlangan maqsad / xizmat:</b> <b>{goal}</b>\n"
        f"🏋️ <b>Zaldagi tajriba:</b> {experience}\n"
        f"📅 <b>Haftalik grafik:</b> {days}\n"
        f"📝 <b>Izoh / Jarohatlar:</b> {injuries}\n"
        f"⏰ <b>Vaqt:</b> <code>{created_at}</code>\n"
    )

    # Agar UTM parametrlar mavjud bo'lsa
    has_utm = bool(utm_source or utm_campaign or utm_medium or utm_term or utm_content)
    if has_utm:
        msg += "────────────────────\n"
        msg += "🌐 <b>MARKETING / TRAFIK MANBASI:</b>\n"
        if utm_source:
            msg += f"🔗 <b>Source:</b> <code>{utm_source}</code>\n"
        if utm_campaign:
            msg += f"🎯 <b>Campaign:</b> <code>{utm_campaign}</code>\n"
        if utm_medium:
            msg += f"📊 <b>Medium:</b> <code>{utm_medium}</code>\n"
        if utm_term:
            msg += f"🔍 <b>Term:</b> <code>{utm_term}</code>\n"
        if utm_content:
            msg += f"📄 <b>Content:</b> <code>{utm_content}</code>\n"
    else:
        msg += "────────────────────\n"
        msg += "🌐 <b>Trafik manbasi:</b> To'g'ridan-to'g'ri tashrif (Organik)\n"

    return msg

def send_lead_to_telegram(data, bot_instance=None):
    """
    Lidni Telegram bot orqali adminga yuboradi
    """
    message_text = format_lead_message(data)
    
    if bot_instance:
        try:
            bot_instance.send_message(ALLOWED_USER_ID, message_text, parse_mode="HTML")
            return {"success": True}
        except Exception as e:
            print(f"[Lead Send Telebot Error]: {e}")

    # Fallback to direct HTTP API
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": ALLOWED_USER_ID,
            "text": message_text,
            "parse_mode": "HTML"
        }
        resp = requests.post(url, json=payload, timeout=10)
        res_json = resp.json()
        if res_json.get("ok"):
            return {"success": True}
        else:
            print(f"[Lead Send HTTP Error]: {res_json}")
            return {"success": False, "error": res_json}
    except Exception as e:
        print(f"[Lead Send HTTP Exception]: {e}")
        return {"success": False, "error": str(e)}
