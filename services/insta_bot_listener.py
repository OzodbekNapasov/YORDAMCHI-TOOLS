# ============================================================
#  services/insta_bot_listener.py
#  Instagram Bot Callbacks & Likes Listener (Daemon Thread)
# ============================================================

import os
import time
import threading
import telebot
from services.insta_poster_service import (
    get_setting,
    DEFAULT_BOT_TOKEN,
    toggle_post_like,
    get_post_inline_keyboard,
    init_insta_tables
)

_LISTENER_THREAD = None
_LISTENER_BOT = None
_IS_RUNNING = False

def start_insta_bot_listener():
    """Instagram botining o'zi uchun polling tinglovchini fonda ishga tushirish"""
    global _LISTENER_THREAD, _LISTENER_BOT, _IS_RUNNING
    
    if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        return
        
    if _IS_RUNNING:
        return
        
    init_insta_tables()
    token = get_setting("bot_token", DEFAULT_BOT_TOKEN)
    if not token:
        print("[Insta Listener Warn]: Bot token topilmadi.")
        return
        
    _LISTENER_BOT = telebot.TeleBot(token, threaded=True)
    
    @_LISTENER_BOT.callback_query_handler(func=lambda call: call.data.startswith("insta_like_"))
    def handle_like_callback(call):
        try:
            post_id = int(call.data.replace("insta_like_", ""))
            user_id = call.from_user.id
            
            res = toggle_post_like(post_id, user_id)
            new_kb = get_post_inline_keyboard(post_id, res["post_url"], res["likes_count"])
            
            try:
                _LISTENER_BOT.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=new_kb
                )
            except Exception as e:
                print(f"[Edit Markup Warn]: {e}")
                
            status_text = f"❤️ Sizga yoqdi! ({res['likes_count']} ta like)" if res["is_liked"] else f"💔 Like bekor qilindi ({res['likes_count']} ta)"
            _LISTENER_BOT.answer_callback_query(call.id, status_text)
        except Exception as e:
            print(f"[Insta Like Error]: {e}")
            try:
                _LISTENER_BOT.answer_callback_query(call.id, "Like qayd etildi!")
            except Exception:
                pass

    @_LISTENER_BOT.message_handler(commands=['start'])
    def handle_start(message):
        _LISTENER_BOT.reply_to(
            message,
            "👋 <b>Assalomu alaykum!</b>\n\n"
            "Ushbu bot Instagramdagi barcha yangi va arxiv postlarni avtomatik Telegramga joylab boradi.",
            parse_mode="HTML"
        )

    def _run_polling():
        global _IS_RUNNING
        _IS_RUNNING = True
        print(f"[Insta Bot Listener]: @{_LISTENER_BOT.get_me().username} tinglovchisi ishga tushdi.")
        while _IS_RUNNING:
            try:
                _LISTENER_BOT.remove_webhook()
                _LISTENER_BOT.infinity_polling(timeout=20, long_polling_timeout=20, skip_pending=True)
            except Exception as e:
                print(f"[Insta Bot Polling Err]: {e}")
                time.sleep(3)

    _LISTENER_THREAD = threading.Thread(target=_run_polling, daemon=True)
    _LISTENER_THREAD.start()


def stop_insta_bot_listener():
    """Tinglovchini to'xtatish"""
    global _IS_RUNNING, _LISTENER_BOT
    _IS_RUNNING = False
    if _LISTENER_BOT:
        try:
            _LISTENER_BOT.stop_polling()
        except Exception:
            pass
