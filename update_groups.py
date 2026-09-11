# ============================================================
#  update_groups.py
#  O'quv yili almashganda guruhlar ro'yxatini va kurs raqamlarini yangilash.
#
#  Ishlatish:
#    python update_groups.py            # dry-run: faqat nima o'zgarishini ko'rsatadi
#    python update_groups.py --apply    # haqiqatan yozadi
# ============================================================

import os
import sys
import json
import argparse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

import requests
from services.atlas_db import _get_supabase_credentials

TABLE = "atlas_student_groups"

# ------------------------------------------------------------
# 2026/2027 o'quv yili holati
# ------------------------------------------------------------

# Yangi 1-kurs guruhlari va ularning rahbarlari
NEW_FIRST_COURSE = [
    ("26-01", "Mirzayeva.D"),
    ("26-02", "Ochilov.D"),
    ("26-03", "To'rayeva.S"),
    ("26-04", "Hamdamova.M"),
    ("26-05", "Rayimova.X"),
    ("26-06", "Yuldashev.O"),
    ("26-07", "Asraliyev.A"),
]

# Mavjud guruhlarning yangi kurs raqami
COURSE_MOVES = {
    "24-11": 3, "24-12": 3, "24-13": 3,
    "24-14": 2, "24-15": 2, "24-16": 2,
    "25-16": 2, "25-17": 2, "25-18": 2, "25-19": 2,
    "25-20": 2, "25-21": 2, "25-22": 2, "25-23": 2,
}


def headers():
    _url, key = _get_supabase_credentials()
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


def fetch_all(url, h):
    r = requests.get(f"{url}/rest/v1/{TABLE}?select=*&order=group_name",
                     headers=h, timeout=25)
    r.raise_for_status()
    return r.json()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Haqiqatan yozish")
    args = ap.parse_args()

    url, key = _get_supabase_credentials()
    if not url or not key:
        print("XATO: Supabase kalitlari topilmadi (.env).")
        return 1

    h = headers()
    rows = fetch_all(url, h)
    cols = set(rows[0].keys()) if rows else set()
    has_rahbar = "rahbar_name" in cols

    print(f"Bazadagi guruhlar: {len(rows)} ta")
    if not has_rahbar:
        print("\nOGOHLANTIRISH: 'rahbar_name' ustuni yo'q — rahbarlar SAQLANMAYDI.")
        print("Avval Supabase Dashboard > SQL Editor da shuni bajaring:\n")
        print("  ALTER TABLE public.atlas_student_groups")
        print("    ADD COLUMN IF NOT EXISTS rahbar_name TEXT;\n")

    # Zaxira nusxa — qaytarish kerak bo'lsa
    backup = os.path.join(BASE_DIR, f"groups_backup_{datetime.now():%Y%m%d_%H%M%S}.json")
    with open(backup, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"Zaxira nusxa: {os.path.basename(backup)}\n")

    existing = {str(g.get("group_name", "")).strip(): g for g in rows}

    # ---- 1. Kurs raqamini o'zgartirish ----
    updates = []
    for gname, new_level in COURSE_MOVES.items():
        g = existing.get(gname)
        if not g:
            print(f"  ? {gname}: bazada topilmadi, o'tkazib yuborildi")
            continue
        old = g.get("course_level")
        if old != new_level:
            updates.append((gname, old, new_level))

    # ---- 2. Yangi guruhlar ----
    inserts = [(gn, rah) for gn, rah in NEW_FIRST_COURSE if gn not in existing]
    already = [gn for gn, _ in NEW_FIRST_COURSE if gn in existing]

    print("KURS O'ZGARISHLARI:")
    if updates:
        for gname, old, new in updates:
            print(f"   {gname}: {old}-kurs -> {new}-kurs")
    else:
        print("   (o'zgarish yo'q)")

    print("\nYANGI GURUHLAR (1-kurs):")
    if inserts:
        for gn, rah in inserts:
            print(f"   {gn}  rahbar: {rah}")
    else:
        print("   (yangisi yo'q)")
    if already:
        print(f"   allaqachon mavjud: {', '.join(already)}")

    if not args.apply:
        print("\n[dry-run] Hech narsa yozilmadi. Yozish uchun: --apply")
        return 0

    # ---- Yozish ----
    ok_u = 0
    for gname, _old, new in updates:
        r = requests.patch(
            f"{url}/rest/v1/{TABLE}?group_name=eq.{gname}",
            headers=h, json={"course_level": new}, timeout=20)
        if r.status_code in (200, 204):
            ok_u += 1
        else:
            print(f"   XATO {gname}: HTTP {r.status_code} {r.text[:90]}")

    ok_i = 0
    for gn, rah in inserts:
        rec = {"group_name": gn, "course_level": 1}
        if has_rahbar:
            rec["rahbar_name"] = rah
        else:
            rec["notes"] = f"Guruh rahbari: {rah}"
        r = requests.post(f"{url}/rest/v1/{TABLE}", headers=h, json=rec, timeout=20)
        if r.status_code in (200, 201, 204):
            ok_i += 1
        else:
            print(f"   XATO {gn}: HTTP {r.status_code} {r.text[:90]}")

    # ---- Rahbarlarni mavjud yangi guruhlarga ham yozish ----
    if has_rahbar:
        for gn, rah in NEW_FIRST_COURSE:
            if gn in existing:
                requests.patch(f"{url}/rest/v1/{TABLE}?group_name=eq.{gn}",
                               headers=h, json={"rahbar_name": rah}, timeout=20)

    print(f"\nYangilandi: {ok_u}/{len(updates)}   Qo'shildi: {ok_i}/{len(inserts)}")

    # ---- Tekshirish ----
    after = fetch_all(url, h)
    lv = {}
    for g in after:
        lv[g.get("course_level")] = lv.get(g.get("course_level"), 0) + 1
    print(f"Endi bazada: {len(after)} ta guruh")
    for k in sorted(lv, key=lambda x: (x is None, x)):
        print(f"   {k}-kurs: {lv[k]} ta")
    return 0


if __name__ == "__main__":
    sys.exit(main())
