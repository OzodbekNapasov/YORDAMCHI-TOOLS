# ============================================================
#  services/mtf_library.py
#  MyTestX testlar bazasi: fayllarning o'zi Telegram kanalda saqlanadi,
#  ro'yxat (indeks) esa Supabase `atlas_settings` jadvalida — har bir test alohida qator.
#  Alohida qator tanlangani: kanalga bir vaqtda 100 ta fayl tashlanganda ham
#  parallel webhooklar bir-birining yozuvini o'chirib yubormaydi.
# ============================================================

import hashlib
import json
import os
import time
from datetime import datetime

import requests

CATEGORY = "mtf_library"
CONFIG_KEY = "mtf_library_channel"
KEY_PREFIX = "mtf:"
DEFAULT_FOLDER = "Umumiy"
TEST_EXTENSIONS = (".mtf", ".xml")

_CACHE = {"ts": 0.0, "items": None}
_CACHE_TTL = 30


def _supa():
    from services.atlas_db import _get_supabase_credentials
    url, key = _get_supabase_credentials()
    headers = {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    return url, key, headers


def is_test_file(file_name: str) -> bool:
    return (file_name or "").lower().endswith(TEST_EXTENSIONS)


def folder_from_caption(caption: str) -> str:
    """Kanal postining izohidan papka nomi: birinchi #heshteg yoki birinchi qator."""
    caption = (caption or "").strip()
    if not caption:
        return DEFAULT_FOLDER
    for word in caption.split():
        if word.startswith("#") and len(word) > 1:
            return word[1:].replace("_", " ").strip()[:60] or DEFAULT_FOLDER
    return caption.splitlines()[0].strip()[:60] or DEFAULT_FOLDER


def folder_id(folder: str) -> str:
    """callback_data uchun qisqa va barqaror papka identifikatori."""
    return hashlib.md5(folder.encode("utf-8")).hexdigest()[:8]


# ---------------- Kanal sozlamasi ----------------

def get_storage():
    """Baza joyi: {"chat_id", "thread_id", "title"} — yopiq kanal yoki mavzuli guruhdagi mavzu.
    thread_id faqat guruh mavzusi uchun (kanalda None)."""
    env_val = (os.environ.get("MTF_CHANNEL_ID") or "").strip()
    if env_val.lstrip("-").isdigit():
        thread = (os.environ.get("MTF_THREAD_ID") or "").strip()
        return {"chat_id": int(env_val), "thread_id": int(thread) if thread.isdigit() else None, "title": ""}
    url, key, headers = _supa()
    if not key:
        return None
    try:
        r = requests.get(f"{url}/rest/v1/atlas_settings?key=eq.{CONFIG_KEY}&select=value",
                         headers=headers, timeout=5)
        if r.status_code == 200 and r.json():
            data = json.loads(r.json()[0].get("value") or "{}")
            if data.get("chat_id"):
                return {"chat_id": int(data["chat_id"]),
                        "thread_id": int(data["thread_id"]) if data.get("thread_id") else None,
                        "title": data.get("title") or ""}
    except Exception as e:
        print(f"[MTF Library] baza sozlamasini o'qib bo'lmadi: {e}")
    return None


def get_channel_id():
    st = get_storage()
    return st["chat_id"] if st else None


def set_channel(chat_id: int, title: str = "", thread_id=None) -> bool:
    url, key, headers = _supa()
    if not key:
        return False
    h = dict(headers, Prefer="resolution=merge-duplicates")
    payload = {"key": CONFIG_KEY, "value": json.dumps({"chat_id": chat_id, "title": title, "thread_id": thread_id},
                                                      ensure_ascii=False),
               "category": "mtf_library_config", "description": "MyTestX testlar bazasi kanali"}
    r = requests.post(f"{url}/rest/v1/atlas_settings", headers=h, json=payload, timeout=5)
    return r.status_code in (200, 201, 204)


# ---------------- Testlar indeksi ----------------

def add_test(file_id: str, file_unique_id: str, file_name: str, file_size: int = 0,
             channel_msg_id=None, folder: str = DEFAULT_FOLDER, keep_existing_folder: bool = True) -> dict:
    """Testni indeksga qo'shadi (yoki yangilaydi). Qaytaradi: yozuv + "is_new" belgisi."""
    existing = get_test(file_unique_id)
    entry = {
        "uid": file_unique_id,
        "file_id": file_id,
        "name": file_name,
        "size": int(file_size or 0),
        "folder": (existing or {}).get("folder") if (existing and keep_existing_folder) else (folder or DEFAULT_FOLDER),
        "channel_msg_id": channel_msg_id or (existing or {}).get("channel_msg_id"),
        "added_at": (existing or {}).get("added_at") or datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    _save(entry)
    entry["is_new"] = existing is None
    return entry


def _save(entry: dict):
    url, key, headers = _supa()
    if not key:
        raise RuntimeError("Supabase kaliti sozlanmagan")
    h = dict(headers, Prefer="resolution=merge-duplicates")
    clean = {k: v for k, v in entry.items() if k != "is_new"}
    payload = {"key": KEY_PREFIX + entry["uid"], "value": json.dumps(clean, ensure_ascii=False),
               "category": CATEGORY, "description": entry["name"][:200]}
    r = requests.post(f"{url}/rest/v1/atlas_settings", headers=h, json=payload, timeout=6)
    if r.status_code not in (200, 201, 204):
        raise RuntimeError(f"Indeksga yozib bo'lmadi: {r.status_code} {r.text[:200]}")
    _CACHE["items"] = None


def get_test(uid: str):
    url, key, headers = _supa()
    if not key:
        return None
    r = requests.get(f"{url}/rest/v1/atlas_settings?key=eq.{KEY_PREFIX}{uid}&select=value",
                     headers=headers, timeout=5)
    if r.status_code == 200 and r.json():
        try:
            return json.loads(r.json()[0]["value"])
        except Exception:
            return None
    return None


def set_folder(uid: str, folder: str):
    entry = get_test(uid)
    if not entry:
        return None
    entry["folder"] = (folder or DEFAULT_FOLDER).strip()[:60] or DEFAULT_FOLDER
    _save(entry)
    return entry


def delete_test(uid: str) -> bool:
    url, key, headers = _supa()
    r = requests.delete(f"{url}/rest/v1/atlas_settings?key=eq.{KEY_PREFIX}{uid}", headers=headers, timeout=5)
    _CACHE["items"] = None
    return r.status_code in (200, 204)


def list_tests(force: bool = False) -> list:
    """Barcha testlar (nomi bo'yicha saralangan). 30 soniya xotirada keshlanadi."""
    if not force and _CACHE["items"] is not None and time.time() - _CACHE["ts"] < _CACHE_TTL:
        return _CACHE["items"]
    url, key, headers = _supa()
    if not key:
        return []
    items, offset, page = [], 0, 1000
    while True:
        r = requests.get(f"{url}/rest/v1/atlas_settings?category=eq.{CATEGORY}&select=value"
                         f"&order=key.asc&limit={page}&offset={offset}", headers=headers, timeout=8)
        if r.status_code != 200:
            break
        rows = r.json()
        for row in rows:
            try:
                items.append(json.loads(row["value"]))
            except Exception:
                pass
        if len(rows) < page:
            break
        offset += page
    items.sort(key=lambda e: (e.get("folder") or "", (e.get("name") or "").lower()))
    _CACHE.update(ts=time.time(), items=items)
    return items


def folders(items=None) -> list:
    """[(papka, testlar_soni)] alifbo tartibida."""
    counts = {}
    for e in (items if items is not None else list_tests()):
        f = e.get("folder") or DEFAULT_FOLDER
        counts[f] = counts.get(f, 0) + 1
    return sorted(counts.items(), key=lambda x: x[0].lower())


def search(query: str, limit: int = 30) -> list:
    q = (query or "").strip().lower()
    if not q:
        return []
    return [e for e in list_tests() if q in (e.get("name") or "").lower() or q in (e.get("folder") or "").lower()][:limit]
