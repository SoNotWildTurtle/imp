import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERFORMANCE_LOG = ROOT / "logs" / "imp-performance.json"

def test_system_performance():
    print("📊 Running Performance Test...")
    
    # Load performance metrics without running the interactive log manager
    with open(PERFORMANCE_LOG, "r") as f:
        data = json.load(f)

    cpu = int(str(data["CPU Usage (%)"]).rstrip("%"))
    mem = int(str(data["Memory Usage (%)"]).rstrip("%"))

    assert cpu < 85, "⚠️ CPU Usage Too High!"
    assert mem < 90, "⚠️ Memory Usage Too High!"
    
    print("✅ System Performance Test Passed!")

test_system_performance()
