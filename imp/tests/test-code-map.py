from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "self-improvement" / "imp-code-map.py"
LOG = ROOT / "logs" / "imp-code-map.json"

spec = importlib.util.spec_from_file_location("code_map", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

print("Generating code map...")
path = module.generate_code_map()

assert path == LOG and path.exists(), "Code map log missing"
with open(path, "r") as f:
    data = json.load(f)
    assert "imp/core/imp-execute.py" in data, "imp-execute missing from code map"
print("Code Map Test Passed!")
