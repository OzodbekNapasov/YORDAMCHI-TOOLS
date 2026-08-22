# ============================================================
#  services/insta_scheduler.py
#  ATLAS Platformasi — Telegram & YouTube Dual-Scheduler (Daemon)
# ============================================================

import time
import threading
from datetime import datetime, timedelta
from services.insta_poster_service import (
    init_insta_tables,
    get_setting,
    set_setting,
    set_settings_batch,
    post_next_queued_item,
    post_next_youtube_video,
    get_youtube_schedule_times,
    get_queue_stats,
    get_uzb_now
)

_SCHEDULER_THREAD = None
_IS_RUNNING = False
_SCHEDULER_LOCK = threading.Lock()

def _supabase_atomic_claim_slot(slot_key: str, setting_key: str) -> bool:
    """
    Supabase da slot ni atomik ravishda band qilish.
    Serverless muhitda threading.Lock() ishlamaydi — faqat Supabase da lock ishlaydi.
    Agar slot allaqachon band bo'lsa — False qaytaradi (boshqa jarayon oldi).
    """
    from services.insta_poster_service import _get_supabase_headers, load_insta_cloud_state
    import requests, json, time

    try:
        supa_url, headers = _get_supabase_headers()
        if not supa_url or not headers:
            # Supabase yo'q — faqat local check (single-server uchun)
            from services.insta_poster_service import get_setting
            return get_setting(setting_key, "") != slot_key

        # 1. Hozirgi holatni o'qish
        r = requests.get(
            f"{supa_url}/rest/v1/atlas_settings?key=eq.insta_poster_state",
            headers=headers, timeout=5
        )
        if r.status_code == 200 and r.json():
            try:
                cloud_state = json.loads(r.json()[0].get("value") or "{}")
            except Exception:
                cloud_state = {}
        else:
            cloud_state = {}

        settings = cloud_state.get("settings", {})

        # 2. Allaqachon band qilinganmi?
        if settings.get(setting_key) == slot_key:
            print(f"[Scheduler Duplicate Guard]: {setting_key}={slot_key} allaqachon band. Skip.")
            return False  # Boshqa jarayon oldi

        # 3. Claim: yozib qo'yish
        settings[setting_key] = slot_key
        settings["last_post_time"] = get_uzb_now().strftime("%Y-%m-%d %H:%M:%S")
        cloud_state["settings"] = settings

        payload = {
            "key": "insta_poster_state",
            "value": json.dumps(cloud_state),
            "category": "instagram",
            "description": "Instagram & YouTube AutoPoster persistent cloud state"
        }
        wr = requests.post(
            f"{supa_url}/rest/v1/atlas_settings",
            headers=headers, json=payload, timeout=5
        )

        # 4. Race condition tekshirish: 0.5s kutib qayta o'qish
        time.sleep(0.5)
        r2 = requests.get(
            f"{supa_url}/rest/v1/atlas_settings?key=eq.insta_poster_state",
            headers=headers, timeout=5
        )
        if r2.status_code == 200 and r2.json():
            try:
                verify_state = json.loads(r2.json()[0].get("value") or "{}")
            except Exception:
                verify_state = {}
            if verify_state.get("settings", {}).get(setting_key) != slot_key:
                print(f"[Scheduler Race Condition]: {setting_key} boshqa jarayon tomonidan o'zgartirildi. Skip.")
                return False

        return True  # Muvaffaqiyatli claim qilindi

    except Exception as e:
        print(f"[Supabase Atomic Claim Error]: {e}")
        # Fallback: local check
        from services.insta_poster_service import get_setting
        return get_setting(setting_key, "") != slot_key


def run_scheduler_tick():
    """Telegram va YouTube jadvalini tekshirib, vaqti kelgan bo'lsa post chiqarish"""
    if not _SCHEDULER_LOCK.acquire(blocking=False):
        return {"checked_at": get_uzb_now().strftime("%Y-%m-%d %H:%M:%S"), "skipped": True, "message": "Avvalgi tekshiruv hali davom etmoqda"}

    try:
        init_insta_tables()
        now = get_uzb_now()
        now_hm = now.strftime("%H:%M")
        today_date = now.strftime("%Y-%m-%d")
        current_hour_str = now.strftime("%H:00")
        results = {"checked_at": now.strftime("%Y-%m-%d %H:%M:%S"), "tg_posted": False, "yt_posted": False}

        # ------------------------------------------------------------
        # 1. Telegram Rejali Yuborish (Har soat boshida :00 da + Tungi rejim)
        # ------------------------------------------------------------
        try:
            tg_enabled = get_setting("auto_schedule_enabled", "1") == "1"
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
                    slot_key = f"{today_date}_{current_hour_str}"

                    # VAQT OYNASI: faqat soat boshida :00-:10 oralig'ida ishlaydi
                    # :11 dan keyin eski slotni qayta trigger qilmaydi!
                    now_minute = now.minute
                    if now_minute > 10:
                        results["tg_skipped"] = f"Trigger oynasi yopiq ({now_hm}, faqat :00-:10 da ishlaydi)"
                    else:
                        # ATOMIC CLAIM: Supabase orqali cross-process lock
                        claimed = _supabase_atomic_claim_slot(slot_key, "tg_last_posted_slot")
                        if claimed:
                            print(f"[Telegram Scheduler]: Soat ({current_hour_str}) sloti claim qilindi! Post yuborilmoqda...")
                            tg_res = post_next_queued_item()
                            results["tg_posted"] = True
                            results["tg_res"] = tg_res
                            return results  # YouTube keyingi tick da bajariladi
                        else:
                            results["tg_skipped"] = f"Slot {slot_key} allaqachon band"
        except Exception as e:
            results["tg_error"] = str(e)
            print(f"[Telegram Scheduler Error]: {e}")

        # ------------------------------------------------------------
        # 2. YouTube Shorts Rejali Yuborish (Aniq vaqtlar bo'yicha)
        # ------------------------------------------------------------
        try:
            yt_sched_enabled = get_setting("youtube_schedule_enabled", "1") == "1"
            yt_auto_upload = get_setting("youtube_auto_upload", "1") == "1"

            if yt_sched_enabled and yt_auto_upload:
                target_times = get_youtube_schedule_times()
                for target_t in target_times:
                    # VAQT OYNASI: faqat target vaqtdan keyin 10 daqiqa ichida ishlaydi
                    # Masalan: 12:00 schedule uchun faqat 12:00-12:10 da trigger bo'ladi
                    # 12:22 da eski slotni trigger QILMAYDI!
                    try:
                        t_h, t_m = map(int, target_t.split(":"))
                        target_total = t_h * 60 + t_m
                        now_total = now.hour * 60 + now.minute
                        diff_minutes = now_total - target_total
                    except Exception:
                        diff_minutes = 0

                    # Faqat vaqt oynasida (0 dan 10 daqiqa ichida) trigger
                    if not (0 <= diff_minutes <= 10):
                        continue  # Bu vaqt oynasida emas — o'tkazib yuborish

                    slot_key = f"{today_date}_{target_t}"

                    # ATOMIC CLAIM: YouTube slot uchun ham cross-process lock
                    claimed = _supabase_atomic_claim_slot(slot_key, "youtube_last_posted_slot")
                    if claimed:
                        print(f"[YouTube Scheduler]: Rek vaqti ({target_t}) claim qilindi! Yuklanmoqda...")
                        yt_res = post_next_youtube_video()
                        results["yt_posted"] = True
                        results["yt_res"] = yt_res
                        break
        except Exception as e:
            results["yt_error"] = str(e)
            print(f"[YouTube Scheduler Error]: {e}")

        return results
    finally:
        _SCHEDULER_LOCK.release()





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
    import os
    if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        return
    if _SCHEDULER_THREAD and _SCHEDULER_THREAD.is_alive():
        return
        
    _IS_RUNNING = True
    _SCHEDULER_THREAD = threading.Thread(target=_scheduler_loop, daemon=True)
    _SCHEDULER_THREAD.start()


def stop_insta_scheduler():
    """Avto-jadval fon jarayonini to'xtatish"""
    global _IS_RUNNING
    _IS_RUNNING = False
