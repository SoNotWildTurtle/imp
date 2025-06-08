import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILE = ROOT / "config" / "imp-personality.json"

def test_ai_personality():
    print("🤖 Validating AI Personality Settings...")

    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)

    assert data["name"] == "IMP"
    assert "trusted_user" in data["user_interaction"]
    
    print("✅ AI Personality Test Passed!")

test_ai_personality()
