import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PERFORMANCE_LOG = os.path.join(BASE_DIR, "logs", "imp-performance.json")

def test_system_performance():
    print("📊 Running Performance Test...")
    
    os.system(f"python3 {os.path.join(BASE_DIR, 'logs', 'imp-log-manager.py')}")
    
    with open(PERFORMANCE_LOG, "r") as f:
        data = json.load(f)

    assert data["CPU Usage (%)"] < 85, "⚠️ CPU Usage Too High!"
    assert data["Memory Usage (%)"] < 90, "⚠️ Memory Usage Too High!"
    
    print("✅ System Performance Test Passed!")

test_system_performance()
