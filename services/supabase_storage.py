# ============================================================
#  services/supabase_storage.py
#  ATLAS Universal Bot Platform — Supabase Cloud Storage & DB Bridge
# ============================================================

import os
import requests
import json
import mimetypes

def get_credentials():
    from services.atlas_db import _get_supabase_credentials
    return _get_supabase_credentials()


def get_headers():
    _, key = get_credentials()
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}"
    }


def upload_document_to_supabase(local_file_path: str, destination_filename: str) -> str:
    """
    Mahalliy PNG yoki Docx faylni Supabase Storage (documents bucket) ga yuklaydi
    va doimiy public CDN havolasini qaytaradi.
    """
    if not os.path.exists(local_file_path):
        return ""

    try:
        import re
        clean_key = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', destination_filename)
        mime_type, _ = mimetypes.guess_type(local_file_path)
        if not mime_type:
            mime_type = "image/png" if local_file_path.endswith(".png") else "application/octet-stream"

        supa_url, _ = get_credentials()
        upload_url = f"{supa_url}/storage/v1/object/{BUCKET_NAME}/{clean_key}"
        
        with open(local_file_path, "rb") as f:
            file_data = f.read()

        res = requests.post(
            upload_url,
            headers={
                **get_headers(),
                "Content-Type": mime_type,
                "x-upsert": "true"
            },
            data=file_data,
            timeout=15
        )

        if res.status_code in [200, 201]:
            public_cdn_url = f"{supa_url}/storage/v1/object/public/{BUCKET_NAME}/{clean_key}"
            print(f"[Supabase Storage] Yuklandi: {public_cdn_url}")
            return public_cdn_url
        else:
            print(f"[Supabase Storage Error] Status {res.status_code}: {res.text}")
            return ""
    except Exception as e:
        print(f"[Supabase Storage Exception] {e}")
        return ""


def delete_document_from_supabase(destination_filename: str) -> bool:
    """
    Supabase Storage dan faylni o'chiradi.
    """
    try:
        supa_url, _ = get_credentials()
        delete_url = f"{supa_url}/storage/v1/object/{BUCKET_NAME}/{destination_filename}"
        res = requests.delete(delete_url, headers=get_headers(), timeout=10)
        return res.status_code in [200, 204]
    except Exception:
        return False
