import json

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
LEARNING_FILE = BASE_DIR / "logs" / "imp-learning-memory.json"
STRATEGY_FILE = BASE_DIR / "logs" / "imp-strategy-plans.json"

def test_ai_learning():
    print("🔍 Testing AI Learning Memory...")
    try:
        with open(LEARNING_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data, list)
        print("✅ AI Learning Memory Test Passed!")
    except Exception as e:
        print(f"❌ AI Learning Memory Test Failed: {e}")

def test_strategy_generation():
    print("🔍 Testing AI Strategy Generator...")
    try:
        with open(STRATEGY_FILE, "r") as f:
            data = json.load(f)
        assert "strategy" in data
        print("✅ AI Strategy Generation Test Passed!")
    except Exception as e:
        print(f"❌ AI Strategy Generation Test Failed: {e}")

test_ai_learning()
test_strategy_generation()
