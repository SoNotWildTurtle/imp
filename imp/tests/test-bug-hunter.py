from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
BUG_HUNTER = ROOT / "self-improvement" / "imp-bug-hunter.py"
BUG_LOG = ROOT / "logs" / "imp-bug-report.json"

spec = importlib.util.spec_from_file_location("bug_hunter", BUG_HUNTER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

print("Running Bug Hunter...")
module.scan_repository()

assert BUG_LOG.exists(), "Bug report not generated"
with open(BUG_LOG, "r") as f:
    json.load(f)
print("Bug Hunter Test Passed!")
