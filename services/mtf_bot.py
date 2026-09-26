# ============================================================
#  services/mtf_bot.py
#  Telegram botdagi "🧪 MyTestX Testlar" bo'limi:
#    * testlar bazasi Telegram kanalda (fayllar) + Supabase'da (ro'yxat);
#    * papkalar / qidiruv / test kartasi;
#    * PDF + Word (javobli yoki javobsiz), asl faylni olish;
#    * kanalga tashlangan har bir .mtf avtomatik bazaga qo'shiladi.
#  Konvertatsiya native (Mtf2Xml.exe'siz) — kompyuter yoniq bo'lishi shart emas.
# ============================================================

import html
import io
import os
import re

import telebot
from telebot import types

from services import mtf_library as lib

MENU_BUTTON = "🧪 MyTestX Testlar"
SEARCH_PROMPT = "🔍 MyTestX qidiruv: test nomidan bir qismini yozing"
FOLDER_PROMPT = "🏷 Yangi papka nomini yozing"
PAGE_SIZE = 8
MAX_DOWNLOAD = 20 * 1024 * 1024  # Bot API getFile chegarasi


def _h(text) -> str:
    return html.escape(str(text or ""))


def _size(n: int) -> str:
    n = int(n or 0)
    return f"{n / 1024 / 1024:.1f} MB" if n >= 1024 * 1024 else f"{max(1, n // 1024)} KB"


def register_mtf_handlers(bot: telebot.TeleBot, is_user_allowed, send_access_denied, primary_admin_id: int):
    """Bot handlerlarini ro'yxatdan o'tkazadi. bot.py dagi umumiy handlerlardan OLDIN chaqirilishi kerak."""

    def allowed(obj) -> bool:
        return bool(getattr(obj, "from_user", None)) and is_user_allowed(obj)

    # ---------------- Ko'rinishlar ----------------

    def menu_view():
        items = lib.list_tests(force=True)
        st = lib.get_storage()
        if st:
            where = f"✅ {_h(st.get('title') or 'ulangan')}" + (" (mavzu)" if st.get("thread_id") else "")
        else:
            where = "⚠️ ulanmagan"
        text = (f"🧪 <b>MyTestX testlar bazasi</b>\n\n"
                f"📚 Jami: <b>{len(items)} ta test</b>, <b>{len(lib.folders(items))} ta papka</b>\n"
                f"📡 Baza: {where}\n\n")
        if not st:
            text += ("<i>Ulash: yopiq kanal yoki mavzuli guruh oching va botni <b>admin</b> qiling. "
                     "Kanal o'zi taniladi; guruhda esa kerakli mavzuga <code>/baza</code> deb yozing.</i>\n\n")
        text += ("<i>Bazaga tashlangan har bir .mtf fayl avtomatik qo'shiladi. "
                 "Papka — fayl izohidagi #heshteg (masalan <code>#Farmakologiya</code>).</i>")
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(*[types.InlineKeyboardButton(f"📁 {f} ({n})", callback_data=f"mt:c:{lib.folder_id(f)}:0")
                 for f, n in lib.folders(items)])
        kb.row(types.InlineKeyboardButton("🔍 Qidirish", callback_data="mt:s"),
               types.InlineKeyboardButton("🔄 Yangilash", callback_data="mt:m"))
        return text, kb

    def folder_view(fid: str, page: int):
        items = lib.list_tests()
        folder = next((f for f, _ in lib.folders(items) if lib.folder_id(f) == fid), None)
        if folder is None:
            return None, None
        tests = [e for e in items if (e.get("folder") or lib.DEFAULT_FOLDER) == folder]
        pages = max(1, (len(tests) + PAGE_SIZE - 1) // PAGE_SIZE)
        page = max(0, min(page, pages - 1))
        chunk = tests[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]
        text = f"📁 <b>{_h(folder)}</b> — {len(tests)} ta test (sahifa {page + 1}/{pages})"
        kb = types.InlineKeyboardMarkup(row_width=1)
        for e in chunk:
            kb.add(types.InlineKeyboardButton(f"📄 {e['name'][:50]}", callback_data=f"mt:t:{e['uid']}"))
        nav = []
        if page > 0:
            nav.append(types.InlineKeyboardButton("⬅️", callback_data=f"mt:c:{fid}:{page - 1}"))
        if page < pages - 1:
            nav.append(types.InlineKeyboardButton("➡️", callback_data=f"mt:c:{fid}:{page + 1}"))
        if nav:
            kb.row(*nav)
        kb.add(types.InlineKeyboardButton("🏠 Barcha papkalar", callback_data="mt:m"))
        return text, kb

    def test_view(entry: dict):
        text = (f"📄 <b>{_h(entry['name'])}</b>\n\n"
                f"📁 Papka: <b>{_h(entry.get('folder') or lib.DEFAULT_FOLDER)}</b>\n"
                f"💾 Hajmi: {_size(entry.get('size'))}\n"
                f"🗓 Qo'shilgan: {_h(entry.get('added_at') or '-')}")
        uid = entry["uid"]
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(types.InlineKeyboardButton("📄 PDF + Word (javoblar bilan)", callback_data=f"mt:g:{uid}:1"),
               types.InlineKeyboardButton("📝 PDF + Word (javobsiz, talabalar uchun)", callback_data=f"mt:g:{uid}:0"),
               types.InlineKeyboardButton("📥 Asl faylni olish", callback_data=f"mt:f:{uid}"))
        kb.row(types.InlineKeyboardButton("🏷 Papkani o'zgartirish", callback_data=f"mt:p:{uid}"),
               types.InlineKeyboardButton("🗑 O'chirish", callback_data=f"mt:x:{uid}"))
        kb.add(types.InlineKeyboardButton("⬅️ Papkaga qaytish",
                                          callback_data=f"mt:c:{lib.folder_id(entry.get('folder') or lib.DEFAULT_FOLDER)}:0"))
        return text, kb

    def results_view(query: str):
        found = lib.search(query)
        if not found:
            return f"🔍 <b>{_h(query)}</b> bo'yicha test topilmadi.", None
        kb = types.InlineKeyboardMarkup(row_width=1)
        for e in found:
            kb.add(types.InlineKeyboardButton(f"📄 {e['name'][:45]} · {e.get('folder', '')[:15]}",
                                              callback_data=f"mt:t:{e['uid']}"))
        kb.add(types.InlineKeyboardButton("🏠 Barcha papkalar", callback_data="mt:m"))
        return f"🔍 <b>{_h(query)}</b> — {len(found)} ta natija:", kb

    # ---------------- Konvertatsiya ----------------

    def convert_and_send(chat_id: int, file_id: str, file_name: str, with_answers: bool, uid: str = None):
        mode = "javoblar bilan" if with_answers else "javobsiz"
        status = bot.send_message(chat_id, f"⏳ <b>{_h(file_name)}</b> — PDF va Word ({mode}) tayyorlanmoqda...",
                                  parse_mode="HTML")
        try:
            info = bot.get_file(file_id)
            if (info.file_size or 0) > MAX_DOWNLOAD:
                raise ValueError("Fayl 20 MB dan katta — Telegram bot uni yuklab ololmaydi.")
            data = bot.download_file(info.file_path)
            from services.mtf_converter import process_mtf_to_pdf
            res = process_mtf_to_pdf(data, file_name, layout="2col", with_answers=with_answers)
            title = res.get("title") or file_name
            stem = re.sub(r"[\\/:*?\"<>|]+", "_", title)[:80] + ("" if with_answers else " (javobsiz)")
            caption = (f"🎓 <b>{_h(title)}</b>\n"
                       f"📊 Savollar: <b>{res.get('questions_count', 0)} ta</b>\n"
                       f"🔑 {'To‘g‘ri javoblar (*) bilan belgilangan' if with_answers else 'Javobsiz — talabalar uchun'}")
            if res.get("pdf_bytes"):
                f = io.BytesIO(res["pdf_bytes"])
                f.name = f"{stem}.pdf"
                bot.send_document(chat_id, f, caption=caption, parse_mode="HTML")
            if res.get("docx_bytes"):
                f = io.BytesIO(res["docx_bytes"])
                f.name = f"{stem}.docx"
                kb = None
                if uid:
                    kb = types.InlineKeyboardMarkup()
                    kb.add(types.InlineKeyboardButton(
                        "📝 Javobsiz variantini ham olish" if with_answers else "📄 Javobli variantini ham olish",
                        callback_data=f"mt:g:{uid}:{0 if with_answers else 1}"))
                bot.send_document(chat_id, f, caption="📝 Word varianti", reply_markup=kb)
            try:
                bot.delete_message(chat_id, status.message_id)
            except Exception:
                pass
        except Exception as e:
            try:
                bot.edit_message_text(f"❌ <b>{_h(file_name)}</b>: {_h(e)}", chat_id, status.message_id, parse_mode="HTML")
            except Exception:
                bot.send_message(chat_id, f"❌ {file_name}: {e}")

    def react(message, emoji="👌"):
        try:
            bot.set_message_reaction(message.chat.id, message.message_id, [types.ReactionTypeEmoji(emoji)])
        except Exception:
            pass

    # ---------------- Handlerlar ----------------

    @bot.message_handler(func=lambda m: m.chat.type == "private"
                         and (m.text == MENU_BUTTON or (m.text or "").split()[0:1] == ["/test"]))
    def open_menu(message):
        if not allowed(message):
            send_access_denied(message.chat.id, message.from_user.id)
            return
        query = (message.text or "").partition(" ")[2].strip() if message.text.startswith("/test") else ""
        try:
            text, kb = results_view(query) if query else menu_view()
        except Exception as e:
            text, kb = f"❌ Bazani o'qib bo'lmadi: {_h(e)}", None
        bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=kb)

    @bot.message_handler(func=lambda m: bool(m.chat.type == "private" and m.reply_to_message and m.text
                                              and m.reply_to_message.text
                                              and m.reply_to_message.text.startswith(SEARCH_PROMPT)))
    def on_search_reply(message):
        if not allowed(message):
            return
        text, kb = results_view(message.text)
        bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=kb)

    @bot.message_handler(func=lambda m: bool(m.chat.type == "private" and m.reply_to_message and m.text
                                              and m.reply_to_message.text
                                              and m.reply_to_message.text.startswith(FOLDER_PROMPT)))
    def on_folder_reply(message):
        if not allowed(message):
            return
        mt = re.search(r"ID: ([A-Za-z0-9_-]+)", message.reply_to_message.text)
        entry = lib.set_folder(mt.group(1), message.text.lstrip("#")) if mt else None
        if not entry:
            bot.send_message(message.chat.id, "❌ Test topilmadi.")
            return
        text, kb = test_view(entry)
        bot.send_message(message.chat.id, "✅ Papka o'zgartirildi.\n\n" + text, parse_mode="HTML", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: (c.data or "").startswith("mt:"))
    def on_callback(call):
        if not allowed(call):
            bot.answer_callback_query(call.id, "Ruxsat yo'q")
            return
        parts = call.data.split(":")
        action = parts[1] if len(parts) > 1 else ""
        chat_id = call.message.chat.id

        def show(text, kb):
            try:
                bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode="HTML", reply_markup=kb)
            except Exception:
                bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=kb)

        try:
            if action == "m":
                bot.answer_callback_query(call.id)
                show(*menu_view())
            elif action == "c":
                bot.answer_callback_query(call.id)
                text, kb = folder_view(parts[2], int(parts[3]) if len(parts) > 3 else 0)
                show(*(folder_view_missing() if text is None else (text, kb)))
            elif action == "t":
                entry = lib.get_test(parts[2])
                bot.answer_callback_query(call.id, None if entry else "Test topilmadi")
                if entry:
                    show(*test_view(entry))
            elif action == "g":
                entry = lib.get_test(parts[2])
                if not entry:
                    bot.answer_callback_query(call.id, "Test topilmadi")
                    return
                bot.answer_callback_query(call.id, "Tayyorlanmoqda...")
                convert_and_send(chat_id, entry["file_id"], entry["name"], parts[3] == "1", uid=entry["uid"])
            elif action == "f":
                entry = lib.get_test(parts[2])
                bot.answer_callback_query(call.id, None if entry else "Test topilmadi")
                if entry:
                    bot.send_document(chat_id, entry["file_id"], caption=f"📥 {entry['name']}")
            elif action == "s":
                bot.answer_callback_query(call.id)
                bot.send_message(chat_id, SEARCH_PROMPT,
                                 reply_markup=types.ForceReply(input_field_placeholder="masalan: farmakologiya"))
            elif action == "p":
                bot.answer_callback_query(call.id)
                bot.send_message(chat_id, f"{FOLDER_PROMPT} (ID: {parts[2]})",
                                 reply_markup=types.ForceReply(input_field_placeholder="masalan: Farmakologiya"))
            elif action == "x":
                bot.answer_callback_query(call.id)
                kb = types.InlineKeyboardMarkup()
                kb.row(types.InlineKeyboardButton("✅ Ha, o'chirish", callback_data=f"mt:X:{parts[2]}"),
                       types.InlineKeyboardButton("❌ Yo'q", callback_data=f"mt:t:{parts[2]}"))
                show("🗑 Test bazadan (ro'yxatdan) o'chirilsinmi?\n<i>Kanaldagi fayl o'zi qoladi.</i>", kb)
            elif action == "X":
                lib.delete_test(parts[2])
                bot.answer_callback_query(call.id, "O'chirildi")
                show(*menu_view())
            else:
                bot.answer_callback_query(call.id)
        except Exception as e:
            try:
                bot.answer_callback_query(call.id, f"Xatolik: {str(e)[:150]}", show_alert=True)
            except Exception:
                pass

    def folder_view_missing():
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🏠 Barcha papkalar", callback_data="mt:m"))
        return "📁 Papka topilmadi (ehtimol o'zgargan).", kb

    # Botga yuborilgan / kanaldan forward qilingan .mtf fayllar
    @bot.message_handler(content_types=["document"],
                         func=lambda m: bool(m.document and lib.is_test_file(m.document.file_name)))
    def on_test_document(message):
        doc = message.document
        # Guruhdagi fayllar: faqat baza mavzusidagilar jimgina indekslanadi
        if message.chat.type != "private":
            index_group_document(message)
            return
        if not allowed(message):
            send_access_denied(message.chat.id, message.from_user.id)
            return
        st = None
        try:
            st = lib.get_storage()
        except Exception:
            pass
        channel_id = st["chat_id"] if st else None
        thread_id = st.get("thread_id") if st else None

        origin = getattr(message, "forward_origin", None)
        origin_chat = getattr(origin, "chat", None) or getattr(origin, "sender_chat", None)
        from_channel = bool(channel_id and origin_chat is not None and origin_chat.id == channel_id)

        # 1) Bazadan forward qilingan eski fayllar — faqat bazaga qo'shiladi (ko'p faylni birdan forward qilish uchun)
        if from_channel:
            try:
                lib.add_test(doc.file_id, doc.file_unique_id, doc.file_name, doc.file_size,
                             channel_msg_id=getattr(origin, "message_id", None),
                             folder=lib.folder_from_caption(message.caption), keep_existing_folder=False)
                react(message, "👌")
            except Exception as e:
                bot.reply_to(message, f"❌ Bazaga qo'shib bo'lmadi: {e}")
            return

        # 2) Boshqa joydan forward qilingan fayl — bazaga saqlanadi, lekin konvertatsiya qilinmaydi
        #    (100 ta faylni forward qilganda 100 ta PDF kelib qolmasligi uchun). Oddiy yuklash — saqlash + PDF/Word.
        is_forward = origin is not None
        uid = None
        note = ""
        try:
            existing = lib.get_test(doc.file_unique_id)
            channel_msg_id = (existing or {}).get("channel_msg_id")
            folder = lib.folder_from_caption(message.caption)
            if channel_id and not channel_msg_id:
                sent = bot.send_document(channel_id, doc.file_id,
                                         caption=f"#{folder.replace(' ', '_')}" if folder != lib.DEFAULT_FOLDER else None,
                                         message_thread_id=thread_id)
                channel_msg_id = sent.message_id
            entry = lib.add_test(doc.file_id, doc.file_unique_id, doc.file_name, doc.file_size,
                                 channel_msg_id=channel_msg_id, folder=folder)
            uid = entry["uid"]
            if is_forward:
                react(message, "👌")
                return
            if entry.get("is_new"):
                note = "📡 Bazaga saqlandi." if channel_id else "📚 Ro'yxatga qo'shildi (baza kanali/mavzusi hali ulanmagan)."
        except Exception as e:
            note = f"⚠️ Bazaga saqlanmadi: {_h(e)}"
        if note:
            bot.send_message(message.chat.id, note, parse_mode="HTML")
        convert_and_send(message.chat.id, doc.file_id, doc.file_name, True, uid=uid)

    def posted_by_admin(message) -> bool:
        """Guruhda admin yozganmi (o'z nomidan yoki guruh nomidan — anonim admin)."""
        sender_chat = getattr(message, "sender_chat", None)
        return allowed(message) or bool(sender_chat and sender_chat.id == message.chat.id)

    def index_group_document(message):
        doc = message.document
        try:
            st = lib.get_storage()
            if not st or message.chat.id != st["chat_id"]:
                return
            if st.get("thread_id") and getattr(message, "message_thread_id", None) != st["thread_id"]:
                return
            if not posted_by_admin(message):
                return
            lib.add_test(doc.file_id, doc.file_unique_id, doc.file_name, doc.file_size,
                         channel_msg_id=message.message_id,
                         folder=lib.folder_from_caption(message.caption),
                         keep_existing_folder=not message.caption)
            react(message, "👌")
        except Exception as e:
            print(f"[MTF Library] guruh faylini indekslab bo'lmadi: {e}")

    @bot.message_handler(func=lambda m: m.chat.type in ("group", "supergroup")
                         and bool(re.match(r"^/(mtf_)?baza(@\w+)?(\s|$)", m.text or "")))
    def set_group_storage(message):
        if not posted_by_admin(message):
            return
        chat = message.chat
        try:
            member = bot.get_chat_member(chat.id, primary_admin_id)
            if member.status not in ("creator", "administrator"):
                bot.reply_to(message, "❌ Baza faqat siz admin bo'lgan guruhda ulanadi.")
                return
            thread_id = message.message_thread_id if getattr(message, "is_topic_message", False) else None
            lib.set_channel(chat.id, chat.title or "", thread_id=thread_id)
            bot.reply_to(message,
                         "✅ " + ("Shu mavzu" if thread_id else "Shu guruh") + " MyTestX testlar bazasi sifatida ulandi!\n\n"
                         "Bu yerga tashlangan .mtf fayllar bazaga avtomatik qo'shiladi (👌 belgisi qo'yiladi). "
                         "Papka uchun izohga heshteg yozing, masalan #Farmakologiya.\n"
                         "Testlarni botning shaxsiy chatida «🧪 MyTestX Testlar» menyusidan oling.")
        except Exception as e:
            bot.reply_to(message, f"❌ Ulab bo'lmadi: {e}")

    # Guruhlardagi boshqa xabarlar: bot hech narsa demaydi (aks holda a'zolarga "ruxsat yo'q" deb yozardi)
    @bot.message_handler(func=lambda m: m.chat.type != "private",
                         content_types=list(telebot.util.content_type_media) + list(telebot.util.content_type_service))
    def ignore_group_messages(message):
        return

    # Kanalga tashlangan fayllar — avtomatik indeks
    @bot.channel_post_handler(content_types=["document"])
    def on_channel_document(message):
        doc = message.document
        if not doc or not lib.is_test_file(doc.file_name):
            return
        try:
            if message.chat.id != lib.get_channel_id():
                return
            lib.add_test(doc.file_id, doc.file_unique_id, doc.file_name, doc.file_size,
                         channel_msg_id=message.message_id,
                         folder=lib.folder_from_caption(message.caption),
                         keep_existing_folder=not message.caption)
        except Exception as e:
            print(f"[MTF Library] kanal postini indekslab bo'lmadi: {e}")

    # Bot kanalga admin qilib qo'shilganda — kanalni baza sifatida ulash
    @bot.my_chat_member_handler(func=lambda u: u.chat.type == "channel" and u.new_chat_member.status == "administrator")
    def on_bot_added(update):
        chat = update.chat
        if not allowed(update):
            return
        try:
            member = bot.get_chat_member(chat.id, primary_admin_id)
            if member.status not in ("creator", "administrator"):
                return
            current = lib.get_channel_id()
            if current and current != chat.id:
                bot.send_message(primary_admin_id,
                                 f"ℹ️ Bot <b>{_h(chat.title)}</b> kanaliga qo'shildi, lekin baza allaqachon boshqa "
                                 f"kanalga ulangan. Almashtirish uchun eski kanaldan botni chiqarib, qayta qo'shing.",
                                 parse_mode="HTML")
                return
            lib.set_channel(chat.id, chat.title or "")
            bot.send_message(primary_admin_id,
                             f"✅ <b>{_h(chat.title)}</b> kanali MyTestX testlar bazasi sifatida ulandi!\n\n"
                             f"Endi kanalga .mtf fayllarni tashlang — ular bazaga avtomatik qo'shiladi.\n"
                             f"Papka uchun izohga heshteg yozing, masalan: <code>#Farmakologiya</code>.\n\n"
                             f"Kanalda avvaldan turgan fayllarni botga <b>forward</b> qiling — ular ham bazaga qo'shiladi.",
                             parse_mode="HTML")
        except Exception as e:
            print(f"[MTF Library] kanalni ulab bo'lmadi: {e}")

    @bot.my_chat_member_handler(func=lambda u: u.chat.type in ("group", "supergroup")
                                and u.new_chat_member.status == "administrator")
    def on_bot_added_to_group(update):
        if not allowed(update):
            return
        try:
            bot.send_message(primary_admin_id,
                             f"ℹ️ Bot <b>{_h(update.chat.title)}</b> guruhiga admin qilindi.\n\n"
                             f"Testlar bazasi uchun guruhdagi kerakli <b>mavzuga</b> <code>/baza</code> deb yozing.",
                             parse_mode="HTML")
        except Exception:
            pass

    # Kanal chiqib ketsa (bot olib tashlansa) — sozlamani tozalash
    @bot.my_chat_member_handler(func=lambda u: u.new_chat_member.status in ("left", "kicked"))
    def on_bot_removed(update):
        try:
            if lib.get_channel_id() == update.chat.id and not os.environ.get("MTF_CHANNEL_ID"):
                lib.set_channel(0, "")
        except Exception:
            pass
