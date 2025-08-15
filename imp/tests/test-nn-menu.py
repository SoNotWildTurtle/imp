import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "core" / "imp-nn-menu.py"

print("Checking neural manager CLI...")
output = subprocess.check_output(["python3", str(SCRIPT), "--register-basic", "--list"]).decode()
assert "basic" in output
print("Neural manager CLI Test Passed!")
