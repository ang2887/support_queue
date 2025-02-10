# neon_kill_switch.py

import os
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()

NEON_API_KEY = os.getenv("NEON_API_KEY")
NEON_PROJECT_ID = os.getenv("NEON_PROJECT_ID")
KILL_SWITCH_THRESHOLD_STORAGE = 450  # 450MB (Neon free tier allows 500MB)
KILL_SWITCH_THRESHOLD_CPU = 0.2  # 0.2 Compute Units (Neon free tier allows 0.25)

def get_neon_usage():
    url = f"https://console.neon.tech/api/v1/projects/{NEON_PROJECT_ID}/stats"
    headers = {"Authorization": f"Bearer {NEON_API_KEY}"}

    response = requests.get(url, headers=headers)
    data = response.json()

    storage_used = data["storage"]["used_mb"]
    cpu_used = data["compute"]["used_units"]

    return storage_used, cpu_used

def pause_neon_db():
    url = f"https://console.neon.tech/api/v1/projects/{NEON_PROJECT_ID}/pause"
    headers = {"Authorization": f"Bearer {NEON_API_KEY}"}

    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print("🛑 Neon database paused successfully.")
    else:
        print("❌ Failed to pause Neon database.")

def check_and_kill():
    storage_used, cpu_used = get_neon_usage()
    print(f"📊 Storage: {storage_used}MB | CPU: {cpu_used} CU")

    if storage_used > KILL_SWITCH_THRESHOLD_STORAGE or cpu_used > KILL_SWITCH_THRESHOLD_CPU:
        print("🚨 Kill switch activated: Pausing Neon database...")
        pause_neon_db()
    else:
        print("✅ Resource usage is within limits.")

if __name__ == "__main__":
    check_and_kill()