from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'core' / 'imp-speech-to-text.py'

print('Testing Speech-to-Text...')
subprocess.run(f"python3 {SCRIPT} --check --offline", shell=True, check=False)
print('Speech-to-Text Test Executed!')
