import os
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

VT_API_KEY = os.getenv("VT_API_KEY")

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def check_virustotal(sha256):
    url = f"https://www.virustotal.com/api/v3/files/{sha256}"
    headers = {"x-apikey": VT_API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        stats = data["data"]["attributes"]["last_analysis_stats"]
        malicious = stats["malicious"]
        undetected = stats["undetected"]
        print(f"  Malicious: {malicious} | Undetected: {undetected}")
        if malicious > 0:
            return "MALICIOUS"
        return "CLEAN"
    elif response.status_code == 404:
        print(f"  Not found in VirusTotal database")
        return "NOT FOUND"
    else:
        print(f"  Error: {response.status_code}")
        return "ERROR"

def scan_and_check():
    SCAN_DIRS = [
        "C:\\Program Files",
        "C:\\Program Files (x86)",
    ]
    
    checked = 0
    for directory in SCAN_DIRS:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".exe"):
                    full_path = os.path.join(root, file)
                    try:
                        h = hash_file(full_path)
                        print(f"\n{file}")
                        result = check_virustotal(h)
                        print(f"  Status: {result}")
                        checked += 1
                        if checked >= 10:
                            print("\nStopped after 10 files (free API limit)")
                            return
                    except (PermissionError, OSError):
                        pass

scan_and_check()