# ============================================================
#  run_pc_bridge.py
#  ATLAS Realtime PC Bridge Standalone Agent (Windows Host)
# ============================================================

import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()

from services.pc_control.bridge import start_pc_bridge_daemon, collect_local_pc_metrics

if __name__ == "__main__":
    print("=" * 60)
    print("  💻 ATLAS Universal — Realtime PC Bridge Agent")
    print("  Vercel Web Platformasi <===> Mahalliy Windows PC")
    print("=" * 60)
    
    metrics = collect_local_pc_metrics()
    print(f"✅ Kompyuter: {metrics.get('hostname')}")
    print(f"✅ CPU: {metrics.get('cpu_percent')}% | RAM: {metrics.get('ram_used_gb')}/{metrics.get('ram_total_gb')} GB")
    print(f"✅ Disks: {len(metrics.get('disks', []))} ta disk aniqlandi")
    print("\n🟢 Realtime Cloud Bridge faollashtirilmoqda...")
    
    start_pc_bridge_daemon()
    
    print("🚀 Bridge muvaffaqiyatli ishga tushdi!")
    print("💡 Endi Vercel platformasida (atlas-my-tools.vercel.app) istalgan buyruqni bosing.")
    print("Ushbu konsol oynasini yopmang (fonda ishlab turadi).\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Bridge to'xtatildi.")
