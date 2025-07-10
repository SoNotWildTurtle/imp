from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'core' / 'imp-voice.py'

print('Testing Voice Synthesis...')
subprocess.run(f"python3 {SCRIPT} 'test phrase'", shell=True, check=False)
print('Voice Synthesis Test Executed!')
