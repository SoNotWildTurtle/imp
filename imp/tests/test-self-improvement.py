import json

UPDATE_LOG = "/root/imp/logs/imp-update-log.json"

def test_code_updates():
    print("🔄 Checking Code Updates...")
    
    with open(UPDATE_LOG, "r") as f:
        updates = json.load(f)

    assert len(updates) > 0, "⚠️ No recent updates detected!"
    
    print("✅ Code Update Test Passed!")

test_code_updates()
