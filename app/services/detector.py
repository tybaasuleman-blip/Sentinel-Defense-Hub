import yt_dlp
import cv2
import numpy as np
import os
import time
import requests
import json
from datetime import datetime

# CONFIG
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1469417372380041338/nY2YwuResfUTYEfqhSp4Rh_wO9mC8_yFcdEIwlFKPeFOTnJ6rF0xBxnkJu_m0g0d_Fcq"
STATS_FILE = "data/stats.json"
ALERT_COOLDOWN = 120 
last_alert_time = 0

def get_live_stream_url(url):
    ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info.get('url')
        except: return None

def capture_live_frame(stream_url):
    save_path = "data/input/live_frame.jpg"
    os.makedirs("data/input", exist_ok=True)
    cap = cv2.VideoCapture(stream_url)
    for _ in range(15): cap.grab()
    success, frame = cap.read()
    if success:
        cv2.imwrite(save_path, frame)
        cap.release()
        return save_path
    cap.release()
    return None

def update_stats(intensity):
    os.makedirs("data", exist_ok=True)
    stats = {"total_alerts": 0, "peak_intensity": 0, "last_reset": str(datetime.now().date()), "hourly_data": {}}
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f: stats = json.load(f)
    stats["total_alerts"] += 1
    stats["peak_intensity"] = max(stats["peak_intensity"], intensity)
    hour = str(datetime.now().hour)
    stats["hourly_data"][hour] = stats["hourly_data"].get(hour, 0) + 1
    with open(STATS_FILE, 'w') as f: json.dump(stats, f)

def send_daily_brief():
    if not os.path.exists(STATS_FILE): return
    with open(STATS_FILE, 'r') as f: data = json.load(f)
    report = f"📋 **STRATEGIC DAILY BRIEF**\n🚨 Alerts: `{data['total_alerts']}`\n📈 Peak: `{data['peak_intensity']}`"
    requests.post(DISCORD_WEBHOOK_URL, json={"content": report})
    os.remove(STATS_FILE)

def analyze_frame(image_path):
    global last_alert_time
    img = cv2.imread(image_path)
    if img is None: return "Error"
    hsv = cv2.cvtColor(img[0:int(img.shape[0]*0.7), :], cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([0, 90, 120]), np.array([35, 255, 255]))
    intensity = cv2.countNonZero(mask)
    print(f"📊 SCAN | Intensity: {intensity}")
    if intensity > 1500:
        update_stats(intensity)
        if (time.time() - last_alert_time) > ALERT_COOLDOWN:
            requests.post(DISCORD_WEBHOOK_URL, data={"content": f"🚨 Alert: {intensity}"}, files={"file": open(image_path, "rb")})
            last_alert_time = time.time()
    return "Processed"