#first thing we are building for this scanner is fairly simple: just find .exe files and hash them
import os
import hashlib

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

def scan():
    results = []
    for directory in SCAN_DIRS:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".exe"):
                    full_path = os.path.join(root, file)
                    try:
                        h = hash_file(full_path)
                        results.append({"name": file, "path": full_path, "sha256": h})
                        print(f"{file}: {h}")
                    except (PermissionError, OSError):
                        pass
    return results

scan()