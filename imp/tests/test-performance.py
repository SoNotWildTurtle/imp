import os
import json

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PERFORMANCE_LOG = BASE_DIR / "logs" / "imp-performance.json"

def test_system_performance():
    print("📊 Running Performance Test...")
    
    
    with open(PERFORMANCE_LOG, "r") as f:
        data = json.load(f)

    cpu = int(str(data["CPU Usage (%)"]).replace("%", ""))
    mem = int(str(data["Memory Usage (%)"]).replace("%", ""))
    assert cpu < 85, "⚠️ CPU Usage Too High!"
    assert mem < 90, "⚠️ Memory Usage Too High!"
    
    print("✅ System Performance Test Passed!")

test_system_performance()
