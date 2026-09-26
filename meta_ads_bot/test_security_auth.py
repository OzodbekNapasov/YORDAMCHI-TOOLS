import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Parol kodda saqlanmaydi: testni ATLAS_ADMIN_PASSWORD bilan ishga tushiring
# (berilmasa, faqat shu test uchun vaqtinchalik parol ishlatiladi).
os.environ.setdefault("ATLAS_ADMIN_PASSWORD", "test-only-admin-password")
ADMIN_PASSWORD = os.environ["ATLAS_ADMIN_PASSWORD"]

from bot import app, TOKEN

def test_auth_security():
    client = app.test_client()

    print("==========================================")
    print("🔒 ATLAS XAVFSIZLIK VA AUTENTIFIKATSIYA TESTI")
    print("==========================================")

    # 1. Ruxsatsiz kirish tekshiruvi (No token)
    endpoints = [
        ('/api/auth/me', 'GET'),
        ('/api/dashboard/stats', 'GET'),
        ('/api/contracts/history', 'GET'),
        ('/api/documents/list', 'GET'),
        ('/api/meta-ads/account', 'GET'),
        ('/api/contracts/download-excel/test1234', 'GET'),
        ('/api/amaliyot/survey/sample-excel', 'GET'),
        ('/api/mtf/submit_job', 'POST'),
        ('/api/mtf/job_status?job_id=x', 'GET'),
        ('/api/mtf/local_tests', 'GET'),
        ('/api/mtf/send_telegram', 'POST')
    ]

    print("\n1️⃣ Begona foydalanuvchilar (tokensiz) uchun barcha API larni tekshirish:")
    for ep, method in endpoints:
        if method == 'GET':
            res = client.get(ep)
        else:
            res = client.post(ep)
        print(f"  - {ep} [{method}]: status={res.status_code} (Kutilgan: 401)")
        assert res.status_code == 401, f"Xatolik: {ep} tokensiz ochilib ketdi!"

    # 1b. Webhook boshqaruvi va soxta Telegram update'lari
    print("\n1️⃣b Webhook marshrutlari (ruxsatsiz):")
    for ep in ['/set_webhook', '/delete_webhook', '/webhook_info']:
        res = client.get(ep)
        print(f"  - {ep}: status={res.status_code} (Kutilgan: 403)")
        assert res.status_code == 403, f"Xatolik: {ep} ruxsatsiz ochilib ketdi!"
    fake_update = {"update_id": 1, "message": {"message_id": 1, "date": 0, "text": "/cmd whoami",
                   "chat": {"id": 8135594558, "type": "private"},
                   "from": {"id": 8135594558, "is_bot": False, "first_name": "x"}}}
    res = client.post('/' + TOKEN, json=fake_update)
    print(f"  - Secret tokensiz soxta update: status={res.status_code} (Kutilgan: 403)")
    assert res.status_code == 403, "Xatolik: soxta webhook update qabul qilindi!"

    # 2. Noto'g'ri login va parol tekshiruvi
    print("\n2️⃣ Noto'g'ri login/parol bilan kirish tekshiruvi:")
    fake_logins = [
        ("admin", "admin123"),
        ("user", "password"),
        ("Ozodbek", "wrongpassword"),
        ("hacker", "12345678")
    ]
    for u, p in fake_logins:
        res = client.post('/api/auth/login', json={"username": u, "password": p})
        print(f"  - Login: '{u}', Parol: '{p}' -> status={res.status_code}, result={res.get_json().get('error')}")
        assert res.status_code == 401, f"Xatolik: {u} noto'g'ri parol bilan kirdi!"

    # 3. To'g'ri admin login tekshiruvi (Faqat siz: Ozodbek)
    print("\n3️⃣ To'g'ri admin kirishi (Ozodbek):")
    res_admin = client.post('/api/auth/login', json={"username": "Ozodbek", "password": ADMIN_PASSWORD})
    print(f"  - Login status: {res_admin.status_code}")
    data = res_admin.get_json()
    assert res_admin.status_code == 200 and data.get("success") is True, "Admin kira olmadi!"
    token = data.get("token")
    print(f"  - Berilgan token: {token[:20]}... (Foydalanuvchi: {data.get('user', {}).get('full_name')})")

    # 4. Token orqali /api/auth/me tekshiruvi
    print("\n4️⃣ Token orqali /api/auth/me tekshiruvi:")
    res_me = client.get('/api/auth/me', headers={"Authorization": f"Bearer {token}"})
    print(f"  - /api/auth/me status: {res_me.status_code}, data: {res_me.get_json()}")
    assert res_me.status_code == 200, "/api/auth/me token bilan ochilmadi!"

    print("\n==========================================")
    print("🎉 BARCHA XAVFSIZLIK TEKSHIRUVLARI 100% MUVAFFAQIYATLI O'TDI!")
    print("🔒 Hech kim login va parolsiz platformaga kira olmaydi!")
    print("==========================================")

if __name__ == "__main__":
    test_auth_security()
