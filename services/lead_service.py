import os
import html
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

META_BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("META_BOT_TOKEN") or "8937819411:AAHrCwLyr_Ob3bM0ypwNFYP-SKb1weL97fs"
META_ADMIN_ID = int(os.getenv("PRIMARY_ADMIN_ID") or os.getenv("META_ADMIN_ID") or "8135594558")

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
    
    created_at = data.get("created_at") or data.get("date") or datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
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

def process_and_send_lead(data):
    """
    Lidni qabul qilib, Telegram bot orqali adminga yuboradi
    """
    message_text = format_lead_message(data)
    try:
        url = f"https://api.telegram.org/bot{META_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": META_ADMIN_ID,
            "text": message_text,
            "parse_mode": "HTML"
        }
        resp = requests.post(url, json=payload, timeout=10)
        res_json = resp.json()
        if res_json.get("ok"):
            return {"success": True, "data": res_json}
        else:
            return {"success": False, "error": res_json}
    except Exception as e:
        return {"success": False, "error": str(e)}
