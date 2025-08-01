from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'core' / 'imp-motivation.py'
MOOD_FILE = ROOT / 'logs' / 'imp-mood.json'
GOAL_FILE = ROOT / 'logs' / 'imp-goals.json'

spec = importlib.util.spec_from_file_location('imp_motivation', MODULE)
mot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mot)

print('Testing Motivation Engine...')
MOOD_FILE.write_text('{"mood": -0.5}')
pre = json.loads(GOAL_FILE.read_text()) if GOAL_FILE.exists() else []
mot.generate_motivations()
post = json.loads(GOAL_FILE.read_text())
assert len(post) >= len(pre)
print('Motivation Test Executed!')

