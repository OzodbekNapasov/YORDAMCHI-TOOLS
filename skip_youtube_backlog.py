# ============================================================
#  skip_youtube_backlog.py
#  YouTube'ga yuklanmagan eski postlarni "o'tkazib yuborilgan" deb belgilash.
#
#  Nima uchun: Telegramga chiqqan, lekin YouTube'ga hech qachon yuklanmagan
#  eski reellar to'planib qolgan. Ularni endi yuklash shart bo'lmasa, shu skript
#  ularni "yuklangan" deb belgilaydi va YouTube jadvali faqat yangi postlarni
#  oladi. Videolarning O'ZI hech qayerdan o'chirilmaydi — faqat belgi qo'yiladi.
#
#  Ishlatish:
#    python skip_youtube_backlog.py                       # dry-run: ro'yxat
#    python skip_youtube_backlog.py --apply               # hammasini o'tkazib yuborish
#    python skip_youtube_backlog.py --before Dc123 --apply  # faqat shu postgacha
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

#: Belgida shu matn turadi — keyinchalik "nega yuklanmagan" degan savolga javob
SKIP_MARK = "skipped"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--before", default="", metavar="SHORTCODE",
                    help="Faqat shu postdan OLDINGILARI o'tkazib yuboriladi")
    args = ap.parse_args()

    conn = ips.get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT id, shortcode, substr(COALESCE(caption,''),1,36)
                 FROM insta_posts_queue
                 WHERE youtube_uploaded = 0
                   AND (media_type IN ('reel','video','unknown')
                        OR post_url LIKE '%/reel/%')
                 ORDER BY id ASC""")
    pending = c.fetchall()

    if args.before:
        c.execute("SELECT id FROM insta_posts_queue WHERE shortcode = ?", (args.before,))
        row = c.fetchone()
        if not row:
            print(f"XATO: {args.before} navbatda topilmadi.")
            conn.close()
            return 1
        cutoff = row[0]
        pending = [p for p in pending if p[0] < cutoff]
        print(f"Chegara: id < {cutoff} ({args.before})")

    conn.close()

    if not pending:
        print("O'tkazib yuboriladigan post yo'q — YouTube navbati toza.")
        return 0

    print(f"O'TKAZIB YUBORILADI: {len(pending)} ta\n")
    print(f"{'id':>5} {'shortcode':<14} izoh")
    print("-" * 58)
    for p in pending:
        print(f"{p[0]:>5} {p[1]:<14} {p[2]}")

    print("\nVideolar o'chirilmaydi — faqat 'yuklangan' belgisi qo'yiladi,")
    print("shunda YouTube jadvali ularni qayta olmaydi.")

    if not args.apply:
        print("\n[dry-run] Yozilmadi. Yozish uchun: --apply")
        return 0

    ok, cloud = ips._fetch_cloud_state()
    if not ok:
        print("\nXATO: Supabase o'qilmadi — yozilmadi. Keyinroq urinib ko'ring.")
        return 1

    backup = os.path.join(BASE_DIR, f"cloud_state_backup_{datetime.now():%Y%m%d_%H%M%S}.json")
    with open(backup, "w", encoding="utf-8") as f:
        json.dump(cloud, f, ensure_ascii=False, indent=2)
    print(f"\nZaxira nusxa: {os.path.basename(backup)}")

    # Lokal baza
    conn = ips.get_db_connection()
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for pid, sc, _cap in pending:
        c.execute("""UPDATE insta_posts_queue
                     SET youtube_uploaded = 1, youtube_url = ?, youtube_uploaded_at = ?
                     WHERE id = ?""", (SKIP_MARK, now, pid))
    conn.commit()
    conn.close()

    # Bulut
    yt = dict(cloud.get("yt_uploaded_shortcodes") or {})
    for _pid, sc, _cap in pending:
        yt.setdefault(sc, SKIP_MARK)
    cloud["yt_uploaded_shortcodes"] = yt
    ips.save_insta_cloud_state(cloud)

    ok2, after = ips._fetch_cloud_state()
    print(f"\nBelgilandi: {len(pending)} ta")
    if ok2:
        print(f"Bulutda 'yuklangan': {len(after.get('yt_uploaded_shortcodes') or {})} ta")

    conn = ips.get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT COUNT(*) FROM insta_posts_queue
                 WHERE youtube_uploaded = 0
                   AND (media_type IN ('reel','video','unknown')
                        OR post_url LIKE '%/reel/%')""")
    print(f"YouTube uchun qolgan: {c.fetchone()[0]} ta")
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
