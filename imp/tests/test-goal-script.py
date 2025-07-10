from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "bin" / "imp-goal.sh"

print("Testing goal script...")
assert SCRIPT.exists(), "imp-goal.sh missing"

# Listing goals should not error
subprocess.run([str(SCRIPT), 'list'], check=True)
print("Goal script test passed!")
