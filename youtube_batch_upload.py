# ============================================================
#  youtube_batch_upload.py
#  Navbatdagi Instagram reel'larini YouTube'ga paket bilan yuklash.
#
#  YouTube Data API kunlik kvotasi 10 000 birlik, bitta yuklash
#  1 600 birlik turadi -> kuniga ~6 ta. Skript kvota tugaganda
#  o'zi to'xtaydi va ertaga qolgan joyidan davom etadi.
#
#  Ishlatish:
#    python youtube_batch_upload.py                 # standart: 5 ta
#    python youtube_batch_upload.py --limit 6
#    python youtube_batch_upload.py --start-id 40 --limit 6
#    python youtube_batch_upload.py --privacy unlisted
#    python youtube_batch_upload.py --dry-run       # yuklamaydi, faqat ko'rsatadi
# ============================================================

import os
import sys
import time
import argparse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

LOG_FILE = os.path.join(BASE_DIR, "youtube_batch.log")

# DX3Qge2IbY7 — foydalanuvchi ko'rsatgan boshlanish nuqtasi
DEFAULT_START_ID = 40
DEFAULT_LIMIT = 5

# Kvota tugaganini bildiruvchi belgilar
QUOTA_MARKERS = ("quotaexceeded", "dailylimitexceeded", "quota", "ratelimitexceeded")


def log(msg):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def is_quota_error(err_text):
    low = str(err_text).lower()
    return any(m in low for m in QUOTA_MARKERS)


def fetch_pending(conn, start_id, limit):
    """Yuklanmagan reel'larni eskisidan yangisiga qarab olish"""
    cur = conn.cursor()
    cur.execute("""
        SELECT id, shortcode, post_url, caption
        FROM insta_posts_queue
        WHERE id >= ?
          AND youtube_uploaded = 0
          AND (media_type IN ('reel','video','unknown') OR post_url LIKE '%/reel/%')
        ORDER BY id ASC
        LIMIT ?
    """, (start_id, limit))
    return cur.fetchall()


def mark_uploaded(conn, post_id, shortcode, yt_url, caption):
    cur = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        UPDATE insta_posts_queue
        SET youtube_uploaded = 1, youtube_url = ?, youtube_uploaded_at = ?
        WHERE id = ?
    """, (yt_url, now_str, post_id))
    conn.commit()

    # Supabase bulut holatiga ham yozish (Vercel paneli shundan o'qiydi)
    try:
        from services.insta_poster_service import mark_youtube_uploaded_in_cloud
        mark_youtube_uploaded_in_cloud(shortcode, yt_url or "")
    except Exception as e:
        log(f"    ! Supabase sinxronlash o'tmadi: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start-id", type=int, default=DEFAULT_START_ID)
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    ap.add_argument("--privacy", default="public",
                    choices=["public", "unlisted", "private"])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    from services.insta_poster_service import get_db_connection, _download_hd_video_ytdlp
    from services.youtube_service import upload_video_to_youtube, is_youtube_ready

    log("=" * 58)
    log(f"Paketli yuklash boshlandi (limit={args.limit}, privacy={args.privacy})")

    if not is_youtube_ready():
        log("XATO: YouTube avtorizatsiyasi yo'q. `python setup_youtube.py` ni ishga tushiring.")
        return 1

    conn = get_db_connection()
    rows = fetch_pending(conn, args.start_id, args.limit)

    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM insta_posts_queue
        WHERE id >= ? AND youtube_uploaded = 0
          AND (media_type IN ('reel','video','unknown') OR post_url LIKE '%/reel/%')
    """, (args.start_id,))
    total_left = cur.fetchone()[0]

    if not rows:
        log(f"Yuklanadigan video qolmadi. Hammasi tugagan.")
        conn.close()
        return 0

    log(f"Navbatda jami {total_left} ta, shu safar {len(rows)} tasi olinadi.")

    done = 0
    quota_hit = False

    for row in rows:
        post_id, shortcode, post_url, caption = row[0], row[1], row[2], (row[3] or "")
        head = caption.split("\n")[0][:50] if caption else "(izohsiz)"
        log(f"--- id={post_id} {shortcode} | {head}")

        if args.dry_run:
            log("    [dry-run] yuklanmadi")
            done += 1
            continue

        vpath = None
        try:
            vpath = _download_hd_video_ytdlp(post_url)
            if not vpath:
                log("    XATO: videoni yuklab bo'lmadi (Instagram bloklagan bo'lishi mumkin)")
                continue

            size_mb = os.path.getsize(vpath) / 1024 / 1024
            log(f"    Yuklab olindi: {size_mb:.1f} MB")

            res = upload_video_to_youtube(
                vpath,
                caption=caption,
                post_url=post_url,
                privacy=args.privacy,
                is_shorts=True,
            )

            if res.get("success"):
                yt_url = res.get("url")
                mark_uploaded(conn, post_id, shortcode, yt_url, caption)
                done += 1
                log(f"    OK -> {yt_url}")
            else:
                err = res.get("error", "")
                if is_quota_error(err):
                    log("    KVOTA TUGADI. Bugungi limit ishlatildi.")
                    quota_hit = True
                    break
                log(f"    XATO: {err}")

        except Exception as e:
            if is_quota_error(e):
                log("    KVOTA TUGADI. Bugungi limit ishlatildi.")
                quota_hit = True
                break
            log(f"    KUTILMAGAN XATO: {e}")
        finally:
            if vpath and os.path.exists(vpath):
                try:
                    os.remove(vpath)
                except Exception:
                    pass

        time.sleep(3)  # API ni bosmaslik uchun kichik tanaffus

    conn.close()

    log(f"Yakun: {done} ta yuklandi, {max(total_left - done, 0)} ta qoldi.")
    if quota_hit:
        log("Kvota ertaga (Tinch okeani vaqti bilan 00:00) tiklanadi.")
    log("=" * 58)
    return 0


if __name__ == "__main__":
    sys.exit(main())
