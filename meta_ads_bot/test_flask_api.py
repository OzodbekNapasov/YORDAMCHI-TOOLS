import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from bot import app

def test_flask_lead_api():
    client = app.test_client()
    
    # 1. Test GET /api/lead
    get_res = client.get('/api/lead')
    assert get_res.status_code == 200, f"GET failed: {get_res.status_code}"
    print(f"✅ GET /api/lead OK: {get_res.get_json()}")

    # 2. Test POST /api/lead
    payload = {
        "name": "Sardor Aliyev",
        "phone": "+998 90 987 65 43",
        "telegram": "@sardor_a",
        "goal": "SOF KUCH VA SHTANGA",
        "experience": "1 YILDAN 3 YILGACHA",
        "daysPerWeek": "3 KUN",
        "injuries": "Tizza bo'g'imida yengil og'riq",
        "utm_source": "telegram_channel",
        "utm_campaign": "powerlifting_promo"
    }
    post_res = client.post('/api/lead', json=payload)
    assert post_res.status_code == 200, f"POST failed: {post_res.status_code}, data: {post_res.data}"
    print(f"✅ POST /api/lead OK: {post_res.get_json()}")

    # 3. Test OPTIONS /api/lead (CORS)
    options_res = client.options('/api/lead')
    assert options_res.status_code == 200, f"OPTIONS failed: {options_res.status_code}"
    assert "Access-Control-Allow-Origin" in options_res.headers
    print(f"✅ OPTIONS /api/lead CORS OK: {dict(options_res.headers)}")

    print("\n🎉 Flask /api/lead endpointi 100% to'g'ri ishlamoqda!")

if __name__ == "__main__":
    test_flask_lead_api()
