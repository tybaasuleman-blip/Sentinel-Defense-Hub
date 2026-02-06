import time
import os
from app.services.detector import get_live_stream_url, capture_live_frame, analyze_frame, send_daily_brief

TARGET_URL = "https://www.youtube.com/watch?v=c-DsgAXWWnc"
last_brief_date = ""

def start_mission():
    global last_brief_date
    print("\n" + "="*50)
    print("🛰️  SENTINEL HUB v3.1 - INTELLIGENCE MODE")
    print("="*50 + "\n")

    while True:
        current_time = time.strftime("%H:%M")
        current_date = time.strftime("%Y-%m-%d")

        # 🧪 MANUAL TEST TRIGGER
        # If you create a file named 'test_now.txt' in your folder, it will trigger the brief!
        if os.path.exists("test_now.txt"):
            print("🧪 Manual Test Triggered! Generating Brief...")
            send_daily_brief()
            os.remove("test_now.txt") # Remove the file so it doesn't loop

        # 🕛 AUTOMATIC MIDNIGHT BRIEF
        if current_time == "00:00" and current_date != last_brief_date:
            print("📦 Midnight reached. Dispatching Daily Brief...")
            send_daily_brief()
            last_brief_date = current_date

        # 📡 NORMAL LIVE SCANNING
        try:
            stream_link = get_live_stream_url(TARGET_URL)
            if stream_link:
                img = capture_live_frame(stream_link)
                if img:
                    analyze_frame(img)
        except Exception as e:
            print(f"⚠️ Pulse Error: {e}")
        
        time.sleep(20)

if __name__ == "__main__":
    start_mission()