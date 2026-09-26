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
PER_PROMPT = "✍️ Har variantda nechta savol bo'lsin? Son yozing"
COUNT_PROMPT = "✍️ Nechta variant yasalsin? Son yozing"
MAX_VARIANTS = 30

# Hujjat turlari: q — javobsiz, k — javobli (kalit), a — to'g'ri javob har doim A
MODES = {
    "q": ("📄 Javobsiz", "javobsiz"),
    "k": ("🔑 Javobli", "javobli"),
    "a": ("🅰️ Faqat A javobli", "A-variant"),
}
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
        kb.row(types.InlineKeyboardButton("📄 Javobsiz PDF", callback_data=f"mt:o:{uid}:q:p"),
               types.InlineKeyboardButton("🔑 Javobli PDF", callback_data=f"mt:o:{uid}:k:p"))
        kb.row(types.InlineKeyboardButton("🅰️ Faqat A javobli", callback_data=f"mt:o:{uid}:a:p"),
               types.InlineKeyboardButton("🔀 Variantlar yasash", callback_data=f"mt:v:{uid}"))
        kb.add(types.InlineKeyboardButton("📥 Asl faylni olish", callback_data=f"mt:f:{uid}"))
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

    def download(file_id: str) -> bytes:
        info = bot.get_file(file_id)
        if (info.file_size or 0) > MAX_DOWNLOAD:
            raise ValueError("Fayl 20 MB dan katta — Telegram bot uni yuklab ololmaydi.")
        return bot.download_file(info.file_path)

    def safe_stem(title: str) -> str:
        return re.sub(r"[\\/:*?\"<>|]+", "_", title)[:80]

    def output_keyboard(uid, mode: str, fmt: str):
        """PDF ostidagi tugmalar: boshqa turlar, variantlar va shu hujjatning Word nusxasi."""
        if not uid:
            return None
        kb = types.InlineKeyboardMarkup()
        others = [types.InlineKeyboardButton(label, callback_data=f"mt:o:{uid}:{m}:p")
                  for m, (label, _) in MODES.items() if m != mode]
        kb.row(*others)
        kb.row(types.InlineKeyboardButton("🔀 Variantlar yasash", callback_data=f"mt:v:{uid}"))
        if fmt == "p":
            kb.row(types.InlineKeyboardButton(f"📝 Word ({MODES[mode][1]})", callback_data=f"mt:o:{uid}:{mode}:w"))
        return kb

    def send_output(chat_id: int, file_id: str, file_name: str, uid, mode: str = "q", fmt: str = "p",
                    note: str = ""):
        """Testdan bitta hujjat: javobsiz / javobli / faqat-A, PDF yoki Word."""
        from services.mtf_converter import test_builder as tb
        label, word = MODES.get(mode, MODES["q"])
        status = bot.send_message(chat_id, f"⏳ <b>{_h(file_name)}</b> — {word} {'Word' if fmt == 'w' else 'PDF'} tayyorlanmoqda...",
                                  parse_mode="HTML")
        try:
            questions, _engine = tb.load_questions(download(file_id), file_name, with_answers=(mode != "q"))
            if uid:
                remember_count(uid, len(tb.unique_questions(questions)))
            title = tb.title_from_filename(file_name)
            if mode == "a":
                questions = tb.answers_first(questions)
            with_answers = mode in ("k", "a")
            doc_title = title + (" (A variant)" if mode == "a" else "")
            data = (tb.build_docx if fmt == "w" else tb.build_pdf)(questions, doc_title, with_answers)
            f = io.BytesIO(data)
            f.name = f"{safe_stem(title)} ({word}).{'docx' if fmt == 'w' else 'pdf'}"
            hint = {"q": "Talabalar uchun, javoblarsiz",
                    "k": "To‘g‘ri javoblar * bilan belgilangan",
                    "a": "To‘g‘ri javob har doim A qatorida (* bilan)"}[mode]
            caption = f"{label}: <b>{_h(title)}</b>\n📊 {len(questions)} ta savol · {hint}"
            if note:
                caption += f"\n{note}"
            bot.send_document(chat_id, f, caption=caption, parse_mode="HTML",
                              reply_markup=output_keyboard(uid, mode, fmt))
            try:
                bot.delete_message(chat_id, status.message_id)
            except Exception:
                pass
        except Exception as e:
            fail(chat_id, status, file_name, e)

    def send_variants(chat_id: int, entry: dict, per: int, count: int):
        from services.mtf_converter import test_builder as tb
        status = bot.send_message(chat_id, f"⏳ <b>{_h(entry['name'])}</b> — {count} ta variant × {per} ta savol yasalmoqda...",
                                  parse_mode="HTML")
        try:
            questions, _ = tb.load_questions(download(entry["file_id"]), entry["name"], with_answers=False)
            title = tb.title_from_filename(entry["name"])
            variants = tb.make_variants(questions, per, count)
            per = len(variants[0])
            stem = f"{safe_stem(title)} ({count} variant x {per})"
            f = io.BytesIO(tb.build_variants_pdf(variants, title))
            f.name = f"{stem}.pdf"
            bot.send_document(chat_id, f, parse_mode="HTML",
                              caption=f"🔀 <b>{_h(title)}</b>\n{count} ta variant × {per} ta savol · savollar va javoblar aralashtirilgan · talabalar uchun")
            k = io.BytesIO(tb.build_key_pdf(variants, title))
            k.name = f"{stem} - kalit.pdf"
            kb = types.InlineKeyboardMarkup()
            kb.row(types.InlineKeyboardButton("🔁 Yana yasash (yangi aralashtirish)", callback_data=f"mt:v:{entry['uid']}:{per}:{count}"))
            kb.row(types.InlineKeyboardButton("🔀 Boshqa sonlar bilan", callback_data=f"mt:v:{entry['uid']}"))
            bot.send_document(chat_id, k, caption="🔑 Javoblar kaliti — faqat o‘qituvchi uchun", reply_markup=kb)
            try:
                bot.delete_message(chat_id, status.message_id)
            except Exception:
                pass
        except Exception as e:
            fail(chat_id, status, entry["name"], e)

    def fail(chat_id, status, file_name, e):
        try:
            bot.edit_message_text(f"❌ <b>{_h(file_name)}</b>: {_h(e)}", chat_id, status.message_id, parse_mode="HTML")
        except Exception:
            bot.send_message(chat_id, f"❌ {file_name}: {e}")

    def remember_count(uid: str, n: int):
        try:
            entry = lib.get_test(uid)
            if entry and entry.get("questions") != n:
                entry["questions"] = n
                lib._save(entry)
        except Exception:
            pass

    def question_count(entry: dict) -> int:
        if entry.get("questions"):
            return int(entry["questions"])
        from services.mtf_converter import test_builder as tb
        n = len(tb.unique_questions(tb.load_questions(download(entry["file_id"]), entry["name"], with_answers=False)[0]))
        remember_count(entry["uid"], n)
        return n

    def ask_per_variant(chat_id: int, entry: dict):
        total = question_count(entry)
        uid = entry["uid"]
        kb = types.InlineKeyboardMarkup(row_width=4)
        opts = [n for n in (10, 15, 20, 25, 30, 40, 50) if n < total]
        kb.add(*[types.InlineKeyboardButton(str(n), callback_data=f"mt:v:{uid}:{n}") for n in opts])
        kb.row(types.InlineKeyboardButton(f"Hammasi ({total})", callback_data=f"mt:v:{uid}:{total}"),
               types.InlineKeyboardButton("✍️ Boshqa son", callback_data=f"mt:V:{uid}"))
        bot.send_message(chat_id, f"🔀 <b>{_h(entry['name'])}</b> — bazada {total} ta savol.\n\n"
                                  f"<b>1/2.</b> Har bir variantda nechta savol bo'lsin?",
                         parse_mode="HTML", reply_markup=kb)

    def ask_count(chat_id: int, entry: dict, per: int):
        uid = entry["uid"]
        kb = types.InlineKeyboardMarkup(row_width=4)
        kb.add(*[types.InlineKeyboardButton(str(n), callback_data=f"mt:v:{uid}:{per}:{n}") for n in (2, 3, 4, 5, 6, 8, 10, 12)])
        kb.row(types.InlineKeyboardButton("✍️ Boshqa son", callback_data=f"mt:W:{uid}:{per}"))
        bot.send_message(chat_id, f"🔀 Har variantda <b>{per} ta savol</b>.\n\n<b>2/2.</b> Nechta variant yasalsin?",
                         parse_mode="HTML", reply_markup=kb)

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

    @bot.message_handler(func=lambda m: bool(m.chat.type == "private" and m.reply_to_message and m.text
                                              and m.reply_to_message.text
                                              and m.reply_to_message.text.startswith((PER_PROMPT, COUNT_PROMPT))))
    def on_number_reply(message):
        if not allowed(message):
            return
        prompt = message.reply_to_message.text
        mt = re.search(r"ID: ([A-Za-z0-9_-]+)", prompt)
        entry = lib.get_test(mt.group(1)) if mt else None
        if not entry:
            bot.send_message(message.chat.id, "❌ Test topilmadi.")
            return
        num = re.sub(r"\D", "", message.text)
        if not num:
            bot.send_message(message.chat.id, "❌ Faqat son yozing, masalan: 30")
            return
        n = int(num)
        if prompt.startswith(PER_PROMPT):
            total = question_count(entry)
            if not 1 <= n <= total:
                bot.send_message(message.chat.id, f"❌ 1 dan {total} gacha son yozing.")
                return
            ask_count(message.chat.id, entry, n)
        else:
            pm = re.search(r"savollar: (\d+)", prompt)
            if not 1 <= n <= MAX_VARIANTS:
                bot.send_message(message.chat.id, f"❌ 1 dan {MAX_VARIANTS} gacha son yozing.")
                return
            send_variants(message.chat.id, entry, int(pm.group(1)) if pm else 30, n)

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
            elif action in ("o", "g"):
                # mt:o:{uid}:{q|k|a}:{p|w}; eski tugmalar: mt:g:{uid}:{1|0}
                entry = lib.get_test(parts[2])
                if not entry:
                    bot.answer_callback_query(call.id, "Test topilmadi")
                    return
                if action == "g":
                    mode, fmt = ("k" if parts[3] == "1" else "q"), "p"
                else:
                    mode, fmt = parts[3], (parts[4] if len(parts) > 4 else "p")
                bot.answer_callback_query(call.id, "Tayyorlanmoqda...")
                send_output(chat_id, entry["file_id"], entry["name"], entry["uid"], mode, fmt)
            elif action == "v":
                # mt:v:{uid} -> savollar soni; mt:v:{uid}:{per} -> variantlar soni; mt:v:{uid}:{per}:{count} -> yasash
                entry = lib.get_test(parts[2])
                if not entry:
                    bot.answer_callback_query(call.id, "Test topilmadi")
                    return
                bot.answer_callback_query(call.id)
                if len(parts) == 3:
                    ask_per_variant(chat_id, entry)
                elif len(parts) == 4:
                    ask_count(chat_id, entry, int(parts[3]))
                else:
                    send_variants(chat_id, entry, int(parts[3]), min(int(parts[4]), MAX_VARIANTS))
            elif action == "V":
                bot.answer_callback_query(call.id)
                bot.send_message(chat_id, f"{PER_PROMPT} (ID: {parts[2]})",
                                 reply_markup=types.ForceReply(input_field_placeholder="masalan: 30"))
            elif action == "W":
                bot.answer_callback_query(call.id)
                bot.send_message(chat_id, f"{COUNT_PROMPT} (ID: {parts[2]}, savollar: {parts[3]})",
                                 reply_markup=types.ForceReply(input_field_placeholder="masalan: 4"))
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
        # Birinchi bo'lib faqat javobsiz PDF; qolganlari (javobli, A, variantlar, Word) — ostidagi tugmalarda
        send_output(message.chat.id, doc.file_id, doc.file_name, uid, mode="q", fmt="p", note=note)

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
