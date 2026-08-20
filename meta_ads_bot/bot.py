import sys
import telebot
from telebot import types
import re

# Fix Windows console utf-8 encoding for emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from config import BOT_TOKEN, ALLOWED_USER_ID, AD_ACCOUNT_ID
from facebook_api import MetaAdsManager
from scheduler import BotScheduler, load_settings, save_settings
from lead_notifier import send_lead_to_telegram

# Initialize bot and API
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
api = MetaAdsManager()

# Start background scheduler
scheduler = BotScheduler(bot)
scheduler.start()

# In-memory state for user inputs
USER_STATE = {}

def is_authorized(user_id):
    return user_id == ALLOWED_USER_ID

def check_auth(func):
    """Decorator to enforce whitelist security"""
    def wrapper(message, *args, **kwargs):
        if not is_authorized(message.from_user.id):
            bot.reply_to(message, "⛔️ <b>Kechirasiz, sizga ushbu botdan foydalanish uchun ruxsat berilmagan!</b>", parse_mode="HTML")
            return
        return func(message, *args, **kwargs)
    return wrapper

def check_auth_callback(func):
    """Decorator for callback query whitelist security"""
    def wrapper(call, *args, **kwargs):
        if not is_authorized(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔️ Ruxsat berilmagan!", show_alert=True)
            return
        return func(call, *args, **kwargs)
    return wrapper

# ==================== KEYBOARDS ====================

def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        types.KeyboardButton("💰 Hisob va Balans"),
        types.KeyboardButton("🎯 Kampaniyalar"),
        types.KeyboardButton("📈 Statistika (Hisobot)"),
        types.KeyboardButton("⏰ Avtomatlashtirish"),
        types.KeyboardButton("🔄 Yangilash")
    )
    return keyboard

def get_insights_inline():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📅 Bugun", callback_data="ins_today"),
        types.InlineKeyboardButton("📆 Kecha", callback_data="ins_yesterday"),
        types.InlineKeyboardButton("📊 Oxirgi 7 kun", callback_data="ins_last_7d"),
        types.InlineKeyboardButton("🗓 Shu oy", callback_data="ins_this_month")
    )
    return markup

# ==================== HANDLERS ====================

@bot.message_handler(commands=['start', 'menu'])
@check_auth
def send_welcome(message):
    welcome_text = (
        "👋 <b>Assalomu alaykum, Targetolog!</b>\n\n"
        "🎯 <b>Meta Ads Manager va Lidlar boshqaruv botiga xush kelibsiz.</b>\n"
        "Bu bot orqali reklamalarni to‘xtatish/yoqish, byudjetni o‘zgartirish, qolgan pulni kuzatish, byudjet 0 ga tushganda ogohlantirish olish hamda saytdan kelgan barcha arizalarni (lidlarni) real-vaqtda qabul qilishingiz mumkin.\n\n"
        "Quyidagi menyudan kerakli bo‘limni tanlang:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")

@bot.message_handler(commands=['test_lead'])
@check_auth
def handle_test_lead(message):
    test_data = {
        "name": "Test Foydalanuvchi",
        "phone": "+998 90 123 45 67",
        "telegram": "@test_user",
        "goal": "MUSHAK MASSASINI YIG'ISH",
        "experience": "1 YILDAN 3 YILGACHA",
        "daysPerWeek": "4 KUN",
        "injuries": "Test xabari, tizim integratsiyasi tekshiruvi",
        "utm_source": "meta_ads_test",
        "utm_campaign": "target_summer_2026",
        "utm_medium": "cpc"
    }
    res = send_lead_to_telegram(test_data, bot)
    if res.get("success"):
        bot.reply_to(message, "✅ <b>Test lid xabari muvaffaqiyatli yuborildi!</b>", parse_mode="HTML")
    else:
        bot.reply_to(message, f"❌ <b>Xatolik yuz berdi:</b> {res.get('error')}", parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text == "💰 Hisob va Balans")
@check_auth
def handle_account_info(message):
    bot.send_chat_action(message.chat.id, "typing")
    bal_info = api.get_balance_details()
    if "error" in bal_info:
        err_msg = bal_info['error'].get('message', 'Nomaʼlum xatolik')
        bot.send_message(message.chat.id, f"❌ <b>Xatolik yuz berdi:</b>\n{err_msg}", parse_mode="HTML")
        return

    settings = load_settings()
    custom_limit = float(settings.get("custom_budget_limit", 0))
    base_spent = float(settings.get("initial_spent_base", 0))
    current_spent = float(bal_info.get("amount_spent", 0))

    if custom_limit > 0:
        spent_since_limit = max(0.0, current_spent - base_spent)
        remaining = custom_limit - spent_since_limit
        if remaining > 0:
            budget_text = (
                f"💵 <b>Kiritilgan mablag‘ (Funds):</b> <code>${custom_limit:.2f}</code>\n"
                f"💸 <b>Ushbu mablag‘dan sarflandi:</b> <code>${spent_since_limit:.2f}</code>\n"
                f"🟢 <b>QOLGAN MABLAG' (Mavjud qoldiq):</b> <b>${remaining:.2f}</b>"
            )
        else:
            budget_text = (
                f"💵 <b>Kiritilgan mablag‘ (Funds):</b> <code>${custom_limit:.2f}</code>\n"
                f"💸 <b>Ushbu mablag‘dan sarflandi:</b> <code>${spent_since_limit:.2f}</code>\n"
                f"🔴 <b>QOLGAN MABLAG':</b> <b>$0.00 (Qarzda: ${abs(remaining):.2f})</b>"
            )
    else:
        budget_text = "ℹ️ <i>Maxsus byudjet limiti belgilanmagan.\n(Qolgan pulni hisoblash uchun quyidagi '⚙️ Byudjet limitini o‘rnatish' tugmasini bosing)</i>"

    status_map = {1: "🟢 Faol (Active)", 2: "🔴 O‘chirilgan (Disabled)", 3: "🟡 To‘lov kutilmoqda (Unsettled)"}
    status_text = status_map.get(bal_info.get("account_status"), "Nomaʼlum")
    card_info = bal_info.get("card", "Karta")

    today_ins = api.get_insights("today")

    text = (
        f"👤 <b>Reklama hisobi:</b> {bal_info.get('account_name')}\n"
        f"🆔 <b>Ad Account ID:</b> <code>{AD_ACCOUNT_ID}</code>\n"
        f"⚡️ <b>Holat:</b> {status_text}\n"
        f"💳 <b>To‘lov usuli:</b> {card_info}\n"
        f"────────────────────\n"
        f"📊 <b>Bugun sarflandi:</b> ${today_ins.get('spend', '0.00')}\n"
        f"🎯 <b>Bugungi lidlar:</b> {today_ins.get('leads', '0')} ta ({today_ins.get('cpl', '—')}/lid)\n"
        f"💳 <b>Jami hisob xarajati:</b> ${current_spent:,.2f}\n"
        f"────────────────────\n"
        f"{budget_text}\n"
    )

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("⚙️ Byudjet limitini o‘rnatish ($)", callback_data="set_budget_limit"),
        types.InlineKeyboardButton("🎯 Kampaniyalarni ko‘rish", callback_data="show_campaigns"),
        types.InlineKeyboardButton("📈 To‘liq hisobot", callback_data="ins_today")
    )
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text == "🎯 Kampaniyalar")
@check_auth
def handle_campaigns_list(message):
    bot.send_chat_action(message.chat.id, "typing")
    campaigns = api.get_campaigns()
    if not campaigns:
        bot.send_message(message.chat.id, "📭 Hech qanday kampaniya topilmadi yoki xatolik yuz berdi.", parse_mode="HTML")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    text = "📋 <b>Mavjud reklama kampaniyalari:</b>\n\nBatafsil ma'lumot yoki boshqarish uchun kampaniya ustiga bosing:\n"

    for c in campaigns:
        status_icon = "🟢" if c.get("status") == "ACTIVE" else "🔴"
        budget = float(c.get("daily_budget", 0)) / 100 if c.get("daily_budget") else 0
        budget_str = f" (${budget:.0f}/kun)" if budget > 0 else ""
        btn_text = f"{status_icon} {c.get('name')}{budget_str}"
        markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"camp_{c['id']}"))

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text == "📈 Statistika (Hisobot)")
@check_auth
def handle_insights_menu(message):
    bot.send_message(
        message.chat.id,
        "📈 <b>Qaysi davr uchun statistikani ko‘rmoqchisiz?</b>\nQuyidagi tugmalardan birini tanlang:",
        reply_markup=get_insights_inline(),
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda message: message.text == "⏰ Avtomatlashtirish")
@check_auth
def handle_automation_menu(message):
    settings = load_settings()
    status_str = "🟢 Yoqilgan" if settings.get("auto_schedule_enabled") else "🔴 O‘chirilgan"
    report_status = "🟢 Yoqilgan" if settings.get("daily_report_enabled") else "🔴 O‘chirilgan"

    text = (
        f"⏰ <b>Avtomatlashtirish va Xavfsizlik sozlamalari</b>\n\n"
        f"🌙 <b>Tungi rejim (Auto-Pause):</b> {status_str}\n"
        f"  └ ⏸ O‘chirish: <code>{settings.get('pause_time')}</code>\n"
        f"  └ ▶️ Qayta yoqish: <code>{settings.get('resume_time')}</code>\n\n"
        f"📊 <b>Kunlik avtomat hisobot:</b> {report_status}\n"
        f"  └ ⏰ Yuborish vaqti: <code>{settings.get('daily_report_time')}</code>\n\n"
        f"ℹ️ <i>Eslatma: Byudjet 0 ga tushganda faqat ogohlantirish xabari keladi, reklamalar to‘xtatilmaydi.</i>"
    )

    toggle_btn_text = "🔴 Tungi rejimni o‘chirish" if settings.get("auto_schedule_enabled") else "🟢 Tungi rejimni yoqish"
    report_toggle_text = "🔴 Hisobotni o‘chirish" if settings.get("daily_report_enabled") else "🟢 Hisobotni yoqish"

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(toggle_btn_text, callback_data="toggle_auto_schedule"),
        types.InlineKeyboardButton("⏱ Tungi o‘chirish vaqtini o‘zgartirish", callback_data="set_pause_time"),
        types.InlineKeyboardButton("⏱ Ertalabki yoqish vaqtini o‘zgartirish", callback_data="set_resume_time"),
        types.InlineKeyboardButton(report_toggle_text, callback_data="toggle_daily_report")
    )

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text == "🔄 Yangilash")
@check_auth
def handle_refresh(message):
    bot.send_message(message.chat.id, "🔄 Ma'lumotlar yangilandi!", reply_markup=get_main_keyboard(), parse_mode="HTML")
    handle_account_info(message)

# ==================== CALLBACK QUERY HANDLERS ====================

@bot.callback_query_handler(func=lambda call: call.data == "set_budget_limit")
@check_auth_callback
def cb_set_budget_limit(call):
    USER_STATE[call.from_user.id] = {"action": "set_custom_budget_limit"}
    bot.send_message(
        call.message.chat.id,
        "💰 <b>Reklama uchun ajratgan byudjetingizni ($ dollarda) yozing:</b>\n\n"
        "Misol uchun: <code>50</code> yoki <code>100</code> yoki <code>250</code>\n\n"
        "<i>(Bot hozirdan boshlab xarajatni hisoblaydi va ushbu summa tugab, 0 $ bo‘lganda sizga darhol bildirishnoma yuboradi. Reklamalar to‘xtatilmaydi).</i>",
        reply_markup=types.ForceReply(selective=True),
        parse_mode="HTML"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "show_campaigns")
@check_auth_callback
def cb_show_campaigns(call):
    handle_campaigns_list(call.message)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("ins_"))
@check_auth_callback
def cb_insights(call):
    period = call.data.replace("ins_", "")
    period_names = {
        "today": "Bugungi",
        "yesterday": "Kechagi",
        "last_7d": "Oxirgi 7 kunlik",
        "this_month": "Shu oylik"
    }
    bot.answer_callback_query(call.id, "Statistika yuklanmoqda...")
    bot.send_chat_action(call.message.chat.id, "typing")

    ins = api.get_insights(period)
    acc = api.get_account_info()

    title = period_names.get(period, "Statistika")
    text = (
        f"📊 <b>{title} hisobot</b>\n"
        f"👤 <b>Hisob:</b> {acc.get('name', 'Ads Account')}\n"
        f"📅 <b>Sana:</b> {ins.get('date_start', '')} — {ins.get('date_stop', '')}\n"
        f"────────────────────\n"
        f"💵 <b>Xarajat (Spend):</b> ${ins.get('spend', '0')}\n"
        f"🎯 <b>Lidlar soni (Leads):</b> {ins.get('leads', '0')} ta\n"
        f"📉 <b>1 ta lid narxi (CPL):</b> {ins.get('cpl', '—')}\n"
        f"👁 <b>Ko‘rishlar (Impressions):</b> {ins.get('impressions', '0')}\n"
        f"🖱 <b>Kliklar (Clicks):</b> {ins.get('clicks', '0')}\n"
        f"🎯 <b>CTR:</b> {ins.get('ctr', '0.00%')}\n"
        f"⚡️ <b>CPC:</b> {ins.get('cpc', '$0.00')}\n"
        f"📈 <b>CPM:</b> {ins.get('cpm', '$0.00')}\n"
    )

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔄 Yangilash", callback_data=f"ins_{period}"),
        types.InlineKeyboardButton("⬅️ Boshqa davr", callback_data="back_to_insights")
    )
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")
    except Exception:
        bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "back_to_insights")
@check_auth_callback
def cb_back_to_insights(call):
    bot.edit_message_text(
        "📈 <b>Qaysi davr uchun statistikani ko‘rmoqchisiz?</b>\nQuyidagi tugmalardan birini tanlang:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=get_insights_inline(),
        parse_mode="HTML"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("camp_"))
@check_auth_callback
def cb_campaign_detail(call):
    campaign_id = call.data.replace("camp_", "")
    bot.answer_callback_query(call.id, "Yuklanmoqda...")
    bot.send_chat_action(call.message.chat.id, "typing")

    c = api.get_campaign(campaign_id)
    if "error" in c:
        bot.send_message(call.message.chat.id, f"❌ Xatolik: {c['error'].get('message')}", parse_mode="HTML")
        return

    ins = api.get_insights("today", campaign_id=campaign_id)

    status = c.get("status")
    status_icon = "🟢 Faol (ACTIVE)" if status == "ACTIVE" else "🔴 To‘xtatilgan (PAUSED)"
    budget = float(c.get("daily_budget", 0)) / 100 if c.get("daily_budget") else 0

    text = (
        f"🎯 <b>Kampaniya:</b> {c.get('name')}\n"
        f"🆔 <b>ID:</b> <code>{c.get('id')}</code>\n"
        f"⚡️ <b>Holat:</b> {status_icon}\n"
        f"🎯 <b>Maqsad:</b> <code>{c.get('objective', 'Nomaʼlum')}</code>\n"
        f"💰 <b>Kunlik byudjet:</b> ${budget:.2f}\n"
        f"────────────────────\n"
        f"📊 <b>Bugungi statistika:</b>\n"
        f"  • Sarflandi: ${ins.get('spend', '0')}\n"
        f"  • Lidlar: {ins.get('leads', '0')} ta\n"
        f"  • Lid narxi: {ins.get('cpl', '—')}\n"
        f"  • Kliklar: {ins.get('clicks', '0')} (CTR: {ins.get('ctr', '0')})\n"
    )

    markup = types.InlineKeyboardMarkup(row_width=2)
    if status == "ACTIVE":
        markup.add(types.InlineKeyboardButton("⏸ To‘xtatish (Pause)", callback_data=f"toggle_camp_{campaign_id}_PAUSED"))
    else:
        markup.add(types.InlineKeyboardButton("▶️ Yoqish (Active)", callback_data=f"toggle_camp_{campaign_id}_ACTIVE"))

    markup.add(
        types.InlineKeyboardButton("💵 Byudjetni o‘zgartirish", callback_data=f"set_budget_{campaign_id}"),
        types.InlineKeyboardButton("⬅️ Barcha kampaniyalar", callback_data="show_campaigns")
    )

    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")
    except Exception:
        bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_camp_"))
@check_auth_callback
def cb_toggle_campaign(call):
    parts = call.data.split("_")
    target_status = parts[-1]
    campaign_id = parts[2]

    bot.answer_callback_query(call.id, "Holat o'zgartirilmoqda...")
    res = api.set_campaign_status(campaign_id, target_status)

    if "error" in res:
        bot.send_message(call.message.chat.id, f"❌ Xatolik yuz berdi: {res['error'].get('message')}", parse_mode="HTML")
    else:
        status_word = "yoqildi (ACTIVE)" if target_status == "ACTIVE" else "to‘xtatildi (PAUSED)"
        bot.answer_callback_query(call.id, f"✅ Kampaniya {status_word}!", show_alert=True)
        call.data = f"camp_{campaign_id}"
        cb_campaign_detail(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("set_budget_"))
@check_auth_callback
def cb_prompt_budget(call):
    campaign_id = call.data.replace("set_budget_", "")
    USER_STATE[call.from_user.id] = {"action": "change_budget", "campaign_id": campaign_id}

    bot.send_message(
        call.message.chat.id,
        "💵 <b>Yangi kunlik byudjet miqdorini dollarda yuboring:</b>\n\nMisol uchun: <code>15</code> yoki <code>25.5</code>",
        reply_markup=types.ForceReply(selective=True),
        parse_mode="HTML"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "toggle_auto_schedule")
@check_auth_callback
def cb_toggle_auto_schedule(call):
    settings = load_settings()
    settings["auto_schedule_enabled"] = not settings.get("auto_schedule_enabled", False)
    save_settings(settings)

    state_word = "faollashtirildi" if settings["auto_schedule_enabled"] else "o‘chirildi"
    bot.answer_callback_query(call.id, f"✅ Tungi rejim {state_word}!", show_alert=True)
    handle_automation_menu(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "toggle_daily_report")
@check_auth_callback
def cb_toggle_daily_report(call):
    settings = load_settings()
    settings["daily_report_enabled"] = not settings.get("daily_report_enabled", True)
    save_settings(settings)

    state_word = "yoqildi" if settings["daily_report_enabled"] else "o‘chirildi"
    bot.answer_callback_query(call.id, f"✅ Kunlik hisobot {state_word}!", show_alert=True)
    handle_automation_menu(call.message)

@bot.callback_query_handler(func=lambda call: call.data in ["set_pause_time", "set_resume_time"])
@check_auth_callback
def cb_prompt_time(call):
    action = call.data
    USER_STATE[call.from_user.id] = {"action": action}
    label = "o‘chirish" if action == "set_pause_time" else "qayta yoqish"
    bot.send_message(
        call.message.chat.id,
        f"⏱ <b>Reklamalarni avtomatik {label} vaqtini yozing (HH:MM formatida):</b>\n\nMisol uchun: <code>23:00</code> yoki <code>07:30</code>",
        reply_markup=types.ForceReply(selective=True),
        parse_mode="HTML"
    )
    bot.answer_callback_query(call.id)

# ==================== TEXT INPUT HANDLER ====================

@bot.message_handler(func=lambda message: message.from_user.id in USER_STATE)
@check_auth
def handle_user_input(message):
    state = USER_STATE.pop(message.from_user.id, None)
    if not state:
        return

    action = state.get("action")

    if action == "set_custom_budget_limit":
        text = message.text.replace("$", "").replace(",", ".").strip()
        try:
            val = float(text)
            if val <= 0:
                bot.reply_to(message, "❌ Byudjet 0 dan katta bo‘lishi kerak.", parse_mode="HTML")
                return

            bal_info = api.get_balance_details()
            current_spent = float(bal_info.get("amount_spent", 0))

            settings = load_settings()
            settings["custom_budget_limit"] = val
            settings["initial_spent_base"] = current_spent
            settings["alert_threshold_sent"] = False
            save_settings(settings)

            bot.reply_to(
                message,
                f"✅ <b>Byudjet limiti muvaffaqiyatli ${val:.2f} qilib belgilandi!</b>\n\n"
                f"📊 Hozirgi qoldiq: <b>${val:.2f}</b>\n"
                f"🚨 Ushbu byudjet sarflanib <b>0.00 $</b> ga yetganda, bot sizga darhol bildirishnoma yuboradi. <i>(Reklamalaringiz to‘xtatilmaydi, qarzga ishlashda davom etadi).</i>",
                reply_markup=get_main_keyboard(),
                parse_mode="HTML"
            )
        except ValueError:
            bot.reply_to(message, "❌ Noto‘g‘ri raqam kiritildi. Iltimos, masalan: <code>50</code> yoki <code>100</code> deb yozing.", parse_mode="HTML")

    elif action == "change_budget":
        campaign_id = state.get("campaign_id")
        text = message.text.replace("$", "").replace(",", ".").strip()
        try:
            val = float(text)
            if val <= 0:
                bot.reply_to(message, "❌ Byudjet 0 dan katta bo‘lishi kerak.", parse_mode="HTML")
                return
            res = api.set_campaign_budget(campaign_id, val)
            if "error" in res:
                bot.reply_to(message, f"❌ Xatolik yuz berdi:\n{res['error'].get('message')}", parse_mode="HTML")
            else:
                bot.reply_to(message, f"✅ <b>Kampaniya kunlik byudjeti muvaffaqiyatli ${val:.2f} ga o‘zgartirildi!</b>", reply_markup=get_main_keyboard(), parse_mode="HTML")
        except ValueError:
            bot.reply_to(message, "❌ Noto‘g‘ri raqam kiritildi. Iltimos, faqat raqam yuboring (masalan: <code>20</code>).", parse_mode="HTML")

    elif action in ["set_pause_time", "set_resume_time"]:
        val = message.text.strip()
        if not re.match(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$", val):
            bot.reply_to(message, "❌ Noto‘g‘ri vaqt formati. Iltimos, <code>23:00</code> yoki <code>07:00</code> kabi formatda yozing.", parse_mode="HTML")
            return

        settings = load_settings()
        key = "pause_time" if action == "set_pause_time" else "resume_time"
        settings[key] = val
        save_settings(settings)

        label = "Tungi to‘xtatish" if key == "pause_time" else "Ertalabki yoqish"
        bot.reply_to(message, f"✅ <b>{label} vaqti <code>{val}</code> ga o‘rnatildi!</b>", reply_markup=get_main_keyboard(), parse_mode="HTML")

# ==================== MAIN RUNNER ====================

if __name__ == "__main__":
    print("==========================================")
    print("🚀 Meta Ads Manager & Lead Bot ishga tushdi!")
    print(f"👤 Ruxsat berilgan ID: {ALLOWED_USER_ID}")
    print(f"🎯 Reklama hisobi: {AD_ACCOUNT_ID}")
    print("==========================================")

    bot.infinity_polling(skip_pending=True)
