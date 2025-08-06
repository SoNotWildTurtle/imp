from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
HEALER_PATH = ROOT / 'self-improvement' / 'imp-self-healer.py'

spec = importlib.util.spec_from_file_location('healer', HEALER_PATH)
healer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(healer)

if __name__ == '__main__':
    healer.auto_verify_and_heal()
