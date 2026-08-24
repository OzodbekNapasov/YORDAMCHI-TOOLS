import os
import sys
import tempfile
import shutil
import logging
import telebot
from telebot.types import Message, CallbackQuery

from .system_tools import (
    get_system_status,
    take_screenshot,
    take_webcam_photo,
    execute_cmd_sync,
    get_running_apps,
    kill_process,
    power_control,
    empty_recycle_bin,
    clean_temp_files,
    set_brightness,
    set_volume,
    set_mute,
    list_directory_info,
    search_user_files,
    pair_sunshine_pin,
    register_sunshine_client_cert,
    get_monitors_list,
    wake_and_unlock_pc,
    is_system_compatible
)
from .keyboards import (
    get_pc_control_keyboard,
    get_power_inline_keyboard,
    get_confirmation_inline,
    get_volume_inline,
    get_brightness_inline,
    get_cleanup_inline,
    get_ai_mode_keyboard,
    make_explorer_markup,
    get_path_by_id,
    get_path_id
)
from .ai_agent import process_ai_agent_request, clear_user_history

logger = logging.getLogger(__name__)

PRIMARY_ADMIN_ID = int(os.getenv("PRIMARY_ADMIN_ID") or os.getenv("ADMIN_ID") or 8135594558)
ACTIVE_AI_USERS = set()


def is_authorized_admin(user_id: int) -> bool:
    """Faqat tasdiqlangan Admin uchun ruxsat beradi."""
    return user_id == PRIMARY_ADMIN_ID


def is_pc_control_available() -> bool:
    """Tizimda PC boshqaruv vositalari ishlashini tekshiradi."""
    return is_system_compatible()


def register_pc_control_handlers(bot: telebot.TeleBot, get_main_keyboard_fn=None):
    """
    Barcha PC Boshqaruv va AI Agent handlerlarini TeleBot obyektiga ulaydi.
    """

    # 1. Kompyuter Boshqaruvi Menyusini ochish
    @bot.message_handler(func=lambda msg: msg.text == "💻 Kompyuter Boshqaruvi")
    def handle_pc_control_menu(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        text = (
            "💻 <b>SHAXSIY KOMPYUTER BOSHQARUVI & AI AGENT</b>\n\n"
            "Ushbu bo'lim orqali kompyuteringiz holatini kuzatish, skrinshot/veb-kamera olish, "
            "fayllarni yuklab olish, quvvatni boshqarish va Gemini AI agentidan foydalanishingiz mumkin.\n\n"
            "Kerakli buyruqni tanlang 👇"
        )
        bot.send_message(
            message.chat.id,
            text,
            parse_mode="HTML",
            reply_markup=get_pc_control_keyboard()
        )

    # 2. Tizim Holati
    @bot.message_handler(func=lambda msg: msg.text in ["📊 Tizim Holati", "/status"])
    def handle_system_status(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        load_msg = bot.send_message(message.chat.id, "⏳ <i>Tizim ma'lumotlari yig'ilmoqda...</i>", parse_mode="HTML")
        status_info = get_system_status()
        bot.edit_message_text(status_info, message.chat.id, load_msg.message_id, parse_mode="HTML")

    # 3. Skrinshot olish (Multi-monitor qo'llab-quvvatlanadi)
    @bot.message_handler(func=lambda msg: (msg.text and (msg.text.startswith("/screenshot") or msg.text == "🖼 Skrinshot")))
    def handle_screenshot(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        load_msg = bot.send_message(message.chat.id, "📸 <i>Ekran tasviri olinmoqda...</i>", parse_mode="HTML")
        temp_dir = tempfile.gettempdir()
        mons = get_monitors_list()

        # Check if user requested specific monitor: e.g. /screenshot 1 or /screenshot 2
        parts = message.text.strip().split()
        mon_req = None
        if len(parts) > 1 and parts[1].isdigit():
            mon_req = int(parts[1])

        try:
            if mon_req and 1 <= mon_req <= len(mons):
                filepath = os.path.join(temp_dir, f"screenshot_mon_{mon_req}_{int(message.date)}.png")
                take_screenshot(filepath, monitor_index=mon_req)
                with open(filepath, "rb") as photo:
                    bot.send_photo(
                        message.chat.id,
                        photo,
                        caption=f"🖼 <b>{mons[mon_req - 1].get('name', f'{mon_req}-Monitor')}</b>",
                        parse_mode="HTML"
                    )
                if os.path.exists(filepath):
                    try: os.remove(filepath)
                    except Exception: pass
            elif len(mons) > 1:
                # 2 va undan ortiq monitor bo'lsa - har birini alohida yuborish
                for i, m in enumerate(mons, 1):
                    filepath = os.path.join(temp_dir, f"screenshot_mon_{i}_{int(message.date)}.png")
                    take_screenshot(filepath, monitor_index=i)
                    with open(filepath, "rb") as photo:
                        bot.send_photo(
                            message.chat.id,
                            photo,
                            caption=f"🖥️ <b>{m.get('name', f'{i}-Monitor')}</b>",
                            parse_mode="HTML"
                        )
                    if os.path.exists(filepath):
                        try: os.remove(filepath)
                        except Exception: pass
            else:
                filepath = os.path.join(temp_dir, f"screenshot_{int(message.date)}.png")
                take_screenshot(filepath)
                with open(filepath, "rb") as photo:
                    bot.send_photo(message.chat.id, photo, caption="🖼 <b>Kompyuter ekran tasviri</b>", parse_mode="HTML")
                if os.path.exists(filepath):
                    try: os.remove(filepath)
                    except Exception: pass

            try:
                bot.delete_message(message.chat.id, load_msg.message_id)
            except Exception:
                pass
        except Exception as e:
            logger.error(f"Screenshot xatoligi: {e}")
            bot.edit_message_text(f"❌ Screenshot olishda xatolik:\n<code>{e}</code>", message.chat.id, load_msg.message_id, parse_mode="HTML")

    # 4. Veb-kamera surati
    @bot.message_handler(func=lambda msg: msg.text in ["📷 Veb-kamera", "/webcam"])
    def handle_webcam(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        load_msg = bot.send_message(message.chat.id, "📷 <i>Veb-kamera surati olinmoqda...</i>", parse_mode="HTML")
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, f"webcam_{int(message.date)}.jpg")

        try:
            take_webcam_photo(filepath)
            with open(filepath, "rb") as photo:
                bot.send_photo(message.chat.id, photo, caption="📷 <b>Veb-kamera surati</b>", parse_mode="HTML")
            try:
                bot.delete_message(message.chat.id, load_msg.message_id)
            except Exception:
                pass
        except Exception as e:
            logger.error(f"Webcam xatoligi: {e}")
            bot.edit_message_text(f"❌ Veb-kamera tasvirini olishda xatolik:\n<code>{e}</code>", message.chat.id, load_msg.message_id, parse_mode="HTML")
        finally:
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception:
                    pass

    # 5. Papka va Fayllar (File Explorer)
    @bot.message_handler(func=lambda msg: msg.text in ["📁 Papka va Fayllar", "/explorer"])
    def handle_file_explorer(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        text, d_path, p_dir, dirs, files = list_directory_info(desktop)
        kb, page, total_pages = make_explorer_markup(d_path, p_dir, dirs, files, page=0)
        bot.send_message(message.chat.id, text, reply_markup=kb, parse_mode="HTML")

    # 6. Dasturlar va Jarayonlar
    @bot.message_handler(func=lambda msg: msg.text in ["🎮 Dasturlar (TOP-20)", "/apps"])
    def handle_running_apps(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        load_msg = bot.send_message(message.chat.id, "🔄 <i>Dasturlar ro'yxati olinmoqda...</i>", parse_mode="HTML")
        apps_info = get_running_apps()
        bot.edit_message_text(apps_info, message.chat.id, load_msg.message_id, parse_mode="HTML")

    # 7. CMD Buyruq maslahati
    @bot.message_handler(func=lambda msg: msg.text == "📝 CMD Buyruq")
    def handle_cmd_hint(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        hint = (
            "📝 <b>CMD Buyruqlarini bajarish uchun:</b>\n\n"
            "<code>/cmd &lt;buyruq&gt;</code> ko'rinishida yuboring.\n\n"
            "<b>Misollar:</b>\n"
            "• <code>/cmd ipconfig</code> — IP va Tarmoq sozlamalari\n"
            "• <code>/cmd ping 8.8.8.8</code> — Internet ping tekshirish\n"
            "• <code>/cmd dir D:\\</code> — D: diskdagi fayllar"
        )
        bot.send_message(message.chat.id, hint, parse_mode="HTML")

    # 8. Quvvat Boshqaruvi
    @bot.message_handler(func=lambda msg: msg.text in ["⚡ Quvvat Boshqaruvi", "/power"])
    def handle_power_menu(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        text = "⚡ <b>QUVVATNI BOSHQARISH MENYUSI</b>\n\nKerakli amalni tanlang:"
        bot.send_message(message.chat.id, text, reply_markup=get_power_inline_keyboard(), parse_mode="HTML")

    # 9. Ovoz va Yorqinlik
    @bot.message_handler(func=lambda msg: msg.text == "🔊 Ovoz & Yorqinlik")
    def handle_media_settings(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        bot.send_message(message.chat.id, "🔊 <b>Ovoz balandligini sozlash:</b>", reply_markup=get_volume_inline(), parse_mode="HTML")
        bot.send_message(message.chat.id, "☀️ <b>Ekran yorqinligini sozlash:</b>", reply_markup=get_brightness_inline(), parse_mode="HTML")

    # 10. Tozalash (Kesh va Korzina)
    @bot.message_handler(func=lambda msg: msg.text == "🧹 Kesh & Korzina Tozalash")
    def handle_cleanup_menu(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        bot.send_message(message.chat.id, "🧹 <b>Tizimni tozalash va optimizatsiya:</b>", reply_markup=get_cleanup_inline(), parse_mode="HTML")

    # 11. AI Agent Rejimiga kirish
    @bot.message_handler(func=lambda msg: msg.text in ["🧠 AI Yordamchi (PC Agent)", "/ai_mode"])
    def handle_enter_ai_mode(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        ACTIVE_AI_USERS.add(message.from_user.id)
        text = (
            "🧠 <b>AI YORDAMCHI (PC AGENT) REJIMIDASIZ!</b>\n\n"
            "Endi har qanday matn, savol yoki topshiriqni <b>to'g'ridan-to'g'ri yozishingiz mumkin</b>.\n\n"
            "<i>Misollar:</i>\n"
            "• <i>\"Ekrandan rasm olib yubor\"</i>\n"
            "• <i>\"Kalkulyatorni och\"</i>\n"
            "• <i>\"Ovozni 30% ga qo'y\"</i>\n"
            "• <i>\"Korzinani tozalab qo'y\"</i>\n"
            "• <i>\"Barcha oynalarni yig'ib ish stolini ko'rsat\"</i>\n\n"
            "💡 <i>Chiqish uchun quyidagi <b>❌ AI Rejimidan chiqish</b> tugmasini bosing.</i>"
        )
        bot.send_message(message.chat.id, text, reply_markup=get_ai_mode_keyboard(), parse_mode="HTML")

    # 12. AI Rejimidan chiqish
    @bot.message_handler(func=lambda msg: msg.text == "❌ AI Rejimidan chiqish")
    def handle_exit_ai_mode(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        ACTIVE_AI_USERS.discard(message.from_user.id)
        text = "👋 <b>AI Rejimidan chiqdingiz.</b>\nStandart kompyuter boshqaruv menyusiga qaytdingiz."
        bot.send_message(message.chat.id, text, reply_markup=get_pc_control_keyboard(), parse_mode="HTML")

    # 13. AI Xotirasini tozalash
    @bot.message_handler(func=lambda msg: msg.text in ["🧹 Chat xotirasini tozalash", "/clear"])
    def handle_clear_ai_memory(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        clear_user_history(message.from_user.id)
        bot.send_message(message.chat.id, "🧹 <b>AI bilan muloqot xotirasi tozalandi!</b>", parse_mode="HTML")

    # 14. /cmd <buyruq>
    @bot.message_handler(commands=["cmd"])
    def handle_cmd_command(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            bot.send_message(message.chat.id, "⚠️ <b>Ishlatish:</b> <code>/cmd &lt;buyruq&gt;</code>\nMasalan: <code>/cmd ipconfig</code>", parse_mode="HTML")
            return

        cmd_text = parts[1].strip()
        load_msg = bot.send_message(message.chat.id, f"⚙️ <b>Buyruq bajarilmoqda:</b> <code>{cmd_text}</code>...", parse_mode="HTML")
        output = execute_cmd_sync(cmd_text)
        bot.edit_message_text(f"💻 <b>CMD NATIJASI:</b>\n\n<code>{output}</code>", message.chat.id, load_msg.message_id, parse_mode="HTML")

    # 15. /kill <target>
    @bot.message_handler(commands=["kill"])
    def handle_kill_command(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            bot.send_message(message.chat.id, "⚠️ <b>Ishlatish:</b> <code>/kill &lt;dastur_nomi_yoki_PID&gt;</code>\nMasalan: <code>/kill chrome.exe</code>", parse_mode="HTML")
            return

        target = parts[1].strip()
        res = kill_process(target)
        bot.send_message(message.chat.id, res, parse_mode="HTML")

    # 16. /getfile <fayl_yoki_papka_yo'li>
    @bot.message_handler(commands=["getfile"])
    def handle_getfile_command(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            bot.send_message(
                message.chat.id,
                "⚠️ <b>Ishlatish:</b> <code>/getfile &lt;fayl_yoki_papka_yo'li&gt;</code>\n\n"
                "Masalan:\n• <code>/getfile C:\\Users\\User\\Desktop\\hisobot.xlsx</code>\n• <code>/getfile D:\\Loyiha</code>",
                parse_mode="HTML"
            )
            return

        target_path = parts[1].strip().strip('"')
        if not os.path.exists(target_path):
            bot.send_message(message.chat.id, f"❌ <b>Manzil topilmadi:</b> <code>{target_path}</code>", parse_mode="HTML")
            return

        is_folder = os.path.isdir(target_path)
        load_msg = bot.send_message(message.chat.id, "📦 <i>Fayl tayyorlanmoqda...</i>", parse_mode="HTML")

        send_path = target_path
        temp_zip = None

        try:
            if is_folder:
                folder_name = os.path.basename(os.path.normpath(target_path)) or "Folder"
                temp_dir = tempfile.gettempdir()
                out_base = os.path.join(temp_dir, f"{folder_name}_archive_{int(message.date)}")
                temp_zip = shutil.make_archive(out_base, 'zip', target_path)
                send_path = temp_zip

            file_sz_mb = os.path.getsize(send_path) / (1024 * 1024)
            if file_sz_mb > 49.5:
                bot.edit_message_text(f"⚠️ Fayl hajmi juda katta (<b>{round(file_sz_mb, 1)} MB</b>). Telegram 50 MB chekloviga ega.", message.chat.id, load_msg.message_id, parse_mode="HTML")
                return

            with open(send_path, "rb") as f_obj:
                bot.send_document(
                    message.chat.id,
                    f_obj,
                    caption=f"📁 <b>Fayl:</b> <code>{os.path.basename(send_path)}</code>\n📊 <b>Hajmi:</b> {round(file_sz_mb, 2)} MB",
                    parse_mode="HTML"
                )
            try:
                bot.delete_message(message.chat.id, load_msg.message_id)
            except Exception:
                pass
        except Exception as e:
            bot.edit_message_text(f"❌ Faylni yuborishda xatolik: {e}", message.chat.id, load_msg.message_id, parse_mode="HTML")
        finally:
            if temp_zip and os.path.exists(temp_zip):
                try:
                    os.remove(temp_zip)
                except Exception:
                    pass

    # 17. /search <keyword>
    @bot.message_handler(commands=["search"])
    def handle_search_command(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            bot.send_message(message.chat.id, "⚠️ <b>Ishlatish:</b> <code>/search &lt;kalit_so'z&gt;</code>\nMasalan: <code>/search kontrakt</code>", parse_mode="HTML")
            return

        kw = parts[1].strip()
        load_msg = bot.send_message(message.chat.id, f"🔍 <code>{kw}</code> nomli fayllar qidirilmoqda...", parse_mode="HTML")
        res = search_user_files(kw)
        bot.edit_message_text(res, message.chat.id, load_msg.message_id, parse_mode="HTML")

    # 18. Sunshine / Moonlight PIN Ulanish
    @bot.message_handler(func=lambda msg: msg.text == "☀️ Sunshine / Moonlight PIN")
    def handle_sunshine_menu_prompt(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        text = (
            "☀️ <b>SUNSHINE / MOONLIGHT PIN ULANISH</b>\n\n"
            "Moonlight ilovasida chiqqan 4 xonali PIN kodni quyidagicha yuboring:\n"
            "👉 <code>/sunshine &lt;4_xonali_pin&gt;</code>\n\n"
            "<b>Misol:</b> <code>/sunshine 1234</code>\n\n"
            "<i>Bot ushbu PIN kodni kompyuteringizdagi Sunshine serveriga lahzada kiritib beradi!</i>"
        )
        bot.send_message(message.chat.id, text, parse_mode="HTML")

    @bot.message_handler(commands=["sunshine"])
    def handle_sunshine_command(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            bot.send_message(
                message.chat.id,
                "⚠️ <b>Ishlatish:</b> <code>/sunshine &lt;4_xonali_pin&gt;</code>\nMasalan: <code>/sunshine 1234</code>",
                parse_mode="HTML"
            )
            return

        pin = parts[1].strip()
        load_msg = bot.send_message(message.chat.id, f"⚡ <code>{pin}</code> PIN kodi Sunshine serveriga kiritilmoqda...", parse_mode="HTML")
        res = pair_sunshine_pin(pin)
        bot.edit_message_text(res, message.chat.id, load_msg.message_id, parse_mode="HTML")

    # 18.5. Ekranni uyg'otish / Windows Lockdan chiqarish
    @bot.message_handler(func=lambda msg: (msg.text and (msg.text == "🔓 Ekranni uyg'otish / Qulfdan chiqarish" or msg.text.startswith("/unlock") or msg.text.startswith("/wake"))))
    def handle_unlock_command(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        parts = message.text.split(maxsplit=1)
        pwd = parts[1].strip() if len(parts) > 1 else None
        res = wake_and_unlock_pc(pwd)
        bot.send_message(message.chat.id, res, parse_mode="HTML")

    # 19. /ai <prompt>
    @bot.message_handler(commands=["ai"])
    def handle_ai_command(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            bot.send_message(message.chat.id, "🧠 <b>Ishlatish:</b> <code>/ai &lt;topshiriq yoki savol&gt;</code>\nMasalan: <code>/ai ekrandan rasm ol</code>", parse_mode="HTML")
            return

        prompt = parts[1].strip()
        _execute_ai_task_sync(prompt, message, bot)

    # 19. AI Rejimida yozilgan oddiy xabarlarni tutish
    @bot.message_handler(func=lambda msg: msg.from_user.id in ACTIVE_AI_USERS and msg.text and not msg.text.startswith("/"))
    def handle_ai_mode_free_text(message: Message):
        if not is_authorized_admin(message.from_user.id):
            return

        if message.text in ["❌ AI Rejimidan chiqish", "🧹 Chat xotirasini tozalash"]:
            return

        _execute_ai_task_sync(message.text, message, bot)

    # --- CALLBACK QUERY HANDLERS ---

    # File Explorer Open
    @bot.callback_query_handler(func=lambda call: call.data.startswith("exp_op:"))
    def cb_exp_open(call: CallbackQuery):
        if not is_authorized_admin(call.from_user.id):
            return

        parts = call.data.split(":")
        path_id = int(parts[1])
        page = int(parts[2]) if len(parts) > 2 else 0

        target_path = get_path_by_id(path_id)
        if not target_path or not os.path.exists(target_path):
            bot.answer_callback_query(call.id, "❌ Papka topilmadi!", show_alert=True)
            return

        text, d_path, p_dir, dirs, files = list_directory_info(target_path)
        kb, page, total_pages = make_explorer_markup(d_path, p_dir, dirs, files, page=page)
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb, parse_mode="HTML")
        except Exception:
            pass
        bot.answer_callback_query(call.id)

    # File Explorer Zip Folder
    @bot.callback_query_handler(func=lambda call: call.data.startswith("exp_zp:"))
    def cb_exp_zip(call: CallbackQuery):
        if not is_authorized_admin(call.from_user.id):
            return

        path_id = int(call.data.split(":")[1])
        folder_path = get_path_by_id(path_id)
        if not folder_path or not os.path.exists(folder_path):
            bot.answer_callback_query(call.id, "❌ Papka topilmadi!", show_alert=True)
            return

        folder_name = os.path.basename(os.path.normpath(folder_path)) or "Folder"
        bot.answer_callback_query(call.id, "ZIP arxiv tayyorlanmoqda...")
        msg = bot.send_message(call.message.chat.id, f"📦 <code>{folder_name}</code> papkasi ZIP arxivga joylanmoqda...", parse_mode="HTML")

        temp_zip = None
        try:
            temp_dir = tempfile.gettempdir()
            out_base = os.path.join(temp_dir, f"{folder_name}_archive_{int(call.message.date)}")
            temp_zip = shutil.make_archive(out_base, 'zip', folder_path)
            file_size_mb = os.path.getsize(temp_zip) / (1024 * 1024)

            if file_size_mb > 49.5:
                bot.edit_message_text(f"⚠️ Arxiv hajmi juda katta (<b>{round(file_size_mb, 1)} MB</b>). Telegram 50MB chekloviga ega.", call.message.chat.id, msg.message_id, parse_mode="HTML")
                return

            with open(temp_zip, "rb") as f_obj:
                bot.send_document(
                    call.message.chat.id,
                    f_obj,
                    caption=f"📦 <b>ZIP Arxiv (Papka):</b> <code>{folder_name}.zip</code>\n📊 <b>Hajmi:</b> {round(file_size_mb, 2)} MB",
                    parse_mode="HTML"
                )
            try:
                bot.delete_message(call.message.chat.id, msg.message_id)
            except Exception:
                pass
        except Exception as e:
            bot.edit_message_text(f"❌ ZIP arxivlashda xatolik: {e}", call.message.chat.id, msg.message_id, parse_mode="HTML")
        finally:
            if temp_zip and os.path.exists(temp_zip):
                try:
                    os.remove(temp_zip)
                except Exception:
                    pass

    # File Explorer File Info
    @bot.callback_query_handler(func=lambda call: call.data.startswith("exp_fl:"))
    def cb_exp_file_info(call: CallbackQuery):
        if not is_authorized_admin(call.from_user.id):
            return

        path_id = int(call.data.split(":")[1])
        filepath = get_path_by_id(path_id)
        if filepath and os.path.exists(filepath):
            sz_mb = round(os.path.getsize(filepath) / (1024 * 1024), 2)
            fname = os.path.basename(filepath)
            icon = "🔗 Yarlik (Shortcut)" if fname.lower().endswith(".lnk") else "📄 Fayl"
            text = (
                f"{icon} <b>FAYL MA'LUMOTI:</b>\n\n"
                f"<b>Nomi:</b> <code>{fname}</code>\n"
                f"<b>Hajmi:</b> {sz_mb} MB\n"
                f"<b>Manzili:</b> <code>{filepath}</code>\n\n"
                f"💡 Telegram'ga yuklab olish uchun: <code>/getfile {filepath}</code>"
            )
            bot.send_message(call.message.chat.id, text, parse_mode="HTML")
            bot.answer_callback_query(call.id)
        else:
            bot.answer_callback_query(call.id, "❌ Fayl topilmadi!", show_alert=True)

    # Power Confirmation
    @bot.callback_query_handler(func=lambda call: call.data.startswith("pc_power_ask:"))
    def cb_power_ask(call: CallbackQuery):
        if not is_authorized_admin(call.from_user.id):
            return

        action = call.data.split(":")[1]
        text = "⚠️ <b>Haqiqatdan ham kompyuterni o'chirmoqchimisiz?</b>" if action == "shutdown" else "⚠️ <b>Haqiqatdan ham kompyuterni qayta yuklamoqchimisiz?</b>"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_confirmation_inline(action), parse_mode="HTML")
        bot.answer_callback_query(call.id)

    # Power Execute
    @bot.callback_query_handler(func=lambda call: call.data.startswith("pc_power_do:"))
    def cb_power_do(call: CallbackQuery):
        if not is_authorized_admin(call.from_user.id):
            return

        action = call.data.split(":")[1]
        res = power_control(action)
        bot.edit_message_text(res, call.message.chat.id, call.message.message_id, parse_mode="HTML")
        bot.answer_callback_query(call.id)

    # Power Cancel
    @bot.callback_query_handler(func=lambda call: call.data == "pc_power_cancel")
    def cb_power_cancel(call: CallbackQuery):
        if not is_authorized_admin(call.from_user.id):
            return

        bot.edit_message_text("❌ Amaliyot bekor qilindi.", call.message.chat.id, call.message.message_id, parse_mode="HTML")
        bot.answer_callback_query(call.id)

    # Volume & Mute
    @bot.callback_query_handler(func=lambda call: call.data.startswith("pc_vol:"))
    def cb_volume(call: CallbackQuery):
        if not is_authorized_admin(call.from_user.id):
            return

        val = int(call.data.split(":")[1])
        res = set_volume(val)
        bot.answer_callback_query(call.id, f"Ovoz {val}% ga o'rnatildi!")
        bot.send_message(call.message.chat.id, res, parse_mode="HTML")

    @bot.callback_query_handler(func=lambda call: call.data == "pc_vol_mute")
    def cb_volume_mute(call: CallbackQuery):
        if not is_authorized_admin(call.from_user.id):
            return

        res = set_mute(True)
        bot.answer_callback_query(call.id, "Mute holati o'zgartirildi!")
        bot.send_message(call.message.chat.id, res, parse_mode="HTML")

    # Brightness
    @bot.callback_query_handler(func=lambda call: call.data.startswith("pc_bright:"))
    def cb_brightness(call: CallbackQuery):
        if not is_authorized_admin(call.from_user.id):
            return

        val = int(call.data.split(":")[1])
        res = set_brightness(val)
        bot.answer_callback_query(call.id, f"Yorqinlik {val}% ga o'rnatildi!")
        bot.send_message(call.message.chat.id, res, parse_mode="HTML")

    # Cleanup
    @bot.callback_query_handler(func=lambda call: call.data == "pc_clean_recycle")
    def cb_clean_recycle(call: CallbackQuery):
        if not is_authorized_admin(call.from_user.id):
            return

        res = empty_recycle_bin()
        bot.answer_callback_query(call.id, "Korzina tozalandi!")
        bot.send_message(call.message.chat.id, res, parse_mode="HTML")

    @bot.callback_query_handler(func=lambda call: call.data == "pc_clean_temp")
    def cb_clean_temp(call: CallbackQuery):
        if not is_authorized_admin(call.from_user.id):
            return

        res = clean_temp_files()
        bot.answer_callback_query(call.id, "Temp fayllar tozalandi!")
        bot.send_message(call.message.chat.id, res, parse_mode="HTML")

    @bot.callback_query_handler(func=lambda call: call.data == "exp_noop")
    def cb_noop(call: CallbackQuery):
        bot.answer_callback_query(call.id)


def _execute_ai_task_sync(prompt: str, message: Message, bot: telebot.TeleBot):
    """AI Agent vazifasini bajaruvchi yordamchi funksiya."""
    load_msg = bot.send_message(message.chat.id, "🧠 <i>AI Agent vazifani o'ylamoqda va bajarmoqda...</i>", parse_mode="HTML")
    try:
        result = process_ai_agent_request(message.from_user.id, prompt)

        if result.get("status") == "error":
            bot.edit_message_text(result.get("message", "❌ Xatolik yuz berdi."), message.chat.id, load_msg.message_id, parse_mode="HTML")
            return

        msg_text = result.get("message", "")
        exec_res = result.get("exec_result", "")
        screenshot_file = result.get("screenshot_file")

        final_text = f"🤖 <b>AI Agent:</b>\n{msg_text}"
        if exec_res:
            final_text += f"\n\n⚙️ <b>Bajarilgan amal:</b>\n{exec_res}"

        if screenshot_file and os.path.exists(screenshot_file):
            try:
                with open(screenshot_file, "rb") as p:
                    bot.send_photo(message.chat.id, p, caption=final_text, parse_mode="HTML")
                try:
                    bot.delete_message(message.chat.id, load_msg.message_id)
                except Exception:
                    pass
            finally:
                if os.path.exists(screenshot_file):
                    try:
                        os.remove(screenshot_file)
                    except Exception:
                        pass
        else:
            bot.edit_message_text(final_text, message.chat.id, load_msg.message_id, parse_mode="HTML")
    except Exception as e:
        logger.error(f"AI Task execution error: {e}")
        bot.edit_message_text(f"❌ AI topshirig'ini bajarishda xatolik: {e}", message.chat.id, load_msg.message_id, parse_mode="HTML")
