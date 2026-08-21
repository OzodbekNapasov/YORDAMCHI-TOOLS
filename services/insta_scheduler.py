# ============================================================
#  services/insta_scheduler.py
#  ATLAS Platformasi — Telegram & YouTube Dual-Scheduler (Daemon)
# ============================================================

import time
import threading
from datetime import datetime, timedelta
from services.insta_poster_service import (
    get_setting,
    set_setting,
    post_next_queued_item,
    post_next_youtube_video,
    get_youtube_schedule_times,
    get_queue_stats,
    get_uzb_now
)

_SCHEDULER_THREAD = None
_IS_RUNNING = False

def run_scheduler_tick():
    """Telegram va YouTube jadvalini 1 marta tekshirib, vaqti kelgan bo'lsa post chiqarish"""
    now = get_uzb_now()
    now_hm = now.strftime("%H:%M")
    today_date = now.strftime("%Y-%m-%d")
    results = {"checked_at": now.strftime("%Y-%m-%d %H:%M:%S"), "tg_posted": False, "yt_posted": False}
    
    # ------------------------------------------------------------
    # 1. Telegram Rejali Yuborish (Interval bo'yicha + Tungi rejim)
    # ------------------------------------------------------------
    try:
        tg_enabled = get_setting("auto_schedule_enabled", "0") == "1"
        if tg_enabled:
            night_mode_on = get_setting("night_mode_enabled", "1") == "1"
            night_start = get_setting("night_mode_start", "00:00")
            night_end = get_setting("night_mode_end", "07:00")

            is_night = False
            if night_mode_on:
                if night_start <= night_end:
                    is_night = (night_start <= now_hm < night_end)
                else:
                    is_night = (now_hm >= night_start or now_hm < night_end)

            if not is_night:
                interval_min = int(get_setting("interval_minutes", "60"))
                last_post_str = get_setting("last_post_time", "")
                
                should_post_tg = False
                if not last_post_str:
                    should_post_tg = True
                else:
                    try:
                        last_post_dt = datetime.strptime(last_post_str, "%Y-%m-%d %H:%M:%S")
                        if (now - last_post_dt).total_seconds() >= interval_min * 60:
                            should_post_tg = True
                    except Exception:
                        should_post_tg = True
                        
                if should_post_tg:
                    print(f"[Telegram Scheduler]: Rejali post yuborilmoqda ({interval_min} daqiqa oraliq)...")
                    tg_res = post_next_queued_item()
                    results["tg_posted"] = True
                    results["tg_res"] = tg_res
    except Exception as e:
        results["tg_error"] = str(e)
        print(f"[Telegram Scheduler Error]: {e}")
        
    # ------------------------------------------------------------
    # 2. YouTube Shorts Rek Rejali Yuborish (Aniq vaqtlar bo'yicha)
    # ------------------------------------------------------------
    try:
        yt_sched_enabled = get_setting("youtube_schedule_enabled", "1") == "1"
        yt_auto_upload = get_setting("youtube_auto_upload", "1") == "1"
        
        if yt_sched_enabled and yt_auto_upload:
            target_times = get_youtube_schedule_times()
            if now_hm in target_times:
                slot_key = f"{today_date}_{now_hm}"
                last_slot = get_setting("youtube_last_posted_slot", "")
                
                if last_slot != slot_key:
                    print(f"[YouTube Scheduler]: Rek vaqti keldi ({now_hm})! YouTube Shorts yuklanmoqda...")
                    set_setting("youtube_last_posted_slot", slot_key)
                    yt_res = post_next_youtube_video()
                    results["yt_posted"] = True
                    results["yt_res"] = yt_res
    except Exception as e:
        results["yt_error"] = str(e)
        print(f"[YouTube Scheduler Error]: {e}")
        
    return results


def _scheduler_loop():
    """Har 25 soniyada Telegram va YouTube jadvalini tekshirib turuvchi fon sikli"""
    global _IS_RUNNING
    print("[Insta/YouTube Scheduler]: Fon rejimida ishga tushdi.")
    
    while _IS_RUNNING:
        try:
            run_scheduler_tick()
        except Exception as e:
            print(f"[Scheduler Loop Error]: {e}")
            
        for _ in range(25):
            if not _IS_RUNNING:
                break
            time.sleep(1)


def start_insta_scheduler():
    """Avto-jadval fon jarayonini ishga tushirish"""
    global _SCHEDULER_THREAD, _IS_RUNNING
    if _SCHEDULER_THREAD and _SCHEDULER_THREAD.is_alive():
        return
        
    _IS_RUNNING = True
    _SCHEDULER_THREAD = threading.Thread(target=_scheduler_loop, daemon=True)
    _SCHEDULER_THREAD.start()


def stop_insta_scheduler():
    """Avto-jadval fon jarayonini to'xtatish"""
    global _IS_RUNNING
    _IS_RUNNING = False
