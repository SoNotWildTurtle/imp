import sys
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "imp-offline-evolution.json"
SKILL_FILE = BASE_DIR / "logs" / "imp-gi-skills.json"
PERF_FILE = BASE_DIR / "logs" / "imp-gi-performance.json"
INSIGHTS_FILE = BASE_DIR / "logs" / "imp-conversation-insights.json"
SCRIPT = BASE_DIR / "self-improvement" / "imp-offline-evolver.py"


def write_sample_logs():
    with open(SKILL_FILE, "w") as f:
        json.dump([
            {"timestamp": "2024", "name": "test", "skill": "python"}
        ], f)
    with open(PERF_FILE, "w") as f:
        json.dump([
            {"timestamp": "2024", "name": "test", "cpu": 50, "memory": 40}
        ], f)
    with open(INSIGHTS_FILE, "w") as f:
        json.dump([
            {"timestamp": "2024", "top_words": [["python", 5], ["security", 3]]}
        ], f)


def test_offline_evolver():
    write_sample_logs()
    before = 0
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            before = len(json.load(f))
    subprocess.run([sys.executable, str(SCRIPT)], check=True)
    with open(LOG_FILE, "r") as f:
        data = json.load(f)
    after = len(data)
    entry = data[-1]
    assert after == before + 1
    assert entry["avg_cpu"] == 50
    assert "security" in entry.get("suggested_skills", [])
    print("✅ Offline Evolver Test Passed!")


test_offline_evolver()
