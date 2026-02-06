import time
from app.services.detector import get_live_stream_url, capture_live_frame, analyze_frame

# SETTINGS
TARGET_URL = "https://www.youtube.com/watch?v=VzIReBHx584&t=5s" # Change this to your live link
SCAN_INTERVAL = 60 # Seconds between each scan

def run_sentinel():
    print(f"🚀 Sentinel Defense Hub: Automatic Mode Started")
    print(f"Target: {TARGET_URL}")
    print("-" * 30)

    while True:
        try:
            # 1. Get the raw stream
            stream_url = get_live_stream_url(TARGET_URL)
            
            # 2. Capture a frame
            if stream_url:
                frame_path = capture_live_frame(stream_url)
                
                # 3. Analyze the frame
                if frame_path:
                    result = analyze_frame(frame_path)
                    print(f"[{time.strftime('%H:%M:%S')}] Analysis Result: {result}")
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] ❌ Failed to capture frame.")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] ❌ Could not extract stream URL.")

        except Exception as e:
            print(f"⚠️ Critical Error: {e}")

        print(f"Waiting {SCAN_INTERVAL} seconds for next scan...")
        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    run_sentinel()