import sys
import time
import threading
from datetime import datetime
import json
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    from meta_ads_bot.facebook_api import MetaAdsManager
    from meta_ads_bot.config import BASE_DIR, ALLOWED_USER_ID
except ImportError:
    from facebook_api import MetaAdsManager
    from config import BASE_DIR, ALLOWED_USER_ID

import tempfile

TEMP_SETTINGS_FILE = Path(tempfile.gettempdir()) / "schedule_settings.json"
LOCAL_SETTINGS_FILE = BASE_DIR / "schedule_settings.json"

DEFAULT_SETTINGS = {
    # Tungi rejim
    "auto_schedule_enabled": False,
    "pause_time": "23:00",
    "resume_time": "07:00",
    "paused_campaign_ids": [],
    
    # Kunlik hisobot
    "daily_report_enabled": True,
    "daily_report_time": "22:00",
    
    # Byudjet monitoringi va 0 ga yetganda ogohlantirish (Hech narsa to'xtatilmaydi!)
    "budget_monitor_enabled": True,
    "custom_budget_limit": 0.0,        # Masalan: 50.0 ($)
    "initial_spent_base": 0.0,         # Limit o'rnatilgandagi boshlang'ich sarf
    "daily_budget_limit": 0.0,         # Bugungi xarajat chegarasi
    "alert_threshold_sent": False,     # 0 ga tushganda xabar ketganmi
    "last_known_account_status": 1     # 1: Active
}

_MEMORY_SETTINGS = DEFAULT_SETTINGS.copy()

def load_settings():
    global _MEMORY_SETTINGS
    for sfile in [TEMP_SETTINGS_FILE, LOCAL_SETTINGS_FILE]:
        if sfile.exists():
            try:
                with open(sfile, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for k, v in DEFAULT_SETTINGS.items():
                        if k not in data:
                            data[k] = v
                    _MEMORY_SETTINGS = data
                    return data
            except Exception:
                pass
    return _MEMORY_SETTINGS.copy()

def save_settings(settings):
    global _MEMORY_SETTINGS
    _MEMORY_SETTINGS = settings.copy()
    for sfile in [TEMP_SETTINGS_FILE, LOCAL_SETTINGS_FILE]:
        try:
            with open(sfile, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            break
        except Exception:
            continue

class BotScheduler:
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.api = MetaAdsManager()
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()
            print("[Scheduler] Fon jarayoni ishga tushdi.")

    def _run_loop(self):
        last_checked_minute = None
        last_monitor_check = 0

        while self.running:
            try:
                now = datetime.now()
                current_time_str = now.strftime("%H:%M")
                current_timestamp = time.time()
                
                # Har daqiqada vaqtga oid vazifalar (Scheduler)
                if current_time_str != last_checked_minute:
                    last_checked_minute = current_time_str
                    settings = load_settings()

                    # 1. Tungi avtomatik o'chirish/yoqish
                    if settings.get("auto_schedule_enabled"):
                        if current_time_str == settings.get("pause_time"):
                            self._auto_pause(settings)
                        elif current_time_str == settings.get("resume_time"):
                            self._auto_resume(settings)

                    # 2. Kunlik avtomat hisobot
                    if settings.get("daily_report_enabled") and current_time_str == settings.get("daily_report_time"):
                        self._send_daily_report()

                # Har 1 daqiqada Byudjet va Hisob holati monitoringi
                if current_timestamp - last_monitor_check >= 60:
                    last_monitor_check = current_timestamp
                    self._check_budget_and_account_status()

            except Exception as e:
                print(f"[Scheduler Exception]: {e}")

            time.sleep(10)

    def _check_budget_and_account_status(self):
        settings = load_settings()
        if not settings.get("budget_monitor_enabled", True):
            return

        bal_info = self.api.get_balance_details()
        if "error" in bal_info:
            return

        status = bal_info.get("account_status", 1)
        last_status = settings.get("last_known_account_status", 1)

        # 1. Hisob holati o'zgargan bo'lsa (Masalan: To'lov o'tmasa)
        if status != last_status:
            settings["last_known_account_status"] = status
            save_settings(settings)

            if status != 1:
                msg = (
                    f"🚨 <b>DIQQAT! Reklama hisobingizda to'lov muammosi!</b>\n\n"
                    f"👤 <b>Hisob:</b> {bal_info.get('account_name')}\n"
                    f"💳 <b>Karta:</b> {bal_info.get('card')}\n"
                    f"❌ <b>Holat:</b> Kartadan to'lov o'tmagan bo'lishi mumkin (Status code: {status}).\n"
                    f"Iltimos, kartangizdagi mablag'ni tekshiring!"
                )
                try:
                    self.bot.send_message(ALLOWED_USER_ID, msg, parse_mode="HTML")
                except Exception as e:
                    print(f"[Budget Alert Error]: {e}")

        # 2. Maxsus belgilangan byudjet limitini tekshirish
        limit = float(settings.get("custom_budget_limit", 0))
        base_spent = float(settings.get("initial_spent_base", 0))
        current_total_spent = float(bal_info.get("amount_spent", 0))

        if limit > 0:
            spent_since_limit = max(0.0, current_total_spent - base_spent)
            remaining_budget = limit - spent_since_limit

            # Agar qolgan pul 0 ga teng yoki qarzga o'tgan bo'lsa
            if remaining_budget <= 0.00:
                if not settings.get("alert_threshold_sent", False):
                    settings["alert_threshold_sent"] = True
                    save_settings(settings)

                    # Faqat bildirishnoma yuboramiz! Hech qanday kampaniya PAUSE QILINMAYDI.
                    alert_msg = (
                        f"🚨 <b>DIQQAT! Belgilangan byudjetingiz tugadi (0.00 $)!</b>\n\n"
                        f"💰 Belgilangan limit: <b>${limit:.2f}</b>\n"
                        f"💸 Sarflangan summa: <b>${spent_since_limit:.2f}</b>\n"
                        f"⚠️ <b>Qoldiq: $0.00 (Reklamalar to'xtatilmadi, qarzga ishlashda davom etmoqda)</b>\n\n"
                        f"Yangi byudjet limitini belgilash uchun botdagi <b>'💰 Hisob va Balans'</b> bo'limiga kiring."
                    )
                    try:
                        self.bot.send_message(ALLOWED_USER_ID, alert_msg, parse_mode="HTML")
                    except Exception as e:
                        print(f"[Budget End Alert Error]: {e}")
            else:
                if settings.get("alert_threshold_sent", False):
                    settings["alert_threshold_sent"] = False
                    save_settings(settings)

    def _auto_pause(self, settings):
        print("[Scheduler] Reklamalarni avtomatik to'xtatish vaqti...")
        campaigns = self.api.get_campaigns()
        active_ids = []
        for c in campaigns:
            if c.get("status") == "ACTIVE":
                res = self.api.set_campaign_status(c["id"], "PAUSED")
                if "error" not in res:
                    active_ids.append(c["id"])

        settings["paused_campaign_ids"] = active_ids
        save_settings(settings)

        msg = (
            f"🌙 <b>Tungi rejim faollashdi!</b>\n\n"
            f"Soat {settings.get('pause_time')} bo'ldi. Jami {len(active_ids)} ta faol kampaniya to'xtatildi (<i>PAUSED</i>).\n"
            f"Ertalab soat {settings.get('resume_time')} da ular qayta yoqiladi."
        )
        try:
            self.bot.send_message(ALLOWED_USER_ID, msg, parse_mode="HTML")
        except Exception as e:
            print(f"[Scheduler send_message error]: {e}")

    def _auto_resume(self, settings):
        print("[Scheduler] Reklamalarni avtomatik yoqish vaqti...")
        paused_ids = settings.get("paused_campaign_ids", [])
        resumed_count = 0
        for cid in paused_ids:
            res = self.api.set_campaign_status(cid, "ACTIVE")
            if "error" not in res:
                resumed_count += 1

        settings["paused_campaign_ids"] = []
        save_settings(settings)

        msg = (
            f"☀️ <b>Xayrli tong!</b>\n\n"
            f"Soat {settings.get('resume_time')} bo'ldi. Kechasi to'xtatilgan {resumed_count} ta kampaniya qayta yoqildi (<i>ACTIVE</i>)."
        )
        try:
            self.bot.send_message(ALLOWED_USER_ID, msg, parse_mode="HTML")
        except Exception as e:
            print(f"[Scheduler send_message error]: {e}")

    def _send_daily_report(self):
        ins = self.api.get_insights("today")
        acc = self.api.get_account_info()
        msg = (
            f"📊 <b>Kunlik yakuniy hisobot ({ins.get('date_start', 'Bugun')})</b>\n\n"
            f"👤 <b>Hisob:</b> {acc.get('name', 'Ads Account')}\n"
            f"💵 <b>Bugun sarflandi:</b> ${ins.get('spend', '0')}\n"
            f"🎯 <b>Lidlar soni:</b> {ins.get('leads', '0')} ta\n"
            f"📉 <b>1 ta lid narxi (CPL):</b> {ins.get('cpl', '—')}\n"
            f"👁 <b>Ko'rishlar (Imp):</b> {ins.get('impressions', '0')}\n"
            f"🖱 <b>Kliklar:</b> {ins.get('clicks', '0')} (CTR: {ins.get('ctr', '0')})\n"
            f"⚡️ <b>CPC:</b> {ins.get('cpc', '0')} | <b>CPM:</b> {ins.get('cpm', '0')}"
        )
        try:
            self.bot.send_message(ALLOWED_USER_ID, msg, parse_mode="HTML")
        except Exception as e:
            print(f"[Scheduler send_message error]: {e}")
