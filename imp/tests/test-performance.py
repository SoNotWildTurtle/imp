import os
import json

PERFORMANCE_LOG = "/root/imp/logs/imp-performance.json"

def test_system_performance():
    print("📊 Running Performance Test...")
    
    os.system("python3 /root/imp/logs/imp-log-manager.py")
    
    with open(PERFORMANCE_LOG, "r") as f:
        data = json.load(f)

    assert data["CPU Usage (%)"] < 85, "⚠️ CPU Usage Too High!"
    assert data["Memory Usage (%)"] < 90, "⚠️ Memory Usage Too High!"
    
    print("✅ System Performance Test Passed!")

test_system_performance()
