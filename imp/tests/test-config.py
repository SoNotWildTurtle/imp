import json

CONFIG_FILE = "/root/imp/config/imp-personality.json"

def test_ai_personality():
    print("🤖 Validating AI Personality Settings...")

    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)

    assert data["name"] == "IMP"
    assert "trusted_user" in data["user_interaction"]
    
    print("✅ AI Personality Test Passed!")

test_ai_personality()
