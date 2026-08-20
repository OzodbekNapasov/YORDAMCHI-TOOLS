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

def test_all_downloads():
    token = create_session(1, "Ozodbek", "Ozodbek Napasov", "superadmin")
    client = app.test_client()

    print("==========================================")
    print("🔍 ATLAS PLATFORMA YUKLAB OLISH TESTLARI")
    print("==========================================")
    
    # 1. Test Document PNG download
    res_png = client.get('/api/documents/download/14', headers={"Authorization": f"Bearer {token}"})
    print(f"1. Document PNG (id:14) status: {res_png.status_code}, length: {len(res_png.data)} bytes")
    
    # 2. Test Document DOCX download
    res_docx = client.get('/api/documents/download_docx/14', headers={"Authorization": f"Bearer {token}"})
    print(f"2. Document DOCX (id:14) status: {res_docx.status_code}, length: {len(res_docx.data)} bytes")
    if res_docx.status_code != 200:
        print(f"   Error: {res_docx.get_json() if res_docx.is_json else res_docx.data}")

    # 3. Test Query param token: /api/documents/download_docx/14?token=...
    res_query_docx = client.get(f'/api/documents/download_docx/14?token={token}')
    print(f"3. Query param token DOCX status: {res_query_docx.status_code}, length: {len(res_query_docx.data)} bytes")

    # 4. Test Sample Survey Excel
    res_survey = client.get('/api/amaliyot/survey/sample-excel')
    print(f"4. Sample Survey Excel status: {res_survey.status_code}, length: {len(res_survey.data)} bytes")

    # 5. Test Cookie token
    client.set_cookie("atlas_token", token)
    res_cookie_docx = client.get('/api/documents/download_docx/14')
    print(f"5. Cookie token DOCX status: {res_cookie_docx.status_code}, length: {len(res_cookie_docx.data)} bytes")

    print("\n==========================================")

if __name__ == "__main__":
    test_all_downloads()
