# ============================================================
#  sync_queue_to_cloud.py
#  Lokal navbatdagi postlarni Supabase'ga (custom_posts) ko'chirish.
#
#  Nima uchun kerak: Vercel'da baza /tmp da har safar noldan quriladi va
#  navbat = DEFAULT_SEEDED_POSTS (kodda) + custom_posts (Supabase) tarzida
#  yig'iladi. Kodadagi ro'yxat 1 taga qisqartirilgani uchun lokal navbatdagi
#  postlar Vercel'ga ko'rinmaydi. Bu skript ularni Supabase'ga qo'shadi.
#
#  Ishlatish:
#    python sync_queue_to_cloud.py              # dry-run: faqat ko'rsatadi
#    python sync_queue_to_cloud.py --apply      # haqiqatan yozadi
#    python sync_queue_to_cloud.py --apply --start-id 40
# ============================================================

import os
import sys
import json
import argparse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

DEFAULT_START_ID = 40  # DX3Qge2IbY7


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start-id", type=int, default=DEFAULT_START_ID)
    ap.add_argument("--apply", action="store_true", help="Haqiqatan yozish")
    args = ap.parse_args()

    import services.insta_poster_service as ips

    state = ips.load_insta_cloud_state() or {}
    custom = list(state.get("custom_posts") or [])
    yt_done = set((state.get("yt_uploaded_shortcodes") or {}).keys())
    seeded = {p.get("shortcode") for p in ips.DEFAULT_SEEDED_POSTS}
    have = {p.get("shortcode") for p in custom} | seeded

    print(f"Bulutdagi hozirgi holat: custom_posts={len(custom)}, "
          f"kodda seeded={len(seeded)}, yt_uploaded={len(yt_done)}")

    # Zaxira nusxa — nimadir noto'g'ri ketsa qaytarish uchun
    backup_path = os.path.join(
        BASE_DIR, f"cloud_state_backup_{datetime.now():%Y%m%d_%H%M%S}.json")
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"Zaxira nusxa: {os.path.basename(backup_path)}")

    conn = ips.get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT shortcode, COALESCE(caption,''), COALESCE(post_url,''),
               COALESCE(media_url,''), COALESCE(post_date,''), COALESCE(media_type,'reel')
        FROM insta_posts_queue
        WHERE id >= ?
          AND (media_type IN ('reel','video','unknown') OR post_url LIKE '%/reel/%')
        ORDER BY id ASC
    """, (args.start_id,))
    rows = c.fetchall()
    conn.close()

    added = []
    for sc, cap, purl, murl, pdate, mtype in rows:
        if not sc or sc in have or sc in yt_done:
            continue
        added.append({
            "shortcode": sc,
            "post_url": purl or f"https://www.instagram.com/reel/{sc}",
            "media_type": mtype or "reel",
            "caption": cap,
            "media_url": murl,
            "post_date": pdate,
        })

    print(f"\nLokal navbatda id>={args.start_id}: {len(rows)} ta")
    print(f"Qo'shiladi: {len(added)} ta")
    for p in added[:5]:
        print(f"   {p['shortcode']:<14} {p['caption'][:45]}")
    if len(added) > 5:
        print(f"   ... yana {len(added) - 5} ta")

    if not added:
        print("\nQo'shadigan narsa yo'q.")
        return 0

    if not args.apply:
        print("\n[dry-run] Hech narsa yozilmadi. Yozish uchun: --apply")
        return 0

    state["custom_posts"] = custom + added
    ips.save_insta_cloud_state(state)

    check = ips.load_insta_cloud_state() or {}
    now_n = len(check.get("custom_posts") or [])
    print(f"\nYozildi. custom_posts: {len(custom)} -> {now_n}")
    if now_n != len(custom) + len(added):
        print("OGOHLANTIRISH: kutilgan son mos kelmadi, zaxiradan tekshiring!")
        return 1

    print("Vercel'da 'Yangilash' tugmasini bosing — postlar ko'rinishi kerak.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
