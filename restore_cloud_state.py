# ============================================================
#  restore_cloud_state.py
#  Bulut holatini lokal atlas.db dan qayta tiklash.
#
#  Nima uchun: insta_scheduler va save_insta_cloud_state da Supabase javob
#  bermagan paytda butun holatni bo'sh dict bilan bosib yuboradigan xato bor edi
#  (tuzatildi). Natijada sent_shortcodes, yt_uploaded_shortcodes va custom_posts
#  yo'qoldi. Lokal SQLite da esa postlar statusi bilan saqlanib qolgan —
#  shu skript o'shandan holatni qayta yig'adi.
#
#  Ishlatish:
#    python restore_cloud_state.py           # dry-run
#    python restore_cloud_state.py --apply
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
    ap.add_argument("--start-from", default="", metavar="SHORTCODE",
                    help="Shu postdan boshlab qayta yuborilsin (undan oldingilari "
                         "yuborilgan deb qoladi). YouTube holatiga tegilmaydi.")
    args = ap.parse_args()

    ok, cloud = ips._fetch_cloud_state()
    if not ok:
        print("XATO: Supabase o'qilmadi. Keyinroq urinib ko'ring.")
        return 1

    print("BULUTDAGI HOZIRGI HOLAT:")
    for k in ("sent_shortcodes", "yt_uploaded_shortcodes", "custom_posts", "deleted_shortcodes"):
        v = cloud.get(k)
        print(f"   {k:<24} {len(v) if isinstance(v, (list, dict)) else 0} ta")

    backup = os.path.join(BASE_DIR, f"cloud_state_backup_{datetime.now():%Y%m%d_%H%M%S}.json")
    with open(backup, "w", encoding="utf-8") as f:
        json.dump(cloud, f, ensure_ascii=False, indent=2)
    print(f"\nZaxira nusxa: {os.path.basename(backup)}")

    # Lokal bazadan haqiqiy holatni yig'ish
    conn = ips.get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT shortcode, status, COALESCE(sent_at,''), youtube_uploaded,
               COALESCE(youtube_url,''), COALESCE(caption,''), COALESCE(post_url,''),
               COALESCE(media_type,'reel'), COALESCE(post_date,'')
        FROM insta_posts_queue
        WHERE shortcode IS NOT NULL AND shortcode <> ''
        ORDER BY id ASC
    """)
    rows = c.fetchall()
    conn.close()
    print(f"Lokal bazada: {len(rows)} ta post")

    sent = dict(cloud.get("sent_shortcodes") or {})
    yt = dict(cloud.get("yt_uploaded_shortcodes") or {})
    custom = list(cloud.get("custom_posts") or [])
    have_custom = {p.get("shortcode") for p in custom}
    seeded = {p.get("shortcode") for p in ips.DEFAULT_SEEDED_POSTS}

    add_sent = add_yt = add_custom = 0
    for sc, status, sent_at, yt_up, yt_url, cap, purl, mtype, pdate in rows:
        if status == "SENT" and sc not in sent:
            sent[sc] = sent_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            add_sent += 1
        if int(yt_up or 0) == 1 and sc not in yt:
            yt[sc] = yt_url or ""
            add_yt += 1
        # Kodda zaxira sifatida yo'q postlar custom_posts orqali saqlanadi,
        # aks holda Vercel navbatni qayta qurganda ular yo'qoladi
        if sc not in seeded and sc not in have_custom:
            custom.append({
                "shortcode": sc,
                "post_url": purl or f"https://www.instagram.com/reel/{sc}",
                "media_type": mtype,
                "caption": cap,
                "media_url": "",
                "post_date": pdate,
            })
            have_custom.add(sc)
            add_custom += 1

    print("\nQO'SHILADI:")
    print(f"   sent_shortcodes        +{add_sent:<4} -> {len(sent)}")
    print(f"   yt_uploaded_shortcodes +{add_yt:<4} -> {len(yt)}")
    print(f"   custom_posts           +{add_custom:<4} -> {len(custom)}")

    # --- Boshlanish nuqtasi ---
    reset_codes = []
    if args.start_from:
        order = [r[0] for r in rows]
        if args.start_from not in order:
            print(f"\nXATO: {args.start_from} navbatda topilmadi.")
            return 1
        start_i = order.index(args.start_from)
        # Shu post va undan keyingilari "yuborilmagan" holatiga qaytariladi.
        # youtube_uploaded ataylab tegilmaydi — aks holda YouTube'ga dublikat chiqadi.
        reset_codes = [sc for sc in order[start_i:] if sc in sent]
        for sc in reset_codes:
            sent.pop(sc, None)
        print(f"\nQAYTA YUBORILADI ({args.start_from} dan boshlab): {len(reset_codes)} ta")
        for sc in reset_codes[:10]:
            print(f"   {sc}")
        print(f"   sent_shortcodes yakuniy: {len(sent)}")
        print("   (YouTube holati o'zgarmaydi — dublikat video chiqmasligi uchun)")

    if not args.apply:
        print("\n[dry-run] Yozilmadi. Yozish uchun: --apply")
        return 0

    if reset_codes:
        conn = ips.get_db_connection()
        c = conn.cursor()
        for sc in reset_codes:
            c.execute("UPDATE insta_posts_queue SET status='PENDING', sent_at=NULL "
                      "WHERE shortcode = ?", (sc,))
        conn.commit()
        conn.close()
        print(f"Lokal bazada {len(reset_codes)} ta post PENDING qilindi.")

    cloud["sent_shortcodes"] = sent
    cloud["yt_uploaded_shortcodes"] = yt
    cloud["custom_posts"] = custom
    ips.save_insta_cloud_state(cloud)

    ok2, after = ips._fetch_cloud_state()
    if not ok2:
        print("OGOHLANTIRISH: tekshirib bo'lmadi.")
        return 1
    print("\nTEKSHIRUV:")
    for k in ("sent_shortcodes", "yt_uploaded_shortcodes", "custom_posts"):
        print(f"   {k:<24} {len(after.get(k) or [])} ta")
    return 0


if __name__ == "__main__":
    sys.exit(main())
