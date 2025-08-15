from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'bin' / 'imp-mood.sh'

print('Testing Mood CLI...')
result = subprocess.run([str(SCRIPT), '--get'], capture_output=True, text=True)
assert result.returncode == 0
print('Mood CLI Test Executed!')

