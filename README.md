# app-integrity-scanner
# App Integrity Scanner

A lightweight Windows security tool that scans installed applications, generates SHA-256 hashes, and monitors for unexpected file changes.

## Purpose
Built to detect unauthorized modifications to installed executables. Focuses on file integrity and reputation checking without the overhead of a full antivirus engine.

## How to Run
python scanner.py

## Features
- Scans Program Files for installed executables
- Generates SHA-256 fingerprints for each application
- (Coming soon) Cloud reputation lookups
- (Coming soon) Scheduled integrity monitoring

## Roadmap
- Phase 1: Application enumeration and hashing ✅
- Phase 2: Cloud backend and reputation checks
- Phase 3: Scheduled integrity monitoring
- Phase 4: VirusTotal integration
