import os
import json
import hashlib
import datetime

SCAN_DIRS = [
    "C:\\Program Files",
    "C:\\Program Files (x86)",
]

SNAPSHOT_FILE = "snapshot.json"

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def take_snapshot():
    snapshot = {}
    for directory in SCAN_DIRS:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".exe"):
                    full_path = os.path.join(root, file)
                    try:
                        h = hash_file(full_path)
                        snapshot[full_path] = h
                    except (PermissionError, OSError):
                        pass
    return snapshot

def save_snapshot(snapshot):
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(snapshot, f, indent=2)
    print(f"Snapshot saved — {len(snapshot)} files recorded.")

def load_snapshot():
    if not os.path.exists(SNAPSHOT_FILE):
        return None
    with open(SNAPSHOT_FILE, "r") as f:
        return json.load(f)

def compare_snapshots(old, new):
    alerts = []
    for path, new_hash in new.items():
        if path in old:
            if old[path] != new_hash:
                alerts.append(f"[ALERT] Hash changed: {os.path.basename(path)}")
        else:
            alerts.append(f"[NEW] New executable found: {os.path.basename(path)}")
    return alerts

def run():
    print(f"\n--- Scan started {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    old_snapshot = load_snapshot()
    new_snapshot = take_snapshot()

    if old_snapshot is None:
        print("No previous snapshot found — saving baseline now.")
        save_snapshot(new_snapshot)
    else:
        alerts = compare_snapshots(old_snapshot, new_snapshot)
        save_snapshot(new_snapshot)
        if alerts:
            print("\n⚠ Changes detected:")
            for alert in alerts:
                print(alert)
        else:
            print("✓ All files match previous snapshot. No changes detected.")

run()