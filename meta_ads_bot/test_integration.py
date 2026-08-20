import sys
from pathlib import Path

# Set up paths
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import BOT_TOKEN, ALLOWED_USER_ID, AD_ACCOUNT_ID, META_ACCESS_TOKEN
from facebook_api import MetaAdsManager
from lead_notifier import send_lead_to_telegram, format_lead_message
from scheduler import load_settings

def run_tests():
    print("==========================================")
    print("🔍 INTEGRATSIYA TESTLARI BOSHLANDI")
    print("==========================================")
    print(f"• BOT_TOKEN: {BOT_TOKEN[:10]}...{BOT_TOKEN[-5:]}")
    print(f"• ALLOWED_USER_ID: {ALLOWED_USER_ID}")
    print(f"• AD_ACCOUNT_ID: {AD_ACCOUNT_ID}")
    print(f"• META_ACCESS_TOKEN: {META_ACCESS_TOKEN[:15]}...{META_ACCESS_TOKEN[-10:]}")
    print("------------------------------------------")

    # 1. Meta Ads API Test
    print("\n1️⃣ Meta Ads API tekshirilmoqda...")
    api = MetaAdsManager()
    acc_info = api.get_account_info()
    if "error" in acc_info:
        print(f"⚠️ Meta API Error: {acc_info['error'].get('message')}")
    else:
        print(f"✅ Meta Hisob nomi: {acc_info.get('name')}")
        print(f"✅ Valyuta: {acc_info.get('currency')}")
        print(f"✅ Jami sarf: ${float(acc_info.get('amount_spent', 0))/100:.2f}")

    # 2. Balance & Insights Test
    print("\n2️⃣ Balans va Statistika tekshirilmoqda...")
    bal = api.get_balance_details()
    print(f"✅ Balans tafsilotlari: {bal}")
    ins = api.get_insights("today")
    print(f"✅ Bugungi statistika: Spend=${ins.get('spend')}, Leads={ins.get('leads')}, Clicks={ins.get('clicks')}")

    # 3. Campaigns Test
    print("\n3️⃣ Kampaniyalar ro'yxati tekshirilmoqda...")
    camps = api.get_campaigns()
    print(f"✅ Topilgan kampaniyalar soni: {len(camps)}")
    for c in camps[:3]:
        print(f"  - [{c.get('status')}] {c.get('name')} (ID: {c.get('id')})")

    # 4. Settings Test
    print("\n4️⃣ Sozlamalar (Scheduler) tekshirilmoqda...")
    settings = load_settings()
    print(f"✅ Sozlamalar: {settings}")

    # 5. Lead Formatting Test
    print("\n5️⃣ Lid formatlash va Telegramga yuborish tekshirilmoqda...")
    test_lead = {
        "name": "Umarbek (Test)",
        "phone": "+998 97 777 77 77",
        "telegram": "@umarchik_coach",
        "goal": "1-GA-1 VIP MURABBIYLIK",
        "experience": "3 YILDAN 5 YILGACHA",
        "daysPerWeek": "4 KUN",
        "injuries": "Test ariza — integratsiya tekshiruvi",
        "utm_source": "instagram_reels",
        "utm_campaign": "target_summer_2026",
        "utm_medium": "cpc",
        "utm_content": "video_ad_1"
    }
    msg = format_lead_message(test_lead)
    print("✅ Formatlangan xabar:")
    print(msg)

    print("\n6️⃣ Telegram botga test lid jo'natilmoqda...")
    res = send_lead_to_telegram(test_lead)
    print(f"✅ Telegram jo'natish natijasi: {res}")

    print("\n==========================================")
    print("🎉 BARCHA TEKSHIRUVLAR YAKUNLANDI!")
    print("==========================================")

if __name__ == "__main__":
    run_tests()
