# ============================================================
#  run_pc_bridge.py
#  ATLAS Realtime PC Bridge Standalone Agent (Windows Host)
# ============================================================

import os
import sys
import time

# .env faylidan kalitlarni yuklash
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from services.pc_control.bridge import (
    start_pc_bridge_daemon,
    collect_local_pc_metrics,
    _push_heartbeat_sync
)

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    print("=" * 60)
    print("  ATLAS Universal -- Realtime PC Bridge Agent")
    print("  Vercel Web Platformasi <===> Mahalliy Windows PC")
    print("=" * 60)

    metrics = collect_local_pc_metrics()
    hostname = metrics.get('hostname', 'Windows-PC')
    cpu = metrics.get('cpu_percent', 0)
    ram_used = metrics.get('ram_used_gb', 0)
    ram_total = metrics.get('ram_total_gb', 0)
    disks = len(metrics.get('disks', []))

    print(f"[OK] Kompyuter: {hostname}")
    print(f"[OK] CPU: {cpu}% | RAM: {ram_used}/{ram_total} GB")
    print(f"[OK] Disks: {disks} ta disk aniqlandi")
    print("\n[START] Realtime Cloud Bridge faollashtirilmoqda...")

    start_pc_bridge_daemon()
    _push_heartbeat_sync(metrics)

    print("[OK] Bridge muvaffaqiyatli ishga tushdi!")
    print("[INFO] Endi Vercel platformasida (atlas-my-tools.vercel.app) istalgan buyruqni bosing.")
    print("[INFO] Ushbu konsol oynasini yopmang (fonda ishlab turadi).")
    print("-" * 60)

    counter = 0
    try:
        while True:
            time.sleep(5)
            counter += 1
            if counter % 6 == 0:  # Har 30 soniyada
                m = collect_local_pc_metrics()
                print(f"[ALIVE] CPU:{m.get('cpu_percent',0)}% RAM:{m.get('ram_percent',0)}% | Bridge ishlamoqda...")
    except KeyboardInterrupt:
        print("\n[STOP] Bridge to'xtatildi.")
