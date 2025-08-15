from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'self-improvement' / 'imp-auto-heal.py'

spec = importlib.util.spec_from_file_location('auto_heal', MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

print('Running Auto Heal...')
mod.healer.auto_verify_and_heal()
print('Auto Heal Test Passed!')
