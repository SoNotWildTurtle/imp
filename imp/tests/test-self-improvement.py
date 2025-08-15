import sys
import json
import subprocess

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
UPDATE_LOG = BASE_DIR / "logs" / "imp-update-log.json"
EVOLUTION_PLAN = BASE_DIR / "logs" / "imp-evolution-plan.json"

def test_code_updates():
    print("🔄 Checking Code Updates...")
    
    with open(UPDATE_LOG, "r") as f:
        updates = json.load(f)

    assert len(updates) > 0, "⚠️ No recent updates detected!"

    print("✅ Code Update Test Passed!")

def test_evolution_plan():
    print("🔄 Checking Evolution Plan...")
    with open(EVOLUTION_PLAN, "r") as f:
        plan = json.load(f)
    assert "plan" in plan
    print("✅ Evolution Plan Test Passed!")


def test_self_healer():
    log_file = BASE_DIR / "logs" / "imp-healing-log.json"
    with open(log_file, "r") as f:
        before = len(json.load(f))
    subprocess.run([sys.executable, str(BASE_DIR / "self-improvement" / "imp-self-healer.py")])
    with open(log_file, "r") as f:
        after = len(json.load(f))
    assert after == before + 1
    print("✅ Self Healer Test Passed!")

test_code_updates()
test_evolution_plan()
test_self_healer()
