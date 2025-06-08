import os
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEBASE_PATH = str(ROOT) + "/"
VERSION_LOG = ROOT / "logs" / "imp-version-log.json"

def list_existing_code():
    return [f for f in os.listdir(CODEBASE_PATH) if f.endswith(".py")]

def test_code_integrity():
    files = list_existing_code()
    for file in files:
        result = subprocess.run(f"python3 -m py_compile {os.path.join(CODEBASE_PATH, file)}", shell=True)
        if result.returncode != 0:
            print(f"⚠️ Code integrity test failed for {file}. Rolling back...")
            os.rename(os.path.join(CODEBASE_PATH, f"{file}.backup"), os.path.join(CODEBASE_PATH, file))

def track_versions():
    versions = []
    if os.path.exists(VERSION_LOG):
        with open(VERSION_LOG, "r") as f:
            versions = json.load(f)

    new_version = {"timestamp": time.ctime(), "files": list_existing_code()}
    versions.append(new_version)

    with open(VERSION_LOG, "w") as f:
        json.dump(versions, f, indent=4)

if __name__ == "__main__":
    test_code_integrity()
    track_versions()
