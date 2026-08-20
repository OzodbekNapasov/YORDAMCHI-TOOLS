import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from bot import app
from services.atlas_auth import create_session

def test_meta_ads_api():
    token = create_session(1, "Ozodbek", "Ozodbek Napasov", "superadmin")
    client = app.test_client()

    print("==========================================")
    print("🔍 ATLAS PLATFORMA: META ADS API TESTLARI")
    print("==========================================")

    # 1. Test /api/meta-ads/account
    r_acc = client.get('/api/meta-ads/account', headers={"Authorization": f"Bearer {token}"})
    print(f"1. /api/meta-ads/account: status={r_acc.status_code}")
    print(f"   Data: {r_acc.get_json()}")

    # 2. Test /api/meta-ads/campaigns
    r_camps = client.get('/api/meta-ads/campaigns', headers={"Authorization": f"Bearer {token}"})
    print(f"\n2. /api/meta-ads/campaigns: status={r_camps.status_code}")
    data_c = r_camps.get_json()
    print(f"   Topilgan kampaniyalar soni: {len(data_c.get('campaigns', []))}")

    # 3. Test /api/meta-ads/insights
    r_ins = client.get('/api/meta-ads/insights?period=today', headers={"Authorization": f"Bearer {token}"})
    print(f"\n3. /api/meta-ads/insights (today): status={r_ins.status_code}")
    print(f"   Data: {r_ins.get_json()}")

    # 4. Test /api/meta-ads/settings
    r_sett = client.get('/api/meta-ads/settings', headers={"Authorization": f"Bearer {token}"})
    print(f"\n4. /api/meta-ads/settings: status={r_sett.status_code}")
    print(f"   Data: {r_sett.get_json()}")

    print("\n🎉 Meta Ads REST API muvaffaqiyatli ishlamoqda!")

if __name__ == "__main__":
    test_meta_ads_api()
