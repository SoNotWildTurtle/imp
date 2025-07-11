from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "core" / "imp-adaptive-planner.py"
PLAN_FILE = ROOT / "logs" / "imp-strategy-plans.json"

# Ensure plan file exists for test
PLAN_FILE.write_text("[]")

spec = importlib.util.spec_from_file_location("imp_adaptive_planner", MODULE_PATH)
planner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(planner)

print("Testing adaptive planner...")
plan = planner.build_plan("Improve security and optimize performance.")
planner.save_plan(plan)

assert isinstance(plan, list) and len(plan) > 0
for item in plan:
    assert 0 <= item["weight"] <= 1
print("Adaptive planner test passed!")
