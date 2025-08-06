import requests
import json
import hashlib
from pathlib import Path
from datetime import datetime

BASE_URL = "https://world-api-stillness.live.tech.evefrontier.com/v2/solarsystems"  # Replace with actual API
LIMIT = 1000
OUTPUT_FILE = Path("universe_data.json")
BACKUP_DIR = Path("universe_backups")
BACKUP_DIR.mkdir(exist_ok=True)

def fetch_all_systems():
    systems = []
    offset = 0
    while True:
        print(f"Fetching {LIMIT} systems starting at offset {offset}...")
        resp = requests.get(BASE_URL, params={"limit": LIMIT, "offset": offset})
        resp.raise_for_status()
        data = resp.json()
        systems.extend(data["data"])
        meta = data.get("metadata", {})
        offset += LIMIT
        if offset >= meta.get("total", len(systems)):
            break
    return systems

def file_hash(path: Path):
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_json(path: Path):
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def summarize_changes(old_data, new_data):
    if old_data is None:
        return len(new_data), 0, 0  # New file
    
    old_ids = {s["id"] for s in old_data}
    new_ids = {s["id"] for s in new_data}
    
    added = len(new_ids - old_ids)
    removed = len(old_ids - new_ids)
    same = len(new_ids & old_ids)
    
    return added, removed, same

if __name__ == "__main__":
    new_systems = fetch_all_systems()
    new_json = json.dumps(new_systems, indent=2, ensure_ascii=False)
    
    old_data = load_json(OUTPUT_FILE)
    old_hash = file_hash(OUTPUT_FILE)
    new_hash = hashlib.sha256(new_json.encode("utf-8")).hexdigest()
    
    if new_hash == old_hash:
        print("No changes detected in universe data. Exiting.")
    else:
        added, removed, same = summarize_changes(old_data, new_systems)
        print(f"Universe data changed! Added: {added}, Removed: {removed}, Same: {same}")
        
        # Backup old file with timestamp
        if OUTPUT_FILE.exists():
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            backup_file = BACKUP_DIR / f"universe_data_{timestamp}.json"
            OUTPUT_FILE.replace(backup_file)
            print(f"Old file backed up to: {backup_file}")
        
        # Save new file
        OUTPUT_FILE.write_text(new_json, encoding="utf-8")
        
        # Commit summary
        Path("universe_update_summary.txt").write_text(
            f"Update universe data: +{added} / -{removed} / ~{same} systems\n",
            encoding="utf-8"
        )
