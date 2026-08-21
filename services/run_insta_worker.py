import sys
import time
import os

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from services.insta_poster_service import init_insta_tables, get_queue_stats
from services.insta_scheduler import start_insta_scheduler
from services.insta_bot_listener import start_insta_bot_listener

if __name__ == "__main__":
    print("==================================================")
    print("ATLAS Instagram AutoPoster & Like Listener Faol")
    print("==================================================")
    
    init_insta_tables()
    start_insta_scheduler()
    start_insta_bot_listener()
    
    stats = get_queue_stats()
    print(f"Navbat holati: Jami={stats['total']}, Kutilmoqda={stats['pending']}, Yuborildi={stats['sent']}")
    print("Bot fon rejimida Like bosishlar va jadvalni tinglamoqda...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("To'xtatildi.")
