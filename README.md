\Open `README.md` in VS Code and replace everything with this:

```
# App Integrity Scanner

A lightweight Windows security tool that monitors installed applications for unauthorized changes using file hashing, cloud reputation checks, and real-time threat intelligence.

## What it does
- Scans Program Files for installed executables
- Generates SHA-256 fingerprints for each application
- Checks hashes against a Supabase cloud database for reputation status
- Detects unauthorized file modifications between scans using snapshot comparison
- Queries VirusTotal's threat intelligence API to check files against 70+ antivirus engines

## Tech Stack
- Python
- Supabase (PostgreSQL cloud database)
- VirusTotal API
- SHA-256 cryptographic hashing

## How to Run

Install dependencies:
```
python -m pip install requests python-dotenv
```

Create a `.env` file with your keys:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
VT_API_KEY=your_virustotal_key
```

Run the scanner:
```
python scanner.py
```

Run integrity monitor:
```
python monitor.py
```

Run VirusTotal check:
```
python virustotal.py
```

## Project Phases
- Phase 1: Application enumeration and SHA-256 hashing ✅
- Phase 2: Supabase cloud reputation lookup ✅
- Phase 3: Snapshot based integrity monitoring and change detection ✅
- Phase 4: VirusTotal threat intelligence integration ✅
```

