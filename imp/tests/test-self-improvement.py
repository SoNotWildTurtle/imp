import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPDATE_LOG = os.path.join(BASE_DIR, "logs", "imp-update-log.json")

def test_code_updates():
    print("🔄 Checking Code Updates...")
    
    with open(UPDATE_LOG, "r") as f:
        updates = json.load(f)

    assert len(updates) > 0, "⚠️ No recent updates detected!"
    
    print("✅ Code Update Test Passed!")

test_code_updates()
