import os
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

SCAN_DIRS = [
    "C:\\Program Files",
    "C:\\Program Files (x86)",
]

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def check_reputation(sha256, app_name):
    url = f"{SUPABASE_URL}/rest/v1/hash_reputation?sha256=eq.{sha256}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    if data:
        return data[0]["trust_status"]
    else:
        new_entry = {
            "sha256": sha256,
            "app_name": app_name,
            "trust_status": "unknown"
        }
        result = requests.post(f"{SUPABASE_URL}/rest/v1/hash_reputation", json=new_entry, headers=HEADERS)
        print(f"Insert status: {result.status_code} - {result.text}")
        return "unknown"

def scan():
    for directory in SCAN_DIRS:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".exe"):
                    full_path = os.path.join(root, file)
                    try:
                        h = hash_file(full_path)
                        status = check_reputation(h, file)
                        print(f"[{status.upper()}] {file}: {h}")
                    except (PermissionError, OSError):
                        pass

scan()