"""Fetch public team artifacts and verify bytes against the committed manifest."""
from pathlib import Path
import hashlib
import json
import os
import requests

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "data_manifest.json").read_text())
folder = Path(os.environ.get("SWAN_DATA_DIR", root / "raw_data"))
folder.mkdir(parents=True, exist_ok=True)
for name, record in manifest["files"].items():
    target = folder / name
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == record["sha256"]:
        print("Verified", name)
        continue
    response = requests.get("https://drive.google.com/uc", params={"export": "download", "id": record["drive_id"]}, timeout=30)
    response.raise_for_status()
    if hashlib.sha256(response.content).hexdigest() != record["sha256"]:
        raise ValueError("Artifact checksum mismatch: " + name + "; check Drive access/version")
    temporary = target.with_suffix(".download")
    temporary.write_bytes(response.content)
    temporary.replace(target)
    print("Downloaded and verified", name)
