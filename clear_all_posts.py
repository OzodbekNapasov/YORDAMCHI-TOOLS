# ============================================================
#  clear_all_posts.py
#  Instagram navbatini to'liq tozalash (qo'lda havola bilan qo'shish uchun).
#
#  Nimalar tozalanadi:
#    - lokal insta_posts_queue jadvali
#    - bulutdagi custom_posts
#    - bulutdagi sent_shortcodes va yt_uploaded_shortcodes
#
#  Nega tarix ham tozalanadi: init_insta_tables bulutdagi sent_shortcodes va
#  yt_uploaded_shortcodes bo'yicha navbatga belgi qo'yadi. Ular qolsa, qo'lda
#  qayta qo'shgan post darhol "yuborilgan" deb belgilanib, hech qachon
#  chiqmaydi. Shuning uchun toza boshlash uchun ular ham olib tashlanadi.
#
#  Kodga yozilgan zaxira post (DEFAULT_SEEDED_POSTS) deleted_shortcodes ga
#  qo'yiladi — aks holda u har safar qaytib keladi.
#
#  Sozlamalar (jadval vaqtlari, kanal ID) TEGILMAYDI.
#
#  Ishlatish:
#    python clear_all_posts.py            # dry-run
#    python clear_all_posts.py --apply
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

import services.insta_poster_service as ips


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--clear-youtube-history", action="store_true",
                    help="YouTube tarixini ham tozalash. DIQQAT: ilgari YouTube'ga "
                         "chiqqan postni qayta qo'shsangiz, u ikkinchi marta "
                         "yuklanadi va kanalda dublikat paydo bo'ladi.")
    args = ap.parse_args()

    conn = ips.get_db_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM insta_posts_queue")
    local_n = c.fetchone()[0]
    conn.close()

    ok, cloud = ips._fetch_cloud_state()
    if not ok:
        print("XATO: Supabase o'qilmadi. Keyinroq urinib ko'ring.")
        return 1

    seeded = [p.get("shortcode") for p in ips.DEFAULT_SEEDED_POSTS if p.get("shortcode")]

    print("HOZIRGI HOLAT")
    print("-" * 46)
    print(f"   lokal navbat             : {local_n} ta")
    print(f"   bulut custom_posts       : {len(cloud.get('custom_posts') or [])} ta")
    print(f"   bulut sent_shortcodes    : {len(cloud.get('sent_shortcodes') or {})} ta")
    print(f"   bulut yt_uploaded        : {len(cloud.get('yt_uploaded_shortcodes') or {})} ta")
    print(f"   kodga yozilgan zaxira    : {len(seeded)} ta {seeded}")

    print("\nTOZALANGANDAN KEYIN")
    print("-" * 46)
    print("   lokal navbat             : 0 ta")
    print("   bulut custom_posts       : 0 ta")
    print("   bulut sent_shortcodes    : 0 ta")
    if args.clear_youtube_history:
        print("   bulut yt_uploaded        : 0 ta  <-- TOZALANADI")
        print("      DIQQAT: ilgari YouTube'ga chiqqan postni qayta qo'shsangiz,")
        print("      u ikkinchi marta yuklanadi (kanalda dublikat).")
    else:
        print(f"   bulut yt_uploaded        : {len(cloud.get('yt_uploaded_shortcodes') or {})} ta  "
              "(SAQLANADI — YouTube'da dublikat chiqmasligi uchun)")
    print(f"   deleted_shortcodes       : {len(seeded)} ta (zaxira post qaytmasligi uchun)")
    print("\n   Sozlamalar (jadval vaqtlari, kanal) tegilmaydi.")
    print("   Telegram va YouTube'dagi chiqqan postlar O'CHIRILMAYDI —")
    print("   bu faqat platformaning ichki ro'yxati.")

    if not args.apply:
        print("\n[dry-run] Hech narsa o'chirilmadi. Tozalash uchun: --apply")
        return 0

    # Zaxira nusxalar
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cloud_backup = os.path.join(BASE_DIR, f"cloud_state_backup_{stamp}.json")
    with open(cloud_backup, "w", encoding="utf-8") as f:
        json.dump(cloud, f, ensure_ascii=False, indent=2)

    conn = ips.get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM insta_posts_queue")
    cols = [d[0] for d in c.description]
    queue_rows = [dict(zip(cols, r)) for r in c.fetchall()]
    queue_backup = os.path.join(BASE_DIR, f"queue_backup_{stamp}.json")
    with open(queue_backup, "w", encoding="utf-8") as f:
        json.dump(queue_rows, f, ensure_ascii=False, indent=2, default=str)

    print(f"\nZaxira nusxalar:")
    print(f"   {os.path.basename(cloud_backup)}")
    print(f"   {os.path.basename(queue_backup)}  ({len(queue_rows)} ta post)")

    # Lokal tozalash
    c.execute("DELETE FROM insta_posts_queue")
    try:
        c.execute("DELETE FROM insta_post_likes")
    except Exception:
        pass
    conn.commit()
    conn.close()

    # Bulut tozalash
    cloud["custom_posts"] = []
    cloud["sent_shortcodes"] = {}
    if args.clear_youtube_history:
        cloud["yt_uploaded_shortcodes"] = {}
    cloud["deleted_shortcodes"] = list(seeded)
    ips.save_insta_cloud_state(cloud)

    # Tekshirish
    ok2, after = ips._fetch_cloud_state()
    conn = ips.get_db_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM insta_posts_queue")
    left = c.fetchone()[0]
    conn.close()

    print("\nTEKSHIRUV")
    print("-" * 46)
    print(f"   lokal navbat             : {left} ta")
    if ok2:
        print(f"   bulut custom_posts       : {len(after.get('custom_posts') or [])} ta")
        print(f"   bulut sent_shortcodes    : {len(after.get('sent_shortcodes') or {})} ta")
        print(f"   bulut yt_uploaded        : {len(after.get('yt_uploaded_shortcodes') or {})} ta")
        print(f"   deleted_shortcodes       : {len(after.get('deleted_shortcodes') or [])} ta")

    print("\nTayyor. Endi panelda 'Havola Bilan Qo'shish' orqali qo'shishingiz mumkin.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
